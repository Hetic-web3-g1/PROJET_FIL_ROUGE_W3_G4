import React, {useState, useContext, useMemo, useEffect } from 'react'

import { Document, Page } from 'react-pdf';
import { ReactReduxContext } from 'react-redux'

import { Button } from '../../button/Button'
import { UploadCard } from '../../upload/UploadCard'
import { useToast } from '../../../utils/toast';
import Field from '../../field/Field'

import './DashboardPartition.css'

export const DashboardPartition = ({partitionData, masterclassData, handleSave}) => {

    const { store } = useContext(ReactReduxContext)
    const [uploadPartition, setUploadPartition] = useState();
    const [partition, setPartition] = useState();   
    const [numPages, setNumPages] = useState(null);
    const [annotations, setAnnotations] = React.useState([]);
    const [tmpAnnotation, setTmpAnnotation] = React.useState({'text': '', 'line': ''});
    const [observable, setObservable] = React.useState(0);
    const toast = useToast();

    /**
     * GET the different annotations of the partition
     */
    useEffect(() => {
        setAnnotations([]);
        const Options = {
          method: 'GET',
          headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/annotations/annotation/partition/${masterclassData.partition_id}`, Options).then((response) => response.json()).then(data => {
          setAnnotations(data.map(e => ({
            text: e.content,
            line: e.measure
          })));
        });
      }, []);

    /**
     * Set the partition id to the masterclass
     * @param {number} id Partition id
     */
    const handleSaveId = (id) => {
        var newMasterclassData = masterclassData
        newMasterclassData.partition_id = id
        newMasterclassData.updated_by = store?.getState().user.user_id
        newMasterclassData.updated_at = new Date()
        handleSave(newMasterclassData)
    }

    /**
     * Save the partition
     * @param {MouseEvent} e 
     */
    const handlePartitionUpload = (e) => {
        e.preventDefault();
        const fileBlob = new Blob([uploadPartition], {type: 'application/pdf'});
        var formData = new FormData();
        formData.append('public', true);
        formData.append('file', fileBlob, "partition.pdf");
        const uploadOptions = {
            method: 'POST',
            headers: { 'authorization': `${store.getState().user.user_token}` },
            body: formData,
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/partitions/partition`, uploadOptions).then((response) => response.json()).then(data => {
            handleSaveId(data);
        })
    }

    /**
     * On document load set the total pages of PDF file
     */
    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    /**
     * Add a new annotation line
     */
    function handleAddLine() {
        if (tmpAnnotation.text !== '' && tmpAnnotation.line !== '') {
            setAnnotations([...annotations, tmpAnnotation]);    
            setTmpAnnotation({'text': '', 'line': ''});
        }
    }

    /**
     * Delete PDF file
     */
    const handleFileDelete = () => {
        const Options = {
            method: 'DELETE',
            headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/partitions/partition/${masterclassData.partition_id}`, Options).then((response) => response.json()).then(data => {
        });
    }

    useMemo(() => {
        if(partitionData?.s3_object_id !== undefined) {
            const Options = {
            method: 'GET',
            headers:  { 'Content-Type': 'video/mp4', 'accept': 'video/mp4', 'authorization': `${store.getState().user.user_token}`},
            };
            fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/s3_objects/url_and_object_info/${partitionData.s3_object_id}`, Options).then((response) => response.json()).then(data => {
                setPartition(data)
            });
        }
    },[]);

    const file = useMemo(() => (partition?.url), [partition?.url]); // trick to avoid the PDF to reload when annotation value change

    /**
     * On click save all the annotations
     * @param {MouseEvent} event 
     */
    const handleSaveAnnotations = (event) => {
        event.preventDefault();
        
        annotations.map((annotation) => {

            var formattedBody = {
                partition_id: masterclassData.partition_id,
                measure: Number(annotation.line),
                content: annotation.text
            }

            const addAnnotation = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
                body: JSON.stringify(formattedBody),
            };
            fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/annotations/annotation`, addAnnotation).then((response) => response.json()).then(data => {
                data == null ? toast.open({message: 'Annotation(s) saved !', type: 'success'}) : toast.open({message: 'An error occurred', type: 'failure'});
            });
        })
        setObservable(observable + 1);
    }

    return(
        <div className={partition ? `partition-container` : null}>
            <div style={!file ? {display: 'none'} : null} className='annotations-container'>
                <h2>Annotations</h2>
                {
                    annotations.map((annotation, index) => {
                        return(
                            <div key={index} className='annotation-field'>
                                <img src={'../../src/assets/partitions/music-note.svg'} alt="plus" style={{marginRight: '1vw'}}/>
                                <div key={index} style={{marginRight: '10px'}}><Field value={annotation.line} type={'number'} placeholder="Line" onChange={e => 
                                    {
                                        let Array = [...annotations];
                                        Array[index].line = e.target.value;
                                        setAnnotations(Array);
                                    }
                                }/>
                                </div>
                                <Field placeholder="Annotation" value={annotation.text} onChange={e =>
                                    {
                                        let Array = [...annotations];
                                        Array[index].text = e.target.value;
                                        setAnnotations(Array);
                                    }
                                }/>
                            </div>
                        )
                    })
                }
                    <div className='modal-bio-prof-infos-field-add'>
                        <img src={'../../src/assets/partitions/music-note.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}}/>
                        <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={handleAddLine}/>
                        <div style={{marginRight: '10px'}}><Field value={tmpAnnotation.line} onChange={(e) => setTmpAnnotation({...tmpAnnotation, 'line': e.target.value})} type={'number'} placeholder="Line"/></div>
                        <Field value={tmpAnnotation.text} placeholder="Annotation" onChange={(e) => setTmpAnnotation({...tmpAnnotation, 'text': e.target.value})}/>
                    </div>

                    <div className='save-annotation-container'>
                        <Button label={"Save"} onClick={(e) => handleSaveAnnotations(e)}/>
                    </div>

            </div>
            
            <div>
                {partitionData?.status ? (
                    <div className='dashboard-partition'>
                        <div className='upload-file-pdf' style={{textAlign: 'center'}}>
                            <button type="button" className='btn' onClick={handleFileDelete}>
                                Delete
                            </button>
                        </div>
                        <Document className="pdf-container-partition" file={file} onLoadError={console.error} onLoadSuccess={onDocumentLoadSuccess}>
                            {Array.apply(null, Array(numPages))
                            .map((x, i)=>i+1)
                            .map(page => <Page pageNumber={page} renderTextLayer={false} renderAnnotationLayer={false}/>)}
                        </Document>
                    </div>    
                    ) : (
                    <div className="dashboard-partition-missing">
                        <div className='dashboard-Partition-missing-title'>
                            No Partition Uploaded yet ...
                        </div>
                        <div className='dashboard-partition-missing-upload-card'>
                            <UploadCard setUploadFile={setUploadPartition}/>
                        </div>
                        <div>
                            <Button label={"Save"} onClick={(e) => handlePartitionUpload(e)}/>
                        </div>
                    </div>
                    )
                }
            </div>
        </div>
    );
}

export default DashboardPartition;
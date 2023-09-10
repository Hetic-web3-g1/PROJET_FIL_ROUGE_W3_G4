import React, {useState, useContext, useEffect } from 'react'
import { ReactReduxContext } from 'react-redux'

import { Document, Page } from 'react-pdf';

import { UploadCard } from '../../upload/UploadCard'
import { Button } from '../../button/Button'
import './DashboardPartition.css'

export const DashboardPartition = ({partitionData, masterclassData, handleSave}) => {

    const { store } = useContext(ReactReduxContext)
    const [uploadPartition, setUploadPartition] = useState();
    const [partition, setPartition] = useState();   
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1); 

    const handleSaveId = (id) => {
        var newMasterclassData = masterclassData
        newMasterclassData.partition_id = id
        newMasterclassData.updated_by = store?.getState().user.user_id
        newMasterclassData.updated_at = new Date()
        handleSave(newMasterclassData)
    }

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

    function onDocumentLoadSuccess({ numPages }) {
        setPageNumber(1);
        setNumPages(numPages);
    }

    function changePage(offset) {
        setPageNumber(prevPageNumber => prevPageNumber + offset);
    }

    function previousPage() {
        changePage(-1);
    }
    
    function nextPage() {
        changePage(1);
    }

    const handleFileDelete = () => {
        console.log('delete tmp')
    }

    useEffect(() => {
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

    return(
        <div>
            {partitionData?.status ? (
                <div className='dashboard-partition'>
                    <div className='upload-file-pdf' style={{textAlign: 'center'}}>
                        <p style={{textAlign: 'center'}}>
                            Page {pageNumber} of {numPages}
                        </p>

                        <button style={{marginRight: '10px'}} type="button" className='btn' disabled={pageNumber <= 1} onClick={previousPage}>
                            Previous
                        </button>

                        <button style={{marginRight: '10px'}} type="button" className='btn' disabled={pageNumber >= numPages} onClick={nextPage}>
                            Next
                        </button>

                        <button type="button" className='btn' onClick={handleFileDelete}>
                            Delete
                        </button>
                    </div>
                    <Document className="pdf-container" file={{url:`${partition?.url}`}} onLoadError={console.error} onLoadSuccess={onDocumentLoadSuccess} >
                        <Page pageNumber={pageNumber} renderTextLayer={false} renderAnnotationLayer={false}/>
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
                        <Button label={"Upload"} onClick={(e) => handlePartitionUpload(e)}/>
                    </div>
                </div>
                )
            }
        </div>
    );
}

export default DashboardPartition;
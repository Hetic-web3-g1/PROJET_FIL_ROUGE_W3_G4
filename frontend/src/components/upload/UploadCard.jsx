import React, {useState} from 'react'
import { Document, Page } from 'react-pdf';

import './uploadCard.css'
import Divider from '../divider/Divider'
import VideoPlayer from '../videoPlayer/VideoPlayer';

const pdfjs = await import('pdfjs-dist/build/pdf');
const pdfjsWorker = await import('pdfjs-dist/build/pdf.worker.entry');

pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker;

export const UploadCard = ({ setUploadFile }) => {
    const [drag, setDrag] = useState(false);
    const [image, setImage] = useState(null);
    const [file, setFile] = useState(null);
    const [video, setVideo] = useState(null);

    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1); //setting 1 to show fisrt page

    /**
     * On loading success set the PDF to the first page and set the total number of pages
     * @param numPages Total number of pages in PDF file
     */
    function onDocumentLoadSuccess({ numPages }) {
        setPageNumber(1);
        setNumPages(numPages);
    }

    /**
     * Set the page number, depending if we click previous or next add +1 or -1 to page number
     * @param {number} offset -1 if we want to see previous page, +1 if we want to see next
     */
    function changePage(offset) {
        setPageNumber(prevPageNumber => prevPageNumber + offset);
    }

    /**
     * Go to previous page
     */
    function previousPage() {
        changePage(-1);
    }
    
    /**
     * Go to next page
     */
    function nextPage() {
        changePage(1);
    }

    /**
     * Detect the drag in HTML
     * @param event Drag event
     */
    const handleDrag = (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (event.type === "dragenter" || event.type === "dragover") {
            setDrag(true);
        } else if (event.type === "dragleave") {
            setDrag(false);
        }
    }

    /**
     * When dropping a file set the file
     * @param event Drop event
     */
    const handleDrop = (event) => {
        event.preventDefault();
        event.stopPropagation();
        setDrag(false);

        if (event.dataTransfer.files && event.dataTransfer.files[0]) {
            let files = event.dataTransfer.files;
            files[0].type === "application/pdf" ? setFile(URL.createObjectURL(files[0])) : setImage(URL.createObjectURL(files[0]));
        }
    }

    /**
     * When uploading a file with upload button set the file
     * @param event Button event
     */
    function handleChange(event) {
        setUploadFile(event.target.files[0]);
        switch (event.target.files[0].type) { 
            case "application/pdf":
                setFile(URL.createObjectURL(event.target.files[0]))
                break;
            case "image/jpeg" && "image/png":
                setImage(URL.createObjectURL(event.target.files[0]))
                break;
            case "video/mp4":
                setVideo(URL.createObjectURL(event.target.files[0]))
                break;
            default:
                break;
        }
    }

    /**
     * Delete file
     */
    function handleFileDelete() {
        setImage(null);
        setFile(null);
        setVideo(null);
    }

    return (
        <div className="upload-card" onDragEnter={handleDrag}>
            <div style={image || file ? {alignItems: 'center'} : null} className="upload-card-content">
                {!image && !file && !video ? 
                <div>
                    <div className="upload-card-drop">
                        Drop Here
                    </div>

                    <Divider text={"Or"}/>

                    <div className='upload-card-upload-button'>
                        <input type='file' id='file' onChange={handleChange}  hidden/>
                        <label htmlFor='file' className='upload-card-inputfile'>
                            Upload
                        </label>
                    </div>
                </div>
                : null}

                {image ? 
                <div className='upload-file-container'>
                    <img style={{maxWidth: '300px'}} src={image} alt="file"/>
                    <button onClick={handleFileDelete} className='btn'>x</button>
                </div>
                : null}

                {file ?
                <>
                    <div className='upload-file-pdf' style={{maxWidth: '300px'}}>
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
                    <Document className="pdf-container" file={file} onLoadSuccess={onDocumentLoadSuccess} >
                        <Page pageNumber={pageNumber} renderTextLayer={false} renderAnnotationLayer={false}/>
                    </Document>
                </>
                : null}

                {video ?
                    <div className='upload-file-container' style={{padding: "2vh"}}>
                        <button type="button" className='btn' onClick={handleFileDelete} style={{position: "unset", transform: "unset", marginBottom: "10px"}}>
                            Delete the video
                        </button>
                        <VideoPlayer video={video}/>
                    </div> 
                : null}

                { drag ? 
                    <div className="upload-card-drag-file-overlay" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div> 
                : null}

            </div>
        </div>
    );
}

export default UploadCard;

import React, {useState} from 'react'

import './uploadCard.css'
import Divider from '../divider/Divider'

export const UploadCard = ({  }) => {
    const [drag, setDrag] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDrag(true);
        } else if (e.type === "dragleave") {
            setDrag(false);
        }
    }

    return (
        <div className="upload-card" onDragEnter={handleDrag}>
            <div className="upload-card-content">
                <div className="upload-card-drop">
                    Drop Here
                </div>
                <Divider text={"Or"}/>
                <div className='upload-card-upload-button'>
                    <input type='file' id='file'  hidden/>
                    <label for='file' className='upload-card-inputfile'>
                        Upload
                    </label>
                </div>
            </div>
        </div>
    );
}

export default UploadCard;

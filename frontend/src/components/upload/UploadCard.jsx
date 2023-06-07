import react from 'React'
import propTypes from 'prop-types'

import './uploadCard.css'
import Divider from '../divider/Divider'
import Button from '../button/Button'

export const UploadCard = ({ }) => {
    return (
        <div className="upload-card">
            <div className="upload-card-content">
                Drop Here
                <Divider text={"Or"}/>
                <Button label={"Upload"} size={"small"}/>
            </div>
        </div>
    );
}

export default UploadCard;

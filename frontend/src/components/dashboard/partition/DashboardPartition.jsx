import React, {useState, useContext} from 'react'
import { ReactReduxContext } from 'react-redux'

import { UploadCard } from '../../upload/UploadCard'
import { Button } from '../../button/Button'
import './DashboardPartition.css'

export const DashboardPartition = ({partitionData}) => {

    const { store } = useContext(ReactReduxContext)
    const [uploadPartition, setUploadPartition] = useState();

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
            console.log(data);
        })
    }

    return(
        <div>
            {partitionData ? (
                <div className='dashboard-partition'>
                    oue
                </div>    
                ) : (
                <div className="dashboard-Partition-missing">
                    <div className='dashboard-Partition-missing-title'>
                        No Partition Uploaded yet ...
                    </div>
                    <div className='dashboard-Partition-missing-upload-card'>
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
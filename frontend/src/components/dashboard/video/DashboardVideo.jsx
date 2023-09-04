import React, { useState, useContext, useEffect } from 'react'
import propTypes from 'prop-types'
import { ReactReduxContext } from 'react-redux'

import './dashboardvideo.css'
import './../../textstyle/textstyles.css'

import Countries from '../../../constants/countries'
import VideoPlayer  from '../../videoPlayer/VideoPlayer.jsx'
import Button from '../../button/Button'
import Label from '../../label/Label'
import UploadCard from '../../upload/UploadCard'
import Logs from '../../../mocks/logMocks.js'

export const DashboardVideo = ({masterclassData}) => {

    const { store } = useContext(ReactReduxContext)
    const [uploadVideo, setUploadVideo] = useState(null);
    const [masterclassVideo, setMasterclassVideo] = useState([]);
    const [video, setVideo] = useState(null);

    useEffect(() => {
        const Options = {
          method: 'GET',
          headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video/masterclass/${masterclassData.id}`, Options).then((response) => response.json()).then(data => {
            setMasterclassVideo(data)
        });
    },[]);

    useEffect(() => {
        const Options = {
          method: 'GET',
          headers:  { 'Content-Type': 'video/mp4', 'accept': 'video/mp4', 'authorization': `${store.getState().user.user_token}`},
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/s3_objects/url_and_object_info/${masterclassVideo[0]?.s3_object_id}`, Options).then((response) => response.json()).then(data => {
            console.log(data)
            setVideo(data)
        });
    },[masterclassVideo]);

    // Video upload -> will be removed later to use only one upload function for all types of files

    const handleVideoUpload = (e) => {

        e.preventDefault();
        const fileBlob = new Blob([uploadVideo], {type: 'video/mp4'});
        var formData = new FormData();
        formData.append('masterclass_id', masterclassData.id);
        formData.append('duration', 1);
        formData.append('version', 1);
        formData.append('public', true);
        formData.append('file', fileBlob, "video.mp4");
        const uploadOptions = {
            method: 'POST',
            headers: { 'authorization': `${store.getState().user.user_token}` },
            body: formData,
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video`, uploadOptions).then((response) => response.json()).then(data => {
            console.log(data);
        })
    }

    return ( 
        <div>
            {masterclassVideo?.length > 0 ? (
            <div className='dashboard-video'>
                <div className='display-main'>
                    <div className='main-video'>
                        <VideoPlayer video={video.url}/>
                    </div>
                    <div className='right-side-wrapper'>
                        <div className='country-wrapper'>
                            <span className='body1semibold bluetext'>Subtitles</span>
                            <div className='country-marg'>
                                {Countries.map((country, index) =>  {
                                    return (
                                        <div key={index}  >
                                            <div className='country'>
                                                <img className='country-img' src={country.image}></img>
                                                <span className='body2regular'>{country.title}</span>
                                            </div>
                                        </div>
                                )})}
                            </div>
                        <div>
                        <Button label='Upload Subtitle'/>
                    </div>
                </div>
                <div className='label-wrapper'>
                    <div className='label-wrapper-header'>
                        <span className='body1semibold bluetext'>Tags</span>
                        <Label type='plus' label='+'/>
                    </div>
                    <Label type='tags' label='Compositor Name'/>
                    <Label type='tags' label='Date'/>
                    <Label type='tags' label='Student Name'/>
                    <Label type='tags' label='Instrument'/>
                    <Label type='tags' label='Teacher Name'/>
                    <Label type='tags' label='Piece'/>
                    <Label type='tags' label='Vues'/>
                </div>
            </div>
            </div>
            <div className='versionning'>
                <div className='versionning-header'>
                    <span className='subtitle2'>Current Version:</span>
                    <div className='version-border'>
                        <span className='subtitle3'>3.0</span>
                    </div>
                    <span className='body1medium'>Video_name</span>
                    <span className='body1medium'>File_name</span>
                </div>
                <div className='log-list'>
                    {Logs.map((log, index) =>  {
                        return (
                            <div key={index}  >
                                <div className='versionning-logs'>
                                    <span className='body1medium'>{log.version}</span>
                                    <span className='body1medium'>{log.author}</span>
                                    <span className='body1regular'>{log.videoname}</span>
                                    <span className='body1regular'>{log.changedate}</span>
                                    <span className='body1regular'>{log.changetime}</span>
                                    <Label type={log.type} log={log.log} label={log.text}/>
                                </div>
                            </div>
                    )})}
                </div>
            </div>
            </div>
            ) : (
                <div className="dashboard-video-missing">
                    <div className='dashboard-video-missing-title'>
                        No Video Uploaded yet ...
                    </div>
                    <div className='dashboard-video-missing-upload-card'>
                        <UploadCard setUploadFile={setUploadVideo}/>
                    </div>
                    <div>
                        <Button label={"Save"} onClick={(e) => handleVideoUpload(e)}/>
                    </div>
                </div>
            )}
        </div>
    )
}

    DashboardVideo.propTypes = {
        title: propTypes.string.isRequired,
        description: propTypes.string.isRequired,
    }

    DashboardVideo.defaultProps = {
        title: 'Upload Video',
        description: 'Upload your video here',
    }

    export default DashboardVideo;
        
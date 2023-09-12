import React, { useState, useContext, useEffect } from 'react'
import propTypes from 'prop-types'
import { ReactReduxContext } from 'react-redux'
import { useToast } from '../../../utils/toast'

import './dashboardvideo.css'
import './../../textstyle/textstyles.css'

import Countries from '../../../constants/countries'
import VideoPlayer  from '../../videoPlayer/VideoPlayer.jsx'
import Button from '../../button/Button'
import Label from '../../label/Label'
import UploadCard from '../../upload/UploadCard'
import Logs from '../../../mocks/logMocks.js'

import { deleteVideo, getVideo, getVideoInfo, uploadNewVideo } from '../../../services/masterclass/video'

export const DashboardVideo = ({masterclassData}) => {

    const { store } = useContext(ReactReduxContext)
    const toast = useToast();

    const [uploadVideo, setUploadVideo] = useState(null);
    const [masterclassVideo, setMasterclassVideo] = useState([]);
    const [video, setVideo] = useState([]);
    const [videoId, setVideoId] = useState(null);
    const [displayedVideo, setDisplayedVideo] = useState(0);
    const [newVideoUploadPopup, setNewVideoUploadPopup] = useState(false); 

    useEffect(() => {
        getVideoInfo(store.getState().user.user_token, masterclassData.id, setMasterclassVideo)
    },[videoId]);

    useEffect(() => {
        if(masterclassVideo.length > 0) {
            for(var i = 0; i < masterclassVideo.length; i++) {
                getVideo(store.getState().user.user_token, video, masterclassVideo[i]?.s3_object_id, setVideo)
            }
        }
    },[masterclassVideo]);

    const handleDeleteVideo = (e) => {
        e.preventDefault();
        deleteVideo(store.getState().user.user_token, masterclassVideo[displayedVideo]?.id, toast)
    }

    const handleVideoUpload = (e) => {
        e.preventDefault();
        if(masterclassVideo?.length > 3) {
            toast.open({message: "You can only upload 5 videos per masterclass", type: "failure"})
            return
        }
        uploadNewVideo(store.getState().user.user_token, uploadVideo, masterclassData, setNewVideoUploadPopup, setVideoId, toast)
    }

    const choseVideoCallback = (e, chosedVideo) => {
        e.preventDefault();
        setDisplayedVideo(chosedVideo)
    }

    const handleAddNewVideo = (e) => {
        e.preventDefault();
        setNewVideoUploadPopup(true)
    }

    const uploadPopup = () => {
        return(
            <div className='dashboard-video-popup'>
                <div className='dashboard-video-popup-upload-card'>
                    <UploadCard setUploadFile={setUploadVideo}/>
                </div>
                <div>
                    <Button label={"Save"} onClick={(e) => handleVideoUpload(e)}/>
                    <Button label={"Close"} onClick={(e) => setNewVideoUploadPopup(false)}/>
                </div>
            </div>
        )
    }

    return (
        <>
            {newVideoUploadPopup ? uploadPopup() : null}
            {masterclassVideo?.length > 0 ? (
            <div className='dashboard-video'>
                <div className='display-main'>
                    <div className='dashboard-video-wrap'>
                        <div className='main-video'>
                            <VideoPlayer video={video[displayedVideo]?.url}/>
                        </div>
                        <div className="dashboard-video-list">
                            <div className='dashboard-video-list-item' onClick={(e) => choseVideoCallback(e, 0)}>
                                {video[0] ? (
                                    <div>
                                        <span style={{position:"absolute"}}>{masterclassVideo[0]?.filename}</span>
                                        <video className='dashboard-video-list-item-video' src={video[0]?.url} controls={false}/>
                                    </div>
                                ) : 'Missing Video'}
                            </div>
                            <div className='dashboard-video-list-item' onClick={(e) => choseVideoCallback(e, 1)}>
                                {video[1] ? (
                                    <div>
                                        <span style={{position:"absolute"}}>{masterclassVideo[0]?.filename}</span>
                                        <video className='dashboard-video-list-item-video' src={video[1]?.url} controls={false}/>
                                    </div>
                                ) : 'Missing Video'}
                            </div>
                            <div className='dashboard-video-list-item' onClick={(e) => choseVideoCallback(e, 2)}>
                                {video[2] ? (
                                    <div>
                                        <span style={{position:"absolute"}}>{masterclassVideo[0]?.filename}</span>
                                        <video className='dashboard-video-list-item-video' src={video[2]?.url} controls={false}/>
                                    </div>
                                ) : 'Missing Video'}
                            </div>
                        </div>
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
                        <Button label="Remove video" onClick={(e) => handleDeleteVideo(e)}/> 
                        <Button label="Add new video" onClick={(e) => handleAddNewVideo(e)}/>            
                    </div>
                </div>
            <div className='versionning'>
                <div className='versionning-header'>
                    <span className='subtitle2'>Current Version:</span>
                    <div className='version-border'>
                        <span className='subtitle3'>{masterclassVideo[0].version}</span>
                    </div>
                    <span className='body1medium'>{masterclassVideo[0].filename}</span>
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
        </>
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
        
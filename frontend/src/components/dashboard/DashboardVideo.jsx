import React from 'react'
import propTypes from 'prop-types'

import './dashboardvideo.css'
import './../textstyle/textstyles.css'

import Countries from '../../constants/countries'
import Uploadcard  from '../../components/upload/UploadCard.jsx'
import VideoPlayer  from '../../components/videoPlayer/VideoPlayer.jsx'
import MasterCardData  from '../../mocks/masterClassMocks.js'
import peppapig from '../../assets/peppa pig wow.mp4'
import Button from '../button/Button'
import Label from '../label/Label'
import Logs from '../../mocks/logMocks.js'

export const DashboardVideo = ({ MasterCardData, Videoname }) => {

    // const [country, setCountry] = React.useState('');

    // const handleCountry = (country) => {
    //     setCountry(country);
    // };

    return ( 
        <div>
        <div className='display-main'>
            {/* <h3 className='upload-label'>No Video Uploaded yet ...</h3>
            <Uploadcard/> */}
            <div className='main-video'>
            <VideoPlayer video={peppapig}/>
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
            
            {/* <div className='tags-wrapper'>
                <span>Tags</span>
                <div className='tags-marg'>
                {Tags.map((tag, index) =>  {
                    return (
                        <div key={index}  >
                            <div className='tag'>
                                <span>{tag.title}</span>
                            </div>
                        </div>
                )})}
                </div>
            </div> */}
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
                )}  )
        }
        </div>

        </div>
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
        
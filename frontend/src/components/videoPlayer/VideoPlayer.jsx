import React, {useState} from "react";
import PropTypes from 'prop-types';
import "./VideoPlayer.css";

import useVideoPlayer from "./useVideoPlayer";

import playButton from "../../assets/videoPlayer/Play/Play.svg";
import pauseButton from "../../assets/videoPlayer/Pause/Pause.svg";
import rewindButton from "../../assets/videoPlayer/Rewind/Rewind.svg";
import forwardButton from "../../assets/videoPlayer/Forward/Forward.svg";
import fullScreenButton from "../../assets/videoPlayer/FullScreen/FullScreen.svg";
import volumeButton from "../../assets/videoPlayer/Volume/Volume.svg";

const VideoPlayer = ({ video }) => {
    const videoElement = React.useRef(null);
    const {
        playerState,
        togglePlay,
        handleProgress,
        handleTimeUpdate,
        handleVideoSpeed,
        handleVolume,
        //handleMute,
        handleFullscreen,
        handleTimeRewind,
        handleTimeForward,
    } = useVideoPlayer(videoElement);

    var pendingClick = 0;

    const handleVideoClick = (e) => {
        if (pendingClick) {
            clearTimeout(pendingClick);
            pendingClick = 0;
        }
    
        switch (e.detail) {
            case 1:
                pendingClick = setTimeout(function() {
                    togglePlay();
                }, 200);
                break;
            case 2:
                handleFullscreen();
                break;
            default:
                console.log('No need to spam mon con');
                break;
        }
    };

    const [volumeHovered, setVolumeHovered] = useState(false); 

    return (
        <div className="video-wrapper">
            <video
                ref={videoElement}
                src={video}
                className="video-player"
                onTimeUpdate={handleProgress}
                onClick={handleVideoClick}
            ></video>
            <div className="video-player-controls">
                <div className="video-player-progress-wrapper">
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={playerState.progress}
                        className="video-player-controls-progress"
                        onChange={(e) => handleTimeUpdate(e)}
                    />
                </div>
                <div className="video-player-controls-wrapper">
                    <button
                        className="video-player-controls-button"
                        onClick={togglePlay}
                    >
                        {playerState.playing ?  
                            <object 
                                className="controls-svg" 
                                data={pauseButton} 
                                width="15" 
                                height="15"
                            /> 
                            : 
                            <object 
                                className="controls-svg" 
                                data={playButton} 
                                width="15" 
                                height="15"
                            />
                        }
                    </button>
                    <button
                        className="video-player-controls-rewind"
                        onClick={handleTimeRewind}
                    >
                        <object className="controls-svg" data={rewindButton}
                            width="15" height="15"
                        />
                    </button>
                    <button
                        className="video-player-controls-forward"
                        onClick={handleTimeForward}
                    >
                        <object className="controls-svg" data={forwardButton}
                            width="15" height="15"
                        />
                    </button>
                    <button
                        onClick={() => setVolumeHovered(true)}
                    >
                        <object className="controls-svg" data={volumeButton} 
                            width="15" height="15"
                        />
                    </button>
                    {volumeHovered ?
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.05"
                            value={playerState.volume}
                            className="video-player-controls-volume"
                            onChange={(e) => handleVolume(e)}
                            onMouseLeave={() => setVolumeHovered(false)}
                        />
                    : null}
                    <div className="video-player-controls-progress-text">
                        {videoElement.current?.currentTime.toFixed(2)} / {videoElement.current?.duration.toFixed(2)}
                    </div>
                    <select
                        value={playerState.speed}
                        className="video-player-controls-speed"
                        onChange={(e) => handleVideoSpeed(e)}
                    >
                        <option value="0.5">0.5x</option>
                        <option value="0.75">0.75x</option>
                        <option value="1">1x</option>
                        <option value="1.25">1.25x</option>
                        <option value="1.5">1.5x</option>
                        <option value="2">2x</option>
                    </select>
                    {/* <button
                        className="video-player-controls-mute"
                        onClick={handleMute}
                    >
                        {playerState.muted ? "Unmute" : "Mute"}
                    </button> */}
                    <button
                        className="video-player-controls-fullscreen"
                        onClick={handleFullscreen}
                    >
                        <object className="controls-svg" data={fullScreenButton} width="15" height="15"/>
                    </button>
                </div>
            </div>
        </div>
    );
};

VideoPlayer.propTypes = {
    video: PropTypes.string.isRequired,
};

export default VideoPlayer;


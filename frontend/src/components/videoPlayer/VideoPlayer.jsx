import React from "react";
import PropTypes from 'prop-types';
import "./VideoPlayer.css";

import useVideoPlayer from "./useVideoPlayer";

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
                        {playerState.playing ? "Pause" : "Play"}
                    </button>
                    <button
                        className="video-player-controls-rewind"
                        onClick={handleTimeRewind}
                    >
                        -10s
                    </button>
                    <button
                        className="video-player-controls-forward"
                        onClick={handleTimeForward}
                    >
                        +10s
                    </button>
                    <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.05"
                        value={playerState.volume}
                        className="video-player-controls-volume"
                        onChange={(e) => handleVolume(e)}
                    />
                    <div className="video-player-controls-progress">
                    {videoElement.current.currentTime} / {videoElement.current.duration}
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
                        Fullscreen
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


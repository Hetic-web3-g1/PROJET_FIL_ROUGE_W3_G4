import React from 'react';

import { useState, useEffect } from 'react';

const useVideoPlayer = (videoElement) => {
    const [playerState, setPlayerState] = useState({
        playing: false,
        muted: false,
        speed: 1,
        volume: 1,
        progress: 0,
        fullscreen: false,
    });

    const [video, setVideo] = useState(null);   

    useEffect(() => {
        setVideo(videoElement.current);
    }, [videoElement]);

    const togglePlay = () => {
        setPlayerState({
            ...playerState,
            playing: !playerState.playing,
        });
    };

    useEffect(() => {
        if (video) {
            playerState.playing ? video.play() : video.pause();
        }
    }, [playerState.playing, video]);

    const handleProgress = () => {
        setPlayerState({
            ...playerState,
            progress: (video.currentTime / video.duration) * 100,
        });
    }

    const handleTimeUpdate = (e) => {
        const time = e.target.value;
        video.currentTime = (time / 100) * video.duration;  
        setPlayerState({
            ...playerState,
            progress: time,
        });
    }

    const handleTimeRewind = () => {
        video.currentTime = video.currentTime - 10;
        setPlayerState({
            ...playerState,
            progress: (video.currentTime / video.duration) * 100,
        });
    }

    const handleTimeForward = () => {
        video.currentTime = video.currentTime + 10;
        setPlayerState({
            ...playerState,
            progress: (video.currentTime / video.duration) * 100,
        });
    }

    const handleVideoSpeed = (e) => {
        const speed = e.target.value;
        video.playbackRate = speed;
        setPlayerState({
            ...playerState,
            speed: speed,
        });
    }

    const handleVolume = (e) => {
        const volume = e.target.value;
        video.volume = volume;
        setPlayerState({
            ...playerState,
            volume: volume,
        });
    }

    const handleMute = () => {
        setPlayerState({
            ...playerState,
            muted: !playerState.muted,
        });
    }

    // useEffect(() => {
    //     playerState?.muted ? video.muted = true : video.muted = false;
    // }, [playerState.muted, video]);

    const handleFullscreen = () => {
        setPlayerState({
            ...playerState,
            fullscreen: !playerState.fullscreen,
        });
    }

    useEffect(() => {
        if (!playerState.fullscreen && document.fullscreenElement != null)
        {
            document.exitFullscreen();
        }
        else if (playerState.fullscreen) {
            video.requestFullscreen();
        }
    }, [playerState.fullscreen, video]);

    return {
        playerState,
        togglePlay,
        handleProgress,
        handleTimeUpdate,
        handleVideoSpeed,
        handleVolume,
        handleMute,
        handleFullscreen,
        handleTimeRewind,
        handleTimeForward,
    };
};

export default useVideoPlayer;
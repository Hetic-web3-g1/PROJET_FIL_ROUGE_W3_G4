import VideoPlayer from "./VideoPLayer";

import video from '../../assets/peppa pig wow.mp4';

export default {
    title: "VideoPlayer",
    component: VideoPlayer,
    tags: ["autodocs"],
    argTypes: {
        video: video,
    },
};

export const Default = {
    args: {
        video: video,
    },
};
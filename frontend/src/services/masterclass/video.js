export function getVideoInfo(token, masterclassId, setMasterclassVideo) {
    const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video/masterclass/${masterclassId}`, Options).then((response) => response.json()).then(data => {
        setMasterclassVideo(data)
    });
}

export function getVideo(token, video, videoId, setVideo) {
    const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'video/mp4', 'accept': 'video/mp4', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/s3_objects/url_and_object_info/${videoId}`, Options).then((response) => response.json()).then(data => {
        var tmp = video;
        tmp = [...tmp, data]
        setVideo([...video, data])
    });
}

export function deleteVideo(token, videoId, setMasterclassVideo, toast) {
    const Options = {
        method: 'DELETE',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video/${videoId}`, Options).then((response) => response.json()).then(data => {
        toast.open({message: "Video deleted successfully", type: "success"})
        setMasterclassVideo([])
    });
}

export function uploadNewVideo(token, uploadVideo, masterclassData, setNewVideoUploadPopup, setVideoId, toast) {
    const fileBlob = new Blob([uploadVideo], {type: 'video/mp4'});
    var formData = new FormData();
    formData.append('masterclass_id', masterclassData.id);
    formData.append('duration', 1);
    formData.append('version', 1);
    formData.append('public', true);
    formData.append('file', fileBlob, uploadVideo.name);
    const uploadOptions = {
        method: 'POST',
        headers: { 'authorization': `${token}` },
        body: formData,
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video`, uploadOptions).then((response) => response.json()).then(data => {
        setNewVideoUploadPopup(false)
        setVideoId(data)
        toast.open({message: "Video uploaded successfully", type: "success"})
    })
}

export function uploadNewSubtitles(token, uploadSubtitles, subtitlesCountry, masterClassData, setUploadSubtitlesPopup, toast) {
    const fileBlob = new Blob([uploadSubtitles], {type: 'text/vtt'});
    var formData = new FormData();
    formData.append('language', subtitlesCountry);
    formData.append('masterclass_id', masterClassData.id);
    formData.append('file', fileBlob, uploadSubtitles.name);
    const uploadOptions = {
        method: 'POST',
        headers: { 'authorization': `${token}` },
        body: formData,
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/subtitles/subtitle`, uploadOptions).then((response) => response.json()).then(data => {
        setUploadSubtitlesPopup(false)
        toast.open({message: "Subtitles uploaded successfully", type: "success"})
    })
}

export function getSubtitles(token, masterclassId, subtitles, setSubtitles) {
    const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'video/mp4', 'accept': 'video/mp4', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/subtitles/subtitle/masterclass/${masterclassId}`, Options).then((response) => response.json()).then(data => {
        var tmp = subtitles;
        tmp = [...tmp, data]
        setSubtitles([...subtitles, data])
    });
}

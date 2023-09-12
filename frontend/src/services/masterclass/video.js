export function getVideoInfo(token, masterclassId, setMasterclassVideo) {
    const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video/masterclass/${masterclassId}`, Options).then((response) => response.json()).then(data => {
        setMasterclassVideo(data)
    });
}

export function getVideo(token, videoId, setVideo) {
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

export function deleteVideo(token, videoId, setMasterclassVideo) {
    const Options = {
        method: 'DELETE',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}`},
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/videos/video/${videoId}`, Options).then((response) => response.json()).then(data => {
        toast.open({message: "Video deleted successfully", type: "success"})
        setMasterclassVideo([])
    });
}

export function uploadNewVideo(token, uploadVideo, masterclassData, setNewVideoUploadPopup, setVideoId) {
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
        toast.open({message: "Video uploaded successfully", type: "success"})
        setNewVideoUploadPopup(false)
        setVideoId(data)
    })
}
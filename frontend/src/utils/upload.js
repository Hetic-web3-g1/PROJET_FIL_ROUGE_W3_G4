export const uploadFile = (file, file_type, isPublic) => {
    const uploadOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
        body : JSON.stringify({
            file: file,
            isPublic: isPublic,
        }),
    };

    fetch(`http://${import.meta.env.API_ENDPOINT}/s3_objects/upload/${file_type}`, uploadOptions).then((response) => response.json()).then(data => {
        if (data?.detail[0].msg != "field required") {
            handleClose();
        } else {
            alert('Invalid data');
        }
    });
};

export default uploadFile;
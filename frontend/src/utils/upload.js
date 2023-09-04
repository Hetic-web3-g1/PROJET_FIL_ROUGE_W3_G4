export const uploadFile = (file, file_type, data, target, store) => {
    const fileBlob = new Blob([file], { type: file_type });
    var formData = new FormData();
    Object.keys(data).forEach((value, key) => {
        console.log(value, key)
        formData.append(key, value);
    });
    formData.append('file', fileBlob, file.name);
    const uploadOptions = {
        method: 'POST',
        headers: { 'authorization': `${store.getState().user.user_token}` },
        body : formData
    };
    var route = '';
    switch (target) {
        case 'partition':
            route = 'partitions/partition';
            break;
        case 'video':
            route = 'videos/video';
            break;
        default:
            break;
    }
    fetch(`http://${import.meta.env.API_ENDPOINT}/${route}`, uploadOptions).then((response) => response.json()).then(data => {
        return data;
    });
};

export default uploadFile;
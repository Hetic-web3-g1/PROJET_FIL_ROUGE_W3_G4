
export function setLocaleUserData(token, dispatch, ProfileActions) {
    const userOptions = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}` },
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/users/user/me`, userOptions).then((response) => response.json()).then(data => {
        dispatch(ProfileActions.updateProfile(data));
    });
}

export function getUserAvatar(token, profile, setAvatar) {
    const userOptions = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}` },
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/images/image/${profile?.image_id}`, userOptions).then((response) => response.json()).then(data => {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/s3_objects/url_and_object_info/${data?.s3_object_id}`, userOptions).then((response) => response.json()).then(data2 => {
            setAvatar(data2);
        });
    });
}
export function setLocaleAcademyData(token, dispatch, AcademyActions) {
    const userOptions = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}` },
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/academies/${store.getState().user.profile.academy_id}`, userOptions).then((response) => response.json()).then(data => {
        dispatch(AcademyActions.setAcademy(data));
    });
}
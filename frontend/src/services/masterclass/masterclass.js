export function getMasterclassTabData(token, masterclassData, setProfessorData, setComposerData, setUserList, setAcademy, setPartitionData, setWorkAnalysisData) {
    const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}`},
    };
    if (masterclassData && masterclassData?.teacher_bio_id !== null) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/biographies/biography/${masterclassData.teacher_bio_id}`, Options).then((response) => response.json()).then(data => {
        setProfessorData(data)
        });
    }
    if (masterclassData && masterclassData?.composer_bio_id !== null) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/biographies/biography/${masterclassData.composer_bio_id}`, Options).then((response) => response.json()).then(data => {
        setComposerData(data)
        });
    }
    if (masterclassData) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/users/academy/${masterclassData?.academy_id}`, Options).then((response) => response.json()).then(data => {
        setUserList(data)
        });
    }
    if (masterclassData) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/academies/${masterclassData?.academy_id}`, Options).then((response) => response.json()).then(data => {
        setAcademy(data)
        });
    }
    if (masterclassData && masterclassData?.partition_id !== null) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/partitions/partition/${masterclassData?.partition_id}`, Options).then((response) => response.json()).then(data => {
        setPartitionData(data)
        });
    }
    if (masterclassData && masterclassData?.work_analysis_id !== null) {
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/work_analyzes/work_analysis/${masterclassData?.work_analysis_id}`, Options).then((response) => response.json()).then(data => {
        setWorkAnalysisData(data)
        });
    }
}
export function login(email, password, setLoginData, toast) {
    const loginOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
        body: JSON.stringify({email, password }),
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/login`, loginOptions).then((response) => response.json()).then(data => {
        if (data && data.detail != "Invalid Credentials") {
            setLoginData(data);
        } else {
            toast.open({message: 'Invalid Credentials', type: 'failure'});
        }
    });
}

export function resetPasswordEmail(email, toast, setResetData) {
    const emailOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/forgot-password?email=${email}`, emailOptions).then((response) => response.json()).then(data => {
        if (data) {
            setResetData(data);    
        } else {
            toast.open({message: 'Invalid Email', type: 'failure'});
        }
    });
}

export function resetPassword(token, password, confirmPassword, toast, setPasswordData) {
    if (password != confirmPassword) {
        toast.open({message: 'Passwords do not match', type: 'failure'});
        return;
    }
    else {
        const resetOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
          body: JSON.stringify({password, token }),
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/reset-password`, resetOptions).then((response) => response.json()).then(data => {
          if (data?.detail != "Invalid Credentials" || data?.detail != "Expired Token") {
            setPasswordData("isok");
          } else {
            toast.open({message: data?.detail, type: 'failure'});
          }
        });
    }
}

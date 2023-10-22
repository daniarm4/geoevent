async function checkIsAuth() {
    let accessToken = localStorage.getItem('accessToken')

    if (accessToken) {
        let response = await fetch('/users/check_auth', {
            method: 'GET',
            headers: {'Authorization': `Bearer ${accessToken}`}
        })
        if (response.status === 401) {
            localStorage.removeItem('accessToken')
            console.log('Invalid access token')
            return false
        }
        if (response.status === 200) {
            return true
        }
    }
    return false
}

let isAuth = checkIsAuth();
if (isAuth) {
    alert('Вы уже авторизованы')
    location.replace('/map');
    console.log('auth')
}

async function onFormSubmit(event) {
    event.preventDefault();

    let form = document.querySelector('#register_form');
    let data = new FormData(form);

    let response = await fetch('/users/create', {
        method: 'POST',
        body: data
    });

    if (response.status === 409) {
        console.log(response.statusText)
    } else {
        await response.json();
    }
}
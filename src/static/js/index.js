const map = L.map('map', {
    center: [-29.50, 400],
    zoom: 3.5
});
const nameInput = document.getElementById('nameInput')
const descriptionInput = document.getElementById('descriptionInput');
const form = document.querySelector('form');
let refsContainer = document.getElementById('refs')
let eventInfo;

form.addEventListener('submit', e => {
    e.preventDefault();
});

descriptionInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    addEvent();
  }
  if (e.key === 'Escape') {
    closeModal();
  }
});

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
            map.on('click', onMapClick);
            return true
        }
    }
    return false
}

async function loadEvents() {
    let response = await fetch('/events', {
        method: 'GET',
    });
    if (response.status === 200) {
        let res = await response.json();
        res.events.forEach(event => {
            let marker = L.marker([+event.latitude, +event.longitude]).addTo(map)
            let content = getContent(event.description);
            marker.bindPopup(`<h2>${event.name}</h2>${content}`);
        })
    }
}

async function loadButtons() {

    let isAuth = await checkIsAuth();

    if (!isAuth) {
        let aEnter = document.createElement('a');
        let aRegister = document.createElement('a');
        aEnter.href = "/login";
        aEnter.innerText = "Войти";
        aRegister.href = "/register";
        aRegister.innerText = "Зарегистрироваться";
        refsContainer.appendChild(aEnter);
        refsContainer.appendChild(aRegister);
    } else {
        let aExit = document.createElement('a');
        aExit.innerText = "Выйти";
        aExit.href = '/map'
        aExit.addEventListener('click', removeAccessToken);
        refsContainer.appendChild(aExit);
    }
}

async function loadPage() {
    await loadButtons();
    await loadEvents();
}

function removeAccessToken() {
    localStorage.removeItem('accessToken');
}

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);

function onMapClick(e) {
    eventInfo = e; 
    showModal()
}

function showModal() {
    modal.style.display = "block";
    descriptionInput.focus()
}

function closeModal() {
    modal.style.display = "none";
    descriptionInput.value = "";
}

function getContent(text) {
    let words = text.split(' ');
    let content = '';
    let line = '';
    for(let word of words) {
        if(line.length + word.length > 30) {
            content += line + '<br>';
            line = ''; 
        }
        line += word + ' ';
    }
    content += line;
    return content
}

async function addEvent() {
    if (!nameInput.value) {
        return
    }

    let lon = +eventInfo.latlng.lng.toFixed(6);
    let lat = +eventInfo.latlng.lat.toFixed(6);
    let body = {
        name: nameInput.value,
        description: descriptionInput.value,
        longitude: lon,
        latitude: lat
    }
    let accessToken = localStorage.getItem('accessToken')
    let response = await fetch('/events/create', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-type': 'application/json',
        }
    });
    if (response.status === 200) {
        let marker = L.marker([lat, lon]).addTo(map)
        let content = getContent(descriptionInput.value);
        marker.bindPopup(`<h2>${nameInput.value}</h2>${content}`);
        descriptionInput.value = "";
        nameInput.value = "";
        console.log('Event created');
        closeModal();
    } else {
        console.log(response.statusText)
    } 
}

loadPage();

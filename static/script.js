let map;

function initMap() {
    map = L.map('map').setView([20.5937, 78.9629], 4); // Centered on India by default

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    map.on('click', function (e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        getWeatherByLocation(lat, lon);
    });
}

function getWeatherByLocation(lat, lon) {
    const weatherType = document.getElementById('weather-type').value;

    let url = `/weather?lat=${lat}&lon=${lon}`;

    if (weatherType === 'forecast') {
        url += '&forecast=true';
    } else if (weatherType === 'history') {
        const date = prompt("Enter a date (YYYY-MM-DD):");
        if (!date) {
            alert('Please enter a date');
            return;
        }
        url += `&history=${date}`;
    }

    axios.get(url)
        .then(response => {
            displayWeather(response.data);
        })
        .catch(() => {
            alert('Could not get weather!');
        });
}

function displayWeather(data) {
    let resultHtml = `<h2>Weather in ${data.name}</h2>`;

    if (data.forecast) {
        resultHtml += `<h3>3-Day Forecast:</h3>`;
        data.forecast.forEach(day => {
            resultHtml += `
                <p><strong>${day.date}:</strong> ${day.temp}°C, ${day.description}, Wind: ${day.wind} km/h</p>
            `;
        });
    } else if (data.history) {
        resultHtml += `
            <p><strong>${data.history.date}:</strong> ${data.history.temp}°C, ${data.history.description}, Wind: ${data.history.wind} km/h</p>
        `;
    } else {
        resultHtml += `
            <p>Temperature: ${data.temp}°C</p>
            <p>Humidity: ${data.humidity}%</p>
            <p>Wind Speed: ${data.wind} km/h</p>
            <p>Description: ${data.description}</p>
            <p>Rain Possibility: ${data.rain} mm</p>
            <p>Thunder: ${data.thunder ? 'Yes' : 'No'}, Storm: ${data.storm ? 'Yes' : 'No'}</p>
        `;
    }

    document.getElementById('weather-result').innerHTML = resultHtml;

    const shareLink = window.location.href;
    document.getElementById('share-link').innerHTML = `<a href="${shareLink}" target="_blank">Share this link</a>`;
}

// Ensure map initializes only after DOM is ready
document.addEventListener("DOMContentLoaded", initMap);

document.getElementById('weather-form').addEventListener('submit', function (e) {
    e.preventDefault(); // prevent page reload

    const city = document.getElementById('city').value;
    const weatherType = document.getElementById('weather-type').value;

    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    let url = `/weather?city=${encodeURIComponent(city)}`;

    if (weatherType === 'forecast') {
        url += '&forecast=true';
    } else if (weatherType === 'history') {
        const date = prompt("Enter a date (YYYY-MM-DD):");
        if (!date) {
            alert('Please enter a date');
            return;
        }
        url += `&history=${date}`;
    }

    axios.get(url)
        .then(response => {
            displayWeather(response.data);
        })
        .catch(() => {
            alert('Could not get weather!');
        });
});

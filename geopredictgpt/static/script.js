const apiKey = "YOUR_API_KEY"; // Replace with your OpenWeather API key

        function fetchResponse(apiUrl, elementId) {
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    document.getElementById(elementId).innerText = data.response || "No response.";
                })
                .catch(error => {
                    document.getElementById(elementId).innerText = "Error fetching data.";
                    console.error(error);
                });
        }

        // Fetch responses from each API
        fetchResponse('/gemini-api3/', 'response3');

async function fetchWeather() {
    const city = document.getElementById("city").value.trim();
    
    if (!city) {
        alert("Please enter a valid city name.");
        return;
    }

    try {
        // Fetch Live Weather
        const weatherRes = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`);
        const weatherData = await weatherRes.json();
        
        if (weatherData.cod !== 200) {
            alert("City not found. Try again!");
            return;
        }

        document.getElementById("live-weather").innerHTML = 
            `<h2>Live Weather</h2><p><strong>${weatherData.name}</strong>: ${weatherData.main.temp}°C, ${weatherData.weather[0].description}</p>`;

        // Fetch Forecast Data
        const forecastRes = await fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=metric`);
        const forecastData = await forecastRes.json();

        let forecastHTML = "<h2>3-Day Forecast</h2>";
        forecastData.list.slice(0, 3).forEach(item => {
            forecastHTML += `<p>${item.dt_txt.split(" ")[0]}: ${item.main.temp}°C</p>`;
        });
        document.getElementById("forecast").innerHTML = forecastHTML;

        // Storm Updates (Placeholder)
        document.getElementById("storm-updates").innerHTML = "<h2>Storm Alerts</h2><p>No storm warnings reported.</p>";

        // Storm Prone Areas (Mock Data)
        document.getElementById("storm-prone-areas").innerHTML = "<h2>Storm Prone Areas</h2><p>Miami, Florida, New Orleans, and Houston</p>";

    } catch (error) {
        console.error("Error fetching weather:", error);
        alert("Something went wrong! Please try again.");
    }
}

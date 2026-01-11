# 🌤️ Real-Time Weather App

A beautiful, user-friendly Python desktop application that displays real-time weather data with automatic location detection.

![Screenshot](https://ibb.co/v0YGc0W)

## ✨ Features

- 🌍 **Automatic Location Detection** - Instantly detects your location using IP geolocation
- 🔍 **City Search** - Search weather for any city worldwide
- 🎨 **Modern UI** - Clean, intuitive interface with dark theme
- 📊 **Comprehensive Weather Data** - Temperature, humidity, wind speed, cloud cover, and more
- ⚡ **Real-Time Updates** - Live weather information from Open-Meteo API
- 🧵 **Smooth Performance** - Non-blocking API calls with threading
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux

## 📸 Screenshot

The app displays:
- Current temperature and weather conditions
- Feels-like temperature
- Wind speed
- Humidity percentage
- Cloud cover
- Visibility status
- UV Index

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository** (or download the files)
```bash
git clone https://github.com/Shriyash-24/weather-app.git
cd weather-app
```

2. **Install required dependencies**
```bash
pip install requests
```

### Running the Application

Simply run the Python script:

```bash
python weather-app.py
```

## 🎯 How to Use

### Automatic Location Detection
1. Launch the app - it automatically detects your location on startup
2. Click the **📍 Auto** button anytime to refresh with your current location

### Manual Search
1. Click on the search box and type any city name
2. Press **Enter** or click the **Search** button
3. Weather data will display instantly

### Keyboard Shortcuts
- **Enter** - Search for the entered city
- Window is resizable for your preferred viewing size

## 🛠️ Technical Details

### APIs Used

- **Open-Meteo API** - Free weather data (no API key required)
  - Endpoint: `https://api.open-meteo.com/v1/forecast`
  - Provides current weather conditions, temperature, wind, humidity, etc.

- **Open-Meteo Geocoding API** - Location search
  - Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
  - Converts city names to coordinates

- **IP-API** - IP geolocation (no API key required)
  - Endpoint: `http://ip-api.com/json/`
  - Automatic location detection

### Technologies

- **Python 3.7+**
- **Tkinter** - GUI framework (included with Python)
- **Requests** - HTTP library for API calls
- **Threading** - Non-blocking API requests


## 🎨 Features Breakdown

### Weather Information Displayed

| Feature | Description |
|---------|-------------|
| Temperature | Current temperature in Celsius |
| Feels Like | Apparent temperature |
| Weather Condition | Clear, cloudy, rainy, snowy, etc. |
| Wind Speed | Wind speed in km/h |
| Humidity | Relative humidity percentage |
| Cloud Cover | Cloud coverage percentage |
| Visibility | Visibility status |
| UV Index | UV radiation level |

### Weather Conditions Supported

The app recognizes and displays various weather conditions:
- Clear sky / Mainly clear
- Partly cloudy / Overcast
- Fog
- Drizzle (light, moderate, dense)
- Rain (slight, moderate, heavy)
- Snow (slight, moderate, heavy)
- Rain showers
- Snow showers
- Thunderstorms
- Hail

## 🔧 Customization

### Change Temperature Units

Modify the API parameters in the `fetch_weather` method:

```python
params = {
    "temperature_unit": "fahrenheit",  # Add this line
    # ... other params
}
```

### Modify Color Scheme

Update the color codes in the `setup_ui` method:

```python
self.root.configure(bg="#YourColorHere")
```

### Adjust Window Size

Change dimensions in the `__init__` method:

```python
self.root.geometry("600x800")  # Width x Height
```

## 🐛 Troubleshooting

### "Location detection failed"
- Check your internet connection
- Ensure firewall isn't blocking the app
- Try manual city search instead

### "Could not fetch weather data"
- Verify internet connectivity
- The API might be temporarily unavailable
- Try searching for a different location

### Module Not Found Error
```bash
pip install --upgrade requests
```

## 🙏 Acknowledgments

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Location services by [IP-API](https://ip-api.com/)

## 📞 Contact

Have questions or suggestions? Feel free to open an issue or reach out!

---

**Made with ❤️ using Python and Tkinter**

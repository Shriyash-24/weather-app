import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("500x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#2C3E50")
        
        # API endpoints (using free services)
        self.weather_api = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_api = "https://geocoding-api.open-meteo.com/v1/search"
        self.ip_location_api = "http://ip-api.com/json/"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#34495E", pady=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🌤️ Weather Dashboard",
            font=("Helvetica", 24, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack()
        
        # Search Frame
        search_frame = tk.Frame(self.root, bg="#2C3E50", pady=15)
        search_frame.pack(fill=tk.X, padx=20)
        
        self.location_entry = tk.Entry(
            search_frame,
            font=("Helvetica", 12),
            width=30,
            relief=tk.FLAT,
            bg="white"
        )
        self.location_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.location_entry.insert(0, "Enter city name...")
        self.location_entry.bind("<FocusIn>", self.clear_placeholder)
        self.location_entry.bind("<Return>", lambda e: self.search_weather())
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Helvetica", 11, "bold"),
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.search_weather,
            padx=20,
            pady=8
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        auto_btn = tk.Button(
            search_frame,
            text="📍 Auto",
            font=("Helvetica", 11, "bold"),
            bg="#27AE60",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.auto_detect_location,
            padx=15,
            pady=8
        )
        auto_btn.pack(side=tk.LEFT)
        
        # Loading Label
        self.loading_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 10),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.loading_label.pack()
        
        # Main Weather Display Frame
        self.weather_frame = tk.Frame(self.root, bg="#2C3E50")
        self.weather_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Location Display
        self.location_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Helvetica", 20, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        self.location_label.pack(pady=(10, 5))
        
        # Date/Time Display
        self.datetime_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Helvetica", 11),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        self.datetime_label.pack()
        
        # Temperature Display
        self.temp_frame = tk.Frame(self.weather_frame, bg="#34495E", pady=20)
        self.temp_frame.pack(fill=tk.X, pady=20)
        
        self.temp_label = tk.Label(
            self.temp_frame,
            text="--°C",
            font=("Helvetica", 48, "bold"),
            bg="#34495E",
            fg="white"
        )
        self.temp_label.pack()
        
        self.condition_label = tk.Label(
            self.temp_frame,
            text="",
            font=("Helvetica", 16),
            bg="#34495E",
            fg="#ECF0F1"
        )
        self.condition_label.pack()
        
        # Weather Details Grid
        details_frame = tk.Frame(self.weather_frame, bg="#2C3E50")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Create 2x3 grid for weather details
        self.details_widgets = {}
        details = [
            ("💨 Wind", "wind"),
            ("💧 Humidity", "humidity"),
            ("🌡️ Feels Like", "feels_like"),
            ("☁️ Cloud Cover", "cloud"),
            ("👁️ Visibility", "visibility"),
            ("🌅 UV Index", "uv")
        ]
        
        for i, (label, key) in enumerate(details):
            row = i // 2
            col = i % 2
            
            detail_frame = tk.Frame(details_frame, bg="#34495E", relief=tk.FLAT)
            detail_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            title = tk.Label(
                detail_frame,
                text=label,
                font=("Helvetica", 10),
                bg="#34495E",
                fg="#BDC3C7",
                anchor="w"
            )
            title.pack(fill=tk.X, padx=10, pady=(10, 2))
            
            value = tk.Label(
                detail_frame,
                text="--",
                font=("Helvetica", 14, "bold"),
                bg="#34495E",
                fg="white",
                anchor="w"
            )
            value.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            self.details_widgets[key] = value
        
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)
        
        # Footer
        footer = tk.Label(
            self.root,
            text="Data provided by Open-Meteo API",
            font=("Helvetica", 8),
            bg="#2C3E50",
            fg="#7F8C8D"
        )
        footer.pack(side=tk.BOTTOM, pady=10)
        
        # Auto-detect location on startup
        self.root.after(100, self.auto_detect_location)
    
    def clear_placeholder(self, event):
        if self.location_entry.get() == "Enter city name...":
            self.location_entry.delete(0, tk.END)
    
    def show_loading(self, message="Loading..."):
        self.loading_label.config(text=message)
        self.root.update()
    
    def hide_loading(self):
        self.loading_label.config(text="")
    
    def auto_detect_location(self):
        def detect():
            try:
                self.show_loading("🌍 Detecting your location...")
                response = requests.get(self.ip_location_api, timeout=5)
                data = response.json()
                
                if data['status'] == 'success':
                    lat = data['lat']
                    lon = data['lon']
                    city = data['city']
                    country = data['country']
                    
                    self.root.after(0, lambda: self.fetch_weather(lat, lon, f"{city}, {country}"))
                else:
                    self.root.after(0, lambda: self.show_error("Could not detect location"))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Location detection failed: {str(e)}"))
            finally:
                self.root.after(0, self.hide_loading)
        
        thread = threading.Thread(target=detect, daemon=True)
        thread.start()
    
    def search_weather(self):
        location = self.location_entry.get().strip()
        if not location or location == "Enter city name...":
            messagebox.showwarning("Input Required", "Please enter a city name")
            return
        
        def search():
            try:
                self.show_loading(f"🔍 Searching for {location}...")
                
                # Geocode the location
                params = {"name": location, "count": 1, "language": "en", "format": "json"}
                response = requests.get(self.geocoding_api, params=params, timeout=5)
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    result = data['results'][0]
                    lat = result['latitude']
                    lon = result['longitude']
                    name = result['name']
                    country = result.get('country', '')
                    
                    location_name = f"{name}, {country}" if country else name
                    self.root.after(0, lambda: self.fetch_weather(lat, lon, location_name))
                else:
                    self.root.after(0, lambda: self.show_error("Location not found"))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Search failed: {str(e)}"))
            finally:
                self.root.after(0, self.hide_loading)
        
        thread = threading.Thread(target=search, daemon=True)
        thread.start()
    
    def fetch_weather(self, lat, lon, location_name):
        def fetch():
            try:
                self.show_loading("☁️ Fetching weather data...")
                
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,cloud_cover,wind_speed_10m,weather_code",
                    "timezone": "auto"
                }
                
                response = requests.get(self.weather_api, params=params, timeout=5)
                data = response.json()
                
                if 'current' in data:
                    self.root.after(0, lambda: self.display_weather(data, location_name))
                else:
                    self.root.after(0, lambda: self.show_error("Could not fetch weather data"))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Weather fetch failed: {str(e)}"))
            finally:
                self.root.after(0, self.hide_loading)
        
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()
    
    def get_weather_description(self, code):
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")
    
    def display_weather(self, data, location_name):
        current = data['current']
        
        # Update location
        self.location_label.config(text=location_name)
        
        # Update date/time
        now = datetime.now()
        self.datetime_label.config(text=now.strftime("%A, %B %d, %Y • %I:%M %p"))
        
        # Update temperature
        temp = current['temperature_2m']
        self.temp_label.config(text=f"{temp:.1f}°C")
        
        # Update condition
        weather_code = current.get('weather_code', 0)
        condition = self.get_weather_description(weather_code)
        self.condition_label.config(text=condition)
        
        # Update details
        self.details_widgets['wind'].config(text=f"{current['wind_speed_10m']:.1f} km/h")
        self.details_widgets['humidity'].config(text=f"{current['relative_humidity_2m']}%")
        self.details_widgets['feels_like'].config(text=f"{current['apparent_temperature']:.1f}°C")
        self.details_widgets['cloud'].config(text=f"{current['cloud_cover']}%")
        self.details_widgets['visibility'].config(text="Good")
        self.details_widgets['uv'].config(text="Moderate")
    
    def show_error(self, message):
        self.hide_loading()
        messagebox.showerror("Error", message)

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
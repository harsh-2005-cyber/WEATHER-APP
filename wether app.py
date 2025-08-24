import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import os

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # API Configuration
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Colors
        self.bg_color = "#87CEEB"
        self.text_color = "#333333"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Weather App", 
                             font=("Arial", 24, "bold"), 
                             bg=self.bg_color, fg=self.text_color)
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg=self.bg_color)
        search_frame.pack(pady=10)
        
        self.city_entry = tk.Entry(search_frame, font=("Arial", 14), width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", 
                                command=self.get_weather,
                                font=("Arial", 12), bg="#4CAF50", fg="white")
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Weather display frame
        self.weather_frame = tk.Frame(main_frame, bg="white", 
                                   relief=tk.RAISED, borderwidth=2)
        self.weather_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Weather info labels
        self.city_label = tk.Label(self.weather_frame, text="", 
                                font=("Arial", 18, "bold"), bg="white")
        self.city_label.pack(pady=10)
        
        self.temp_label = tk.Label(self.weather_frame, text="", 
                                font=("Arial", 24), bg="white")
        self.temp_label.pack(pady=5)
        
        self.desc_label = tk.Label(self.weather_frame, text="", 
                                font=("Arial", 14), bg="white")
        self.desc_label.pack(pady=5)
        
        self.humidity_label = tk.Label(self.weather_frame, text="", 
                                      font=("Arial", 12), bg="white")
        self.humidity_label.pack(pady=5)
        
        self.wind_label = tk.Label(self.weather_frame, text="", 
                                 font=("Arial", 12), bg="white")
        self.wind_label.pack(pady=5)
        
        self.time_label = tk.Label(self.weather_frame, text="", 
                                  font=("Arial", 10), bg="white")
        self.time_label.pack(pady=5)
        
    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        try:
            # Construct API URL
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Update UI with weather data
            self.update_weather_display(data)
            
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Failed to connect to weather service. Please check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messagebox.showerror("Error", "City not found. Please check the city name.")
            elif e.response.status_code == 401:
                messagebox.showerror("Error", "Invalid API key. Please check your configuration.")
            else:
                messagebox.showerror("Error", f"HTTP Error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid response format: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def update_weather_display(self, data):
        # Extract weather information
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']
        
        # Update labels
        self.city_label.config(text=f"{city_name}, {country}")
        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=description)
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        self.wind_label.config(text=f"Wind: {wind_speed} m/s")
        
        # Update time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Last updated: {current_time}")
        
        # Change background based on weather
        weather_main = data['weather'][0]['main'].lower()
        self.set_background_color(weather_main)
    
    def set_background_color(self, weather_condition):
        color_map = {
            'clear': "#87CEEB",
            'clouds': "#B0C4DE",
            'rain': "#708090",
            'snow': "#F0F8FF",
            'thunderstorm': "#4B0082",
            'drizzle': "#D3D3D3",
            'mist': "#DCDCDC",
            'fog': "#DCDCDC"
        }
        
        color = color_map.get(weather_condition, "#87CEEB")
        self.root.configure(bg=color)
        
        # Update all frames with new color
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child != self.temp_label:
                        child.configure(bg=color)

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

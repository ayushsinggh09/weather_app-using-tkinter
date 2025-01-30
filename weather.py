import tkinter as tk
from tkinter import Frame
import requests
from PIL import Image, ImageTk
from io import BytesIO
#api keys :2b7132983f7a12072e5f41122b32a695
#api url :https://api.openweathermap.org/data/2.5/weather
#icon :http://openweathermap.org/img/wn/{icon_code}@2x.png
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x500")

        self.weather_key = '2b7132983f7a12072e5f41122b32a695'
        self.api_url = 'https://api.openweathermap.org/data/2.5/weather'

        self.image_path = r"C:\Users\ayush\OneDrive\Desktop\Python project\venv\Scripts\1738262629657.jpg"
        self.pil_image = Image.open(self.image_path)
        self.pil_image = self.pil_image.resize((600, 500), Image.Resampling.LANCZOS)
        self.img_photo = ImageTk.PhotoImage(self.pil_image)

        self.bg_lbl = tk.Label(root, image=self.img_photo)
        self.bg_lbl.place(x=0, y=0, width=600, height=500)

        self.frame_one = Frame(self.bg_lbl, bg="blue", bd=5)
        self.frame_one.place(x=80, y=60, width=450, height=50)
        # widget
        self.txt_box = tk.Entry(self.frame_one, font=('Times New Roman', 16), width=20)
        self.txt_box.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Button
        self.btn = tk.Button(self.frame_one, text='Get Weather', fg='black', font=('Times New Roman', 17, 'bold'), command=self.get_weather)
        self.btn.grid(row=0, column=1, padx=10)

        # Second frame 
        self.frame_two = Frame(self.bg_lbl, bg="blue", bd=5)
        self.frame_two.place(x=80, y=130, width=450, height=300)

        self.result_label = tk.Label(self.frame_two, font=('Times New Roman', 16), bg='white', wraplength=400, justify="left", anchor="nw")
        self.result_label.place(relwidth=1, relheight=1)

        self.icon_label = tk.Label(self.frame_two, bg='white')
        self.icon_label.place(x=350, y=10)  

    def format_response(self, weather):
        try:
            city = weather['name']
            condition = weather['weather'][0]['description']
            temp = weather['main']['temp']
            icon_code = weather['weather'][0]['icon']
            final_str = f"City: {city}\nCondition: {condition}\nTemperature: {temp}C"
            return final_str, icon_code
        except:
            return 'There was a problem retrieving that information', None

    def get_weather(self):
        city = self.txt_box.get()
        if not city:
            self.result_label.config(text="Please enter a city name", fg="black")
            return

        params = {'q': city, 'appid': self.weather_key, 'units': 'metric'}
        response = requests.get(self.api_url, params=params)
        weather = response.json()

        if response.status_code == 200:
            formatted_weather, icon_code = self.format_response(weather)
            self.result_label.config(text=formatted_weather, fg="black")

            if icon_code:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_response = requests.get(icon_url)
                icon_data = icon_response.content
                icon_image = Image.open(BytesIO(icon_data))
                icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.icon_label.config(image=icon_photo)
                self.icon_label.image = icon_photo 
        else:
            self.result_label.config(text="Failed to retrieve weather data", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
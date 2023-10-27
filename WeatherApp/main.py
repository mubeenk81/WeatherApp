from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

# Create the Tkinter root window
app = Tk()
app.title("Weather App")
app.geometry("400x400")

# Load the moving GIF image
gif = Image.open("cloud.gif")
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

# Create a Label widget to display the GIF frames as the background
bg_label = Label(app)
bg_label.place(relwidth=1, relheight=1)
bg_label.lower()

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

# Extract the API key from the configuration file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['gfg']['api']
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Explicit function to get weather details
def getweather(city):
    result = requests.get(url.format(city, api_key))

    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = round(temp_kelvin - 273.15, 2)
        weather1 = json['weather'][0]['description']
        feels_like = json['main']['feels_like']
        feels_like_celsius = round(feels_like - 273.15, 2)
        wind_speed = json['wind']['speed']
        final = [city, country, temp_celsius, weather1, feels_like_celsius, wind_speed]
        return final
    else:
        print("No Content Found")

# Explicit function to search city
def search():
    city = city_text.get()
    weather = getweather(city)
    if weather:
        location_lbl.config(text='{}, {}'.format(weather[0], weather[1]))
        temperature_label.config(text='Temperature: {}°C'.format(weather[2]))
        weather_label.config(text='Weather: {}'.format(weather[3]))
        feels_like_label.config(text='Feels Like: {}°C'.format(weather[4]))
        wind_speed_label.config(text='Wind Speed: {} m/s'.format(weather[5]))
    else:
        messagebox.showerror('Error', "Cannot find {}".format(city))

# Add labels, buttons, and text
search_btn = Button(app, text="Search Weather", width=15, command=search)
search_btn.pack()

location_lbl = Label(app, text="Location", font=('bold', 20))
location_lbl.pack()

temperature_label = Label(app, text="")
temperature_label.pack()

weather_label = Label(app, text="")
weather_label.pack()

feels_like_label = Label(app, text="")
feels_like_label.pack()

wind_speed_label = Label(app, text="")
wind_speed_label.pack()

def on_enter(event):
    search()

# Bind the Enter key to the search function
app.bind('<Return>', on_enter)

# Function to update the GIF
def update_gif(index=0):
    frame = frames[index]
    bg_label.configure(image=frame)
    app.after(100, update_gif, (index + 1) % len(frames))  # 100ms delay for the next frame

# Start the GIF animation
update_gif()

app.mainloop()

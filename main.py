import tkinter as tk
import requests
from PIL import Image, ImageTk, ImageSequence

# Initialize the main window
root = tk.Tk()
root.geometry("550x400")
root.title("WEATHER NOW")

def get_weather(city):
    weather_key = "8217a71a00336faf72711ceebd5644be"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"APPID": weather_key, "q": city, "units": "imperial"}
    
    try:
        response = requests.get(url, params=params)
        weather = response.json()
        
        if response.status_code == 200:
            result["text"] = format_response(weather)
        else:
            result["text"] = "Error fetching weather data. Please try again."
    except requests.exceptions.RequestException as e:
        result["text"] = f"Error: {e}"

def format_response(weather):
    try:
        city = weather["name"]
        description = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]
        final_str = f"City: {city}\nWeather: {description}\nTemperature: {temp} °F"
    except KeyError:
        final_str = "Weather data not found for that location."
    return final_str

# Add a title label with bold font and centered alignment
title_label = tk.Label(root, text="WEATHER NOW", font=("Helvetica", 24, "bold"), fg="#00796B", bg="white")
title_label.pack(side="top", pady=10)

# Load the GIF
gif = Image.open("images/bg.gif")
frames = [ImageTk.PhotoImage(frame.copy().resize((550, 400))) for frame in ImageSequence.Iterator(gif)]

# Create a label to hold the GIF
label = tk.Label(root)
label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to update frames
def update_frame(frame_index):
    frame = frames[frame_index]
    label.configure(image=frame)
    root.after(100, update_frame, (frame_index + 1) % len(frames))

# Start the animation
update_frame(0)

# Create frames for layout
frame_one = tk.Frame(root, bg="#E0F7FA", bd=5)
frame_two = tk.Frame(root, bg="#E0F7FA", bd=5)

# Calculate the horizontal center position dynamically
def center_frame(event=None):
    frame_width = 400
    frame_x = (root.winfo_width() - frame_width) // 2
    frame_one.place(x=frame_x, y=50, width=frame_width, height=100)
    frame_two.place(x=frame_x, y=165, width=frame_width, height=100)  # Adjusted y for 15px space

root.bind('<Configure>', center_frame)

center_frame()

label_one = tk.Label(frame_one, text="Enter city name:", font=("Helvetica", 16, "bold"), fg="#004D40", bg="#E0F7FA")
label_one.grid(row=0, column=0, columnspan=2, pady=10)

entry_box = tk.Entry(frame_one, font=("Helvetica", 12))
entry_box.grid(row=1, column=0, padx=5, pady=5)

button = tk.Button(frame_one, text="Get Weather", font=("Helvetica", 12, "bold"), bg="#00796B", fg="#FFFFFF", command=lambda: get_weather(entry_box.get()))
button.grid(row=1, column=1, padx=5, pady=5)

frame_one.lift()

result = tk.Label(frame_two, font=("Helvetica", 12, "bold"), fg="#004D40", bg="#E0F7FA", wraplength=350, justify="left")
result.place(relwidth=1, relheight=1)

root.mainloop()

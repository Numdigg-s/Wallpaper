import time
import threading
import ctypes
import requests
import os

# Replace with your Unsplash API access key
UNSPLASH_ACCESS_KEY = 'xiKSNi5gaXQxGXgkL10bdR2-Au8QdbtBzZmVh53v4Sc'

# Function to fetch a random wallpaper from Unsplash using the API
def get_random_wallpaper():
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}',
    }
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': 'wallpaper',  # You can adjust the query to your preference
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        download_url = data['urls']['full']
        return download_url
    else:
        print("Failed to fetch wallpaper from Unsplash.")
        return None

# Function to set the wallpaper from an online source
def set_online_wallpaper():
    download_url = get_random_wallpaper()
    if download_url:
        response = requests.get(download_url)
        with open('downloaded_wallpaper.jpg', 'wb') as f:
            f.write(response.content)

        # Set the wallpaper (Windows)
        if os.name == 'nt':
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath('downloaded_wallpaper.jpg'), 3)

# Function to change wallpaper at scheduled intervals
def change_wallpaper_scheduled(interval):
    while True:
        set_online_wallpaper()
        time.sleep(interval)

# Create a thread for scheduled wallpaper changes
default_change_interval = 3600  # Change every 1 hour (3600 seconds)
change_interval = default_change_interval
change_thread = threading.Thread(target=change_wallpaper_scheduled, args=(change_interval,))
change_thread.daemon = True
change_thread.start()

# Initial wallpaper change
set_online_wallpaper()

# Keep the script running
while True:
    pass

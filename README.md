# 🎬 IMDB Movie Player

A simple Linux desktop app to watch movies from IMDB using playimdb.com.

## Features

- 🔍 Search movies by name
- 📋 Paste any IMDB URL directly
- 🌐 Opens videos in your web browser
- 🎨 Clean dark theme interface
- ⭐ Built-in popular movie database

## Installation

### Install Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-3.


## Run the App
cd ~/IMDBPlayer-Linux
python3 src/movie_player_final.py

## Usage
    Search by name: Type movie name (e.g., "Avatar", "Inception")
    Paste URL: Enter any IMDB URL directly
    Popular movies: Click on any popular movie to play


## How It Works
This app is a launcher that:
    Takes a movie name or IMDB URL
    Converts it to playimdb.com format
    Opens it in your default web browser
    Video plays in the browser (Chrome/Firefox)

## Why Browser?
playimdb.com requires JavaScript and a full web browser to display the video player. MPV/VLC cannot play web pages directly.

## Requirements
    Python 3.6+
    GTK 3.0
    Any web browser (Firefox, Chrome, etc.)

## ⚠️ Disclaimer

* This project is intended for **educational purposes only**
* Do not misuse or violate any website's **terms of service**
* Respect copyright laws and content ownership

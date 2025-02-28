# YouTube Video Downloader

YouTube Video Downloader is a Python-based application that allows users to download YouTube videos in various qualities. The application features a modern dark mode UI and provides an easy-to-use interface for selecting video quality and download location.

## Features

- Fetch available video qualities from YouTube
- Download videos in selected quality
- Save downloaded videos to a user-specified directory
- Modern dark mode UI using ttkbootstrap
- Progress bars for each download

## Requirements

- Python 3.x
- `yt-dlp` library
- `ttkbootstrap` library
- `ffmpeg` (Ensure `ffmpeg` is installed and the path is set correctly in the script)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/YTVideoDownloader.git
    cd YTVideoDownloader
    ```

2. Install the required libraries:
    ```bash
    pip install yt-dlp ttkbootstrap
    ```

3. Ensure `ffmpeg` is installed and the path is set correctly in the script:
    ```python
    'ffmpeg_location': r'C:\\ffmpeg\\bin\\ffmpeg.exe'
    ```

## Usage

1. Run the application:
    ```bash
    python app.py
    ```

2. Enter the YouTube URL in the provided input field.

3. Click on "🔍 Check Available Qualities" to fetch available video qualities.

4. Select the desired video quality from the dropdown menu.

5. Choose the download location by clicking on "📁 Choose Folder".

6. Click on "⬇️ Download Video" to start the download.

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) - A supercharged theme library for ttk

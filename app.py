import yt_dlp
import threading
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Frame
import re

CONFIG_FILE = "config.txt"

# 🔹 Get user's default Downloads folder
def load_last_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return file.read().strip()
    return os.path.join(os.path.expanduser("~"), "Downloads")  # Default to Downloads

# 🔹 Save folder selection
def save_folder(path):
    with open(CONFIG_FILE, "w") as file:
        file.write(path)

# 🔹 Default folder (last used or Downloads)
DEFAULT_DOWNLOAD_PATH = load_last_folder()

# 🔹 Fetch available video qualities
def get_video_qualities():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            available_qualities = {}
            for f in formats:
                height = f.get('height')
                if height and height >= 144 and height not in available_qualities:
                    available_qualities[height] = f['format_id']

            # 🔹 Sort resolutions from lowest to highest
            sorted_qualities = sorted(available_qualities.items())

            # 🔹 Update dropdown menu
            quality_dropdown["values"] = [f"{h}p" for h, _ in sorted_qualities]


            quality_var.set(f"{sorted_qualities[-1][0]}p")  # Auto-select highest quality
            format_map.clear()
            format_map.update(sorted_qualities)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch qualities: {e}")

# 🔹 Opens a dialog to choose download directory
def choose_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)
        save_folder(folder_selected)  # Save selection

# 🔹 Start download in a separate thread
def start_download():
    threading.Thread(target=download_video, daemon=True).start()

# 🔹 Download video and create a progress bar for each video
def download_video():
    url = url_entry.get()
    download_path = path_var.get() or DEFAULT_DOWNLOAD_PATH  # Default to Downloads if not selected
    selected_quality = quality_var.get().replace("p", "")

    if not url:
        messagebox.showerror("Error", "Please enter a video URL")
        return
    if not selected_quality:
        messagebox.showerror("Error", "Please select a video quality")
        return

    format_id = format_map.get(int(selected_quality))
    if not format_id:
        messagebox.showerror("Error", "Invalid quality selection")
        return

    # 🔹 Create a new frame for this specific download
    download_frame = Frame(downloads_container, height=100)
    download_frame.pack(fill="x", pady=5, padx=10)

    # 🔹 Extract the video title for UI display
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown Video')
    except Exception:
        video_title = "Unknown Video"

    # 🔹 Left side: Video details
    details_label = ttk.Label(download_frame, text=f"{video_title} - {selected_quality}p", font=("Arial", 10))
    details_label.pack(side="left", padx=10)

    # 🔹 Right side: Download progress bar
    progress_bar = ttk.Progressbar(download_frame, length=300, mode="determinate", bootstyle="success-striped")
    progress_bar.pack(side="right", padx=10, pady=5)

    # 🔹 Progress hook to update the specific progress bar
    def hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('_percent_str', '0.0%')
            downloaded = re.sub(r'\x1b\[[0-9;]*m', '', downloaded)  # Remove ANSI escape codes
            downloaded = downloaded.strip('%')
            try:
                progress_bar["value"] = float(downloaded)
            except ValueError:
                pass
        elif d['status'] == 'finished':
            details_label.config(text=f"{video_title} - Download Complete ✅")

    options = {
        'format': f"{format_id}+bestaudio",
        'outtmpl': f"{download_path}/%(title)s.%(ext)s",
        'merge_output_format': 'mp4',
        'ffmpeg_location': r'C:\\ffmpeg\bin\\ffmpeg.exe',  # 🔹 Set full path to ffmpeg
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
            {'key': 'FFmpegEmbedSubtitle'},
        ],
        'progress_hooks': [hook],
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        details_label.config(text=f"{video_title} - Download Failed ❌")
        messagebox.showerror("Error", f"Download failed: {e}")




# 🔹 UI Setup - Modern Dark Mode
root = ttk.Window(themename="darkly")  # Cool modern UI
root.title("🎬 4K Video Downloader")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.state("zoomed")
root.resizable(True, True)

path_var = ttk.StringVar(value=DEFAULT_DOWNLOAD_PATH)

# 🔹 Stylish Header
ttk.Label(root, text="🎬 4K Video Downloader", font=("Arial", 16, "bold"), bootstyle="primary").pack(pady=20)

# 🔹 URL Entry
ttk.Label(root, text="Enter YouTube URL:", font=("Arial", 12), bootstyle="light").pack(pady=5, padx=30)
url_entry = ttk.Entry(root, width=70, font=("Arial", 12), bootstyle="info")
url_entry.pack(pady=5, padx=10)

# 🔹 Fetch Quality Button
ttk.Button(root, text="🔍 Check Available Qualities", bootstyle="primary-outline", command=get_video_qualities).pack(pady=5)

# 🔹 Quality Dropdown
quality_var = ttk.StringVar()
quality_dropdown = ttk.Combobox(root, textvariable=quality_var, state="readonly", font=("Arial", 12), bootstyle="info")
quality_dropdown.pack(pady=5, padx=10)
format_map = {}

# 🔹 Choose Folder Button
ttk.Button(root, text="📁 Choose Folder", bootstyle="secondary-outline", command=choose_directory).pack(pady=5)
ttk.Label(root, text=f"Download Location:", font=("Arial", 10), bootstyle="light").pack()
ttk.Label(root, textvariable=path_var, font=("Arial", 10), bootstyle="info").pack(pady=5)

# 🔹 Download Button
ttk.Button(root, text="⬇️ Download Video", bootstyle="success-outline", command=start_download).pack(pady=10)

# 🔹 Container for download progress bars
downloads_container = ttk.Frame(root)
downloads_container.pack(fill="both", expand=True, pady=40, padx=30)

# 🔹 Run the GUI
root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import yt_dlp
from datetime import datetime
import re

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Biến để lưu trạng thái
        self.downloading = False
        self.output_path = "./downloads"
        
        # Tạo thư mục downloads mặc định nếu chưa tồn tại
        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
        except Exception as e:
            print(f"Không thể tạo thư mục downloads: {e}")
            self.output_path = "."
        
        self.setup_ui()
        
    def is_valid_youtube_url(self, url):
        """Kiểm tra URL YouTube hợp lệ"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/channel/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/@[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/c/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/user/[\w-]+',
            r'(?:https?://)?youtu\.be/[\w-]+',
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
        
    def setup_ui(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Tab control
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure notebook to expand
        main_frame.rowconfigure(1, weight=1)
        
        # Create tabs
        self.create_single_video_tab()
        self.create_playlist_tab()
        self.create_channel_tab()
        self.create_batch_tab()
        
        # Output directory
        ttk.Label(main_frame, text="Thư mục lưu:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.output_var = tk.StringVar(value=self.output_path)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(10, 5))
        
        browse_btn = ttk.Button(main_frame, text="Chọn thư mục", command=self.browse_output_dir)
        browse_btn.grid(row=2, column=2, pady=(10, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def create_single_video_tab(self):
        """Tab tải video đơn lẻ"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Video Đơn")
        
        # URL input
        ttk.Label(tab, text="URL Video:").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(tab, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=(10, 5))
        
        # Quality selection
        ttk.Label(tab, text="Chất lượng:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(tab, textvariable=self.quality_var, 
                                    values=["best", "1080p", "720p", "480p", "worst"], 
                                    state="readonly", width=15)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 5))
        
        # Download button
        download_btn = ttk.Button(tab, text="Tải Video", command=self.download_single_video)
        download_btn.grid(row=1, column=2, padx=(10, 0), pady=(10, 5))
        
        # Check formats button
        check_btn = ttk.Button(tab, text="Kiểm tra chất lượng", command=self.check_formats)
        check_btn.grid(row=2, column=2, padx=(10, 0), pady=(5, 10))
        
        # Configure grid
        tab.columnconfigure(1, weight=1)
        
    def create_playlist_tab(self):
        """Tab tải playlist"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Playlist")
        
        # URL input
        ttk.Label(tab, text="URL Playlist:").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.playlist_url_var = tk.StringVar()
        playlist_entry = ttk.Entry(tab, textvariable=self.playlist_url_var, width=60)
        playlist_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=(10, 5))
        
        # Download button
        download_btn = ttk.Button(tab, text="Tải Playlist", command=self.download_playlist)
        download_btn.grid(row=1, column=2, padx=(10, 0), pady=(10, 5))
        
        # Configure grid
        tab.columnconfigure(1, weight=1)
        
    def create_channel_tab(self):
        """Tab tải video từ kênh"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Kênh")
        
        # Channel URL input
        ttk.Label(tab, text="URL Kênh:").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.channel_url_var = tk.StringVar()
        channel_entry = ttk.Entry(tab, textvariable=self.channel_url_var, width=60)
        channel_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=(10, 5))
        
        # Number of videos
        ttk.Label(tab, text="Số video:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        self.video_count_var = tk.StringVar(value="10")
        count_entry = ttk.Entry(tab, textvariable=self.video_count_var, width=10)
        count_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 5))
        
        # Sort type
        ttk.Label(tab, text="Sắp xếp:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.sort_var = tk.StringVar(value="newest")
        sort_combo = ttk.Combobox(tab, textvariable=self.sort_var, 
                                 values=["newest", "oldest", "popular"], 
                                 state="readonly", width=15)
        sort_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 5))
        
        # Buttons
        preview_btn = ttk.Button(tab, text="Xem trước", command=self.preview_channel)
        preview_btn.grid(row=1, column=2, padx=(10, 0), pady=(10, 5))
        
        download_btn = ttk.Button(tab, text="Tải Video", command=self.download_channel)
        download_btn.grid(row=2, column=2, padx=(10, 0), pady=(10, 5))
        
        # Configure grid
        tab.columnconfigure(1, weight=1)
        
    def create_batch_tab(self):
        """Tab tải nhiều video"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Tải Hàng Loạt")
        
        # URLs input
        ttk.Label(tab, text="Danh sách URLs (mỗi URL một dòng):").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.urls_text = scrolledtext.ScrolledText(tab, height=8, width=70)
        self.urls_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                           padx=(0, 0), pady=(5, 10))
        
        # Quality selection
        ttk.Label(tab, text="Chất lượng:").grid(row=2, column=0, sticky=tk.W, pady=(5, 5))
        
        self.batch_quality_var = tk.StringVar(value="best")
        batch_quality_combo = ttk.Combobox(tab, textvariable=self.batch_quality_var, 
                                          values=["best", "1080p", "720p", "480p", "worst"], 
                                          state="readonly", width=15)
        batch_quality_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 5))
        
        # Download button
        download_btn = ttk.Button(tab, text="Tải Tất Cả", command=self.download_batch)
        download_btn.grid(row=2, column=2, padx=(10, 0), pady=(5, 5))
        
        # Configure grid
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        
    def browse_output_dir(self):
        """Chọn thư mục lưu file"""
        directory = filedialog.askdirectory(initialdir=self.output_path)
        if directory:
            self.output_path = directory
            self.output_var.set(directory)
            self.log_message(f"Đã chọn thư mục lưu: {directory}")
            
    def log_message(self, message):
        """Ghi log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Cập nhật status"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def download_single_video(self):
        """Tải video đơn lẻ"""
        if self.downloading:
            messagebox.showwarning("Đang tải", "Vui lòng đợi tải xong!")
            return
            
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL video!")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Lỗi", "URL không hợp lệ! Vui lòng nhập URL YouTube đúng định dạng.")
            return
            
        self.downloading = True
        self.update_status("Đang tải video...")
        self.progress_var.set(0)
        
        def download_thread():
            try:
                self.log_message(f"Bắt đầu tải: {url}")
                
                # Tạo thư mục nếu chưa tồn tại
                try:
                    if not os.path.exists(self.output_path):
                        os.makedirs(self.output_path)
                        self.log_message(f"Đã tạo thư mục: {self.output_path}")
                except Exception as e:
                    self.log_message(f"Lỗi khi tạo thư mục: {str(e)}")
                    messagebox.showerror("Lỗi", f"Không thể tạo thư mục: {str(e)}")
                    return
                
                # Cấu hình yt-dlp
                quality = self.quality_var.get()
                if quality == "best":
                    format_selector = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                elif quality == "1080p":
                    format_selector = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"
                elif quality == "720p":
                    format_selector = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"
                elif quality == "480p":
                    format_selector = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"
                else:
                    format_selector = quality
                
                ydl_opts = {
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                    'format': format_selector,
                    'merge_output_format': 'mp4',
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    self.log_message(f"Tiêu đề: {info.get('title', 'N/A')}")
                    self.log_message(f"Độ dài: {info.get('duration', 'N/A')} giây")
                    self.log_message(f"Kênh: {info.get('uploader', 'N/A')}")
                    
                    ydl.download([url])
                    
                self.log_message("✓ Tải thành công!")
                self.update_status("Tải thành công!")
                messagebox.showinfo("Thành công", "Tải video thành công!")
                
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                self.log_message(f"✗ {error_msg}")
                self.update_status("Tải thất bại!")
                messagebox.showerror("Lỗi", error_msg)
            finally:
                self.downloading = False
                self.progress_var.set(0)
                
        threading.Thread(target=download_thread, daemon=True).start()
        
    def check_formats(self):
        """Kiểm tra chất lượng có sẵn"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL video!")
            return
            
        def check_thread():
            try:
                self.log_message("Đang kiểm tra các format có sẵn...")
                
                ydl_opts = {
                    'listformats': True,
                    'quiet': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    
                    self.log_message(f"Tiêu đề: {info.get('title', 'N/A')}")
                    self.log_message("=" * 50)
                    self.log_message("CÁC CHẤT LƯỢNG VIDEO CÓ SẴN:")
                    
                    video_formats = []
                    audio_formats = []
                    
                    for f in formats:
                        if f.get('vcodec') != 'none' and f.get('height'):
                            video_formats.append(f)
                        elif f.get('acodec') != 'none' and not f.get('height'):
                            audio_formats.append(f)
                    
                    for f in sorted(video_formats, key=lambda x: x.get('height', 0), reverse=True):
                        fps = f"@{f.get('fps')}fps" if f.get('fps') else ""
                        size = f" ({f.get('filesize_approx', 'Unknown size')} bytes)" if f.get('filesize_approx') else ""
                        self.log_message(f"- {f.get('height')}p{fps} ({f.get('ext')}) - {f.get('format_note', '')}{size}")
                    
                    self.log_message("\nCÁC CHẤT LƯỢNG AUDIO:")
                    for f in audio_formats[:5]:
                        bitrate = f.get('abr', 'Unknown')
                        self.log_message(f"- {f.get('ext')} - {bitrate}kbps")
                        
            except Exception as e:
                self.log_message(f"Lỗi khi kiểm tra formats: {str(e)}")
                
        threading.Thread(target=check_thread, daemon=True).start()
        
    def download_playlist(self):
        """Tải playlist"""
        if self.downloading:
            messagebox.showwarning("Đang tải", "Vui lòng đợi tải xong!")
            return
            
        url = self.playlist_url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL playlist!")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Lỗi", "URL playlist không hợp lệ! Vui lòng nhập URL YouTube đúng định dạng.")
            return
            
        self.downloading = True
        self.update_status("Đang tải playlist...")
        self.progress_var.set(0)
        
        def download_thread():
            try:
                self.log_message(f"Bắt đầu tải playlist: {url}")
                
                if not os.path.exists(self.output_path):
                    os.makedirs(self.output_path)
                
                ydl_opts = {
                    'outtmpl': os.path.join(self.output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
                self.log_message("✓ Tải playlist thành công!")
                self.update_status("Tải playlist thành công!")
                messagebox.showinfo("Thành công", "Tải playlist thành công!")
                
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                self.log_message(f"✗ {error_msg}")
                self.update_status("Tải playlist thất bại!")
                messagebox.showerror("Lỗi", error_msg)
            finally:
                self.downloading = False
                self.progress_var.set(0)
                
        threading.Thread(target=download_thread, daemon=True).start()
        
    def preview_channel(self):
        """Xem trước video của kênh"""
        url = self.channel_url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL kênh!")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Lỗi", "URL kênh không hợp lệ! Vui lòng nhập URL YouTube đúng định dạng.")
            return
            
        try:
            limit = int(self.video_count_var.get())
        except ValueError:
            limit = 10
            
        sort_type = self.sort_var.get()
        
        def preview_thread():
            try:
                self.log_message("Đang xem trước video của kênh...")
                
                # Xử lý URL kênh
                if "/channel/" in url:
                    base_url = url
                elif "/@" in url:
                    base_url = url
                elif "/c/" in url:
                    base_url = url
                elif "/user/" in url:
                    base_url = url
                else:
                    self.log_message("URL kênh không hợp lệ!")
                    return
                
                if not base_url.endswith('/videos'):
                    if base_url.endswith('/'):
                        video_url = base_url + "videos"
                    else:
                        video_url = base_url + "/videos"
                else:
                    video_url = base_url
                
                ydl_opts = {
                    'quiet': True,
                    'extract_flat': True,
                    'playlistend': limit,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    final_url = f"{video_url}?sort={sort_type}"
                    info = ydl.extract_info(final_url, download=False)
                    
                    if 'entries' in info:
                        channel_name = info.get('uploader', 'Unknown Channel')
                        self.log_message(f"Kênh: {channel_name}")
                        self.log_message(f"Xem trước {limit} video {sort_type}:")
                        self.log_message("=" * 70)
                        
                        for i, entry in enumerate(list(info['entries'])[:limit], 1):
                            title = entry.get('title', 'No title')
                            duration = entry.get('duration_string', 'Unknown')
                            upload_date = entry.get('upload_date', 'Unknown')
                            
                            if upload_date != 'Unknown' and len(upload_date) == 8:
                                formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                            else:
                                formatted_date = upload_date
                            
                            self.log_message(f"{i:2d}. {title[:50]}{'...' if len(title) > 50 else ''}")
                            self.log_message(f"    Ngày: {formatted_date} | Thời lượng: {duration}")
                            self.log_message("")
                    else:
                        self.log_message("Không tìm thấy video nào!")
                        
            except Exception as e:
                self.log_message(f"Lỗi khi xem trước: {str(e)}")
                
        threading.Thread(target=preview_thread, daemon=True).start()
        
    def download_channel(self):
        """Tải video từ kênh"""
        if self.downloading:
            messagebox.showwarning("Đang tải", "Vui lòng đợi tải xong!")
            return
            
        url = self.channel_url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL kênh!")
            return
            
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Lỗi", "URL kênh không hợp lệ! Vui lòng nhập URL YouTube đúng định dạng.")
            return
            
        try:
            limit = int(self.video_count_var.get())
        except ValueError:
            limit = 10
            
        sort_type = self.sort_var.get()
        
        self.downloading = True
        self.update_status("Đang tải video từ kênh...")
        self.progress_var.set(0)
        
        def download_thread():
            try:
                self.log_message(f"Bắt đầu tải {limit} video từ kênh...")
                
                if not os.path.exists(self.output_path):
                    os.makedirs(self.output_path)
                
                # Xử lý URL kênh
                if "/channel/" in url:
                    base_url = url
                elif "/@" in url:
                    base_url = url
                elif "/c/" in url:
                    base_url = url
                elif "/user/" in url:
                    base_url = url
                else:
                    self.log_message("URL kênh không hợp lệ!")
                    return
                
                if not base_url.endswith('/videos'):
                    if base_url.endswith('/'):
                        video_url = base_url + "videos"
                    else:
                        video_url = base_url + "/videos"
                else:
                    video_url = base_url
                
                ydl_opts = {
                    'outtmpl': os.path.join(self.output_path, '%(uploader)s - %(title)s.%(ext)s'),
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'playlistend': limit,
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    final_url = f"{video_url}?sort={sort_type}"
                    ydl.download([final_url])
                    
                self.log_message("✓ Tải video từ kênh thành công!")
                self.update_status("Tải video từ kênh thành công!")
                messagebox.showinfo("Thành công", "Tải video từ kênh thành công!")
                
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                self.log_message(f"✗ {error_msg}")
                self.update_status("Tải video từ kênh thất bại!")
                messagebox.showerror("Lỗi", error_msg)
            finally:
                self.downloading = False
                self.progress_var.set(0)
                
        threading.Thread(target=download_thread, daemon=True).start()
        
    def download_batch(self):
        """Tải nhiều video"""
        if self.downloading:
            messagebox.showwarning("Đang tải", "Vui lòng đợi tải xong!")
            return
            
        urls_text = self.urls_text.get("1.0", tk.END).strip()
        if not urls_text:
            messagebox.showerror("Lỗi", "Vui lòng nhập danh sách URLs!")
            return
            
        # Tách URLs và kiểm tra tính hợp lệ
        url_list = []
        invalid_urls = []
        
        for url in urls_text.split('\n'):
            url = url.strip()
            if url:
                if self.is_valid_youtube_url(url):
                    url_list.append(url)
                else:
                    invalid_urls.append(url)
        
        if invalid_urls:
            invalid_msg = "Các URL không hợp lệ:\n" + "\n".join(invalid_urls[:5])
            if len(invalid_urls) > 5:
                invalid_msg += f"\n... và {len(invalid_urls) - 5} URL khác"
            messagebox.showwarning("Cảnh báo", invalid_msg)
        
        if not url_list:
            messagebox.showerror("Lỗi", "Không có URL hợp lệ nào!")
            return
            
        self.downloading = True
        self.update_status(f"Đang tải {len(url_list)} video...")
        self.progress_var.set(0)
        
        def download_thread():
            try:
                self.log_message(f"Bắt đầu tải {len(url_list)} video...")
                
                if not os.path.exists(self.output_path):
                    os.makedirs(self.output_path)
                
                quality = self.batch_quality_var.get()
                if quality == "best":
                    format_selector = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                elif quality == "1080p":
                    format_selector = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"
                elif quality == "720p":
                    format_selector = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"
                elif quality == "480p":
                    format_selector = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"
                else:
                    format_selector = quality
                
                ydl_opts = {
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                    'format': format_selector,
                    'merge_output_format': 'mp4',
                }
                
                success_count = 0
                failed_count = 0
                
                for i, url in enumerate(url_list, 1):
                    try:
                        self.log_message(f"[{i}/{len(url_list)}] Đang tải: {url}")
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            self.log_message(f"Tiêu đề: {info.get('title', 'N/A')}")
                            
                            ydl.download([url])
                            self.log_message(f"✓ Tải thành công: {info.get('title', 'N/A')}")
                            success_count += 1
                            
                    except Exception as e:
                        self.log_message(f"✗ Lỗi khi tải {url}: {str(e)}")
                        failed_count += 1
                    
                    # Cập nhật progress
                    progress = (i / len(url_list)) * 100
                    self.progress_var.set(progress)
                    self.update_status(f"Đang tải... {i}/{len(url_list)}")
                
                self.log_message(f"\n=== KẾT QUẢ TẢI ===")
                self.log_message(f"Thành công: {success_count}/{len(url_list)}")
                self.log_message(f"Thất bại: {failed_count}/{len(url_list)}")
                
                self.update_status("Tải hàng loạt hoàn thành!")
                messagebox.showinfo("Hoàn thành", f"Tải xong!\nThành công: {success_count}\nThất bại: {failed_count}")
                
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                self.log_message(f"✗ {error_msg}")
                self.update_status("Tải hàng loạt thất bại!")
                messagebox.showerror("Lỗi", error_msg)
            finally:
                self.downloading = False
                self.progress_var.set(0)
                
        threading.Thread(target=download_thread, daemon=True).start()
        
    def progress_hook(self, d):
        """Hook để cập nhật progress bar"""
        try:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_var.set(percentage)
            elif d['status'] == 'finished':
                self.progress_var.set(100)
        except Exception as e:
            # Bỏ qua lỗi progress hook để không ảnh hưởng đến download
            pass

def main():
    """Hàm chính"""
    # Kiểm tra thư viện
    try:
        import yt_dlp
    except ImportError:
        print("Vui lòng cài đặt yt-dlp: pip install yt-dlp")
        sys.exit(1)
    
    try:
        root = tk.Tk()
        app = YouTubeDownloaderGUI(root)
        
        # Thêm xử lý khi đóng cửa sổ
        def on_closing():
            if app.downloading:
                if messagebox.askokcancel("Đang tải", "Đang tải video. Bạn có chắc muốn thoát?"):
                    root.destroy()
            else:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"Lỗi khởi động GUI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
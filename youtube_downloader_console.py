#!/usr/bin/env python3
"""
YouTube Downloader Console Interface
Giao diện console cho YouTube downloader không cần Tcl/Tk
"""

import os
import sys
import yt_dlp
import threading
import time
from datetime import datetime

class YouTubeDownloaderConsole:
    def __init__(self):
        self.output_path = "./downloads"
        self.downloading = False
        
        # Tạo thư mục downloads mặc định
        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
                print(f"✓ Đã tạo thư mục: {self.output_path}")
        except Exception as e:
            print(f"⚠️  Không thể tạo thư mục downloads: {e}")
            self.output_path = "."
    
    def is_valid_youtube_url(self, url):
        """Kiểm tra URL YouTube hợp lệ"""
        import re
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
    
    def log_message(self, message):
        """Ghi log message với timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def download_single_video(self, url, quality="best"):
        """Tải video đơn lẻ"""
        if not self.is_valid_youtube_url(url):
            print("❌ URL không hợp lệ!")
            return False
        
        self.log_message(f"Bắt đầu tải: {url}")
        
        try:
            # Tạo thư mục nếu chưa tồn tại
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            
            # Cấu hình format
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
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.log_message(f"Tiêu đề: {info.get('title', 'N/A')}")
                self.log_message(f"Độ dài: {info.get('duration', 'N/A')} giây")
                self.log_message(f"Kênh: {info.get('uploader', 'N/A')}")
                
                ydl.download([url])
                
            self.log_message("✅ Tải thành công!")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Lỗi: {str(e)}")
            return False
    
    def download_playlist(self, url):
        """Tải playlist"""
        if not self.is_valid_youtube_url(url):
            print("❌ URL playlist không hợp lệ!")
            return False
        
        self.log_message(f"Bắt đầu tải playlist: {url}")
        
        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            
            ydl_opts = {
                'outtmpl': os.path.join(self.output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.log_message("✅ Tải playlist thành công!")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Lỗi: {str(e)}")
            return False
    
    def download_batch(self, urls, quality="best"):
        """Tải nhiều video"""
        if not urls:
            print("❌ Không có URL nào!")
            return
        
        # Lọc URL hợp lệ
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            url = url.strip()
            if url:
                if self.is_valid_youtube_url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
        
        if invalid_urls:
            print(f"⚠️  Các URL không hợp lệ: {invalid_urls}")
        
        if not valid_urls:
            print("❌ Không có URL hợp lệ nào!")
            return
        
        self.log_message(f"Bắt đầu tải {len(valid_urls)} video...")
        
        success_count = 0
        failed_count = 0
        
        for i, url in enumerate(valid_urls, 1):
            self.log_message(f"[{i}/{len(valid_urls)}] Đang tải: {url}")
            
            if self.download_single_video(url, quality):
                success_count += 1
            else:
                failed_count += 1
            
            print("-" * 50)
        
        self.log_message(f"📊 KẾT QUẢ:")
        self.log_message(f"✅ Thành công: {success_count}/{len(valid_urls)}")
        self.log_message(f"❌ Thất bại: {failed_count}/{len(valid_urls)}")
    
    def check_formats(self, url):
        """Kiểm tra chất lượng có sẵn"""
        if not self.is_valid_youtube_url(url):
            print("❌ URL không hợp lệ!")
            return
        
        self.log_message("Đang kiểm tra các format có sẵn...")
        
        try:
            ydl_opts = {
                'listformats': True,
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                print(f"\nTiêu đề: {info.get('title', 'N/A')}")
                print("=" * 50)
                print("CÁC CHẤT LƯỢNG VIDEO CÓ SẴN:")
                
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
                    print(f"- {f.get('height')}p{fps} ({f.get('ext')}) - {f.get('format_note', '')}{size}")
                
                print("\nCÁC CHẤT LƯỢNG AUDIO:")
                for f in audio_formats[:5]:
                    bitrate = f.get('abr', 'Unknown')
                    print(f"- {f.get('ext')} - {bitrate}kbps")
                    
        except Exception as e:
            self.log_message(f"❌ Lỗi khi kiểm tra formats: {str(e)}")
    
    def preview_channel(self, url, limit=10, sort_type="newest"):
        """Xem trước video của kênh"""
        if not self.is_valid_youtube_url(url):
            print("❌ URL kênh không hợp lệ!")
            return
        
        self.log_message("Đang xem trước video của kênh...")
        
        try:
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
                    print(f"\nKênh: {channel_name}")
                    print(f"Xem trước {limit} video {sort_type}:")
                    print("=" * 70)
                    
                    for i, entry in enumerate(list(info['entries'])[:limit], 1):
                        title = entry.get('title', 'No title')
                        duration = entry.get('duration_string', 'Unknown')
                        upload_date = entry.get('upload_date', 'Unknown')
                        
                        if upload_date != 'Unknown' and len(upload_date) == 8:
                            formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                        else:
                            formatted_date = upload_date
                        
                        print(f"{i:2d}. {title[:50]}{'...' if len(title) > 50 else ''}")
                        print(f"    Ngày: {formatted_date} | Thời lượng: {duration}")
                        print()
                else:
                    print("Không tìm thấy video nào!")
                    
        except Exception as e:
            self.log_message(f"❌ Lỗi khi xem trước: {str(e)}")
    
    def download_channel(self, url, limit=10, sort_type="newest"):
        """Tải video từ kênh"""
        if not self.is_valid_youtube_url(url):
            print("❌ URL kênh không hợp lệ!")
            return False
        
        self.log_message(f"Bắt đầu tải {limit} video từ kênh...")
        
        try:
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
                return False
            
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
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                final_url = f"{video_url}?sort={sort_type}"
                ydl.download([final_url])
                
            self.log_message("✅ Tải video từ kênh thành công!")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Lỗi: {str(e)}")
            return False
    
    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*60)
        print("🎬 YOUTUBE VIDEO DOWNLOADER - CONSOLE VERSION")
        print("="*60)
        print("1. Tải video đơn lẻ")
        print("2. Tải playlist")
        print("3. Tải nhiều video")
        print("4. Tải video từ kênh")
        print("5. Xem trước video của kênh")
        print("6. Kiểm tra chất lượng có sẵn")
        print("7. Thay đổi thư mục lưu")
        print("8. Thoát")
        print("="*60)
    
    def run(self):
        """Chạy ứng dụng console"""
        print("🚀 Khởi động YouTube Downloader Console...")
        print(f"📁 Thư mục lưu: {os.path.abspath(self.output_path)}")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nChọn tùy chọn (1-8): ").strip()
                
                if choice == "1":
                    # Tải video đơn lẻ
                    url = input("Nhập URL video: ").strip()
                    if url:
                        quality = input("Chất lượng (best/1080p/720p/480p) [best]: ").strip() or "best"
                        self.download_single_video(url, quality)
                    else:
                        print("❌ Vui lòng nhập URL!")
                
                elif choice == "2":
                    # Tải playlist
                    url = input("Nhập URL playlist: ").strip()
                    if url:
                        self.download_playlist(url)
                    else:
                        print("❌ Vui lòng nhập URL!")
                
                elif choice == "3":
                    # Tải nhiều video
                    print("Nhập danh sách URLs (mỗi URL một dòng, nhập 'done' để kết thúc):")
                    urls = []
                    while True:
                        url = input().strip()
                        if url.lower() == 'done':
                            break
                        if url:
                            urls.append(url)
                    
                    if urls:
                        quality = input("Chất lượng (best/1080p/720p/480p) [best]: ").strip() or "best"
                        self.download_batch(urls, quality)
                    else:
                        print("❌ Không có URL nào!")
                
                elif choice == "4":
                    # Tải video từ kênh
                    url = input("Nhập URL kênh: ").strip()
                    if url:
                        try:
                            limit = int(input("Số video (mặc định 10): ") or "10")
                        except ValueError:
                            limit = 10
                        
                        print("Kiểu sắp xếp:")
                        print("1. Mới nhất (newest)")
                        print("2. Cũ nhất (oldest)")
                        print("3. Xem nhiều nhất (popular)")
                        sort_choice = input("Chọn (1-3) [1]: ").strip() or "1"
                        
                        if sort_choice == "1":
                            sort_type = "newest"
                        elif sort_choice == "2":
                            sort_type = "oldest"
                        elif sort_choice == "3":
                            sort_type = "popular"
                        else:
                            sort_type = "newest"
                        
                        self.download_channel(url, limit, sort_type)
                    else:
                        print("❌ Vui lòng nhập URL!")
                
                elif choice == "5":
                    # Xem trước video của kênh
                    url = input("Nhập URL kênh: ").strip()
                    if url:
                        try:
                            limit = int(input("Số video xem trước (mặc định 10): ") or "10")
                        except ValueError:
                            limit = 10
                        
                        print("Kiểu sắp xếp:")
                        print("1. Mới nhất (newest)")
                        print("2. Cũ nhất (oldest)")
                        print("3. Xem nhiều nhất (popular)")
                        sort_choice = input("Chọn (1-3) [1]: ").strip() or "1"
                        
                        if sort_choice == "1":
                            sort_type = "newest"
                        elif sort_choice == "2":
                            sort_type = "oldest"
                        elif sort_choice == "3":
                            sort_type = "popular"
                        else:
                            sort_type = "newest"
                        
                        self.preview_channel(url, limit, sort_type)
                    else:
                        print("❌ Vui lòng nhập URL!")
                
                elif choice == "6":
                    # Kiểm tra chất lượng
                    url = input("Nhập URL video: ").strip()
                    if url:
                        self.check_formats(url)
                    else:
                        print("❌ Vui lòng nhập URL!")
                
                elif choice == "7":
                    # Thay đổi thư mục lưu
                    new_path = input(f"Thư mục lưu hiện tại: {self.output_path}\nNhập thư mục mới: ").strip()
                    if new_path:
                        try:
                            if not os.path.exists(new_path):
                                os.makedirs(new_path)
                            self.output_path = new_path
                            print(f"✅ Đã thay đổi thư mục lưu: {os.path.abspath(new_path)}")
                        except Exception as e:
                            print(f"❌ Không thể tạo thư mục: {e}")
                    else:
                        print("❌ Vui lòng nhập đường dẫn!")
                
                elif choice == "8":
                    # Thoát
                    print("👋 Tạm biệt!")
                    break
                
                else:
                    print("❌ Lựa chọn không hợp lệ!")
                
            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")

def main():
    """Hàm chính"""
    # Kiểm tra thư viện
    try:
        import yt_dlp
    except ImportError:
        print("❌ Vui lòng cài đặt yt-dlp: pip install yt-dlp")
        sys.exit(1)
    
    try:
        app = YouTubeDownloaderConsole()
        app.run()
    except Exception as e:
        print(f"❌ Lỗi khởi động: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
# -*- coding: utf-8 -*-
r"""
GỘP VIDEO BILIBILI - bản giao diện (build thành file .exe trên Windows)
Cách dùng: bấm đúp file .exe, chọn file Video (hình) + file Audio (tiếng)
(hoặc bấm "Chọn thư mục chứa 2 file" để tool tự nhận diện), chọn thư mục
lưu mặc định, bấm "GỘP VIDEO". Sau khi gộp xong, tool tự tạo thư mục con
tên như video trong thư mục lưu và lưu video hoàn thiện vào đó.
Ví dụ: thư mục lưu = Desktop\Video-Da-Gop, video = "Thanh Dong.mp4"
  -> Desktop\Video-Da-Gop\Thanh Dong\Thanh Dong.mp4
Cần ffmpeg: tool tự tìm ffmpeg trên máy (cùng thư mục với .exe, PATH,
C:\ffmpeg, C:\iContent...). Nếu không thấy sẽ báo link tải.
Viết bởi Gà Con cho CYAN - 17/11/2026
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

APP_TITLE = "Gộp Video Bilibili"
FFMPEG_LINK = "https://www.gyan.dev/ffmpeg/builds/"
MEDIA_EXTS = (".mp4", ".m4a", ".webm", ".mkv")


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def config_path():
    return os.path.join(app_dir(), "config.json")


def mac_dinh_thu_muc_luu():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, "Video-Da-Gop")


def doc_config():
    try:
        with open(config_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def luu_config(cfg):
    try:
        with open(config_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def tim_ffmpeg():
    """Tìm ffmpeg: PATH -> cùng thư mục với tool -> C:\\ffmpeg -> C:\\iContent."""
    p = shutil.which("ffmpeg")
    if p:
        return p
    here = app_dir()
    for cand in (
        os.path.join(here, "ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\iContent\ffmpeg\bin\ffmpeg.exe",
    ):
        if os.path.isfile(cand):
            return cand
    base = r"C:\iContent"
    if os.path.isdir(base):
        for root, dirs, files in os.walk(base):
            depth = root[len(base):].count(os.sep)
            if depth > 4:
                dirs[:] = []
                continue
            for f in files:
                low = f.lower()
                if low.startswith("ffmpeg") and low.endswith(".exe"):
                    return os.path.join(root, f)
    return None


def tim_ffprobe(ffmpeg):
    """Tìm ffprobe: PATH -> cùng thư mục với ffmpeg."""
    p = shutil.which("ffprobe")
    if p:
        return p
    d = os.path.dirname(ffmpeg) if ffmpeg else ""
    if d:
        for name in ("ffprobe.exe", "ffprobe"):
            cand = os.path.join(d, name)
            if os.path.isfile(cand):
                return cand
    return None


def file_co_video(ffprobe, path):
    """True nếu file có luồng video, False nếu không, None nếu không đọc được."""
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "stream=codec_type",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30)
        types = [t.strip() for t in r.stdout.splitlines() if t.strip()]
        return "video" in types
    except Exception:
        return None


def nhan_dien_cap(folder, ffmpeg):
    """Nhận diện cặp (video, audio) trong thư mục. Cần đúng 2 file media.
    Ưu tiên dùng ffprobe xem file nào thật sự có hình, không đọc được thì
    đoán theo cỡ file (file to = hình, file nhỏ = tiếng)."""
    files = []
    for name in os.listdir(folder):
        low = name.lower()
        if not low.endswith(MEDIA_EXTS):
            continue
        if "_gop" in low:
            continue
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            files.append(name)
    if len(files) == 0:
        raise ValueError("Thư mục này không có file video/audio nào.")
    if len(files) != 2:
        raise ValueError(
            "Tìm thấy %d file, tool chỉ nhận diện khi có đúng 2 file:\n%s"
            % (len(files), "\n".join("  - " + f for f in sorted(files))))
    ffprobe = tim_ffprobe(ffmpeg) if ffmpeg else None
    if ffprobe:
        co_video = {f: file_co_video(ffprobe, os.path.join(folder, f)) for f in files}
        co_video_files = [f for f in files if co_video.get(f) is True]
        if len(co_video_files) == 1:
            video = co_video_files[0]
            audio = files[1] if files[0] == video else files[0]
            return video, audio
    files.sort(key=lambda f: os.path.getsize(os.path.join(folder, f)))
    return files[1], files[0]


def ten_file_dau_ra(thu_muc, ten_goc):
    """Tên file không trùng: ten.mp4, ten(1).mp4, ten(2).mp4..."""
    out = ten_goc + ".mp4"
    n = 1
    while os.path.exists(os.path.join(thu_muc, out)):
        out = "%s(%d).mp4" % (ten_goc, n)
        n += 1
    return out


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("680x520")
        self.resizable(True, True)
        self.ffmpeg = None

        cfg = doc_config()
        self.video_var = tk.StringVar()
        self.audio_var = tk.StringVar()
        self.outdir_var = tk.StringVar(
            value=cfg.get("output_dir") or mac_dinh_thu_muc_luu())

        pad = {"padx": 8, "pady": 5}

        tk.Label(self, text="Video (hình):").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.video_var).grid(
            row=0, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn file...", command=self.chon_video).grid(
            row=0, column=2, **pad)

        tk.Label(self, text="Audio (tiếng):").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.audio_var).grid(
            row=1, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn file...", command=self.chon_audio).grid(
            row=1, column=2, **pad)

        tk.Button(self, text="Chọn thư mục chứa 2 file (tự nhận diện)",
                  command=self.chon_thu_muc).grid(
            row=2, column=0, columnspan=3, sticky="ew", **pad)

        tk.Label(self, text="Thư mục lưu:").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.outdir_var).grid(
            row=3, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...", command=self.chon_thu_muc_luu).grid(
            row=3, column=2, **pad)

        tk.Label(self, text="Video sau khi gộp sẽ lưu vào "
                 "<thư mục lưu>\\<tên video>\\<tên video>.mp4",
                 fg="gray").grid(row=4, column=0, columnspan=3, sticky="w", **pad)

        self.btn_gop = tk.Button(self, text="GỘP VIDEO", font=("", 13, "bold"),
                                 bg="#2e7d32", fg="white", height=2,
                                 command=self.bam_gop)
        self.btn_gop.grid(row=5, column=0, columnspan=3, sticky="ew", **pad)

        self.log = scrolledtext.ScrolledText(self, height=13, state="disabled")
        self.log.grid(row=6, column=0, columnspan=3, sticky="nsew", **pad)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.ghi_log("Tool sẵn sàng. Chọn 2 file rồi bấm GỘP VIDEO.")
        self.ffmpeg = tim_ffmpeg()
        if self.ffmpeg:
            self.ghi_log("Đã tìm thấy ffmpeg.")
        else:
            self.ghi_log("CHƯA tìm thấy ffmpeg! Khi bấm GỘP VIDEO sẽ báo link tải.")

    def ghi_log(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def chon_video(self):
        p = filedialog.askopenfilename(
            title="Chọn file video (hình)",
            filetypes=[("Video", "*.mp4 *.m4a *.webm *.mkv"),
                       ("Tất cả file", "*.*")])
        if p:
            self.video_var.set(p)

    def chon_audio(self):
        p = filedialog.askopenfilename(
            title="Chọn file audio (tiếng)",
            filetypes=[("Video/Audio", "*.mp4 *.m4a *.webm *.mkv"),
                       ("Tất cả file", "*.*")])
        if p:
            self.audio_var.set(p)

    def chon_thu_muc(self):
        folder = filedialog.askdirectory(title="Chọn thư mục chứa 2 file video")
        if not folder:
            return
        try:
            video, audio = nhan_dien_cap(folder, self.ffmpeg or tim_ffmpeg())
        except ValueError as e:
            messagebox.showerror("Không nhận diện được", str(e))
            return
        self.video_var.set(os.path.join(folder, video))
        self.audio_var.set(os.path.join(folder, audio))
        self.ghi_log("Đã nhận diện trong thư mục %s:" % folder)
        self.ghi_log("  Hình: " + video)
        self.ghi_log("  Tiếng: " + audio)

    def chon_thu_muc_luu(self):
        folder = filedialog.askdirectory(title="Chọn thư mục lưu mặc định")
        if folder:
            self.outdir_var.set(folder)
            luu_config({"output_dir": folder})
            self.ghi_log("Thư mục lưu mặc định: " + folder)

    def bam_gop(self):
        video = self.video_var.get().strip()
        audio = self.audio_var.get().strip()
        outdir = self.outdir_var.get().strip()
        if not video or not os.path.isfile(video):
            messagebox.showerror("Thiếu file", "Chưa chọn file Video (hình).")
            return
        if not audio or not os.path.isfile(audio):
            messagebox.showerror("Thiếu file", "Chưa chọn file Audio (tiếng).")
            return
        if not outdir:
            messagebox.showerror("Thiếu thư mục", "Chưa chọn thư mục lưu.")
            return
        ffmpeg = self.ffmpeg or tim_ffmpeg()
        if not ffmpeg:
            messagebox.showerror(
                "Không tìm thấy ffmpeg",
                "Chưa tìm thấy ffmpeg trên máy.\n\n"
                "Hãy tải ffmpeg tại:\n" + FFMPEG_LINK + "\n"
                "Giải nén, copy file ffmpeg.exe vào cùng thư mục với tool "
                "này rồi bấm GỘP VIDEO lại.")
            return
        self.ffmpeg = ffmpeg
        luu_config({"output_dir": outdir})
        self.btn_gop.config(state="disabled")
        self.ghi_log("Đang gộp, chờ một chút...")
        threading.Thread(target=self._gop_worker,
                         args=(video, audio, outdir, ffmpeg),
                         daemon=True).start()

    def _gop_worker(self, video, audio, outdir, ffmpeg):
        try:
            ten = os.path.splitext(os.path.basename(video))[0]
            folder = os.path.join(outdir, ten)
            os.makedirs(folder, exist_ok=True)
            out_name = ten_file_dau_ra(folder, ten)
            out_path = os.path.join(folder, out_name)
            cmd = [ffmpeg, "-i", video, "-i", audio, "-c", "copy", out_path]
            r = subprocess.run(cmd, capture_output=True, text=True,
                               errors="replace", timeout=3600)
            if r.returncode != 0:
                err = (r.stderr or "").strip().splitlines()[-5:]
                raise RuntimeError("ffmpeg báo lỗi:\n" + "\n".join(err))
            self.after(0, self._gop_xong, out_path, folder)
        except Exception as e:
            self.after(0, self._gop_loi, str(e))
        finally:
            self.after(0, lambda: self.btn_gop.config(state="normal"))

    def _gop_xong(self, out_path, folder):
        self.ghi_log("GỘP XONG: " + out_path)
        if messagebox.askyesno("Xong rồi!",
                               "Video đã gộp xong:\n" + out_path +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    def _gop_loi(self, msg):
        self.ghi_log("GỘP THẤT BẠI: " + msg)
        messagebox.showerror("Gộp thất bại", msg)


if __name__ == "__main__":
    App().mainloop()

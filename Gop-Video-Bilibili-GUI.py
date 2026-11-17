# -*- coding: utf-8 -*-
r"""
GỘP VIDEO BILIBILI - bản giao diện (build thành file .exe trên Windows)
Luồng chính (dán link -> tải bằng IDM -> gộp -> xem):
1. Tải video từ Bilibili bằng yt-dlp: dán link, chọn chất lượng, tải về rồi
   tự gộp thành 1 video hoàn chỉnh.
2. Tải video từ Bilibili bằng IDM: dán link, chọn chất lượng, tool đẩy link
   hình + link tiếng sang IDM qua COM API (kèm Referer + cookie) để IDM tải
   nhanh nhiều luồng; tool hiện % tải (đo dung lượng file đang lớn dần),
   tải xong tự điền 2 file vào mục Gộp.
3. Gộp 2 file đã có (tải bằng IDM): chọn file hình + file tiếng, gộp lại;
   gộp xong bấm XEM THÀNH QUẢ để mở video.
Video hoàn thiện lưu vào <thư mục lưu>\<tên video>\<tên video>.mp4
(thư mục lưu mặc định: Desktop\Video-Da-Gop, nhớ lựa chọn lần sau).
Cần ffmpeg + yt-dlp: tool tự tìm trên máy (cùng thư mục với .exe, PATH,
C:\ffmpeg, C:\iContent...). Nếu không thấy sẽ báo link tải.
Viết bởi Gà Con cho CYAN - 17/11/2026
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

APP_TITLE = "Gộp Video Bilibili"
FFMPEG_LINK = "https://www.gyan.dev/ffmpeg/builds/"
YTDLP_LINK = "https://github.com/yt-dlp/yt-dlp/releases"
MEDIA_EXTS = (".mp4", ".m4a", ".webm", ".mkv")
COOKIES_MAC_DINH = r"C:\Users\Administrator\Desktop\Cookiebili\cookies.txt"
UA_TRINH_DUYET = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36")
# GUID của thư viện kiểu IDM (IDManTypeInfo.tlb) để gọi COM API.
IDM_TLB_GUID = "{ECF21EAB-3AA8-4355-82BE-F777990001DD}"
# Mã chất lượng (qn) của Bilibili -> nhãn hiển thị. Dùng mã qn thay vì chiều
# cao pixel vì video dọc (vd. 1080x1920) có height=1920 nhưng vẫn là "1080p".
QN_LABEL = {6: "240p", 16: "360p", 32: "480p", 64: "720p", 74: "720p60",
            80: "1080p", 112: "1080p+", 116: "1080p60", 120: "4K",
            125: "HDR", 126: "Dolby", 127: "8K"}


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


def tim_ytdlp():
    """Tìm yt-dlp: PATH -> cùng thư mục với tool -> C:\\iContent."""
    p = shutil.which("yt-dlp")
    if p:
        return p
    here = app_dir()
    for cand in (
        os.path.join(here, "yt-dlp.exe"),
        os.path.join(here, "yt-dlp"),
        r"C:\iContent\yt-dlp.exe",
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
                if f.lower() in ("yt-dlp.exe", "yt-dlp"):
                    return os.path.join(root, f)
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


def sanitize_ten(name):
    """Tên file/thư mục an toàn trên Windows, tối đa 100 ký tự."""
    name = re.sub(r'[<>:"/\\|?*%]', "_", name)
    name = re.sub(r"\s+", " ", name).strip().strip(".")
    if not name:
        name = "video"
    return name[:100]


def dinh_dang_thoi_luong(sec):
    if sec is None:
        return "?"
    sec = int(sec)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return "%d:%02d:%02d" % (h, m, s) if h else "%02d:%02d" % (m, s)


def kiem_tra_link(url, cookies):
    """Đọc thông tin video Bilibili: tiêu đề, thời lượng, các chất lượng có.
    Trả về dict {title, duration, options}, trong đó options là danh sách
    {label, quality, video_id, audio_id} xếp từ cao xuống thấp.
    Ưu tiên bản avc1 (H.264) thay vì HEVC để tương thích tốt hơn.
    Cần yt-dlp."""
    ytdlp = tim_ytdlp()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    cmd = [ytdlp, "-J", "--no-playlist"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True,
                       errors="replace", timeout=120)
    if r.returncode != 0:
        raise RuntimeError("Không đọc được link. Kiểm tra lại link / mạng.")
    info = json.loads(r.stdout)
    title = info.get("title") or "video"
    duration = info.get("duration")
    videos = {}
    for f in info.get("formats", []):
        if f.get("vcodec") in (None, "none") or f.get("quality") is None:
            continue
        q = f["quality"]
        cur = videos.get(q)
        if cur is None or (str(f.get("vcodec", "")).startswith("avc")
                           and not str(cur.get("vcodec", "")).startswith("avc")):
            videos[q] = f
    audios = [f for f in info.get("formats", [])
              if f.get("acodec") not in (None, "none")]
    best_audio = max(audios, key=lambda f: f.get("abr") or 0) if audios else None
    options = []
    for q in sorted(videos, reverse=True):
        vsize = videos[q].get("filesize") or videos[q].get("filesize_approx") or 0
        asize = ((best_audio.get("filesize")
                  or best_audio.get("filesize_approx") or 0)
                 if best_audio else 0)
        options.append({"label": QN_LABEL.get(q, "%dp" % q),
                        "quality": q,
                        "video_id": videos[q]["format_id"],
                        "audio_id": best_audio["format_id"] if best_audio else None,
                        "tong_dung_luong": vsize + asize})
    if not options:
        raise RuntimeError("Không tìm thấy chất lượng video nào.")
    return {"title": title, "duration": duration, "options": options}


def tai_va_gop(url, option, cookies, outdir, log, tien_trinh):
    """Tải video+audio theo lựa chọn chất lượng rồi gộp thành 1 mp4 trong
    <outdir>/<tên video>/<tên video>.mp4. Trả về (đường dẫn file, thư mục)."""
    ytdlp = tim_ytdlp()
    ffmpeg = tim_ffmpeg()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    if not ffmpeg:
        raise RuntimeError("Chưa tìm thấy ffmpeg (cần để gộp hình + tiếng).")
    info = kiem_tra_link(url, cookies)
    ten = sanitize_ten(info["title"])
    folder = os.path.join(outdir, ten)
    os.makedirs(folder, exist_ok=True)
    out_tmpl = os.path.join(folder, ten + ".%(ext)s")
    if option.get("audio_id"):
        fmt = "%s+%s" % (option["video_id"], option["audio_id"])
    else:
        fmt = option["video_id"]
    cmd = [ytdlp, "--no-playlist", "-f", fmt, "--merge-output-format", "mp4",
           "-o", out_tmpl]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    log("Đang tải: %s (%s, %s)"
        % (info["title"], dinh_dang_thoi_luong(info["duration"]),
           option["label"]))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, errors="replace", bufsize=1)
    pct_re = re.compile(r"(\d+(?:\.\d+)?%)")
    for line in proc.stdout:
        if pct_re.search(line) and "download" in line.lower():
            tien_trinh(line.strip()[:140])
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("Tải thất bại (mã %d). Thử lại hoặc kiểm tra link."
                           % proc.returncode)
    out_path = os.path.join(folder, ten + ".mp4")
    if not os.path.isfile(out_path):
        mp4s = [f for f in os.listdir(folder) if f.lower().endswith(".mp4")]
        if not mp4s:
            raise RuntimeError("Tải xong nhưng không thấy file video.")
        out_path = os.path.join(folder, sorted(mp4s)[0])
    return out_path, folder


def doc_cookies_txt(path):
    """Đọc file cookies.txt (định dạng Netscape) -> chuỗi 'name=value; ...'
    dùng cho IDM. Trả về '' nếu không đọc được / không có cookie."""
    cookies = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 7:
                    name, value = parts[5].strip(), parts[6].strip()
                    if name and value:
                        cookies.append("%s=%s" % (name, value))
    except Exception:
        return ""
    return "; ".join(cookies)


def lay_link_stream(url, format_id, cookies):
    """Lấy link trực tiếp (.m4s) của 1 format bằng yt-dlp --get-url.
    Chỉ lấy link, không tải. Trả về URL (chuỗi)."""
    ytdlp = tim_ytdlp()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    cmd = [ytdlp, "--no-playlist", "-f", format_id, "--get-url"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True,
                       errors="replace", timeout=120)
    if r.returncode != 0:
        raise RuntimeError("Không lấy được link tải. Kiểm tra lại link / mạng.")
    links = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    if not links:
        raise RuntimeError("Không lấy được link tải.")
    return links[0]


def gui_sang_idm(link, referer, cookie_str, local_path, local_filename,
                 user_agent=None):
    """Đẩy 1 link sang IDM bằng COM API (SendLinkToIDM2) — đúng cơ chế
    extension trình duyệt dùng: gửi kèm Referer + cookie nên Bilibili
    không chặn 403. Cần IDM đã cài trên máy (Windows).
    Trả về True nếu gửi thành công."""
    try:
        import comtypes.client as cc
        from comtypes import automation
    except ImportError:
        raise RuntimeError("Thiếu thư viện comtypes (cần để gọi IDM).")
    try:
        try:
            cc.GetModule([IDM_TLB_GUID, 1, 0])
        except Exception:
            tlb = None
            for base in (r"C:\Program Files (x86)\Internet Download Manager",
                         r"C:\Program Files\Internet Download Manager"):
                cand = os.path.join(base, "IDManTypeInfo.tlb")
                if os.path.isfile(cand):
                    tlb = cand
                    break
            if tlb:
                cc.GetModule(tlb)
            else:
                raise
        import comtypes.gen.IDManLib as idman
    except Exception:
        raise RuntimeError("Không tìm thấy IDM trên máy. Hãy cài IDM rồi thử lại.")
    try:
        idm = cc.CreateObject(idman.CIDMLinkTransmitter, None, None,
                              idman.ICIDMLinkTransmitter2)
    except Exception as e:
        raise RuntimeError("Không kết nối được với IDM: %s" % e)
    reserved1 = automation.VARIANT()
    if user_agent:
        reserved1.vt = automation.VT_BSTR
        reserved1.value = user_agent
    else:
        reserved1.vt = automation.VT_EMPTY
    reserved2 = automation.VARIANT()
    reserved2.vt = automation.VT_EMPTY
    local_path = os.path.realpath(local_path)
    try:
        # lFlags=1: không hiện hộp thoại xác nhận, tải ngay.
        idm.SendLinkToIDM2(link, referer, cookie_str or "", "", "", "",
                           local_path, local_filename, 1, reserved1, reserved2)
    except Exception as e:
        raise RuntimeError("IDM báo lỗi: %s" % e)
    return True


def tai_bang_idm(url, option, cookies, outdir, log):
    """Lấy link hình + tiếng rồi đẩy cả 2 sang IDM tải nhanh nhiều luồng.
    Trả về (thư mục chứa file, tên file hình, tên file tiếng,
    tổng dung lượng ước tính để theo dõi %).
    IDM tải xong thì dùng mục Gộp để gộp lại."""
    info = kiem_tra_link(url, cookies)
    ten = sanitize_ten(info["title"])
    folder = os.path.join(outdir, ten)
    os.makedirs(folder, exist_ok=True)
    cookie_str = (doc_cookies_txt(cookies)
                  if cookies and os.path.isfile(cookies) else "")
    referer = url.strip()
    log("Đang lấy link %s (%s) để đẩy sang IDM..."
        % (info["title"], option["label"]))
    link_video = lay_link_stream(url, option["video_id"], cookies)
    link_audio = (lay_link_stream(url, option["audio_id"], cookies)
                  if option.get("audio_id") else None)
    ten_video = ten + "_hinh.mp4"
    ten_audio = ten + "_tieng.m4a"
    gui_sang_idm(link_video, referer, cookie_str, folder, ten_video,
                 UA_TRINH_DUYET)
    log("Đã đẩy link hình sang IDM: " + ten_video)
    if link_audio:
        gui_sang_idm(link_audio, referer, cookie_str, folder, ten_audio,
                     UA_TRINH_DUYET)
        log("Đã đẩy link tiếng sang IDM: " + ten_audio)
    return folder, ten_video, ten_audio if link_audio else None, option.get("tong_dung_luong") or 0


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("700x800")
        self.resizable(True, True)
        self.ffmpeg = None
        self.link_info = None
        self.chat_luong_options = []

        cfg = doc_config()
        self.video_var = tk.StringVar()
        self.audio_var = tk.StringVar()
        self.outdir_var = tk.StringVar(
            value=cfg.get("output_dir") or mac_dinh_thu_muc_luu())
        self.link_var = tk.StringVar()
        self.chat_luong_var = tk.StringVar()
        self.cookies_var = tk.StringVar(
            value=cfg.get("cookies") or (
                COOKIES_MAC_DINH if os.path.isfile(COOKIES_MAC_DINH) else ""))
        self.status_var = tk.StringVar(value="Sẵn sàng.")

        pad = {"padx": 8, "pady": 4}

        # ---- Khung 1: Tải video từ Bilibili ----
        f1 = tk.LabelFrame(self, text=" 1. Tải video từ Bilibili ", padx=8, pady=6)
        f1.grid(row=0, column=0, columnspan=3, sticky="ew", **pad)
        f1.grid_columnconfigure(1, weight=1)

        tk.Label(f1, text="Link phim:").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(f1, textvariable=self.link_var).grid(
            row=0, column=1, sticky="ew", **pad)
        self.btn_kiem_tra = tk.Button(f1, text="Kiểm tra link",
                                      command=self.bam_kiem_tra)
        self.btn_kiem_tra.grid(row=0, column=2, **pad)

        self.info_var = tk.StringVar(value="Dán link Bilibili (BV...) rồi bấm Kiểm tra link.")
        tk.Label(f1, textvariable=self.info_var, fg="gray", wraplength=640,
                 justify="left").grid(row=1, column=0, columnspan=3,
                                      sticky="w", **pad)

        tk.Label(f1, text="Chất lượng:").grid(row=2, column=0, sticky="w", **pad)
        self.cbo_chat_luong = ttk.Combobox(f1, textvariable=self.chat_luong_var,
                                           state="readonly", width=12)
        self.cbo_chat_luong.grid(row=2, column=1, sticky="w", **pad)
        self.btn_tai = tk.Button(f1, text="TẢI XUỐNG + GỘP LUÔN (yt-dlp)",
                                 command=self.bam_tai, state="disabled")
        self.btn_tai.grid(row=2, column=2, **pad)

        self.btn_idm = tk.Button(f1, text="TẢI BẰNG IDM (nhanh, nhiều luồng)",
                                 command=self.bam_idm, state="disabled")
        self.btn_idm.grid(row=3, column=0, columnspan=3, sticky="ew", **pad)

        tk.Label(f1, text="File cookies.txt (để tải 1080p):").grid(
            row=4, column=0, sticky="w", **pad)
        tk.Entry(f1, textvariable=self.cookies_var).grid(
            row=4, column=1, sticky="ew", **pad)
        tk.Button(f1, text="Chọn...",
                  command=self.chon_cookies).grid(row=4, column=2, **pad)
        tk.Label(f1, text="Không có cookies thì thường chỉ tải được 480p.",
                 fg="gray").grid(row=5, column=0, columnspan=3, sticky="w", **pad)
        self.tien_trinh_idm = ttk.Progressbar(f1, mode="determinate",
                                              maximum=100)
        self.tien_trinh_idm.grid(row=6, column=0, columnspan=2,
                                 sticky="ew", **pad)
        self.phan_tram_var = tk.StringVar(value="")
        tk.Label(f1, textvariable=self.phan_tram_var, fg="gray").grid(
            row=6, column=2, sticky="w", **pad)

        # ---- Khung 2: Gộp 2 file đã có ----
        f2 = tk.LabelFrame(self, text=" 2. Gộp 2 file đã có (tải bằng IDM) ",
                           padx=8, pady=6)
        f2.grid(row=1, column=0, columnspan=3, sticky="ew", **pad)
        f2.grid_columnconfigure(1, weight=1)

        tk.Label(f2, text="Video (hình):").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(f2, textvariable=self.video_var).grid(
            row=0, column=1, sticky="ew", **pad)
        tk.Button(f2, text="Chọn file...", command=self.chon_video).grid(
            row=0, column=2, **pad)

        tk.Label(f2, text="Audio (tiếng):").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(f2, textvariable=self.audio_var).grid(
            row=1, column=1, sticky="ew", **pad)
        tk.Button(f2, text="Chọn file...", command=self.chon_audio).grid(
            row=1, column=2, **pad)

        tk.Button(f2, text="Chọn thư mục chứa 2 file (tự nhận diện)",
                  command=self.chon_thu_muc).grid(
            row=2, column=0, columnspan=3, sticky="ew", **pad)

        self.btn_gop = tk.Button(f2, text="GỘP VIDEO", font=("", 12, "bold"),
                                 height=2, command=self.bam_gop)
        self.btn_gop.grid(row=3, column=0, columnspan=3, sticky="ew", **pad)

        self.thanh_qua = None
        self.btn_xem = tk.Button(f2, text="XEM THÀNH QUẢ",
                                 font=("", 11, "bold"),
                                 command=self.bam_xem, state="disabled")
        self.btn_xem.grid(row=4, column=0, columnspan=3, sticky="ew", **pad)

        # ---- Thư mục lưu ----
        tk.Label(self, text="Thư mục lưu:").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.outdir_var).grid(
            row=2, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...",
                  command=self.chon_thu_muc_luu).grid(row=2, column=2, **pad)
        tk.Label(self, text="Video hoàn thiện lưu vào "
                 "<thư mục lưu>\\<tên video>\\<tên video>.mp4",
                 fg="gray").grid(row=3, column=0, columnspan=3, sticky="w", **pad)

        # ---- Log + trạng thái ----
        self.log = scrolledtext.ScrolledText(self, height=12, state="disabled")
        self.log.grid(row=4, column=0, columnspan=3, sticky="nsew", **pad)
        tk.Label(self, textvariable=self.status_var, fg="gray",
                 anchor="w").grid(row=5, column=0, columnspan=3, sticky="ew", **pad)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.ghi_log("Tool sẵn sàng.")
        self.ffmpeg = tim_ffmpeg()
        if self.ffmpeg:
            self.ghi_log("Đã tìm thấy ffmpeg.")
        else:
            self.ghi_log("CHƯA tìm thấy ffmpeg! Khi gộp/tải sẽ báo link tải.")
        if tim_ytdlp():
            self.ghi_log("Đã tìm thấy yt-dlp.")
        else:
            self.ghi_log("CHƯA tìm thấy yt-dlp! Phần tải video cần yt-dlp.")

    # ---------- tiện ích ----------
    def ghi_log(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def log_threadsafe(self, text):
        self.after(0, self.ghi_log, text)

    def status_threadsafe(self, text):
        self.after(0, self.status_var.set, text)

    def luu_cau_hinh(self):
        luu_config({"output_dir": self.outdir_var.get().strip(),
                    "cookies": self.cookies_var.get().strip()})

    # ---------- khung 1: tải video ----------
    def bam_kiem_tra(self):
        url = self.link_var.get().strip()
        if not url:
            messagebox.showerror("Thiếu link", "Dán link Bilibili vào trước đã.")
            return
        if not tim_ytdlp():
            messagebox.showerror(
                "Không tìm thấy yt-dlp",
                "Chưa tìm thấy yt-dlp trên máy.\n\n"
                "Hãy tải yt-dlp tại:\n" + YTDLP_LINK + "\n"
                "Tải file yt-dlp.exe, để vào cùng thư mục với tool này rồi thử lại.")
            return
        self.btn_kiem_tra.config(state="disabled")
        self.info_var.set("Đang đọc thông tin video, chờ một chút...")
        threading.Thread(target=self._kiem_tra_worker,
                         args=(url,), daemon=True).start()

    def _kiem_tra_worker(self, url):
        try:
            info = kiem_tra_link(url, self.cookies_var.get().strip())
            self.after(0, self._kiem_tra_xong, info)
        except Exception as e:
            self.after(0, self._kiem_tra_loi, str(e))
        finally:
            self.after(0, lambda: self.btn_kiem_tra.config(state="normal"))

    def _kiem_tra_xong(self, info):
        self.link_info = info
        options = info["options"]
        self.chat_luong_options = options
        self.cbo_chat_luong["values"] = [o["label"] for o in options]
        self.chat_luong_var.set(options[0]["label"])
        self.info_var.set("Tiêu đề: %s\nThời lượng: %s | Chất lượng có: %s"
                          % (info["title"],
                             dinh_dang_thoi_luong(info["duration"]),
                             ", ".join(o["label"] for o in options)))
        self.btn_tai.config(state="normal")
        self.btn_idm.config(state="normal")
        self.ghi_log("Đã đọc link: %s" % info["title"])

    def _kiem_tra_loi(self, msg):
        self.info_var.set("Lỗi: " + msg)
        messagebox.showerror("Không đọc được link", msg)

    def chon_cookies(self):
        p = filedialog.askopenfilename(
            title="Chọn file cookies.txt",
            filetypes=[("Text", "*.txt"), ("Tất cả file", "*.*")])
        if p:
            self.cookies_var.set(p)
            self.luu_cau_hinh()

    def bam_tai(self):
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        url = self.link_var.get().strip()
        chon = self.chat_luong_var.get().strip()
        option = None
        for o in getattr(self, "chat_luong_options", []):
            if o["label"] == chon:
                option = o
                break
        if option is None:
            messagebox.showerror("Chưa chọn", "Chọn chất lượng tải về trước đã.")
            return
        outdir = self.outdir_var.get().strip()
        if not outdir:
            messagebox.showerror("Thiếu thư mục", "Chưa chọn thư mục lưu.")
            return
        cookies = self.cookies_var.get().strip()
        self.luu_cau_hinh()
        self.btn_tai.config(state="disabled")
        self.status_var.set("Đang tải...")
        threading.Thread(target=self._tai_worker,
                         args=(url, option, cookies, outdir),
                         daemon=True).start()

    def _tai_worker(self, url, option, cookies, outdir):
        try:
            out_path, folder = tai_va_gop(url, option, cookies, outdir,
                                          self.log_threadsafe,
                                          self.status_threadsafe)
            self.after(0, self._tai_xong, out_path, folder)
        except Exception as e:
            self.after(0, self._tai_loi, str(e))
        finally:
            self.after(0, lambda: self.btn_tai.config(state="normal"))

    def _tai_xong(self, out_path, folder):
        self.status_var.set("Tải xong.")
        self.ghi_log("TẢI XONG: " + out_path)
        if messagebox.askyesno("Xong rồi!",
                               "Video đã tải + gộp xong:\n" + out_path +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    def _tai_loi(self, msg):
        self.status_var.set("Tải thất bại.")
        self.ghi_log("TẢI THẤT BẠI: " + msg)
        messagebox.showerror("Tải thất bại", msg)

    def bam_idm(self):
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        url = self.link_var.get().strip()
        chon = self.chat_luong_var.get().strip()
        option = None
        for o in getattr(self, "chat_luong_options", []):
            if o["label"] == chon:
                option = o
                break
        if option is None:
            messagebox.showerror("Chưa chọn", "Chọn chất lượng tải về trước đã.")
            return
        outdir = self.outdir_var.get().strip()
        if not outdir:
            messagebox.showerror("Thiếu thư mục", "Chưa chọn thư mục lưu.")
            return
        cookies = self.cookies_var.get().strip()
        self.luu_cau_hinh()
        self.btn_idm.config(state="disabled")
        self.status_var.set("Đang đẩy link sang IDM...")
        threading.Thread(target=self._idm_worker,
                         args=(url, option, cookies, outdir),
                         daemon=True).start()

    def _idm_worker(self, url, option, cookies, outdir):
        try:
            folder, ten_video, ten_audio, tong_dung_luong = tai_bang_idm(
                url, option, cookies, outdir, self.log_threadsafe)
            self.after(0, self._idm_xong, folder, ten_video, ten_audio,
                       tong_dung_luong)
        except Exception as e:
            self.after(0, self._idm_loi, str(e))
        finally:
            self.after(0, lambda: self.btn_idm.config(state="normal"))

    def _idm_xong(self, folder, ten_video, ten_audio, tong_dung_luong):
        self.status_var.set("Đã đẩy sang IDM, đang theo dõi tiến độ...")
        self.ghi_log("ĐÃ ĐẨY SANG IDM. IDM đang tải 2 file vào: " + folder)
        messagebox.showinfo(
            "Đã đẩy sang IDM",
            "IDM đang tải 2 file:\n- %s\n- %s\n\nTool sẽ hiện %% tải ở thanh "
            "tiến độ bên dưới, tải xong tự điền 2 file vào mục Gộp."
            % (ten_video, ten_audio or "(chỉ có hình)"))
        threading.Thread(target=self._theo_doi_idm,
                         args=(folder, ten_video, ten_audio, tong_dung_luong),
                         daemon=True).start()

    def _cap_nhat_tien_trinh(self, ty_le):
        self.tien_trinh_idm["value"] = ty_le
        self.phan_tram_var.set("%d%%" % ty_le)
        self.status_var.set("IDM đang tải... %d%%" % ty_le)

    def _theo_doi_idm(self, folder, ten_video, ten_audio, tong_dung_luong):
        """Theo dõi tiến độ tải của IDM bằng cách đo dung lượng file đang
        lớn dần. Khi đủ dung lượng (hoặc file ngừng lớn sau 3 lần đo) thì
        coi là tải xong, tự điền 2 file vào mục Gộp."""
        duong_video = os.path.join(folder, ten_video)
        duong_audio = os.path.join(folder, ten_audio) if ten_audio else None
        lan_khong_doi = 0
        kich_truoc = -1
        while True:
            time.sleep(2)
            kich_hien = 0
            for p in (duong_video, duong_audio):
                if p and os.path.isfile(p):
                    try:
                        kich_hien += os.path.getsize(p)
                    except OSError:
                        pass
            if kich_hien == kich_truoc and kich_hien > 0:
                lan_khong_doi += 1
            else:
                lan_khong_doi = 0
            kich_truoc = kich_hien
            if tong_dung_luong and tong_dung_luong > 0:
                ty_le = min(100, int(kich_hien * 100 / tong_dung_luong))
                self.after(0, self._cap_nhat_tien_trinh, ty_le)
                if kich_hien >= tong_dung_luong:
                    break
                if lan_khong_doi >= 15:
                    self.after(0, self._tai_idm_dung,
                               "File ngừng lớn trước khi đủ dung lượng "
                               "dự kiến. Kiểm tra IDM xem có lỗi không.")
                    return
            else:
                if lan_khong_doi >= 3:
                    break
        self.after(0, self._tai_idm_hoan_tat, folder, ten_video, ten_audio)

    def _tai_idm_hoan_tat(self, folder, ten_video, ten_audio):
        self.tien_trinh_idm["value"] = 100
        self.phan_tram_var.set("100%")
        duong_video = os.path.join(folder, ten_video)
        duong_audio = os.path.join(folder, ten_audio) if ten_audio else ""
        if os.path.isfile(duong_video):
            self.video_var.set(duong_video)
        if duong_audio and os.path.isfile(duong_audio):
            self.audio_var.set(duong_audio)
        self.status_var.set("Tải xong. Bấm GỘP VIDEO để gộp.")
        self.ghi_log("IDM TẢI XONG. Đã điền sẵn 2 file vào mục Gộp.")
        messagebox.showinfo("Tải xong rồi!",
                            "IDM đã tải xong 2 file.\nBấm GỘP VIDEO ở mục 2 "
                            "để gộp lại.")

    def _tai_idm_dung(self, msg):
        self.status_var.set("Tải IDM có vẻ dừng.")
        self.ghi_log("TẢI IDM DỪNG: " + msg)
        messagebox.showwarning("Tải IDM có vẻ dừng", msg)

    def bam_xem(self):
        if getattr(self, "thanh_qua", None) and os.path.isfile(self.thanh_qua):
            os.startfile(self.thanh_qua)
        else:
            messagebox.showinfo("Chưa có thành quả",
                                "Chưa gộp xong video nào. Gộp xong rồi bấm lại.")

    def _idm_loi(self, msg):
        self.status_var.set("Đẩy sang IDM thất bại.")
        self.ghi_log("ĐẨY SANG IDM THẤT BẠI: " + msg)
        messagebox.showerror("Đẩy sang IDM thất bại", msg)

    # ---------- khung 2: gộp file ----------
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
            self.luu_cau_hinh()
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
        self.luu_cau_hinh()
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
        self.thanh_qua = out_path
        self.btn_xem.config(state="normal")
        if messagebox.askyesno("Xong rồi!",
                               "Video đã gộp xong:\n" + out_path +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    def _gop_loi(self, msg):
        self.ghi_log("GỘP THẤT BẠI: " + msg)
        messagebox.showerror("Gộp thất bại", msg)


if __name__ == "__main__":
    App().mainloop()

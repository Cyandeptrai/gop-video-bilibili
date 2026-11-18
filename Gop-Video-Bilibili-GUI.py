# -*- coding: utf-8 -*-
r"""
GỘP VIDEO BILIBILI - bản giao diện (build thành file .exe trên Windows)
v6: nhiều cửa sổ (mỗi cửa sổ 1 video), lịch sử job lưu lại để mở lại,
tự gộp sau khi IDM tải xong, theo dõi % tải (quét thư mục) + % gộp từng
cửa sổ, gộp xong tự xóa 2 file gốc.
v6.1: thiếu yt-dlp/ffmpeg thì tool hỏi và tự tải về (yt-dlp từ GitHub,
ffmpeg bản essentials từ gyan.dev) thay vì chỉ báo link tải tay.

Luồng chính (dán link -> tải bằng IDM -> tự gộp -> xem):
1. Tải video từ Bilibili bằng yt-dlp: dán link, chọn chất lượng, tải về rồi
   tự gộp thành 1 video hoàn chỉnh.
2. Tải video từ Bilibili bằng IDM: dán link, chọn chất lượng, tool đẩy link
   hình + link tiếng sang IDM qua COM API (kèm Referer + cookie) để IDM tải
   nhanh nhiều luồng; tool hiện % tải (quét dung lượng mọi file media trong
   thư mục, không phụ thuộc tên file), tải xong tự nhận diện cặp file rồi
   TỰ GỘP luôn (không cần bấm tay).
3. Gộp 2 file đã có (tải bằng IDM): chọn file hình + file tiếng, gộp lại;
   gộp xong bấm XEM THÀNH QUẢ để mở video.
Video hoàn thiện lưu vào <thư mục lưu>\<tên video>\<tên video>.mp4
(thư mục lưu mặc định: Desktop\Video-Da-Gop, nhớ lựa chọn lần sau).
Gộp xong (thành công) tool tự xóa 2 file gốc hình + tiếng cho nhẹ ổ.
Cần ffmpeg + yt-dlp: tool tự tìm trên máy (cùng thư mục với .exe, PATH,
C:\ffmpeg, C:\iContent...). Nếu không thấy sẽ báo link tải.
Viết bởi Gà Con cho CYAN - 18/11/2026 (v6)
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
import urllib.request
import uuid
import zipfile
from tkinter import filedialog, messagebox, scrolledtext, ttk

APP_TITLE = "Gộp Video Bilibili"
FFMPEG_LINK = "https://www.gyan.dev/ffmpeg/builds/"
YTDLP_LINK = "https://github.com/yt-dlp/yt-dlp/releases"
# Link tải trực tiếp (bản mới nhất) để tool tự tải khi thiếu thư viện.
YTDLP_DOWNLOAD_URL = ("https://github.com/yt-dlp/yt-dlp/releases/"
                      "latest/download/yt-dlp.exe")
FFMPEG_DOWNLOAD_URL = ("https://www.gyan.dev/ffmpeg/builds/"
                       "ffmpeg-release-essentials.zip")
# .m4s: file tiếng IDM tải về thực tế có đuôi .m4s (không phải .m4a như đặt
# tên lúc đẩy sang IDM) - v5 chỉ nhận .m4a nên tracker không đếm được file
# tiếng, chỉ hiện 77%. v6 nhận cả .m4s.
MEDIA_EXTS = (".mp4", ".m4a", ".m4s", ".webm", ".mkv")
COOKIES_MAC_DINH = r"C:\Users\Administrator\Desktop\Cookiebili\cookies.txt"
UA_TRINH_DUYET = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36")
# GUID của thư viện kiểu IDM (IDManTypeInfo.tlb) để gọi COM API.
IDM_TLB_GUID = "{ECF21EAB-3AA8-4355-82BE-F777990001DD}"


def chay_ngam_kwargs():
    """Tham số để chạy chương trình con trên Windows mà không hiện cửa sổ
    đen (console). Trên hệ khác thì không cần."""
    if sys.platform == "win32":
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


def chuan_hoa_link_bilibili(url):
    """Chuẩn hóa link Bilibili về dạng https://www.bilibili.com/video/BV...
    (bỏ tiền tố ngôn ngữ /vi/, /en/... và các tham số theo dõi) để yt-dlp
    nhận đúng extractor Bilibili. Link không phải Bilibili thì giữ nguyên."""
    if not url or "bilibili.com" not in url:
        return url
    m = re.search(r"(BV[0-9A-Za-z]+)", url)
    if m:
        return "https://www.bilibili.com/video/" + m.group(1)
    return url


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


def jobs_path():
    """File lịch sử job (v6): lưu trạng thái từng cửa sổ/job để lần sau mở
    lại vẫn còn, tiếp tục tải/gộp được."""
    return os.path.join(app_dir(), "jobs.json")


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


def doc_jobs():
    """Đọc danh sách job đã lưu. Trả về list (có thể rỗng)."""
    try:
        with open(jobs_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def luu_jobs(jobs):
    try:
        with open(jobs_path(), "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
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


def tai_ytdlp_tu_dong(log_cb=None):
    """(v6.1) Tự tải yt-dlp.exe bản mới nhất từ GitHub về cùng thư mục với
    tool, trả về đường dẫn file. Raise RuntimeError nếu tải thất bại."""
    dest = os.path.join(app_dir(), "yt-dlp.exe")
    if log_cb:
        log_cb("Đang tải yt-dlp tự động từ GitHub...")
    req = urllib.request.Request(YTDLP_DOWNLOAD_URL,
                                 headers={"User-Agent": UA_TRINH_DUYET})
    with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)
    if not os.path.isfile(dest) or os.path.getsize(dest) < 100000:
        raise RuntimeError("Tải yt-dlp về nhưng file không hợp lệ.")
    if log_cb:
        log_cb("Đã tải xong yt-dlp: " + dest)
    return dest


def tai_ffmpeg_tu_dong(log_cb=None):
    """(v6.1) Tự tải ffmpeg (bản essentials của gyan.dev) về, giải nén lấy
    ffmpeg.exe + ffprobe.exe ra cùng thư mục với tool. Trả về đường dẫn
    ffmpeg.exe. Raise RuntimeError nếu tải/giải nén thất bại."""
    zip_path = os.path.join(app_dir(), "ffmpeg-essentials.zip")
    if log_cb:
        log_cb("Đang tải ffmpeg tự động từ gyan.dev (khoảng 80MB)...")
    req = urllib.request.Request(FFMPEG_DOWNLOAD_URL,
                                 headers={"User-Agent": UA_TRINH_DUYET})
    with urllib.request.urlopen(req, timeout=600) as resp, open(zip_path, "wb") as f:
        shutil.copyfileobj(resp, f)
    ffmpeg_path = None
    ffprobe_path = None
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            base = os.path.basename(name)
            if base in ("ffmpeg.exe", "ffprobe.exe") and "/bin/" in name.replace("\\", "/"):
                dest = os.path.join(app_dir(), base)
                with z.open(name) as src, open(dest, "wb") as out:
                    shutil.copyfileobj(src, out)
                if base == "ffmpeg.exe":
                    ffmpeg_path = dest
                else:
                    ffprobe_path = dest
    try:
        os.remove(zip_path)
    except OSError:
        pass
    if not ffmpeg_path or not os.path.isfile(ffmpeg_path):
        raise RuntimeError("Tải ffmpeg về nhưng không giải nén được ffmpeg.exe.")
    if log_cb:
        log_cb("Đã tải xong ffmpeg: " + ffmpeg_path)
    return ffmpeg_path


def file_co_video(ffprobe, path):
    """True nếu file có luồng video, False nếu không, None nếu không đọc được."""
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "stream=codec_type",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30,
            **chay_ngam_kwargs())
        types = [t.strip() for t in r.stdout.splitlines() if t.strip()]
        return "video" in types
    except Exception:
        return None


def lay_thoi_luong(ffprobe, path):
    """Thời lượng file (giây, float) qua ffprobe, None nếu không đọc được."""
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30,
            **chay_ngam_kwargs())
        return float(r.stdout.strip())
    except Exception:
        return None


def quet_dung_luong_thu_muc(folder):
    """(v6) Tổng dung lượng mọi file media trong thư mục (kể cả .m4s),
    không phụ thuộc tên file. Dùng để theo dõi % tải IDM: IDM lưu file
    tiếng với tên/đuôi thực tế khác tên tool đặt, quét thư mục vẫn đếm đủ.
    Không đếm file thành phẩm đã gộp (tên chứa '_gop')."""
    tong = 0
    try:
        for name in os.listdir(folder):
            low = name.lower()
            if not low.endswith(MEDIA_EXTS):
                continue
            if "_gop" in low:
                continue
            p = os.path.join(folder, name)
            try:
                if os.path.isfile(p):
                    tong += os.path.getsize(p)
            except OSError:
                pass
    except OSError:
        pass
    return tong


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


def dinh_dang_trang_thai(status):
    return {
        "moi": "Mới",
        "da_kiem_tra": "Đã kiểm tra link",
        "dang_tai_idm": "Đang tải (IDM)",
        "cho_gop": "Chờ gộp",
        "dang_gop": "Đang gộp",
        "xong": "Đã xong",
        "loi": "Lỗi",
    }.get(status, status)


def kiem_tra_link(url, cookies):
    """Đọc thông tin video Bilibili: tiêu đề, thời lượng, các chất lượng có.
    Trả về dict {title, duration, options}, trong đó options là danh sách
    {label, quality, video_id, audio_id} xếp từ cao xuống thấp.
    Ưu tiên bản avc1 (H.264) thay vì HEVC để tương thích tốt hơn.
    Cần yt-dlp."""
    url = chuan_hoa_link_bilibili(url)
    ytdlp = tim_ytdlp()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    cmd = [ytdlp, "-J", "--no-playlist"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True,
                       errors="replace", timeout=120, **chay_ngam_kwargs())
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
    url = chuan_hoa_link_bilibili(url)
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
                            text=True, errors="replace", bufsize=1,
                            **chay_ngam_kwargs())
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
    url = chuan_hoa_link_bilibili(url)
    ytdlp = tim_ytdlp()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    cmd = [ytdlp, "--no-playlist", "-f", format_id, "--get-url"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True,
                       errors="replace", timeout=120, **chay_ngam_kwargs())
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
    url = chuan_hoa_link_bilibili(url)
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


def gop_co_tien_trinh(video, audio, out_path, ffmpeg, tien_trinh_cb):
    """(v6) Gộp hình + tiếng bằng ffmpeg, báo % gộp qua tien_trinh_cb(pct).
    Tính % từ thời gian đã xử lý (out_time_ms) so với thời lượng video.
    Trả về out_path nếu thành công, raise RuntimeError nếu lỗi."""
    ffprobe = tim_ffprobe(ffmpeg)
    tong_giay = None
    if ffprobe:
        tong_giay = lay_thoi_luong(ffprobe, video)
        if tong_giay is None:
            tong_giay = lay_thoi_luong(ffprobe, audio)
    cmd = [ffmpeg, "-y", "-i", video, "-i", audio, "-c", "copy",
           "-progress", "pipe:1", "-nostats", out_path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True,
                            errors="replace", bufsize=1,
                            **chay_ngam_kwargs())
    out_ms_re = re.compile(r"out_time_ms=(\d+)")
    for line in proc.stdout:
        m = out_ms_re.search(line)
        if m and tong_giay:
            try:
                pct = int(int(m.group(1)) / (tong_giay * 1000.0) * 100)
                tien_trinh_cb(max(0, min(100, pct)))
            except Exception:
                pass
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("ffmpeg báo lỗi (mã %d)." % proc.returncode)
    if not os.path.isfile(out_path):
        raise RuntimeError("Gộp xong nhưng không thấy file thành phẩm.")
    tien_trinh_cb(100)
    return out_path


class CuaSoJob(tk.Toplevel):
    """(v6) Một cửa sổ xử lý 1 video: tải (yt-dlp/IDM) + gộp + xem.
    Trạng thái job được lưu vào jobs.json để lần sau mở lại tiếp tục được.
    Đóng cửa sổ = dừng theo dõi, job vẫn lưu lại trong lịch sử."""

    def __init__(self, quan_ly, job):
        super().__init__(quan_ly)
        self.quan_ly = quan_ly
        self.job = job
        self.job_id = job.get("id") or str(uuid.uuid4())[:8]
        self.job["id"] = self.job_id
        self.ffmpeg = None
        self.link_info = None
        self.chat_luong_options = []
        self.thanh_qua = job.get("output_file") or None
        self.da_dong = False
        self.dang_theo_doi_idm = False
        self.dang_gop = False

        cfg = doc_config()
        self.video_var = tk.StringVar(value=job.get("video_file") or "")
        self.audio_var = tk.StringVar(value=job.get("audio_file") or "")
        self.outdir_var = tk.StringVar(
            value=job.get("outdir") or cfg.get("output_dir")
            or mac_dinh_thu_muc_luu())
        self.link_var = tk.StringVar(value=job.get("link") or "")
        self.chat_luong_var = tk.StringVar(value=job.get("quality_label") or "")
        self.cookies_var = tk.StringVar(
            value=cfg.get("cookies") or (
                COOKIES_MAC_DINH if os.path.isfile(COOKIES_MAC_DINH) else ""))
        self.status_var = tk.StringVar(value="Sẵn sàng.")
        self.tu_gop_var = tk.BooleanVar(value=job.get("tu_gop", True))
        self.xoa_goc_var = tk.BooleanVar(value=job.get("xoa_goc", True))

        ten = job.get("title") or "Video mới"
        self.title("%s - %s" % (APP_TITLE, ten[:60]))
        self.geometry("700x860")
        self.resizable(True, True)

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
        if job.get("title"):
            self.info_var.set("Tiêu đề: %s" % job["title"])
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
        tk.Label(f1, text="% tải (IDM):").grid(row=6, column=0, sticky="w", **pad)
        self.tien_trinh_idm = ttk.Progressbar(f1, mode="determinate",
                                              maximum=100)
        self.tien_trinh_idm.grid(row=6, column=1, sticky="ew", **pad)
        self.phan_tram_var = tk.StringVar(value="")
        tk.Label(f1, textvariable=self.phan_tram_var, fg="gray").grid(
            row=6, column=2, sticky="w", **pad)
        tk.Checkbutton(f1, text="Tải xong tự gộp luôn",
                       variable=self.tu_gop_var,
                       command=self.luu_job_hien_tai).grid(
            row=7, column=0, columnspan=3, sticky="w", **pad)

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

        tk.Label(f2, text="% gộp:").grid(row=4, column=0, sticky="w", **pad)
        self.tien_trinh_gop = ttk.Progressbar(f2, mode="determinate",
                                              maximum=100)
        self.tien_trinh_gop.grid(row=4, column=1, sticky="ew", **pad)
        self.phan_tram_gop_var = tk.StringVar(value="")
        tk.Label(f2, textvariable=self.phan_tram_gop_var, fg="gray").grid(
            row=4, column=2, sticky="w", **pad)
        tk.Checkbutton(f2, text="Gộp xong tự xóa 2 file gốc (hình + tiếng)",
                       variable=self.xoa_goc_var,
                       command=self.luu_job_hien_tai).grid(
            row=5, column=0, columnspan=3, sticky="w", **pad)

        self.btn_xem = tk.Button(f2, text="XEM THÀNH QUẢ",
                                 font=("", 11, "bold"),
                                 command=self.bam_xem,
                                 state="normal" if self.thanh_qua else "disabled")
        self.btn_xem.grid(row=6, column=0, columnspan=3, sticky="ew", **pad)

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
        self.protocol("WM_DELETE_WINDOW", self.dong_cua_so)

        self.ghi_log("Cửa sổ job: %s" % ten)
        self.ffmpeg = tim_ffmpeg()
        if self.ffmpeg:
            self.ghi_log("Đã tìm thấy ffmpeg.")
        else:
            self.ghi_log("CHƯA tìm thấy ffmpeg! Khi gộp/tải sẽ báo link tải.")
        if tim_ytdlp():
            self.ghi_log("Đã tìm thấy yt-dlp.")
        else:
            self.ghi_log("CHƯA tìm thấy yt-dlp! Phần tải video cần yt-dlp.")
        # Khôi phục lựa chọn chất lượng đã lưu (nếu có).
        if job.get("chat_luong_options"):
            self.chat_luong_options = job["chat_luong_options"]
            self.cbo_chat_luong["values"] = [o["label"] for o in self.chat_luong_options]
            self.btn_tai.config(state="normal")
            self.btn_idm.config(state="normal")
            # Khôi phục link_info để bấm tải được ngay.
            self.link_info = {"title": job.get("title") or "video",
                              "duration": job.get("duration"),
                              "options": self.chat_luong_options}
        if job.get("status") == "xong" and self.thanh_qua:
            self.status_var.set("Đã xong: " + self.thanh_qua)

    # ---------- tiện ích ----------
    def con_song(self):
        try:
            return (not self.da_dong) and bool(self.winfo_exists())
        except Exception:
            return False

    def after_an_toan(self, ms, func, *args):
        if not self.con_song():
            return
        try:
            self.after(ms, func, *args)
        except Exception:
            pass

    def ghi_log(self, text):
        if not self.con_song():
            return
        try:
            self.log.config(state="normal")
            self.log.insert("end", text + "\n")
            self.log.see("end")
            self.log.config(state="disabled")
        except Exception:
            pass

    def log_threadsafe(self, text):
        self.after_an_toan(0, self.ghi_log, text)

    def status_threadsafe(self, text):
        if not self.con_song():
            return
        try:
            self.after(0, self.status_var.set, text)
        except Exception:
            pass

    def luu_cau_hinh(self):
        luu_config({"output_dir": self.outdir_var.get().strip(),
                    "cookies": self.cookies_var.get().strip()})

    def luu_job_hien_tai(self, status=None, pct_tai=None, pct_gop=None):
        try:
            if status:
                self.job["status"] = status
            if pct_tai is not None:
                self.job["pct_tai"] = pct_tai
            if pct_gop is not None:
                self.job["pct_gop"] = pct_gop
            self.job["link"] = self.link_var.get().strip()
            self.job["title"] = self.link_info.get("title") if self.link_info else self.job.get("title")
            self.job["quality_label"] = self.chat_luong_var.get().strip()
            self.job["outdir"] = self.outdir_var.get().strip()
            self.job["video_file"] = self.video_var.get().strip()
            self.job["audio_file"] = self.audio_var.get().strip()
            self.job["output_file"] = self.thanh_qua or ""
            self.job["tu_gop"] = bool(self.tu_gop_var.get())
            self.job["xoa_goc"] = bool(self.xoa_goc_var.get())
            if self.chat_luong_options:
                self.job["chat_luong_options"] = self.chat_luong_options
            if self.link_info and self.link_info.get("duration") is not None:
                self.job["duration"] = self.link_info.get("duration")
            self.quan_ly.cap_nhat_job(self.job)
        except Exception:
            pass

    def dong_cua_so(self):
        if self.dang_theo_doi_idm or self.dang_gop:
            if not messagebox.askyesno(
                    "Job đang chạy",
                    "Job này đang tải/gộp. Đóng cửa sổ sẽ dừng theo dõi "
                    "(IDM vẫn tải xong file của nó, lần sau mở lại job để "
                    "tiếp tục).\n\nĐóng cửa sổ này?"):
                return
        self.da_dong = True
        self.dang_theo_doi_idm = False
        self.luu_job_hien_tai()
        try:
            self.quan_ly.dong_cua_so_job(self.job_id)
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass


    # ---------- khung 1: tải video ----------
    def bam_kiem_tra(self):
        url = self.link_var.get().strip()
        if not url:
            messagebox.showerror("Thiếu link", "Dán link Bilibili vào trước đã.")
            return
        if not tim_ytdlp():
            # (v6.1) Chưa có yt-dlp thì hỏi tải tự động thay vì chỉ báo link.
            if messagebox.askyesno(
                    "Chưa có yt-dlp",
                    "Máy chưa có yt-dlp (cần để đọc link + tải video).\n\n"
                    "Bấm Có để tool tự tải yt-dlp bản mới nhất về (để cùng "
                    "thư mục với tool), xong tự kiểm tra link lại.\n"
                    "Bấm Không để tự tải tay tại:\n" + YTDLP_LINK):
                self.btn_kiem_tra.config(state="disabled")
                self.info_var.set("Đang tải yt-dlp tự động, chờ một chút...")
                threading.Thread(target=self._tai_ytdlp_roi_kiem_tra,
                                 args=(url,), daemon=True).start()
            else:
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

    def _tai_ytdlp_roi_kiem_tra(self, url):
        try:
            tai_ytdlp_tu_dong(self.log_threadsafe)
            self.after_an_toan(0, self._kiem_tra_xong_tai_ytdlp, url)
        except Exception as e:
            self.after_an_toan(0, self._tai_ytdlp_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_kiem_tra.config(state="normal"))

    def _kiem_tra_xong_tai_ytdlp(self, url):
        self.ghi_log("Đã có yt-dlp, kiểm tra link lại.")
        self.bam_kiem_tra()

    def _tai_ytdlp_loi(self, msg):
        self.info_var.set("Tải yt-dlp thất bại: " + msg)
        messagebox.showerror(
            "Tải yt-dlp thất bại",
            "Không tải tự động được yt-dlp:\n" + msg + "\n\n"
            "Hãy tải tay tại:\n" + YTDLP_LINK + "\n"
            "Tải file yt-dlp.exe, để vào cùng thư mục với tool này rồi thử lại.")

    def _kiem_tra_worker(self, url):
        try:
            info = kiem_tra_link(url, self.cookies_var.get().strip())
            self.after_an_toan(0, self._kiem_tra_xong, info)
        except Exception as e:
            self.after_an_toan(0, self._kiem_tra_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_kiem_tra.config(state="normal"))

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
        self.luu_job_hien_tai(status="da_kiem_tra")

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

    def _lay_option_da_chon(self):
        chon = self.chat_luong_var.get().strip()
        for o in getattr(self, "chat_luong_options", []):
            if o["label"] == chon:
                return o
        return None

    def bam_tai(self):
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        url = self.link_var.get().strip()
        option = self._lay_option_da_chon()
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
            self.after_an_toan(0, self._tai_xong, out_path, folder)
        except Exception as e:
            self.after_an_toan(0, self._tai_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_tai.config(state="normal"))

    def _tai_xong(self, out_path, folder):
        self.status_var.set("Tải xong.")
        self.thanh_qua = out_path
        self.btn_xem.config(state="normal")
        self.ghi_log("TẢI XONG: " + out_path)
        self.luu_job_hien_tai(status="xong", pct_tai=100, pct_gop=100)
        if messagebox.askyesno("Xong rồi!",
                               "Video đã tải + gộp xong:\n" + out_path +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    def _tai_loi(self, msg):
        self.status_var.set("Tải thất bại.")
        self.ghi_log("TẢI THẤT BẠI: " + msg)
        self.luu_job_hien_tai(status="loi")
        messagebox.showerror("Tải thất bại", msg)

    def bam_idm(self):
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        url = self.link_var.get().strip()
        option = self._lay_option_da_chon()
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
            self.after_an_toan(0, self._idm_xong, folder, ten_video, ten_audio,
                               tong_dung_luong)
        except Exception as e:
            self.after_an_toan(0, self._idm_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_idm.config(state="normal"))

    def _idm_xong(self, folder, ten_video, ten_audio, tong_dung_luong):
        self.status_var.set("Đã đẩy sang IDM, đang theo dõi tiến độ...")
        self.ghi_log("ĐÃ ĐẨY SANG IDM. IDM đang tải 2 file vào: " + folder)
        self.job["folder"] = folder
        self.job["tong_dung_luong"] = tong_dung_luong
        self.luu_job_hien_tai(status="dang_tai_idm")
        messagebox.showinfo(
            "Đã đẩy sang IDM",
            "IDM đang tải 2 file:\n- %s\n- %s\n\nTool sẽ hiện %% tải ở thanh "
            "tiến độ bên dưới (quét dung lượng cả thư mục nên đếm đủ cả "
            "file tiếng), tải xong sẽ tự nhận diện và tự gộp luôn."
            % (ten_video, ten_audio or "(chỉ có hình)"))
        self.dang_theo_doi_idm = True
        threading.Thread(target=self._theo_doi_idm,
                         args=(folder, tong_dung_luong),
                         daemon=True).start()

    def _cap_nhat_tien_trinh_tai(self, ty_le):
        if not self.con_song():
            return
        try:
            self.tien_trinh_idm["value"] = ty_le
            self.phan_tram_var.set("%d%%" % ty_le)
            self.status_var.set("IDM đang tải... %d%%" % ty_le)
        except Exception:
            pass

    def _theo_doi_idm(self, folder, tong_dung_luong):
        """(v6) Theo dõi tiến độ tải của IDM bằng cách QUÉT dung lượng mọi
        file media trong thư mục (kể cả .m4s, bất kể tên file) thay vì chỉ
        đo 2 đường dẫn cố định như v5. Sửa lỗi v5 chỉ hiện 77% vì file
        tiếng IDM lưu thực tế là .m4s, không phải .m4a như tên đã đặt.
        Khi đủ dung lượng (hoặc file ngừng lớn) thì tự nhận diện cặp file
        rồi tự gộp luôn (nếu bật)."""
        lan_khong_doi = 0
        kich_truoc = -1
        while self.dang_theo_doi_idm and not self.da_dong:
            time.sleep(2)
            if not self.dang_theo_doi_idm or self.da_dong:
                return
            kich_hien = quet_dung_luong_thu_muc(folder)
            if kich_hien == kich_truoc and kich_hien > 0:
                lan_khong_doi += 1
            else:
                lan_khong_doi = 0
            kich_truoc = kich_hien
            if tong_dung_luong and tong_dung_luong > 0:
                ty_le = min(100, int(kich_hien * 100 / tong_dung_luong))
                self.after_an_toan(0, self._cap_nhat_tien_trinh_tai, ty_le)
                if kich_hien >= tong_dung_luong:
                    break
                if lan_khong_doi >= 15:
                    self.after_an_toan(0, self._tai_idm_dung,
                                       "File ngừng lớn trước khi đủ dung lượng "
                                       "dự kiến. Kiểm tra IDM xem có lỗi không.")
                    return
            else:
                if lan_khong_doi >= 3:
                    break
        if self.da_dong or not self.dang_theo_doi_idm:
            return
        self.dang_theo_doi_idm = False
        self.after_an_toan(0, self._tai_idm_hoan_tat, folder)

    def _tai_idm_hoan_tat(self, folder):
        self.tien_trinh_idm["value"] = 100
        self.phan_tram_var.set("100%")
        # Tự nhận diện cặp file thực tế trong thư mục (kể cả .m4s).
        try:
            video, audio = nhan_dien_cap(folder, self.ffmpeg or tim_ffmpeg())
        except Exception as e:
            self.status_var.set("Tải xong nhưng không nhận diện được cặp file.")
            self.ghi_log("NHẬN DIỆN THẤT BẠI: " + str(e))
            self.luu_job_hien_tai(status="cho_gop", pct_tai=100)
            messagebox.showwarning("Tải xong",
                                   "IDM đã tải xong nhưng tool không nhận diện "
                                   "được đúng 2 file trong thư mục:\n%s\n\n%s"
                                   % (folder, e))
            return
        duong_video = os.path.join(folder, video)
        duong_audio = os.path.join(folder, audio)
        self.video_var.set(duong_video)
        self.audio_var.set(duong_audio)
        self.status_var.set("Tải xong. Đã nhận diện 2 file.")
        self.ghi_log("IDM TẢI XONG. Đã nhận diện: %s + %s" % (video, audio))
        self.luu_job_hien_tai(status="cho_gop", pct_tai=100)
        if self.tu_gop_var.get():
            self.ghi_log("Tự gộp luôn (đã bật 'Tải xong tự gộp luôn').")
            self.bam_gop()
        else:
            messagebox.showinfo("Tải xong rồi!",
                                "IDM đã tải xong 2 file.\nBấm GỘP VIDEO ở mục 2 "
                                "để gộp lại.")

    def _tai_idm_dung(self, msg):
        self.dang_theo_doi_idm = False
        self.status_var.set("Tải IDM có vẻ dừng.")
        self.ghi_log("TẢI IDM DỪNG: " + msg)
        self.luu_job_hien_tai(status="loi")
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
        self.luu_job_hien_tai(status="loi")
        messagebox.showerror("Đẩy sang IDM thất bại", msg)


    # ---------- khung 2: gộp file ----------
    def chon_video(self):
        p = filedialog.askopenfilename(
            title="Chọn file video (hình)",
            filetypes=[("Video", "*.mp4 *.m4a *.m4s *.webm *.mkv"),
                       ("Tất cả file", "*.*")])
        if p:
            self.video_var.set(p)

    def chon_audio(self):
        p = filedialog.askopenfilename(
            title="Chọn file audio (tiếng)",
            filetypes=[("Video/Audio", "*.mp4 *.m4a *.m4s *.webm *.mkv"),
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
            self.luu_job_hien_tai()

    def _cap_nhat_tien_trinh_gop(self, ty_le):
        if not self.con_song():
            return
        try:
            self.tien_trinh_gop["value"] = ty_le
            self.phan_tram_gop_var.set("%d%%" % ty_le)
            self.status_var.set("Đang gộp... %d%%" % ty_le)
        except Exception:
            pass

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
            # (v6.1) Chưa có ffmpeg thì hỏi tải tự động thay vì chỉ báo link.
            if messagebox.askyesno(
                    "Chưa có ffmpeg",
                    "Máy chưa có ffmpeg (cần để gộp hình + tiếng).\n\n"
                    "Bấm Có để tool tự tải ffmpeg về (khoảng 80MB, để cùng "
                    "thư mục với tool), xong tự gộp lại.\n"
                    "Bấm Không để tự tải tay tại:\n" + FFMPEG_LINK):
                self.btn_gop.config(state="disabled")
                self.ghi_log("Đang tải ffmpeg tự động, chờ một chút...")
                threading.Thread(target=self._tai_ffmpeg_roi_gop,
                                 args=(video, audio, outdir),
                                 daemon=True).start()
            else:
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
        self.dang_gop = True
        self.tien_trinh_gop["value"] = 0
        self.phan_tram_gop_var.set("0%")
        self.ghi_log("Đang gộp, chờ một chút...")
        self.luu_job_hien_tai(status="dang_gop")
        threading.Thread(target=self._gop_worker,
                         args=(video, audio, outdir, ffmpeg),
                         daemon=True).start()

    def _tai_ffmpeg_roi_gop(self, video, audio, outdir):
        try:
            ffmpeg = tai_ffmpeg_tu_dong(self.log_threadsafe)
            self.ffmpeg = ffmpeg
            self.after_an_toan(0, self._gop_sau_tai_ffmpeg, video, audio, outdir)
        except Exception as e:
            self.after_an_toan(0, self._tai_ffmpeg_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_gop.config(state="normal"))

    def _gop_sau_tai_ffmpeg(self, video, audio, outdir):
        self.ghi_log("Đã có ffmpeg, gộp lại.")
        self.bam_gop()

    def _tai_ffmpeg_loi(self, msg):
        messagebox.showerror(
            "Tải ffmpeg thất bại",
            "Không tải tự động được ffmpeg:\n" + msg + "\n\n"
            "Hãy tải tay tại:\n" + FFMPEG_LINK + "\n"
            "Giải nén, copy file ffmpeg.exe vào cùng thư mục với tool này "
            "rồi bấm GỘP VIDEO lại.")

    def _gop_worker(self, video, audio, outdir, ffmpeg):
        try:
            ten = os.path.splitext(os.path.basename(video))[0]
            folder = os.path.join(outdir, ten)
            os.makedirs(folder, exist_ok=True)
            out_name = ten_file_dau_ra(folder, ten)
            out_path = os.path.join(folder, out_name)
            gop_co_tien_trinh(
                video, audio, out_path, ffmpeg,
                lambda pct: self.after_an_toan(
                    0, self._cap_nhat_tien_trinh_gop, pct))
            self.after_an_toan(0, self._gop_xong, out_path, folder,
                               video, audio)
        except Exception as e:
            self.after_an_toan(0, self._gop_loi, str(e))
        finally:
            self.dang_gop = False
            self.after_an_toan(
                0, lambda: self.btn_gop.config(state="normal"))

    def _gop_xong(self, out_path, folder, video, audio):
        self.ghi_log("GỘP XONG: " + out_path)
        self.thanh_qua = out_path
        self.btn_xem.config(state="normal")
        self.tien_trinh_gop["value"] = 100
        self.phan_tram_gop_var.set("100%")
        self.status_var.set("Gộp xong.")
        # (v6) Gộp xong tự xóa 2 file gốc cho nhẹ ổ, chỉ xóa sau khi gộp
        # thành công và file gốc khác file thành phẩm.
        if self.xoa_goc_var.get():
            da_xoa = []
            for p in (video, audio):
                try:
                    if p and os.path.isfile(p) and os.path.abspath(p) != os.path.abspath(out_path):
                        os.remove(p)
                        da_xoa.append(os.path.basename(p))
                except Exception as e:
                    self.ghi_log("Không xóa được %s: %s" % (p, e))
            if da_xoa:
                self.ghi_log("Đã xóa 2 file gốc cho nhẹ ổ: " + ", ".join(da_xoa))
                self.video_var.set("")
                self.audio_var.set("")
        self.luu_job_hien_tai(status="xong", pct_gop=100)
        if messagebox.askyesno("Xong rồi!",
                               "Video đã gộp xong:\n" + out_path +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    def _gop_loi(self, msg):
        self.ghi_log("GỘP THẤT BẠI: " + msg)
        self.luu_job_hien_tai(status="loi")
        messagebox.showerror("Gộp thất bại", msg)


class QuanLy(tk.Tk):
    """(v6) Cửa sổ quản lý: nút + mở cửa sổ job mới, danh sách lịch sử job
    (đọc từ jobs.json), mở lại / xóa job. Cài đặt chung (thư mục lưu,
    cookies) dùng chung cho mọi cửa sổ job."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE + " - Quản lý (v6.1)")
        self.geometry("640x520")
        self.resizable(True, True)
        self.cua_so_mo = {}

        cfg = doc_config()
        self.outdir_var = tk.StringVar(
            value=cfg.get("output_dir") or mac_dinh_thu_muc_luu())
        self.cookies_var = tk.StringVar(
            value=cfg.get("cookies") or (
                COOKIES_MAC_DINH if os.path.isfile(COOKIES_MAC_DINH) else ""))

        pad = {"padx": 8, "pady": 4}

        hang_nut = tk.Frame(self)
        hang_nut.grid(row=0, column=0, columnspan=3, sticky="ew", **pad)
        tk.Button(hang_nut, text="+ Mở cửa sổ mới", font=("", 11, "bold"),
                  command=self.mo_cua_so_moi).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Mở lại job đã chọn",
                  command=self.mo_lai_job_da_chon).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Xóa job đã chọn",
                  command=self.xoa_job_da_chon).pack(side="left", padx=4)

        tk.Label(self, text="Lịch sử job (bấm đúp để mở lại cửa sổ):").grid(
            row=1, column=0, columnspan=3, sticky="w", **pad)
        cot = ("ten", "trang_thai", "tai", "gop")
        self.bang = ttk.Treeview(self, columns=cot, show="headings", height=12)
        self.bang.heading("ten", text="Video")
        self.bang.heading("trang_thai", text="Trạng thái")
        self.bang.heading("tai", text="% tải")
        self.bang.heading("gop", text="% gộp")
        self.bang.column("ten", width=300)
        self.bang.column("trang_thai", width=130)
        self.bang.column("tai", width=60, anchor="center")
        self.bang.column("gop", width=60, anchor="center")
        self.bang.grid(row=2, column=0, columnspan=3, sticky="nsew", **pad)
        self.bang.bind("<Double-1>", lambda e: self.mo_lai_job_da_chon())

        tk.Label(self, text="Thư mục lưu:").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.outdir_var).grid(
            row=3, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...",
                  command=self.chon_thu_muc_luu).grid(row=3, column=2, **pad)
        tk.Label(self, text="File cookies.txt (để tải 1080p):").grid(
            row=4, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.cookies_var).grid(
            row=4, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...",
                  command=self.chon_cookies).grid(row=4, column=2, **pad)
        tk.Label(self, text="Mỗi cửa sổ xử lý 1 video (tải + gộp). Đóng cửa sổ "
                 "khi xong, hoặc đóng = hủy theo dõi (job vẫn lưu trong lịch sử).",
                 fg="gray", wraplength=600, justify="left").grid(
            row=5, column=0, columnspan=3, sticky="w", **pad)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.dong_quan_ly)

        self.cap_nhat_bang()
        # Tự mở lại cửa sổ cho các job chưa xong để tiếp tục.
        for job in doc_jobs():
            if job.get("status") in ("dang_tai_idm", "cho_gop", "dang_gop",
                                     "da_kiem_tra"):
                self.mo_cua_so_job(job)

    # ---------- tiện ích ----------
    def luu_cau_hinh(self):
        luu_config({"output_dir": self.outdir_var.get().strip(),
                    "cookies": self.cookies_var.get().strip()})

    def cap_nhat_job(self, job):
        jobs = doc_jobs()
        for i, j in enumerate(jobs):
            if j.get("id") == job.get("id"):
                jobs[i] = job
                break
        else:
            jobs.append(job)
        luu_jobs(jobs)
        self.cap_nhat_bang()

    def cap_nhat_bang(self):
        try:
            for item in self.bang.get_children():
                self.bang.delete(item)
            for job in doc_jobs():
                self.bang.insert("", "end", iid=job.get("id"),
                                 values=(job.get("title") or "(chưa có tên)",
                                         dinh_dang_trang_thai(job.get("status") or "moi"),
                                         "%d%%" % (job.get("pct_tai") or 0),
                                         "%d%%" % (job.get("pct_gop") or 0)))
        except Exception:
            pass

    def chon_thu_muc_luu(self):
        folder = filedialog.askdirectory(title="Chọn thư mục lưu mặc định")
        if folder:
            self.outdir_var.set(folder)
            self.luu_cau_hinh()

    def chon_cookies(self):
        p = filedialog.askopenfilename(
            title="Chọn file cookies.txt",
            filetypes=[("Text", "*.txt"), ("Tất cả file", "*.*")])
        if p:
            self.cookies_var.set(p)
            self.luu_cau_hinh()

    # ---------- cửa sổ job ----------
    def mo_cua_so_moi(self):
        self.luu_cau_hinh()
        job = {"id": str(uuid.uuid4())[:8], "title": "", "link": "",
               "status": "moi", "pct_tai": 0, "pct_gop": 0,
               "tu_gop": True, "xoa_goc": True}
        self.mo_cua_so_job(job)

    def mo_cua_so_job(self, job):
        jid = job.get("id")
        if jid in self.cua_so_mo:
            try:
                win = self.cua_so_mo[jid]
                win.lift()
                win.focus_set()
                return
            except Exception:
                pass
        self.luu_cau_hinh()
        win = CuaSoJob(self, job)
        self.cua_so_mo[jid] = win

    def dong_cua_so_job(self, job_id):
        self.cua_so_mo.pop(job_id, None)
        self.cap_nhat_bang()

    def _job_da_chon(self):
        sel = self.bang.selection()
        if not sel:
            messagebox.showinfo("Chưa chọn", "Chọn một job trong danh sách trước đã.")
            return None
        jid = sel[0]
        for job in doc_jobs():
            if job.get("id") == jid:
                return job
        return None

    def mo_lai_job_da_chon(self):
        job = self._job_da_chon()
        if job:
            self.mo_cua_so_job(job)

    def xoa_job_da_chon(self):
        job = self._job_da_chon()
        if not job:
            return
        if not messagebox.askyesno("Xóa job",
                                   "Xóa job này khỏi lịch sử?\n%s"
                                   % (job.get("title") or "(chưa có tên)")):
            return
        jobs = [j for j in doc_jobs() if j.get("id") != job.get("id")]
        luu_jobs(jobs)
        self.cap_nhat_bang()

    def dong_quan_ly(self):
        self.luu_cau_hinh()
        if self.cua_so_mo:
            if not messagebox.askyesno(
                    "Còn cửa sổ job đang mở",
                    "Còn %d cửa sổ job đang mở. Đóng hết (job vẫn lưu trong "
                    "lịch sử, lần sau mở lại tiếp tục được)?"
                    % len(self.cua_so_mo)):
                return
            for win in list(self.cua_so_mo.values()):
                try:
                    win.da_dong = True
                    win.destroy()
                except Exception:
                    pass
            self.cua_so_mo.clear()
        self.destroy()


if __name__ == "__main__":
    QuanLy().mainloop()

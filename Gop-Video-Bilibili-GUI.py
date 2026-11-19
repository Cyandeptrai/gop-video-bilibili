# -*- coding: utf-8 -*-
r"""
GỘP VIDEO BILIBILI - bản giao diện (build thành file .exe trên Windows)
v6: nhiều cửa sổ (mỗi cửa sổ 1 video), lịch sử job lưu lại để mở lại,
tự gộp sau khi IDM tải xong, theo dõi % tải (quét thư mục) + % gộp từng
cửa sổ, gộp xong tự xóa 2 file gốc.
v6.1: thiếu yt-dlp/ffmpeg thì tool hỏi và tự tải về (yt-dlp từ GitHub,
ffmpeg bản essentials từ gyan.dev) thay vì chỉ báo link tải tay.
v6.2 (Chipchipdownload): đổi tên hiển thị thành Chipchipdownload, icon gà
con; thêm nút Kiểm tra cập nhật (tự vá exe từ GitHub Release, cần token
GitHub chỉ-đọc repo này vì repo là private); có bản cài đặt Inno Setup
(cài vào Program Files\\Chipchipdownload, shortcut Desktop + Start Menu;
gỡ cài đặt xóa luôn yt-dlp/ffmpeg/config/jobs đã tải về khi chạy).
v6.3: sửa lỗi SSL khi tự tải yt-dlp/ffmpeg (CERTIFICATE_VERIFY_FAILED trên
máy CYAN): thử xác minh chứng chỉ trước, chỉ fallback bỏ xác minh khi lỗi
chứng chỉ; kiểm chứng file tải về bằng --version/-version, file hỏng thì
xóa và báo lỗi rõ (kèm nguyên nhân diệt virus/proxy có thể chặn chứng chỉ).
v6.4: thêm nút "Dán" ở phần Kiểm tra link (khung 1): dán link Bilibili từ
clipboard vào ô Link phim, tự tách lấy URL đầu tiên nếu clipboard có thêm
chữ khác, rồi focus lại ô link để bấm Kiểm tra link ngay.
v6.5: bấm TẢI BẰNG IDM thì tạo ngay 1 file text trong thư mục của phim,
lưu link Bilibili + tên phim gốc + tên phim dịch sang tiếng Việt, ghi ngay
trước khi đẩy sang IDM nên dù IDM hủy / lỗi thì file vẫn còn. Từ nay tên
thư mục trùng tên phim đã dịch sang tiếng Việt (thư mục = <thư mục lưu>/
<tên phim tiếng Việt>), dịch bằng Google Translate miễn phí, lỗi mạng thì
giữ nguyên tên gốc.
v6.6: thư mục trùng tên thì không ghi đè: tạo thêm thư mục mới tên
"<tên phim tiếng Việt> - YYYY-MM-DD HH-MM-SS" (ngày-giờ, không dùng dấu
":" vì Windows cấm, tên đã làm sạch ký tự cấm và cắt tối đa 100 ký tự).
Nếu vẫn trùng (cùng giây) thì thêm (1), (2)... cho đến khi hết trùng.
v6.7: repo đã public nên Kiểm tra cập nhật KHÔNG cần token GitHub nữa:
ấn là kiểm tra luôn, không hỏi token; token cũ nếu đã lưu thì vẫn dùng
kèm cho đỡ giới hạn lượt gọi API, không có token thì gọi API công khai.
v6.8: mở lại job cũ vẫn hiện link + tên phim đã lưu; gộp ở mục 2 thì
lấy tên phim từ tên file hình, bỏ hậu tố _hinh/_tieng rồi dịch sang
tiếng Việt, đặt tên file thành phẩm đúng tên phim tiếng Việt đó rồi
mới báo hoàn thành, đồng thời hiển thị tên phim tiếng Việt trong
cửa sổ job, bảng lịch sử và thông báo xong.
v7.0 (ChipChipStudio - GOP 1 SOURCE DUY NHAT): gop Chipchipdownload
v6.8 + SRT Reader v1.4 vao 1 file duy nhat. Giu NGUYEN toan bo chuc
nang ca 2 tool (xem audit o cuoi bao cao): tai yt-dlp, tai IDM, gop,
quan ly job, cap nhat, dich ten, file text, thu muc trung ngay-gio;
doc SRT, Edge TTS HoaiMy/NamMinh (+ giong may SAPI), toc do 0.5-2.0x,
atempo tu dong toi da 1.35x, tien-trinh.json, nghe thu, huy/tiep tuc.
Moi: bang lich su du an (Ten phim TV + Link + Trang thai + Duong dan
thu muc mo duoc + Phu de Co/Khong + nut Xoa/Lam lai/Dich/Them phu de
tung dong); kiem tra phu de bang yt-dlp --list-subs (khong dung nut
phu de tren trinh phat web); tai phu de ve cung thu muc phim; tab Xu
ly phu de (dich bang Muse/GPT/Gemini, key luu local, xuat prompt+SRT);
tab Doc phu de HoaiMy. Chi 1 luong cap nhat duy nhat (ChipChip):
SRT Reader von la portable, khi gop thi thanh tool setup cai 1 lan,
va chi bam Cap nhat trong tool la len ban moi, khong cai lai.
v7.1 (SUA LAI - BO GIOI HAN 15 PHUT): gioi han "chi tach giong cho
video ngan hon 15 phut" la GIOI HAN CUA CAPCUT, khong phai quy tac
cua ChipChipStudio - CYAN dinh chinh 19/11. CapCut chi tach duoc
video <15 phut nen voi phim dai cua CYAN thi KHONG dung duoc CapCut.
ChipChipStudio BO HAN cua 15 phut: khong co bat ky logic nao chan
tach giong theo thoi luong. Phuong an thuc te cho phim dai la GIAM
am luong tieng goc xuong 15% (ffmpeg volume=0.15) truoc khi gop voi
giong Viet. Nut tach giong AI DA BO HAN theo lenh CYAN 19/11 04:38: bo qua han
tach giong bang AI, chi giu phan de: giam tieng goc xuong 15% + tu
giam tieng nen khi co loi bang FFmpeg sidechaincompress.
v7.2 (BAN CUOI): bo han tach giong AI; co file MP3 giong Viet HoaiMy
trong cung thu muc du an thi tron 2 track bang FFmpeg sidechaincompress
- nhac nen (tieng goc da giam) tu nho xuong khi co loi, to lai khi het
loi. Chua co giong thi chi giam co dinh tieng goc xuong 15% truoc khi
gop. Khong gioi han thoi luong, chay bang FFmpeg, khong dung AI tach
giong. File tron xong luu cung thu muc du an. Moi thu cung 1 thu muc
du an, file goc khong doi.
v7.3 (LUONG LONG TIENG CHO CAPCUT - CYAN 19/11 04:53): CYAN tu tach
nen, bo giong (Bo loi kieu CapCut) o ngoai, lay giong tu SRT tao ra,
chen vao, giu nguyen nen. KHONG can tool gop video - cau them thu
cong vao CapCut de gop. Tool chi can XUAT RIENG 2 file audio trong
cung thu muc du an: file nen (tieng goc giam xuong 15%) + file giong
Viet HoaiMy tu SRT, de cau import vao CapCut. Gop video trong tool
la tuy chon rieng, khong bat buoc trong luong nay. (v7.3) O "Tai xong
tu gop luon (IDM)" (tu_gop_var, co tu v6.8, mac dinh BAT, luu theo
tung job) duoc dat RO ngay duoi nut TAI BANG IDM cho de thay: bo
tich thi IDM tai xong chi nhan dien 2 file vao muc 2, KHONG tu gop,
de cau xu ly audio / gop tay trong CapCut sau; tich thi giu hanh vi
tu gop nhu cu. Luu y: file nen cua tool KHONG phai file da bo giong
that su (bo giong that su cau tu lam o CapCut); tool chi giam nho
tieng goc lam nen. Khong dung AI tach giong (da bo theo lenh CYAN
19/11 04:38).
v7.4 (SUA LOI TAI PHU DE + 1 CUA SO DUY NHAT - CYAN 19/11 05:35/05:37):
Loi tai phu de BV1xFs36uE8p: quet --list-subs thay "Co phu de (ai-zh)"
(nho file cookies san co cua CYAN) nhung tai_phu_de chi thu zh-Hans/
zh-CN/zh roi en, KHONG bao gio thu ai-zh, va dung --sub-format srt
trong khi ai-zh cua Bilibili la json3 -> bao khong tim ra. v7.4 thu
dung ngon ngu DA DO DUOC truoc (uu tien ai-zh), them --write-auto-subs
+ --convert-subs srt, file .vtt/.json3/.json tai ve duoc doi sang SRT
trong code; yt-dlp that bai het thi dung API Bilibili truc tiep lam du
phong (view API lay aid/cid -> x/player/v2 lay subtitle_url, dung
SESSDATA tu dung file cookies do -> tai JSON body from/to/content
-> doi sang SRT). Ca 2 duong deu dung file cookies san co cua job
(cookies_var / COOKIES_MAC_DINH neu file ton tai), khong doi cach xu
ly cookies. Giao dien 1 cua so duy nhat: cua so chinh la ttk.Notebook
3 tab (Quan ly / Xu ly phu de / Doc phu de HoaiMy), cac tab phu de la
Frame nhung trong Notebook, khong con Toplevel mo rieng chong nhau;
nut "Kiem tra cap nhat" day ra canh ngoai cung GOC PHAI cua thanh nut,
tach rieng khoi cac nut chuc nang khac. Cua so job van la 1 cua so phu (duy nhat duoc phep) cho 1 du an.
v7.5 (LUONG PHU DE VIETSUBK+ + 1 MACH - CYAN 19/11 05:44/05:45/05:46/
05:47/05:48/05:49): UU TIEN SO 1 la tai duoc file SRT GOC tieng Trung
ve thu muc du an (cau tu quang vao AI ben ngoai de dich); dich Gemini
/ dich thu cong trong tool chi la TUY CHON, khong bat buoc, khong duoc
chan luong tai file goc. Luong API Bilibili du phong nang cap theo
Vietsubk+ v5.9.2: view API lay aid/cid/duration (pages[] cho cid tung
phan) -> thu WBI da ky (tinh w_rid theo thuat toan mixin-key cong khai)
-> WBI khong ky /x/player/wbi/v2 -> plain /x/player/v2, gui SESSDATA
tu dung file cookies.txt + Referer, kiem tra data.bvid/cid/aid phai
khop dung video (khong khop la bo), track AI chi tin khi nguon la
wbi-player (track AI tu plain-player thi AI_SUBTITLE_SOURCE_NOT_READY),
need_login_subtitle=true thi bao can dang nhap, chi lay subtitle_url
https o hdslb.com/bilibili.com/bilivideo.com, parse JSON body
from/to/content -> SRT, ten file <ten>_<BV>_P<page>_cid<cid>_<lan>.srt,
kiem tra do phu maxEnd/duration <0.4 thi nghi ngo, danh dau, khong
trinh bay nhu phu de tot. Khong co phu de thi bao thang "Khong co phu
de" (cot Phu de de "Khong", log ro), KHONG tao file SRT rong, KHONG
tao file SRT gia, KHONG ghi de file SRT da co bang file rong. Nut
"LẤY PHỤ ĐỀ + DỊCH + ĐỌC (1 mạch)" o tab Quan ly: Buoc 1 LUON chay
(tai SRT goc, khong can key Gemini), tai xong thi DUNG HAN, chi bao
duong dan file + hien 2 nut "Dich trong tool" / "Mo tab HoaiMy" cho
cau chon tiep (khong tu chuyen tab, khong tu chay dich); cong tac "Tu
dich sau khi lay phu de" mac dinh TAT, chi bat moi tu dich tiep.
File SRT goc LUON giu lai: dich loi giua chung thi KHONG ghi gi len
file goc; luu de ban dich thi sao luu 1 ban .bak truoc, chi tao 1 lan
(.bak da co thi giu nguyen). Tab Xu ly phu de co them che do "Dich
thu cong": mo SRT goc, tu go tieng Viet tung cau (o nhap canh tung
cau, co nut Luu nhap / tu luu nhap), luu thang ra SRT Viet, khong goi
AI, van giu moc gio goc; luu xong mo tab Doc phu de HoaiMy.
v7.6 (BANG TREEVIEW + DICH TOAN BO + MUSE CHAT TAY - CYAN 19/11):
bang lich su du an doi sang ttk.Treeview cot co dinh (ten/link/
trang thai/thu muc/phu de rut gon co "...", gia tri day du hien o
label chi tiet duoi bang khi chon dong) + hang nut hanh dong cho
dong dang chon, them nut "Mo thu muc phu de" (Explorer chon dung
file .srt). Dich phu de doi sang MAC DINH dich TOAN BO file trong
1 prompt duy nhat (dung prompt cu, dich theo boi canh toan bo);
thieu cau/sai so cau/lech timestamp thi BAO LOI, KHONG luu de
file goc; loi thi tu chuyen sang chia cum 20 cau (du phong, co
cong tac chon "cum"), log/UI ghi ro che do da dung. Them "Muse"
(tro ly Muse, chat tay, KHONG API/key/endpoint) ben canh Gemini/
GPT/Claude (Claude = Anthropic, truoc day goi nham la "Muse" —
config cu tu dong doi sang "Claude" 1 lan); Muse dung "Xuat
prompt + SRT toan bo" roi "Nhap ban dich ve" (kiem tra so cau/
timestamp khop goc moi cho luu de, co .bak 1 lan). Them o chon/
go model tung nha cung cap (luu local): Gemini mac dinh
gemini-3.8-flash, du phong gemini-3.5-flash-lite (KHONG dung
gemini-2.5-flash, tat 01/12/2026), GPT mac dinh gpt-4o-mini,
Claude mac dinh claude-sonnet-4-5. Cookie: KHONG them login
trong tool — login trong trinh duyet roi export cookies.txt
bang Get cookies.txt LOCALLY, import vao tool; cookie Bilibili
chi dung cho Bilibili, cookie web AI la rieng tung web.
Sua loi CYAN bao 19/11: (A) nut "Tai phu de" trong cua so job
gio tao thu muc phim truoc khi tai (khong de .srt roi thang vao
thu muc goc); bang Treeview hien "(chua co thu muc)" khi job
chua co folder, khong fallback ve outdir. (B) file tieng day
sang IDM doi ten _tieng.m4a -> _tieng.mp4 (stream tieng thuc
chat la container mp4, server tra MIME video/mp4 nen IDM het
hoi doi ten); nhan dien cap van phan biet bang ffprobe (file
nao co luong video) nen 2 file .mp4 khong lan nhau.
v7.7 (VIET LAI XUAT MP3 HOAIMY - CYAN 19/11): sua loi bam XUAT MP3
thi cho mai, trang thai dung o "Chưa chạy." (luong worker chet im
ngay tai `from pydub import AudioSegment` dau ham _chay vi ban exe
thieu pydub, khong try/except nen khong bao loi, khong mo khoa nut).
Toan bo luong _chay co try/except + log loi ro + mo khoa nut + hop
thoai loi; trang thai doi "Đang khởi động..." ngay khi bam XUAT.
BO GopDan-WAV-tam (file WAV tam to bang tong thoi luong phim, ffmpeg
chuyen co timeout cung 600s, loi khong ghi ly do): moi cau doc xong
luu file MP3 rieng trong tung-cau nhu cu, gop cuoi bang ffmpeg
concat demuxer (file tung cau xen ke file im lang dung moc gio SRT,
cat bang outpoint khi tran slot), thu -c copy truoc, loi thi thu lai
re-encode, kiem tra do dai file ra bang ffprobe; loi ffmpeg ghi day
du vao ffmpeg-loi.log. Edge TTS co timeout 120s/cau (asyncio.
wait_for), het gio thi failover luot sau; nut Huy dung duoc that
sau cau dang doc. Duong dan dai Windows: thao tac file cua Python
dung tien to \\\\?\\ khi can, ffmpeg thi khong (ffmpeg co the khong
hieu). Khong doi giao dien, ten file ra, tien-trinh.json, che do
Gop/Tung cau rieng/Ca hai.

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
import asyncio
import hashlib
import json
import os
import queue
import re
import shutil
import ssl
import subprocess
import sys
import threading
import time
import traceback
import tkinter as tk
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

# (v7.0) Ten hien thi cua app gop la ChipChipStudio, NHUNG APP_TITLE
# van giu "Chipchipdownload" vi luong cap nhat (kiem_tra_cap_nhat)
# tim asset theo APP_TITLE + ".exe" - doi ten exe se lam hong nut
# Cap nhat. Chi co 1 luong cap nhat duy nhat (cua ChipChip).
APP_TITLE = "Chipchipdownload"
STUDIO_TITLE = "ChipChipStudio"
VERSION = "7.7"
# (v7.7) GHI CHU BUILD EXE (PyInstaller) CHO CHUC NANG XUAT MP3
# HOAIMY — de khong lap lai loi v7.5 "bam XUAT thi chet im vi ban
# exe thieu thu vien": luong xuat MP3 chi import luoi (lazy import)
# cac thu vien sau, PyInstaller KHONG tu thay duoc vi chung khong
# nam o import dau file, nen build PHai khai bao hidden import:
#   edge_tts, edge_tts.communicate, aiohttp, certifi
# (vd: pyinstaller --hidden-import=edge_tts
#  --hidden-import=edge_tts.communicate --hidden-import=aiohttp
#  --hidden-import=certifi ...; hoac khai trong file .spec).
# pydub KHONG con can cho xuat MP3 tu v7.7 (gop bang ffmpeg concat,
# do thoi luong bang ffprobe); neu build van muon giu pydub cho
# du phong thi them --hidden-import=pydub --hidden-import=pydub.audio_segment.
# ffmpeg/ffprobe KHONG dong goi trong exe: tool tu tim ffmpeg.exe/
# ffprobe o PATH, cung thu muc voi exe, C:\ffmpeg, C:\iContent.
# (v7.6) Model dich phu de — KHONG hardcode trong ham goi API nua,
# lay tu config (nguoi dung chon/go o tab Xu ly phu de).
# Gemini 2.5-flash DA DEPRECATED, tat 01/12/2026: TUYET DOI khong
# dung nua. Mac dinh Gemini = 3.8-flash, du phong = 3.5-flash-lite.
MODEL_GEMINI_MAC_DINH = "gemini-3.8-flash"
MODEL_GEMINI_DU_PHONG = "gemini-3.5-flash-lite"
MODEL_GPT_MAC_DINH = "gpt-4o-mini"
MODEL_CLAUDE_MAC_DINH = "claude-sonnet-4-5"
GITHUB_REPO = "Cyandeptrai/gop-video-bilibili"
GITHUB_API_LATEST_RELEASE = ("https://api.github.com/repos/"
                             + GITHUB_REPO + "/releases/latest")
GITHUB_API_VERSION_JSON = ("https://api.github.com/repos/"
                           + GITHUB_REPO + "/contents/version.json")
GITHUB_RELEASES_URL = "https://github.com/" + GITHUB_REPO + "/releases"
FFMPEG_LINK = "https://www.gyan.dev/ffmpeg/builds/"
YTDLP_LINK = "https://github.com/yt-dlp/yt-dlp/releases"
# Link tải trực tiếp (bản mới nhất) để tool tự tải khi thiếu thư viện.
YTDLP_DOWNLOAD_URL = ("https://github.com/yt-dlp/yt-dlp/releases/"
                      "latest/download/yt-dlp.exe")
FFMPEG_DOWNLOAD_URL = ("https://www.gyan.dev/ffmpeg/builds/"
                       "ffmpeg-release-essentials.zip")
# (v7.6) File tieng day sang IDM dat ten _tieng.mp4 (khong con
# _tieng.m4a): stream tieng cua Bilibili thuc chat la container
# mp4, server tra MIME video/mp4 nen IDM hoi doi ten .m4a -> .mp4.
# Dat thang .mp4 thi IDM het hoi, khong lan voi file hinh vi
# nhan_dien_cap phan biet bang ffprobe (file nao co luong video).
# .m4s van giu trong MEDIA_EXTS cho file cu da tai truoc day.
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


def mac_dinh_thu_muc_luu_srt():
    """(v7.0) Thu muc mac dinh cua SRT Reader, doi ten tu
    mac_dinh_thu_muc_luu() cua SRT de tranh trung voi ham mac dinh
    cua Chipchipdownload (Desktop/Video-Da-Gop)."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser("~")
    return os.path.join(desktop, "SRT-HoaiMy")


def doc_config():
    """(v7.0) Config GOP: mac dinh gom ca 2 tool (Chipchip + SRT Reader)
    + key dich phu de. Key KHONG bao gio hardcode, chi luu o config.json
    canh exe khi nguoi dung nhap. Khoa cu trong file cu van giu."""
    mac_dinh = {
        "output_dir": "", "cookies": "", "github_token": "",
        "giong": GIONG_MAC_DINH, "toc_do": 1.0, "cao_do": 0,
        "thu_muc_luu": mac_dinh_thu_muc_luu_srt(),
        "toc_do_toi_da": 1.35, "tu_dong_toc_do": True, "che_do": "gop",
        "phu_de_provider": "Gemini", "gemini_api_key": "",
        "openai_api_key": "", "anthropic_api_key": "",
        # (v7.6) Che do dich + model tung nha cung cap (luu local).
        # che_do: "toan_bo" (mac dinh, 1 prompt duy nhat) / "cum"
        # (chi chia cum 20 cau). Model de trong thi dung mac dinh
        # o tren; nguoi dung duoc go model khac o tab Xu ly phu de.
        "phu_de_che_do": "toan_bo",
        "phu_de_model_gemini": MODEL_GEMINI_MAC_DINH,
        "phu_de_model_gemini_du_phong": MODEL_GEMINI_DU_PHONG,
        "phu_de_model_gpt": MODEL_GPT_MAC_DINH,
        "phu_de_model_claude": MODEL_CLAUDE_MAC_DINH,
        "phu_de_the_loai": "", "phu_de_nhan_vat": "",
        "phu_de_xung_ho": "", "phu_de_boi_canh": "",
    }
    try:
        with open(config_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        # (v7.6) MIGRATION 1 LAN: cau hinh cu (truoc v7.6) dung
        # "Muse" de chi Claude (Anthropic); tu v7.6 "Muse" la tro ly
        # Muse (chat tay, khong API), Claude co ten rieng. Chi doi
        # khi file config chua co khoa "phu_de_che_do" (tuc la file
        # cu) — file da luu o v7.6 tro di thi "Muse" giu nguyen la Muse.
        if "phu_de_che_do" not in data and data.get("phu_de_provider") == "Muse":
            data["phu_de_provider"] = "Claude"
        for k, v in mac_dinh.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(mac_dinh)


def luu_config(cfg):
    """(v7.0) Luu config kieu GOP (merge): doc file cu roi cap nhat
    tung khoa, khong ghi de toan bo file nhu ban cu - neu khong,
    QuanLy.luu_cau_hinh() (chi co output_dir/cookies) se xoa sach
    khoa giong/toc_do/key dich phu de cua SRT Reader."""
    try:
        try:
            with open(config_path(), "r", encoding="utf-8") as f:
                cu = json.load(f)
                if not isinstance(cu, dict):
                    cu = {}
        except Exception:
            cu = {}
        cu.update(cfg or {})
        with open(config_path(), "w", encoding="utf-8") as f:
            json.dump(cu, f, ensure_ascii=False, indent=2)
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
    """Tìm ffmpeg (v7.0, GOP ca 2 danh sach duong dan cua Chipchip +
    SRT Reader): PATH -> cùng thư mục với tool -> C:\\ffmpeg ->
    C:\\iContent (ke ca .venv/Scripts)."""
    p = shutil.which("ffmpeg")
    if p:
        return p
    here = app_dir()
    for cand in (
        os.path.join(here, "ffmpeg.exe"),
        os.path.join(here, "ffmpeg"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\iContent\ffmpeg\bin\ffmpeg.exe",
        r"C:\iContent\.venv\Scripts\ffmpeg.exe",
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


def la_loi_chung_chi_ssl(e):
    """True nếu ngoại lệ là lỗi xác minh chứng chỉ SSL
    (CERTIFICATE_VERIFY_FAILED). Nhận cả ssl.SSLCertVerificationError
    trực tiếp và URLError bọc nó bên trong."""
    if isinstance(e, ssl.SSLCertVerificationError):
        return True
    ly_do = getattr(e, "reason", None)
    if isinstance(ly_do, ssl.SSLCertVerificationError):
        return True
    return "CERTIFICATE_VERIFY_FAILED" in str(e)


def mo_url_co_fallback_ssl(req, timeout, log_cb=None):
    """(v6.3) Mở URL bằng urllib: thử TRƯỚC bằng SSL context mặc định
    (xác minh chứng chỉ). Chỉ khi lỗi là do xác minh chứng chỉ thất bại
    (kho chứng chỉ trên máy thiếu/bị chặn, thường do phần mềm diệt
    virus/proxy) mới thử lại bằng context không xác minh chứng chỉ, và
    ghi rõ vào log. Không bao giờ bỏ xác minh ngay từ đầu.
    Trả về response (dùng với with)."""
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except Exception as e:
        if not la_loi_chung_chi_ssl(e):
            raise
        if log_cb:
            log_cb("Lỗi chứng chỉ SSL, thử lại không xác minh chứng chỉ "
                   "(kho chứng chỉ trên máy có thể thiếu/bị chặn)...")
        try:
            return urllib.request.urlopen(
                req, timeout=timeout,
                context=ssl._create_unverified_context())
        except Exception as e2:
            raise RuntimeError(
                "Lỗi chứng chỉ SSL cả khi đã thử bỏ xác minh (%s). "
                "Nguyên nhân có thể: phần mềm diệt virus hoặc proxy trên "
                "máy chặn chứng chỉ SSL." % e2)


def tai_file_qua_url(url, dest, timeout, log_cb, ten, headers=None):
    """(v6.3) Tải 1 file qua HTTP(S) về dest, dùng mo_url_co_fallback_ssl
    (xác minh chứng chỉ trước, fallback bỏ xác minh chỉ khi lỗi chứng chỉ).
    Raise RuntimeError nếu tải thất bại."""
    head = {"User-Agent": UA_TRINH_DUYET}
    if headers:
        head.update(headers)
    req = urllib.request.Request(url, headers=head)
    with mo_url_co_fallback_ssl(req, timeout, log_cb) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def _xoa_file_quiet(path):
    """Xóa file, bỏ qua mọi lỗi (dùng khi file tải về bị hỏng)."""
    try:
        os.remove(path)
    except OSError:
        pass


def kiem_chung_exe_chay_duoc(path, tham_so, ten):
    """(v6.3) Chạy file vừa tải với tham số kiểm chứng (vd: --version) để
    chắc file thật sự dùng được. Trả về dòng đầu tiên của output.
    Nếu chạy lỗi thì XÓA file hỏng và raise RuntimeError (không để file
    hỏng nằm lại rồi báo thành công)."""
    try:
        r = subprocess.run([path] + tham_so, capture_output=True, text=True,
                           timeout=60, **chay_ngam_kwargs())
    except Exception as e:
        _xoa_file_quiet(path)
        raise RuntimeError("Không chạy kiểm chứng được %s vừa tải (%s)."
                           % (ten, e))
    out = (r.stdout or "").strip()
    if r.returncode != 0 or not out:
        _xoa_file_quiet(path)
        raise RuntimeError("File %s vừa tải không chạy được (kiểm chứng %s "
                           "thất bại)." % (ten, " ".join(tham_so)))
    return out.splitlines()[0]


def tai_ytdlp_tu_dong(log_cb=None):
    """(v6.1) Tự tải yt-dlp.exe bản mới nhất từ GitHub về cùng thư mục với
    tool, trả về đường dẫn file. (v6.3) Tải bằng SSL xác minh trước, fallback
    bỏ xác minh chỉ khi lỗi chứng chỉ; kiểm chứng bằng --version sau khi tải.
    Raise RuntimeError nếu tải thất bại."""
    dest = os.path.join(app_dir(), "yt-dlp.exe")
    if log_cb:
        log_cb("Đang tải yt-dlp tự động từ GitHub...")
    tai_file_qua_url(YTDLP_DOWNLOAD_URL, dest, 300, log_cb, "yt-dlp")
    if not os.path.isfile(dest) or os.path.getsize(dest) < 100000:
        _xoa_file_quiet(dest)
        raise RuntimeError("Tải yt-dlp về nhưng file không hợp lệ.")
    ban = kiem_chung_exe_chay_duoc(dest, ["--version"], "yt-dlp")
    if log_cb:
        log_cb("Đã tải xong yt-dlp (%s): %s" % (ban, dest))
    return dest


def tai_ffmpeg_tu_dong(log_cb=None):
    """(v6.1) Tự tải ffmpeg (bản essentials của gyan.dev) về, giải nén lấy
    ffmpeg.exe + ffprobe.exe ra cùng thư mục với tool. Trả về đường dẫn
    ffmpeg.exe. (v6.3) Tải bằng SSL xác minh trước, fallback bỏ xác minh chỉ
    khi lỗi chứng chỉ; kiểm chứng ffmpeg/ffprobe bằng -version sau khi giải
    nén. Raise RuntimeError nếu tải/giải nén thất bại."""
    zip_path = os.path.join(app_dir(), "ffmpeg-essentials.zip")
    if log_cb:
        log_cb("Đang tải ffmpeg tự động từ gyan.dev (khoảng 80MB)...")
    tai_file_qua_url(FFMPEG_DOWNLOAD_URL, zip_path, 600, log_cb, "ffmpeg")
    ffmpeg_path = None
    ffprobe_path = None
    try:
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
    except zipfile.BadZipFile:
        _xoa_file_quiet(zip_path)
        raise RuntimeError("File ffmpeg tải về không phải file zip hợp lệ "
                           "(có thể tải bị lỗi).")
    try:
        os.remove(zip_path)
    except OSError:
        pass
    if not ffmpeg_path or not os.path.isfile(ffmpeg_path):
        raise RuntimeError("Tải ffmpeg về nhưng không giải nén được ffmpeg.exe.")
    ban = kiem_chung_exe_chay_duoc(ffmpeg_path, ["-version"], "ffmpeg")
    if ffprobe_path and os.path.isfile(ffprobe_path):
        kiem_chung_exe_chay_duoc(ffprobe_path, ["-version"], "ffprobe")
    if log_cb:
        log_cb("Đã tải xong ffmpeg (%s): %s" % (ban, ffmpeg_path))
    return ffmpeg_path


def so_sanh_version(a, b):
    """So sánh 2 chuỗi version dạng '6.2' / 'v6.10': trả 1 nếu a>b, -1 nếu
    a<b, 0 nếu bằng. Dùng để biết bản trên GitHub có mới hơn bản đang chạy."""
    def tach(s):
        s = (s or "").strip().lstrip("vV")
        parts = []
        for p in s.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return parts
    pa, pb = tach(a), tach(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    if pa > pb:
        return 1
    if pa < pb:
        return -1
    return 0


def lay_token_github():
    """Token GitHub chỉ-đọc repo này (do người dùng nhập 1 lần, lưu ở
    config.json cạnh exe). (v6.7) Repo đã public nên token không bắt buộc
    nữa; có token thì kèm theo cho đỡ giới hạn lượt gọi API, không có
    thì vẫn kiểm tra được bằng API công khai."""
    return (doc_config().get("github_token") or "").strip()


def luu_token_github(token):
    cfg = doc_config()
    cfg["github_token"] = (token or "").strip()
    luu_config(cfg)


def goi_github_api(url, token):
    """GET JSON từ GitHub API. (v6.3) Dùng mo_url_co_fallback_ssl: xác
    minh chứng chỉ trước, fallback bỏ xác minh chỉ khi lỗi chứng chỉ
    (cùng lỗi SSL như khi tự tải yt-dlp). (v6.7) Repo đã public nên
    token không bắt buộc: có token thì kèm Authorization, không có
    thì gọi API công khai."""
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": UA_TRINH_DUYET}
    if (token or "").strip():
        headers["Authorization"] = "token " + token.strip()
    req = urllib.request.Request(url, headers=headers)
    with mo_url_co_fallback_ssl(req, 60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def kiem_tra_cap_nhat(token):
    """(v6.2) Kiểm tra bản mới trên GitHub. Trả về dict:
    {version_moi, tag, tai_url, ten_file} hoặc None nếu đã là bản mới nhất.
    Ưu tiên đọc GitHub Releases (latest); nếu chưa có Release nào thì đọc
    version.json trong repo. Raise RuntimeError nếu không đọc được.
    (v6.7) Repo đã public nên token không bắt buộc nữa."""
    # 1) Thử Releases/latest.
    try:
        data = goi_github_api(GITHUB_API_LATEST_RELEASE, token)
        tag = (data.get("tag_name") or "").strip()
        if tag and so_sanh_version(tag, VERSION) > 0:
            tai_url = None
            ten_file = None
            for asset in data.get("assets") or []:
                if (asset.get("name") or "") == APP_TITLE + ".exe":
                    tai_url = asset.get("url")
                    ten_file = asset.get("name")
                    break
            return {"version_moi": tag.lstrip("vV"), "tag": tag,
                    "tai_url": tai_url, "ten_file": ten_file}
        if tag:
            return None
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise RuntimeError("GitHub API báo lỗi HTTP %d." % e.code)
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError("Không kết nối được GitHub: %s" % e)
    # 2) Chưa có Release: đọc version.json trong repo.
    try:
        data = goi_github_api(GITHUB_API_VERSION_JSON, token)
        import base64
        noi_dung = json.loads(base64.b64decode(data.get("content") or "").decode("utf-8"))
        ver = (noi_dung.get("version") or "").strip()
        if ver and so_sanh_version(ver, VERSION) > 0:
            return {"version_moi": ver, "tag": "v" + ver,
                    "tai_url": None, "ten_file": None}
        return None
    except Exception as e:
        raise RuntimeError("Không đọc được version trên GitHub: %s" % e)


def tai_ban_moi_va_cap_nhat(tai_url, token, log_cb=None):
    """(v6.2) Tải exe bản mới về file tạm <exe>.new, ghi script cập nhật
    (capnhat.bat) rồi trả về đường dẫn script. Script chờ tool thoát
    (file exe hết bị khóa) rồi thay exe cũ bằng exe mới và mở lại tool.
    Người gọi phải thoát tool ngay sau khi chạy script này."""
    exe_hien_tai = os.path.abspath(sys.executable) if getattr(sys, "frozen", False) else None
    if not exe_hien_tai:
        raise RuntimeError("Đang chạy dạng mã nguồn (.py), không tự vá exe được. "
                           "Hãy dùng bản .exe đã cài.")
    thu_muc = os.path.dirname(exe_hien_tai)
    ten_exe = os.path.basename(exe_hien_tai)
    file_moi = os.path.join(thu_muc, ten_exe + ".new")
    if log_cb:
        log_cb("Đang tải bản mới về...")
    headers = {"Accept": "application/octet-stream"}
    if (token or "").strip():
        headers["Authorization"] = "token " + token.strip()
    tai_file_qua_url(tai_url, file_moi, 600, log_cb, "bản mới",
                     headers=headers)
    if not os.path.isfile(file_moi) or os.path.getsize(file_moi) < 1000000:
        _xoa_file_quiet(file_moi)
        raise RuntimeError("Tải bản mới về nhưng file không hợp lệ.")
    bat_path = os.path.join(thu_muc, "capnhat.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("@echo off\r\n")
        f.write("chcp 65001 >nul\r\n")
        f.write(":cho\r\n")
        f.write("ping -n 2 127.0.0.1 >nul\r\n")
        f.write('move /y "%s" "%s" >nul 2>&1\r\n' % (file_moi, exe_hien_tai))
        f.write("if errorlevel 1 goto cho\r\n")
        f.write('start "" "%s"\r\n' % exe_hien_tai)
        f.write('del "%%~f0"\r\n')
    return bat_path


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
    đoán theo cỡ file (file to = hình, file nhỏ = tiếng).
    (v7.6) Cả 2 file có thể cùng đuôi .mp4 (file tiếng IDM giờ là
    _tieng.mp4): phân biệt bằng luồng video của ffprobe, KHÔNG dựa
    vào đuôi file, nên không lẫn hình/tiếng."""
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


def dich_ten_sang_tieng_viet(ten_goc):
    """(v6.5) Dịch tên phim sang tiếng Việt bằng Google Translate miễn phí
    (không cần API key). Lỗi mạng / không dịch được thì giữ nguyên tên gốc.
    Trả về tên đã dịch (đã strip), hoặc tên gốc nếu dịch thất bại."""
    ten_goc = (ten_goc or "").strip()
    if not ten_goc:
        return "video"
    # Tên đã là tiếng Việt / không có chữ Trung thì khỏi dịch.
    if not re.search(r"[\u4e00-\u9fff]", ten_goc):
        return ten_goc
    try:
        query = urllib.parse.urlencode({
            "client": "gtx", "sl": "auto", "tl": "vi", "dt": "t",
            "q": ten_goc,
        })
        req = urllib.request.Request(
            "https://translate.googleapis.com/translate_a/single?" + query,
            headers={"User-Agent": UA_TRINH_DUYET})
        with urllib.request.urlopen(req, timeout=10) as resp:
            du_lieu = json.loads(resp.read().decode("utf-8", "replace"))
        dich = "".join(
            phan[0] for phan in (du_lieu[0] or []) if phan and phan[0])
        dich = dich.strip()
        return dich or ten_goc
    except Exception:
        return ten_goc


def ten_phim_tieng_viet(ten_goc, dich=True):
    """(v6.5) Tên phim dùng cho thư mục / file: tên đã dịch sang tiếng Việt,
    làm sạch ký tự cấm trên Windows. Thư mục tạo ra trùng tên phim này.
    (v7.3) dich=False (o "Tự dịch tên phim sang tiếng Việt" dang TAT):
    giu nguyen ten goc, KHONG goi dich - khong ton mang, khong doi ten."""
    if not dich:
        return sanitize_ten(ten_goc or "video")
    return sanitize_ten(dich_ten_sang_tieng_viet(ten_goc))


def ten_phim_tu_ten_file(duong_file, dich=True):
    """(v6.8) Lấy tên phim tiếng Việt từ tên file hình: bỏ đuôi file,
    bỏ hậu tố _hinh/_tieng/-hinh/-tieng và (1), (2)... rồi dịch sang
    tiếng Việt. Vd: 'Tên Trung_hinh.mp4' -> tên phim tiếng Việt.
    (v7.3) dich=False: chi bo hau to, giu nguyen ten goc."""
    ten = os.path.splitext(os.path.basename(duong_file or ""))[0].strip()
    for hau_to in ("_hinh", "_tieng", "-hinh", "-tieng"):
        if ten.lower().endswith(hau_to):
            ten = ten[:-len(hau_to)].strip()
            break
    ten = re.sub(r"\(\d+\)\s*$", "", ten).strip()
    return ten_phim_tieng_viet(ten, dich=dich)



# ======================================================================
# PHU DE v7.0 (ChipChipStudio)
# Nguon xac thuc DUY NHAT: yt-dlp --list-subs / -J (subtitles,
# automatic_captions). KHONG dung nut phu de tren trinh phat web
# Bilibili lam can cu (anh chup man hinh chi de tham khao) - nut do
# co the hien/ an theo tai khoan, con --list-subs tra ve danh sach
# phu de that cua video. Neu quet khong ra thi de TRONG, khong doan.
# QUY TAC THU MUC DU AN (v7.0, phu luc 4): moi thu cua 1 du an nam
# chung 1 thu muc phim: video, audio, .srt goc, .srt da dich (ghi de
# len file goc, co 1 ban .bak), MP3 long tieng HoaiMy. Khong rai rac.
# ======================================================================

def mo_thu_muc(duong_dan):
    """Mo thu muc trong Explorer (Windows) / file manager (he khac)."""
    if not duong_dan or not os.path.isdir(duong_dan):
        return False
    try:
        if sys.platform.startswith("win"):
            os.startfile(duong_dan)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", duong_dan])
        else:
            subprocess.Popen(["xdg-open", duong_dan])
        return True
    except Exception:
        return False


def mo_file_trong_explorer(duong_dan):
    """(v7.6) Mo thu muc chua file va CHON DUNG file do trong
    Explorer (Windows: explorer /select,). Dung cho nut "Mo thu
    muc phu de": file .srt co the nam ngoai thu muc du an (import
    tay) nen mo thu muc du an khong thay no. That bai thi tra
    False de ham goi mo thu muc cha bang mo_thu_muc()."""
    if not duong_dan or not os.path.isfile(duong_dan):
        return False
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen(["explorer", "/select,",
                              os.path.normpath(duong_dan)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", duong_dan])
        else:
            subprocess.Popen(["xdg-open", os.path.dirname(duong_dan)])
        return True
    except Exception:
        return False


def rut_gon_chu(text, gioi_han=40):
    """(v7.6) Rut gon chu de hien trong bang co dinh: qua gioi han
    thi cat o cuoi + "…". Gia tri day du KHONG mat: luu o job va
    hien o label chi tiet duoi bang khi chon dong."""
    text = (text or "").strip()
    if len(text) <= gioi_han:
        return text
    return text[:max(gioi_han - 1, 1)].rstrip() + "…"


def rut_gon_link(link):
    """(v7.6) Link Bilibili dai vi ?spm_id_from=...&vd_source=...:
    chi hien dang bilibili.com/video/BVxxxx. Khong co BV thi rut
    gon nhu chu thuong."""
    link = (link or "").strip()
    m = re.search(r"BV[0-9A-Za-z]+", link)
    if m:
        return "bilibili.com/video/" + m.group(0)
    return rut_gon_chu(link, 32)


def rut_gon_duong_dan(duong_dan):
    """(v7.6) Duong dan thu muc chi hien ...\\ten-thu-muc-cuoi."""
    duong_dan = (duong_dan or "").strip()
    if len(duong_dan) <= 28:
        return duong_dan
    phan = [p for p in re.split(r"[\\/]+", duong_dan) if p]
    cuoi = phan[-1] if phan else duong_dan
    if len(cuoi) > 25:
        cuoi = cuoi[-25:]
    return "…\\" + cuoi


def cap_nhat_job_trong_jobs(job):
    """Cap nhat 1 job vao jobs.json (dung chung cho QuanLy/CuaSoJob/
    tab phu de). Tra ve True neu ghi duoc."""
    try:
        jobs = doc_jobs()
        for i, j in enumerate(jobs):
            if j.get("id") == job.get("id"):
                jobs[i] = job
                break
        else:
            jobs.append(job)
        luu_jobs(jobs)
        return True
    except Exception:
        return False


def ten_file_phu_de(folder, ten_viet):
    """Ten file phu de trong thu muc phim: <Ten phim TV>.srt"""
    return os.path.join(folder or "", sanitize_ten(ten_viet) + ".srt")


def ten_file_phu_de_vi(folder, ten_viet):
    """Ban dich rieng (tuy chon, khong phai mac dinh): <Ten>_vi.srt"""
    return os.path.join(folder or "", sanitize_ten(ten_viet) + "_vi.srt")


def sao_luu_bak(duong_dan):
    """(v7.0) Sao luu 1 ban .bak truoc khi ghi de file goc. Chi tao
    1 lan: neu file .bak da co thi giu nguyen (do moi la ban goc that),
    khong ghi de len ban sao luu cu. Tra ve duong dan .bak hoac ''."""
    if not duong_dan or not os.path.isfile(duong_dan):
        return ""
    bak = duong_dan + ".bak"
    if os.path.isfile(bak):
        return bak
    try:
        shutil.copyfile(duong_dan, bak)
        return bak
    except Exception:
        return ""


def luu_ban_dich_an_toan(duong_dan, cac_cau_dich, log=None):
    """(v7.5) Luu ban dich DE LEN FILE GOC mot cach an toan, dung
    chung cho dich Gemini, dich thu cong va luong 1 mach:
    1) Sao luu 1 ban .bak truoc (sao_luu_bak: .bak da co thi GIU
    NGUYEN, khong ghi de len ban sao luu cu — file goc that chi duoc
    sao luu 1 lan duy nhat).
    2) Chi ghi de SAU KHI da co du ban dich (cac_cau_dich khong rong).
    Dich loi giua chung thi ham nay KHONG DUOC GOI, file goc con
    nguyen, khong mat. Tra ve (duong_dan, bak)."""
    if not cac_cau_dich:
        raise ValueError("Chưa có bản dịch để lưu.")
    bak = sao_luu_bak(duong_dan)
    ghi_srt_chung(cac_cau_dich, duong_dan)
    if log:
        log("Đã lưu đè bản dịch lên file gốc: %s (bản sao lưu: %s)"
            % (duong_dan, bak or "không có"))
    return duong_dan, bak


def ghep_ban_dich_thu_cong(cac_cau_goc, ban_dich):
    """(v7.5) Ghep ban dich thu cong: giu NGUYEN moc gio goc,
    lay chu tieng Viet tu ban_dich {chi_so: text} (khoa so hoac
    chuoi); cau nao chua go thi giu nguyen chu goc de SRT van du
    cau. Tra ve list cau da dich. Khong goi mang."""
    ban_dich = ban_dich or {}
    out = []
    for c in cac_cau_goc or []:
        chi_so = c.get("chi_so")
        text = ban_dich.get(chi_so)
        if text is None:
            text = ban_dich.get(str(chi_so))
        text = (text or "").strip()
        out.append({"chi_so": chi_so,
                    "bat_dau_ms": c.get("bat_dau_ms"),
                    "ket_thuc_ms": c.get("ket_thuc_ms"),
                    "text": text if text else (c.get("text") or "")})
    return out


def dinh_dang_ms_srt(ms):
    ms = int(ms)
    s, mmm = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, mmm)


def ghi_srt_chung(cac_cau, duong_dan):
    """Ghi list cau {chi_so, bat_dau_ms, ket_thuc_ms, text} ra file .srt."""
    os.makedirs(os.path.dirname(os.path.abspath(duong_dan)) or ".", exist_ok=True)
    with open(duong_dan, "w", encoding="utf-8") as f:
        for i, c in enumerate(cac_cau, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (
                c.get("chi_so") or i,
                dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
                dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0),
                (c.get("text") or "").strip()))


def doc_srt_text(noi_dung):
    """Parse noi dung SRT dang text (vd: ket qua tra ve cua API dich).
    Tra ve list cau, [] neu khong parse duoc."""
    try:
        import tempfile
        fd, tam = tempfile.mkstemp(suffix=".srt")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(noi_dung)
        try:
            return doc_srt(tam)
        finally:
            _xoa_file_quiet(tam)
    except Exception:
        return []


# ---------------- kiem tra / tai phu de ----------------

def parse_ket_qua_list_subs(text):
    """Parse output cua `yt-dlp --list-subs --skip-download`.
    Vi du dong co phu de:
      zh-Hans  srt, vtt
      zh-CN    srt
      en       vtt, srt
    Dong 'has no subtitles' / 'No subtitles' -> (False, []).
    Tra ve (has_subtitle, [ngon ngu...]). Khong tim thay thi (False, []),
    KHONG doan co phu de."""
    if not text:
        return False, []
    if re.search(r"no subtitles|has no subtitle", text, re.I):
        return False, []
    langs = []
    for dong in text.splitlines():
        m = re.match(r"\s*([a-z]{2,3}(?:-[A-Za-z0-9]+)?)\s+(srt|vtt|ass|ttml|json3|srv[123]?)\b",
                     dong)
        if m and m.group(1) not in langs:
            langs.append(m.group(1))
        # dang "zh-Hans srt, vtt" cung khop regex tren (chi lay srt dau);
        # dang chi co ten ngon ngu + danh sach dinh dang:
        m2 = re.match(r"\s*([a-z]{2,3}(?:-[A-Za-z0-9]+)?)\s+((?:srt|vtt|ass|ttml)(?:\s*,\s*(?:srt|vtt|ass|ttml))*)",
                      dong)
        if m2 and m2.group(1) not in langs:
            langs.append(m2.group(1))
    return (len(langs) > 0), langs


def kiem_tra_phu_de(url, cookies):
    """(v7.0) Kiem tra phu de bang yt-dlp --list-subs --skip-download.
    Tra ve {"has_subtitle": bool, "languages": [...]}.
    Neu lenh loi / khong chay duoc thi tra (False, []) - de trong,
    khong doan. Fallback: -J co subtitles/automatic_captions."""
    url = chuan_hoa_link_bilibili(url)
    ytdlp = tim_ytdlp()
    if not ytdlp:
        return {"has_subtitle": False, "languages": []}
    cmd = [ytdlp, "--list-subs", "--skip-download", "--no-playlist"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           errors="replace", timeout=120,
                           **chay_ngam_kwargs())
        out = (r.stdout or "") + "\n" + (r.stderr or "")
        co, langs = parse_ket_qua_list_subs(out)
        if co:
            return {"has_subtitle": True, "languages": langs}
    except Exception:
        pass
    # (v7.4) Fallback: doc -J, lay key subtitles/automatic_captions
    # (co cookies thi -J thay ai-zh, khong cookies thi {} / None).
    try:
        cmd2 = [ytdlp, "-J", "--no-playlist"]
        if cookies and os.path.isfile(cookies):
            cmd2 += ["--cookies", cookies]
        cmd2.append(url)
        r2 = subprocess.run(cmd2, capture_output=True, text=True,
                            errors="replace", timeout=120,
                            **chay_ngam_kwargs())
        info = json.loads(r2.stdout or "{}")
        langs2 = []
        for kho in ("subtitles", "automatic_captions"):
            for lang in (info.get(kho) or {}).keys():
                if lang and lang not in langs2:
                    langs2.append(lang)
        if langs2:
            return {"has_subtitle": True, "languages": langs2}
    except Exception:
        pass
    return {"has_subtitle": False, "languages": []}


def thu_tu_ngon_ngu_phu_de(langs_da_dung):
    """(v7.4) Thu tu thu ngon ngu phu de khi tai: ngon ngu da do duoc
    tu --list-subs truoc (uu tien ai-zh - phu de AI cua Bilibili),
    roi zh-Hans/zh-CN/zh, roi en. Khong trung lap."""
    thu_tu = []
    for lang in (langs_da_dung or []):
        lang = (lang or "").strip()
        if lang and lang not in thu_tu:
            thu_tu.append(lang)
    # ai-zh len dau (sort on dinh: ai-zh ve truoc, cac ngon ngu khac
    # giu nguyen thu tu da do).
    thu_tu.sort(key=lambda l: 0 if l.lower() == "ai-zh" else 1)
    for lang in ("zh-Hans", "zh-CN", "zh", "en"):
        if lang not in thu_tu:
            thu_tu.append(lang)
    return thu_tu


def chuyen_json_phu_de_bilibili_sang_cac_cau(du_lieu):
    """(v7.4) JSON phu de Bilibili -> list cau {chi_so, bat_dau_ms,
    ket_thuc_ms, text}.
    Dang 1 (API aisubtitle): {"body": [{"from": 1.2, "to": 3.4,
    "content": "..."}, ...]} - from/to tinh theo GIAY.
    Dang 2 (json3 cua yt-dlp): {"events": [{"tStartMs": 1200,
    "dDurationMs": 2200, "segs": [{"utf8": "..."}]}, ...]}.
    Tra ve [] neu khong parse duoc."""
    cac_cau = []
    try:
        if isinstance(du_lieu, dict) and isinstance(du_lieu.get("body"), list):
            for i, muc in enumerate(du_lieu["body"], 1):
                noi_dung = (muc.get("content") or "").strip()
                if not noi_dung:
                    continue
                cac_cau.append({
                    "chi_so": i,
                    "bat_dau_ms": int(float(muc.get("from", 0)) * 1000),
                    "ket_thuc_ms": int(float(muc.get("to", 0)) * 1000),
                    "text": noi_dung})
            return cac_cau
        if isinstance(du_lieu, dict) and isinstance(du_lieu.get("events"), list):
            for ev in du_lieu["events"]:
                segs = ev.get("segs") or []
                noi_dung = "".join(s.get("utf8", "") for s in segs
                                   if isinstance(s, dict)).strip()
                if not noi_dung:
                    continue
                bat_dau = int(ev.get("tStartMs") or 0)
                cac_cau.append({
                    "chi_so": len(cac_cau) + 1,
                    "bat_dau_ms": bat_dau,
                    "ket_thuc_ms": bat_dau + int(ev.get("dDurationMs") or 0),
                    "text": noi_dung})
            return cac_cau
    except Exception:
        return []
    return cac_cau


def _ts_vtt_sang_ms(chuoi):
    """'00:00:01.000' (VTT) -> ms."""
    m = re.match(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})", chuoi.strip())
    if not m:
        return None
    h = int(m.group(1) or 0)
    return ((h * 3600 + int(m.group(2)) * 60 + int(m.group(3))) * 1000
            + int(m.group(4)))


def chuyen_vtt_sang_cac_cau(text):
    """(v7.4) Noi dung .vtt -> list cau SRT. Bo header WEBVTT, bo
    the <c...> / vi tri, doi dau '.' trong timestamp thanh ','."""
    cac_cau = []
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    khoi = [k.strip("\n") for k in re.split(r"\n\s*\n", text) if k.strip()]
    for k in khoi:
        dong = [d for d in k.split("\n") if d.strip() != ""]
        if not dong or dong[0].strip().upper().startswith("WEBVTT"):
            continue
        i_ts = None
        for i, d in enumerate(dong):
            if "-->" in d:
                i_ts = i
                break
        if i_ts is None:
            continue
        phan = dong[i_ts].split("-->")
        bat_dau = _ts_vtt_sang_ms(phan[0])
        ket_thuc = _ts_vtt_sang_ms(phan[1]) if len(phan) > 1 else None
        if bat_dau is None or ket_thuc is None:
            continue
        noi_dung = " ".join(dong[i_ts + 1:]).strip()
        noi_dung = re.sub(r"<[^>]+>", "", noi_dung).strip()
        if not noi_dung:
            continue
        cac_cau.append({"chi_so": len(cac_cau) + 1,
                        "bat_dau_ms": bat_dau, "ket_thuc_ms": ket_thuc,
                        "text": noi_dung})
    return cac_cau


def chuyen_file_phu_de_sang_srt(duong_dan, dich):
    """(v7.4) Doi file phu de .vtt / .json / .json3 ve .srt tai `dich`.
    Tra ve dich neu doi duoc, None neu khong. File goc giu nguyen."""
    try:
        ext = os.path.splitext(duong_dan)[1].lower()
        with open(duong_dan, "r", encoding="utf-8-sig", errors="replace") as f:
            noi_dung = f.read()
        cac_cau = []
        if ext == ".vtt":
            cac_cau = chuyen_vtt_sang_cac_cau(noi_dung)
        else:
            try:
                du_lieu = json.loads(noi_dung)
            except Exception:
                return None
            cac_cau = chuyen_json_phu_de_bilibili_sang_cac_cau(du_lieu)
        if not cac_cau:
            return None
        ghi_srt_chung(cac_cau, dich)
        return dich
    except Exception:
        return None


def lay_cookies_dict(cookies_path):
    """(v7.4) Doc file cookies.txt (Netscape) -> dict {ten: gia tri}.
    Dung DUNG file cookies san co cua job (khong doi cach xu ly
    cookies, khong hoi cookies moi)."""
    ket_qua = {}
    try:
        with open(cookies_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 7:
                    ten, gia_tri = parts[5].strip(), parts[6].strip()
                    if ten and gia_tri:
                        ket_qua[ten] = gia_tri
    except Exception:
        pass
    return ket_qua


WBI_MIXIN_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43,
    5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16,
    24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59,
    6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
]


def tinh_wbi_mixin_key(img_key, sub_key):
    """(v7.5) Mixin key WBI theo thuat toan cong khai cua Bilibili
    (bili-api / cac client mo): xao tron img_key + sub_key theo bang
    co dinh 64 vi tri, lay 32 ky tu dau. Tra ve "" neu khong du."""
    raw = (img_key or "") + (sub_key or "")
    if len(raw) < 64:
        return ""
    return "".join(raw[i] for i in WBI_MIXIN_TAB)[:32]


def lay_wbi_mixin_key(headers, log=None):
    """(v7.5) Lay mixin key qua nav API (x/web-interface/nav ->
    data.wbi_img.img_url/sub_url, lay ten file khong duoi .png).
    Tra ve "" neu khong lay duoc (khi do bo qua URL WBI da ky)."""
    try:
        req = urllib.request.Request(
            "https://api.bilibili.com/x/web-interface/nav", headers=headers)
        with mo_url_co_fallback_ssl(req, timeout=20, log_cb=log) as resp:
            nav = json.loads(resp.read().decode("utf-8", "replace"))
        wbi = (nav.get("data") or {}).get("wbi_img") or {}
        img = os.path.splitext(os.path.basename(wbi.get("img_url") or ""))[0]
        sub = os.path.splitext(os.path.basename(wbi.get("sub_url") or ""))[0]
        return tinh_wbi_mixin_key(img, sub)
    except Exception:
        return ""


def ky_url_wbi(url_goc, mixin_key):
    """(v7.5) Ky URL WBI: them wts (giay hien tai) + w_rid =
    md5(urlencode(params da sap xep) + mixin_key)."""
    parsed = urllib.parse.urlparse(url_goc)
    params = dict(urllib.parse.parse_qsl(parsed.query))
    params["wts"] = str(int(time.time()))
    chuoi = urllib.parse.urlencode(sorted(params.items())) + mixin_key
    params["w_rid"] = hashlib.md5(chuoi.encode("utf-8")).hexdigest()
    moi = urllib.parse.urlencode(sorted(params.items()))
    return urllib.parse.urlunparse(parsed._replace(query=moi))


def _doc_json_url(url, headers, log=None):
    """GET 1 URL JSON qua mo_url_co_fallback_ssl. Raise neu loi."""
    req = urllib.request.Request(url, headers=headers)
    with mo_url_co_fallback_ssl(req, timeout=30, log_cb=log) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def kiem_tra_khop_video(data, bvid, cid, aid):
    """(v7.5) Kiem tra data.bvid/cid/aid cua player API co khop dung
    video dang can khong (tranh lay nham sub video khac). Truong nao
    co trong data thi phai khop; it nhat 1 trong aid/cid phai co va
    khop, neu khong co truong nao thi coi nhu khong khop."""
    if not isinstance(data, dict):
        return False
    co_truong = False
    if data.get("bvid"):
        co_truong = True
        if str(data.get("bvid")) != str(bvid):
            return False
    if data.get("aid"):
        co_truong = True
        try:
            if int(data.get("aid")) != int(aid):
                return False
        except Exception:
            return False
    if data.get("cid"):
        co_truong = True
        try:
            if int(data.get("cid")) != int(cid):
                return False
        except Exception:
            return False
    return co_truong


def ten_file_phu_de_api(folder, ten_viet, bvid, page, cid, lan):
    """(v7.5) Ten file phu de theo Vietsubk+:
    <ten>_<BV>_P<page>_cid<cid>_<lan>.srt"""
    return os.path.join(
        folder or "",
        "%s_%s_P%d_cid%s_%s.srt" % (
            sanitize_ten(ten_viet), bvid, page, cid,
            sanitize_ten(lan or "zh")))


def danh_gia_do_phu(cac_cau, duration):
    """(v7.5) Do phu phu de = maxEnd / duration. Tra ve None neu
    khong co cau nao hoac khong biet thoi luong video."""
    if not cac_cau or not duration:
        return None
    try:
        dur = float(duration)
    except Exception:
        return None
    if dur <= 0:
        return None
    max_end = max((c.get("ket_thuc_ms") or 0) for c in cac_cau) / 1000.0
    return max_end / dur


def tai_phu_de_qua_api_bilibili(url, folder, ten_viet, cookies, log=None, page=1):
    """(v7.5) DU PHONG khi yt-dlp khong tai duoc phu de — luong API
    truc tiep theo Vietsubk+ v5.9.2 (da doc code that):
    view API (lay aid/cid/duration, pages[] cho cid tung phan) ->
    thu WBI da ky -> WBI khong ky /x/player/wbi/v2 -> plain
    /x/player/v2, gui SESSDATA tu DUNG file cookies san co cua job
    (cookies_var / COOKIES_MAC_DINH neu file ton tai) + Referer,
    kiem tra data.bvid/cid/aid phai khop dung video (khong khop la
    bo), track AI chi tin khi nguon la wbi-player (track AI tu
    plain-player thi AI_SUBTITLE_SOURCE_NOT_READY), need_login_subtitle
    =true thi bao can dang nhap, chi lay subtitle_url https o
    hdslb.com/bilibili.com/bilivideo.com, tai JSON body
    (from/to/content, giay) -> sap xep theo gio -> doi sang SRT,
    ten file kieu Vietsubk+, kiem tra do phu maxEnd/duration <0.4
    thi nghi ngo (van luu file nhung danh dau, khong trinh bay nhu
    phu de tot). Khong co phu de thi tra None, KHONG tao file SRT
    rong, KHONG tao file gia. Tra ve duong dan .srt hoac None."""
    def _log(s):
        if log:
            log(s)
    m = re.search(r"BV[0-9A-Za-z]+", url or "")
    if not m:
        _log("API Bilibili: không lấy được BVid từ link.")
        return None
    bvid = m.group(0)
    headers = {"User-Agent": UA_TRINH_DUYET,
               "Referer": "https://www.bilibili.com/video/" + bvid}
    cookie_dict = {}
    if cookies and os.path.isfile(cookies):
        cookie_dict = lay_cookies_dict(cookies)
        _log("API Bilibili: dùng file cookies sẵn có (%s, %d cookie)."
             % (cookies, len(cookie_dict)))
    if cookie_dict:
        headers["Cookie"] = "; ".join("%s=%s" % (k, v)
                                      for k, v in cookie_dict.items())
    os.makedirs(folder or ".", exist_ok=True)
    # 1) view API: lay aid + cid (theo page) + duration.
    try:
        info = _doc_json_url(
            "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid,
            headers, _log)
    except Exception as e:
        _log("API Bilibili: lỗi gọi view API (%s)." % e)
        return None
    try:
        data = info.get("data") or {}
        aid = data.get("aid")
        pages = data.get("pages") or []
        duration = data.get("duration")
        if pages:
            idx = max(0, min(int(page or 1) - 1, len(pages) - 1))
            cid = pages[idx].get("cid")
            page_so = idx + 1
        else:
            cid = data.get("cid")
            page_so = int(page or 1)
    except Exception:
        aid = cid = duration = None
        page_so = int(page or 1)
    if not aid or not cid:
        _log("API Bilibili: view API không trả aid/cid.")
        return None
    # 2) Thu tu Vietsubk+: WBI da ky -> WBI khong ky -> plain v2.
    mixin = lay_wbi_mixin_key(headers, _log)
    co_so = "https://api.bilibili.com/x/player/wbi/v2"
    tham_so = "aid=%s&bvid=%s&cid=%s" % (aid, bvid, cid)
    ung_vien = []
    if mixin:
        ung_vien.append((ky_url_wbi(co_so + "?" + tham_so, mixin), "wbi-signed"))
        _log("API Bilibili: đã tính được khóa WBI, thử URL WBI đã ký trước.")
    else:
        _log("API Bilibili: không lấy được khóa WBI, bỏ qua URL WBI đã ký.")
    ung_vien.append((co_so + "?" + tham_so, "wbi"))
    ung_vien.append(("https://api.bilibili.com/x/player/v2?" + tham_so,
                     "plain"))
    host_cho_phep = ("hdslb.com", "bilibili.com", "bilivideo.com")
    for player_url, nguon in ung_vien:
        try:
            player = _doc_json_url(player_url, headers, _log)
        except Exception as e:
            _log("API Bilibili (%s): lỗi gọi player (%s)." % (nguon, e))
            continue
        if not isinstance(player, dict) or player.get("code") != 0:
            _log("API Bilibili (%s): trả về lỗi (code=%s)."
                 % (nguon, player.get("code") if isinstance(player, dict) else "?"))
            continue
        data_p = player.get("data") or {}
        if not kiem_tra_khop_video(data_p, bvid, cid, aid):
            _log("API Bilibili (%s): BỎ — bvid/cid/aid không khớp video "
                 "đang cần (tránh lấy nhầm phụ đề video khác)." % nguon)
            continue
        sub = data_p.get("subtitle") or {}
        if sub.get("need_login_subtitle"):
            _log("API Bilibili (%s): cần đăng nhập (need_login_subtitle) "
                 "— kiểm tra file cookies.txt (SESSDATA)." % nguon)
        danh_sach = sub.get("subtitles") or []
        if not danh_sach:
            _log("API Bilibili (%s): không có phụ đề." % nguon)
            continue
        # Uu tien ai-zh, roi ngon ngu khac.
        danh_sach = sorted(
            danh_sach,
            key=lambda s: 0 if (s.get("lan") or "") == "ai-zh" else 1)
        for muc in danh_sach:
            lan = (muc or {}).get("lan") or "zh"
            la_ai = bool((muc or {}).get("ai_type")) or lan == "ai-zh"
            if la_ai and nguon == "plain":
                _log("API Bilibili (plain): AI_SUBTITLE_SOURCE_NOT_READY — "
                     "track AI (%s) từ plain-player, chưa tin được, "
                     "thử nguồn khác." % lan)
                continue
            sub_url = (muc or {}).get("subtitle_url") or ""
            if not sub_url:
                continue
            if not sub_url.startswith("http"):
                sub_url = "https:" + sub_url
            host = (urllib.parse.urlparse(sub_url).netloc or "").lower()
            if not any(host == h or host.endswith("." + h)
                       for h in host_cho_phep):
                _log("API Bilibili: BỎ subtitle_url lạ (%s)." % sub_url)
                continue
            try:
                du_lieu = _doc_json_url(sub_url, headers, _log)
            except Exception as e:
                _log("API Bilibili: lỗi tải subtitle_url (%s)." % e)
                continue
            cac_cau = chuyen_json_phu_de_bilibili_sang_cac_cau(du_lieu)
            if not cac_cau:
                continue
            cac_cau.sort(key=lambda c: c.get("bat_dau_ms") or 0)
            dich = ten_file_phu_de_api(folder, ten_viet, bvid, page_so,
                                       cid, lan)
            do_phu = danh_gia_do_phu(cac_cau, duration)
            try:
                ghi_srt_chung(cac_cau, dich)
            except Exception as e:
                _log("API Bilibili: lỗi ghi SRT (%s)." % e)
                return None
            if do_phu is not None and do_phu < 0.4:
                _log("API Bilibili (%s): NGHI NGỜ — độ phủ phụ đề chỉ "
                     "%.0f%% (<40%%), file vẫn lưu nhưng đánh dấu nghi "
                     "ngờ, độ phủ thấp, không trình bày như phụ đề tốt: "
                     "%s" % (lan, do_phu * 100, dich))
            else:
                _log("Đã tải phụ đề qua API Bilibili (%s, nguồn %s): %s"
                     % (lan, nguon, dich))
            return dich
        _log("API Bilibili (%s): có danh sách nhưng không đổi được track "
             "nào sang SRT." % nguon)
    _log("API Bilibili: không lấy được phụ đề nào dùng được — video "
         "này có thể không có phụ đề, hoặc cần đăng nhập (kiểm tra "
         "cookies.txt).")
    return None

def tai_phu_de(url, folder, ten_viet, cookies, log=None, langs_da_dung=None):
    """(v7.4) Tai phu de ve CUNG thu muc phim, ten <Ten phim TV>.srt.
    (v7.3) chi thu zh-Hans/zh-CN/zh roi en, KHONG bao gio thu ai-zh
    da do duoc, va dung --sub-format srt trong khi ai-zh cua Bilibili
    la json3 -> bao khong tim ra du quet thay "Co phu de (ai-zh)".
    (v7.4) thu dung ngon ngu DA DO DUOC truoc (uu tien ai-zh), them
    --write-auto-subs + --convert-subs srt de json3 doi sang SRT;
    file .vtt/.json3/.json tai ve duoc doi sang SRT trong code.
    Dung DUNG file cookies san co cua job (--cookies <file> cho yt-dlp,
    SESSDATA tu file do cho API du phong), khong doi cach xu ly cookies.
    yt-dlp that bai het thi dung API Bilibili truc tiep lam du phong.
    Tra ve duong dan file .srt hoac None neu khong co phu de de tai."""
    def _log(s):
        if log:
            log(s)
    url = chuan_hoa_link_bilibili(url)
    ytdlp = tim_ytdlp()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    os.makedirs(folder, exist_ok=True)
    dich = ten_file_phu_de(folder, ten_viet)
    ten_goc = sanitize_ten(ten_viet)
    for lang in thu_tu_ngon_ngu_phu_de(langs_da_dung):
        mau = os.path.join(folder, ten_goc)
        cmd = [ytdlp, "--skip-download", "--no-playlist",
               "--write-subs", "--write-auto-subs",
               "--sub-langs", lang,
               "--sub-format", "srt", "--convert-subs", "srt",
               "-o", mau + ".%(ext)s"]
        if cookies and os.path.isfile(cookies):
            cmd += ["--cookies", cookies]
        # (v7.5) Anh chup thu muc TRUOC khi chay: chi nhan file MOI
        # hoac DOI (mtime/size) sau lan chay nay — file SRT cu tu lan
        # truoc khong duoc tinh la vua tai ve (khong tra file cu,
        # khong ghi de file da co bang file rong).
        tap_truoc = {}
        try:
            for ten0 in os.listdir(folder):
                d0 = os.path.join(folder, ten0)
                if os.path.isfile(d0):
                    tap_truoc[ten0] = (os.path.getmtime(d0),
                                       os.path.getsize(d0))
        except Exception:
            tap_truoc = {}
        cmd.append(url)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               errors="replace", timeout=300,
                               **chay_ngam_kwargs())
        except Exception as e:
            _log("Tải phụ đề (%s): lỗi chạy yt-dlp (%s)." % (lang, e))
            continue
        _log("Tải phụ đề (%s): mã %d" % (lang, r.returncode))
        # yt-dlp ghi <ten>.<lang>.srt (hoac .vtt/.json3 neu chua doi
        # duoc) - doi/doi ten ve <ten>.srt. Chi xet file moi/doi,
        # file rong thi bo qua, khong dung.
        for ten in sorted(os.listdir(folder)):
            if not ten.startswith(ten_goc):
                continue
            duong = os.path.join(folder, ten)
            if not os.path.isfile(duong):
                continue
            try:
                tt = (os.path.getmtime(duong), os.path.getsize(duong))
            except Exception:
                continue
            if ten in tap_truoc and tap_truoc[ten] == tt:
                continue
            if os.path.getsize(duong) <= 0:
                _log("Tải phụ đề (%s): file %s rỗng — bỏ qua, không dùng."
                     % (lang, ten))
                continue
            ext = os.path.splitext(ten)[1].lower()
            if ext == ".srt":
                if ten == os.path.basename(dich):
                    _log("Đã tải phụ đề qua yt-dlp (%s): %s" % (lang, dich))
                    return dich
                try:
                    if os.path.isfile(dich):
                        os.remove(dich)
                    os.rename(duong, dich)
                    _log("Đã tải phụ đề qua yt-dlp (%s): %s" % (lang, dich))
                    return dich
                except Exception:
                    return duong
            if ext in (".vtt", ".json", ".json3"):
                ket_qua = chuyen_file_phu_de_sang_srt(duong, dich)
                if ket_qua:
                    _log("Đã tải phụ đề qua yt-dlp (%s, đổi %s sang SRT): %s"
                         % (lang, ext, dich))
                    return ket_qua
    # yt-dlp that bai het -> API Bilibili truc tiep (du phong).
    _log("yt-dlp không tải được phụ đề, thử API Bilibili trực tiếp...")
    ket_qua = tai_phu_de_qua_api_bilibili(url, folder, ten_viet, cookies, _log)
    if ket_qua:
        return ket_qua
    _log("Không tải được phụ đề bằng yt-dlp lẫn API Bilibili. "
         "Phụ đề ai-zh của Bilibili thường cần đăng nhập - kiểm tra "
         "file cookies.txt (SESSDATA) rồi thử lại.")
    return None



def dich_srt_1_mach(cac_cau, log=None, dich_fn=None):
    """(v7.6) Dich bang dung logic cua tab Xu ly phu de (dich_srt):
    MAC DINH dich TOAN BO file trong 1 prompt duy nhat; neu toan
    bo loi thi tu chuyen sang chia cum 20 cau (du phong). dich_fn
    (cac_cau) -> list neu truyen (dung cho test). Raise RuntimeError
    neu thieu key — KHONG goi API khi khong co key. Muse (chat tay)
    thi raise loi huong dan dung che do chat tay, khong goi API.
    KHONG ghi gi len file goc o day (chi tra ve list cau dich);
    viec luu do chay_luong_1_mach / nut Luu lam SAU KHI dich xong
    va kiem tra khop, nen dich loi thi file goc con nguyen."""
    if dich_fn is not None:
        return dich_fn(cac_cau)
    cfg = doc_config()
    provider = chuan_hoa_provider(cfg.get("phu_de_provider") or "Gemini")
    if provider == "Muse":
        raise RuntimeError(
            "Nhà cung cấp đang chọn là Muse (trợ lý chat tay, không "
            "có API) — luồng 1 mạch không tự dịch được. Dùng chế độ "
            "chat tay: 'Xuất prompt + SRT toàn bộ' ở tab Xử lý phụ "
            "đề, dán vào chat với Muse, rồi 'Nhập bản dịch về' "
            "(file SRT gốc vẫn còn nguyên).")
    khoa = {"Gemini": "gemini_api_key", "GPT": "openai_api_key",
            "Claude": "anthropic_api_key"}.get(provider, "gemini_api_key")
    key = (cfg.get(khoa) or "").strip()
    if not key:
        raise RuntimeError(
            "Chưa có key %s — lưu key trong tab Xử lý phụ đề rồi "
            "chạy lại (file SRT gốc vẫn còn nguyên)." % provider)
    ket_qua, che_do = dich_srt(
        cac_cau, provider, key,
        cfg.get("phu_de_the_loai") or "",
        cfg.get("phu_de_nhan_vat") or "",
        cfg.get("phu_de_xung_ho") or "",
        cfg.get("phu_de_boi_canh") or "",
        model=model_cua_provider(provider, cfg),
        che_do=cfg.get("phu_de_che_do") or "toan_bo",
        log=log)
    if log:
        log("Đã dịch xong bằng chế độ: %s." % che_do)
    return ket_qua


def chay_luong_1_mach(url, folder, ten_viet, cookies, langs_da_dung,
                      tu_dich=False, log=None, tai_fn=None, dich_fn=None):
    """(v7.5) Luong 1 mach. UU TIEN SO 1: Buoc 1 LUON chay — lay SRT
    GOC tieng Trung (yt-dlp thu dung ai-zh -> API Bilibili luong
    Vietsubk+) ve thu muc du an, KHONG can key Gemini, KHONG goi
    dich, KHONG doi dich. Tai xong thi DUNG (tra ve ket qua de UI
    hoi cau chon tiep: Dich trong tool / Mo tab HoaiMy).
    Buoc 2 (dich Gemini) CHI chay khi tu_dich=True (MAC DINH TAT, vi
    CYAN dich bang AI ben ngoai): dich xong thi luu de file goc (co
    .bak 1 lan, qua luu_ban_dich_an_toan). Dich loi giua chung ->
    KHONG ghi gi len file goc, file goc con nguyen, tra ve loi buoc
    'dich'. Khong co phu de -> tra ve loi buoc 'lay_phu_de', KHONG
    tao file SRT nao.
    Tra ve dict {thanh_cong, buoc_dung, loi, srt_goc, srt_viet,
    da_dich, so_cau}."""
    def _log(s):
        if log:
            log(s)
    tai = tai_fn or tai_phu_de
    _log("Bước 1: Lấy phụ đề gốc (yt-dlp → API Bilibili)...")
    try:
        srt = tai(url, folder, ten_viet, cookies, _log,
                  langs_da_dung=langs_da_dung)
    except Exception as e:
        return {"thanh_cong": False, "buoc_dung": "lay_phu_de",
                "loi": "Lỗi tải phụ đề: %s" % e,
                "srt_goc": None, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    if not srt or not os.path.isfile(srt) or os.path.getsize(srt) <= 0:
        return {"thanh_cong": False, "buoc_dung": "lay_phu_de",
                "loi": "Không có phụ đề cho video này (quét + tải đều "
                       "không thấy). Không tạo file SRT nào.",
                "srt_goc": None, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    _log("Bước 1 xong: Đã tải SRT gốc: %s" % srt)
    if not tu_dich:
        _log("DỪNG tại đây: công tắc 'Tự dịch sau khi lấy phụ đề' đang "
             "TẮT — không tự dịch, không tự chuyển tab. Cậu chọn tiếp: "
             "Dịch trong tool / Mở tab HoaiMy.")
        return {"thanh_cong": True, "buoc_dung": "lay_phu_de",
                "loi": "", "srt_goc": srt, "srt_viet": None,
                "da_dich": False, "so_cau": 0}
    _log("Bước 2: Dịch sang tiếng Việt (giữ nguyên mốc giờ, chế độ "
         "toàn bộ 1 prompt, lỗi thì tự chuyển cụm 20 câu)...")
    try:
        cac_goc = doc_srt(srt)
        if not cac_goc:
            raise RuntimeError("Đọc được file SRT gốc nhưng không có "
                               "câu nào.")
        cac_dich = dich_srt_1_mach(cac_goc, _log, dich_fn=dich_fn)
    except Exception as e:
        _log("Dịch lỗi, file gốc còn nguyên: %s" % e)
        return {"thanh_cong": False, "buoc_dung": "dich",
                "loi": "Dịch lỗi: %s — file SRT gốc còn nguyên, không "
                       "mất." % e,
                "srt_goc": srt, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    if not cac_dich:
        _log("Dịch lỗi, file gốc còn nguyên: API không trả câu nào.")
        return {"thanh_cong": False, "buoc_dung": "dich",
                "loi": "Dịch lỗi: API không trả câu nào — file SRT gốc "
                       "còn nguyên, không mất.",
                "srt_goc": srt, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    # (v7.6) Kiem tra CUNG truoc khi luu: thieu/lech thi DUNG,
    # KHONG luu de (truoc day chi canh bao roi van luu).
    ok_khop, loi_khop = kiem_tra_ban_dich_khop_goc(cac_goc, cac_dich)
    if not ok_khop:
        _log("Bản dịch KHÔNG KHỚP file gốc (%s) — KHÔNG lưu, file "
             "gốc còn nguyên." % loi_khop)
        return {"thanh_cong": False, "buoc_dung": "dich",
                "loi": "Bản dịch không khớp file gốc: %s — file SRT "
                       "gốc còn nguyên, không mất." % loi_khop,
                "srt_goc": srt, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    _log("Bước 3: Lưu đè bản dịch lên file gốc (sao lưu .bak 1 lần)...")
    try:
        duong, bak = luu_ban_dich_an_toan(srt, cac_dich, _log)
    except Exception as e:
        return {"thanh_cong": False, "buoc_dung": "luu",
                "loi": "Lỗi lưu: %s — file SRT gốc còn nguyên." % e,
                "srt_goc": srt, "srt_viet": None, "da_dich": False,
                "so_cau": 0}
    return {"thanh_cong": True, "buoc_dung": "xong", "loi": "",
            "srt_goc": srt, "srt_viet": duong, "da_dich": True,
            "so_cau": len(cac_dich)}


def them_phu_de_tu_ngoai(job, parent=None):
    """(v7.0, phu luc 1) Them phu de thu cong cho 1 du an khi cot Phu de
    dang trong (khong tai duoc / khong tim duoc phu de).
    Mo hop chon file .srt, LUU DUONG DAN file vao job (khong copy file,
    KHONG ghi de file goc khi import), cap nhat cot Phu de thanh Co +
    ten file. Tra ve duong dan da chon hoac '' neu huy.
    Khong doan noi dung phu de."""
    p = filedialog.askopenfilename(
        title="Chọn file phụ đề .srt để thêm cho dự án",
        filetypes=[("Phụ đề SRT", "*.srt"), ("Mọi file", "*.*")])
    if not p:
        return ""
    job["subtitle_file"] = p
    job["has_subtitle"] = True
    job["subtitle_status"] = "da_them_tay"
    if not job.get("subtitle_langs"):
        job["subtitle_langs"] = []
    cap_nhat_job_trong_jobs(job)
    return p


# ---------------- dich phu de qua API ----------------

def tao_prompt_dich_phu_de(the_loai, nhan_vat, xung_ho, boi_canh, khoi_srt):
    """Prompt dich phu de: giu nguyen timestamp + thu tu cau, dich theo
    boi canh toan bo, dung ngu phap/xung ho/vai ve/gioi tinh, van phong
    dung boi canh. Tra ve prompt text."""
    return (
        "Bạn là dịch giả phụ đề phim. Dịch các câu phụ đề sau sang "
        "tiếng Việt, đúng bối cảnh toàn bộ, đúng tính cách/cảm xúc/"
        "tình huống từng câu, nghe tự nhiên như người Việt nói, "
        "không dịch word-by-word khô cứng.\n"
        "Thể loại: %s\nNhân vật: %s\nXưng hô/vai vế: %s\n"
        "Bối cảnh thêm: %s\n"
        "YÊU CẦU BẮT BUỘC: trả về ĐÚNG định dạng SRT gốc, giữ nguyên "
        "số thứ tự và timestamp từng câu, chỉ thay phần lời thoại "
        "bằng tiếng Việt. Không thêm/bớt câu, không giải thích thêm.\n\n"
        "%s\n" % (the_loai or "(chưa rõ)", nhan_vat or "(chưa rõ)",
                  xung_ho or "(theo phim)", boi_canh or "(không có)",
                  khoi_srt))


def chuan_hoa_provider(provider):
    """Ten nha cung cap hop le: Gemini / GPT / Claude / Muse.
    "Muse" o day la tro ly Muse (chat tay, KHONG co API), KHONG
    phai Claude/Anthropic. Trong thi mac dinh Gemini."""
    p = (provider or "").strip()
    if p in ("Gemini", "GPT", "Claude", "Muse"):
        return p
    return "Gemini" if not p else p


def model_cua_provider(provider, cfg=None):
    """Model da chon cho provider (tu config, nguoi dung chon/go
    o tab Xu ly phu de); trong thi dung mac dinh. Muse (chat tay)
    khong dung model API -> tra ''."""
    cfg = cfg or {}
    khoa = {"Gemini": "phu_de_model_gemini",
            "GPT": "phu_de_model_gpt",
            "Claude": "phu_de_model_claude"}.get(provider)
    if khoa is None:
        return ""
    mac_dinh = {"Gemini": MODEL_GEMINI_MAC_DINH,
                "GPT": MODEL_GPT_MAC_DINH,
                "Claude": MODEL_CLAUDE_MAC_DINH}.get(provider, "")
    return (cfg.get(khoa) or "").strip() or mac_dinh


def kiem_tra_ban_dich_khop_goc(cac_goc, cac_dich):
    """(v7.6) Kiem tra cung truoc khi cho luu de file goc: ban
    dich phai DU so cau, timestamp tung cau KHOP goc, cau nao
    cung co loi thoai. Tra (True, '') neu khop; (False, 'loi...')
    neu khong — ham goi KHONG DUOC luu de khi False, file goc
    con nguyen."""
    goc = cac_goc or []
    dich = cac_dich or []
    if len(dich) != len(goc):
        return (False, "sai số câu (gốc %d câu, bản dịch %d câu)"
                % (len(goc), len(dich)))
    for g, d in zip(goc, dich):
        if (d.get("bat_dau_ms") != g.get("bat_dau_ms")
                or d.get("ket_thuc_ms") != g.get("ket_thuc_ms")):
            return (False, "lệch timestamp ở câu #%s (gốc %s --> %s, "
                    "dịch %s --> %s)"
                    % (g.get("chi_so"),
                       dinh_dang_ms_srt(g.get("bat_dau_ms") or 0),
                       dinh_dang_ms_srt(g.get("ket_thuc_ms") or 0),
                       dinh_dang_ms_srt(d.get("bat_dau_ms") or 0),
                       dinh_dang_ms_srt(d.get("ket_thuc_ms") or 0)))
        if not (d.get("text") or "").strip():
            return (False, "câu #%s chưa có lời thoại trong bản dịch"
                    % (g.get("chi_so"),))
    return (True, "")


def _goi_gemini_once(model, key, prompt, timeout):
    """1 lan goi Gemini generateContent voi model da cho. Tra text
    tra loi; raise RuntimeError neu loi mang / tra ve khong doc duoc."""
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           + urllib.parse.quote(model) + ":generateContent?key="
           + urllib.parse.quote(key))
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        d = json.loads(resp.read().decode("utf-8", "replace"))
    try:
        return d["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise RuntimeError("Gemini trả về không đọc được: %s" % str(d)[:300])


def goi_api_dich(provider, api_key, prompt, model=None, toan_bo=False,
                 log=None):
    """Goi API dich (Gemini / GPT / Claude). Model lay tu tham so
    (da chon o tab Xu ly phu de, luu local), KHONG hardcode.
    Gemini mac dinh gemini-3.8-flash; loi thi thu 1 lan voi model
    du phong gemini-3.5-flash-lite. KHONG dung gemini-2.5-flash
    (deprecated, tat 01/12/2026). Muse = tro ly Muse (chat tay):
    KHONG co API key/endpoint trong tool — raise loi huong dan
    dung che do chat tay thay vi goi API la. Key KHONG ghi log."""
    provider = chuan_hoa_provider(provider)
    if provider == "Muse":
        raise RuntimeError(
            "Muse là trợ lý chat tay, không có API key/endpoint "
            "trong tool — dùng chế độ chat tay: bấm 'Xuất prompt + "
            "SRT toàn bộ', dán vào chat với Muse, rồi 'Nhập bản "
            "dịch về'. Không gọi API nào cho Muse.")
    if not (api_key or "").strip():
        raise RuntimeError("Chưa nhập API key cho %s (nhập ở tab Xử lý "
                           "phụ đề, key chỉ lưu local trong config.json)."
                           % provider)
    key = api_key.strip()
    timeout = 600 if toan_bo else 180
    if provider == "Gemini":
        model_chon = (model or "").strip() or MODEL_GEMINI_MAC_DINH
        try:
            return _goi_gemini_once(model_chon, key, prompt, timeout)
        except Exception as e:
            if model_chon == MODEL_GEMINI_DU_PHONG:
                raise
            if log:
                log("Gemini %s lỗi (%s) — thử lại với model dự phòng %s."
                    % (model_chon, e, MODEL_GEMINI_DU_PHONG))
            return _goi_gemini_once(MODEL_GEMINI_DU_PHONG, key, prompt,
                                    timeout)
    if provider == "GPT":
        model_chon = (model or "").strip() or MODEL_GPT_MAC_DINH
        url = "https://api.openai.com/v1/chat/completions"
        body = json.dumps({"model": model_chon, "messages": [
            {"role": "user", "content": prompt}]}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            d = json.loads(resp.read().decode("utf-8", "replace"))
        try:
            return d["choices"][0]["message"]["content"]
        except Exception:
            raise RuntimeError("GPT trả về không đọc được: %s" % str(d)[:300])
    if provider == "Claude":
        # Claude = Anthropic Messages API (truoc v7.6 goi nham la "Muse").
        model_chon = (model or "").strip() or MODEL_CLAUDE_MAC_DINH
        url = "https://api.anthropic.com/v1/messages"
        body = json.dumps({"model": model_chon,
                           "max_tokens": 64000 if toan_bo else 8000,
                           "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "x-api-key": key, "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            d = json.loads(resp.read().decode("utf-8", "replace"))
        try:
            return "".join(p.get("text", "") for p in d.get("content", []))
        except Exception:
            raise RuntimeError("Claude trả về không đọc được: %s" % str(d)[:300])
    raise RuntimeError("Nhà cung cấp không rõ: %s" % provider)


def dich_srt_toan_bo(cac_cau, provider, api_key, the_loai, nhan_vat,
                     xung_ho, boi_canh, model=None, log=None):
    """(v7.6) Dich TOAN BO file SRT goc trong 1 prompt duy nhat
    (dung dung prompt tao_prompt_dich_phu_de: dich theo boi canh
    toan bo, dung tinh cach/cam xuc/tinh huong tung cau, tu nhien
    nhu nguoi Viet noi, khong word-by-word, tra DUNG dinh dang
    SRT goc, giu nguyen so thu tu + timestamp, chi thay loi thoai,
    khong them/bot cau, khong giai thich). File dai vai nghin cau
    gui 1 lan de bi cat/timeout/lech — nen kiem tra cung: thieu
    cau, sai so cau hoac lech timestamp thi raise RuntimeError,
    KHONG tra ve ban dich lech, ham goi KHONG luu gi, file goc
    con nguyen. Tra list cau dich (timestamp lay tu goc)."""
    if not cac_cau:
        raise RuntimeError("Không có câu nào để dịch.")
    khoi = []
    for c in cac_cau:
        khoi.append("%d\n%s --> %s\n%s" % (
            c.get("chi_so") or 0,
            dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
            dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0),
            c.get("text") or ""))
    prompt = tao_prompt_dich_phu_de(the_loai, nhan_vat, xung_ho,
                                    boi_canh, "\n\n".join(khoi))
    if log:
        log("Chế độ dịch: toàn bộ 1 prompt (%d câu, %s)."
            % (len(cac_cau), provider))
    tra_loi = goi_api_dich(provider, api_key, prompt, model=model,
                           toan_bo=True, log=log)
    da_parse = doc_srt_text(tra_loi)
    ok, loi = kiem_tra_ban_dich_khop_goc(cac_cau, da_parse)
    if not ok:
        raise RuntimeError(
            "Bản dịch toàn bộ KHÔNG KHỚP file gốc: %s — không lưu "
            "gì, file gốc còn nguyên. Thử lại, hoặc để tool tự "
            "chuyển sang chia cụm 20 câu." % loi)
    return [{"chi_so": g.get("chi_so"),
             "bat_dau_ms": g.get("bat_dau_ms"),
             "ket_thuc_ms": g.get("ket_thuc_ms"),
             "text": m.get("text") or g.get("text")}
            for g, m in zip(cac_cau, da_parse)]


def dich_srt(cac_cau, provider, api_key, the_loai, nhan_vat, xung_ho,
             boi_canh, model=None, che_do="toan_bo", tien_trinh_cb=None,
             dung_event=None, log=None):
    """(v7.6) Dieu phoi dich: mac dinh TOAN BO 1 prompt; neu toan
    bo loi (cat/timeout/lech) thi TU CHUYEN sang chia cum 20 cau
    (du phong, dich_srt_theo_cum) va ghi ro che do da dung vao
    log. che_do="cum" thi chi dich theo cum ngay tu dau. Tra
    (ket_qua, che_do_da_dung). Muse (chat tay) thi raise loi
    huong dan, khong goi API."""
    provider = chuan_hoa_provider(provider)
    if provider == "Muse":
        raise RuntimeError(
            "Muse là trợ lý chat tay, không có API — dùng chế độ "
            "chat tay: 'Xuất prompt + SRT toàn bộ' rồi 'Nhập bản "
            "dịch về'.")
    if (che_do or "toan_bo") == "cum":
        if log:
            log("Chế độ dịch: chỉ chia cụm 20 câu (theo lựa chọn).")
        ket = dich_srt_theo_cum(
            cac_cau, provider, api_key, the_loai, nhan_vat, xung_ho,
            boi_canh, tien_trinh_cb=tien_trinh_cb, dung_event=dung_event,
            model=model, log=log)
        return (ket, "cum")
    try:
        ket = dich_srt_toan_bo(
            cac_cau, provider, api_key, the_loai, nhan_vat, xung_ho,
            boi_canh, model=model, log=log)
        if tien_trinh_cb:
            tien_trinh_cb(100)
        return (ket, "toan_bo")
    except Exception as e:
        if dung_event is not None and dung_event.is_set():
            raise
        if log:
            log("Dịch toàn bộ lỗi (%s) — tự chuyển sang chia cụm "
                "20 câu (dự phòng)." % e)
        ket = dich_srt_theo_cum(
            cac_cau, provider, api_key, the_loai, nhan_vat, xung_ho,
            boi_canh, tien_trinh_cb=tien_trinh_cb, dung_event=dung_event,
            model=model, log=log)
        return (ket, "cum (dự phòng sau khi toàn bộ lỗi)")


def dich_srt_theo_cum(cac_cau, provider, api_key, the_loai, nhan_vat,
                      xung_ho, boi_canh, tien_trinh_cb=None,
                      dung_event=None, model=None, log=None):
    """Dich SRT theo cum 20 cau, giu timestamp goc. Tra ve list cau da
    dich (cung chi_so/bat_dau/ket_thuc, text tieng Viet). Neu API tra
    ve khong parse duoc thanh SRT thi map theo thu tu cau.
    (v7.6) Day la che do DU PHONG cua dich toan bo: chi dung khi
    nguoi dung chon "cum", hoac khi dich toan bo loi va tool tu
    chuyen sang. Timestamp lay tu goc nen luon khop goc."""
    ket_qua = []
    cum = 20
    for bat_dau in range(0, len(cac_cau), cum):
        if dung_event is not None and dung_event.is_set():
            break
        nhom = cac_cau[bat_dau:bat_dau + cum]
        khoi = []
        for c in nhom:
            khoi.append("%d\n%s --> %s\n%s" % (
                c.get("chi_so") or 0,
                dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
                dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0),
                c.get("text") or ""))
        prompt = tao_prompt_dich_phu_de(the_loai, nhan_vat, xung_ho,
                                        boi_canh, "\n\n".join(khoi))
        tra_loi = goi_api_dich(provider, api_key, prompt, model=model,
                               log=log)
        da_parse = doc_srt_text(tra_loi)
        if len(da_parse) == len(nhom):
            for goc, moi in zip(nhom, da_parse):
                ket_qua.append({"chi_so": goc.get("chi_so"),
                                "bat_dau_ms": goc.get("bat_dau_ms"),
                                "ket_thuc_ms": goc.get("ket_thuc_ms"),
                                "text": moi.get("text") or goc.get("text")})
        else:
            # Fallback: lay tung dong khong phai so/timestamp lam ban dich.
            dong_dich = [d.strip() for d in tra_loi.splitlines()
                         if d.strip() and not d.strip().isdigit()
                         and "-->" not in d]
            for i, goc in enumerate(nhom):
                text = dong_dich[i] if i < len(dong_dich) else goc.get("text")
                ket_qua.append({"chi_so": goc.get("chi_so"),
                                "bat_dau_ms": goc.get("bat_dau_ms"),
                                "ket_thuc_ms": goc.get("ket_thuc_ms"),
                                "text": text})
        if tien_trinh_cb:
            tien_trinh_cb(min(100, int(len(ket_qua) * 100 / max(1, len(cac_cau)))))
    return ket_qua

def luu_file_thong_tin_phim(folder, ten_goc, ten_viet, url, chat_luong=""):
    """(v6.5) Tạo 1 file text trong thư mục của phim, lưu link Bilibili +
    tên phim gốc + tên phim tiếng Việt. Ghi ngay khi bấm TẢI BẰNG IDM nên
    dù IDM hủy / lỗi thì file vẫn còn. Trả về đường dẫn file đã ghi."""
    os.makedirs(folder, exist_ok=True)
    duong_file = os.path.join(folder, ten_viet + ".txt")
    noi_dung = (
        "Tên phim (tiếng Việt): %s\n"
        "Tên phim (gốc): %s\n"
        "Link Bilibili: %s\n"
        "Chất lượng: %s\n"
    ) % (ten_viet, ten_goc, url.strip(), chat_luong or "")
    with open(duong_file, "w", encoding="utf-8") as f:
        f.write(noi_dung)
    return duong_file


def tao_thu_muc_duy_nhat(outdir, ten):
    """(v6.6) Tạo thư mục <outdir>/<ten>, trùng tên phim.
    Nếu thư mục đã có rồi thì không ghi đè: tạo thêm thư mục mới tên
    "<ten> - YYYY-MM-DD HH-MM-SS" (ngày-giờ, không dùng ":" vì Windows
    cấm). Tên đã qua sanitize_ten nên không còn ký tự cấm, tối đa 100
    ký tự. Nếu vẫn trùng (cùng giây) thì thêm (1), (2)..."""
    ten = sanitize_ten(ten)
    folder = os.path.join(outdir, ten)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        return folder
    stamp = time.strftime("%Y-%m-%d %H-%M-%S")
    # Chừa chỗ cho " - <stamp>" (22 ký tự) để tên không vượt 100 ký tự.
    ten_goc = ten[:75].strip().strip(".")
    ten_moi = sanitize_ten("%s - %s" % (ten_goc, stamp))
    folder = os.path.join(outdir, ten_moi)
    n = 1
    while os.path.exists(folder):
        ten_moi = sanitize_ten("%s - %s (%d)" % (ten_goc, stamp, n))
        folder = os.path.join(outdir, ten_moi)
        n += 1
    os.makedirs(folder, exist_ok=True)
    return folder


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


def tai_va_gop(url, option, cookies, outdir, log, tien_trinh,
               dich_ten=True, tu_gop=True):
    """Tải video+audio theo lựa chọn chất lượng rồi gộp thành 1 mp4 trong
    <outdir>/<tên video>/<tên video>.mp4. Trả về (đường dẫn file, thư mục).
    (v7.3) dich_ten=False: ten thu muc / ten file giu nguyen ten goc,
    khong dich. tu_gop=False (o "Tải yt-dlp xong tự gộp luôn" dang
    TAT): chi tai video + audio rieng (ten_hinh / ten_tieng), KHONG
    gop, tra ve (None, folder) de UI nhan dien 2 file vao muc 2."""
    url = chuan_hoa_link_bilibili(url)
    ytdlp = tim_ytdlp()
    ffmpeg = tim_ffmpeg()
    if not ytdlp:
        raise RuntimeError("Chưa tìm thấy yt-dlp trên máy.")
    if not ffmpeg:
        raise RuntimeError("Chưa tìm thấy ffmpeg (cần để gộp hình + tiếng).")
    info = kiem_tra_link(url, cookies)
    # (v6.5) Thư mục trùng tên phim đã dịch sang tiếng Việt.
    # (v6.6) Trùng tên thì tạo thêm thư mục tên + ngày-giờ, tránh ghi đè.
    ten = ten_phim_tieng_viet(info["title"], dich=dich_ten)
    folder = tao_thu_muc_duy_nhat(outdir, ten)
    try:
        luu_file_thong_tin_phim(folder, info["title"], ten, url,
                                option.get("label") or "")
    except Exception:
        pass
    if not tu_gop:
        # (v7.3) Chi tai rieng, khong gop: video + audio thanh 2 file
        # rieng ten_hinh / ten_tieng trong cung thu muc du an.
        log("Chỉ tải riêng video + audio (ô tự gộp yt-dlp đang TẮT), "
            "không gộp.")
        for format_id, hau_to in ((option["video_id"], "_hinh"),
                                  (option.get("audio_id"), "_tieng")):
            if not format_id:
                continue
            out_tmpl = os.path.join(folder, ten + hau_to + ".%(ext)s")
            cmd = [ytdlp, "--no-playlist", "-f", format_id,
                   "-o", out_tmpl]
            if cookies and os.path.isfile(cookies):
                cmd += ["--cookies", cookies]
            cmd.append(url)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True,
                                    errors="replace", bufsize=1,
                                    **chay_ngam_kwargs())
            pct_re_rieng = re.compile(r"(\d+(?:\.\d+)?%)")
            for line in proc.stdout:
                if pct_re_rieng.search(line) and "download" in line.lower():
                    tien_trinh(line.strip()[:140])
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(
                    "Tải thất bại (mã %d). Thử lại hoặc kiểm tra link."
                    % proc.returncode)
        return None, folder
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


def tai_bang_idm(url, option, cookies, outdir, log, dich_ten=True):
    """Lấy link hình + tiếng rồi đẩy cả 2 sang IDM tải nhanh nhiều luồng.
    Trả về (thư mục chứa file, tên file hình, tên file tiếng,
    tổng dung lượng ước tính để theo dõi %).
    IDM tải xong thì dùng mục Gộp để gộp lại.
    (v7.3) dich_ten=False: ten thu muc / ten file giu nguyen ten goc,
    khong dich. (v7.6) File tieng dat ten _tieng.mp4 (khong con
    _tieng.m4a): stream tieng thuc chat la container mp4, server
    tra MIME video/mp4 nen IDM het hoi doi ten; nhan dien cap
    phan biet bang ffprobe nen 2 file .mp4 khong lan nhau."""
    url = chuan_hoa_link_bilibili(url)
    info = kiem_tra_link(url, cookies)
    # (v6.5) Thư mục trùng tên phim đã dịch sang tiếng Việt.
    # (v6.6) Trùng tên thì tạo thêm thư mục tên + ngày-giờ, tránh ghi đè.
    ten = ten_phim_tieng_viet(info["title"], dich=dich_ten)
    folder = tao_thu_muc_duy_nhat(outdir, ten)
    # (v6.5) Tạo file text lưu link + tên phim ngay khi bấm TẢI BẰNG IDM,
    # trước khi đẩy sang IDM, nên dù IDM hủy / lỗi thì file vẫn còn.
    try:
        duong_txt = luu_file_thong_tin_phim(
            folder, info["title"], ten, url, option.get("label") or "")
        log("Đã lưu thông tin phim vào: " + duong_txt)
    except Exception as e:
        log("Không ghi được file thông tin phim: %s" % e)
    cookie_str = (doc_cookies_txt(cookies)
                  if cookies and os.path.isfile(cookies) else "")
    referer = url.strip()
    log("Đang lấy link %s (%s) để đẩy sang IDM..."
        % (info["title"], option["label"]))
    link_video = lay_link_stream(url, option["video_id"], cookies)
    link_audio = (lay_link_stream(url, option["audio_id"], cookies)
                  if option.get("audio_id") else None)
    ten_video = ten + "_hinh.mp4"
    ten_audio = ten + "_tieng.mp4"
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


# ======================================================================
# v7.2 - XU LY TIENG GOC KHI LONG TIENG VIET (BAN CUOI)
# Dinh chinh 19/11: gioi han 15 phut la cua CapCut (CapCut chi tach
# giong cho video < 15 phut), KHONG phai quy tac cua ChipChipStudio.
# Code nay KHONG co bat ky cua thoi luong nao: thoi luong chi duoc
# doc de ghi log, khong dung de chan.
# - "Bo loi" (CapCut) = bo giong noi, giu nhac nen, de long tieng Viet.
# - CYAN lenh 19/11 04:38: BO QUA HAN tach giong bang AI (khong lam
#   tach giong kho bang AI trong ChipChipStudio nua). Chi giu phan de:
# - Phuong an mac dinh: giam tieng goc xuong 15% (ffmpeg volume=0.15)
#   roi gop chung voi giong Viet (amix).
# - Tu giam tieng nen khi co loi (mac dinh BAT): neu da co file MP3
#   giong Viet HoaiMy trong cung thu muc du an thi tron 2 track bang
#   FFmpeg sidechaincompress - nhac nen tu nho xuong khi co loi, to
#   lai khi het loi. Chua co giong thi chi giam co dinh 15%.
# - Khong gioi han thoi luong. Chi dung FFmpeg, khong dung AI.
# - Moi file ra deu cung thu muc du an, file goc khong bi ghi de.
# ======================================================================
AM_LUONG_TIENG_GOC_KHI_LONG_TIENG = 0.15  # 15% - muc CYAN chot
# Ghi chu: con so 15 phut cua CapCut KHONG dung o day, chi ghi lai de
# giai thich tai sao khong dung CapCut cho phim dai.
GIOI_HAN_CAPCUT_PHUT = 15  # chi la ghi chu, KHONG dung lam cua chan
# (v7.2) Thong so sidechaincompress cho tu giam tieng nen khi co loi:
# threshold=0.03: giong Viet noi to hon muc nay thi bat dau nen nhac
# xuong (giong doc thuong to, nhac nen da giam 15% nen nguong nay
# vua du de khong bi kich nham boi nhac nen). ratio=8: khi co loi,
# nhac nen bi nen xuong manh (kha nang nghe thay ro). attack=200ms:
# giam xuong trong 200ms (khong giat cuc, khong cat mat dau cau).
# release=1000ms: het loi 1 giay moi to lai tu tu (khong giat len
# xuong lien tuc giua cac khoang ngat cau). makeup=1: khong tang
# bu am luong nhac nen sau khi nen.
SIDECHAIN_THRESHOLD = 0.03
SIDECHAIN_RATIO = 8
SIDECHAIN_ATTACK_MS = 200
SIDECHAIN_RELEASE_MS = 1000


def quyet_dinh_xu_ly_tieng_goc(tu_giam_tieng_nen=True,
                              co_giong_viet=False, giam_15=True):
    """(v7.2, sua v7.3) Quyet dinh xu ly tieng goc. Tra ve (che_do, ly_do).
    Chi con 3 duong, KHONG co tach giong AI, KHONG co cua thoi luong:
    - "sidechain": da co file giong Viet + cong tac tu giam dang BAT
      -> tron bang FFmpeg sidechaincompress. Am luong nen tuy o giam
      15%: BAT thi nen giam con 15% roi sidechain, TAT thi nen giu
      nguyen am luong roi sidechain.
    - "giam_15": chua co giong Viet, hoac cong tac dang TAT, va o
      giam 15% dang BAT -> chi giam co dinh tieng goc xuong 15%
      truoc khi gop.
    - "goc": o giam 15% dang TAT (va khong du dieu kien sidechain)
      -> giu nguyen am luong goc, khong giam, khong sidechain."""
    if tu_giam_tieng_nen and co_giong_viet:
        if giam_15:
            return ("sidechain",
                    "Da co file giong Viet HoaiMy + cong tac tu giam "
                    "dang BAT - tron bang FFmpeg sidechaincompress: "
                    "nhac nen (da giam con 15%) tu nho xuong khi co "
                    "loi, to lai khi het loi.")
        return ("sidechain",
                "Da co file giong Viet HoaiMy + cong tac tu giam dang "
                "BAT - tron bang FFmpeg sidechaincompress, nhac nen "
                "GIU NGUYEN am luong (o giam 15% dang TAT).")
    if giam_15:
        if tu_giam_tieng_nen and not co_giong_viet:
            return ("giam_15",
                    "Cong tac tu giam dang BAT nhung chua co file "
                    "giong Viet trong thu muc du an nen chi giam co "
                    "dinh tieng goc xuong 15% truoc khi gop.")
        return ("giam_15",
                "Cong tac tu giam dang TAT - chi giam co dinh tieng "
                "goc xuong 15% truoc khi gop voi giong Viet.")
    return ("goc",
            "O 'Giam tieng goc xuong 15%' dang TAT - giu nguyen am "
            "luong tieng goc, khong giam, khong sidechain.")


def lenh_giam_am_luong_15(ffmpeg, video, audio_goc, out_path):
    """(v7.1) Lenh ffmpeg giam tieng goc xuong 15% roi gop voi hinh.
    Video copy nguyen, audio encode lai aac. Dung khi khong co file
    long tieng Viet rieng. Tra ve list lenh (chua chay)."""
    return [ffmpeg, "-y", "-i", video, "-i", audio_goc,
            "-filter_complex",
            "[1:a]volume=0.15[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", out_path]


def lenh_gop_voi_long_tieng(ffmpeg, video, audio_goc, audio_long, out_path,
                           am_luong_goc=AM_LUONG_TIENG_GOC_KHI_LONG_TIENG,
                           tu_giam_tieng_nen=True, giam_15=True):
    """(v7.2, sua v7.3) Lenh ffmpeg gop hinh + tieng goc + giong Viet long tieng.
    - tu_giam_tieng_nen=True (mac dinh): tieng goc giam con
      am_luong_goc roi qua sidechaincompress, lay giong
      Viet lam sidechain: nhac nen tu nho xuong khi co loi, to lai
      khi het loi. Sau do amix voi giong Viet o muc day du.
    - False: chi amix don gian (tieng goc giam 15% + giong day du).
    - giam_15=False (o "Giam tieng goc xuong 15%" dang TAT): am luong
      goc giu nguyen 1.0 - khong co volume=0.15 trong lenh.
    Tra ve list lenh (chua chay). Khong gioi han thoi luong."""
    if not giam_15:
        am_luong_goc = 1.0
    if tu_giam_tieng_nen:
        fc = ("[1:a]volume=%.2f[nen];"
              "[nen][2:a]sidechaincompress=threshold=%.2f:ratio=%d:"
              "attack=%d:release=%d[nen_duc];"
              "[nen_duc][2:a]amix=inputs=2:duration=longest[aout]"
              % (am_luong_goc, SIDECHAIN_THRESHOLD, SIDECHAIN_RATIO,
                 SIDECHAIN_ATTACK_MS, SIDECHAIN_RELEASE_MS))
    else:
        fc = ("[1:a]volume=%.2f[nen];[2:a]volume=1.0[long];"
              "[nen][long]amix=inputs=2:duration=longest[aout]"
              % am_luong_goc)
    return [ffmpeg, "-y", "-i", video, "-i", audio_goc, "-i", audio_long,
            "-filter_complex", fc,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", out_path]


def tim_file_long_tieng(thu_muc, ten_viet=""):
    """(v7.2) Tim file MP3 giong Viet HoaiMy trong cung thu muc du an.
    Uu tien file co ten <ten_viet>_long-tieng.mp3 hoac bat ky file
    .mp3 nao co 'long-tieng' / 'long_tieng' trong ten. Tra ve duong
    dan hoac None neu chua co. Khong doi ten, khong di chuyen file."""
    if not thu_muc or not os.path.isdir(thu_muc):
        return None
    ung_vien = []
    for ten in sorted(os.listdir(thu_muc)):
        if not ten.lower().endswith(".mp3"):
            continue
        ten_thap = ten.lower()
        if "long-tieng" in ten_thap or "long_tieng" in ten_thap:
            duong = os.path.join(thu_muc, ten)
            if ten_viet and ten.startswith(ten_viet + "_long-tieng"):
                return duong  # khop dung ten phim -> lay ngay
            ung_vien.append(duong)
    return ung_vien[0] if ung_vien else None


def ten_file_da_tron(thu_muc, ten_viet):
    """(v7.2) Ten file tron xong, cung thu muc du an, khong trung:
    <ten_viet>_da-tron.mp4, <ten_viet>_da-tron(1).mp4..."""
    return ten_file_dau_ra(thu_muc, ten_viet + "_da-tron")


def ten_file_audio_khong_trung(thu_muc, ten_goc, ext=".mp3"):
    """(v7.3) Ten file audio khong trung: ten.mp3, ten(1).mp3..."""
    ten_goc = sanitize_ten(ten_goc)
    out = ten_goc + ext
    n = 1
    while os.path.exists(os.path.join(thu_muc, out)):
        out = "%s(%d)%s" % (ten_goc, n, ext)
        n += 1
    return out


def ten_file_nen_15(thu_muc, ten_viet):
    """(v7.3) Ten file nen 15%, cung thu muc du an, khong trung:
    <ten_viet>_nen-15.mp3, <ten_viet>_nen-15(1).mp3..."""
    return ten_file_audio_khong_trung(thu_muc, ten_viet + "_nen-15",
                                      ".mp3")


def ten_file_nen_goc(thu_muc, ten_viet):
    """(v7.3) Ten file nen GIU NGUYEN am luong goc (khi o giam 15%
    dang TAT), cung thu muc du an, khong trung:
    <ten_viet>_nen-goc.mp3, <ten_viet>_nen-goc(1).mp3..."""
    return ten_file_audio_khong_trung(thu_muc, ten_viet + "_nen-goc",
                                      ".mp3")


def lenh_xuat_nen_15(ffmpeg, audio_goc, out_path, giam_15=True):
    """(v7.3) Lenh ffmpeg xuat RIENG file nen: audio goc giam xuong 15%
    (volume=0.15), CHI XUAT AUDIO (co -vn, khong map video, khong
    gop video). Output MP3 (libmp3lame, q:a 3). Tra ve list lenh
    (chua chay).
    (v7.3) giam_15=False (o "Giam tieng goc xuong 15%" dang TAT):
    khong co -af volume trong lenh - file nen giu nguyen am luong
    goc.
    LUU Y QUAN TRONG: day KHONG phai file da bo giong that su - bo
    giong that su CYAN tu lam o CapCut (Bo loi); tool chi giam nho
    tieng goc de lam nen cho CapCut. Khong dung AI tach giong (da
    bo theo lenh CYAN 19/11 04:38)."""
    if giam_15:
        return [ffmpeg, "-y", "-i", audio_goc,
                "-vn", "-af", "volume=0.15",
                "-c:a", "libmp3lame", "-q:a", "3", out_path]
    return [ffmpeg, "-y", "-i", audio_goc,
            "-vn", "-c:a", "libmp3lame", "-q:a", "3", out_path]


def xuat_nen_15(audio_goc, out_path, ffmpeg, log_cb=None, giam_15=True):
    """(v7.3) Chay lenh xuat file nen 15% (hoac giu nguyen am luong
    neu o giam 15% dang TAT). Tra ve out_path, raise RuntimeError
    neu loi (kem stderr cuoi cua ffmpeg). KHONG gop video, KHONG
    doi file goc."""
    def _log(s):
        if log_cb:
            log_cb(s)
    if giam_15:
        _log("Dang xuat file nen (tieng goc giam con 15%%): " + out_path)
    else:
        _log("Dang xuat file nen (GIU NGUYEN am luong goc - o giam "
             "15% dang TAT): " + out_path)
    cmd = lenh_xuat_nen_15(ffmpeg, audio_goc, out_path, giam_15=giam_15)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True,
                          errors="replace", **chay_ngam_kwargs())
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip()[-600:]
        raise RuntimeError("ffmpeg bao loi khi xuat file nen (ma %d)."
                           "%s" % (proc.returncode,
                                   ("\n" + tail) if tail else ""))
    if not os.path.isfile(out_path):
        raise RuntimeError("Xuat file nen xong nhung khong thay file.")
    _log("Da xuat file nen xong: " + out_path)
    return out_path


def xuat_2_file_audio_capcut(audio_goc, thu_muc_du_an, ten_viet, ffmpeg,
                             log_cb=None, giam_15=True):
    """(v7.3) XUAT RIENG 2 file audio cho CapCut (luong long tieng
    CYAN chot 19/11 04:53), KHONG gop video:
    (1) file nen: audio goc giam xuong 15% -> <ten_viet>_nen-15.mp3
        (cung thu muc du an; KHONG phai file da bo giong that su -
        bo giong that su CYAN tu lam o CapCut). Neu o giam 15%
        dang TAT thi file nen giu nguyen am luong goc, ten
        <ten_viet>_nen-goc.mp3.
    (2) file giong Viet HoaiMy tu SRT: tim file <ten_viet>_long-tieng
        .mp3 (hoac bat ky file *long-tieng*.mp3) trong cung thu muc
        du an - file nay tab Doc phu de HoaiMy da xuat san.
    Tra ve (duong_nen, duong_giong). Raise RuntimeError "CHUA_CO_
    GIONG_VIET: ..." neu chua co file giong (UI se mo tab Doc phu
    de voi SRT cua du an de cau tao giong); raise RuntimeError neu
    thieu file goc / thieu ffmpeg / ffmpeg loi. Khong doi file goc,
    khong gop video, khong dung AI tach giong."""
    def _log(s):
        if log_cb:
            log_cb(s)
    if not ffmpeg or not os.path.isfile(ffmpeg):
        raise RuntimeError("Chua tim thay ffmpeg (can de xuat file nen).")
    if not audio_goc or not os.path.isfile(audio_goc):
        raise RuntimeError("Khong tim thay file Audio (tieng) goc.")
    if not thu_muc_du_an or not os.path.isdir(thu_muc_du_an):
        raise RuntimeError("Khong tim thay thu muc du an.")
    dub = tim_file_long_tieng(thu_muc_du_an, ten_viet)
    if not dub:
        raise RuntimeError(
            "CHUA_CO_GIONG_VIET: chua co file giong Viet HoaiMy "
            "(*long-tieng.mp3) trong thu muc du an. Mo tab Doc phu de "
            "de tao giong tu SRT roi xuat lai.")
    _log("File giong Viet da co trong thu muc du an: " + dub)
    if giam_15:
        ten_nen = ten_file_nen_15(thu_muc_du_an, ten_viet)
    else:
        ten_nen = ten_file_nen_goc(thu_muc_du_an, ten_viet)
    nen_path = os.path.join(thu_muc_du_an, ten_nen)
    xuat_nen_15(audio_goc, nen_path, ffmpeg, log_cb=log_cb,
                giam_15=giam_15)
    _log("Da xuat xong 2 file audio rieng (cho CapCut):\n- Nen: "
         + nen_path + "\n- Giong Viet: " + dub)
    return (nen_path, dub)


def gop_voi_long_tieng(video, audio_goc, audio_long, out_path, ffmpeg,
                      tien_trinh_cb, tu_giam_tieng_nen=True, log_cb=None,
                      giam_15=True):
    """(v7.2, sua v7.3) Gop hinh + tieng goc (da xu ly) + giong Viet long tieng.
    - Doc thoi luong bang ffprobe CHI DE GHI LOG, khong dung de chan.
    - Neu cong tac tu giam BAT va co file giong Viet: sidechaincompress
      (nhac nen tu nho xuong khi co loi, to lai khi het loi).
    - Con lai: tieng goc giam xuong 15% (volume=0.15) roi amix voi
      giong Viet - TRU KHI o giam 15% dang TAT thi giu nguyen am
      luong goc ("goc"). KHONG co tach giong AI. Tra ve out_path,
      raise RuntimeError neu loi (ke ca stderr cuoi cua ffmpeg)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    ffprobe = tim_ffprobe(ffmpeg)
    tong_giay = lay_thoi_luong(ffprobe, video) if ffprobe else None
    if tong_giay is not None:
        _log("Thoi luong video: %.0f giay (chi de ghi log, KHONG gioi "
             "han 15 phut cua CapCut)." % tong_giay)
    else:
        _log("Khong do duoc thoi luong video - van xu ly binh thuong "
             "(khong gioi han 15 phut).")
    co_giong = bool(audio_long) and os.path.isfile(audio_long)
    che_do, ly_do = quyet_dinh_xu_ly_tieng_goc(tu_giam_tieng_nen, co_giong,
                                              giam_15)
    _log("Xu ly tieng goc: " + ly_do)
    if not co_giong:
        raise RuntimeError("Khong tim thay file giong Viet (MP3 long "
                           "tieng) de gop cung.")
    cmd = lenh_gop_voi_long_tieng(ffmpeg, video, audio_goc, audio_long,
                                  out_path,
                                  tu_giam_tieng_nen=(che_do == "sidechain"),
                                  giam_15=giam_15)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True,
                            errors="replace", bufsize=1,
                            **chay_ngam_kwargs())
    out_ms_re = re.compile(r"out_time_ms=(\d+)")
    loi_tail = []
    for line in proc.stdout:
        loi_tail.append(line)
        if len(loi_tail) > 20:
            loi_tail.pop(0)
        m2 = out_ms_re.search(line)
        if m2 and tong_giay:
            try:
                pct = int(int(m2.group(1)) / (tong_giay * 1000.0) * 100)
                tien_trinh_cb(max(0, min(100, pct)))
            except Exception:
                pass
    proc.wait()
    if proc.returncode != 0:
        tail = "".join(loi_tail).strip()[-600:]
        raise RuntimeError("ffmpeg bao loi khi tron long tieng (ma %d)."
                           "%s" % (proc.returncode,
                                   ("\n" + tail) if tail else ""))
    if not os.path.isfile(out_path):
        raise RuntimeError("Tron long tieng xong nhung khong thay file.")
    tien_trinh_cb(100)
    if che_do == "sidechain":
        _log("Da tron xong (sidechain): nhac nen tu giam khi co loi. "
             "File: " + out_path)
    elif che_do == "goc":
        _log("Da tron xong (giu nguyen am luong goc - o giam 15% dang "
             "TAT). File: " + out_path)
    else:
        _log("Da tron xong (giam tieng goc co dinh 15%%). File: "
             + out_path)
    return out_path


# ======================================================================
# PHAN SRT READER v1.4 GOP VAO (ChipChipStudio v7.0)
# Nguon: SRT-Reader-HoaiMy.py v1.4 (SRT Reader v1.4, gop vao ChipChipStudio).
# Giu NGUYEN toan bo ham/lop doc SRT + Edge TTS + atempo + tien-trinh
# (xem audit cuoi file gop / bao cao ban giao). Chi co 2 ngoai le:
#  (1) Cac ham trung ten voi Chipchipdownload (app_dir, config_path,
#      doc_config, luu_config, tim_ffmpeg, tim_ffprobe, ...) KHONG
#      lay ban SRT ma dung 1 ban gop duy nhat o phan Chipchip ben
#      tren (doc_config/luu_config gop ca 2 bo khoa; tim_ffmpeg gop
#      ca 2 danh sach duong dan; mac_dinh_thu_muc_luu cua SRT doi
#      ten thanh mac_dinh_thu_muc_luu_srt).
#  (2) Luong cap nhat RIENG cua SRT Reader (kiem_tra_cap_nhat,
#      tai_ban_moi_va_cap_nhat, ten exe rieng, repo rieng cua SRT Reader) DA
#      BO HAN: ChipChipStudio chi dung DUY NHAT luong cap nhat cua
#      ChipChip (QuanLy.bam_kiem_tra_cap_nhat, Release latest, asset
#      Chipchipdownload.exe, capnhat.bat). SRT Reader von la portable,
#      khi gop vao thi thanh tool setup cai 1 lan, va chi cap nhat
#      trong tool, khong cai lai.
# ======================================================================

GIONG_MAY = "Giọng máy (cũ)"  # giong SAPI tieng Viet co san tren may Windows


GIONG = {
    "HoaiMy (nữ)": "vi-VN-HoaiMyNeural",
    "NamMinh (nam)": "vi-VN-NamMinhNeural",
    GIONG_MAY: "may",
}


GIONG_MAC_DINH = "HoaiMy (nữ)"


MAU_DOC_THU = "Xin chào, đây là giọng đọc thử."


DO_DAI_TOI_DA_MOT_LAN = 500  # ky tu; cau dai hon se tach nho
# (v7.7) Gioi han thoi gian cho 1 lan goi Edge TTS (moi doan). Het
# gio thi failover sang luot sau thay vi treo vo han (asyncio.run
# khong timeout o v7.5: mang cham/treo thi luong worker dung mai o
# cau do, trang thai khong doi, nut Huy cung khong dung duoc).
THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY = 120


_TS_RE = re.compile(
    r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)"
)


_TAG_RE = re.compile(r"<[^>]+>")


def _ts_sang_ms(h, m, s, ms):
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)


def _dinh_dang_ms(ms):
    """ms -> chuoi 'HH:MM:SS,mmm' de hien trong danh sach cau."""
    ms = int(ms)
    s, mmm = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, mmm)


def _duong_dan_dai_win(path):
    """(v7.7) Tra ve duong dan dung duoc tren Windows khi duong dan
    DAI (gan/vuot gioi han 260 ky tu cua Windows - thu muc phim +
    ten file SRT cua CYAN rat dai): them tien to \\\\?\\ vao duong
    dan tuyet doi. CHI dung cho cac thao tac file cua Python
    (open/makedirs/stat/isfile); KHONG dung cho doi so dong lenh
    ffmpeg/ffprobe (ffmpeg co the khong hieu tien to nay). Ngoai
    Windows, hoac duong dan ngan, tra nguyen path."""
    if not path or sys.platform != "win32":
        return path
    try:
        p = os.path.abspath(str(path))
    except Exception:
        return path
    if p.startswith("\\\\?\\") or p.startswith("\\\\"):
        return p
    if len(p) > 240:
        return "\\\\?\\" + p
    return path


def doc_srt(duong_dan):
    """Tra ve list dict: {chi_so, bat_dau_ms, ket_thuc_ms, text}."""
    with open(_duong_dan_dai_win(duong_dan), "r",
              encoding="utf-8-sig", errors="replace") as f:
        noi_dung = f.read()
    noi_dung = noi_dung.replace("\r\n", "\n").replace("\r", "\n")
    khoi = [k.strip("\n") for k in re.split(r"\n\s*\n", noi_dung) if k.strip()]
    ket_qua = []
    chi_so_tu_dong = 0
    for k in khoi:
        dong = [d for d in k.split("\n") if d.strip() != ""]
        if not dong:
            continue
        i_ts = None
        chi_so = None
        for i, d in enumerate(dong):
            if _TS_RE.search(d):
                i_ts = i
                break
        if i_ts is None:
            continue
        m = _TS_RE.search(dong[i_ts])
        bat_dau = _ts_sang_ms(m.group(1), m.group(2), m.group(3), m.group(4))
        ket_thuc = _ts_sang_ms(m.group(5), m.group(6), m.group(7), m.group(8))
        if i_ts == 1:
            try:
                chi_so = int(dong[0].strip())
            except ValueError:
                chi_so = None
        if chi_so is None:
            chi_so_tu_dong += 1
            chi_so = chi_so_tu_dong
        else:
            chi_so_tu_dong = max(chi_so_tu_dong, chi_so)
        text = " ".join(dong[i_ts + 1:])
        text = _TAG_RE.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        ket_qua.append({
            "chi_so": chi_so,
            "bat_dau_ms": bat_dau,
            "ket_thuc_ms": ket_thuc,
            "text": text,
        })
    ket_qua.sort(key=lambda x: x["bat_dau_ms"])
    return ket_qua


def tach_cau_dai(text, gioi_han=DO_DAI_TOI_DA_MOT_LAN):
    """Tach cau dai thanh nhieu doan ngan de Edge TTS doc on dinh."""
    if len(text) <= gioi_han:
        return [text]
    doan = []
    tam = ""
    for cau in re.split(r"(?<=[.!?;:,])\s+", text):
        if len(tam) + len(cau) + 1 <= gioi_han:
            tam = (tam + " " + cau).strip()
        else:
            if tam:
                doan.append(tam)
            if len(cau) > gioi_han:
                # cat cung theo khoang trang
                while len(cau) > gioi_han:
                    cat = cau.rfind(" ", 0, gioi_han)
                    cat = cat if cat > 0 else gioi_han
                    doan.append(cau[:cat].strip())
                    cau = cau[cat:].strip()
                if cau:
                    tam = cau
                else:
                    tam = ""
            else:
                tam = cau
    if tam:
        doan.append(tam)
    return [d for d in doan if d]


def _tom_tat_loi(e, gioi_han=160):
    """Lay dong dau tien cua loi, cat ngan de hien len giao dien (v1.3:
    KHONG hien toan bo log tho ffmpeg dai, nhay lien tuc - log ffmpeg
    day du chi ghi vao file, xem _ghi_log_loi_ffmpeg)."""
    s = str(e).replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > gioi_han:
        s = s[:gioi_han].rstrip() + "..."
    return s or type(e).__name__


def _ghi_log_loi_ffmpeg(thu_muc, noi_dung):
    """Ghi log loi ffmpeg DAY DU vao file ffmpeg-loi.log trong thu muc ket
    qua (de chan doan sau), thay vi hien toan bo len man hinh (v1.3)."""
    try:
        os.makedirs(_duong_dan_dai_win(thu_muc), exist_ok=True)
        with open(_duong_dan_dai_win(
                os.path.join(thu_muc, "ffmpeg-loi.log")), "a",
                  encoding="utf-8") as f:
            f.write("\n--- %s ---\n%s\n"
                    % (time.strftime("%Y-%m-%d %H:%M:%S"), noi_dung))
    except Exception:
        pass


def kiem_chung_pe(path):
    """Kiem tra nhanh file vua tai co phai exe Windows that khong
    (header MZ + chu ky PE), de khong va phai trang loi HTML doi lot file.
    Tra ve True neu dung dinh dang PE."""
    try:
        with open(path, "rb") as f:
            dau = f.read(64)
        if len(dau) < 64 or dau[:2] != b"MZ":
            return False
        e_lfanew = int.from_bytes(dau[60:64], "little")
        with open(path, "rb") as f:
            f.seek(e_lfanew)
            return f.read(4) == b"PE\x00\x00"
    except Exception:
        return False


def _dinh_dang_toc_do(he_so):
    """Hien thi toc do dang he so nhan (giong trang web test): '1.00x',
    '1.35x', '0.50x'."""
    return "%.2fx" % float(he_so)


def _toc_do_sang_phan_tram(he_so):
    """Doi he so nhan (1.35x) sang phan tram cho edge-tts/SAPI (+35)."""
    return int(round((float(he_so) - 1.0) * 100))


def _toc_do_sang_edge(he_so):
    """Doi he so nhan sang chuoi rate edge-tts nhan ('+35%').
    Edge-tts nhan rate dang '+35%' cho toc do 1.35x."""
    return "%+d%%" % _toc_do_sang_phan_tram(he_so)


def _chuyen_toc_do_cu(gia_tri):
    """Chuyen toc do tu config cu (v1.0-1.2 luu dang phan tram so nguyen,
    vd 9 = +9%) sang he so nhan v1.3 (1.09x). Config moi da luu so thuc
    (vd 1.35) thi giu nguyen."""
    if isinstance(gia_tri, bool):
        return 1.0
    if isinstance(gia_tri, int):
        # So nguyen -50..50: phan tram cu -> he so nhan.
        if -50 <= gia_tri <= 50:
            return round(1.0 + gia_tri / 100.0, 2)
        return 1.0
    try:
        he_so = float(gia_tri)
    except (TypeError, ValueError):
        return 1.0
    return max(0.5, min(2.0, he_so))


def _dinh_dang_cao_do(hz):
    return ("+" if hz >= 0 else "") + str(int(hz)) + "Hz"


def _tao_connector(bo_xac_minh):
    if not bo_xac_minh:
        return None
    import aiohttp
    ctx = ssl._create_unverified_context()
    return aiohttp.TCPConnector(ssl=ctx)


EDGE_ALT_WSS_URL = ("wss://api.msedgeservices.com/tts/cognitiveservices/"
                    "websocket/v1?Ocp-Apim-Subscription-Key={token}")


_dung_may_chu_phu = False  # da chuyen sang may chu phu trong phien nay


_khoa_may_chu = threading.Lock()


def _lay_proxy_he_thong():
    """Proxy he thong neu co (bien moi truong https_proxy/HTTPS_PROXY).
    May nha thuong khong co proxy -> tra None (khong doi hanh vi)."""
    return (os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
            or os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"))


def _ten_may_chu(url):
    try:
        return url.split("/")[2]
    except Exception:
        return url


def _chuyen_sang_may_chu_phu(log_cb=None):
    """Doi edge-tts sang may chu phu api.msedgeservices.com cho den het
    phien (giong FluentVoice Pro 1.6.3). Tra ve True neu vua chuyen,
    False neu da o may chu phu roi."""
    global _dung_may_chu_phu
    import edge_tts.communicate as comm
    from edge_tts.constants import TRUSTED_CLIENT_TOKEN
    with _khoa_may_chu:
        if _dung_may_chu_phu:
            return False
        comm.WSS_URL = EDGE_ALT_WSS_URL.format(token=TRUSTED_CLIENT_TOKEN)
        _dung_may_chu_phu = True
    if log_cb:
        log_cb("  -> May chu giong goc tu choi ket noi, chuyen sang may chu "
               "phu api.msedgeservices.com...")
    return True


def _mo_ta_loi_giong(e, timeout_giay=None):
    """Phan loai loi doc giong de log ro rang.
    Tra ve (ma, giai_thich). Ma: '403' | '429' | 'khong-co-audio' |
    'ssl' | 'mang' | 'khac'. (v7.7) `timeout_giay`: so giay timeout
    thuc te cua luot goi (de bao dung so, khong lay nham hang so
    mac dinh 120s khi test/goi voi timeout khac)."""
    ten = type(e).__name__
    s = str(e)
    status = getattr(e, "status", None)
    if status == 403 or " 403" in s or s.startswith("403"):
        return ("403", "Microsoft tu choi ket noi (HTTP 403) - may chu "
                       "giong goc siet ket noi tu tool ngoai trinh duyet")
    if status == 429 or " 429" in s or s.startswith("429"):
        return ("429", "bi gioi han toc do (HTTP 429) - Microsoft chan tam, "
                       "doi vai giay roi thu lai")
    if ten == "NoAudioReceived" or "No audio was received" in s:
        return ("khong-co-audio", "may chu chap nhan ket noi nhung ngat "
                                   "khong tra audio (Microsoft tu choi ngam)")
    if la_loi_chung_chi_ssl(e):
        return ("ssl", "loi chung chi SSL - proxy/phan mem diet virus chan "
                       "chung chi")
    # (v7.7) Timeout cua asyncio.wait_for: str(e) rong nen phai bat
    # theo kieu exception, khong chi theo chuoi.
    if isinstance(e, TimeoutError) or ten in ("TimeoutError",):
        so_giay = timeout_giay if timeout_giay else \
            THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY
        return ("mang", "hết thời gian chờ %ds - mạng chậm hoặc máy chủ "
                         "giọng không phản hồi, sẽ thử lượt sau"
                % so_giay)
    if "timeout" in s.lower() or "timed out" in s.lower():
        return ("mang", "het thoi gian cho - mang cham hoac may chu tre")
    return ("khac", "%s: %s" % (ten, s))


async def _doc_mot_doan(text, voice, toc_do, cao_do, duong_dan_ra,
                        bo_xac_minh, proxy=None,
                        timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY):
    # (v7.7) edge-tts import luoi o day: ban exe thieu edge_tts thi
    # ImportError nay duoc bat o _doc_mot_doan_co_failover (co log ro),
    # khong chet im nhu loi pydub o _chay v7.5.
    import edge_tts
    import edge_tts.communicate as _comm
    # edge-tts truyen thang ssl=_SSL_CTX (certifi) vao ws_connect, ghi de
    # context cua connector -> muon bo xac minh that thi phai doi ca
    # _SSL_CTX cua edge-tts (neu khong, fallback bo xac minh o v1.1 chi
    # la hinh thuc, WSS van xac minh nhu thuong).
    try:
        if bo_xac_minh:
            _comm._SSL_CTX = ssl._create_unverified_context()
        else:
            import certifi
            _comm._SSL_CTX = ssl.create_default_context(
                cafile=certifi.where())
    except Exception:
        pass
    comm = edge_tts.Communicate(
        text, voice,
        # v1.3: toc_do la he so nhan tren giao dien (1.35x) - doi sang
        # dang '+35%' truoc khi dua cho edge-tts.
        rate=_toc_do_sang_edge(toc_do),
        pitch=_dinh_dang_cao_do(cao_do),
        connector=_tao_connector(bo_xac_minh),
        proxy=proxy,
    )
    # (v7.7) Gioi han thoi gian cho: het gio thi huy luot goi nay
    # (asyncio.TimeoutError) de failover sang luot sau, khong treo
    # vo han khi mang cham/may chu giong treo.
    await asyncio.wait_for(comm.save(duong_dan_ra),
                           timeout=max(10, float(timeout_giay)))


def _doc_mot_doan_co_failover(text, voice, toc_do, cao_do, duong_dan_ra,
                              log_cb=None,
                              timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                              dung=None):
    """Doc 1 doan ngan thanh file MP3, co failover may chu giong.
    Thu tu: may chu goc (SSL xac minh -> bo xac minh) roi may chu phu
    api.msedgeservices.com (SSL xac minh -> bo xac minh). Gap 429 thi
    doi 3 giay truoc khi thu lai. Tra ve (thanh_cong, da_dung_bo_xac_minh,
    thong_bao_loi). (v7.7) Moi luot goi co timeout rieng; `dung`
    (threading.Event, tuy chon) de nut Huy dung duoc ngay ca khi dang
    cho giong, khong phai doi het 4 luot."""
    import time
    proxy = _lay_proxy_he_thong()
    if proxy and log_cb:
        log_cb("  (phat hien proxy he thong, dung proxy de goi giong)")
    if _dung_may_chu_phu:
        cac_luot = [("phu", False), ("phu", True)]
    else:
        cac_luot = [("goc", False), ("goc", True),
                    ("phu", False), ("phu", True)]
    loi_cuoi = ""
    for i, (may_chu, bo_xac_minh) in enumerate(cac_luot, 1):
        if dung is not None and dung.is_set():
            return False, False, "đã hủy"
        if may_chu == "phu":
            _chuyen_sang_may_chu_phu(log_cb)
            if i == 3:
                time.sleep(2)  # tranh 429 khi vua doi may chu
        ten_may = ("may chu goc" if may_chu == "goc"
                   else "may chu phu")
        try:
            # (v7.7) Xoa file dich cua luot truoc (neu co): luot truoc
            # timeout/loi giua chung co the de lai file MP3 doan, neu
            # khong xoa thi buoc kiem tra "file > 0 byte" ben duoi se
            # nhan nham file doan do la thanh cong.
            _xoa_file_quiet(duong_dan_ra)
            asyncio.run(_doc_mot_doan(text, voice, toc_do, cao_do,
                                      duong_dan_ra, bo_xac_minh, proxy,
                                      timeout_giay=timeout_giay))
            if os.path.isfile(duong_dan_ra) and os.path.getsize(duong_dan_ra) > 0:
                if log_cb and may_chu == "phu":
                    log_cb("  OK qua may chu phu api.msedgeservices.com")
                return True, bo_xac_minh, ""
            raise RuntimeError("file am thanh rong (0 byte)")
        except ImportError as e:
            # (v7.7) Thieu thu vien trong ban exe: bao ro TEN thu
            # vien thieu ngay, khong thu 4 luot vo ich. (edge_tts
            # hay aiohttp deu la hidden import khi build exe.)
            ten_thieu = str(e)
            if "edge_tts" in ten_thieu:
                loi = ("thiếu thư viện edge-tts trong bản exe "
                       "(lỗi build: thiếu hidden import edge_tts) - %s"
                       % e)
            elif "aiohttp" in ten_thieu:
                loi = ("thiếu thư viện aiohttp trong bản exe "
                       "(lỗi build: thiếu hidden import aiohttp) - %s"
                       % e)
            else:
                loi = "thiếu thư viện trong bản exe: %s" % e
            if log_cb:
                log_cb("  LỖI: %s" % loi)
            return False, False, loi
        except Exception as e:
            ma, giai_thich = _mo_ta_loi_giong(e,
                                              timeout_giay=timeout_giay)
            loi_cuoi = "%s [%s]" % (giai_thich, ma)
            if log_cb:
                log_cb("  Thu lan %d/%d (%s, %s) loi [%s]: %s"
                       % (i, len(cac_luot), ten_may,
                          "bo xac minh SSL" if bo_xac_minh else "SSL xac minh",
                          ma, giai_thich))
            if ma == "429":
                time.sleep(3)
            continue
    return False, False, loi_cuoi


def doc_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra, log_cb=None,
                  ffmpeg=None,
                  timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                  dung=None):
    """Doc 1 cau thanh file MP3 (co failover may chu giong, xem
    _doc_mot_doan_co_failover). toc_do la HE SO NHAN (v1.3: 1.0x mac
    dinh, 0.5x-2.0x) - doi sang dang '+35%' trong _doc_mot_doan truoc
    khi dua cho edge-tts. Tra ve (thanh_cong, da_dung_bo_xac_minh,
    thong_bao_loi). v1.3: doc loi thi XOA file dich (neu co) de khong de
    lai file MP3 hong (0 byte / doan giua chung) lam hong buoc gop sau.
    (v7.7) Cau dai: doc tung doan roi noi lai bang ffmpeg concat
    demuxer (_gop_mp3_concat), KHONG dung pydub nua (pydub la
    nguyen nhan nghi ngo gay chet im luong _chay o v7.5 vi ban exe
    thieu thu vien nay)."""
    doan_list = tach_cau_dai(text)
    if len(doan_list) == 1:
        ok, bo_xac_minh, loi = _doc_mot_doan_co_failover(
            text, voice, toc_do, cao_do, duong_dan_ra, log_cb,
            timeout_giay=timeout_giay, dung=dung)
        if not ok:
            _xoa_file_quiet(duong_dan_ra)
        return ok, bo_xac_minh, loi
    # Cau dai: doc tung doan roi noi lai bang ffmpeg concat.
    if not ffmpeg:
        return False, False, ("câu dài cần ffmpeg để nối các đoạn "
                              "(đặt ffmpeg.exe cạnh tool hoặc thêm vào "
                              "PATH)")
    import tempfile
    tam_files = []
    try:
        for j, doan in enumerate(doan_list):
            if dung is not None and dung.is_set():
                _xoa_file_quiet(duong_dan_ra)
                return False, False, "đã hủy"
            with tempfile.NamedTemporaryFile(suffix=".mp3",
                                            delete=False) as tmp:
                tam_path = tmp.name
            tam_files.append(tam_path)
            ok, _, loi = doc_thanh_mp3(doan, voice, toc_do, cao_do,
                                       tam_path, log_cb, ffmpeg=ffmpeg,
                                       timeout_giay=timeout_giay, dung=dung)
            if not ok:
                _xoa_file_quiet(duong_dan_ra)
                return False, False, "doan %d loi: %s" % (j + 1, loi)
        ok_gop, loi_gop = _gop_mp3_concat(
            [(p, None) for p in tam_files], duong_dan_ra, ffmpeg,
            log_cb=log_cb, dung=dung, timeout_giay=180,
            log_loi_dir=os.path.dirname(duong_dan_ra) or ".")
        if not ok_gop:
            _xoa_file_quiet(duong_dan_ra)
            return False, False, "nối các đoạn lỗi: %s" % loi_gop
        return True, False, ""
    finally:
        for p in tam_files:
            _xoa_file_quiet(p)


def _ps_quote(s):
    """Nhung chuoi vao chuoi don PowerShell (nhan doi dau ')."""
    return "'" + str(s).replace("'", "''") + "'"


def _ps_giong_may(text, toc_do, cao_do, wav_path, dung_ssml):
    """Tao script PowerShell doc 1 doan bang SAPI (System.Speech).
    wav_path=None -> phat ra loa; khac None -> ghi ra file WAV.
    Giong: uu tien giong tieng Viet (vi-*) nu, neu khong co thi lay
    giong mac dinh cua may. Toc do qua thuoc tinh Rate (-10..10);
    cao do chi chinh duoc qua SSML prosody (neu dung_ssml)."""
    from xml.sax.saxutils import escape as xml_escape
    # v1.3: toc_do la he so nhan (1.35x) - doi sang phan tram (+35) roi
    # moi doi sang thang Rate -10..10 cua SAPI.
    phan_tram = _toc_do_sang_phan_tram(toc_do)
    rate_plain = max(-10, min(10, int(round(phan_tram / 5.0))))
    ssml = ""
    if dung_ssml:
        rate_str = "medium" if phan_tram == 0 else ("%+d%%" % phan_tram)
        pitch_str = "default" if cao_do == 0 else ("%+dHz" % cao_do)
        ssml = ('<speak version="1.0" '
                'xmlns="http://www.w3.org/2001/10/synthesis" '
                'xml:lang="vi-VN"><prosody rate="%s" pitch="%s">%s'
                '</prosody></speak>'
                % (rate_str, pitch_str, xml_escape(text)))
    wav_ps = "$null" if wav_path is None else _ps_quote(wav_path)
    dung = "$true" if dung_ssml else "$false"
    return "\n".join([
        "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
        "$ErrorActionPreference = 'Stop'",
        "Add-Type -AssemblyName System.Speech",
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer",
        "$tatCa = $synth.GetInstalledVoices() | Where-Object { $_.Enabled }",
        "$vi = @($tatCa | Where-Object { "
        "$_.VoiceInfo.Culture.Name -like 'vi*' })",
        "if ($vi.Count -eq 0) { $vi = @($tatCa) }",
        "if ($vi.Count -eq 0) { Write-Error 'NO_VOICE'; exit 1 }",
        "$chon = $vi | Where-Object { $_.VoiceInfo.Gender -eq 'Female' } "
        "| Select-Object -First 1",
        "if (-not $chon) { $chon = $vi | Select-Object -First 1 }",
        "$synth.SelectVoice($chon.VoiceInfo.Name)",
        "Write-Output ('VOICE:' + $chon.VoiceInfo.Name)",
        "$wav = %s" % wav_ps,
        "if ($wav) { $synth.SetOutputToWaveFile($wav) }",
        "$daDoc = $false",
        "if (%s) {" % dung,
        "    try {",
        "        $synth.SpeakSsml(%s)" % _ps_quote(ssml),
        "        $daDoc = $true",
        "        Write-Output 'MODE:SSML'",
        "    } catch {",
        "        Write-Output ('SSML_FAIL:' + $_.Exception.Message)",
        "        if ($wav) {",
        "            $synth.SetOutputToDefaultAudioDevice()",
        "            Remove-Item -LiteralPath $wav -ErrorAction "
        "SilentlyContinue",
        "            $synth.SetOutputToWaveFile($wav)",
        "        }",
        "    }",
        "}",
        "if (-not $daDoc) {",
        "    $synth.Rate = %d" % rate_plain,
        "    $synth.Speak(%s)" % _ps_quote(text),
        "    Write-Output 'MODE:PLAIN'",
        "}",
        "$synth.Dispose()",
    ])


def _chay_giong_may(text, toc_do, cao_do, wav_path, log_cb=None, dung=None):
    """Chay PowerShell System.Speech doc 1 doan.
    wav_path=None -> phat ra loa; wav_path=... -> ghi ra file WAV.
    `dung` (threading.Event, tuy chon): khi duoc dat thi tat tien trinh
    PowerShell ngay (nut 'Dung' khi nghe thu). Tra ve (thanh_cong,
    ten_giong, loi)."""
    if not sys.platform.startswith("win"):
        return False, "", "giọng máy chỉ dùng được trên Windows"
    import tempfile
    dung_ssml = (cao_do != 0)
    ps = _ps_giong_may(text, toc_do, cao_do, wav_path, dung_ssml)
    fd, ps_path = tempfile.mkstemp(suffix=".ps1")
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig") as f:
            f.write(ps)
        try:
            proc = subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive",
                 "-ExecutionPolicy", "Bypass", "-File", ps_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace")
        except Exception as e:
            return False, "", "không chạy được PowerShell: %s" % e
        # Cho tien trinh xong, vua cho vua kiem tra nut Dung / het gio.
        bat_dau = time.monotonic()
        while proc.poll() is None:
            if dung is not None and dung.is_set():
                try:
                    proc.kill()
                except Exception:
                    pass
                proc.wait()
                return False, "", "đã dừng nghe thử"
            if time.monotonic() - bat_dau > 180:
                try:
                    proc.kill()
                except Exception:
                    pass
                proc.wait()
                return False, "", "hết thời gian chờ giọng máy (180s)"
            time.sleep(0.1)
        out, err = proc.communicate()
        out = (out or "") + "\n" + (err or "")
        ten_giong = ""
        for dong in out.splitlines():
            if dong.strip().startswith("VOICE:"):
                ten_giong = dong.strip()[len("VOICE:"):].strip()
        if "NO_VOICE" in out or proc.returncode != 0:
            return False, ten_giong, _tom_tat_loi(
                out.strip() or "PowerShell báo lỗi (mã %d)" % proc.returncode)
        if dung_ssml and "MODE:PLAIN" in out and log_cb:
            log_cb("  (giọng máy không nhận cao độ, đã đọc bằng giọng "
                   "thường)")
        return True, ten_giong, ""
    finally:
        _xoa_file_quiet(ps_path)


def nghe_giong_may(text, toc_do, cao_do, log_cb=None, dung=None):
    """Doc 1 doan bang giong may ra loa (khong tao file). Tra ve
    (thanh_cong, loi)."""
    ok, ten_giong, loi = _chay_giong_may(text, toc_do, cao_do, None, log_cb,
                                         dung)
    if ok and log_cb and ten_giong:
        log_cb("  Giọng máy đang dùng: %s" % ten_giong)
    return ok, loi


def _doc_giong_may_1_doan(text, toc_do, cao_do, duong_dan_ra, log_cb,
                          ffmpeg):
    """Doc 1 doan ngan bang giong may ra file WAV tam, chuyen sang MP3."""
    import tempfile
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        ok, ten_giong, loi = _chay_giong_may(text, toc_do, cao_do,
                                             wav_path, log_cb)
        if not ok:
            return False, False, loi
        if log_cb and ten_giong:
            log_cb("  Giọng máy đang dùng: %s" % ten_giong)
        try:
            r = subprocess.run([ffmpeg, "-y", "-i", wav_path,
                                duong_dan_ra],
                               capture_output=True, timeout=120)
        except Exception as e:
            return False, False, "lỗi chạy ffmpeg: %s" % e
        if (r.returncode != 0 or not os.path.isfile(duong_dan_ra)
                or os.path.getsize(duong_dan_ra) == 0):
            return False, False, "ffmpeg không chuyển được WAV sang MP3"
        return True, False, ""
    finally:
        _xoa_file_quiet(wav_path)


def doc_giong_may(text, toc_do, cao_do, duong_dan_ra, log_cb=None,
                  ffmpeg=None):
    """Doc 1 cau bang giong may tren Windows thanh file MP3.
    Tra ve (thanh_cong, False, thong_bao_loi). Can ffmpeg de chuyen
    WAV sang MP3."""
    if not sys.platform.startswith("win"):
        return False, False, "giọng máy chỉ dùng được trên Windows"
    if not ffmpeg:
        return False, False, ("cần ffmpeg để xuất MP3 bằng giọng máy "
                              "(đặt ffmpeg.exe cạnh tool hoặc thêm vào "
                              "PATH)")
    doan_list = tach_cau_dai(text)
    if len(doan_list) == 1:
        return _doc_giong_may_1_doan(text, toc_do, cao_do, duong_dan_ra,
                                     log_cb, ffmpeg)
    # (v7.7) Cau dai: doc tung doan roi noi lai bang ffmpeg concat
    # demuxer, KHONG dung pydub nua (xem doc_thanh_mp3).
    import tempfile
    tam_files = []
    try:
        for j, doan in enumerate(doan_list):
            with tempfile.NamedTemporaryFile(suffix=".mp3",
                                             delete=False) as tmp:
                tam_path = tmp.name
            tam_files.append(tam_path)
            ok, _, loi = _doc_giong_may_1_doan(doan, toc_do, cao_do,
                                               tam_path, log_cb, ffmpeg)
            if not ok:
                _xoa_file_quiet(duong_dan_ra)
                return False, False, "doan %d loi: %s" % (j + 1, loi)
        ok_gop, loi_gop = _gop_mp3_concat(
            [(p, None) for p in tam_files], duong_dan_ra, ffmpeg,
            log_cb=log_cb, timeout_giay=180,
            log_loi_dir=os.path.dirname(duong_dan_ra) or ".")
        if not ok_gop:
            _xoa_file_quiet(duong_dan_ra)
            return False, False, "nối các đoạn lỗi: %s" % loi_gop
        return True, False, ""
    finally:
        for p in tam_files:
            _xoa_file_quiet(p)


def doc_cau_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra,
                      log_cb=None, ffmpeg=None,
                      timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                      dung=None):
    """Doc 1 cau thanh file MP3, chon duong giong theo `voice`:
    'may' -> giong SAPI tren may Windows (PowerShell System.Speech);
    con lai -> Edge TTS online (HoaiMy/NamMinh).
    Tra ve (thanh_cong, da_dung_bo_xac_minh, thong_bao_loi).
    (v7.7) `dung` (threading.Event) de nut Huy dung duoc ngay ca
    khi dang cho giong; `timeout_giay` gioi han moi lan goi giong."""
    if voice == "may":
        return doc_giong_may(text, toc_do, cao_do, duong_dan_ra, log_cb,
                             ffmpeg)
    return doc_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra,
                         log_cb, ffmpeg=ffmpeg,
                         timeout_giay=timeout_giay, dung=dung)


TOC_DO_DOC_TRUNG_BINH_KY_TU_GIAY = 13.5  # toc do doc trung binh tieng


DUNG_SAI_TRAN_SLOT_MS = 100  # dung sai khi so thoi luong audio voi


def _uoc_luong_thoi_luong_ms(text, toc_do=1.0):
    """Uoc luong thoi luong doc (ms) tu do dai van ban, khi khong do
    duoc file audio that. Chi la uoc luong - duong chinh van la do
    thoi luong that cua file sau khi tao."""
    ky_tu = len((text or "").strip())
    if ky_tu == 0:
        return 0
    return int(ky_tu / TOC_DO_DOC_TRUNG_BINH_KY_TU_GIAY * 1000
               / max(0.5, float(toc_do)))


def _do_dai_mp3_ms(duong_dan, ffmpeg):
    """Do thoi luong file MP3 (ms). Chi dung ffprobe (nhanh, chinh
    xac). (v7.7) BO fallback pydub: ban exe thieu pydub thi fallback
    nay chet im/khong do duoc; khong do duoc thi tra None de ben goi
    uoc luong tu do dai van ban (xem _ap_dung_toc_do_tu_dong).
    Tra ve None neu khong do duoc (vd: thieu ffmpeg, file loi)."""
    if not os.path.isfile(duong_dan):
        return None
    try:
        if os.path.getsize(duong_dan) == 0:
            return None
    except OSError:
        return None
    ffprobe = tim_ffprobe(ffmpeg) if ffmpeg else None
    if ffprobe:
        try:
            r = subprocess.run(
                [ffprobe, "-v", "error", "-show_entries",
                 "format=duration", "-of",
                 "default=noprint_wrappers=1:nokey=1", duong_dan],
                capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and r.stdout.strip():
                return int(float(r.stdout.strip()) * 1000)
        except Exception:
            pass
    return None


def _tinh_toc_do_can(slot_ms, do_dai_ms, toc_do_co_ban, toc_do_toi_da):
    """Tinh toc do thuc te can dung cho 1 cau (he so nhan so voi 1.00x).
    - slot_ms: do dai slot SRT cua cau (ket_thuc - bat_dau).
    - do_dai_ms: thoi luong audio da tao o toc_do_co_ban (None neu
      khong do duoc).
    Tra ve (toc_do_thuc_te, he_so_atempo, vuot_toc_do_toi_da):
    - Doc vua slot thi toc_do_thuc = toc_do_co_ban, he_so = 1.0.
    - Can nhanh hon: he_so = do_dai/slot; toc_do_thuc =
      toc_do_co_ban * he_so, nhung KHONG vuot toc_do_toi_da (toc do toi
      da hieu dung it nhat bang toc do co ban - khong the cham lai duoi
      toc do da doc).
    - vuot_toc_do_toi_da=True khi can nhanh hon ca toc do toi da (cau
      do se tran slot du da o toc do toi da)."""
    try:
        co_ban = float(toc_do_co_ban)
    except (TypeError, ValueError):
        co_ban = 1.0
    try:
        toi_da = float(toc_do_toi_da)
    except (TypeError, ValueError):
        toi_da = 1.35
    toi_da = max(toi_da, co_ban)  # khong cham lai duoi toc do co ban
    if not slot_ms or slot_ms <= 0 or not do_dai_ms or do_dai_ms <= 0:
        return co_ban, 1.0, False
    if do_dai_ms <= slot_ms:
        return co_ban, 1.0, False
    he_so = do_dai_ms / float(slot_ms)
    toc_do_thuc = co_ban * he_so
    if toc_do_thuc > toi_da:
        return toi_da, toi_da / co_ban, True
    return toc_do_thuc, he_so, False


def _chuoi_atempo(he_so):
    """Tach he so tang toc thanh chuoi filter atempo cua ffmpeg (moi
    atempo chi nhan 0.5-2.0). vd: 1.6 -> 'atempo=1.6000';
    3.2 -> 'atempo=2.0000,atempo=1.6000'."""
    chuoi = []
    con = float(he_so)
    while con > 2.0:
        chuoi.append("atempo=2.0000")
        con /= 2.0
    chuoi.append("atempo=%.4f" % con)
    return ",".join(chuoi)


def _tang_toc_mp3(duong_dan, he_so, ffmpeg):
    """Tang toc file MP3 tai cho bang ffmpeg atempo (ghi qua file tam
    roi chep de len file goc). Tra ve True neu xong, False neu loi
    (khong co ffmpeg, he_so khong hop le, ffmpeg bao loi)."""
    if not ffmpeg or not he_so or he_so <= 1.0:
        return False
    import tempfile
    fd, tam = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    try:
        r = subprocess.run([ffmpeg, "-y", "-i", duong_dan, "-vn",
                            "-af", _chuoi_atempo(he_so),
                            "-b:a", "128k", tam],
                           capture_output=True, timeout=120)
        if (r.returncode != 0 or not os.path.isfile(tam)
                or os.path.getsize(tam) == 0):
            return False
        shutil.copyfile(tam, duong_dan)
        return True
    except Exception:
        return False
    finally:
        _xoa_file_quiet(tam)


def _ap_dung_toc_do_tu_dong(duong_dan, cau, toc_do_co_ban, toc_do_toi_da,
                            tu_dong, ffmpeg, log_cb=None):
    """Ap dung toc do tu dong theo slot SRT cho 1 cau vua doc xong.
    Tra ve toc_do_thuc_te (he so nhan) cua cau do.
    - Tat tu_dong: tra ve toc_do_co_ban, khong lam gi (hanh vi cu v1.3).
    - Do thoi luong that cua file (ffprobe); khong do duoc thi
      uoc luong tu do dai van ban.
    - Can nhanh hon thi dung ffmpeg atempo tang toc file tai cho.
    - Khong kip du o toc do toi da (hoac khong tang toc duoc) thi ghi
      log canh bao 'Câu X đọc hết Ys nhưng slot chỉ có Zs (tràn sang
      câu sau)'."""
    try:
        co_ban = float(toc_do_co_ban)
    except (TypeError, ValueError):
        co_ban = 1.0
    if not tu_dong:
        return co_ban
    slot_ms = cau["ket_thuc_ms"] - cau["bat_dau_ms"]
    if slot_ms <= 0:
        return co_ban
    do_dai = _do_dai_mp3_ms(duong_dan, ffmpeg)
    if do_dai is None:
        do_dai = _uoc_luong_thoi_luong_ms(cau["text"], co_ban)
        if log_cb and do_dai > 0:
            log_cb("  (câu %d: không đo được thời lượng file, ước lượng "
                   "%.1fs từ độ dài văn bản)" % (cau["chi_so"],
                                                do_dai / 1000.0))
    if do_dai <= 0:
        return co_ban
    toc_do_thuc, he_so, vuot_max = _tinh_toc_do_can(
        slot_ms, do_dai, co_ban, toc_do_toi_da)
    if he_so > 1.005:
        if ffmpeg and _tang_toc_mp3(duong_dan, he_so, ffmpeg):
            if log_cb:
                log_cb("  Câu %d: đọc %.1fs, slot %.1fs -> tăng tốc lên "
                       "%.2fx" % (cau["chi_so"], do_dai / 1000.0,
                                  slot_ms / 1000.0, toc_do_thuc))
        else:
            if log_cb:
                log_cb("  Câu %d: cần %.2fx mới kịp slot nhưng không tăng "
                       "tốc được (thiếu ffmpeg) - giữ tốc độ %.2fx"
                       % (cau["chi_so"], toc_do_thuc, co_ban))
            toc_do_thuc = co_ban
            he_so = 1.0
    # Kiem tra tran slot sau khi tang toc (do lai thoi luong that neu
    # vua tang toc; neu khong thi dung so da do/uoc luong).
    do_dai_cuoi = do_dai
    if he_so > 1.005:
        do_dai_moi = _do_dai_mp3_ms(duong_dan, ffmpeg)
        do_dai_cuoi = (do_dai_moi if do_dai_moi is not None
                       else int(do_dai / he_so))
    if do_dai_cuoi > slot_ms + DUNG_SAI_TRAN_SLOT_MS:
        if log_cb:
            log_cb("  Cảnh báo: Câu %d đọc hết %.1fs nhưng slot chỉ có "
                   "%.1fs (tràn sang câu sau)"
                   % (cau["chi_so"], do_dai_cuoi / 1000.0,
                      slot_ms / 1000.0))
    return toc_do_thuc


def _phat_mp3(path, dung=None):
    """Phat 1 file MP3 ra loa NGAY trong tool (dung cho nut 'Nghe thu
    giong'). Windows: dung winmm (MCI) co san - phat khong cho roi
    tu cho xong, KHONG mo trinh phat ngoai, KHONG luu file. `dung`
    (threading.Event, tuy chon): khi duoc dat thi dung phat ngay (nut
    'Dung' khi nghe thu). Tra ve (thanh_cong, loi)."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            winmm = ctypes.windll.winmm
            winmm.mciSendStringW("close tts_nghe", None, 0, 0)
            r = winmm.mciSendStringW(
                'open "%s" alias tts_nghe' % path, None, 0, 0)
            if r != 0:
                return False, "không mở được file âm thanh để phát (mã %d)" % r
            r = winmm.mciSendStringW("play tts_nghe", None, 0, 0)
            if r != 0:
                winmm.mciSendStringW("close tts_nghe", None, 0, 0)
                return False, "không phát được audio (mã %d)" % r
            # Cho phat xong hoac bi dung (poll trang thai MCI).
            buf = ctypes.create_unicode_buffer(64)
            bat_dau = time.monotonic()
            da_phat = False
            while True:
                if dung is not None and dung.is_set():
                    winmm.mciSendStringW("stop tts_nghe", None, 0, 0)
                    winmm.mciSendStringW("close tts_nghe", None, 0, 0)
                    return False, "đã dừng nghe thử"
                winmm.mciSendStringW("status tts_nghe mode", buf, 64, 0)
                che_do = buf.value.strip().lower()
                if che_do == "playing":
                    da_phat = True
                elif da_phat:
                    break
                elif time.monotonic() - bat_dau > 2:
                    # Khong thay phat (file rat ngan hoac loi) - thoat.
                    break
                time.sleep(0.1)
            winmm.mciSendStringW("close tts_nghe", None, 0, 0)
            return True, ""
        except Exception as e:
            return False, "không phát được audio: %s" % e
    # Khong phai Windows (chi dung khi test): thu ffplay neu co.
    try:
        proc = subprocess.Popen(["ffplay", "-nodisp", "-autoexit",
                                 "-loglevel", "error", path],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        while proc.poll() is None:
            if dung is not None and dung.is_set():
                proc.kill()
                proc.wait()
                return False, "đã dừng nghe thử"
            time.sleep(0.1)
        return True, ""
    except Exception as e:
        return False, "không phát được audio trên hệ này: %s" % e


def _ffprobe_thong_so_audio(duong_dan, ffmpeg):
    """(v7.7) Do (sample_rate, channels) cua 1 file audio qua ffprobe
    (de tao file im lang cung thong so khi gop). Tra ve None neu
    khong do duoc."""
    ffprobe = tim_ffprobe(ffmpeg) if ffmpeg else None
    if not ffprobe:
        return None
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=sample_rate,channels",
             "-of", "json", duong_dan],
            capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            data = json.loads(r.stdout)
            streams = data.get("streams") or []
            if streams:
                sr = int(streams[0].get("sample_rate") or 0)
                ch = int(streams[0].get("channels") or 0)
                if sr > 0 and ch > 0:
                    return sr, ch
    except Exception:
        pass
    return None


def _tao_file_im_lang_1s(ffmpeg, thu_muc, sample_rate=24000, channels=1):
    """(v7.7) Tao file im lang 1 giay (MP3) cung thong so audio voi
    file cau, de lam khoang lang trong danh sach concat. File duoc
    tao 1 lan roi dung lai. Tra ve duong dan hoac None neu tao
    khong duoc."""
    ten = "_im-lang-1s-%d-%d.mp3" % (sample_rate, channels)
    dich = os.path.join(thu_muc, ten)
    try:
        if os.path.isfile(dich) and os.path.getsize(dich) > 0:
            return dich
    except OSError:
        pass
    layout = "mono" if channels <= 1 else "stereo"
    try:
        r = subprocess.run(
            [ffmpeg, "-y", "-f", "lavfi", "-i",
             "anullsrc=channel_layout=%s:sample_rate=%d"
             % (layout, sample_rate),
             "-t", "1", "-b:a", "128k", dich],
            capture_output=True, timeout=60)
        if (r.returncode == 0 and os.path.isfile(dich)
                and os.path.getsize(dich) > 0):
            return dich
    except Exception:
        pass
    return None


def _them_doan_im_lang(danh_sach, gap_ms, file_im_lang):
    """(v7.7) Them khoang lang gap_ms vao danh sach concat: lap lai
    file im lang 1s (phan du < 1s thi cat bang outpoint)."""
    con = max(0, int(gap_ms))
    while con >= 1000:
        danh_sach.append((file_im_lang, None))
        con -= 1000
    if con >= 50:
        danh_sach.append((file_im_lang, con / 1000.0))


def _chay_ffmpeg_co_gioi_han(cmd, timeout_giay, dung=None, log_cb=None,
                            nhan="ffmpeg"):
    """(v7.7) Chay ffmpeg, vua chay vua kiem tra nut Huy (dung) va
    het gio. Tra ve (returncode, stderr_text). Het gio thi kill va
    raise TimeoutError; bam Huy thi kill va tra (-1, "đã hủy")."""
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
        **chay_ngam_kwargs())
    bat_dau = time.monotonic()
    da_log = 0
    while True:
        try:
            _, err = proc.communicate(timeout=5)
            return proc.returncode, err or ""
        except subprocess.TimeoutExpired:
            pass
        if dung is not None and dung.is_set():
            try:
                proc.kill()
            except Exception:
                pass
            try:
                proc.communicate()
            except Exception:
                pass
            return -1, "đã hủy"
        da_cho = time.monotonic() - bat_dau
        if timeout_giay and da_cho > timeout_giay:
            try:
                proc.kill()
            except Exception:
                pass
            try:
                proc.communicate()
            except Exception:
                pass
            raise TimeoutError("%s chạy quá %ds"
                               % (nhan, int(timeout_giay)))
        if log_cb and da_cho - da_log >= 60:
            da_log = da_cho
            log_cb("  (%s đang chạy... đã chờ %ds)"
                   % (nhan, int(da_cho)))


def _gop_mp3_concat(danh_sach_doan, dich, ffmpeg, log_cb=None, dung=None,
                    timeout_giay=None, log_loi_dir=None,
                    do_dai_mong_doi_ms=None):
    """(v7.7) Gop cac file MP3 thanh 1 file bang ffmpeg concat demuxer.
    danh_sach_doan: list (duong_dan, outpoint_giay_hoac_None) —
    outpoint de cat file khi audio dai hon slot SRT cua no; None thi
    lay het file. Thu -c copy truoc (nhanh, khong re-encode); loi thi
    thu lai re-encode libmp3lame; xong kiem tra do dai file ra bang
    ffprobe neu co do_dai_mong_doi_ms. Loi day du ghi vao
    ffmpeg-loi.log trong log_loi_dir. Tra ve (True, "") hoac
    (False, loi_ngan).
    LUU Y (da kiem chung tren ffmpeg 8.1): chi thi `duration` cua
    concat demuxer KHONG duoc dung o day — no bi bo qua hoan toan
    (file van lay het do dai that). Muon dung khoang lang/slot thi
    dung file im lang co do dai that + outpoint de cat."""
    if not ffmpeg:
        return False, "không tìm thấy ffmpeg"
    if not danh_sach_doan:
        return False, "không có đoạn nào để gộp"
    thu_muc_txt = os.path.dirname(dich) or "."
    txt_path = os.path.join(thu_muc_txt, "_gop-danh-sach.txt")
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            for duong_dan, outpoint in danh_sach_doan:
                f.write("file '%s'\n"
                        % str(duong_dan).replace("'", "'\\''"))
                if outpoint is not None and float(outpoint) > 0:
                    f.write("outpoint %.3f\n" % float(outpoint))
    except OSError as e:
        return False, "không ghi được danh sách gộp: %s" % e
    stderr_day_du = ""
    for che_do in ("copy", "re-encode"):
        if che_do == "copy":
            cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0",
                   "-i", txt_path, "-c", "copy", dich]
        else:
            cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0",
                   "-i", txt_path, "-c:a", "libmp3lame", "-b:a", "128k",
                   dich]
        try:
            rc, err = _chay_ffmpeg_co_gioi_han(
                cmd, timeout_giay, dung=dung, log_cb=log_cb,
                nhan="gộp MP3 (%s)" % che_do)
        except TimeoutError as e:
            if log_loi_dir:
                _ghi_log_loi_ffmpeg(
                    log_loi_dir, "gop MP3 %s timeout: %s" % (che_do, e))
            return False, "gộp MP3 hết thời gian chờ (%s)" % che_do
        stderr_day_du = err
        if rc == -1:
            return False, "đã hủy khi đang gộp MP3"
        if rc == 0 and os.path.isfile(dich) and os.path.getsize(dich) > 0:
            if do_dai_mong_doi_ms:
                do_dai = _do_dai_mp3_ms(dich, ffmpeg)
                if (do_dai is not None
                        and abs(do_dai - do_dai_mong_doi_ms)
                        > max(2000, do_dai_mong_doi_ms // 50)):
                    if log_cb:
                        log_cb("  (gộp MP3 %s: file ra dài %.1fs, lệch "
                               "%.1fs so với mong đợi %.1fs — thử lại "
                               "bằng re-encode)"
                               % (che_do, do_dai / 1000.0,
                                  abs(do_dai - do_dai_mong_doi_ms)
                                  / 1000.0,
                                  do_dai_mong_doi_ms / 1000.0))
                    if che_do == "copy":
                        continue
                    return False, ("file gộp dài %.1fs, lệch nhiều so "
                                   "với %.1fs mong đợi"
                                   % (do_dai / 1000.0,
                                      do_dai_mong_doi_ms / 1000.0))
            return True, ""
        if log_cb:
            if che_do == "copy":
                log_cb("  (gộp MP3 copy lỗi, mã %s — thử lại bằng "
                       "re-encode)" % rc)
            else:
                log_cb("  (gộp MP3 re-encode lỗi, mã %s)" % rc)
    if log_loi_dir:
        _ghi_log_loi_ffmpeg(
            log_loi_dir,
            "gop MP3 that bai (copy + re-encode):\n%s" % stderr_day_du)
    return False, "ffmpeg gộp MP3 lỗi (xem chi tiết trong ffmpeg-loi.log)"


class GopDan:
    """Gop MP3 theo moc thoi gian SRT bang ffmpeg concat demuxer
    (v7.7, VIET LAI — thay GopDan-WAV-tam cua v1.3/v7.5).
    Moi cau doc xong chi luu file MP3 rieng trong tung-cau (nhu tool
    cu da lam duoc); toi buoc hoan tat moi gop 1 lan: lap danh sach
    concat gom file tung cau xen ke file im lang 1s, dung moc gio
    SRT (cau nao doc dai hon slot thi cat bang outpoint), chay
    ffmpeg concat (thu -c copy, loi thi re-encode), kiem tra do dai
    file ra bang ffprobe.
    Loi ich so voi ban cu: khong con file WAV tam to bang tong thoi
    luong phim (voi 8156s thi vai tram MB den >1GB, truncate co the
    loi tren duong dan dai/o dia day), khong con timeout cung 600s
    o buoc chuyen WAV->MP3, loi ffmpeg ghi ro ra ffmpeg-loi.log.
    API giu nguyen nhu ban cu (them_cau / hoan_tat / so_cau /
    bo_qua / tran_slot / da_tao / do_dai_ms) de _chay khong phai
    doi logic goi."""

    def __init__(self, duong_dan_mp3, tong_ms=0, log_cb=None,
                 ffmpeg=None, thu_muc=None):
        self.mp3 = duong_dan_mp3
        # tong_ms: moc ket thuc cua cau cuoi trong SRT - file gop phai
        # dai du den moc nay (du cau cuoi doc ngan hon slot cua no).
        self.tong_ms = tong_ms
        self.log_cb = log_cb
        self.ffmpeg = ffmpeg
        # thu_muc: cho file im lang + danh sach concat tam (mac dinh
        # la thu muc tung-cau, khong de rac thu muc du an).
        self.thu_muc = thu_muc or os.path.dirname(duong_dan_mp3) or "."
        self.danh_sach = []  # list dict {cau, file, do_dai_ms}
        self.so_cau = 0       # so cau da ghi nhan
        self.bo_qua = 0       # so cau loi da bo qua (khong co audio)
        self.tran_slot = 0    # so cau doc dai hon slot cua no
        self.da_tao = False   # da ghi nhan cau dau tien

    def them_cau(self, cau, duong_dan_mp3_cau):
        """Ghi nhan 1 cau vua doc xong (KHONG ghep ngay nhu ban cu):
        kiem tra file audio co that/khong rong, do thoi luong that,
        dem tran slot. Cau nao khong co audio (thieu file, file rong)
        thi BO QUA - slot cua no se thanh khoang lang khi gop cuoi -
        cac cau khac van gop binh thuong. Tra ve True neu ghi nhan
        duoc, False neu bo qua."""
        try:
            ok_file = (os.path.isfile(duong_dan_mp3_cau)
                       and os.path.getsize(duong_dan_mp3_cau) > 0)
        except OSError:
            ok_file = False
        if not ok_file:
            if self.log_cb:
                self.log_cb("  Đã bỏ qua câu %d (file audio lỗi, không đọc "
                            "được)" % cau["chi_so"])
            self.bo_qua += 1
            return False
        do_dai = _do_dai_mp3_ms(duong_dan_mp3_cau, self.ffmpeg)
        if do_dai is None:
            # Khong do duoc (thieu ffprobe): uoc luong tu do dai van
            # ban, van ghi nhan de gop (sai so nho o moc gio).
            do_dai = _uoc_luong_thoi_luong_ms(cau["text"], 1.0)
            if do_dai <= 0:
                do_dai = cau["ket_thuc_ms"] - cau["bat_dau_ms"]
        cho_trong = cau["ket_thuc_ms"] - cau["bat_dau_ms"]
        # v1.4: dung sai 100ms (padding MP3) - tran it hon thi khong
        # dem la tran slot.
        if do_dai > cho_trong + DUNG_SAI_TRAN_SLOT_MS:
            self.tran_slot += 1
            if self.log_cb:
                self.log_cb("  Canh bao: cau %d doc het %.1fs nhung slot "
                            "chi co %.1fs (phan tran se bi cat khi cau sau "
                            "bat dau)" % (cau["chi_so"], do_dai / 1000.0,
                                         cho_trong / 1000.0))
        self.danh_sach.append({"cau": cau, "file": duong_dan_mp3_cau,
                               "do_dai_ms": do_dai})
        self.so_cau += 1
        self.da_tao = True
        return True

    def do_dai_ms(self):
        """Do dai du kien cua file gop (ms): moc ket thuc cua cau cuoi
        trong SRT (tong_ms)."""
        if not self.da_tao:
            return 0
        return self.tong_ms or 0

    def hoan_tat(self, ffmpeg=None, dung=None):
        """Gop cac cau da ghi nhan thanh 1 file MP3 duy nhat bang
        ffmpeg concat demuxer, dung moc thoi gian SRT. Tra ve
        (thanh_cong, do_dai_ms). `dung` (threading.Event) de nut Huy
        dung duoc ngay ca khi dang gop."""
        ffmpeg = ffmpeg or self.ffmpeg
        if not self.da_tao or self.so_cau == 0:
            return False, 0
        if not ffmpeg:
            if self.log_cb:
                self.log_cb("LỖI hoàn tất file gộp: không tìm thấy ffmpeg "
                            "(cần ffmpeg để gộp MP3).")
            return False, 0
        # (v7.7) Don sach file WAV tam cua ban cu neu con sot tu lan
        # chay v7.5 truoc (ten _long-tieng-tam.wav cung thu muc voi
        # file gop) de khoi nham voi file moi.
        if self.mp3.endswith("_long-tieng.mp3"):
            _xoa_file_quiet(self.mp3[:-len("_long-tieng.mp3")]
                            + "_long-tieng-tam.wav")
        # Thong so audio de tao file im lang cung loai voi file cau.
        sr, ch = 24000, 1
        thong_so = _ffprobe_thong_so_audio(self.danh_sach[0]["file"],
                                           ffmpeg)
        if thong_so:
            sr, ch = thong_so
        file_im_lang = _tao_file_im_lang_1s(ffmpeg, self.thu_muc, sr, ch)
        if file_im_lang is None and self.log_cb:
            self.log_cb("  (không tạo được file im lặng — các khoảng lặng "
                        "giữa câu sẽ bị bỏ qua, mốc giờ có thể lệch)")
        # Xay danh sach concat theo moc gio SRT.
        cac_cau = sorted(self.danh_sach,
                         key=lambda d: d["cau"]["bat_dau_ms"])
        danh_sach_doan = []
        con_troi = 0  # moc thoi gian hien tai trong file ra (ms)
        for idx, muc in enumerate(cac_cau):
            cau = muc["cau"]
            bat_dau = cau["bat_dau_ms"]
            # Slot cua cau: toi bat dau cau ke; cau cuoi thi toi ket
            # thuc cua no.
            if idx + 1 < len(cac_cau):
                ket_thuc_slot = cac_cau[idx + 1]["cau"]["bat_dau_ms"]
            else:
                ket_thuc_slot = cau["ket_thuc_ms"]
            slot_ms = max(0, ket_thuc_slot - bat_dau)
            if bat_dau > con_troi:
                if file_im_lang:
                    _them_doan_im_lang(danh_sach_doan,
                                       bat_dau - con_troi, file_im_lang)
                con_troi = bat_dau
            do_dai = muc["do_dai_ms"]
            if slot_ms > 0 and do_dai > slot_ms + DUNG_SAI_TRAN_SLOT_MS:
                danh_sach_doan.append((muc["file"], slot_ms / 1000.0))
                con_troi = max(con_troi, bat_dau + slot_ms)
            else:
                danh_sach_doan.append((muc["file"], None))
                con_troi = max(con_troi, bat_dau + do_dai)
        # Dem khoang lang cuoi cho du tong thoi luong phim.
        if self.tong_ms > con_troi and file_im_lang:
            _them_doan_im_lang(danh_sach_doan,
                               self.tong_ms - con_troi, file_im_lang)
            con_troi = self.tong_ms
        if self.log_cb:
            self.log_cb("Đang gộp %d câu thành 1 file MP3 (ffmpeg "
                        "concat, đúng mốc giờ SRT)..." % self.so_cau)
        # (v7.7) Timeout ti le voi tong thoi luong phim (toi thieu
        # 600s), khong con timeout cung 600s cho moi phim nhu ban cu.
        timeout_giay = max(600, self.tong_ms // 1000 + 600)
        ok, loi = _gop_mp3_concat(
            danh_sach_doan, self.mp3, ffmpeg, log_cb=self.log_cb,
            dung=dung, timeout_giay=timeout_giay,
            log_loi_dir=os.path.dirname(self.mp3) or ".",
            do_dai_mong_doi_ms=self.tong_ms if self.tong_ms > 0 else None)
        if not ok:
            if self.log_cb:
                self.log_cb("LỖI hoàn tất file gộp: %s (xem chi tiết "
                            "trong file ffmpeg-loi.log ở thư mục kết "
                            "quả)." % loi)
            return False, 0
        do_dai_ra = _do_dai_mp3_ms(self.mp3, ffmpeg)
        return True, (do_dai_ra if do_dai_ra is not None
                      else self.do_dai_ms())


TEN_FILE_TIEN_TRINH = "tien-trinh.json"


def _luu_tien_trinh(thu_muc, du_lieu):
    """Ghi tien trinh xuat dang do vao thu_muc/tien-trinh.json."""
    try:
        os.makedirs(_duong_dan_dai_win(thu_muc), exist_ok=True)
        with open(_duong_dan_dai_win(
                os.path.join(thu_muc, TEN_FILE_TIEN_TRINH)), "w",
                  encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _doc_tien_trinh(thu_muc):
    """Doc tien-trinh.json trong thu muc (tra ve dict hoac None)."""
    try:
        with open(_duong_dan_dai_win(
                os.path.join(thu_muc, TEN_FILE_TIEN_TRINH)), "r",
                  encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _xoa_tien_trinh(thu_muc):
    """Xoa file tien trinh (khi xuat xong 100%)."""
    _xoa_file_quiet(_duong_dan_dai_win(
        os.path.join(thu_muc, TEN_FILE_TIEN_TRINH)))


def _thu_muc_co_ket_qua(thu_muc):
    """Thu muc da co ket qua xuat nao chua (file MP3 gop, file cau rieng,
    hay file tien trinh)? Dung de biet co can tao thu muc moi khi
    'Sub lai tu dau' hay khong."""
    if not os.path.isdir(thu_muc):
        return False
    if os.path.isfile(os.path.join(thu_muc, TEN_FILE_TIEN_TRINH)):
        return True
    try:
        for ten in os.listdir(thu_muc):
            if ten.lower().endswith(".mp3"):
                return True
    except OSError:
        return False
    tc = os.path.join(thu_muc, "tung-cau")
    if os.path.isdir(tc):
        try:
            for ten in os.listdir(tc):
                if ten.lower().endswith(".mp3"):
                    return True
        except OSError:
            pass
    return False


def _thu_muc_xuat_moi(thu_muc_goc, ten_goc):
    """Thu muc xuat cho lan sub moi. Neu thu muc mac dinh da co ket qua
    (file MP3 cu / tien trinh cu) thi dung ten moi 'ten (1)', 'ten (2)'...
    de KHONG ghi de file cu (khoi mat cong da sub)."""
    base = os.path.join(thu_muc_goc, ten_goc)
    if not _thu_muc_co_ket_qua(base):
        return base
    n = 1
    while True:
        cand = os.path.join(thu_muc_goc, "%s (%d)" % (ten_goc, n))
        if not _thu_muc_co_ket_qua(cand):
            return cand
        n += 1


class CuaSoDocPhuDe(tk.Frame):  # (v7.4) Frame trong Notebook, khong con Toplevel
    def __init__(self, quan_ly, parent=None, srt_path=None, job=None):
        super().__init__(parent if parent is not None else quan_ly)
        self.quan_ly = quan_ly
        self.job = job or {}
        self._srt_path_khoi_dong = srt_path
        self.cfg = doc_config()
        self.hang_doi = queue.Queue()
        self.dang_chay = False
        self._yeu_cau_huy = threading.Event()  # co huy: worker kiem tra
        # giua cac cau, dung sau khi cau dang doc xong (khong ngat giua
        # cau, khong treo giao dien).
        # v1.3: tien trinh dang do de nut "Tiep tuc" dung (None neu khong
        # co); thu muc xuat dang dung cho file SRT da nap (mac dinh
        # <thu muc luu>/<ten file SRT>, doi khi "Sub lai tu dau" tao
        # thu muc moi).
        self.tien_trinh = None
        self.thu_muc_xuat = None
        self.cac_cau = []  # v1.3: danh sach cau SRT da nap (nut Nghe thu)
        # v1.3: trang thai nghe thu giong (nut PLAY phat ra loa).
        self.dang_nghe = False
        self._dung_nghe = threading.Event()  # nut Dung dat co nay
        self._dung_ui()
        if self._srt_path_khoi_dong and os.path.isfile(self._srt_path_khoi_dong):
            self.e_srt.delete(0, "end")
            self.e_srt.insert(0, self._srt_path_khoi_dong)
            self._nap_danh_sach_cau(self._srt_path_khoi_dong)
        self.after(200, self._xu_ly_hang_doi)

    def _dong_cua_so_doc(self):
        # (v7.4) Panel nam trong Notebook nen khong co nut dong cua so
        # rieng: chi dat co huy de worker dung sau cau hien tai (luu
        # tien-trinh.json), roi chuyen ve tab Quan ly.
        try:
            self._yeu_cau_huy.set()
        except Exception:
            pass
        try:
            if self.quan_ly is not None:
                self.quan_ly.chon_tab_quan_ly()
        except Exception:
            pass

    def _mo_cap_nhat_chipchip(self):
        # (v7.0) Khong con updater rieng cua SRT Reader: dung duy nhat
        # luong cap nhat cua ChipChip (QuanLy.bam_kiem_tra_cap_nhat).
        try:
            if self.quan_ly is not None:
                self.quan_ly.bam_kiem_tra_cap_nhat()
        except Exception:
            pass

    # ----- giao dien -----
    def _dung_ui(self):
        pad = {"padx": 8, "pady": 4}
        f = tk.Frame(self)
        f.pack(fill="x", **pad)

        tk.Label(f, text="File SRT:").grid(row=0, column=0, sticky="w")
        self.e_srt = tk.Entry(f, width=62)
        self.e_srt.grid(row=0, column=1, sticky="we")
        self.btn_chon_srt = tk.Button(f, text="Chọn...",
                                      command=self._chon_srt)
        self.btn_chon_srt.grid(row=0, column=2)
        f.columnconfigure(1, weight=1)

        tk.Label(f, text="Thư mục lưu:").grid(row=1, column=0, sticky="w")
        self.e_luu = tk.Entry(f, width=62)
        self.e_luu.grid(row=1, column=1, sticky="we")
        self.e_luu.insert(0, self.cfg.get("thu_muc_luu", ""))
        self.btn_chon_luu = tk.Button(f, text="Chọn...",
                                      command=self._chon_thu_muc)
        self.btn_chon_luu.grid(row=1, column=2)

        f2 = tk.Frame(self)
        f2.pack(fill="x", **pad)
        tk.Label(f2, text="Giọng đọc:").grid(row=0, column=0, sticky="w")
        self.cb_giong = ttk.Combobox(f2, values=list(GIONG.keys()),
                                     state="readonly", width=22)
        self.cb_giong.set(self.cfg.get("giong", GIONG_MAC_DINH))
        self.cb_giong.grid(row=0, column=1, sticky="w", padx=4)
        # Doi giong thi tien trinh cu khong con hop le -> danh gia lai
        # nut "Tiep tuc" (v1.3).
        self.cb_giong.bind("<<ComboboxSelected>>",
                           lambda e: self._cap_nhat_nut_tiep_tuc())

        # v1.3: toc do dang HE SO NHAN giong trang web test (0.5x-2.0x,
        # buoc 0.01 - 1.35x chinh duoc, gia tri config cu nhu 1.09x
        # cung giu nguyen duoc), mac dinh 1.00x.
        tk.Label(f2, text="Tốc độ:").grid(row=1, column=0, sticky="w")
        self.sl_toc_do = tk.Scale(f2, from_=0.5, to=2.0, resolution=0.01,
                                  orient="horizontal", length=220)
        self.sl_toc_do.set(_chuyen_toc_do_cu(self.cfg.get("toc_do", 1.0)))
        self.sl_toc_do.grid(row=1, column=1, sticky="w", padx=4)
        self.lb_toc_do = tk.Label(f2, text="1.00x")
        self.lb_toc_do.grid(row=1, column=2, sticky="w")
        self.sl_toc_do.configure(command=self._doi_toc_do)

        # v1.4 - Toc do tu dong theo tung cau (theo iContent): cau dai
        # doc nhanh hon moi kip slot, cau ngan doc dung nhip. Bat thi
        # moi cau tu tang toc toi da den "Toc do toi da" (mac dinh
        # 1.35x); tat thi moi cau doc dung toc do co ban (hanh vi cu
        # v1.3).
        self.var_tu_dong_toc_do = tk.BooleanVar(
            value=bool(self.cfg.get("tu_dong_toc_do", True)))
        self.cb_tu_dong = tk.Checkbutton(
            f2, text="Tự động chỉnh tốc độ từng câu",
            variable=self.var_tu_dong_toc_do,
            command=self._doi_tu_dong_toc_do)
        self.cb_tu_dong.grid(row=2, column=1, sticky="w", padx=4)
        tk.Label(f2, text="Tốc độ tối đa:").grid(row=3, column=0,
                                                 sticky="w")
        self.sl_toc_do_toi_da = tk.Scale(
            f2, from_=1.0, to=2.0, resolution=0.01, orient="horizontal",
            length=220)
        self.sl_toc_do_toi_da.set(
            max(1.0, min(2.0, float(self.cfg.get("toc_do_toi_da", 1.35)))))
        self.sl_toc_do_toi_da.grid(row=3, column=1, sticky="w", padx=4)
        self.lb_toc_do_toi_da = tk.Label(f2, text="1.35x")
        self.lb_toc_do_toi_da.grid(row=3, column=2, sticky="w")
        self.sl_toc_do_toi_da.configure(command=self._doi_toc_do_toi_da)
        if not self.var_tu_dong_toc_do.get():
            self.sl_toc_do_toi_da.configure(state="disabled")

        tk.Label(f2, text="Cao độ:").grid(row=4, column=0, sticky="w")
        self.sl_cao_do = tk.Scale(f2, from_=-20, to=20, orient="horizontal",
                                  length=220)
        self.sl_cao_do.set(int(self.cfg.get("cao_do", 0)))
        self.sl_cao_do.grid(row=4, column=1, sticky="w", padx=4)
        self.lb_cao_do = tk.Label(f2, text="+0Hz")
        self.lb_cao_do.grid(row=4, column=2, sticky="w")
        self.sl_cao_do.configure(command=self._doi_cao_do)
        # v1.3 - Nghe thu giong: go 1 doan van ngan vao o nay (de trong
        # thi nghe cau dang chon trong danh sach), bam nut PLAY la doc
        # va PHAT TIENG RA LOA NGAY trong tool (khong tao file MP3,
        # khong mo trinh phat ngoai). Nut Dung de dung giua chung.
        tk.Label(f2, text="Nghe thử:").grid(row=5, column=0, sticky="w")
        self.e_nghe_thu = tk.Entry(f2, width=30)
        self.e_nghe_thu.grid(row=5, column=1, sticky="w", padx=4)
        self.btn_nghe_thu = tk.Button(f2, text="▶ Nghe thử",
                                      command=self.bam_nghe_thu)
        self.btn_nghe_thu.grid(row=5, column=2, sticky="w", padx=2)
        self.btn_dung_nghe = tk.Button(f2, text="Dừng",
                                       command=self._dung_nghe_thu,
                                       state="disabled")
        self.btn_dung_nghe.grid(row=5, column=3, sticky="w", padx=2)
        self.lb_toc_do.configure(text=_dinh_dang_toc_do(self.sl_toc_do.get()))
        self.lb_toc_do_toi_da.configure(
            text=_dinh_dang_toc_do(self.sl_toc_do_toi_da.get()))
        self.lb_cao_do.configure(text=_dinh_dang_cao_do(self.sl_cao_do.get()))

        f3 = tk.Frame(self)
        f3.pack(fill="x", **pad)
        tk.Label(f3, text="Đầu ra:").grid(row=0, column=0, sticky="w")
        self.che_do = tk.StringVar(value=self.cfg.get("che_do", "gop"))
        tk.Radiobutton(f3, text="Gộp 1 file lồng tiếng (MP3)",
                       variable=self.che_do, value="gop",
                       command=self._cap_nhat_nut_tiep_tuc).grid(
                           row=0, column=1, sticky="w")
        tk.Radiobutton(f3, text="Từng câu riêng (MP3)",
                       variable=self.che_do, value="rieng",
                       command=self._cap_nhat_nut_tiep_tuc).grid(
                           row=0, column=2, sticky="w")
        tk.Radiobutton(f3, text="Cả hai",
                       variable=self.che_do, value="ca_hai",
                       command=self._cap_nhat_nut_tiep_tuc).grid(
                           row=0, column=3, sticky="w")

        # Danh sach cau trong file SRT: hien ngay khi chon file, cap nhat
        # trang thai tung cau trong luc xu ly (Cho/Dang doc/Xong/Loi).
        f_ds = tk.Frame(self)
        f_ds.pack(fill="both", expand=True, **pad)
        self.lb_so_cau = tk.Label(f_ds, text="Chưa chọn file SRT.",
                                  anchor="w")
        self.lb_so_cau.pack(fill="x")
        cot = ("stt", "bat_dau", "ket_thuc", "noi_dung", "trang_thai")
        self.tree_cau = ttk.Treeview(f_ds, columns=cot, show="headings",
                                     height=6)
        self.tree_cau.heading("stt", text="#")
        self.tree_cau.heading("bat_dau", text="Bắt đầu")
        self.tree_cau.heading("ket_thuc", text="Kết thúc")
        self.tree_cau.heading("noi_dung", text="Nội dung")
        self.tree_cau.heading("trang_thai", text="Trạng thái")
        self.tree_cau.column("stt", width=40, anchor="center")
        self.tree_cau.column("bat_dau", width=95, anchor="center")
        self.tree_cau.column("ket_thuc", width=95, anchor="center")
        self.tree_cau.column("noi_dung", width=300)
        self.tree_cau.column("trang_thai", width=130)
        sb_tree = ttk.Scrollbar(f_ds, orient="vertical",
                                command=self.tree_cau.yview)
        self.tree_cau.configure(yscrollcommand=sb_tree.set)
        self.tree_cau.pack(side="left", fill="both", expand=True)
        sb_tree.pack(side="left", fill="y")
        self._tree_ids = {}
        self.thu_muc_ket_qua = None
        self.file_gop = None

        f4 = tk.Frame(self)
        f4.pack(fill="x", **pad)
        # Nut chinh: xuat MP3 long tieng (nut to, chu dam).
        self.btn_bat_dau = tk.Button(
            f4, text="XUẤT MP3 LỒNG TIẾNG", command=self._bat_dau,
            font=("TkDefaultFont", 11, "bold"), padx=10, pady=4)
        self.btn_bat_dau.pack(side="left", padx=4)
        # v1.3 - nut "Tiep tuc": chi sang khi co tien trinh dang do da luu
        # (da xong den cau nao, file MP3 nao); bam thi doc tiep tu cau
        # chua xong va noi vao file cu, khong doc lai cau da xong.
        self.btn_tiep_tuc = tk.Button(
            f4, text="Tiếp tục", command=self._bat_dau_tiep_tuc,
            state="disabled", padx=10, pady=4)
        self.btn_tiep_tuc.pack(side="left", padx=4)
        # v1.3 - nut "Sub lai tu dau": doc lai tu cau 1, tao file MP3 moi
        # (thu muc moi ten (1), (2)... neu file cu da co, khong ghi de).
        self.btn_sub_lai = tk.Button(
            f4, text="Sub lại từ đầu", command=self._bat_dau_sub_lai,
            state="disabled", padx=10, pady=4)
        self.btn_sub_lai.pack(side="left", padx=4)
        # Nut Huy: chi bat khi dang chay, bam la dung sau cau hien tai.
        self.btn_huy = tk.Button(f4, text="Hủy", command=self._bam_huy,
                                 state="disabled", padx=10, pady=4)
        self.btn_huy.pack(side="left", padx=4)
        self.btn_kiem_tra = tk.Button(
            f4, text="Kiểm tra kết nối giọng",
            command=self._kiem_tra_giong)
        self.btn_kiem_tra.pack(side="left", padx=4)
        self.btn_cap_nhat = tk.Button(
            f4, text="Kiểm tra cập nhật (ChipChip)",
            command=self._mo_cap_nhat_chipchip)
        self.btn_cap_nhat.pack(side="left", padx=4)
        tk.Button(f4, text="Mở thư mục kết quả",
                  command=self._mo_thu_muc_ket_qua).pack(side="left", padx=4)

        self.lb_tien_trinh = tk.Label(self, text="Chưa chạy.")
        self.lb_tien_trinh.pack(fill="x", padx=8)
        self.thanh_tien_trinh = ttk.Progressbar(self, orient="horizontal",
                                                mode="determinate")
        self.thanh_tien_trinh.pack(fill="x", padx=8, pady=4)
        # Dong ket qua sau khi xuat xong: duong dan + do dai file MP3.
        self.lb_ket_qua = tk.Label(self, text="", anchor="w", wraplength=680,
                                   justify="left", fg="green")
        self.lb_ket_qua.pack(fill="x", padx=8)

        tk.Label(self, text="Nhật ký:").pack(anchor="w", padx=8)
        self.txt_log = tk.Text(self, height=16, wrap="word")
        self.txt_log.pack(fill="both", expand=True, padx=8, pady=4)
        sb = tk.Scrollbar(self.txt_log, command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=sb.set)

    # ----- doi toc do / cao do (v1.3: doi cai dat thi tien trinh cu co
    # the khong con hop le -> danh gia lai nut "Tiep tuc") -----
    def _doi_toc_do(self, v):
        # v1.3: toc do la he so nhan (1.35x) - hien thi '1.35x'.
        self.lb_toc_do.configure(text=_dinh_dang_toc_do(float(v)))
        self._cap_nhat_nut_tiep_tuc()

    def _doi_tu_dong_toc_do(self):
        # v1.4: bat/tat tu dong toc do - thanh Toc do toi da chi co
        # nghia khi bat (tat thi mo di). Doi cai dat thi tien trinh cu
        # co the khong con hop le -> danh gia lai nut "Tiep tuc".
        if self.var_tu_dong_toc_do.get():
            self.sl_toc_do_toi_da.configure(state="normal")
        else:
            self.sl_toc_do_toi_da.configure(state="disabled")
        self._cap_nhat_nut_tiep_tuc()

    def _doi_toc_do_toi_da(self, v):
        # v1.4: toc do toi da la he so nhan (1.35x) - hien thi '1.35x'.
        self.lb_toc_do_toi_da.configure(text=_dinh_dang_toc_do(float(v)))
        self._cap_nhat_nut_tiep_tuc()

    def _doi_cao_do(self, v):
        self.lb_cao_do.configure(text=_dinh_dang_cao_do(int(float(v))))
        self._cap_nhat_nut_tiep_tuc()

    # ----- khoa / mo nut khi dang chay (v1.3) -----
    def _khoa_nut_khi_chay(self, cho_huy=True):
        """Vo hieu hoa cac nut hanh dong trong luc dang xuat (hoac dang
        kiem tra giong): nut Kiem tra ket noi giong, Kiem tra cap nhat,
        2 nut Chon... file/thu muc, nut Tiep tuc, nut Sub lai tu dau va
        nut XUAT deu mo di - chi de nut Huy sang (neu cho_huy). Tranh
        truong hop bam kiem tra cung luc voi dang xuat gay xung dot
        (ca hai cung goi giong)."""
        for b in (self.btn_chon_srt, self.btn_chon_luu, self.btn_kiem_tra,
                  self.btn_cap_nhat, self.btn_tiep_tuc, self.btn_sub_lai,
                  self.btn_bat_dau, self.btn_nghe_thu):
            b.configure(state="disabled")
        self.btn_dung_nghe.configure(state="disabled")
        self.btn_huy.configure(state="normal" if cho_huy else "disabled")

    def _mo_khoa_nut(self):
        """Bat lai cac nut sau khi xuat/kiem tra xong (hoac da huy).
        Nut Tiep tuc / Sub lai tu dau thi danh gia lai theo tien trinh
        da luu (co the vua duoc luu khi huy)."""
        for b in (self.btn_chon_srt, self.btn_chon_luu, self.btn_kiem_tra,
                  self.btn_cap_nhat, self.btn_bat_dau, self.btn_nghe_thu):
            b.configure(state="normal")
        self.btn_dung_nghe.configure(state="disabled")
        self.btn_huy.configure(state="disabled")
        self._cap_nhat_nut_tiep_tuc()

    # ----- nut "Tiep tuc" / "Sub lai tu dau" (v1.3) -----
    def _cap_nhat_nut_tiep_tuc(self):
        """Danh gia lai nut Tiep tuc / Sub lai tu dau theo file SRT da nap
        va tien trinh da luu. Goi sau khi nap SRT, doi cai dat (giong/toc
        do/cao do/che do/thu muc luu), xuat xong hoac da huy.
        - Sub lai tu dau: sang khi da nap file SRT (co danh sach cau).
        - Tiep tuc: chi sang khi co tien trinh dang do HOP LE (dung file
          SRT, dung giong/toc do/cao do/che do, con cau chua xong, file
          cac cau da xong van con)."""
        co_srt = bool(self._tree_ids)
        self.btn_sub_lai.configure(state="normal" if co_srt else "disabled")
        self.tien_trinh = self._tien_trinh_hop_le() if co_srt else None
        self.btn_tiep_tuc.configure(
            state="normal" if self.tien_trinh else "disabled")

    def _tien_trinh_hop_le(self):
        """Doc tien-trinh.json trong thu muc xuat hien tai (va cac thu
        muc (1), (2)... neu lan xuat truoc tao thu muc moi), kiem tra
        con hop le khong. Tra ve dict tien trinh da loc (chi giu cau
        nao co file audio that) hoac None neu khong dung duoc nua (doi
        file SRT, doi giong/toc do/cao do/che do, khong con cau chua
        xong, hoac file cac cau da xong da mat). Neu co nhieu tien
        trinh thi lay cai co nhieu cau xong nhat."""
        if not self.thu_muc_xuat:
            return None
        srt = self.e_srt.get().strip()
        if not srt or not os.path.isfile(_duong_dan_dai_win(srt)):
            return None
        try:
            st = os.stat(_duong_dan_dai_win(srt))
        except OSError:
            return None
        # Cac thu muc ung vien: thu muc mac dinh + cac thu muc (1),
        # (2)... (lan xuat truoc co the da tao thu muc moi vi thu muc
        # cu da co ket qua).
        thu_muc_goc = os.path.dirname(self.thu_muc_xuat)
        ten_goc = os.path.basename(self.thu_muc_xuat)
        ung_vien = [self.thu_muc_xuat]
        for i in range(1, 21):
            thu_muc_i = os.path.join(thu_muc_goc, "%s (%d)" % (ten_goc, i))
            if os.path.isdir(thu_muc_i):
                ung_vien.append(thu_muc_i)
            else:
                break
        tot_nhat = None
        for thu_muc in ung_vien:
            tt = _doc_tien_trinh(thu_muc)
            if not tt:
                continue
            if os.path.abspath(tt.get("srt", "")) != os.path.abspath(srt):
                continue
            if (tt.get("srt_kich_thuoc") != st.st_size
                    or int(tt.get("srt_mtime", -1)) != int(st.st_mtime)):
                continue
            try:
                # v1.3: toc_do la he so nhan (so thuc) - so sanh co
                # dung sai nho vi slider luu dang float.
                toc_do_tt = float(tt.get("toc_do", 1.0))
                toc_do_hien = float(self.sl_toc_do.get())
                # v1.4: toc_do_toi_da + tu_dong_toc_do cung phai khop
                # (doi cai dat toc do thi cac cau con lai doc khac di).
                # Tien trinh v1.3 cu khong co 2 khoa nay -> mac dinh
                # (1.35x, True) nen van hop le neu giao dien dang de
                # mac dinh.
                toi_da_tt = float(tt.get("toc_do_toi_da", 1.35))
                toi_da_hien = float(self.sl_toc_do_toi_da.get())
                tu_dong_tt = bool(tt.get("tu_dong_toc_do", True))
                if (tt.get("giong") != self.cb_giong.get()
                        or abs(toc_do_tt - toc_do_hien) > 0.001
                        or abs(toi_da_tt - toi_da_hien) > 0.001
                        or tu_dong_tt != bool(
                            self.var_tu_dong_toc_do.get())
                        or int(tt.get("cao_do", 0)) != int(self.sl_cao_do.get())
                        or tt.get("che_do") != self.che_do.get()):
                    continue
            except (TypeError, ValueError):
                continue
            tong = int(tt.get("tong_cau", 0))
            if tong != len(self._tree_ids) or tong <= 0:
                continue
            thu_muc_rieng = tt.get("thu_muc_rieng") or os.path.join(
                tt.get("thu_muc", thu_muc), "tung-cau")
            xong = []
            for chi_so in tt.get("cau_da_xong", []):
                try:
                    chi_so = int(chi_so)
                except (TypeError, ValueError):
                    continue
                f = os.path.join(thu_muc_rieng, "%03d.mp3" % chi_so)
                # Chi tinh la xong neu file audio that su ton tai VA co
                # du lieu (file 0 byte do doc loi de lai thi phai doc
                # lai).
                if os.path.isfile(f) and os.path.getsize(f) > 0:
                    xong.append(chi_so)
            if not xong or len(xong) >= tong:
                continue
            tt = dict(tt)
            tt["cau_da_xong"] = sorted(set(xong))
            tt["thu_muc_rieng"] = thu_muc_rieng
            tt["thu_muc"] = tt.get("thu_muc", thu_muc)
            # v1.4: toc do thuc tung cau da xong (de hien lai trang thai
            # "Xong (1.60x)" khi noi lai file cu; khoa JSON la chuoi nen
            # doi lai sang so nguyen).
            toc_do_cau = {}
            try:
                for k, v in (tt.get("toc_do_cau") or {}).items():
                    toc_do_cau[int(k)] = float(v)
            except (TypeError, ValueError):
                toc_do_cau = {}
            tt["toc_do_cau"] = toc_do_cau
            if tot_nhat is None or len(xong) > len(
                    tot_nhat["cau_da_xong"]):
                tot_nhat = tt
        return tot_nhat

    # ----- chon file / danh sach cau -----
    def _chon_srt(self):
        p = filedialog.askopenfilename(filetypes=[("Phụ đề SRT", "*.srt"),
                                                 ("Mọi file", "*.*")])
        if p:
            self.e_srt.delete(0, "end")
            self.e_srt.insert(0, p)
            self._nap_danh_sach_cau(p)

    def _nap_danh_sach_cau(self, duong_dan):
        """Import file SRT: doc ngay va hien danh sach cau + thoi gian.
        Tra ve list cau, hoac None neu loi."""
        for item in self.tree_cau.get_children():
            self.tree_cau.delete(item)
        self._tree_ids = {}
        try:
            cac_cau = doc_srt(duong_dan)
        except Exception as e:
            self.lb_so_cau.configure(
                text="Lỗi đọc file SRT: %s" % e)
            messagebox.showerror(STUDIO_TITLE, "Lỗi đọc file SRT:\n%s" % e)
            return None
        if not cac_cau:
            self.lb_so_cau.configure(
                text="Không tìm thấy câu phụ đề nào trong file này.")
            self.cac_cau = []
            return []
        # v1.3: giu danh sach cau de nut 'Nghe thu' lay cau dang chon.
        self.cac_cau = cac_cau
        for cau in cac_cau:
            iid = self.tree_cau.insert("", "end", values=(
                cau["chi_so"],
                _dinh_dang_ms(cau["bat_dau_ms"]),
                _dinh_dang_ms(cau["ket_thuc_ms"]),
                cau["text"][:80],
                "Chờ"))
            self._tree_ids[cau["chi_so"]] = iid
        tong_ms = max(c["ket_thuc_ms"] for c in cac_cau)
        self.lb_so_cau.configure(
            text="Đã nạp %d câu, tổng dài %.1f giây (từ %s đến %s)." % (
                len(cac_cau), tong_ms / 1000.0,
                _dinh_dang_ms(cac_cau[0]["bat_dau_ms"]),
                _dinh_dang_ms(tong_ms)))
        self._log("Đã nạp %d câu từ file SRT." % len(cac_cau))
        # v1.3: thu muc xuat mac dinh cho file SRT nay + danh gia lai
        # nut "Tiep tuc" (co tien trinh dang do cua file nay khong?).
        ten_goc = os.path.splitext(os.path.basename(duong_dan))[0]
        # (v7.0, phu luc 4) Thu muc xuat mac dinh = thu muc chua file SRT.
        thu_muc_srt = os.path.dirname(os.path.abspath(duong_dan))
        self.e_luu.delete(0, "end")
        self.e_luu.insert(0, thu_muc_srt)
        self.thu_muc_xuat = thu_muc_srt
        self._cap_nhat_nut_tiep_tuc()
        return cac_cau

    def _dat_trang_thai_cau(self, chi_so, trang_thai):
        """Dat trang thai 1 cau trong danh sach (goi tu luong worker,
        qua hang doi de dung luong chinh cap nhat giao dien)."""
        self.hang_doi.put(("trang_thai_cau", chi_so, trang_thai))

    def _chon_thu_muc(self):
        p = filedialog.askdirectory()
        if p:
            self.e_luu.delete(0, "end")
            self.e_luu.insert(0, p)
            # Doi thu muc luu thi thu muc xuat doi theo -> danh gia lai
            # nut "Tiep tuc" (v1.3).
            if self._tree_ids:
                srt = self.e_srt.get().strip()
                ten_goc = os.path.splitext(os.path.basename(srt))[0]
                self.thu_muc_xuat = os.path.join(p, ten_goc)
            self._cap_nhat_nut_tiep_tuc()

    def _mo_thu_muc_ket_qua(self):
        # Uu tien mo dung thu muc chua file MP3 vua xuat; chua co thi mo
        # thu muc luu da chon.
        p = self.thu_muc_ket_qua or self.e_luu.get().strip() \
            or mac_dinh_thu_muc_luu_srt()
        if os.path.isdir(p):
            if sys.platform.startswith("win"):
                os.startfile(p)
            else:
                messagebox.showinfo(STUDIO_TITLE, "Thư mục kết quả:\n" + p)
        else:
            messagebox.showinfo(STUDIO_TITLE, "Chưa có thư mục kết quả:\n" + p)

    # ----- log / tien trinh -----
    def _log(self, s):
        self.hang_doi.put(("log", s))

    def _tien_trinh(self, phan_tram, nhan):
        self.hang_doi.put(("tien_trinh", phan_tram, nhan))

    def _xu_ly_hang_doi(self):
        try:
            while True:
                muc = self.hang_doi.get_nowait()
                if muc[0] == "log":
                    self.txt_log.insert("end", muc[1] + "\n")
                    self.txt_log.see("end")
                elif muc[0] == "tien_trinh":
                    self.thanh_tien_trinh["value"] = muc[1]
                    self.lb_tien_trinh.configure(text=muc[2])
                elif muc[0] == "trang_thai_cau":
                    iid = self._tree_ids.get(muc[1])
                    if iid and self.tree_cau.exists(iid):
                        vals = list(self.tree_cau.item(iid, "values"))
                        vals[4] = muc[2]
                        self.tree_cau.item(iid, values=tuple(vals))
                        self.tree_cau.see(iid)
                elif muc[0] == "ket_qua":
                    self.lb_ket_qua.configure(text=muc[1])
                elif muc[0] == "loi_hop_thoai":
                    # (v7.7) Worker gap loi nghiem trong thi bao bang hop
                    # thoai tren luong chinh (khong goi messagebox truc
                    # tiep tu luong worker - khong an toan voi tkinter).
                    messagebox.showerror(APP_TITLE, muc[1])
                elif muc[0] == "nghe_xong":
                    # v1.3: nghe thu xong (tu nhien hoac bam Dung) - mo
                    # lai nut Nghe thu, tat nut Dung.
                    self.dang_nghe = False
                    self._dung_nghe.clear()
                    if not self.dang_chay:
                        self.btn_nghe_thu.configure(state="normal")
                    self.btn_dung_nghe.configure(state="disabled")
                elif muc[0] == "xong":
                    self.dang_chay = False
                    self._mo_khoa_nut()
        except queue.Empty:
            pass
        self.after(200, self._xu_ly_hang_doi)

    def _luu_cai_dat_hien_tai(self):
        self.cfg.update({
            "giong": self.cb_giong.get(),
            # v1.3: toc_do luu dang he so nhan (1.35x).
            "toc_do": float(self.sl_toc_do.get()),
            # v1.4: toc do toi da + bat/tat tu dong toc do tung cau.
            "toc_do_toi_da": float(self.sl_toc_do_toi_da.get()),
            "tu_dong_toc_do": bool(self.var_tu_dong_toc_do.get()),
            "cao_do": int(self.sl_cao_do.get()),
            "thu_muc_luu": self.e_luu.get().strip(),
            "che_do": self.che_do.get(),
        })
        luu_config(self.cfg)

    # ----- kiem tra giong -----
    def _kiem_tra_giong(self):
        if self.dang_chay:
            return
        self._luu_cai_dat_hien_tai()
        # Lay het gia tri giao dien o luong chinh, truyen sang luong worker
        # (luong worker khong doc truc tiep widget tkinter - khong an toan).
        ts = {
            "voice": GIONG.get(self.cb_giong.get(), GIONG[GIONG_MAC_DINH]),
            "giong_hien_thi": self.cb_giong.get(),
            "toc_do": float(self.sl_toc_do.get()),
            "cao_do": int(self.sl_cao_do.get()),
            "thu_muc": self.e_luu.get().strip() or mac_dinh_thu_muc_luu_srt(),
        }
        self.dang_chay = True
        # v1.3: khoa cac nut khac trong luc kiem tra (khong cho Huy vi
        # kiem tra chi doc 1 cau ngan, xong ngay).
        self._khoa_nut_khi_chay(cho_huy=False)
        threading.Thread(target=self._chay_kiem_tra, args=(ts,),
                         daemon=True).start()

    def _chay_kiem_tra(self, ts):
        voice = ts["voice"]
        # v1.3 - giong may: khong can edge-tts, doc thu thang ra loa
        # (khong can file, khong can ffmpeg).
        if voice == "may":
            self._log("Kiểm tra giọng %s (giọng tiếng Việt có sẵn trên "
                      "máy Windows)..." % ts["giong_hien_thi"])
            ok, loi = nghe_giong_may(MAU_DOC_THU, ts["toc_do"],
                                     ts["cao_do"], log_cb=self._log)
            if ok:
                self._log("OK! Đã đọc thử ra loa bằng giọng máy.")
            else:
                self._log("LỖI: không dùng được giọng máy. %s" % loi)
            self.hang_doi.put(("xong",))
            return
        try:
            import edge_tts
            ver = getattr(edge_tts, "__version__", "?")
            import edge_tts.communicate as _comm
            may_chu = _ten_may_chu(_comm.WSS_URL)
        except Exception as e:
            # (v7.7) Thieu thu vien edge-tts trong ban exe: bao ro
            # ngay thay vi de doc thu loi mo ho o duoi.
            self._log("LỖI: thiếu thư viện edge-tts trong bản exe (lỗi "
                      "build: thiếu hidden import edge_tts) - %s" % e)
            self._log("Cài lại bản mới hoặc chạy file .py trực tiếp "
                      "(pip install edge-tts).")
            self.hang_doi.put(("xong",))
            return
        self._log("Kiểm tra giọng %s (%s)..." % (ts["giong_hien_thi"], voice))
        self._log("edge-tts %s; máy chủ giọng: %s" % (ver, may_chu))
        thu_muc = ts["thu_muc"]
        try:
            os.makedirs(thu_muc, exist_ok=True)
        except OSError as e:
            self._log("Lỗi tạo thư mục: %s" % e)
            self.hang_doi.put(("xong",))
            return
        dich = os.path.join(thu_muc, "doc-thu.mp3")
        ok, bo_xac_minh, loi = doc_cau_thanh_mp3(
            MAU_DOC_THU, voice, ts["toc_do"], ts["cao_do"], dich,
            log_cb=self._log)
        if ok:
            self._log("OK! Đã tạo file đọc thử: %s%s" % (
                dich, " (đã dùng chế độ bỏ xác minh SSL)" if bo_xac_minh else ""))
        else:
            self._log("LỖI: không tạo được giọng. %s" % loi)
            self._log("Tool đã thử cả máy chủ gốc speech.platform.bing.com "
                      "và máy chủ phụ api.msedgeservices.com. Kiểm tra mạng "
                      "rồi bấm lại; nếu vẫn lỗi, xem mã lỗi [403/429/"
                      "khong-co-audio] trong log ở trên.")
        self.hang_doi.put(("xong",))

    # ----- nghe thu giong (nut PLAY phat ra loa, v1.3) -----
    def bam_nghe_thu(self):
        """Nut '▶ Nghe thu': doc 1 cau va PHAT TIENG RA LOA NGAY trong
        tool (khong tao file MP3, khong mo trinh phat ngoai). Lay van
        ban tu o go (neu co) hoac tu cau dang chon trong danh sach.
        Khong nghe duoc trong luc dang xuat (tranh 2 viec cung goi
        giong 1 luc)."""
        if self.dang_chay or self.dang_nghe:
            return
        text = self.e_nghe_thu.get().strip()
        if not text:
            # Lay cau dang chon trong danh sach (neu co). _tree_ids map
            # chi_so -> iid nen phai tim nguoc chi_so tu iid da chon.
            chon = self.tree_cau.selection()
            if chon:
                iid_chon = chon[0]
                chi_so = None
                for cs, iid in self._tree_ids.items():
                    if iid == iid_chon:
                        chi_so = cs
                        break
                if chi_so is not None:
                    for cau in (self.cac_cau or []):
                        if cau["chi_so"] == chi_so:
                            text = cau["text"]
                            break
        if not text:
            messagebox.showinfo(
                APP_TITLE,
                "Hãy gõ 1 đoạn văn ngắn vào ô Nghe thử, hoặc chọn 1 câu "
                "trong danh sách rồi bấm ▶ Nghe thử.")
            return
        voice = GIONG.get(self.cb_giong.get(), GIONG[GIONG_MAC_DINH])
        toc_do = float(self.sl_toc_do.get())
        cao_do = int(self.sl_cao_do.get())
        self.dang_nghe = True
        self._dung_nghe.clear()
        self.btn_nghe_thu.configure(state="disabled")
        self.btn_dung_nghe.configure(state="normal")
        self._log("Nghe thử giọng %s: %s"
                  % (self.cb_giong.get(), text[:80]))
        threading.Thread(target=self._nghe_thu_worker,
                         args=(text, voice, toc_do, cao_do),
                         daemon=True).start()

    def _nghe_thu_worker(self, text, voice, toc_do, cao_do):
        """Luong nghe thu: giong may thi doc thang ra loa; giong online
        thi doc ra file MP3 tam roi phat ra loa trong tool (MCI), xong
        xoa file tam (khong luu file)."""
        try:
            if voice == "may":
                ok, loi = nghe_giong_may(text, toc_do, cao_do,
                                         log_cb=self._log,
                                         dung=self._dung_nghe)
                if not ok:
                    self._log("LỖI nghe thử giọng máy: %s" % loi)
            else:
                import tempfile
                fd, tam_path = tempfile.mkstemp(suffix=".mp3")
                os.close(fd)
                try:
                    ok, _, loi = doc_thanh_mp3(
                        text, voice, toc_do, cao_do, tam_path,
                        log_cb=self._log)
                    if not ok:
                        self._log("LỖI nghe thử: %s" % loi)
                    elif not self._dung_nghe.is_set():
                        ok_phat, loi_phat = _phat_mp3(
                            tam_path, dung=self._dung_nghe)
                        if not ok_phat and "đã dừng" not in loi_phat:
                            self._log("LỖI phát âm thanh: %s" % loi_phat)
                finally:
                    _xoa_file_quiet(tam_path)
        except Exception as e:
            self._log("LỖI nghe thử: %s" % _tom_tat_loi(e))
        finally:
            self.hang_doi.put(("nghe_xong",))

    def _dung_nghe_thu(self):
        """Nut 'Dung': dung nghe thu giua chung (dung phat audio /
        tat tien trinh giong may)."""
        if not self.dang_nghe:
            return
        self._dung_nghe.set()
        self._log("Đã dừng nghe thử.")

    # ----- tu cap nhat (v1.1, theo mau Chipchipdownload v6.2) -----
    # Repo PUBLIC nen khong can token: doc Releases qua API khong xac thuc.







    # ----- chay chinh -----
    def _bam_huy(self):
        """Nut Huy: dat co, worker se dung sau khi cau dang doc xong
        (khong ngat giua cau). Mo nut ngay de khong bam 2 lan."""
        if not self.dang_chay:
            return
        self._yeu_cau_huy.set()
        self.btn_huy.configure(state="disabled")
        self._log("Đã bấm Hủy — sẽ dừng sau khi câu đang đọc xong...")

    def _bat_dau(self):
        """Nut XUAT MP3 LONG TIENG: xuat moi tu cau 1 vao thu muc mac
        dinh (neu thu muc da co ket qua cu thi tu dong dung thu muc
        moi ten (1), (2)... de khong ghi de - giong nut 'Sub lai tu
        dau')."""
        if self.dang_chay:
            return
        srt = self.e_srt.get().strip()
        if not srt or not os.path.isfile(_duong_dan_dai_win(srt)):
            messagebox.showwarning(STUDIO_TITLE, "Hãy chọn file SRT trước.")
            return
        # Neu danh sach cau chua nap (vd: go duong dan tay), nap ngay.
        if not self._tree_ids:
            if self._nap_danh_sach_cau(srt) is None:
                return
        ffmpeg = tim_ffmpeg()
        che_do = self.che_do.get()
        if che_do in ("gop", "ca_hai") and not ffmpeg:
            messagebox.showwarning(
                APP_TITLE,
                "Chế độ gộp cần ffmpeg. Không tìm thấy ffmpeg trong PATH "
                "hay cạnh file exe.\nHãy đặt ffmpeg.exe cạnh tool rồi chạy lại, "
                "hoặc chọn chế độ 'Từng câu riêng'.")
            return
        thu_muc_goc = self.e_luu.get().strip() or mac_dinh_thu_muc_luu_srt()
        ten_goc = os.path.splitext(os.path.basename(srt))[0]
        # (v7.0, phu luc 4) Moi thu cung 1 thu muc du an: MP3 long tieng
        # luu ngay trong thu muc chua file phu de, khong tao thu muc moi.
        thu_muc_moi = thu_muc_goc
        self._log("Xuất MP3 vào cùng thư mục dự án: %s" % thu_muc_moi)
        self.thu_muc_xuat = thu_muc_moi
        self._bat_dau_chung(srt, ffmpeg, thu_muc_ghi_de=thu_muc_moi)

    def _bat_dau_tiep_tuc(self):
        """Nut Tiep tuc: doc tiep tu cau chua xong va noi vao file cu
        (khong doc lai cac cau da xong, khong tao file moi). Chi sang
        khi co tien trinh dang do hop le."""
        if self.dang_chay:
            return
        tt = self._tien_trinh_hop_le()
        if not tt:
            messagebox.showinfo(
                APP_TITLE,
                "Không còn tiến trình dở dang nào khớp với file SRT và "
                "cài đặt hiện tại (có thể anh đã đổi file SRT, giọng, "
                "tốc độ, cao độ hoặc chế độ đầu ra).")
            self._cap_nhat_nut_tiep_tuc()
            return
        srt = self.e_srt.get().strip()
        ffmpeg = tim_ffmpeg()
        if tt["che_do"] in ("gop", "ca_hai") and not ffmpeg:
            messagebox.showwarning(
                APP_TITLE,
                "Chế độ gộp cần ffmpeg. Không tìm thấy ffmpeg trong PATH "
                "hay cạnh file exe.\nHãy đặt ffmpeg.exe cạnh tool rồi chạy lại, "
                "hoặc chọn chế độ 'Từng câu riêng'.")
            return
        # Dong bo giao dien theo cai dat da luu trong tien trinh (de cac
        # cau moi doc cung giong/toc do/cao do/che do voi cau cu).
        self.cb_giong.set(tt["giong"])
        # v1.3: toc_do luu dang he so nhan (1.35x).
        self.sl_toc_do.set(float(tt["toc_do"]))
        # v1.4: toc_do_toi_da + tu_dong_toc_do (mac dinh v1.3 cu).
        self.sl_toc_do_toi_da.set(
            max(1.0, min(2.0, float(tt.get("toc_do_toi_da", 1.35)))))
        self.var_tu_dong_toc_do.set(bool(tt.get("tu_dong_toc_do", True)))
        if self.var_tu_dong_toc_do.get():
            self.sl_toc_do_toi_da.configure(state="normal")
        else:
            self.sl_toc_do_toi_da.configure(state="disabled")
        self.sl_cao_do.set(int(tt["cao_do"]))
        self.che_do.set(tt["che_do"])
        self.lb_toc_do.configure(
            text=_dinh_dang_toc_do(float(tt["toc_do"])))
        self.lb_toc_do_toi_da.configure(
            text=_dinh_dang_toc_do(float(tt.get("toc_do_toi_da", 1.35))))
        self.lb_cao_do.configure(
            text=_dinh_dang_cao_do(int(tt["cao_do"])))
        self.thu_muc_xuat = tt["thu_muc"]
        self._log("Tiếp tục từ tiến trình đã lưu: đã xong %d/%d câu, đọc "
                  "tiếp từ câu chưa xong và nối vào file cũ."
                  % (len(tt["cau_da_xong"]), tt["tong_cau"]))
        self._bat_dau_chung(srt, ffmpeg, thu_muc_ghi_de=tt["thu_muc"],
                            cau_da_xong_truoc=set(tt["cau_da_xong"]),
                            toc_do_cau_truoc=tt.get("toc_do_cau") or {},
                            la_tiep_tuc=True)

    def _bat_dau_sub_lai(self):
        """Nut Sub lai tu dau: doc lai tu cau 1, tao file MP3 moi (thu
        muc moi ten (1), (2)... neu file cu da co - khong ghi de file
        cu)."""
        if self.dang_chay:
            return
        srt = self.e_srt.get().strip()
        if not srt or not os.path.isfile(_duong_dan_dai_win(srt)):
            messagebox.showwarning(STUDIO_TITLE, "Hãy chọn file SRT trước.")
            return
        if not self._tree_ids:
            if self._nap_danh_sach_cau(srt) is None:
                return
        ffmpeg = tim_ffmpeg()
        che_do = self.che_do.get()
        if che_do in ("gop", "ca_hai") and not ffmpeg:
            messagebox.showwarning(
                APP_TITLE,
                "Chế độ gộp cần ffmpeg. Không tìm thấy ffmpeg trong PATH "
                "hay cạnh file exe.\nHãy đặt ffmpeg.exe cạnh tool rồi chạy lại, "
                "hoặc chọn chế độ 'Từng câu riêng'.")
            return
        thu_muc_goc = self.e_luu.get().strip() or mac_dinh_thu_muc_luu_srt()
        ten_goc = os.path.splitext(os.path.basename(srt))[0]
        # (v7.0, phu luc 4) Sub lai van o cung thu muc du an.
        thu_muc_moi = thu_muc_goc
        self.thu_muc_xuat = thu_muc_moi
        self._log("Sub lại từ đầu trong cùng thư mục dự án: %s" % thu_muc_moi)
        self._bat_dau_chung(srt, ffmpeg, thu_muc_ghi_de=thu_muc_moi)

    def _bat_dau_chung(self, srt, ffmpeg, thu_muc_ghi_de=None,
                       cau_da_xong_truoc=None, la_tiep_tuc=False,
                       toc_do_cau_truoc=None):
        """Chuan bi chung truoc khi chay worker xuat (lay het gia tri
        giao dien o luong chinh, khoa nut, mo worker)."""
        self._luu_cai_dat_hien_tai()
        # Lay het gia tri giao dien o luong chinh, truyen sang luong worker
        # (luong worker khong doc truc tiep widget tkinter - khong an toan).
        ts = {
            "voice": GIONG.get(self.cb_giong.get(), GIONG[GIONG_MAC_DINH]),
            "giong_hien_thi": self.cb_giong.get(),
            # v1.3: toc_do la he so nhan (1.35x).
            "toc_do": float(self.sl_toc_do.get()),
            # v1.4: toc do toi da + bat/tat tu dong toc do tung cau.
            "toc_do_toi_da": float(self.sl_toc_do_toi_da.get()),
            "tu_dong_toc_do": bool(self.var_tu_dong_toc_do.get()),
            "cao_do": int(self.sl_cao_do.get()),
            "che_do": self.che_do.get(),
            "thu_muc_goc": self.e_luu.get().strip() or mac_dinh_thu_muc_luu_srt(),
        }
        self.dang_chay = True
        self._yeu_cau_huy.clear()
        # v1.3: khoa cac nut khac trong luc xuat (chi de nut Huy sang).
        # Neu dang nghe thu thi dung phat luon (tranh 2 viec cung goi
        # giong 1 luc).
        self._dung_nghe.set()
        self._khoa_nut_khi_chay(cho_huy=True)
        self.hang_doi.put(("ket_qua", ""))
        # (v7.7) Doi trang thai NGAY truoc khi mo luong worker: ban
        # cu de "Chưa chạy." cho toi khi doc xong cau 1 nen CYAN
        # tuong tool dung im; gio bam XUAT la thay "Đang khởi động..."
        # lien, neu luong chet thi cung co log loi chu khong im.
        self._tien_trinh(0, "Đang khởi động...")
        self._log("Đang khởi động xuất MP3...")
        threading.Thread(target=self._chay,
                         args=(srt, ffmpeg, ts, thu_muc_ghi_de,
                               cau_da_xong_truoc, la_tiep_tuc,
                               toc_do_cau_truoc),
                         daemon=True).start()

    def _chay(self, srt, ffmpeg, ts, thu_muc_ghi_de=None,
              cau_da_xong_truoc=None, la_tiep_tuc=False,
              toc_do_cau_truoc=None):
        """Luong worker xuat MP3 — chi la lop boc an toan quanh
        _chay_thuc. (v7.7) NGUYEN NHAN GOC LOI v7.5: _chay cu bat dau
        bang `from pydub import AudioSegment` KHONG co try/except;
        ban exe thieu pydub thi ImportError giet chet luong ngay tai
        do, khong log, khong queue ("xong",) nen UI dung mai o
        "Chưa chạy.", nut Huy cung vo dung. Tu nay moi exception
        trong worker deu duoc log ro + mo khoa nut + hop thoai loi,
        KHONG BAO GIO chet im nua."""
        try:
            self._chay_thuc(srt, ffmpeg, ts, thu_muc_ghi_de,
                            cau_da_xong_truoc, la_tiep_tuc,
                            toc_do_cau_truoc)
        except Exception as e:
            tb = traceback.format_exc()
            thu_muc_log = (getattr(self, "thu_muc_ket_qua", None)
                           or thu_muc_ghi_de
                           or ts.get("thu_muc_goc") or ".")
            try:
                _ghi_log_loi_ffmpeg(thu_muc_log,
                                    "LOI LUONG XUAT MP3 (chet dot ngot):\n"
                                    + tb)
            except Exception:
                pass
            loi_ngan = _tom_tat_loi(e)
            self._log("LỖI XUẤT MP3: luồng worker dừng đột ngột: %s "
                      "(chi tiết đã ghi vào ffmpeg-loi.log trong thư "
                      "mục kết quả)" % loi_ngan)
            self.hang_doi.put(("ket_qua", "LỖI XUẤT MP3: %s" % loi_ngan))
            self.hang_doi.put(("loi_hop_thoai",
                               "Xuất MP3 lồng tiếng bị lỗi:\n%s\n\n"
                               "Chi tiết đã ghi vào file ffmpeg-loi.log "
                               "trong thư mục kết quả — gửi file đó lại "
                               "để kiểm tra." % loi_ngan))
            self.hang_doi.put(("xong",))

    def _chay_thuc(self, srt, ffmpeg, ts, thu_muc_ghi_de=None,
                   cau_da_xong_truoc=None, la_tiep_tuc=False,
                   toc_do_cau_truoc=None):
        # (v7.7) KHONG con `from pydub import AudioSegment` o dau
        # ham nay — do la dong giet chet luong o v7.5. Doc giong,
        # do thoi luong, gop file deu dung edge-tts + ffmpeg/ffprobe.
        voice = ts["voice"]
        toc_do = ts["toc_do"]
        cao_do = ts["cao_do"]
        che_do = ts["che_do"]
        thu_muc_goc = ts["thu_muc_goc"]
        # v1.4: toc do toi da + bat/tat tu dong toc do tung cau.
        toc_do_toi_da = ts.get("toc_do_toi_da", 1.35)
        tu_dong_toc_do = ts.get("tu_dong_toc_do", True)
        ten_goc = os.path.splitext(os.path.basename(srt))[0]
        # v1.3: thu muc xuat co the duoc chi dinh truoc (Tiep tuc: dung
        # lai thu muc cu; Xuat moi/Sub lai: thu muc moi (1), (2)...).
        thu_muc = thu_muc_ghi_de or os.path.join(thu_muc_goc, ten_goc)
        thu_muc_rieng = os.path.join(thu_muc, "tung-cau")
        self.thu_muc_ket_qua = thu_muc
        self.file_gop = None
        # (v7.7) Canh bao duong dan dai Windows: thu muc phim + ten
        # file cua CYAN rat dai, gan/vuot 260 ky tu thi tao file co
        # the loi — bao truoc de doi ten ngan lai neu can.
        if sys.platform == "win32" and len(os.path.abspath(thu_muc)) > 240:
            self._log("Cảnh báo: đường dẫn thư mục kết quả rất dài "
                      "(%d ký tự), Windows giới hạn 260 ký tự — nếu "
                      "tạo file lỗi thì đổi tên thư mục phim ngắn lại."
                      % len(os.path.abspath(thu_muc)))
        try:
            os.makedirs(_duong_dan_dai_win(thu_muc_rieng), exist_ok=True)
        except OSError as e:
            self._log("Lỗi tạo thư mục: %s" % e)
            self.hang_doi.put(("xong",))
            return
        # v1.3: chay moi (khong phai Tiep tuc) thi xoa tien trinh cu cua
        # thu muc nay (lan chay moi thay the no).
        if not la_tiep_tuc:
            _xoa_tien_trinh(thu_muc)
        try:
            cac_cau = doc_srt(srt)
        except Exception as e:
            self._log("Lỗi đọc file SRT: %s" % e)
            self.hang_doi.put(("xong",))
            return
        if not cac_cau:
            self._log("Không tìm thấy câu phụ đề nào trong file SRT.")
            self.hang_doi.put(("xong",))
            return
        tong = len(cac_cau)
        self._log("Đọc %d câu bằng giọng %s (%s), tốc độ %s, cao độ %s"
                  % (tong, ts["giong_hien_thi"], voice,
                     _dinh_dang_toc_do(toc_do), _dinh_dang_cao_do(cao_do)))
        # v1.4: bao ro che do toc do tu dong dang dung (de anh biet cau
        # dai se tu tang toc toi da bao nhieu).
        if tu_dong_toc_do:
            if not ffmpeg:
                self._log("Tự động chỉnh tốc độ từng câu đang BẬT nhưng "
                          "không tìm thấy ffmpeg (cần ffmpeg để đo thời "
                          "lượng và tăng tốc) - các câu sẽ đọc ở tốc độ "
                          "cơ bản %s." % _dinh_dang_toc_do(toc_do))
            else:
                self._log("Tự động chỉnh tốc độ từng câu: câu dài tự "
                          "tăng tốc tối đa %s (đo thời lượng thật rồi "
                          "dùng ffmpeg atempo, không gọi lại API giọng)."
                          % _dinh_dang_toc_do(toc_do_toi_da))
        self._log("Thư mục lưu: %s" % thu_muc)
        for cau in cac_cau:
            self._dat_trang_thai_cau(cau["chi_so"], "Chờ")
        loi_cau = {}  # chi_so -> ly do loi
        can_gop = che_do in ("gop", "ca_hai")
        so_cau_xong = 0  # dem that, dung ca khi huy giua chung
        cau_da_xong = set()  # chi_so cac cau da doc xong
        # v1.4: toc do thuc tung cau da xong (de luu vao tien trinh va
        # hien lai trang thai "Xong (1.60x)" khi Tiep tuc).
        toc_do_cau = dict(toc_do_cau_truoc or {})
        da_huy = False
        cau_dung = 0  # chi so cau dang doc luc bam Huy
        # (v7.7) Gop o CUOI bang ffmpeg concat (khong con ghep dan
        # vao WAV tam): moi cau doc xong chi luu file MP3 rieng
        # trong tung-cau; huy giua chung hay loi giua chung thi cac
        # file cau da xong van con, bam Tiep tuc doc not roi gop.
        gop = None
        dich_gop = None
        if can_gop:
            dich_gop = os.path.join(thu_muc, ten_goc + "_long-tieng.mp3")
            gop = GopDan(
                dich_gop,
                tong_ms=max(c["ket_thuc_ms"] for c in cac_cau),
                log_cb=self._log, ffmpeg=ffmpeg,
                thu_muc=thu_muc_rieng)
            self._log("Gộp cuối bằng ffmpeg concat: mỗi câu đọc xong "
                      "lưu file MP3 riêng trong tung-cau, xong hết mới "
                      "gộp thành 1 file lồng tiếng (đúng timestamp "
                      "SRT). Vì API giọng Microsoft chỉ nhận 1 đoạn "
                      "văn mỗi lần gọi nên tool phải đọc từng câu "
                      "riêng rồi mới ghép lại thành 1 file duy nhất - "
                      "không gọi 1 lần cho cả %d câu được." % tong)
        # v1.3 - TIEP TUC: cac cau da xong o lan truoc thi danh dau Xong
        # va noi lai vao file gop (doc lai file MP3 tung cau da co,
        # khong goi lai API giong). Cau nao file bi hong thi doc lai.
        if la_tiep_tuc and cau_da_xong_truoc:
            cau_hong = set()
            for cau in cac_cau:
                if cau["chi_so"] in cau_da_xong_truoc:
                    dich_cu = os.path.join(
                        thu_muc_rieng, "%03d.mp3" % cau["chi_so"])
                    if (gop is not None
                            and not gop.them_cau(cau, dich_cu)):
                        cau_hong.add(cau["chi_so"])
                        continue
                    cau_da_xong.add(cau["chi_so"])
                    so_cau_xong += 1
                    # v1.4: hien lai toc do thuc cua cau da xong (neu co
                    # luu trong tien trinh).
                    toc_do_cu = toc_do_cau.get(cau["chi_so"])
                    if tu_dong_toc_do and toc_do_cu is not None:
                        self._dat_trang_thai_cau(
                            cau["chi_so"], "Xong (%.2fx)" % toc_do_cu)
                    else:
                        self._dat_trang_thai_cau(cau["chi_so"], "Xong")
            if cau_hong:
                self._log("Có %d câu đã xong nhưng file bị hỏng, sẽ đọc "
                          "lại: %s" % (len(cau_hong), sorted(cau_hong)))
            self._log("Đã nối lại %d câu đã xong vào file gộp."
                      % len(cau_da_xong))

        def doc_1_cau(cau, i):
            """Doc 1 cau, cap nhat tien trinh + trang thai trong danh sach.
            Cau xong thi GHEP NGAY vao file gop (neu che do gop).
            Tra ve True neu xong."""
            nonlocal so_cau_xong
            dich = os.path.join(thu_muc_rieng, "%03d.mp3" % cau["chi_so"])
            self._tien_trinh(int((i - 1) * 100 / tong),
                             "Đang đọc câu %d/%d..." % (i, tong))
            self._dat_trang_thai_cau(cau["chi_so"], "Đang đọc...")
            self._log("Câu %d/%d (%.1fs): %s" % (
                i, tong, (cau["ket_thuc_ms"] - cau["bat_dau_ms"]) / 1000.0,
                cau["text"][:80]))
            # (v7.7) Truyen co Huy + timeout giong: nut Huy dung duoc
            # ngay ca khi dang cho giong, het 120s thi failover luot
            # sau thay vi treo vo han o cau nay.
            ok, bo_xac_minh, loi = doc_cau_thanh_mp3(
                cau["text"], voice, toc_do, cao_do, dich,
                log_cb=self._log, ffmpeg=ffmpeg,
                timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                dung=self._yeu_cau_huy)
            if not ok:
                if self._yeu_cau_huy.is_set():
                    # Huy giua cau dang doc: khong ghi "LỖI câu" nua,
                    # vong lap chinh se dung va bao "Đã hủy".
                    return False
                self._dat_trang_thai_cau(cau["chi_so"], "Lỗi: " + (loi or "?")[:60])
                self._log("  -> LỖI câu %d: %s" % (cau["chi_so"], loi))
                return False
            # v1.4: toc do tu dong theo slot SRT - do thoi luong that
            # cua file vua tao roi dung ffmpeg atempo tang toc neu can
            # (khong goi lai API giong). Trang thai hien toc do thuc
            # cua cau (vd "Xong (1.60x)").
            toc_do_thuc = _ap_dung_toc_do_tu_dong(
                dich, cau, toc_do, toc_do_toi_da, tu_dong_toc_do, ffmpeg,
                log_cb=self._log)
            toc_do_cau[cau["chi_so"]] = toc_do_thuc
            so_cau_xong += 1
            cau_da_xong.add(cau["chi_so"])
            if tu_dong_toc_do:
                self._dat_trang_thai_cau(cau["chi_so"],
                                         "Xong (%.2fx)" % toc_do_thuc)
            else:
                self._dat_trang_thai_cau(cau["chi_so"], "Xong")
            if bo_xac_minh:
                self._log("  -> Xong (đã dùng chế độ bỏ xác minh SSL)")
            # v1.3: ghep ngay cau vua xong vao file long tieng.
            if gop is not None:
                gop.them_cau(cau, dich)
            return True

        # Luot 1: doc het cac cau (dung ngay khi bam Huy). Cau nao da
        # xong o lan truoc (Tiep tuc) thi bo qua, khong doc lai.
        for i, cau in enumerate(cac_cau, 1):
            if self._yeu_cau_huy.is_set():
                da_huy = True
                cau_dung = i
                break
            if cau["chi_so"] in cau_da_xong:
                continue
            if not doc_1_cau(cau, i):
                loi_cau[cau["chi_so"]] = True
        # Luot 2: cau nao loi thi THU LAI 1 lan nua (loi mang thoang qua),
        # ghi ro ket qua tung cau, khong lang le bo qua. Bo qua neu da huy.
        if loi_cau and not da_huy:
            self._log("Thử lại %d câu lỗi: %s" % (len(loi_cau),
                                                  sorted(loi_cau)))
            for i, cau in enumerate(cac_cau, 1):
                if self._yeu_cau_huy.is_set():
                    da_huy = True
                    cau_dung = i
                    break
                if cau["chi_so"] not in loi_cau:
                    continue
                self._log("Đọc lại câu %d..." % cau["chi_so"])
                if doc_1_cau(cau, i):
                    del loi_cau[cau["chi_so"]]
                    self._log("  -> Câu %d đọc lại THÀNH CÔNG." % cau["chi_so"])
                else:
                    self._log("  -> Câu %d vẫn lỗi sau khi thử lại." % cau["chi_so"])
        so_xong = so_cau_xong
        if da_huy:
            self._tien_trinh(int(so_xong * 100 / tong),
                             "Đã hủy ở câu %d/%d." % (cau_dung, tong))
            self._log("Đã hủy ở câu %d/%d. Đã xong %d câu, giữ nguyên file "
                      "các câu đã xong trong %s."
                      % (cau_dung, tong, so_xong, thu_muc_rieng))
        else:
            self._tien_trinh(100, "Đã đọc xong %d/%d câu." % (so_xong, tong))
        if loi_cau:
            self._log("Cảnh báo: %d câu vẫn lỗi sau 2 lượt: %s"
                      % (len(loi_cau), sorted(loi_cau)))
            # v1.3: cau loi khong co audio - slot cua no giu khoang lang
            # trong file gop, khong lam hong file gop.
            for chi_so in sorted(loi_cau):
                self._log("Đã bỏ qua câu %d (không có audio) - slot của "
                          "nó giữ khoảng lặng trong file gộp." % chi_so)
        # (v7.7) HOAN TAT file gop: gop cac file MP3 tung cau bang
        # ffmpeg concat (dung moc gio SRT). Chi ghi 1 dong loi ngan
        # ra giao dien khi gap su co; log chi tiet ffmpeg chi ghi
        # vao file ffmpeg-loi.log trong thu muc ket qua (khong hien
        # tab log dai nhay lien tuc len man hinh).
        tong_ms_gop = 0
        if can_gop and gop is not None and gop.so_cau > 0:
            self._log("Đang hoàn tất file lồng tiếng: %s" % dich_gop)
            try:
                ok_gop, tong_ms_gop = gop.hoan_tat(
                    ffmpeg, dung=self._yeu_cau_huy)
                if ok_gop:
                    self.file_gop = dich_gop
                    self._log("XONG file gộp: %s (dài %.1fs, %d câu bị "
                              "tràn slot, %d câu lỗi đã bỏ qua)"
                              % (dich_gop, tong_ms_gop / 1000.0,
                                 gop.tran_slot, gop.bo_qua))
                else:
                    self._log("LỖI hoàn tất file gộp (xem chi tiết trong "
                              "file ffmpeg-loi.log ở thư mục kết quả).")
                    _ghi_log_loi_ffmpeg(thu_muc, "hoan_tat tra ve False")
            except Exception as e:
                _ghi_log_loi_ffmpeg(thu_muc, traceback.format_exc())
                self._log("LỖI hoàn tất file gộp: %s (xem chi tiết trong "
                          "file ffmpeg-loi.log ở thư mục kết quả)"
                          % _tom_tat_loi(e))
        elif can_gop:
            self._log("Không có câu nào đọc xong nên không tạo file gộp.")
        # v1.3 - LUU/XOA tien trinh: con cau chua xong (huy giua chung
        # hoac loi) thi luu de bam 'Tiep tuc' doc not; xong tron ven
        # 100% thi xoa (khong con gi de tiep tuc).
        if 0 < so_xong < tong:
            try:
                st = os.stat(_duong_dan_dai_win(srt))
                _luu_tien_trinh(thu_muc, {
                    "srt": srt,
                    "srt_kich_thuoc": st.st_size,
                    "srt_mtime": int(st.st_mtime),
                    "tong_cau": tong,
                    "cau_da_xong": sorted(cau_da_xong),
                    "file_gop": dich_gop,
                    "che_do": che_do,
                    "giong": ts["giong_hien_thi"],
                    "toc_do": float(toc_do),
                    # v1.4: toc do toi da + bat/tat tu dong + toc do thuc
                    # tung cau da xong (de Tiep tuc noi dung toc do).
                    "toc_do_toi_da": float(toc_do_toi_da),
                    "tu_dong_toc_do": bool(tu_dong_toc_do),
                    "toc_do_cau": {str(k): float(v)
                                   for k, v in toc_do_cau.items()},
                    "cao_do": int(cao_do),
                    "thu_muc": thu_muc,
                    "thu_muc_rieng": thu_muc_rieng,
                })
                self._log("Đã lưu tiến trình (xong %d/%d câu) - bấm "
                          "'Tiếp tục' để đọc nốt các câu còn lại."
                          % (so_xong, tong))
            except Exception:
                pass
        else:
            _xoa_tien_trinh(thu_muc)
        # Bao ro ket qua: duong dan + do dai file MP3 long tieng.
        if dich_gop and os.path.isfile(dich_gop):
            if da_huy:
                ket_qua = ("ĐÃ HỦY ở câu %d/%d. Đã xong %d/%d câu. File MP3 "
                           "lồng tiếng (dang dở, chỉ có các câu đã xong):"
                           "\n%s\nĐộ dài: %.1f giây."
                           % (cau_dung, tong, so_xong, tong,
                              dich_gop, tong_ms_gop / 1000.0))
            else:
                ket_qua = ("HOÀN TẤT: %d/%d câu. File MP3 lồng tiếng:\n%s\n"
                           "Độ dài: %.1f giây."
                           % (so_xong, tong, dich_gop, tong_ms_gop / 1000.0))
            if loi_cau:
                ket_qua += " (còn %d câu lỗi: %s)" % (len(loi_cau),
                                                      sorted(loi_cau))
            self.hang_doi.put(("ket_qua", ket_qua))
            self._log(ket_qua)
        elif che_do == "rieng":
            if da_huy:
                ket_qua = ("ĐÃ HỦY ở câu %d/%d. Đã xong %d/%d câu. File "
                           "từng câu đã xong nằm trong:\n%s"
                           % (cau_dung, tong, so_xong, tong, thu_muc_rieng))
            else:
                ket_qua = ("HOÀN TẤT: %d/%d câu. File từng câu nằm trong:\n%s"
                           % (so_xong, tong, thu_muc_rieng))
            self.hang_doi.put(("ket_qua", ket_qua))
            self._log(ket_qua)
        elif da_huy:
            ket_qua = ("ĐÃ HỦY ở câu %d/%d. Chưa xong câu nào."
                       % (cau_dung, tong))
            self.hang_doi.put(("ket_qua", ket_qua))
            self._log(ket_qua)
        self._log("Thư mục kết quả: %s (bấm 'Mở thư mục kết quả' để xem)"
                  % thu_muc)
        self.hang_doi.put(("xong",))
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
        # (v7.0) Phu de: None = chua quet, True/False = ket qua --list-subs.
        self.has_subtitle = job.get("has_subtitle")
        self.subtitle_langs = job.get("subtitle_langs") or []
        self.subtitle_file = job.get("subtitle_file") or ""
        self.subtitle_vi_file = job.get("subtitle_vi_file") or ""
        self.thu_muc_phim = job.get("folder") or ""
        self.tu_gop_var = tk.BooleanVar(value=job.get("tu_gop", True))
        self.xoa_goc_var = tk.BooleanVar(value=job.get("xoa_goc", True))
        # (v7.2) Tu giam tieng nen khi co loi: mac dinh BAT. Co file
        # MP3 giong Viet trong thu muc du an thi tron bang FFmpeg
        # sidechaincompress; chua co giong thi chi giam co dinh 15%.
        # Khong gioi han thoi luong. Khong dung AI tach giong.
        self.tu_giam_tieng_nen_var = tk.BooleanVar(
            value=job.get("tu_giam_tieng_nen", True))
        # (v7.3) NGUYEN TAC CYAN 19/11 04:56 - moi buoc tu dong deu
        # phai co cong tac bat/tat rieng, tat la bo qua han buoc do,
        # luu theo tung job. Mac dinh BAT het (giu hanh vi cu).
        self.giam_15_var = tk.BooleanVar(value=job.get("giam_15", True))
        self.tu_gop_ytdlp_var = tk.BooleanVar(
            value=job.get("tu_gop_ytdlp", True))
        self.dich_ten_var = tk.BooleanVar(value=job.get("dich_ten", True))
        self.tu_nhan_dien_var = tk.BooleanVar(
            value=job.get("tu_nhan_dien", True))
        # (v7.5) Tu dich sau khi lay phu de (luong 1 mach): MAC DINH
        # TAT, vi CYAN dich bang AI ben ngoai; chi bat moi tu dich.
        self.tu_dich_sau_lay_phu_de_var = tk.BooleanVar(
            value=job.get("tu_dich_sau_lay_phu_de", False))

        ten = job.get("title") or "Video mới"
        self.title("%s - %s" % (STUDIO_TITLE, ten[:60]))
        self.geometry("700x860")
        self.resizable(True, True)

        pad = {"padx": 8, "pady": 4}

        # ---- Khung 1: Tải video từ Bilibili ----
        f1 = tk.LabelFrame(self, text=" 1. Tải video từ Bilibili ", padx=8, pady=6)
        f1.grid(row=0, column=0, columnspan=3, sticky="ew", **pad)
        f1.grid_columnconfigure(1, weight=1)

        tk.Label(f1, text="Link phim:").grid(row=0, column=0, sticky="w", **pad)
        self.ent_link = tk.Entry(f1, textvariable=self.link_var)
        self.ent_link.grid(row=0, column=1, sticky="ew", **pad)
        # (v6.4) Nút Dán: dán link Bilibili từ clipboard vào ô Link phim.
        self.btn_dan = tk.Button(f1, text="Dán",
                                 command=self.bam_dan_link)
        self.btn_dan.grid(row=0, column=2, **pad)
        self.btn_kiem_tra = tk.Button(f1, text="Kiểm tra link",
                                      command=self.bam_kiem_tra)
        self.btn_kiem_tra.grid(row=0, column=3, **pad)

        self.info_var = tk.StringVar(value="Dán link Bilibili (BV...) rồi bấm Kiểm tra link.")
        if job.get("title"):
            self.info_var.set("Tiêu đề: %s" % job["title"])
        tk.Label(f1, textvariable=self.info_var, fg="gray", wraplength=640,
                 justify="left").grid(row=1, column=0, columnspan=4,
                                      sticky="w", **pad)

        tk.Label(f1, text="Chất lượng:").grid(row=2, column=0, sticky="w", **pad)
        self.cbo_chat_luong = ttk.Combobox(f1, textvariable=self.chat_luong_var,
                                           state="readonly", width=12)
        self.cbo_chat_luong.grid(row=2, column=1, sticky="w", **pad)
        self.btn_tai = tk.Button(f1, text="TẢI XUỐNG + GỘP LUÔN (yt-dlp)",
                                 command=self.bam_tai, state="disabled")
        self.btn_tai.grid(row=2, column=2, columnspan=2, **pad)

        self.btn_idm = tk.Button(f1, text="TẢI BẰNG IDM (nhanh, nhiều luồng)",
                                 command=self.bam_idm, state="disabled")
        self.btn_idm.grid(row=3, column=0, columnspan=4, sticky="ew", **pad)

        # (v7.3) O "Tai xong tu gop luon (IDM)" (tu_gop_var, co tu
        # v6.8, mac dinh BAT, luu theo tung job) dat RO NGAY DUOI
        # nut TAI BANG IDM cho de thay, khong de o cuoi khung lan
        # voi phan yt-dlp. Bo tich: IDM tai xong chi nhan dien 2
        # file vao muc 2, KHONG tu gop, de cau xu ly audio / gop tay
        # trong CapCut sau. Tich: giu hanh vi tu gop nhu cu.
        self.chk_tu_gop = tk.Checkbutton(
            f1, text="Tải xong tự gộp luôn (IDM)",
            variable=self.tu_gop_var,
            command=self.luu_job_hien_tai)
        self.chk_tu_gop.grid(row=4, column=0, columnspan=4, sticky="w",
                             **pad)
        tk.Label(f1, text="File cookies.txt (để tải 1080p):").grid(
            row=5, column=0, sticky="w", **pad)
        tk.Entry(f1, textvariable=self.cookies_var).grid(
            row=5, column=1, sticky="ew", **pad)
        tk.Button(f1, text="Chọn...",
                  command=self.chon_cookies).grid(row=5, column=2,
                                                  columnspan=2, **pad)
        tk.Label(f1, text="Không có cookies thì thường chỉ tải được 480p.",
                 fg="gray").grid(row=6, column=0, columnspan=4, sticky="w", **pad)
        tk.Label(f1, text="% tải (IDM):").grid(row=7, column=0, sticky="w", **pad)
        self.tien_trinh_idm = ttk.Progressbar(f1, mode="determinate",
                                              maximum=100)
        self.tien_trinh_idm.grid(row=7, column=1, sticky="ew", **pad)
        self.phan_tram_var = tk.StringVar(value="")
        tk.Label(f1, textvariable=self.phan_tram_var, fg="gray").grid(
            row=7, column=2, columnspan=2, sticky="w", **pad)
        # (v7.0) Phu de: checkbox tick = co phu de (theo yt-dlp
        # --list-subs), khong tick = khong co. Khong dung nut phu de
        # tren trinh phat web lam can cu.
        self.phu_de_var = tk.BooleanVar(value=bool(self.has_subtitle))
        tk.Checkbutton(f1, text="Phụ đề", variable=self.phu_de_var,
                       state="disabled").grid(row=8, column=0, sticky="w", **pad)
        self.phu_de_info_var = tk.StringVar(value=self._nhan_phu_de())
        tk.Label(f1, textvariable=self.phu_de_info_var, fg="gray").grid(
            row=8, column=1, sticky="w", **pad)
        tk.Button(f1, text="Tải phụ đề", command=self.bam_tai_phu_de).grid(
            row=8, column=2, **pad)
        tk.Button(f1, text="Thêm phụ đề...", command=self.bam_them_phu_de).grid(
            row=8, column=3, **pad)
        tk.Button(f1, text="Dịch phụ đề", command=self.bam_dich_phu_de).grid(
            row=9, column=0, columnspan=4, sticky="ew", **pad)

        # ---- (v7.3) Khung: Các bước tự động - NGUYEN TAC CYAN 19/11
        # 04:56: moi buoc tu dong deu phai co cong tac bat/tat rieng,
        # tat la bo qua han buoc do. CapCut da xu ly tach giong +
        # chinh lon nho roi, tool chi de audio SRT len thoi - neu
        # tool tu lam het cac buoc do thi se trung, khong duoc.
        # O "Tai xong tu gop luon (IDM)" vua o ngay duoi nut TAI BANG
        # IDM o tren (de thay khi tai IDM) vua co mat o day (cung 1
        # bien tu_gop_var, tich/bỏ o cho nao cung dong bo).
        f_auto = tk.LabelFrame(
            self, text=" Các bước tự động (tắt là bỏ qua bước đó) ",
            padx=8, pady=6)
        f_auto.grid(row=1, column=0, columnspan=3, sticky="ew", **pad)
        tk.Checkbutton(f_auto, text="Tải xong tự gộp luôn (IDM)",
                       variable=self.tu_gop_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Tải yt-dlp xong tự gộp luôn",
                       variable=self.tu_gop_ytdlp_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Tự dịch tên phim sang tiếng Việt",
                       variable=self.dich_ten_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Giảm tiếng gốc xuống 15%",
                       variable=self.giam_15_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(
            f_auto, text="Tự giảm tiếng nền khi có lời (FFmpeg sidechain)",
            variable=self.tu_giam_tieng_nen_var,
            command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Gộp xong tự xóa 2 file gốc",
                       variable=self.xoa_goc_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Tự nhận diện 2 file sau khi tải",
                       variable=self.tu_nhan_dien_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Checkbutton(f_auto, text="Tự dịch sau khi lấy phụ đề (luồng 1 mạch) — mặc định TẮT",
                       variable=self.tu_dich_sau_lay_phu_de_var,
                       command=self.luu_job_hien_tai).pack(anchor="w")
        tk.Label(f_auto, text="Tắt ô nào là bỏ qua hẳn bước đó. CapCut đã xử lý tách giọng + chỉnh lớn nhỏ rồi — tool chỉ đè audio SRT lên thôi.",
                 fg="gray", wraplength=640, justify="left").pack(anchor="w")

        # ---- Khung 2: Gộp 2 file đã có ----
        f2 = tk.LabelFrame(self, text=" 2. Gộp 2 file đã có (tải bằng IDM) ",
                           padx=8, pady=6)
        f2.grid(row=2, column=0, columnspan=3, sticky="ew", **pad)
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
        # (v7.3) Cac o tich buoc tu dong (xoa file goc, tu giam tieng
        # nen sidechain) da doi vao khung "Cac buoc tu dong" o tren,
        # khong de rieng o khung 2 nua - de cau bat/tat 1 cho duy nhat.
        self.btn_gop_long = tk.Button(
            f2, text="GỘP VỚI LỒNG TIẾNG VIỆT (giảm tiếng gốc 15%)",
            font=("", 11, "bold"), command=self.bam_gop_voi_long_tieng)
        self.btn_gop_long.grid(row=5, column=0, columnspan=3, sticky="ew", **pad)
        self.btn_tron = tk.Button(
            f2, text="TRỘN TIẾNG NỀN + LỒNG TIẾNG (tự giảm khi có lời)",
            font=("", 11, "bold"), command=self.bam_tron_tieng_nen)
        self.btn_tron.grid(row=6, column=0, columnspan=3, sticky="ew", **pad)

        # (v7.3) XUAT 2 FILE AUDIO RIENG CHO CAPCUT - luong long tieng
        # CYAN chot 19/11 04:53: cau tu tach nen / bo giong o CapCut,
        # tool chi xuat file nen (giam 15%) + file giong Viet HoaiMy
        # tu SRT, de cau import vao CapCut. KHONG gop video o day;
        # gop video trong tool (nut Gop / Tron o tren) la tuy chon
        # rieng, khong bat buoc trong luong nay.
        self.btn_xuat_audio = tk.Button(
            f2, text="XUẤT 2 FILE AUDIO RIÊNG (cho CapCut)",
            font=("", 11, "bold"), command=self.bam_xuat_audio_capcut)
        self.btn_xuat_audio.grid(row=7, column=0, columnspan=3,
                                 sticky="ew", **pad)
        tk.Label(f2, text="Cậu tự tách nền / bỏ giọng ở CapCut; tool chỉ xuất file nền (giảm 15%) + file giọng Việt để cậu import vào CapCut. Gộp video trong tool là tùy chọn riêng.",
                 fg="gray", wraplength=640, justify="left").grid(
            row=8, column=0, columnspan=3, sticky="w", **pad)

        self.btn_xem = tk.Button(f2, text="XEM THÀNH QUẢ",
                                 font=("", 11, "bold"),
                                 command=self.bam_xem,
                                 state="normal" if self.thanh_qua else "disabled")
        self.btn_xem.grid(row=9, column=0, columnspan=3, sticky="ew", **pad)

        # ---- Thư mục lưu ----
        tk.Label(self, text="Thư mục lưu:").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.outdir_var).grid(
            row=3, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...",
                  command=self.chon_thu_muc_luu).grid(row=3, column=2, **pad)
        tk.Label(self, text="Video hoàn thiện lưu vào "
                 "<thư mục lưu>\\<tên video>\\<tên video>.mp4",
                 fg="gray").grid(row=4, column=0, columnspan=3, sticky="w", **pad)

        # ---- Log + trạng thái ----
        self.log = scrolledtext.ScrolledText(self, height=12, state="disabled")
        self.log.grid(row=5, column=0, columnspan=3, sticky="nsew", **pad)
        tk.Label(self, textvariable=self.status_var, fg="gray",
                 anchor="w").grid(row=6, column=0, columnspan=3, sticky="ew", **pad)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)
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
            self.job["has_subtitle"] = self.has_subtitle
            self.job["subtitle_langs"] = list(self.subtitle_langs or [])
            self.job["subtitle_file"] = self.subtitle_file or ""
            self.job["subtitle_vi_file"] = self.subtitle_vi_file or ""
            if getattr(self, "thu_muc_phim", ""):
                self.job["folder"] = self.thu_muc_phim
            self.job["tu_gop"] = bool(self.tu_gop_var.get())
            self.job["xoa_goc"] = bool(self.xoa_goc_var.get())
            self.job["tu_giam_tieng_nen"] = bool(self.tu_giam_tieng_nen_var.get())
            # (v7.3) Luu trang thai cac cong tac buoc tu dong theo job.
            self.job["giam_15"] = bool(self.giam_15_var.get())
            self.job["tu_gop_ytdlp"] = bool(self.tu_gop_ytdlp_var.get())
            self.job["dich_ten"] = bool(self.dich_ten_var.get())
            self.job["tu_nhan_dien"] = bool(self.tu_nhan_dien_var.get())
            self.job["tu_dich_sau_lay_phu_de"] = bool(
                self.tu_dich_sau_lay_phu_de_var.get())
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

    def _nhan_phu_de(self):
        """Nhan cot phu de: Co (ngon ngu) / Khong co / chua quet (trong)."""
        if self.has_subtitle is None:
            return "Chưa kiểm tra phụ đề."
        if self.has_subtitle:
            langs = ", ".join(self.subtitle_langs or [])
            ten = os.path.basename(self.subtitle_file) if self.subtitle_file else ""
            return "Có phụ đề%s%s" % (
                (" (%s)" % langs) if langs else "",
                (" - " + ten) if ten else "")
        return "Không có phụ đề."

    def _cap_nhat_phu_de_ui(self):
        try:
            self.phu_de_var.set(bool(self.has_subtitle))
            self.phu_de_info_var.set(self._nhan_phu_de())
        except Exception:
            pass

    def bam_tai_phu_de(self):
        """Tai phu de ve CUNG thu muc phim (luong ngam).
        (v7.6, loi CYAN 19/11 06:28) Neu job chua co thu muc phim
        thi TAO thu muc con theo ten phim TRUOC khi tai — khong de
        .srt roi thang vao thu muc goc (outdir)."""
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        ten_viet = self.job.get("title") or ten_phim_tu_ten_file(self.video_var.get().strip(), dich=self.dich_ten_var.get()) if self.video_var.get().strip() else (self.job.get("title") or "video")
        folder_cu = getattr(self, "thu_muc_phim", "")
        if folder_cu:
            folder = folder_cu
        else:
            outdir = self.outdir_var.get().strip()
            if not outdir:
                messagebox.showerror("Thiếu thư mục", "Chưa chọn thư mục lưu.")
                return
            folder = tao_thu_muc_duy_nhat(outdir, ten_viet)
            self.thu_muc_phim = folder
            self.job["folder"] = folder
            self.luu_job_hien_tai()
            self.ghi_log("Đã tạo thư mục phim: " + folder)
        threading.Thread(target=self._tai_phu_de_worker,
                         args=(self.link_var.get().strip(), folder, ten_viet,
                               self.cookies_var.get().strip()),
                         daemon=True).start()

    def _tai_phu_de_worker(self, url, folder, ten_viet, cookies):
        try:
            p = tai_phu_de(url, folder, ten_viet, cookies, self.log_threadsafe,
                           langs_da_dung=getattr(self, "subtitle_langs", None))
            self.after_an_toan(0, self._tai_phu_de_xong, p)
        except Exception as e:
            self.after_an_toan(0, self._tai_phu_de_loi, str(e))

    def _tai_phu_de_xong(self, path):
        if path:
            self.subtitle_file = path
            self.has_subtitle = True
            if not self.subtitle_langs:
                self.subtitle_langs = ["zh"]
            self._cap_nhat_phu_de_ui()
            self.ghi_log("Đã tải phụ đề: " + path)
            self.luu_job_hien_tai()
            messagebox.showinfo("Đã tải phụ đề", "File phụ đề:\n" + path)
        else:
            self.has_subtitle = False
            self._cap_nhat_phu_de_ui()
            self.luu_job_hien_tai()
            messagebox.showinfo("Không có phụ đề",
                                "Video này không có phụ đề để tải.\nBấm 'Thêm phụ đề...' để tự import file .srt ngoài vào.")

    def _tai_phu_de_loi(self, msg):
        self.ghi_log("TẢI PHỤ ĐỀ LỖI: " + msg)
        messagebox.showerror("Tải phụ đề lỗi", msg)

    def bam_them_phu_de(self):
        """(v7.0, phu luc 1) Them phu de thu cong: chon file .srt ngoai,
        luu duong dan vao job (khong copy, khong ghi de file goc), cap
        nhat cot Phu de thanh Co + ten file, roi mo tab Xu ly phu de
        voi file do da nap san."""
        p = them_phu_de_tu_ngoai(self.job, self)
        if not p:
            return
        self.subtitle_file = p
        self.has_subtitle = True
        self._cap_nhat_phu_de_ui()
        self.ghi_log("Đã thêm phụ đề ngoài: " + p)
        self.luu_job_hien_tai()
        try:
            self.quan_ly.mo_tab_xu_ly_phu_de(srt_path=p, job=self.job)
        except Exception as e:
            messagebox.showinfo("Đã thêm phụ đề", "File: %s\n(Không mở được tab Xử lý phụ đề: %s)" % (p, e))

    def bam_dich_phu_de(self):
        """Mo tab Xu ly phu de voi file phu de cua job nay (neu co)."""
        p = self.subtitle_file or ""
        if p and not os.path.isfile(p):
            p = ""
        try:
            self.quan_ly.mo_tab_xu_ly_phu_de(srt_path=p or None, job=self.job)
        except Exception as e:
            messagebox.showerror("Không mở được tab", str(e))

    def bam_dan_link(self):
        """(v6.4) Dán link Bilibili từ clipboard vào ô Link phim."""
        try:
            text = self.clipboard_get().strip()
        except tk.TclError:
            text = ""
        if not text:
            messagebox.showinfo(
                "Clipboard trống",
                "Chưa có gì trong clipboard để dán.\n"
                "Copy link Bilibili trước đã.")
            return
        # Clipboard có thể có thêm chữ khác: tách lấy URL đầu tiên nếu có.
        tim_url = re.search(r"https?://\S+", text)
        url = tim_url.group(0).strip() if tim_url else text.splitlines()[0].strip()
        self.link_var.set(url)
        self.info_var.set("Đã dán link, bấm Kiểm tra link để đọc thông tin.")
        self.ghi_log("Đã dán link từ clipboard.")
        try:
            self.ent_link.focus_set()
            self.ent_link.icursor(tk.END)
        except Exception:
            pass
        self.luu_job_hien_tai()

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
            # (v7.0) Kiem tra phu de bang yt-dlp --list-subs (nguon that),
            # khong dung nut phu de tren trinh phat web. Loi thi de trong.
            try:
                pd = kiem_tra_phu_de(url, self.cookies_var.get().strip())
                info["has_subtitle"] = pd.get("has_subtitle", False)
                info["subtitle_langs"] = pd.get("languages", [])
            except Exception:
                info["has_subtitle"] = False
                info["subtitle_langs"] = []
            self.after_an_toan(0, self._kiem_tra_xong, info)
        except Exception as e:
            self.after_an_toan(0, self._kiem_tra_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_kiem_tra.config(state="normal"))

    def _kiem_tra_xong(self, info):
        self.link_info = info
        self.has_subtitle = info.get("has_subtitle", False)
        self.subtitle_langs = info.get("subtitle_langs", []) or []
        self._cap_nhat_phu_de_ui()
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
                                          self.status_threadsafe,
                                          dich_ten=self.dich_ten_var.get(),
                                          tu_gop=self.tu_gop_ytdlp_var.get())
            self.after_an_toan(0, self._tai_xong, out_path, folder)
        except Exception as e:
            self.after_an_toan(0, self._tai_loi, str(e))
        finally:
            self.after_an_toan(
                0, lambda: self.btn_tai.config(state="normal"))

    def _tai_xong(self, out_path, folder):
        # (v7.3) out_path=None = chi tai rieng video + audio (o tu gop
        # yt-dlp dang TAT): nhan dien 2 file vao muc 2, KHONG tu gop,
        # de cau xu ly / gop tay trong CapCut sau.
        if out_path is None:
            ten_viet = os.path.basename(folder.rstrip(os.sep))
            self.job["title"] = ten_viet
            if self.link_info:
                self.link_info["title"] = ten_viet
            self.title("%s - %s" % (STUDIO_TITLE, ten_viet[:60]))
            self.info_var.set("Tiêu đề: %s" % ten_viet)
            self.thu_muc_phim = folder
            self.status_var.set("Tải xong (chỉ tải riêng, chưa gộp).")
            self.ghi_log("TẢI XONG (CHỈ TẢI RIÊNG, KHÔNG TỰ GỘP - ô "
                         "'Tải yt-dlp xong tự gộp luôn' đang BỎ tích): "
                         + folder)
            try:
                video, audio = nhan_dien_cap(
                    folder, self.ffmpeg or tim_ffmpeg())
                self.video_var.set(os.path.join(folder, video))
                self.audio_var.set(os.path.join(folder, audio))
                self.ghi_log("Đã nhận diện 2 file: %s + %s"
                             % (video, audio))
            except Exception as e:
                self.ghi_log("Chưa nhận diện được cặp file trong thư "
                             "mục, chọn tay ở mục 2: %s" % e)
            self.luu_job_hien_tai(status="cho_gop", pct_tai=100)
            messagebox.showinfo(
                "Tải xong rồi!",
                "Đã tải xong 2 file riêng vào:\n%s\n\nÔ 'Tải yt-dlp "
                "xong tự gộp luôn' đang BỎ tích nên tool KHÔNG tự "
                "gộp - để cậu xử lý audio / gộp tay trong CapCut "
                "sau, hoặc bấm GỘP VIDEO ở mục 2 để gộp lại."
                % folder)
            return
        # (v6.8) Tên phim tiếng Việt = tên file thành phẩm, hiển thị rõ
        # trong tool rồi mới báo hoàn thành.
        ten_viet = os.path.splitext(os.path.basename(out_path))[0]
        self.job["title"] = ten_viet
        if self.link_info:
            self.link_info["title"] = ten_viet
        self.title("%s - %s" % (STUDIO_TITLE, ten_viet[:60]))
        self.info_var.set("Tiêu đề: %s" % ten_viet)
        self.status_var.set("Tải xong: %s" % ten_viet)
        self.thanh_qua = out_path
        self.thu_muc_phim = folder
        self.btn_xem.config(state="normal")
        self.ghi_log("TẢI XONG: %s - %s" % (ten_viet, out_path))
        self.luu_job_hien_tai(status="xong", pct_tai=100, pct_gop=100)
        if messagebox.askyesno("Xong rồi!",
                               "Video đã tải + gộp xong:\n"
                               "Tên phim: %s\nFile: %s"
                               % (ten_viet, out_path) +
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
                url, option, cookies, outdir, self.log_threadsafe,
                dich_ten=self.dich_ten_var.get())
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
        self.thu_muc_phim = folder
        self.job["folder"] = folder
        self.job["tong_dung_luong"] = tong_dung_luong
        self.luu_job_hien_tai(status="dang_tai_idm")
        if self.tu_gop_var.get():
            thong_bao_idm = ("IDM đang tải 2 file:\n- %s\n- %s\n\nTool sẽ "
                             "hiện %% tải ở thanh tiến độ bên dưới (quét "
                             "dung lượng cả thư mục nên đếm đủ cả file "
                             "tiếng), tải xong sẽ tự nhận diện và tự gộp "
                             "luôn (ô 'Tải xong tự gộp luôn (IDM)' đang "
                             "tích)." % (ten_video,
                                         ten_audio or "(chỉ có hình)"))
        else:
            thong_bao_idm = ("IDM đang tải 2 file:\n- %s\n- %s\n\nTool sẽ "
                             "hiện %% tải ở thanh tiến độ bên dưới (quét "
                             "dung lượng cả thư mục nên đếm đủ cả file "
                             "tiếng). Tải xong chỉ nhận diện 2 file vào "
                             "mục 2, KHÔNG tự gộp (ô 'Tải xong tự gộp "
                             "luôn (IDM)' đang BỎ tích) - để cậu xử lý "
                             "audio / gộp tay trong CapCut sau."
                             % (ten_video, ten_audio or "(chỉ có hình)"))
        messagebox.showinfo("Đã đẩy sang IDM", thong_bao_idm)
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
        file media trong thư mục (kể cả .m4s/.mp4, bất kể tên file) thay
        vì chỉ đo 2 đường dẫn cố định như v5. Sửa lỗi v5 chỉ hiện 77%
        vì file tiếng IDM lưu thực tế là .m4s, không phải .m4a như tên
        đã đặt. (v7.6) File tiếng giờ đẩy sang IDM với tên _tieng.mp4
        (stream tiếng thực chất là container mp4) nên IDM không hỏi
        đổi tên nữa; tracker vẫn quét theo dung lượng thư mục nên
        không phụ thuộc đuôi file.
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
        # (v7.3) O tu nhan dien TAT thi bo qua han buoc nhan dien:
        # khong dien 2 file vao muc 2, de cau chon tay.
        if not self.tu_nhan_dien_var.get():
            self.status_var.set(
                "Tải xong. Chưa nhận diện file (ô tự nhận diện đang TẮT).")
            self.ghi_log("Ô 'Tự nhận diện 2 file sau khi tải' đang BỎ "
                         "tích nên KHÔNG tự nhận diện - chọn tay 2 file "
                         "ở mục 2 (nút Chọn file... / Chọn thư mục chứa "
                         "2 file), hoặc xử lý audio / gộp tay trong "
                         "CapCut sau.")
            self.luu_job_hien_tai(status="cho_gop", pct_tai=100)
            messagebox.showinfo(
                "Tải xong rồi!",
                "IDM đã tải xong.\nÔ 'Tự nhận diện 2 file sau khi "
                "tải' đang BỎ tích nên tool KHÔNG tự nhận diện - "
                "chọn tay 2 file ở mục 2 để gộp, hoặc xử lý audio / "
                "gộp tay trong CapCut sau.")
            return
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
            self.ghi_log("Tự gộp luôn (đã bật 'Tải xong tự gộp luôn (IDM)').")
            self.bam_gop()
        else:
            self.ghi_log("Ô 'Tải xong tự gộp luôn (IDM)' đang BỎ tích nên "
                         "KHÔNG tự gộp - 2 file đã nhận diện vào mục 2, để "
                         "cậu xử lý audio / gộp tay trong CapCut sau.")
            messagebox.showinfo("Tải xong rồi!",
                                "IDM đã tải xong 2 file, đã nhận diện vào "
                                "mục 2.\nÔ 'Tải xong tự gộp luôn (IDM)' "
                                "đang BỎ tích nên tool KHÔNG tự gộp - để "
                                "cậu xử lý audio / gộp tay trong CapCut "
                                "sau, hoặc bấm GỘP VIDEO ở mục 2 để gộp "
                                "lại.")

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
            # (v6.8) Dịch tên phim sang tiếng Việt trước khi gộp: lấy
            # tên từ file hình, bỏ _hinh/_tieng rồi dịch. File thành
            # phẩm đặt đúng tên phim tiếng Việt đó, không còn _hinh.
            ten_viet = ten_phim_tu_ten_file(video, dich=self.dich_ten_var.get())
            # Nếu 2 file đã nằm sẵn trong thư mục phim thì gộp ra ngay
            # trong thư mục đó; còn file lẻ thì tạo thư mục tên phim.
            thu_muc_video = os.path.dirname(os.path.abspath(video))
            if thu_muc_video != os.path.abspath(outdir):
                folder = thu_muc_video
            else:
                folder = tao_thu_muc_duy_nhat(outdir, ten_viet)
            os.makedirs(folder, exist_ok=True)
            out_name = (ten_file_da_tron(folder, ten_viet) if da_tron
                        else ten_file_dau_ra(folder, ten_viet))
            out_path = os.path.join(folder, out_name)
            gop_co_tien_trinh(
                video, audio, out_path, ffmpeg,
                lambda pct: self.after_an_toan(
                    0, self._cap_nhat_tien_trinh_gop, pct))
            self.after_an_toan(0, self._gop_xong, out_path, folder,
                               video, audio, ten_viet)
        except Exception as e:
            self.after_an_toan(0, self._gop_loi, str(e))
        finally:
            self.dang_gop = False
            self.after_an_toan(
                0, lambda: self.btn_gop.config(state="normal"))

    def _gop_xong(self, out_path, folder, video, audio, ten_viet=None):
        # (v6.8) Hiển thị tên phim tiếng Việt trong tool rồi mới báo xong.
        if not ten_viet:
            ten_viet = ten_phim_tu_ten_file(video, dich=self.dich_ten_var.get())
        self.job["title"] = ten_viet
        if self.link_info:
            self.link_info["title"] = ten_viet
        self.title("%s - %s" % (STUDIO_TITLE, ten_viet[:60]))
        self.info_var.set("Tiêu đề: %s" % ten_viet)
        self.thu_muc_phim = folder
        self.ghi_log("GỘP XONG: %s - %s" % (ten_viet, out_path))
        self.thanh_qua = out_path
        self.btn_xem.config(state="normal")
        self.tien_trinh_gop["value"] = 100
        self.phan_tram_gop_var.set("100%")
        self.status_var.set("Gộp xong: %s" % ten_viet)
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
                               "Video đã gộp xong:\n"
                               "Tên phim: %s\nFile: %s"
                               % (ten_viet, out_path) +
                               "\n\nMở thư mục chứa video?"):
            os.startfile(folder)

    # ---------- v7.1: gop voi long tieng Viet ----------
    def bam_gop_voi_long_tieng(self):
        """(v7.2) Chon file long tieng Viet (.mp3, tu tab Doc phu de)
        roi gop: hinh + tieng goc + giong Viet. Neu cong tac tu giam
        dang BAT thi tron sidechain (nhac nen tu nho khi co loi);
        neu TAT thi chi giam co dinh 15%. Khong gioi han 15 phut.
        Chay luong ngam, file ra cung thu muc du an."""
        video = self.video_var.get().strip()
        audio = self.audio_var.get().strip()
        outdir = self.outdir_var.get().strip()
        if not video or not os.path.isfile(video):
            messagebox.showerror("Thiếu file", "Chưa chọn file Video (hình).")
            return
        if not audio or not os.path.isfile(audio):
            messagebox.showerror("Thiếu file", "Chưa chọn file Audio (tiếng).")
            return
        dub = filedialog.askopenfilename(
            title="Chọn file lồng tiếng Việt (.mp3)",
            filetypes=[("Audio MP3", "*.mp3"),
                       ("Audio", "*.mp3 *.wav *.m4a"),
                       ("Tất cả file", "*.*")])
        if not dub:
            return
        ffmpeg = self.ffmpeg or tim_ffmpeg()
        if not ffmpeg:
            messagebox.showerror("Thiếu ffmpeg",
                                 "Chưa tìm thấy ffmpeg (cần để gộp).")
            return
        self.ffmpeg = ffmpeg
        self.luu_cau_hinh()
        self.btn_gop_long.config(state="disabled")
        self.dang_gop = True
        self.tien_trinh_gop["value"] = 0
        self.phan_tram_gop_var.set("0%")
        self.ghi_log("Đang gộp với lồng tiếng Việt, chờ một chút...")
        self.luu_job_hien_tai(status="dang_gop")
        threading.Thread(target=self._gop_long_tieng_worker,
                         args=(video, audio, dub, outdir, ffmpeg),
                         daemon=True).start()

    def _gop_long_tieng_worker(self, video, audio, dub, outdir, ffmpeg,
                             da_tron=False):
        try:
            ten_viet = ten_phim_tu_ten_file(video, dich=self.dich_ten_var.get())
            thu_muc_video = os.path.dirname(os.path.abspath(video))
            if thu_muc_video != os.path.abspath(outdir):
                folder = thu_muc_video
            else:
                folder = tao_thu_muc_duy_nhat(outdir, ten_viet)
            os.makedirs(folder, exist_ok=True)
            out_name = ten_file_dau_ra(folder, ten_viet)
            out_path = os.path.join(folder, out_name)
            gop_voi_long_tieng(
                video, audio, dub, out_path, ffmpeg,
                lambda pct: self.after_an_toan(
                    0, self._cap_nhat_tien_trinh_gop, pct),
                tu_giam_tieng_nen=bool(self.tu_giam_tieng_nen_var.get()),
                log_cb=self.log_threadsafe,
                giam_15=bool(self.giam_15_var.get()))
            self.after_an_toan(0, self._gop_xong, out_path, folder,
                               video, audio, ten_viet)
        except Exception as e:
            self.after_an_toan(0, self._gop_loi, str(e))
        finally:
            self.dang_gop = False
            self.after_an_toan(
                0, lambda: self.btn_gop_long.config(state="normal"))
            self.after_an_toan(
                0, lambda: self.btn_tron.config(state="normal"))

    def bam_tron_tieng_nen(self):
        """(v7.2) Nut TRON TIENG NEN + LONG TIENG: tu tim file MP3
        giong Viet HoaiMy trong CUNG thu muc du an (cung thu muc voi
        file video); tim thay thi dung luon, khong thay thi mo hop
        chon file. Tron bang sidechain neu cong tac tu giam dang BAT,
        khong thi giam co dinh 15%. File ra <ten_viet>_da-tron.mp4
        cung thu muc du an, chay luong ngam, bao ro tron xong / loi."""
        video = self.video_var.get().strip()
        audio = self.audio_var.get().strip()
        outdir = self.outdir_var.get().strip()
        if not video or not os.path.isfile(video):
            messagebox.showerror("Thiếu file", "Chưa chọn file Video (hình).")
            return
        if not audio or not os.path.isfile(audio):
            messagebox.showerror("Thiếu file", "Chưa chọn file Audio (tiếng).")
            return
        thu_muc_video = os.path.dirname(os.path.abspath(video))
        ten_viet = ten_phim_tu_ten_file(video, dich=self.dich_ten_var.get())
        dub = tim_file_long_tieng(thu_muc_video, ten_viet)
        if dub:
            self.ghi_log("Tìm thấy file giọng Việt trong thư mục dự án: "
                         + dub)
        else:
            self.ghi_log("Chưa thấy file giọng Việt trong thư mục dự án "
                         "- mở hộp chọn file.")
            dub = filedialog.askopenfilename(
                title="Chọn file lồng tiếng Việt (.mp3)",
                filetypes=[("Audio MP3", "*.mp3"),
                           ("Audio", "*.mp3 *.wav *.m4a"),
                           ("Tất cả file", "*.*")])
            if not dub:
                return
        ffmpeg = self.ffmpeg or tim_ffmpeg()
        if not ffmpeg:
            messagebox.showerror("Thiếu ffmpeg",
                                 "Chưa tìm thấy ffmpeg (cần để trộn).")
            return
        self.ffmpeg = ffmpeg
        self.luu_cau_hinh()
        self.btn_gop_long.config(state="disabled")
        self.btn_tron.config(state="disabled")
        self.dang_gop = True
        self.tien_trinh_gop["value"] = 0
        self.phan_tram_gop_var.set("0%")
        self.ghi_log("Đang trộn tiếng nền + lồng tiếng Việt, chờ một chút...")
        self.luu_job_hien_tai(status="dang_gop")
        threading.Thread(target=self._gop_long_tieng_worker,
                         args=(video, audio, dub, outdir, ffmpeg, True),
                         daemon=True).start()

    def _gop_loi(self, msg):
        self.ghi_log("GỘP THẤT BẠI: " + msg)
        self.luu_job_hien_tai(status="loi")
        messagebox.showerror("Gộp thất bại", msg)

    # ---------- (v7.3) Xuat 2 file audio rieng cho CapCut ----------
    def bam_xuat_audio_capcut(self):
        """(v7.3) Nut XUAT 2 FILE AUDIO RIENG (cho CapCut): xuat vao
        CUNG thu muc du an (cung thu muc voi file Audio goc):
        (1) file nen <ten_viet>_nen-15.mp3 (tieng goc giam con 15% -
        KHONG phai file da bo giong that su, bo giong that su CYAN
        tu lam o CapCut); (2) file giong Viet HoaiMy tu SRT
        (<ten_viet>_long-tieng.mp3) ma tab Doc phu de da xuat san.
        KHONG gop video o day. Chay luong ngam. Neu chua co file
        giong Viet thi mo tab Doc phu de voi SRT cua du an de cau
        tao giong, khong crash, khong tu gop video."""
        audio = self.audio_var.get().strip()
        video = self.video_var.get().strip()
        if not audio or not os.path.isfile(audio):
            messagebox.showerror("Thiếu file",
                                 "Chưa chọn file Audio (tiếng).")
            return
        ffmpeg = self.ffmpeg or tim_ffmpeg()
        if not ffmpeg:
            messagebox.showerror("Thiếu ffmpeg",
                                 "Chưa tìm thấy ffmpeg (cần để xuất "
                                 "file nền).")
            return
        self.ffmpeg = ffmpeg
        nguon_ten = video if video and os.path.isfile(video) else audio
        ten_viet = ten_phim_tu_ten_file(nguon_ten)
        thu_muc_du_an = os.path.dirname(os.path.abspath(audio))
        self.luu_cau_hinh()
        self.btn_xuat_audio.config(state="disabled")
        self.status_var.set("Đang xuất 2 file audio riêng cho CapCut...")
        self.ghi_log("Đang xuất 2 file audio riêng (cho CapCut) vào: "
                     + thu_muc_du_an)
        self.luu_job_hien_tai(status="dang_xuat_audio")
        threading.Thread(target=self._xuat_audio_capcut_worker,
                         args=(audio, thu_muc_du_an, ten_viet, ffmpeg),
                         daemon=True).start()

    def _xuat_audio_capcut_worker(self, audio, thu_muc_du_an, ten_viet,
                                  ffmpeg):
        try:
            nen_path, dub_path = xuat_2_file_audio_capcut(
                audio, thu_muc_du_an, ten_viet, ffmpeg,
                log_cb=self.log_threadsafe,
                giam_15=bool(self.giam_15_var.get()))
            self.after_an_toan(0, self._xuat_audio_xong,
                               nen_path, dub_path)
        except Exception as e:
            msg = str(e)
            if msg.startswith("CHUA_CO_GIONG_VIET"):
                self.after_an_toan(
                    0, self._xuat_audio_thieu_giong,
                    thu_muc_du_an, ten_viet, msg)
            else:
                self.after_an_toan(0, self._xuat_audio_loi, msg)
        finally:
            self.after_an_toan(
                0, lambda: self.btn_xuat_audio.config(state="normal"))

    def _xuat_audio_xong(self, nen_path, dub_path):
        self.status_var.set("Đã xuất xong 2 file audio riêng (cho CapCut).")
        self.ghi_log("ĐÃ XUẤT XONG 2 FILE AUDIO RIÊNG (cho CapCut):\n"
                     "- File nền: " + nen_path + "\n"
                     "- File giọng Việt: " + dub_path + "\n"
                     "File nền: tiếng gốc giảm còn 15% - phần bỏ giọng "
                     "cậu tự làm ở CapCut. Import cả 2 file này vào "
                     "CapCut để gộp tay.")
        self.luu_job_hien_tai(status="xuat_audio_xong")
        messagebox.showinfo(
            "Đã xuất xong 2 file audio",
            "Đã xuất xong 2 file audio riêng vào cùng thư mục dự án:\n"
            "- File nền: %s\n- File giọng Việt: %s\n\n"
            "File nền: tiếng gốc giảm còn 15%% - phần bỏ giọng cậu "
            "tự làm ở CapCut. Import cả 2 file này vào CapCut để "
            "gộp tay." % (nen_path, dub_path))

    def _xuat_audio_thieu_giong(self, thu_muc_du_an, ten_viet, msg):
        """(v7.3) Chua co file giong Viet: mo tab Doc phu de HoaiMy
        voi SRT cua du an da nap san de cau tao giong, roi xuat lai.
        Khong crash, khong tu gop video."""
        self.status_var.set("Chưa có file giọng Việt - mở tab Đọc phụ đề.")
        self.ghi_log("CHƯA CÓ FILE GIỌNG VIỆT: " + msg + "\n"
                     "Đã mở tab Đọc phụ đề (HoaiMy) với phụ đề của dự "
                     "án để cậu tạo giọng Việt, xong bấm lại nút "
                     "XUẤT 2 FILE AUDIO RIÊNG.")
        self.luu_job_hien_tai(status="cho_giong_viet")
        srt_path = None
        for ung_vien in (self.subtitle_vi_file, self.subtitle_file):
            if ung_vien and os.path.isfile(ung_vien):
                srt_path = ung_vien
                break
        if srt_path is None:
            for ung_vien in (ten_file_phu_de_vi(thu_muc_du_an, ten_viet),
                             ten_file_phu_de(thu_muc_du_an, ten_viet)):
                if os.path.isfile(ung_vien):
                    srt_path = ung_vien
                    break
        self.quan_ly.mo_tab_doc_phu_de(srt_path=srt_path, job=self.job)
        messagebox.showinfo(
            "Chưa có file giọng Việt",
            "Chưa có file giọng Việt HoaiMy (*long-tieng.mp3) trong "
            "thư mục dự án.\n\nĐã mở tab Đọc phụ đề (HoaiMy) với phụ "
            "đề của dự án để cậu tạo giọng Việt, xong bấm lại nút "
            "XUẤT 2 FILE AUDIO RIÊNG (cho CapCut).")

    def _xuat_audio_loi(self, msg):
        self.status_var.set("Xuất audio thất bại.")
        self.ghi_log("XUẤT AUDIO THẤT BẠI: " + msg)
        self.luu_job_hien_tai(status="loi")
        messagebox.showerror("Xuất audio thất bại", msg)



class CuaSoXuLyPhuDe(tk.Frame):  # (v7.4) Frame trong Notebook, khong con Toplevel
    """(v7.0) Tab Xu ly phu de: nap file .srt, dich sang tieng Viet bang
    Gemini/GPT/Claude (key luu local, khong hardcode) hoac Muse (tro
    ly chat tay, khong key — xuat prompt + SRT toan bo roi nhap ban
    dich ve), xem/sua ban dich, luu DE LEN FILE GOC (co 1 ban .bak)
    - theo phu luc 4: moi thu cung 1 thu muc du an, khong tao file
    lech ten. Ban dich xong co the nhap lai vao tab nay roi mo tab
    Doc phu de de chay HoaiMy. Dich chay luong ngam, tien trinh luu
    vao dich-phu-de-tien-trinh.json trong cung thu muc phim; dong
    tab khong mat tien trinh.
    (v7.6) Mac dinh dich TOAN BO file trong 1 prompt duy nhat; loi
    thi tu chuyen sang chia cum 20 cau (du phong), che do da dung
    hien o thanh trang thai + log. Model tung nha cung cap chon/go
    o o Model, luu local."""

    def __init__(self, quan_ly, parent=None, srt_path=None, job=None):
        super().__init__(parent if parent is not None else quan_ly)
        self.quan_ly = quan_ly
        self.job = job or {}
        cfg = doc_config()
        self.srt_var = tk.StringVar(value=srt_path or "")
        self.provider_var = tk.StringVar(
            value=chuan_hoa_provider(cfg.get("phu_de_provider") or "Gemini"))
        self.key_var = tk.StringVar(value="")
        self.model_var = tk.StringVar(value="")
        self.che_do_var = tk.StringVar(value="Toàn bộ 1 prompt (mặc định)")
        self.ghi_chu_provider_var = tk.StringVar(value="")
        self.the_loai_var = tk.StringVar(value=cfg.get("phu_de_the_loai") or "")
        self.nhan_vat_var = tk.StringVar(value=cfg.get("phu_de_nhan_vat") or "")
        self.xung_ho_var = tk.StringVar(value=cfg.get("phu_de_xung_ho") or "")
        self.boi_canh_var = tk.StringVar(value=cfg.get("phu_de_boi_canh") or "")
        self.status_var = tk.StringVar(value="Chưa nạp file SRT.")
        self.cac_cau_goc = []
        self.cac_cau_dich = []
        self.dang_chay = False
        self.dung_event = threading.Event()
        pad = {"padx": 8, "pady": 4}
        tk.Label(self, text="File SRT:").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.srt_var).grid(row=0, column=1, sticky="ew", **pad)
        tk.Button(self, text="Chọn...", command=self._chon_srt).grid(row=0, column=2, **pad)
        tk.Label(self, text="Nhà cung cấp:").grid(row=1, column=0, sticky="w", **pad)
        self.cbo_provider = ttk.Combobox(self, textvariable=self.provider_var,
                                         values=["Gemini", "GPT", "Claude", "Muse"],
                                         state="readonly", width=12)
        self.cbo_provider.grid(row=1, column=1, sticky="w", **pad)
        self.cbo_provider.bind("<<ComboboxSelected>>", lambda e: self._khi_doi_provider())
        # (v7.6) Model tung nha cung cap: chon san hoac GO model khac
        # (Combobox de o che do go duoc, khong readonly). Luu local.
        tk.Label(self, text="Model:").grid(row=2, column=0, sticky="w", **pad)
        self.cbo_model = ttk.Combobox(self, textvariable=self.model_var, width=24)
        self.cbo_model.grid(row=2, column=1, sticky="w", **pad)
        tk.Label(self, text="API key (chỉ lưu local):").grid(row=3, column=0, sticky="w", **pad)
        self.ent_key = tk.Entry(self, textvariable=self.key_var, show="*")
        self.ent_key.grid(row=3, column=1, sticky="ew", **pad)
        self.btn_luu_key = tk.Button(self, text="Lưu key", command=self._luu_key)
        self.btn_luu_key.grid(row=3, column=2, **pad)
        # (v7.6) Che do dich: toan bo 1 prompt (mac dinh, loi thi tu
        # chuyen cum 20 cau) hoac chi chia cum 20 cau ngay tu dau.
        tk.Label(self, text="Chế độ dịch:").grid(row=4, column=0, sticky="w", **pad)
        self.cbo_che_do = ttk.Combobox(self, textvariable=self.che_do_var,
                                       values=["Toàn bộ 1 prompt (mặc định)",
                                               "Chỉ chia cụm 20 câu"],
                                       state="readonly", width=28)
        self.cbo_che_do.grid(row=4, column=1, sticky="w", **pad)
        self.cbo_che_do.bind("<<ComboboxSelected>>", lambda e: self._luu_key())
        tk.Label(self, text="Thể loại:").grid(row=5, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.the_loai_var).grid(row=5, column=1, sticky="ew", **pad)
        tk.Label(self, text="Nhân vật:").grid(row=6, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.nhan_vat_var).grid(row=6, column=1, sticky="ew", **pad)
        tk.Label(self, text="Xưng hô/vai vế:").grid(row=7, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.xung_ho_var).grid(row=7, column=1, sticky="ew", **pad)
        tk.Label(self, text="Bối cảnh thêm:").grid(row=8, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.boi_canh_var).grid(row=8, column=1, sticky="ew", **pad)
        tk.Label(self, textvariable=self.ghi_chu_provider_var, fg="gray",
                 wraplength=640, justify="left").grid(
                     row=9, column=0, columnspan=3, sticky="w", **pad)
        hang = tk.Frame(self)
        hang.grid(row=10, column=0, columnspan=3, sticky="ew", **pad)
        self.btn_dich = tk.Button(hang, text="DỊCH PHỤ ĐỀ", font=("", 11, "bold"),
                                  command=self.bam_dich)
        self.btn_dich.pack(side="left", padx=4)
        tk.Button(hang, text="Dừng", command=self.bam_dung).pack(side="left", padx=4)
        tk.Button(hang, text="Xuất prompt + SRT toàn bộ", command=self.bam_xuat_prompt).pack(side="left", padx=4)
        tk.Button(hang, text="Nhập bản dịch về", command=self.bam_nhap_ban_dich).pack(side="left", padx=4)
        tk.Button(hang, text="Mở tab Đọc phụ đề", command=self.bam_mo_doc).pack(side="left", padx=4)
        tk.Button(hang, text="Dịch thủ công", command=self.bam_dich_thu_cong).pack(side="left", padx=4)
        hang2 = tk.Frame(self)
        hang2.grid(row=11, column=0, columnspan=3, sticky="ew", **pad)
        tk.Button(hang2, text="LƯU ĐÈ LÊN FILE GỐC (.bak giữ lại)",
                  font=("", 11, "bold"), command=self.bam_luu_de_goc).pack(side="left", padx=4)
        tk.Button(hang2, text="Lưu bản _vi riêng", command=self.bam_luu_vi_rieng).pack(side="left", padx=4)
        self.tien_trinh = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.tien_trinh.grid(row=12, column=0, columnspan=3, sticky="ew", **pad)
        tk.Label(self, text="Bản dịch (xem/sửa được trước khi lưu):").grid(
            row=13, column=0, columnspan=3, sticky="w", **pad)
        self.txt_dich = scrolledtext.ScrolledText(self, height=16)
        self.txt_dich.grid(row=14, column=0, columnspan=3, sticky="nsew", **pad)
        tk.Label(self, textvariable=self.status_var, fg="gray").grid(
            row=15, column=0, columnspan=3, sticky="ew", **pad)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(14, weight=1)
        # (v7.5) Dich thu cong: khung an, hien khi bam "Dich thu cong".
        # Mo SRT goc, tu go tieng Viet tung cau (o nhap canh tung cau),
        # khong goi AI, van giu moc gio goc.
        self.khung_thu_cong = tk.LabelFrame(
            self, text=" Dịch thủ công (không gọi AI — tự gõ từng câu, giữ nguyên mốc giờ) ",
            padx=8, pady=6)
        self.khung_thu_cong.grid(row=16, column=0, columnspan=3,
                                 sticky="nsew", **pad)
        self.khung_thu_cong.grid_remove()
        hang_tc = tk.Frame(self.khung_thu_cong)
        hang_tc.pack(fill="x")
        tk.Button(hang_tc, text="Lưu nháp",
                  command=self._luu_nhap_thu_cong).pack(side="left", padx=4)
        tk.Button(hang_tc, text="LƯU SRT VIỆT (ghi đè, có .bak)",
                  font=("", 11, "bold"),
                  command=self._luu_srt_viet_thu_cong).pack(side="left", padx=4)
        tk.Button(hang_tc, text="Đóng",
                  command=self._dong_dich_thu_cong).pack(side="left", padx=4)
        self.nhap_tc_var = tk.StringVar(value="")
        tk.Label(self.khung_thu_cong, textvariable=self.nhap_tc_var,
                 fg="gray", wraplength=640, justify="left").pack(anchor="w")
        canvas_tc = tk.Canvas(self.khung_thu_cong, height=220)
        sb_tc = ttk.Scrollbar(self.khung_thu_cong, orient="vertical",
                              command=canvas_tc.yview)
        self.khung_dong_tc = tk.Frame(canvas_tc)
        self.khung_dong_tc.bind(
            "<Configure>",
            lambda e: canvas_tc.configure(
                scrollregion=canvas_tc.bbox("all")))
        canvas_tc.create_window((0, 0), window=self.khung_dong_tc, anchor="nw")
        canvas_tc.configure(yscrollcommand=sb_tc.set)
        canvas_tc.pack(side="left", fill="both", expand=True)
        sb_tc.pack(side="right", fill="y")
        self.cac_entry_tc = {}
        self.nhap_tc = {}
        self._nap_key()
        if srt_path and os.path.isfile(srt_path):
            self._nap_srt(srt_path)

    def _khoa_key(self, provider):
        # (v7.6) "Claude" = Anthropic. "Muse" (tro ly Muse, chat tay)
        # KHONG co key -> tra None.
        return {"Gemini": "gemini_api_key", "GPT": "openai_api_key",
                "Claude": "anthropic_api_key"}.get(
                    chuan_hoa_provider(provider))

    def _khoa_model(self, provider):
        return {"Gemini": "phu_de_model_gemini",
                "GPT": "phu_de_model_gpt",
                "Claude": "phu_de_model_claude"}.get(
                    chuan_hoa_provider(provider))

    def _che_do_tu_hien_thi(self):
        return "cum" if "cụm" in (self.che_do_var.get() or "") else "toan_bo"

    def _hien_thi_tu_che_do(self, che_do):
        return ("Chỉ chia cụm 20 câu" if (che_do or "toan_bo") == "cum"
                else "Toàn bộ 1 prompt (mặc định)")

    def _nap_model(self):
        """Nap model + danh sach goi y theo provider; Muse thi tat o Model."""
        provider = chuan_hoa_provider(self.provider_var.get())
        goi_y = {"Gemini": [MODEL_GEMINI_MAC_DINH, MODEL_GEMINI_DU_PHONG],
                 "GPT": [MODEL_GPT_MAC_DINH, "gpt-4o"],
                 "Claude": [MODEL_CLAUDE_MAC_DINH]}.get(provider, [])
        try:
            self.cbo_model.configure(values=goi_y)
        except Exception:
            pass
        cfg = doc_config()
        self.model_var.set(model_cua_provider(provider, cfg))
        try:
            self.cbo_model.configure(
                state="disabled" if provider == "Muse" else "normal")
        except Exception:
            pass

    def _cap_nhat_ghi_chu_provider(self):
        provider = chuan_hoa_provider(self.provider_var.get())
        la_muse = provider == "Muse"
        try:
            self.ent_key.configure(state="disabled" if la_muse else "normal")
            self.btn_luu_key.configure(state="disabled" if la_muse else "normal")
        except Exception:
            pass
        if la_muse:
            self.ghi_chu_provider_var.set(
                "Muse = trợ lý Muse (chat tay, KHÔNG dùng API key): bấm "
                "'Xuất prompt + SRT toàn bộ', dán file vào chat với "
                "Muse, rồi bấm 'Nhập bản dịch về'.")
        else:
            self.ghi_chu_provider_var.set(
                "Key và model chỉ lưu local trong config.json, không "
                "gửi đi đâu khác ngoài API của nhà cung cấp đã chọn.")

    def _khi_doi_provider(self):
        self._nap_key()
        self._cap_nhat_ghi_chu_provider()

    def _nap_key(self):
        try:
            cfg = doc_config()
            khoa = self._khoa_key(self.provider_var.get())
            self.key_var.set((cfg.get(khoa) or "") if khoa else "")
            che_do = cfg.get("phu_de_che_do") or "toan_bo"
            self.che_do_var.set(self._hien_thi_tu_che_do(che_do))
        except Exception:
            pass
        self._nap_model()
        self._cap_nhat_ghi_chu_provider()

    def _luu_key(self):
        try:
            cfg = doc_config()
            provider = chuan_hoa_provider(self.provider_var.get())
            cfg["phu_de_provider"] = provider
            khoa = self._khoa_key(provider)
            if khoa:
                cfg[khoa] = self.key_var.get().strip()
            khoa_model = self._khoa_model(provider)
            if khoa_model and self.model_var.get().strip():
                cfg[khoa_model] = self.model_var.get().strip()
            cfg["phu_de_che_do"] = self._che_do_tu_hien_thi()
            cfg["phu_de_the_loai"] = self.the_loai_var.get()
            cfg["phu_de_nhan_vat"] = self.nhan_vat_var.get()
            cfg["phu_de_xung_ho"] = self.xung_ho_var.get()
            cfg["phu_de_boi_canh"] = self.boi_canh_var.get()
            luu_config(cfg)
            self.status_var.set("Đã lưu nhà cung cấp / key / model / chế độ dịch (local).")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def _chon_srt(self):
        p = filedialog.askopenfilename(title="Chọn file phụ đề .srt",
                                       filetypes=[("Phụ đề SRT", "*.srt"), ("Mọi file", "*.*")])
        if p:
            self.srt_var.set(p)
            self._nap_srt(p)

    def _nap_srt(self, path):
        try:
            self.cac_cau_goc = doc_srt(path)
            self.cac_cau_dich = []
            self.txt_dich.delete("1.0", "end")
            self.status_var.set("Đã nạp %d câu từ %s." % (len(self.cac_cau_goc), os.path.basename(path)))
        except Exception as e:
            messagebox.showerror("Lỗi đọc SRT", str(e))

    def _lay_cac_cau_dich_tu_preview(self):
        text = self.txt_dich.get("1.0", "end")
        da = doc_srt_text(text)
        if len(da) == len(self.cac_cau_goc) and da:
            return da
        # Preview sua tay khong dung dang SRT: giu timestamp goc, lay
        # tung dong dich theo thu tu.
        dong = [d for d in text.splitlines() if d.strip()]
        out = []
        for i, goc in enumerate(self.cac_cau_goc):
            out.append({"chi_so": goc.get("chi_so"), "bat_dau_ms": goc.get("bat_dau_ms"),
                        "ket_thuc_ms": goc.get("ket_thuc_ms"),
                        "text": dong[i] if i < len(dong) else goc.get("text")})
        return out

    def bam_dich(self):
        if self.dang_chay:
            return
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        if not self.cac_cau_goc:
            self._nap_srt(p)
        if not self.cac_cau_goc:
            messagebox.showerror("Lỗi", "Không đọc được câu nào trong file SRT.")
            return
        provider = chuan_hoa_provider(self.provider_var.get())
        if provider == "Muse":
            # (v7.6) Muse la chat tay, khong co API: khong khoi worker.
            messagebox.showinfo(
                "Muse — dịch bằng chat tay",
                "Muse không có API key trong tool.\n\n"
                "Bấm 'Xuất prompt + SRT toàn bộ' để lấy file prompt + "
                "toàn bộ SRT gốc, dán vào chat với Muse, rồi bấm "
                "'Nhập bản dịch về' để tool kiểm tra khớp file gốc "
                "rồi mới cho lưu đè.")
            return
        self._luu_key()
        self.dang_chay = True
        self.dung_event.clear()
        self.btn_dich.config(state="disabled")
        self.status_var.set("Đang dịch phụ đề...")
        args = (list(self.cac_cau_goc), provider,
                self.key_var.get().strip(), self.the_loai_var.get(),
                self.nhan_vat_var.get(), self.xung_ho_var.get(),
                self.boi_canh_var.get(),
                self.model_var.get().strip(),
                self._che_do_tu_hien_thi())
        threading.Thread(target=self._dich_worker, args=args, daemon=True).start()

    def _dich_worker(self, cac_cau, provider, key, the_loai, nhan_vat, xung_ho, boi_canh, model="", che_do="toan_bo"):
        try:
            ket_qua, che_do_da_dung = dich_srt(
                cac_cau, provider, key, the_loai, nhan_vat, xung_ho, boi_canh,
                model=model or None, che_do=che_do,
                tien_trinh_cb=lambda pct: self.after(0, lambda: self.tien_trinh.configure(value=pct)),
                dung_event=self.dung_event,
                log=lambda s: self.after(0, lambda: self.status_var.set(s)))
            self.after(0, self._dich_xong, ket_qua, che_do_da_dung)
        except Exception as e:
            self.after(0, self._dich_loi, str(e))

    def _dich_xong(self, ket_qua, che_do=""):
        self.dang_chay = False
        self.btn_dich.config(state="normal")
        # (v7.6) Kiem tra phong thu: so cau dich phai khop goc, neu
        # khong thi KHONG thay preview, bao loi ro.
        if not ket_qua or len(ket_qua) != len(self.cac_cau_goc):
            self.status_var.set("Dịch lỗi: bản dịch có %d câu, file gốc có %d câu — không khớp, chưa lưu gì." % (len(ket_qua or []), len(self.cac_cau_goc)))
            messagebox.showerror("Dịch lỗi", "Bản dịch trả về %d câu, file gốc có %d câu — không khớp nên không nạp. Thử dịch lại." % (len(ket_qua or []), len(self.cac_cau_goc)))
            return
        self.cac_cau_dich = ket_qua or []
        self.tien_trinh.configure(value=100)
        text = "".join("%d\n%s --> %s\n%s\n\n" % (
            c.get("chi_so") or 0, dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
            dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0), c.get("text") or "")
            for c in self.cac_cau_dich)
        self.txt_dich.delete("1.0", "end")
        self.txt_dich.insert("1.0", text)
        # Luu tien trinh dich vao cung thu muc phim.
        try:
            folder = os.path.dirname(os.path.abspath(self.srt_var.get().strip()))
            with open(os.path.join(folder, "dich-phu-de-tien-trinh.json"), "w", encoding="utf-8") as f:
                json.dump({"srt": self.srt_var.get().strip(),
                           "da_dich": len(self.cac_cau_dich),
                           "tong_cau": len(self.cac_cau_goc)}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        self.status_var.set("Đã dịch xong %d/%d câu (chế độ: %s). Kiểm tra lại trong ô dưới rồi bấm Lưu đè lên file gốc." % (len(self.cac_cau_dich), len(self.cac_cau_goc), che_do or "?"))

    def _dich_loi(self, msg):
        self.dang_chay = False
        self.btn_dich.config(state="normal")
        self.status_var.set("Dịch lỗi: " + msg)
        messagebox.showerror("Dịch phụ đề lỗi", msg)

    def bam_dung(self):
        self.dung_event.set()
        self.status_var.set("Đã yêu cầu dừng sau cụm đang dịch.")

    def bam_xuat_prompt(self):
        """(v7.6) Xuat TOAN BO prompt + TOAN BO SRT goc ra file text
        cung thu muc phim, de dan vao chat voi Muse (chat tay, khong
        can key) hoac GPT/Gemini. File chua dung prompt toan bo cua
        tao_prompt_dich_phu_de + toan bo SRT goc."""
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        if not self.cac_cau_goc:
            self._nap_srt(p)
        khoi = "".join("%d\n%s --> %s\n%s\n\n" % (
            c.get("chi_so") or 0, dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
            dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0), c.get("text") or "")
            for c in self.cac_cau_goc)
        prompt = tao_prompt_dich_phu_de(self.the_loai_var.get(), self.nhan_vat_var.get(),
                                        self.xung_ho_var.get(), self.boi_canh_var.get(), khoi)
        out = os.path.join(os.path.dirname(os.path.abspath(p)),
                           os.path.splitext(os.path.basename(p))[0] + "_prompt.txt")
        try:
            with open(out, "w", encoding="utf-8") as f:
                f.write(prompt)
            try:
                self.clipboard_clear()
                self.clipboard_append(prompt)
            except Exception:
                pass
            messagebox.showinfo("Đã xuất prompt",
                                "File prompt + SRT toàn bộ:\n%s\n\nĐã copy prompt vào clipboard (nếu được).\nDán vào chat với Muse rồi bấm 'Nhập bản dịch về'." % out)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def bam_luu_de_goc(self):
        """(v7.0, phu luc 4) Luu DE LEN FILE GOC: sao luu 1 ban .bak roi
        ghi ban dich de len dung file .srt goc, khong tao file lech ten."""
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        cac = self._lay_cac_cau_dich_tu_preview()
        if not cac:
            messagebox.showerror("Chưa có bản dịch", "Bấm Dịch phụ đề trước, hoặc nhập bản dịch về rồi mới lưu.")
            return
        # (v7.6) Kiem tra CUNG truoc khi luu de: so cau/timestamp
        # phai khop file goc — khong khop thi KHONG luu, file goc
        # con nguyen (ke ca ban dich nhap ve tu Muse).
        if self.cac_cau_goc:
            ok, loi = kiem_tra_ban_dich_khop_goc(self.cac_cau_goc, cac)
            if not ok:
                messagebox.showerror("Bản dịch không khớp file gốc",
                                     "Không lưu đè: %s\nFile gốc còn nguyên." % loi)
                return
        try:
            duong, bak = luu_ban_dich_an_toan(p, cac)
            self.cac_cau_dich = cac
            if self.job:
                self.job["subtitle_file"] = p
                self.job["subtitle_vi_file"] = p
                self.job["has_subtitle"] = True
                self.job["subtitle_status"] = "da_dich"
                cap_nhat_job_trong_jobs(self.job)
            self.status_var.set("Đã lưu đè lên file gốc: %s (bản sao lưu: %s)" % (p, bak or "không có"))
            messagebox.showinfo("Đã lưu", "Đã ghi đè bản dịch lên file gốc:\n%s\nBản sao lưu: %s" % (p, bak or "(không tạo được)"))
        except Exception as e:
            messagebox.showerror("Lỗi lưu", str(e))

    def bam_luu_vi_rieng(self):
        """Tuy chon: luu them 1 ban <Ten>_vi.srt rieng (khong phai mac dinh)."""
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        cac = self._lay_cac_cau_dich_tu_preview()
        if not cac:
            messagebox.showerror("Chưa có bản dịch", "Bấm Dịch phụ đề trước đã.")
            return
        folder = os.path.dirname(os.path.abspath(p))
        ten = os.path.splitext(os.path.basename(p))[0]
        # ten da co _vi thi giu nguyen, khong them _vi lan nua
        if ten.endswith("_vi"):
            dich = os.path.join(folder, ten + ".srt")
        else:
            dich = ten_file_phu_de_vi(folder, ten)
        try:
            ghi_srt_chung(cac, dich)
            messagebox.showinfo("Đã lưu", "File bản dịch riêng:\n" + dich)
        except Exception as e:
            messagebox.showerror("Lỗi lưu", str(e))

    def bam_nhap_ban_dich(self):
        """(v7.6) Nhap ban dich (.srt da dich o ngoai — thuong la Muse
        tra ve sau khi dan prompt toan bo) ve tab nay. Kiem tra so cau/
        timestamp khop file goc TRUOC khi nap: khong khop thi bao loi
        chi tiet va KHONG thay preview; khop moi nap de luu de
        (co .bak 1 lan nhu cu)."""
        p = filedialog.askopenfilename(title="Chọn file SRT đã dịch",
                                       filetypes=[("Phụ đề SRT", "*.srt"), ("Mọi file", "*.*")])
        if not p:
            return
        try:
            cac = doc_srt(p)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            return
        if not cac:
            messagebox.showerror("Lỗi", "File bản dịch không có câu nào.")
            return
        goc_path = self.srt_var.get().strip()
        if not self.cac_cau_goc and goc_path and os.path.isfile(goc_path):
            self._nap_srt(goc_path)
        if self.cac_cau_goc:
            ok, loi = kiem_tra_ban_dich_khop_goc(self.cac_cau_goc, cac)
            if not ok:
                messagebox.showerror(
                    "Bản dịch không khớp file gốc",
                    "Không nạp bản dịch này: %s\n\nFile gốc: %s\nBản dịch: %s"
                    % (loi, goc_path or "(chưa chọn)", p))
                return
        else:
            messagebox.showinfo(
                "Đã nhập (chưa đối chiếu được)",
                "Đã nhập %d câu từ %s, nhưng chưa nạp được file SRT gốc "
                "để đối chiếu số câu/timestamp.\nNạp file gốc vào ô SRT "
                "trước rồi nhập lại, hoặc kiểm tra kỹ trước khi bấm "
                "Lưu đè." % (len(cac), os.path.basename(p)))
        self.cac_cau_dich = cac
        text = "".join("%d\n%s --> %s\n%s\n\n" % (
            c.get("chi_so") or 0, dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
            dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0), c.get("text") or "")
            for c in cac)
        self.txt_dich.delete("1.0", "end")
        self.txt_dich.insert("1.0", text)
        # Ban dich nhap ve tro thanh ban dich hien tai cua file goc
        # dang mo (de luu de / doc tiep), khong doi duong dan goc.
        self.status_var.set("Đã nhập %d câu bản dịch từ %s (đã kiểm tra khớp file gốc)." % (len(cac), os.path.basename(p)))

    def bam_mo_doc(self):
        p = self.srt_var.get().strip()
        try:
            self.quan_ly.mo_tab_doc_phu_de(srt_path=p if p and os.path.isfile(p) else None, job=self.job)
        except Exception as e:
            messagebox.showerror("Không mở được tab", str(e))

    # ---- (v7.5) Dich thu cong ----
    def _duong_nhap_thu_cong(self, srt_path):
        folder = os.path.dirname(os.path.abspath(srt_path))
        goc = os.path.splitext(os.path.basename(srt_path))[0]
        return os.path.join(folder, goc + "_dich-tay-nhap.json")

    def _doc_nhap_thu_cong(self, srt_path):
        try:
            with open(self._duong_nhap_thu_cong(srt_path), "r",
                      encoding="utf-8") as f:
                du_lieu = json.load(f)
            if isinstance(du_lieu, dict):
                return du_lieu.get("ban_dich") or {}
        except Exception:
            pass
        return {}

    def _lay_ban_dich_thu_cong_hien_tai(self):
        out = {}
        for chi_so, ent in (self.cac_entry_tc or {}).items():
            try:
                out[chi_so] = ent.get().strip()
            except Exception:
                pass
        return out

    def _luu_nhap_thu_cong(self, am_tham=False):
        p = self.srt_var.get().strip()
        if not p or not self.cac_entry_tc:
            return
        try:
            duong = self._duong_nhap_thu_cong(p)
            with open(duong, "w", encoding="utf-8") as f:
                json.dump({"srt": p,
                           "ban_dich": self._lay_ban_dich_thu_cong_hien_tai()},
                          f, ensure_ascii=False, indent=2)
            if not am_tham:
                self.nhap_tc_var.set("Đã lưu nháp: %s" % duong)
        except Exception as e:
            if not am_tham:
                messagebox.showerror("Lỗi lưu nháp", str(e))

    def bam_dich_thu_cong(self):
        """(v7.5) Mo che do dich thu cong: hien danh sach cau kem
        moc gio, o nhap tieng Viet canh tung cau. Khong goi AI."""
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        if not self.cac_cau_goc:
            self._nap_srt(p)
        if not self.cac_cau_goc:
            messagebox.showerror("Lỗi", "Không đọc được câu nào trong file SRT.")
            return
        self.nhap_tc = self._doc_nhap_thu_cong(p)
        for w in list(self.khung_dong_tc.winfo_children()):
            w.destroy()
        self.cac_entry_tc = {}
        for c in self.cac_cau_goc:
            chi_so = c.get("chi_so")
            dong = tk.Frame(self.khung_dong_tc)
            dong.pack(fill="x", pady=1)
            tk.Label(dong, text="%d" % (chi_so or 0), width=5,
                     anchor="w").pack(side="left")
            tk.Label(dong, text="%s --> %s" % (
                dinh_dang_ms_srt(c.get("bat_dau_ms") or 0),
                dinh_dang_ms_srt(c.get("ket_thuc_ms") or 0)),
                width=24, anchor="w", fg="gray").pack(side="left")
            tk.Label(dong, text=(c.get("text") or ""), anchor="w",
                     wraplength=260, justify="left").pack(
                         side="left", padx=4)
            ent = tk.Entry(dong, width=40)
            ent.pack(side="left", fill="x", expand=True, padx=4)
            cu = (self.nhap_tc.get(chi_so)
                  if isinstance(self.nhap_tc, dict) else None)
            if cu is None and isinstance(self.nhap_tc, dict):
                cu = self.nhap_tc.get(str(chi_so))
            if cu:
                ent.insert(0, cu)
            ent.bind("<FocusOut>",
                     lambda e: self._luu_nhap_thu_cong(am_tham=True))
            self.cac_entry_tc[chi_so] = ent
        self.nhap_tc_var.set(
            "Đã nạp %d câu — gõ tiếng Việt vào ô bên phải từng câu. "
            "Lưu nháp để lưu tạm (tự lưu nháp khi rời ô). Bấm LƯU SRT "
            "VIỆT để lưu đè lên file gốc (có .bak 1 lần) rồi mở tab "
            "Đọc phụ đề HoaiMy." % len(self.cac_cau_goc))
        self.khung_thu_cong.grid()

    def _dong_dich_thu_cong(self):
        try:
            self.khung_thu_cong.grid_remove()
        except Exception:
            pass

    def _luu_srt_viet_thu_cong(self):
        """(v7.5) Luu ban dich thu cong: ghep cau (giu moc gio
        goc), luu de len file goc qua luu_ban_dich_an_toan (.bak 1
        lan), roi mo tab Doc phu de HoaiMy voi file SRT Viet."""
        p = self.srt_var.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showerror("Thiếu file", "Chọn file SRT trước đã.")
            return
        if not self.cac_cau_goc:
            messagebox.showerror("Lỗi", "Chưa nạp câu nào để dịch.")
            return
        cac = ghep_ban_dich_thu_cong(
            self.cac_cau_goc, self._lay_ban_dich_thu_cong_hien_tai())
        try:
            duong, bak = luu_ban_dich_an_toan(p, cac)
        except Exception as e:
            messagebox.showerror("Lỗi lưu", str(e))
            return
        self.cac_cau_dich = cac
        if self.job:
            self.job["subtitle_file"] = p
            self.job["subtitle_vi_file"] = p
            self.job["has_subtitle"] = True
            self.job["subtitle_status"] = "da_dich"
            cap_nhat_job_trong_jobs(self.job)
        self.status_var.set("Đã lưu SRT Việt (dịch thủ công): %s "
                            "(bản sao lưu: %s)" % (duong, bak or "không có"))
        messagebox.showinfo("Đã lưu",
                            "Đã lưu SRT Việt (dịch thủ công):\n%s\n"
                            "Bản sao lưu file gốc: %s"
                            % (duong, bak or "(không tạo được)"))
        try:
            self.quan_ly.mo_tab_doc_phu_de(srt_path=p, job=self.job)
        except Exception as e:
            messagebox.showinfo("Đã lưu",
                                "File: %s\n(Không mở được tab Đọc phụ đề: "
                                "%s)" % (p, e))


class QuanLy(tk.Tk):
    """(v6) Cửa sổ quản lý: nút + mở cửa sổ job mới, danh sách lịch sử job
    (đọc từ jobs.json), mở lại / xóa job. Cài đặt chung (thư mục lưu,
    cookies) dùng chung cho mọi cửa sổ job."""

    def __init__(self):
        super().__init__()
        self.title("%s (v%s)" % (STUDIO_TITLE, VERSION))
        self.geometry("1020x860")
        self.resizable(True, True)
        self.cua_so_mo = {}
        self.job_da_chon_id = None

        cfg = doc_config()
        self.outdir_var = tk.StringVar(
            value=cfg.get("output_dir") or mac_dinh_thu_muc_luu())
        self.cookies_var = tk.StringVar(
            value=cfg.get("cookies") or (
                COOKIES_MAC_DINH if os.path.isfile(COOKIES_MAC_DINH) else ""))

        pad = {"padx": 8, "pady": 4}

        # ---- (v7.4, 05:37) Thanh nut chinh: nut chuc nang ben TRAI,
        # nut "Kiem tra cap nhat" day ra canh ngoai cung GOC PHAI,
        # tach rieng bang separator + khoang trong de de thay/bam.
        # Chuc nang kiem tra cap nhat giu nguyen (khong token,
        # Release latest, asset Chipchipdownload.exe).
        hang_nut = tk.Frame(self)
        hang_nut.pack(fill="x", **pad)
        tk.Button(hang_nut, text="+ Mở cửa sổ mới", font=("", 11, "bold"),
                  command=self.mo_cua_so_moi).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Mở lại job đã chọn",
                  command=self.mo_lai_job_da_chon).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Xóa job đã chọn",
                  command=self.xoa_job_da_chon).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Xử lý phụ đề",
                  command=lambda: self.mo_tab_xu_ly_phu_de()).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Đọc phụ đề (HoaiMy)",
                  command=lambda: self.mo_tab_doc_phu_de()).pack(side="left", padx=4)
        tk.Button(hang_nut, text="Kiểm tra cập nhật", font=("", 11, "bold"),
                  command=self.bam_kiem_tra_cap_nhat).pack(side="right", padx=4)
        ttk.Separator(hang_nut, orient="vertical").pack(side="right", fill="y", padx=8)

        # ---- (v7.4) 1 cua so duy nhat: ttk.Notebook 3 tab. Cac tab
        # Xu ly phu de / Doc phu de la Frame nhung trong Notebook,
        # khong con Toplevel mo rieng chong nhau.
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=4, pady=4)
        self.tab_quan_ly = tk.Frame(self.notebook)
        self.tab_xu_ly = tk.Frame(self.notebook)
        self.tab_doc = tk.Frame(self.notebook)
        self.notebook.add(self.tab_quan_ly, text="Quản lý")
        self.notebook.add(self.tab_xu_ly, text="Xử lý phụ đề")
        self.notebook.add(self.tab_doc, text="Đọc phụ đề (HoaiMy)")
        self.panel_xu_ly = CuaSoXuLyPhuDe(self, parent=self.tab_xu_ly)
        self.panel_xu_ly.pack(fill="both", expand=True)
        self.panel_doc = CuaSoDocPhuDe(self, parent=self.tab_doc)
        self.panel_doc.pack(fill="both", expand=True)

        # ---- Tab Quan ly: lich su du an + cai dat chung (nhu cu) ----
        tk.Label(self.tab_quan_ly, text="Lịch sử dự án (bấm 1 dòng để chọn, bấm đúp để mở lại cửa sổ):").grid(
            row=0, column=0, columnspan=3, sticky="w", **pad)
        khung_bang_ngoai = tk.Frame(self.tab_quan_ly)
        khung_bang_ngoai.grid(row=1, column=0, columnspan=3, sticky="nsew", **pad)
        # (v7.6) Bang lich su = ttk.Treeview cot CO DINH, thay cho
        # Canvas + moi dong 1 Frame o v7.5 (header o frame cha, cot
        # trong dong weight rieng -> header/dong khong thang hang,
        # khong co scrollbar ngang, cot tu gian theo noi dung dai).
        # Cot khong gian theo noi dung: gia tri hien da rut gon
        # (rut_gon_chu/rut_gon_link/rut_gon_duong_dan), gia tri day
        # du hien o label chi tiet duoi bang khi chon dong.
        cot_bang = ("ten", "link", "trang_thai", "thu_muc", "phu_de")
        self.tree_du_an = ttk.Treeview(khung_bang_ngoai, columns=cot_bang,
                                       show="headings", height=7)
        self.tree_du_an.heading("ten", text="Tên phim")
        self.tree_du_an.heading("link", text="Link")
        self.tree_du_an.heading("trang_thai", text="Trạng thái")
        self.tree_du_an.heading("thu_muc", text="Đường dẫn lưu thư mục")
        self.tree_du_an.heading("phu_de", text="Phụ đề")
        self.tree_du_an.column("ten", width=260, minwidth=180,
                               stretch=tk.YES, anchor="w")
        self.tree_du_an.column("link", width=180, minwidth=120,
                               stretch=tk.NO, anchor="w")
        self.tree_du_an.column("trang_thai", width=110, minwidth=90,
                               stretch=tk.NO, anchor="w")
        self.tree_du_an.column("thu_muc", width=180, minwidth=120,
                               stretch=tk.NO, anchor="w")
        self.tree_du_an.column("phu_de", width=220, minwidth=150,
                               stretch=tk.NO, anchor="w")
        sb_bang_doc = ttk.Scrollbar(khung_bang_ngoai, orient="vertical",
                                    command=self.tree_du_an.yview)
        sb_bang_ngang = ttk.Scrollbar(khung_bang_ngoai, orient="horizontal",
                                      command=self.tree_du_an.xview)
        self.tree_du_an.configure(yscrollcommand=sb_bang_doc.set,
                                  xscrollcommand=sb_bang_ngang.set)
        self.tree_du_an.grid(row=0, column=0, sticky="nsew")
        sb_bang_doc.grid(row=0, column=1, sticky="ns")
        sb_bang_ngang.grid(row=1, column=0, sticky="ew")
        self.tree_du_an.bind("<<TreeviewSelect>>", self._khi_chon_du_an)
        self.tree_du_an.bind("<Double-1>", self._mo_doi_du_an)
        self.bang = self.tree_du_an
        self.chi_tiet_du_an_var = tk.StringVar(
            value="Chưa chọn dự án nào — bấm 1 dòng trong bảng để xem đầy đủ.")
        tk.Label(khung_bang_ngoai, textvariable=self.chi_tiet_du_an_var,
                 fg="gray", wraplength=900, justify="left",
                 anchor="w").grid(row=2, column=0, columnspan=2,
                                  sticky="w", padx=3, pady=2)
        # (v7.6) Hang nut hanh dong cho dong DANG CHON (Treeview
        # khong chua nut tung dong). Tai dung dung ham cu.
        hang_nut_bang = tk.Frame(khung_bang_ngoai)
        hang_nut_bang.grid(row=3, column=0, columnspan=2, sticky="w",
                           padx=3, pady=2)
        self.btn_mo_thu_muc_du_an = tk.Button(
            hang_nut_bang, text="Mở thư mục dự án",
            command=lambda: self._mo_thu_muc_du_an(self._lay_job_da_chon()))
        self.btn_mo_thu_muc_du_an.pack(side="left", padx=2)
        self.btn_mo_thu_muc_phu_de = tk.Button(
            hang_nut_bang, text="Mở thư mục phụ đề",
            command=lambda: self._mo_thu_muc_phu_de(self._lay_job_da_chon()))
        self.btn_mo_thu_muc_phu_de.pack(side="left", padx=2)
        self.btn_lam_lai_du_an = tk.Button(
            hang_nut_bang, text="Làm lại",
            command=lambda: self._lam_lai_du_an(self._lay_job_da_chon()))
        self.btn_lam_lai_du_an.pack(side="left", padx=2)
        self.btn_dich_phu_de_du_an = tk.Button(
            hang_nut_bang, text="Dịch phụ đề",
            command=self._dich_hoac_them_phu_de_du_an)
        self.btn_dich_phu_de_du_an.pack(side="left", padx=2)
        self.btn_xoa_du_an = tk.Button(
            hang_nut_bang, text="Xóa",
            command=lambda: self._xoa_du_an(self._lay_job_da_chon()))
        self.btn_xoa_du_an.pack(side="left", padx=2)
        khung_bang_ngoai.grid_columnconfigure(0, weight=1)
        # (v7.6, sua sau test xvfb) minsize: tab chi cao 640 trong
        # khi noi dung xin ~800 — grid se lay het phan thieu o
        # row co weight duy nhat (chinh la row chua bang) nen
        # Treeview bi bop ve 0px. minsize giu bang luon thay duoc.
        khung_bang_ngoai.grid_rowconfigure(0, weight=1, minsize=170)

        tk.Label(self.tab_quan_ly, text="Thư mục lưu:").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self.tab_quan_ly, textvariable=self.outdir_var).grid(
            row=2, column=1, sticky="ew", **pad)
        tk.Button(self.tab_quan_ly, text="Chọn...",
                  command=self.chon_thu_muc_luu).grid(row=2, column=2, **pad)
        tk.Label(self.tab_quan_ly, text="File cookies.txt (để tải 1080p):").grid(
            row=3, column=0, sticky="w", **pad)
        tk.Entry(self.tab_quan_ly, textvariable=self.cookies_var).grid(
            row=3, column=1, sticky="ew", **pad)
        tk.Button(self.tab_quan_ly, text="Chọn...",
                  command=self.chon_cookies).grid(row=3, column=2, **pad)
        tk.Label(self.tab_quan_ly, text="Mỗi cửa sổ xử lý 1 video (tải + gộp). Đóng cửa sổ "
                 "khi xong, hoặc đóng = hủy theo dõi (job vẫn lưu trong lịch sử).\n"
                 "Cookie: KHÔNG login trong tool — login 1 lần trong trình duyệt rồi export cookies.txt "
                 "bằng Get cookies.txt LOCALLY, import vào ô trên. Cookie Bilibili chỉ dùng cho Bilibili "
                 "(yt-dlp + API phụ đề); cookie của web AI (nếu có) là riêng từng web, không dùng chung.",
                 fg="gray", wraplength=600, justify="left").grid(
            row=4, column=0, columnspan=3, sticky="w", **pad)

        # ---- (v7.5) Luong 1 mach: dan link -> lay SRT goc -> DUNG.
        # UU TIEN SO 1 la tai duoc file SRT GOC tieng Trung ve thu muc
        # du an (cau tu quang vao AI ben ngoai de dich); dich trong
        # tool chi la tuy chon sau do. Tai xong thi DUNG HAN, chi bao
        # duong dan file + hien 2 nut cho cau chon tiep (khong tu
        # chuyen tab, khong tu chay dich).
        f_1mach = tk.LabelFrame(
            self.tab_quan_ly,
            text=" Lấy phụ đề (1 mạch: dán link → tải SRT gốc) ",
            padx=8, pady=6)
        f_1mach.grid(row=5, column=0, columnspan=3, sticky="ew", **pad)
        tk.Label(f_1mach, text="Link phim Bilibili:").grid(
            row=0, column=0, sticky="w", **pad)
        self.link_1mach_var = tk.StringVar(value="")
        tk.Entry(f_1mach, textvariable=self.link_1mach_var).grid(
            row=0, column=1, sticky="ew", **pad)
        tk.Button(f_1mach, text="Dán",
                  command=self._dan_link_1mach).grid(row=0, column=2, **pad)
        self.btn_1mach = tk.Button(
            f_1mach, text="LẤY PHỤ ĐỀ + DỊCH + ĐỌC (1 mạch)",
            font=("", 11, "bold"), command=self.bam_luong_1_mach)
        self.btn_1mach.grid(row=1, column=0, columnspan=3, sticky="ew", **pad)
        self.tu_dich_1mach_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            f_1mach,
            text="Tự dịch sau khi lấy phụ đề (mặc định TẮT — cậu dịch bằng AI bên ngoài)",
            variable=self.tu_dich_1mach_var).grid(
                row=2, column=0, columnspan=3, sticky="w", **pad)
        self.status_1mach_var = tk.StringVar(
            value="Dán link rồi bấm nút — tải SRT gốc xong thì dừng, cậu chọn tiếp.")
        tk.Label(f_1mach, textvariable=self.status_1mach_var, fg="gray",
                 wraplength=900, justify="left").grid(
                     row=3, column=0, columnspan=3, sticky="w", **pad)
        hang_sau_tai = tk.Frame(f_1mach)
        hang_sau_tai.grid(row=4, column=0, columnspan=3, sticky="ew", **pad)
        self.btn_sau_tai_dich = tk.Button(
            hang_sau_tai, text="Dịch trong tool",
            command=self._sau_tai_dich, state="disabled")
        self.btn_sau_tai_dich.pack(side="left", padx=4)
        self.btn_sau_tai_doc = tk.Button(
            hang_sau_tai, text="Mở tab HoaiMy",
            command=self._sau_tai_doc, state="disabled")
        self.btn_sau_tai_doc.pack(side="left", padx=4)
        self.log_1mach = scrolledtext.ScrolledText(f_1mach, height=6,
                                                   state="disabled")
        self.log_1mach.grid(row=5, column=0, columnspan=3, sticky="nsew",
                            **pad)
        f_1mach.grid_columnconfigure(1, weight=1)
        self._srt_1mach = ""
        self._job_1mach = None

        self.tab_quan_ly.grid_columnconfigure(1, weight=1)
        # (v7.6) minsize 370: label chi tiet 5-7 dong (~124px) +
        # Treeview 170 + scrollbar + hang nut 38 = ~351px; nho
        # hon la hang nut roi xuong duoi mep frame va bi cat mat.
        self.tab_quan_ly.grid_rowconfigure(1, weight=1, minsize=370)
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
        self._xay_bang_du_an()

    def _xay_bang_du_an(self):
        """(v7.6) Xay lai bang lich su du an dang Treeview cot co
        dinh: Ten phim | Link | Trang thai | Duong dan luu thu muc
        | Phu de. Moi dong chi hien gia tri DA RUT GON (co "…"),
        gia tri day du luu o job + hien o label chi tiet duoi bang
        khi chon dong, khong mat. Truong nao quet khong ra thi de
        TRONG, khong doan. Khong xay lai khi chi chon dong (chon
        dong chi goi _khi_chon_du_an) de khong mat vi tri cuon."""
        tree = getattr(self, "tree_du_an", None)
        if tree is None:
            return
        try:
            chon_cu = self.job_da_chon_id
            for iid in list(tree.get_children()):
                tree.delete(iid)
            for r, job in enumerate(doc_jobs()):
                jid = job.get("id") or ("dong-%d" % r)
                ten = job.get("title") or ""
                link = job.get("link") or ""
                tt = dinh_dang_trang_thai(job.get("status") or "moi")
                # (v7.6) Khong fallback ve outdir: job chua co folder
                # thi hien "(chua co thu muc)" chu khong gia vo da co
                # thu muc phim (loi .srt roi thang vao thu muc goc).
                folder = job.get("folder") or ""
                if job.get("has_subtitle") is True:
                    ten_srt = os.path.basename(job.get("subtitle_file") or "")
                    pd = "Có" + ((" - " + rut_gon_chu(ten_srt, 30))
                                 if ten_srt else "")
                elif job.get("has_subtitle") is False:
                    pd = "Không"
                else:
                    pd = ""
                tree.insert("", "end", iid=jid, values=(
                    rut_gon_chu(ten, 40),
                    rut_gon_link(link),
                    tt,
                    rut_gon_duong_dan(folder) if folder
                    else "(chưa có thư mục)",
                    pd))
            if chon_cu and tree.exists(chon_cu):
                tree.selection_set(chon_cu)
                tree.see(chon_cu)
            self._hien_chi_tiet_du_an(self._lay_job_da_chon())
            self._cap_nhat_nut_hanh_dong()
        except Exception:
            return

    def _lay_job_da_chon(self):
        """Job cua dong dang chon trong Treeview (theo
        job_da_chon_id). Tra None neu chua chon."""
        jid = getattr(self, "job_da_chon_id", None)
        if not jid:
            return None
        for job in doc_jobs():
            if job.get("id") == jid:
                return job
        return None

    def _hien_chi_tiet_du_an(self, job):
        """(v7.6) Hien DAY DU gia tri cua dong dang chon o label
        duoi bang (ten/link/thu muc/duong dan file .srt day du),
        vi trong bang chi hien ban rut gon."""
        var = getattr(self, "chi_tiet_du_an_var", None)
        if var is None:
            return
        if not job:
            var.set("Chưa chọn dự án nào — bấm 1 dòng trong bảng "
                    "để xem đầy đủ.")
            return
        srt = job.get("subtitle_file") or ""
        var.set("Tên phim: %s\nLink: %s\nThư mục: %s\nPhụ đề: %s"
                % (job.get("title") or "(chưa có tên)",
                   job.get("link") or "(chưa có link)",
                   job.get("folder") or "(chưa có thư mục)",
                   srt or "Chưa có file phụ đề"))

    def _cap_nhat_nut_hanh_dong(self):
        """(v7.6) Bat/tat hang nut duoi bang theo dong dang chon:
        chua chon thi tat het; co phu de that thi nut Dich, khong
        thi nut Them phu de; da xong thi tat nut Lam lai."""
        job = self._lay_job_da_chon()
        co_job = job is not None
        co_srt = bool(job and job.get("subtitle_file")
                      and os.path.isfile(job.get("subtitle_file")))
        da_xong = bool(job and (job.get("status") or "moi") == "xong")
        for ten_nut in ("btn_mo_thu_muc_du_an", "btn_mo_thu_muc_phu_de",
                        "btn_lam_lai_du_an", "btn_dich_phu_de_du_an",
                        "btn_xoa_du_an"):
            nut = getattr(self, ten_nut, None)
            if nut is None:
                continue
            nut.configure(state="normal" if co_job else "disabled")
        nut_pd = getattr(self, "btn_mo_thu_muc_phu_de", None)
        if nut_pd is not None:
            nut_pd.configure(state="normal" if co_srt else "disabled")
        nut_lam = getattr(self, "btn_lam_lai_du_an", None)
        if nut_lam is not None:
            nut_lam.configure(
                state="disabled" if (not co_job or da_xong) else "normal")
        nut_dich = getattr(self, "btn_dich_phu_de_du_an", None)
        if nut_dich is not None:
            nut_dich.configure(
                text="Dịch phụ đề" if co_srt else "Thêm phụ đề")

    def _khi_chon_du_an(self, event=None):
        """Bam 1 lan: chon dong, cap nhat job_da_chon_id + label
        chi tiet + nut hanh dong. KHONG xay lai bang."""
        tree = getattr(self, "tree_du_an", None)
        if tree is None:
            return
        chon = tree.selection()
        if not chon:
            return
        self.job_da_chon_id = chon[0]
        self._hien_chi_tiet_du_an(self._lay_job_da_chon())
        self._cap_nhat_nut_hanh_dong()

    def _mo_doi_du_an(self, event=None):
        """Bam dup: mo lai cua so job cua dong duoi con tro."""
        tree = getattr(self, "tree_du_an", None)
        if tree is None:
            return
        try:
            iid = tree.identify_row(event.y) if event is not None else ""
        except Exception:
            iid = ""
        if not iid:
            return
        self.job_da_chon_id = iid
        job = self._lay_job_da_chon()
        if job:
            self.mo_cua_so_job(job)

    def _dich_hoac_them_phu_de_du_an(self):
        """Nut Dich/Them phu de duoi bang: co file .srt that thi
        dich, khong thi them file ngoai (dung logic cu)."""
        job = self._lay_job_da_chon()
        if not job:
            return
        if job.get("subtitle_file") and os.path.isfile(
                job.get("subtitle_file")):
            self._dich_phu_de_du_an(job)
        else:
            self._them_phu_de_du_an(job)

    def _mo_thu_muc_phu_de(self, job):
        """(v7.6) Mo thu muc chua file .srt va CHON DUNG file do
        (explorer /select,). File import tay co the nam ngoai thu
        muc du an nen nut nay khong dung thu muc du an."""
        p = (job or {}).get("subtitle_file") or ""
        if not p or not os.path.isfile(p):
            messagebox.showinfo(
                "Chưa có phụ đề",
                "Dự án này chưa có file phụ đề.\n"
                "Bấm 'Thêm phụ đề' để tự import file .srt ngoài vào.")
            return
        if mo_file_trong_explorer(p):
            return
        thu_muc = os.path.dirname(p)
        if thu_muc and os.path.isdir(thu_muc):
            if not mo_thu_muc(thu_muc):
                messagebox.showinfo("Đường dẫn phụ đề", p)
        else:
            messagebox.showinfo("Đường dẫn phụ đề", p)

    def _chon_du_an(self, jid):
        self.job_da_chon_id = jid
        tree = getattr(self, "tree_du_an", None)
        if tree is not None and jid and tree.exists(jid):
            tree.selection_set(jid)
            tree.see(jid)
        self._hien_chi_tiet_du_an(self._lay_job_da_chon())
        self._cap_nhat_nut_hanh_dong()

    def _mo_thu_muc_du_an(self, job):
        folder = (job or {}).get("folder") or (job or {}).get("outdir") or ""
        if not folder or not os.path.isdir(folder):
            messagebox.showinfo("Chưa có thư mục", "Dự án này chưa có thư mục lưu.")
            return
        if not mo_thu_muc(folder):
            messagebox.showinfo("Đường dẫn lưu", folder)

    def _lam_lai_du_an(self, job):
        """Mo lai cua so job de tiep tuc tai/gop (chi dung khi chua xong)."""
        if not job:
            return
        if (job.get("status") or "") == "xong":
            messagebox.showinfo("Đã xong", "Dự án này đã hoàn thành rồi.")
            return
        self.job_da_chon_id = job.get("id")
        self.mo_cua_so_job(job)

    def _xoa_du_an(self, job):
        if not job:
            return
        if not messagebox.askyesno("Xóa dự án",
                                   "Xóa dự án này khỏi lịch sử?\n%s"
                                   % (job.get("title") or "(chưa có tên)")):
            return
        try:
            win = self.cua_so_mo.pop(job.get("id"), None)
            if win is not None:
                try:
                    win.da_dong = True
                    win.destroy()
                except Exception:
                    pass
        except Exception:
            pass
        jobs = [j for j in doc_jobs() if j.get("id") != job.get("id")]
        luu_jobs(jobs)
        if self.job_da_chon_id == job.get("id"):
            self.job_da_chon_id = None
        self.cap_nhat_bang()

    def _dich_phu_de_du_an(self, job):
        p = (job or {}).get("subtitle_file") or ""
        if not p or not os.path.isfile(p):
            messagebox.showinfo("Chưa có phụ đề",
                                "Dự án này chưa có file phụ đề.\nBấm 'Thêm phụ đề' để tự import file .srt ngoài vào.")
            return
        self.mo_tab_xu_ly_phu_de(srt_path=p, job=job)

    def _them_phu_de_du_an(self, job):
        """(v7.0, phu luc 1) Cot Phu de trong -> nut Them phu de: chon
        file .srt ngoai, luu duong dan vao job (khong copy, khong ghi
        de file goc), cap nhat cot Phu de thanh Co + ten file, roi mo
        tab Xu ly phu de voi file do da nap san."""
        p = them_phu_de_tu_ngoai(job, self)
        if not p:
            return
        self.cap_nhat_bang()
        self.mo_tab_xu_ly_phu_de(srt_path=p, job=job)

    def chon_tab_quan_ly(self):
        """(v7.4) Chuyen ve tab Quan ly trong Notebook."""
        try:
            self.notebook.select(self.tab_quan_ly)
        except Exception:
            pass

    def mo_tab_xu_ly_phu_de(self, srt_path=None, job=None):
        """(v7.4) Chuyen sang tab Xu ly phu de trong Notebook (1 cua
        so duy nhat, khong mo Toplevel). Nap file SRT neu co.
        Dong tab khong dung luong dich dang chay: worker luu tien
        trinh vao dich-phu-de-...json."""
        panel = getattr(self, "panel_xu_ly", None)
        if panel is None:
            return None
        if job is not None:
            panel.job = job
        if srt_path and os.path.isfile(srt_path):
            try:
                panel.srt_var.set(srt_path)
                panel._nap_srt(srt_path)
            except Exception:
                pass
        self.notebook.select(self.tab_xu_ly)
        return panel

    def mo_tab_doc_phu_de(self, srt_path=None, job=None):
        """(v7.4) Chuyen sang tab Doc phu de HoaiMy trong Notebook (1
        cua so duy nhat, khong mo Toplevel). Nap file SRT neu co.
        Dong tab khong mat tien trinh: worker luu tien-trinh.json,
        mo lai bam Tiep tuc."""
        panel = getattr(self, "panel_doc", None)
        if panel is None:
            return None
        if job is not None:
            panel.job = job
        if srt_path and os.path.isfile(srt_path):
            try:
                panel.e_srt.delete(0, "end")
                panel.e_srt.insert(0, srt_path)
                panel._nap_danh_sach_cau(srt_path)
            except Exception:
                pass
        self.notebook.select(self.tab_doc)
        return panel

    # ---- (v7.5) Luong 1 mach ----
    def _dan_link_1mach(self):
        try:
            text = self.clipboard_get().strip()
        except tk.TclError:
            text = ""
        tim_url = re.search(r"https?://\S+", text) if text else None
        self.link_1mach_var.set(
            tim_url.group(0).strip() if tim_url
            else (text.splitlines()[0].strip() if text else ""))

    def _ghi_log_1_mach(self, s):
        try:
            self.after(0, lambda: self._ghi_log_1_mach_truc_tiep(s))
        except Exception:
            pass

    def _ghi_log_1_mach_truc_tiep(self, s):
        try:
            self.log_1mach.config(state="normal")
            self.log_1mach.insert("end", s + "\n")
            self.log_1mach.see("end")
            self.log_1mach.config(state="disabled")
        except Exception:
            pass

    def bam_luong_1_mach(self):
        """(v7.5) Bat dau luong 1 mach: tao job moi tu link, chay
        nen. Buoc 1 (tai SRT goc) luon chay, khong can key Gemini;
        dich chi chay khi cong tac tu dich dang BAT."""
        url = self.link_1mach_var.get().strip()
        if not url or "BV" not in url:
            messagebox.showerror("Thiếu link",
                                 "Dán link Bilibili (BV...) vào trước đã.")
            return
        outdir = self.outdir_var.get().strip()
        if not outdir:
            messagebox.showerror("Thiếu thư mục", "Chưa chọn thư mục lưu.")
            return
        job = {"id": str(uuid.uuid4())[:8], "title": "", "link": url,
               "status": "moi", "pct_tai": 0, "pct_gop": 0,
               "tu_gop": True, "xoa_goc": True,
               "giam_15": True, "tu_gop_ytdlp": True,
               "dich_ten": True, "tu_nhan_dien": True,
               "tu_dich_sau_lay_phu_de": bool(self.tu_dich_1mach_var.get()),
               "has_subtitle": None, "subtitle_langs": [],
               "subtitle_file": "", "subtitle_vi_file": "", "folder": ""}
        self._job_1mach = job
        self.cap_nhat_job(job)
        self.btn_1mach.config(state="disabled")
        self.btn_sau_tai_dich.config(state="disabled")
        self.btn_sau_tai_doc.config(state="disabled")
        self.status_1mach_var.set("Đang chạy luồng 1 mạch...")
        self._ghi_log_1_mach("Bắt đầu luồng 1 mạch: %s" % url)
        threading.Thread(target=self._luong_1_mach_worker,
                         args=(job, outdir), daemon=True).start()

    def _luong_1_mach_worker(self, job, outdir):
        log = self._ghi_log_1_mach
        url = job.get("link") or ""
        cookies = self.cookies_var.get().strip()
        try:
            log("Bước 0: Đọc thông tin video...")
            info = kiem_tra_link(url, cookies)
            ten_viet = ten_phim_tieng_viet(
                info.get("title") or "video",
                dich=job.get("dich_ten", True))
            folder = tao_thu_muc_duy_nhat(outdir, ten_viet)
            job["title"] = ten_viet
            job["folder"] = folder
            if info.get("duration") is not None:
                job["duration"] = info.get("duration")
            try:
                self.after(0, lambda: self.cap_nhat_job(job))
            except Exception:
                pass
            log("Bước 0 xong: %s -> %s" % (info.get("title"), folder))
            try:
                pd = kiem_tra_phu_de(url, cookies)
                langs = pd.get("languages", []) or []
            except Exception:
                langs = []
            log("Quét phụ đề: %s"
                % (("có: " + ", ".join(langs)) if langs
                   else "không thấy (vẫn thử tải)"))
            ket = chay_luong_1_mach(
                url, folder, ten_viet, cookies, langs,
                job.get("tu_dich_sau_lay_phu_de", False), log)
            job["subtitle_file"] = ket.get("srt_goc") or ""
            job["has_subtitle"] = True if ket.get("srt_goc") else False
            if ket.get("da_dich"):
                job["subtitle_vi_file"] = ket.get("srt_viet") or ""
                job["subtitle_status"] = "da_dich"
            elif ket.get("srt_goc"):
                job["subtitle_status"] = "da_tai_goc"
            job["status"] = "da_kiem_tra"
            self.after(0, self._luong_1_mach_xong, job, ket)
        except Exception as e:
            self.after(0, self._luong_1_mach_loi, job, str(e))

    def _luong_1_mach_xong(self, job, ket):
        self.btn_1mach.config(state="normal")
        self.cap_nhat_job(job)
        if ket.get("srt_goc"):
            self._srt_1mach = ket["srt_goc"]
            self._job_1mach = job
            self.btn_sau_tai_dich.config(state="normal")
            self.btn_sau_tai_doc.config(state="normal")
            if ket.get("da_dich"):
                self.status_1mach_var.set(
                    "Đã tải + dịch xong: %s — chọn tiếp hoặc bấm Mở tab HoaiMy."
                    % os.path.basename(ket["srt_goc"]))
                messagebox.showinfo(
                    "Luồng 1 mạch xong",
                    "Đã tải SRT gốc + dịch xong, lưu đè file gốc (có .bak):\n%s\n\n"
                    "Bấm 'Mở tab HoaiMy' để lấy giọng đọc, hoặc 'Dịch trong "
                    "tool' để xem/sửa bản dịch." % ket["srt_goc"])
            elif ket.get("buoc_dung") == "dich":
                self.status_1mach_var.set(
                    "Đã tải SRT gốc nhưng DỊCH LỖI — file gốc còn nguyên: %s"
                    % os.path.basename(ket["srt_goc"]))
                messagebox.showwarning(
                    "Đã tải SRT gốc — dịch lỗi",
                    "Đã tải SRT gốc:\n%s\n\nDỊCH LỖI: %s\nFile gốc còn "
                    "nguyên, không mất. Bấm 'Dịch trong tool' để dịch lại "
                    "hoặc dịch thủ công." % (ket["srt_goc"], ket.get("loi") or ""))
            else:
                self.status_1mach_var.set(
                    "Đã tải SRT gốc: %s — dừng tại đây, cậu chọn tiếp."
                    % os.path.basename(ket["srt_goc"]))
                messagebox.showinfo(
                    "Đã tải SRT gốc",
                    "File SRT gốc:\n%s\n\nĐã DỪNG tại đây — không tự dịch, "
                    "không tự chuyển tab. Bấm 'Dịch trong tool' để dịch "
                    "trong tool, hoặc 'Mở tab HoaiMy' để lấy giọng đọc."
                    % ket["srt_goc"])
        else:
            self.status_1mach_var.set(
                "Không có phụ đề: %s" % (ket.get("loi") or ""))
            messagebox.showinfo(
                "Không có phụ đề",
                "Không lấy được phụ đề cho video này.\n%s\n\nKhông tạo "
                "file SRT nào." % (ket.get("loi") or ""))

    def _luong_1_mach_loi(self, job, msg):
        self.btn_1mach.config(state="normal")
        self.status_1mach_var.set("Luồng 1 mạch lỗi: " + msg)
        self._ghi_log_1_mach("Luồng 1 mạch LỖI: " + msg)
        messagebox.showerror("Luồng 1 mạch lỗi", msg)

    def _sau_tai_dich(self):
        if getattr(self, "_srt_1mach", "") and os.path.isfile(self._srt_1mach):
            self.mo_tab_xu_ly_phu_de(srt_path=self._srt_1mach,
                                     job=self._job_1mach)

    def _sau_tai_doc(self):
        if getattr(self, "_srt_1mach", "") and os.path.isfile(self._srt_1mach):
            self.mo_tab_doc_phu_de(srt_path=self._srt_1mach,
                                   job=self._job_1mach)

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
               "tu_gop": True, "xoa_goc": True,
               "giam_15": True, "tu_gop_ytdlp": True,
               "dich_ten": True, "tu_nhan_dien": True,
               "tu_dich_sau_lay_phu_de": False,
               "has_subtitle": None, "subtitle_langs": [],
               "subtitle_file": "", "subtitle_vi_file": "", "folder": ""}
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
        jid = getattr(self, "job_da_chon_id", None)
        if not jid:
            messagebox.showinfo("Chưa chọn", "Chọn một dự án trong bảng lịch sử trước đã.")
            return None
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
        if job:
            self._xoa_du_an(job)

    # ---------- cập nhật (v6.2) ----------
    def bam_kiem_tra_cap_nhat(self):
        """Nút Kiểm tra cập nhật: (v6.7) repo đã public nên KHÔNG cần
        token GitHub nữa, ấn là kiểm tra luôn trên GitHub Releases.
        Token cũ nếu đã lưu thì vẫn kèm theo cho đỡ giới hạn lượt gọi
        API, không có token thì vẫn kiểm tra được."""
        token = lay_token_github()
        threading.Thread(target=self._cap_nhat_worker,
                         args=(token,), daemon=True).start()

    def _cap_nhat_worker(self, token):
        try:
            ket_qua = kiem_tra_cap_nhat(token)
            self.after(0, self._cap_nhat_xong, ket_qua)
        except Exception as e:
            self.after(0, self._cap_nhat_loi, str(e))

    def _cap_nhat_xong(self, ket_qua):
        if not ket_qua:
            messagebox.showinfo("Đã là bản mới nhất",
                                "Bạn đang dùng bản mới nhất: v%s." % VERSION)
            return
        ver_moi = ket_qua["version_moi"]
        if not ket_qua.get("tai_url"):
            messagebox.showinfo(
                "Có bản mới: v%s" % ver_moi,
                "Đã có bản v%s nhưng bản này chưa có file exe đính kèm "
                "trên Release.\n\nTải bản cài đặt mới tại:\n%s"
                % (ver_moi, GITHUB_RELEASES_URL))
            return
        if not messagebox.askyesno(
                "Có bản mới: v%s" % ver_moi,
                "Bản đang dùng: v%s → Bản mới: v%s.\n\n"
                "Bấm Có để tải exe mới về và vá lên bản đang dùng "
                "(không cần cài lại, giữ nguyên lịch sử job + cài đặt). "
                "Tool sẽ tự thoát rồi mở lại bản mới."
                % (VERSION, ver_moi)):
            return
        token = lay_token_github()
        threading.Thread(target=self._tai_ban_moi_worker,
                         args=(ket_qua["tai_url"], token),
                         daemon=True).start()

    def _cap_nhat_loi(self, msg):
        if msg == "CHUA_CO_TOKEN":
            return
        if "401" in msg or "Bad credentials" in msg:
            if messagebox.askyesno(
                    "Token không đúng",
                    "Token GitHub đã lưu không dùng được (sai hoặc hết hạn).\n\n"
                    "Bấm Có để nhập token mới, bấm Không để hủy."):
                luu_token_github("")
                self.bam_kiem_tra_cap_nhat()
            return
        messagebox.showerror(
            "Không kiểm tra được cập nhật",
            msg + "\n\nBản đang dùng: v%s.\nLấy bản mới bằng tay tại:\n%s"
            % (VERSION, GITHUB_RELEASES_URL))

    def _tai_ban_moi_worker(self, tai_url, token):
        try:
            bat_path = tai_ban_moi_va_cap_nhat(tai_url, token)
            self.after(0, self._tai_ban_moi_xong, bat_path)
        except Exception as e:
            self.after(0, self._tai_ban_moi_loi, str(e))

    def _tai_ban_moi_xong(self, bat_path):
        # Chạy script cập nhật (chờ tool thoát rồi thay exe + mở lại).
        try:
            subprocess.Popen(["cmd", "/c", bat_path],
                             **chay_ngam_kwargs())
        except Exception:
            subprocess.Popen(bat_path, shell=True, **chay_ngam_kwargs())
        messagebox.showinfo(
            "Đang cập nhật...",
            "Đã tải xong bản mới. Tool sẽ thoát ngay, script cập nhật sẽ "
            "thay exe cũ bằng exe mới rồi tự mở lại tool.")
        try:
            self.destroy()
        finally:
            os._exit(0)

    def _tai_ban_moi_loi(self, msg):
        messagebox.showerror(
            "Tải bản mới thất bại",
            msg + "\n\nLấy bản mới bằng tay tại:\n" + GITHUB_RELEASES_URL)

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

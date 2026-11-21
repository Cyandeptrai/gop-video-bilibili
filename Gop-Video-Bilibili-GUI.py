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
cat bang outpoint khi tran slot), luon re-encode ve MP3 chuan 44100 Hz
stereo 192k libmp3lame (v7.12), kiem tra do dai file ra bang ffprobe;
loi ffmpeg ghi day
du vao ffmpeg-loi.log. Edge TTS co timeout 120s/cau (asyncio.
wait_for), het gio thi failover luot sau; nut Huy dung duoc that
sau cau dang doc. Duong dan dai Windows: thao tac file cua Python
dung tien to \\\\?\\ khi can, ffmpeg thi khong (ffmpeg co the khong
hieu). Khong doi giao dien, ten file ra, tien-trinh.json, che do
Gop/Tung cau rieng/Ca hai.
v7.15 (2 COT EN/VI LUON HIEN + JSON TU NHAN MODE - CYAN 20/11):
Tab Voice for YouTube Faceless LUON co 2 cot song song (EN trai, VI
phai), moi cot co setting rieng giong tab SRT Reader (giong/toc do/
cao do/nghi giua cue/re-time/tu dong toc do), tien do % + cue hien
tai + file ra rieng tung cot. JSON dan vao co truong "mode" /
"languages" / "choice" o cap cao nhat: tool TU NHAN che do (dual /
en_only / vi_only) va TU BAT/TAT cot tuong ung — khong tick tay.
Khong co truong mode thi suy ra tu khoa en/vi co trong JSON.
Mode co trong JSON thang khoa phu (en_only ma co ca vi thi bo vi,
log ro). Che do song song v7.14 van giu: BAT = 2 luong doc lap,
TAT = tuan tu — nhung KHONG ghi de mode JSON (en_only thi cot VI
van tat du song song co BAT). JSON schema khong doi ngoai 2 truong
mode/languages them o cap cao nhat.
v7.16 (DOI THOAI CO GIOI TINH + GOI LAI CHO CHUA XU LY - CYAN 20/11):
JSON them "voice_mode" ("single" = 1 giong, "dialogue" = 2 giong) o cap
cao nhat; moi speaker co "character" (vd co gai / chang trai) va
"gender" ("female"/"male") — gioi tinh trong JSON thang mac dinh
(vd co gai hoi = A nu, chang trai dap = B nam, du mac dinh cu la
A nam / B nu). Tool canh bao neu gioi tinh nhan vat khong khop
giong da chon, KHONG tu doi giong. Cue Edge loi thi GHI VAO danh
sach "Giong chua xu ly" rieng tung cot EN/VI (cue/speaker/nhan
vat/gioi tinh/loi/so lan thu), co nut "Goi lai cho chua xu ly" va
"Goi lai 1 cue da chon" — goi lai dung giong/gioi tinh goc, chi
khi danh sach rong moi duoc goi la xong (MP3/SRT final chi xuat
khi het cue chua xu ly). Giong may local (SAPI) CHI khi anh BAT
tay cong tac rieng tung cot (mac dinh TAT): Edge loi roi moi doc
bang local va ghi ro trong log + danh sach. Khong doi cac tab cu.
v7.14 (CHE DO SONG SONG EN+VI - CYAN 20/11): them cong tac bat/tat
"Che do song song EN+VI" trong tab Voice for YouTube Faceless (mac
dinh TAT = lam tuan tu EN roi VI, an toan nhat lan dau). BAT: EN va VI
chay 2 luong doc lap (2 thread rieng), moi ben co trang thai / tien do
/ log / thu muc tam / file ra rieng; dung/huy/loi 1 ben KHONG anh
huong ben kia. Luong VI lech 2 giay khi bat dong thoi de giam nguy co
Edge TTS bi gioi han toc do; so luong toi da chinh duoc 1 hoac 2.
JSON KHONG doi (dual {en, vi} van la format chinh). Khong doi cac tab cu.
v7.13 (TAB VOICE FOR YOUTUBE FACELESS - CYAN 20/11): them tab moi
"Voice for YouTube Faceless" trong Notebook (1 cua so, khong Toplevel).
Format CHINH la DUAL JSON 1 file chua ca Anh + Viet:
{en:{voice_settings, script_text, srt_cues}, vi:{...}} - dan 1 lan,
EN va VI la 2 KICH BAN DOC LAP (chi chung 1 key/chu de, moi ban
viet theo phong cach/nhip ke rieng cho khan gia tung nuoc, KHONG
phai dich y het tung cau, KHONG ep timing/chuong 2 ban giong nhau).
tool xuat ca 2 MP3 + 2 SRT final (EN + VI). JSON 1 ngon ngu van duoc
chap nhan lam fallback. Giong mac dinh: EN = Helio nam My
(avocado_v2:MAI_03, giong noi bo cua Muse - KHONG chay native tren
Windows, tab anh xa sang en-US-ChristopherNeural va log ro viec nay;
audio Helio day du chi tao duoc trong chat Muse), VI = HoaiMy nu
(vi-VN-HoaiMyNeural). Doc tung cue SRT mot (khong doc mot hoi),
nghi ngan giua cac cue, do thoi luong that tung cue roi CAN LAI SRT
(re-time) cho khop audio that, gop MP3 ve chuan 44100/stereo/192k/
libmp3lame (giong v7.12). Toc do toi da 1.35x, atempo that, giu cao
do. Moi buoc tu dong deu co cong tac bat/tat. Khong doi hanh vi cac
tab cu, khong lam thumbnail (CYAN tu thiet ke sau).
v7.8 (TU BAM NUT IDM - CYAN 19/11): IDM hien hop thoai "Tep thuc thi
chinh cua IDM bi hong", nut "Tiep tuc tai xuong (4)" bi mo, dem nguoc
vai giay moi sang de bam duoc. Them cong tac (mac dinh TAT, luu
config chung) "Tu bam 'Tiep tuc tai xuong' tren hop thoai IDM" o
khung "Cac buoc tu dong" trong cua so job: bat thi sau khi day link
sang IDM xong, tool chay luong nen canh hop thoai IDM toi da 60s
(poll 0.5s), doi nut sang (enabled) roi bam ho 1 lan duy nhat bang
Win32 user32 qua ctypes (KHONG them dependency moi); het 60s khong
thay hop/nut thi log ro roi dung, khong treo tool; cau bam tay truoc
(hop da dong) thi luong tu dung, khong bam lai; chi xu ly cua so IDM
xuat hien SAU lan day link gan nhat (chup hwnd truoc khi day, loai
tru cua so cu). Chi bam dung nut "Tiep tuc tai xuong", khong bam
"Mo trang web IDM" hay nut khac. LUU Y: day chi la bam ho nut doi
dem nguoc, KHONG sua duoc loi IDM bi hong — muon het han thi cai de
ban IDM moi nhat (ghi ro trong tooltip). Moi loi deu log vao nhat
ky, khong chet im, khong hien hop thoai chan.

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
import html
import io
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

try:
    import webview as _pywebview  # (v7.17) cua so web AI trong tool
except Exception:
    _pywebview = None  # Linux / may chua cai: nut Mo web AI bao ro

try:
    import numpy as np  # (v7.21) tach AI (MDX-Net)
except Exception:
    np = None  # Linux / may chua cai: nut Tach AI bao loi ro

# (v7.0) Ten hien thi cua app gop la ChipChipStudio, NHUNG APP_TITLE
# van giu "Chipchipdownload" vi luong cap nhat (kiem_tra_cap_nhat)
# tim asset theo APP_TITLE + ".exe" - doi ten exe se lam hong nut
# Cap nhat. Chi co 1 luong cap nhat duy nhat (cua ChipChip).
APP_TITLE = "Chipchipdownload"
STUDIO_TITLE = "ChipChipStudio"
# (v7.24-merge 21/11 ~21:35): them engine VieNeu vao tab Doc phu de + tab Voice Faceless
# (snippet /tmp/v724/vieneu_snippet.py) + parse JSON Canh 1 tuong thich field tieng Viet
# trong postman2d.py. Khong doi kien truc module postman2d.py da co.
VERSION = "7.26"
# (v7.24, CYAN 21/11 ~21:29): PostmanStudio 2D — làm video YouTube
# faceless bằng tool local, KHÔNG dùng iCast nữa. Thêm VieNeu
# (Xuân Vĩnh chính, Phạm Tuyên dự phòng, nút "Tải tài nguyên" nếu
# chưa có) + tab mới "Postman 2D" (module postman2d.py đi kèm):
# dán JSON kịch bản -> tự nhận/chia cảnh, mỗi cảnh có ô prompt
# tạo video Postman + chọn nhân vật tham chiếu đã lưu, JSON có
# SRT tạo voice đồng nhất với cảnh. Thêm tab "Tạo nhân vật"
# (21/11 ~21:33): chỉnh thông số code + xem trước ngay + lưu
# theo tên (nhan_vat_postman.json, dùng chung với Postman 2D);
# thẻ tag @Tên trong prompt Postman: tool thay tag bằng mô tả
# nhân vật đã lưu trước khi gửi, tag lạ thì báo rõ, không bịa.
# BỎ HẲN tự mở lại cửa sổ cũ
# khi khởi động (xóa vòng lặp doc_jobs/mo_cua_so_job cuối
# QuanLy.__init__): mở tool chỉ mở 1 cửa sổ chính duy nhất.
# Build exe: postman2d.py phải đi kèm exe (cùng thư mục) + thêm
# hidden import Pillow; vieneu import lười trong postman2d.py
# (pip install vieneu trên máy CYAN, KHÔNG bundle model vào exe).
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
# (v7.21) Tach AI (MDX-Net): onnxruntime + numpy PHAI co trong
# build exe (pip install onnxruntime; numpy di kem onnxruntime).
# onnxruntime import luoi trong ham (lazy) nen PyInstaller KHONG
# tu thay duoc — build PHAI them --collect-all onnxruntime
# (onnxruntime co .dll/.so + du lieu rieng; chi hidden-import
# khong du). Model .onnx KHONG bundle trong exe (tai 1 lan o
# muc Tai nguyen AI trong tool).
# (v7.6) Model dich phu de — KHONG hardcode trong ham goi API nua,
# lay tu config (nguoi dung chon/go o tab Xu ly phu de).
# Gemini 2.5-flash DA DEPRECATED, tat 01/12/2026: TUYET DOI khong
# dung nua. Mac dinh Gemini = 3.8-flash, du phong = 3.5-flash-lite.
MODEL_GEMINI_MAC_DINH = "gemini-3.8-flash"
MODEL_GEMINI_DU_PHONG = "gemini-3.5-flash-lite"
MODEL_GPT_MAC_DINH = "gpt-4o-mini"
MODEL_CLAUDE_MAC_DINH = "claude-sonnet-4-5"
# (v7.17) Model tu dong (Auto): thu lan luot model con dung duoc
# (gemini-3.8-flash roi gemini-3.5-flash-lite); model nao loi thi
# bo qua. TUYET DOI khong dung gemini-2.5-flash (tat 01/12/2026).
MODEL_TU_DONG = "Tự động (Auto)"
# (v7.17) Dich bang web AI: mo trang Gemini ngay trong tool
# (pywebview / Edge WebView2 co san tren Windows 10/11).
GEMINI_WEB_URL = "https://gemini.google.com"
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


def _python_he_thong():
    """(v7.25, SỬA LỖI GỐC nhân bản vô hạn — bản tương đương hàm cùng
    tên trong postman2d.py, vì 2 file độc lập; v7.26 KIỂM CHỨNG ứng
    viên) Trả đường dẫn Python hệ thống để chạy pip, KHÔNG BAO GIỜ
    dùng sys.executable khi đã đóng gói: trong bản exe PyInstaller,
    sys.executable CHÍNH LÀ Chipchipdownload.exe — chạy
    [sys.executable, "-m", ...] sẽ mở thêm 1 bản tool thay vì chạy
    Python.
    - Chưa đóng gói (chạy .py): trả sys.executable.
    - Đã đóng gói (frozen): thử từng ứng viên theo thứ tự
      ("py", "python", "python3") trên Windows, ("python3",
      "python", "py") ngoài Windows ("py" là Python Launcher,
      không có stub Microsoft Store nên ưu tiên trước trên
      Windows); mỗi ứng viên PHẢI qua kiểm chứng
      [ứng_viên, "--version"] (ẩn console, timeout 10s): chỉ
      chấp nhận khi returncode == 0 VÀ "Python 3" có trong
      stdout+stderr — stub Microsoft Store (in câu "Python was
      not found...", exit != 0) bị loại. Hết ứng viên → trả None
      (người gọi PHẢI báo rõ và KHÔNG spawn gì)."""
    if not getattr(sys, "frozen", False):
        return sys.executable
    if os.name == "nt":
        thu_tu = ("py", "python", "python3")
    else:
        thu_tu = ("python3", "python", "py")
    try:
        kw = chay_ngam_kwargs()
    except Exception:
        kw = {}
    for ten in thu_tu:
        try:
            p = shutil.which(ten)
        except Exception:
            p = None
        if not p:
            continue
        try:
            r = subprocess.run([p, "--version"], capture_output=True,
                               text=True, timeout=10, **kw)
        except Exception:
            continue
        if r.returncode == 0 and "Python 3" in ((r.stdout or "")
                                                + (r.stderr or "")):
            return p
    return None


# (v7.26) Thông báo khi máy chưa có Python thật + nhận diện lỗi do
# chạy phải stub Microsoft Store (không phải lỗi mạng).
THIEU_PYTHON_THAT = ("Máy chưa có Python thật (chỉ có đường tắt "
                     "Microsoft Store) — tải Python ở python.org/downloads, "
                     "lúc cài nhớ tick 'Add Python to PATH', cài xong mở "
                     "lại tool rồi bấm lại nút này.")


def _loi_thieu_python_that(text):
    """True nếu output/lỗi pip là do chạy phải stub Microsoft Store
    (máy chưa có Python thật) chứ không phải lỗi mạng."""
    t = str(text or "")
    return ("Python was not found" in t or "Microsoft Store" in t)


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


def video_yeu_thich_path():
    """(v7.21) File luu danh sach video yeu thich o tab Duyet video:
    video-yeu-thich.json trong thu muc config cua tool (cung cho
    voi config.json, canh exe)."""
    return os.path.join(app_dir(), "video-yeu-thich.json")


def doc_video_yeu_thich():
    """(v7.21) Doc file yeu thich -> dict {bvid: muc} voi muc gom
    bvid, title, author, link, pic, duration, play, pubdate,
    ngay_danh_dau. File khong co / hong / sai dang -> {} (khong
    crash, khong doan)."""
    try:
        with open(video_yeu_thich_path(), "r", encoding="utf-8") as f:
            du_lieu = json.load(f)
    except Exception:
        return {}
    if not isinstance(du_lieu, dict):
        return {}
    ket_qua = {}
    for bvid, muc in du_lieu.items():
        if not isinstance(muc, dict) or not bvid:
            continue
        muc = dict(muc)
        muc["bvid"] = bvid
        ket_qua[bvid] = muc
    return ket_qua


def luu_video_yeu_thich(cac_muc):
    """(v7.21) Ghi danh sach yeu thich XUONG FILE theo cach ATOMIC
    (ghi file .tmp + fsync + os.replace, nhu luu progress dich phu
    de): thoat tool giua chung / ghi hong thi file cu van nguyen.
    Tra ve True neu ghi duoc."""
    try:
        duong_dan = video_yeu_thich_path()
        duong_tam = duong_dan + ".tmp"
        with open(duong_tam, "w", encoding="utf-8") as f:
            json.dump(cac_muc or {}, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(duong_tam, duong_dan)
        return True
    except Exception:
        return False


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
        # (v7.8) Gop bu cau loi sau khi xuat xong: mac dinh BAT, doi
        # 60s cho may chu het chan 429 roi goi lai chi cau loi, toi
        # da 1 vong bu; cau loi qua so lan thi doc bang giong may
        # local (mac dinh TAT — giong Windows se khac giong HoaiMy).
        "gop_bu_cau_loi": True, "gop_bu_doi_giay": 60,
        "cau_loi_dung_giong_may": False,
        # (v7.8) Toc do: gop nhieu cau vao 1 lan goi Edge TTS (mac
        # dinh 1 = goi tung cau nhu cu); goi song song (mac dinh TAT)
        # + so luong (2-20, mac dinh 3); che do may chu/local (mac
        # dinh "may_chu_goi_lai_sau" = hanh vi cu: Edge loi thi de
        # Luot 2/gop bu goi lai sau, khong dung giong may).
        "so_cau_gop_1_lan_goi": 1,
        "goi_song_song": False, "so_luong_song_song": 3,
        "che_do_may_chu_local": "may_chu_goi_lai_sau",
        # (v7.8) Cau tran slot khi gop: "cat" (mac dinh, hanh vi cu:
        # cat duoi) / "de" (phan tran phat nho duoi dau cau sau).
        "cau_tran_che_do": "cat",
        # (v7.18) Tron nhac nen khi doc (tab Doc phu de): mac dinh
        # TAT; am luong giong doc / nhac nen mac dinh 100/100, KHONG
        # goi y. File nen KHONG luu config — dien mac dinh theo tung
        # phim (file <ten>_nen-tach.mp3 trong thu muc phim, neu co).
        "tron_nhac_khi_doc": False,
        "tron_nhac_vol_voice": 100, "tron_nhac_vol_nen": 100,
        # (v7.23) Tach + long mot lan (tab Doc phu de): mac dinh
        # TAT; am luong giong goc mac dinh 0% (khong tron giong goc
        # — giu hanh vi cu); dinh dang file gop cuoi mac dinh MP3.
        "tach_nen_truoc_khi_doc": False,
        "tron_nhac_vol_giong_goc": 0, "tron_nhac_dinh_dang": "MP3",
        # (v7.21) Tach AI (tab Xu ly am thanh): thu muc chua model
        # AI (file .onnx). Rong = mac dinh <thu muc luu>\TaiNguyenAI
        # (thu muc luu la thu muc CYAN chon, KHONG ep o C:).
        "ai_tach_thu_muc": "",
        # (v7.22) Thiet bi tach AI: "tu_dong" (mac dinh: GPU neu co,
        # khong thi CPU) / "cpu" / "gpu". Luu rieng theo chuc nang
        # (muc Cai dat GPU) — sau nay them chuc nang GPU thi them
        # khoa gpu_thiet_bi_<ten chuc nang> tuong tu.
        "ai_tach_thiet_bi": "tu_dong",
        "phu_de_provider": "Gemini", "gemini_api_key": "",
        "openai_api_key": "", "anthropic_api_key": "",
        # (v7.6) Che do dich + model tung nha cung cap (luu local).
        # che_do: "toan_bo" (mac dinh, 1 prompt duy nhat) / "cum"
        # (chi chia cum 20 cau). Model de trong thi dung mac dinh
        # o tren; nguoi dung duoc go model khac o tab Xu ly phu de.
        "phu_de_che_do": "toan_bo",
        "phu_de_model_gemini": MODEL_TU_DONG,
        "phu_de_model_gemini_du_phong": MODEL_GEMINI_DU_PHONG,
        "phu_de_model_gpt": MODEL_GPT_MAC_DINH,
        "phu_de_model_claude": MODEL_CLAUDE_MAC_DINH,
        "phu_de_the_loai": "", "phu_de_nhan_vat": "",
        "phu_de_xung_ho": "", "phu_de_boi_canh": "",
        # (v7.8) Tu bam nut "Tiep tuc tai xuong" tren hop thoai IDM
        # (IDM bao file chay chinh bi hong, bat doi dem nguoc):
        # MAC DINH TAT, luu config chung (khong theo job). Chi bam
        # ho nut doi dem nguoc, KHONG sua duoc loi IDM bi hong.
        "idm_tu_bam_tiep_tuc": False,
        # (v7.9) Duyet video - giai doan 1 (tim theo tu khoa): tu tai
        # anh bia ket qua ve hien o hang ket qua. MAC DINH BAT; tat
        # thi chi hien khung cho "Anh bia" (khong tai anh).
        "duyet_video_tu_tai_anh_bia": True,
        # (v7.13) Voice for YouTube Faceless: luu theo project.
        "ytf_ngon_ngu": "en", "ytf_giong_en": "Helio (nam, Mỹ)",
        "ytf_giong_vi": "Xuân Vĩnh (VieNeu, nam Bắc)",
        "ytf_toc_do": 1.0, "ytf_cao_do": 0,
        "ytf_tu_dong_retime": True,
        "ytf_tu_dong_toc_do": True, "ytf_toc_do_toi_da": 1.35,
        "ytf_nghi_giua_cue_ms": 350,
        "ytf_thu_muc_luu": "",
        # (v7.14) Che do song song EN+VI: mac dinh TAT (tuan tu).
        "ytf_song_song": False, "ytf_dong_bo_toi_da": 2,
        # (v7.15) Setting RIENG tung cot EN/VI (2 cot luon hien).
        "ytf_giong_b_en": "Aria (nữ, Mỹ)", "ytf_giong_b_vi": "NamMinh (nam)",
        "ytf_toc_do_en": 1.0, "ytf_toc_do_vi": 1.0,
        "ytf_cao_do_en": 0, "ytf_cao_do_vi": 0,
        "ytf_nghi_en_ms": 350, "ytf_nghi_vi_ms": 350,
        "ytf_retime_en": True, "ytf_retime_vi": True,
        "ytf_tu_dong_toc_do_en": True, "ytf_tu_dong_toc_do_vi": True,
        # (v7.16) Cho dung giong may local (SAPI) khi Edge loi o tab
        # Voice: MAC DINH TAT — cau loi chi goi lai bang Edge.
        "ytf_cho_dung_giong_may_en": False, "ytf_cho_dung_giong_may_vi": False,
        # (v7.24) Postman 2D: giọng VieNeu (không phải Edge).
        # Xuân Vĩnh = chính, Phạm Tuyên = dự phòng (cả 2 Bắc/nam/
        # Natural; SDK vieneu pin "3.8.5", 25 preset — README
        # v3.7.1 cũ chỉ có 23 giọng, mặc định Minh Quân).
        "postman_giong_vi": "Xuân Vĩnh (nam, Bắc)",
        "postman_giong_vi_du_phong": "Phạm Tuyên (nam, Bắc)",
        "postman_toc_do": 0.95, "postman_vieneu_da_tai": False,
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
    cookies, khong hoi cookies moi). (v7.21) Get cookies.txt LOCALLY
    ghi cookie HttpOnly dang '#HttpOnly_.bilibili.com' — SESSDATA
    chinh la HttpOnly — nen GIU lai dong nay (cat tien to) chu khong
    bo nhu dong chu thich '#' thuong (loi cu bo mat SESSDATA)."""
    ket_qua = {}
    try:
        with open(cookies_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#") and not line.startswith("#HttpOnly_"):
                    continue
                if line.startswith("#HttpOnly_"):
                    line = line[len("#HttpOnly_"):]
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


def _ten_thu_muc_phim_cua_job(job):
    """(v7.8) Ten thu muc phim cua 1 job, theo dung cong tac dich
    ten cua job do (dich_ten=True mac dinh: dung ten tieng Viet da
    dich; False: giu nguyen ten goc). Dung chung cho them phu de
    tay va don job cu."""
    tieu_de = ((job or {}).get("title") or "").strip()
    return ten_phim_tieng_viet(tieu_de, dich=(job or {}).get("dich_ten", True))


def _thu_muc_phim_co_san(outdir, ten):
    """(v7.8) Thu muc phim cho job CU / them phu de tay: neu thu muc
    dung ten phim DA CO SAN (vd video da tai vao do truoc, job chi
    chua luu folder) thi dung luon thu muc do — khong tao ban
    "- YYYY-MM-DD HH-MM-SS" nhu tao_thu_muc_duy_nhat (tranh 1 phim
    tach thanh 2 thu muc). Chi tao moi khi chua co thu muc nao."""
    thu_muc = os.path.join(outdir, sanitize_ten(ten))
    if os.path.isdir(thu_muc):
        return thu_muc
    return tao_thu_muc_duy_nhat(outdir, ten)


def don_phu_de_ve_thu_muc_phim(job, outdir=None, log=None):
    """(v7.8) Don job CU (tao tu v7.5 tro ve): file .srt dang nam
    thang o goc thu muc luu thi MOVE vao thu muc phim moi theo ten
    phim (theo cong tac dich_ten cua job), cap nhat job["folder"],
    job["subtitle_file"] (+ "subtitle_vi_file" neu co), tao
    link.txt, luu job. Chi move khi file cha TRUC TIEP la outdir;
    file da nam trong thu muc con nao do thi de yen. Ten dich trung
    thi them (1), (2)... khong ghi de. Tra ve True neu da don (co
    thay doi), False neu khong can / khong don duoc. Ghi log dong
    "Đã dọn phụ đề vào thư mục phim: <duong dan moi>" khi don xong."""
    def _log(s):
        if log:
            try:
                log(s)
            except Exception:
                pass
    if not job or job.get("folder"):
        return False
    out = outdir or job.get("outdir") or ""
    if not out or not os.path.isdir(out):
        return False
    out_abs = os.path.abspath(out)
    folder = None
    da_don = False
    for khoa in ("subtitle_file", "subtitle_vi_file"):
        p = job.get(khoa) or ""
        if not p or not os.path.isfile(p):
            continue
        if os.path.dirname(os.path.abspath(p)) != out_abs:
            continue
        if folder is None:
            ten = _ten_thu_muc_phim_cua_job(job)
            if not ten:
                ten = os.path.splitext(os.path.basename(p))[0]
            try:
                # (v7.10) 1 thu muc duy nhat: dung lai thu muc da co
                # (ten Viet hoac ten goc), doi ten ve ten Viet neu
                # duoc — thay cho _thu_muc_phim_co_san chi biet ten
                # Viet.
                folder, _da_tao = _thu_muc_phim_duy_nhat(
                    out, ten, (job or {}).get("title") or "",
                    job=job, url=job.get("link") or "", log=_log)
            except Exception as e:
                _log("Không tạo được thư mục phim để dọn phụ đề: %s" % e)
                return da_don
            job["folder"] = folder
        dich = os.path.join(folder, os.path.basename(p))
        if os.path.abspath(dich) != os.path.abspath(p):
            goc, ext = os.path.splitext(os.path.basename(p))
            n = 1
            while os.path.isfile(dich):
                dich = os.path.join(folder, "%s (%d)%s" % (goc, n, ext))
                n += 1
            try:
                shutil.move(p, dich)
            except Exception as e:
                _log("Không dọn được %s: %s" % (p, e))
                continue
        job[khoa] = dich
        da_don = True
    if da_don:
        try:
            if job.get("link"):
                luu_link_phim(folder, job["link"])
        except Exception:
            pass
        cap_nhat_job_trong_jobs(job)
        _log("Đã dọn phụ đề vào thư mục phim: %s" % folder)
    return da_don


def them_phu_de_tu_ngoai(job, parent=None, outdir=None):
    """(v7.8, phu luc 1) Them phu de thu cong cho 1 du an khi cot Phu de
    dang trong (khong tai duoc / khong tim duoc phu de).
    Mo hop chon file .srt, COPY file vao thu muc phim (tao thu muc
    phim truoc neu job chua co, theo dung cong tac dich_ten cua job),
    cap nhat job tro duong dan MOI trong thu muc phim + tao link.txt.
    File goc ngoai kia GIU NGUYEN (khong xoa, khong ghi de). Ten dich
    trung thi them (1), (2)... Tra ve duong dan moi trong thu muc
    phim hoac '' neu huy. Neu khong xac dinh duoc thu muc luu thi
    giu hanh vi cu: chi luu duong dan file ngoai vao job.
    Khong doan noi dung phu de."""
    p = filedialog.askopenfilename(
        title="Chọn file phụ đề .srt để thêm cho dự án",
        filetypes=[("Phụ đề SRT", "*.srt"), ("Mọi file", "*.*")])
    if not p:
        return ""
    job = job or {}
    folder = job.get("folder") or ""
    if not folder or not os.path.isdir(folder):
        out = outdir or job.get("outdir") or ""
        if not out or not os.path.isdir(out):
            job["subtitle_file"] = p
            job["has_subtitle"] = True
            job["subtitle_status"] = "da_them_tay"
            if not job.get("subtitle_langs"):
                job["subtitle_langs"] = []
            cap_nhat_job_trong_jobs(job)
            return p
        try:
            # (v7.10) 1 thu muc duy nhat: dung lai thu muc da co
            # (ten Viet hoac ten goc), doi ten ve ten Viet neu duoc
            # — thay cho _thu_muc_phim_co_san chi biet ten Viet.
            folder, _da_tao = _thu_muc_phim_duy_nhat(
                out, _ten_thu_muc_phim_cua_job(job) or
                os.path.splitext(os.path.basename(p))[0],
                (job or {}).get("title") or "", job=job,
                url=job.get("link") or "", log=None)
        except Exception:
            job["subtitle_file"] = p
            job["has_subtitle"] = True
            job["subtitle_status"] = "da_them_tay"
            if not job.get("subtitle_langs"):
                job["subtitle_langs"] = []
            cap_nhat_job_trong_jobs(job)
            return p
        job["folder"] = folder
    dich = os.path.join(folder, os.path.basename(p))
    if os.path.abspath(dich) != os.path.abspath(p):
        goc, ext = os.path.splitext(os.path.basename(p))
        n = 1
        while os.path.isfile(dich):
            dich = os.path.join(folder, "%s (%d)%s" % (goc, n, ext))
            n += 1
        try:
            shutil.copyfile(p, dich)
        except Exception:
            job["subtitle_file"] = p
            job["has_subtitle"] = True
            job["subtitle_status"] = "da_them_tay"
            if not job.get("subtitle_langs"):
                job["subtitle_langs"] = []
            cap_nhat_job_trong_jobs(job)
            return p
    try:
        if job.get("link"):
            luu_link_phim(folder, job["link"])
    except Exception:
        pass
    job["subtitle_file"] = dich
    job["has_subtitle"] = True
    job["subtitle_status"] = "da_them_tay"
    if not job.get("subtitle_langs"):
        job["subtitle_langs"] = []
    cap_nhat_job_trong_jobs(job)
    return dich


# ---------------- dich phu de qua API ----------------

PROMPT_DICH_WEB_AI_MAC_DINH = """Bạn là dịch giả phụ đề phim chuyên nghiệp, dịch từ tiếng Trung sang tiếng Việt.

NHIỆM VỤ 1 — NHẬN DẠNG LOẠI PHIM TRƯỚC KHI DỊCH:
Đọc toàn bộ phụ đề gốc bên dưới trước, rồi tự xác định:
- Thể loại chính: tu tiên, sinh tồn, hệ thống, hay kết hợp (ví dụ: tu tiên + hệ thống, sinh tồn + hệ thống).
- Bối cảnh: thời Hồng Hoang, huyền huyễn, hư không, ngoài Tam Giới, ngoài Địa Đạo, hỗn độn, dị giới, hiện đại, mạt thế... Tự nhận dạng bối cảnh của từng shot từng cảnh dựa trên thoại
- Nhân vật chính, Tên phiên âm, quan hệ và vai vế giữa các nhân vật, giới tính, tuổi tác, nếu có
- Xưng hô phù hợp cho từng nhân vật dùng tên hoặc (anh/em, ta/ngươi, sư huynh/sư muội, cậu/tớ...) dựa trên bản dịch, và giữ nhất quán suốt file. Khi xưng hô có dùng tên nhân vật thì dùng tên đã phiên âm sang tiếng Việt, nhất quán một kiểu suốt file, không lúc tên này lúc tên khác, không lẫn tên gốc tiếng Trung với tên phiên âm.
- Giọng điệu chung của phim: xem cốt truyện để tự nhận ra — tùy tình huống các cảnh sẽ có cảm xúc giọng điệu nghiêm túc, hài hước, căng thẳng, nhẹ nhàng, hay bất kỳ giọng điệu nào khác mà cốt truyện thể hiện, không bó buộc trong mấy kiểu liệt kê sẵn.
Không cần viết phần nhận dạng này ra — chỉ dùng nó để dịch cho đúng ngữ cảnh.

sau khi nhận dạng ở nhiệm vụ một đã đúc kết ra cách dịch phụ đề đúng theo logic trên ta là nhiệm vụ 2.
NHIỆM VỤ 2 — DỊCH TOÀN BỘ PHỤ ĐỀ:
Dịch TOÀN BỘ các câu phụ đề gốc sang tiếng Việt, theo đúng bối cảnh, thể loại, tính cách, cảm xúc và tình huống từng câu, nghe tự nhiên như người Việt nói, không dịch word-by-word khô cứng.

QUY TẮC BẮT BUỘC:
- Trả về ĐÚNG định dạng SRT gốc, giữ nguyên số thứ tự và timestamp từng câu, chỉ thay phần lời thoại bằng tiếng Việt. Không thêm, không bớt câu, không gộp/tách câu, không giải thích thêm, không viết gì ngoài SRT.
- Thuật ngữ tu tiên / hệ thống / sinh tồn (ví dụ: hệ thống, nhiệm vụ, điểm, cấp bậc, linh lực, tu vi, đan điền...) dịch nhất quán một kiểu suốt file, không lúc kiểu này lúc kiểu khác.
- Xưng hô đúng vai vế và giới tính đã nhận dạng ở trên, nhất quán suốt file. Tên nhân vật phiên âm sang tiếng Việt một kiểu duy nhất suốt file, không đổi cách phiên âm giữa chừng, không lẫn tên gốc tiếng Trung với tên phiên âm.
- Khi nhân vật và tình huống cho phép, dùng các từ teencode hài hước của Việt Nam, câu trêu nhau, châm chọc vui giữa các nhân vật — càng tự nhiên, càng tốt. Chỉ dùng khi hợp tính cách và mạch truyện, không biến câu nghiêm túc thành câu đùa.
- Các từ chửi: khi nhân vật chửi trong bản gốc thì dịch đúng mức độ, dùng từ chửi tiếng Việt tự nhiên như người Việt chửi thật, không làm nhẹ, không lược bỏ, không thay bằng từ lịch sự. Chỉ chửi khi bản gốc có chửi, không tự thêm từ chửi vào câu vốn không có.
- Thả thính: khi nhân vật tán tỉnh / thả thính trong bản gốc thì dịch đúng kiểu thả thính tiếng Việt tự nhiên, giữ nguyên độ ngọt, độ trêu, không làm nhạt đi, không giảng đạo hay né tránh.
- Thơ văn hài hước người Việt hay dùng: khi nhân vật và tình huống cho phép, dùng thơ văn, câu vần, đối đáp hài hước kiểu người Việt hay dùng (thơ chế, câu đối vui, vần điệu trêu nhau) để câu thoại nghe duyên và vui hơn — chỉ dùng khi hợp tính cách và mạch truyện, không gượng ép vào câu nghiêm túc.
- Nếu gặp câu khó hiểu vì thiếu ngữ cảnh, dịch theo nghĩa hợp lý nhất với mạch truyện, không bỏ trống, không bịa thêm tình tiết.

Tôi đã đính kèm file SRT bên trên"""


class _ApiWebAI:
    """(v7.17) API cho nut Huy trong cua so web AI (pywebview js_api):
    nut Huy bam -> dong cua so web, dung luon."""
    def __init__(self):
        self.cua_so = None

    def huy(self):
        try:
            if self.cua_so is not None:
                self.cua_so.destroy()
        except Exception:
            pass


_JS_NUT_HUY_WEB_AI = """(function(){
  function themNut(){
    if (document.getElementById('chipchip-nut-huy')) return;
    if (!document.body) return;
    var b = document.createElement('button');
    b.id = 'chipchip-nut-huy';
    b.type = 'button';
    b.textContent = 'H\u1ee7y \u2014 \u0111\u00f3ng c\u1eeda s\u1ed5 web AI';
    b.style.cssText = 'position:fixed;top:10px;right:12px;z-index:2147483647;'
      + 'background:#c0392b;color:#fff;border:0;border-radius:8px;'
      + 'padding:8px 14px;font-size:14px;font-weight:bold;cursor:pointer;'
      + 'box-shadow:0 2px 8px rgba(0,0,0,.4);';
    b.addEventListener('click', function(){
      try {
        if (window.pywebview && window.pywebview.js_api
            && window.pywebview.js_api.huy) {
          window.pywebview.js_api.huy();
        } else { window.close(); }
      } catch (e) { window.close(); }
    });
    document.body.appendChild(b);
  }
  themNut();
  setInterval(themNut, 2000);
})();"""


def _them_nut_huy_web_ai(win):
    """(v7.17) Chen nut Huy (goc phai tren) vao trang Gemini trong
    cua so web; tu them lai neu trang tu render lai lam mat nut."""
    try:
        win.evaluate_js(_JS_NUT_HUY_WEB_AI)
    except Exception:
        pass


def doc_cookies_txt_web_ai(duong_dan):
    """(v7.17) Doc file cookies.txt dang Netscape/Mozilla (Get
    cookies.txt LOCALLY xuat tu Chrome): moi dong:
    domain<TAB>flag<TAB>path<TAB>secure<TAB>expires<TAB>name<TAB>value.
    Domain co tien to #HttpOnly_ nghia la cookie HttpOnly. Bo dong
    trong + dong chu thich (#, tru #HttpOnly_). Tra ve list dict
    {domain, path, secure, expires, name, value, httponly}."""
    out = []
    with open(duong_dan, "r", encoding="utf-8", errors="replace") as f:
        for dong in f:
            dong = dong.rstrip("\r\n")
            if not dong.strip():
                continue
            if dong.startswith("#") and not dong.startswith("#HttpOnly_"):
                continue
            httponly = False
            if dong.startswith("#HttpOnly_"):
                httponly = True
                dong = dong[len("#HttpOnly_"):]
            phan = dong.split("\t")
            if len(phan) < 7:
                phan = dong.split()
            if len(phan) < 7:
                continue
            domain, _flag, path, secure, expires, name, value = phan[:7]
            try:
                expires_i = int(expires)
            except Exception:
                expires_i = 0
            out.append({"domain": domain, "path": path or "/",
                        "secure": secure.strip().upper() == "TRUE",
                        "expires": expires_i, "name": name,
                        "value": value, "httponly": httponly})
    return out


def _ap_cookie_web_ai(win, cac_cookie):
    """(v7.17) Ap list cookie (doc tu cookies.txt) vao cua so web AI
    qua CookieManager cua WebView2 (pywebview 6.2: win.native.browser
    .webview.CoreWebView2.CookieManager; CreateCookie + AddOrUpdate
    Cookie — ap duoc ca cookie HttpOnly, khac voi document.cookie
    cua JS). Chi chay tren ban Windows (can WebView2). Tra ve
    (so_cookie_da_ap, thong_bao_loi): loi rong neu ap duoc it nhat
    1 cookie; 0 cookie + loi neu khong toi duoc CookieManager."""
    try:
        goc = getattr(win, "native", None)
        trinh_duyet = getattr(goc, "browser", None) if goc is not None else None
        webview2 = getattr(trinh_duyet, "webview", None) if trinh_duyet is not None else None
        core = getattr(webview2, "CoreWebView2", None) if webview2 is not None else None
        mgr = getattr(core, "CookieManager", None) if core is not None else None
        if mgr is None:
            return 0, ("không tới được CookieManager của WebView2 "
                       "(cửa sổ web chưa khởi tạo xong)")
        dem = 0
        for ck in (cac_cookie or []):
            try:
                cookie = mgr.CreateCookie(ck["name"], ck["value"],
                                          ck["domain"], ck["path"])
                try:
                    cookie.IsSecure = bool(ck.get("secure"))
                except Exception:
                    pass
                try:
                    cookie.IsHttpOnly = bool(ck.get("httponly"))
                except Exception:
                    pass
                try:
                    import clr  # pythonnet, co san khi pywebview chay
                    from System import DateTime
                    het_han = int(ck.get("expires") or 0)
                    if het_han > 0:
                        cookie.Expires = DateTime(
                            1970, 1, 1).AddSeconds(het_han)
                except Exception:
                    pass
                mgr.AddOrUpdateCookie(cookie)
                dem += 1
            except Exception:
                continue
        if dem <= 0:
            return 0, "CookieManager không nhận cookie nào"
        return dem, ""
    except Exception as e:
        return 0, str(e)


def _dat_cookie_js_web_ai(win, cac_cookie):
    """(v7.17) Du phong khi khong ap duoc qua CookieManager: dat
    cookie KHONG HttpOnly bang document.cookie (JS). Cookie HttpOnly
    (vd SID dang nhap Google) KHONG dat duoc cach nay — van can dang
    nhap tay 1 lan trong cua so. Tra so cookie da dat."""
    dat = [c for c in (cac_cookie or []) if not c.get("httponly")]
    if not dat:
        return 0
    dong = []
    for c in dat:
        gia_tri = ("document.cookie = %s;"
                   % json.dumps("%s=%s; domain=%s; path=%s%s"
                                % (c["name"], c["value"], c["domain"],
                                   c["path"] or "/",
                                   "; Secure" if c.get("secure") else "")))
        dong.append(gia_tri)
    try:
        win.evaluate_js("\n".join(dong))
    except Exception:
        return 0
    return len(dat)


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
    mac_dinh = {"Gemini": MODEL_TU_DONG,
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
    (v7.17) Gemini mac dinh "Tự động (Auto)": thu lan luot
    gemini-3.8-flash roi gemini-3.5-flash-lite, model nao loi thi
    bo qua; chon tay 1 model thi thu model do, loi thi thu 1 lan
    voi model du phong. KHONG dung gemini-2.5-flash (deprecated,
    tat 01/12/2026). Muse = tro ly Muse (chat tay):
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
        # (v7.17) Auto = thu lan luot model con dung duoc; chon tay
        # 1 model thi thu model do, loi thi thu du phong 1 lan.
        model_chon = (model or "").strip() or MODEL_TU_DONG
        if model_chon == MODEL_TU_DONG:
            thu = [MODEL_GEMINI_MAC_DINH, MODEL_GEMINI_DU_PHONG]
        elif model_chon == MODEL_GEMINI_DU_PHONG:
            thu = [MODEL_GEMINI_DU_PHONG]
        else:
            thu = [model_chon, MODEL_GEMINI_DU_PHONG]
        loi_cuoi = None
        for i, m in enumerate(thu):
            try:
                return _goi_gemini_once(m, key, prompt, timeout)
            except Exception as e:
                loi_cuoi = e
                if i + 1 < len(thu) and log:
                    log("Gemini %s lỗi (%s) — thử lại với model %s."
                        % (m, e, thu[i + 1]))
        raise loi_cuoi
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


def luu_link_phim(folder, url):
    """(v7.8) Ghi link phim day du vao file link.txt trong thu muc
    phim (moi thu muc phim chi co 1 link). Goi ngay sau khi tao
    thu muc phim o moi duong tai (tai phu de, luong 1 mach, tai
    video IDM/yt-dlp, them phu de tay, don job cu). Neu link.txt
    da co thi ghi de bang link hien tai. Tra ve duong dan file
    hoac '' neu thieu du lieu / loi ghi."""
    if not folder or not (url or "").strip():
        return ""
    try:
        os.makedirs(folder, exist_ok=True)
        duong_file = os.path.join(folder, "link.txt")
        with open(duong_file, "w", encoding="utf-8") as f:
            f.write((url or "").strip() + "\n")
        return duong_file
    except Exception:
        return ""


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


def _link_trong_thu_muc_khop(folder, url):
    """link.txt trong folder (neu co) co phai link phim hien tai
    khong? Dung de phan biet 2 phim khac nhau nhung TRUNG TEN (vd
    2 video khac nhau cung ten): trung ten nhung khac link thi KHONG
    duoc dung chung thu muc. Khong co link.txt -> coi nhu khop (thu
    muc cu chua co link). So sanh sau khi chuan hoa link (bo ?p= va
    tham so theo doi) nen cac phan cua cung 1 phim van chung 1 thu
    muc."""
    if not url:
        return True
    try:
        p = os.path.join(folder, "link.txt")
        if not os.path.isfile(p):
            return True
        with open(p, encoding="utf-8") as f:
            return (chuan_hoa_link_bilibili(f.read().strip())
                    == chuan_hoa_link_bilibili((url or "").strip()))
    except Exception:
        return True


def _thu_muc_phim_theo_link(outdir, url, ten_viet):
    """(v7.10) Tim thu muc phim trong outdir theo NOI DUNG link.txt
    (khong theo ten): thu muc nao co link.txt trung link hien tai
    thi chinh la thu muc cua phim nay — ke ca khi ten thu muc la
    ten goc (buoc truoc dich loi) hay ten Viet (buoc truoc dich
    duoc). Tra ve duong dan thu muc, uu tien thu muc da mang dung
    ten dich; khong co thi tra ''. Chi quet thu muc con cap 1."""
    if not outdir or not url or not os.path.isdir(outdir):
        return ""
    chuan = chuan_hoa_link_bilibili((url or "").strip())
    khop = []
    try:
        muc = os.listdir(outdir)
    except Exception:
        return ""
    for ten in muc:
        duong = os.path.join(outdir, ten)
        if not os.path.isdir(duong):
            continue
        try:
            p = os.path.join(duong, "link.txt")
            if not os.path.isfile(p):
                continue
            with open(p, encoding="utf-8") as f:
                if (chuan_hoa_link_bilibili(f.read().strip())
                        == chuan):
                    khop.append(duong)
        except Exception:
            continue
    if not khop:
        return ""
    khop.sort()
    for duong in khop:
        if os.path.basename(duong.rstrip(os.sep)) == sanitize_ten(
                ten_viet or "video"):
            return duong
    return khop[0]


def _thu_muc_phim_duy_nhat(outdir, ten_viet, ten_goc, job=None, url="",
                           log=None):
    """(v7.10) Tra ve DUY NHAT 1 thu muc phim cho 1 phim trong outdir.

    NGUYEN NHAN LOI v7.9: moi duong tao thu muc (tai phu de, luong
    1 mach, tai video IDM/yt-dlp, gop, don job cu) deu goi
    ten_phim_tieng_viet() rieng — ham nay goi Google Translate
    truc tiep va LANG LE tra ve ten goc (tieng Trung) khi dich loi
    (mat mang / bi chan / het luot). Cung 1 phim, buoc truoc dich
    duoc -> thu muc ten Viet (co link.txt), buoc sau dich loi ->
    thu muc ten Trung (co phu de): 2 thu muc cho 1 phim. Ham nay
    gom moi viec tinh thu muc vao 1 cho duy nhat, theo thu tu:
    1) job["folder"] da co tren dia -> dung luon (day la thu muc
       cua dung job nay).
    2) Quet outdir theo link.txt: thu muc nao co link trung link
       hien tai thi dung luon — bat ke ten Viet hay ten Trung (doi
       ten ve ten Viet neu duoc). Buoc nay bat ca truong hop lan
       goi hien tai dich loi nen ten_viet truyen vao da la ten
       Trung, trong khi buoc truoc da tao thu muc ten Viet.
    3) outdir/<ten_viet> da co + link khop (hoac khong co link.txt)
       -> dung luon (khong tao them "<ten> - ngay-gio" nhu
       tao_thu_muc_duy_nhat).
    4) chi con outdir/<ten_goc> + link khop (buoc truoc dich loi
       nen tao nham thu muc ten Trung) -> doi ten sang <ten_viet>
       neu duoc (dung 1 thu muc ten Viet nhu CYAN muon); doi ten
       loi (vd IDM dang tai vao do) thi dung luon thu muc goc,
       khong tao thu muc thu 2.
    5) chua co gi -> tao moi bang ten dich (theo cong tac dich_ten)
       qua tao_thu_muc_duy_nhat.
    Ghi link.txt (neu co url) vao thu muc tra ve trong moi truong
    hop. Tra ve (folder, da_tao_moi). Neu co job thi cap nhat
    job["folder"] = folder. Thu muc ten Viet nhung link KHAC (2
    phim trung ten) thi KHONG dung chung — roi xuong buoc 5 tao
    thu muc moi (co them ngay-gio)."""
    def _log(s):
        if log:
            try:
                log(s)
            except Exception:
                pass
    ten_viet = sanitize_ten(ten_viet or "video")
    ten_goc = sanitize_ten(ten_goc or "")
    folder_cu = ((job or {}).get("folder") or "").strip()
    if folder_cu and os.path.isdir(folder_cu):
        if url:
            luu_link_phim(folder_cu, url)
        if job is not None:
            job["folder"] = folder_cu
        return folder_cu, False
    if not outdir or not os.path.isdir(outdir):
        raise RuntimeError("Chưa chọn thư mục lưu.")
    if url:
        tim = _thu_muc_phim_theo_link(outdir, url, ten_viet)
        if tim:
            # Chi doi ten khi dich that su thanh cong (ten_viet khac
            # ten_goc): neu lan goi nay dich loi thi ten_viet truyen
            # vao da la ten Trung — doi ten thu muc Viet sang Trung
            # lai la sai, chi dung luon thu muc tim duoc.
            if (ten_goc and ten_goc != ten_viet
                    and os.path.basename(tim.rstrip(os.sep)) != ten_viet):
                duong_viet = os.path.join(outdir, ten_viet)
                if not os.path.exists(duong_viet):
                    try:
                        os.rename(tim, duong_viet)
                        _log("Đã đổi tên thư mục phim về tên tiếng "
                             "Việt: %s" % duong_viet)
                        tim = duong_viet
                    except Exception as e:
                        _log("Không đổi tên được thư mục phim sang "
                             "tên tiếng Việt (%s) — dùng luôn thư mục "
                             "cũ." % e)
            luu_link_phim(tim, url)
            if job is not None:
                job["folder"] = tim
            return tim, False
    duong_viet = os.path.join(outdir, ten_viet)
    if os.path.isdir(duong_viet) and _link_trong_thu_muc_khop(
            duong_viet, url):
        if url:
            luu_link_phim(duong_viet, url)
        if job is not None:
            job["folder"] = duong_viet
        return duong_viet, False
    if ten_goc and ten_goc != ten_viet:
        duong_goc = os.path.join(outdir, ten_goc)
        if os.path.isdir(duong_goc) and _link_trong_thu_muc_khop(
                duong_goc, url):
            try:
                os.rename(duong_goc, duong_viet)
                _log("Đã đổi tên thư mục phim về tên tiếng Việt: %s"
                     % duong_viet)
                if url:
                    luu_link_phim(duong_viet, url)
                if job is not None:
                    job["folder"] = duong_viet
                return duong_viet, False
            except Exception as e:
                _log("Không đổi tên được thư mục phim sang tên tiếng "
                     "Việt (%s) — dùng luôn thư mục cũ." % e)
                if url:
                    luu_link_phim(duong_goc, url)
                if job is not None:
                    job["folder"] = duong_goc
                return duong_goc, False
    folder = tao_thu_muc_duy_nhat(outdir, ten_viet)
    if url:
        luu_link_phim(folder, url)
    if job is not None:
        job["folder"] = folder
    return folder, True


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
    # (v7.10) 1 thu muc duy nhat cho 1 phim (xem
    # _thu_muc_phim_duy_nhat) — dung lai / doi ten thay vi tao moi.
    folder, _da_tao = _thu_muc_phim_duy_nhat(
        outdir, ten, info["title"], url=url, log=log)
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
    dùng cho IDM. Trả về '' nếu không đọc được / không có cookie.
    (v7.21) Giu lai dong '#HttpOnly_' (cat tien to) vi SESSDATA la
    HttpOnly — loi cu bo het dong '#' nen mat SESSDATA, API Bilibili
    coi nhu chua dang nhap."""
    cookies = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#") and not line.startswith("#HttpOnly_"):
                    continue
                if line.startswith("#HttpOnly_"):
                    line = line[len("#HttpOnly_"):]
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
    # (v7.10) 1 thu muc duy nhat cho 1 phim (xem
    # _thu_muc_phim_duy_nhat) — dung lai / doi ten thay vi tao moi.
    folder, _da_tao = _thu_muc_phim_duy_nhat(
        outdir, ten, info["title"], url=url, log=log)
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


# ======================================================================
# v7.8 - TU BAM NUT "TIEP TUC TAI XUONG" TREN HOP THOAI IDM
# IDM hien hop thoai "Tep thuc thi chinh cua IDM bi hong", nut
# "Tiep tuc tai xuong (4)" bi mo, dem nguoc vai giay moi sang de bam.
# Chi bam ho nut doi dem nguoc, KHONG sua duoc loi IDM bi hong.
# Bam bang Win32 user32 qua ctypes (thu vien chuan Python, KHONG
# them dependency moi cho ban exe). Moi ham deu nhan `api` de test
# bang fake (Linux khong co IDM that).
# ======================================================================

IDM_TU_BAM_TOI_DA_GIAY = 60      # canh hop IDM toi da 60s roi dung
IDM_TU_BAM_CHU_KY_GIAY = 0.5     # poll moi 0.5s
IDM_TIEU_DE_CHUA = "Internet Download Manager"
IDM_NUT_TIEP_TUC = "Tiếp tục tải xuống"   # ca dang "Tiếp tục tải xuống (4)"
IDM_BM_CLICK = 0x00F5            # tin nhan Win32: bam nut


# ========== (v7.9) DUYET VIDEO - GIAI DOAN 1: TIM THEO TU KHOA ==========
# API tim kiem / chi tiet / lien quan cong khai cua Bilibili, KHONG
# can dang nhap. Co cookies.txt (CYAN import san) thi kem Cookie
# de ket qua day du hon; khong co van tim an danh duoc. KHONG
# dang nhap trong tool (quy tac cookie nhu cu). Moi ham nhan them
# doc_json / lay_mixin de test mock mang (kieu dich_fn cua dich_srt).
DUYET_VIDEO_API_TIM_KIEM = (
    "https://api.bilibili.com/x/web-interface/wbi/search/type")
DUYET_VIDEO_API_CHI_TIET = (
    "https://api.bilibili.com/x/web-interface/view")
DUYET_VIDEO_API_LIEN_QUAN = (
    "https://api.bilibili.com/x/web-interface/archive/related")
DUYET_VIDEO_API_DE_XUAT = (
    "https://api.bilibili.com/x/web-interface/index/top/feed/rcmd")
DUYET_VIDEO_LOI_CAN_COOKIE_DE_XUAT = (
    "Bilibili yêu cầu đăng nhập để xem đề xuất trang chủ — import "
    "cookies.txt (đăng nhập Bilibili trên trình duyệt rồi xuất file) "
    "vào tool rồi bấm 'Tải đề xuất' lại.")
DUYET_VIDEO_SO_KET_QUA = 20


def headers_bilibili(cookies_path=None):
    """Header goi API Bilibili: UA trinh duyet + Referer; co file
    cookies.txt thi kem chuoi Cookie (doc_cookies_txt); khong co
    thi tim an danh, khong doi dang nhap."""
    head = {"User-Agent": UA_TRINH_DUYET,
            "Referer": "https://www.bilibili.com/"}
    if cookies_path and os.path.isfile(cookies_path):
        chuoi = doc_cookies_txt(cookies_path)
        if chuoi:
            head["Cookie"] = chuoi
    return head


def kiem_tra_cookie_bilibili(cookies_path):
    """(v7.21) Kiem tra cookie Bilibili con song khong: doc file,
    kiem tra co SESSDATA khong, roi goi API nav
    (x/web-interface/nav) voi header tu headers_bilibili, doc
    isLogin/mid/uname. Tra ve dict:
      {"trang_thai": "song" | "chet" | "khong_sessdata" |
                     "khong_file",
       "ten": ten tai khoan (chi khi song), "mid": 0,
       "chi_tiet": giai thich ngan}.
    Loi mang khi goi nav -> "chet" kem chi tiet (de CYAN biet la
    loi goi API, khong phai cookie het han — khong ket luan vo).
    Chi goi 1 API nhe, khong tai gi."""
    if not cookies_path or not os.path.isfile(cookies_path):
        return {"trang_thai": "khong_file", "ten": "", "mid": 0,
                "chi_tiet": "Chưa có file cookies.txt."}
    try:
        ck = lay_cookies_dict(cookies_path)
    except Exception:
        ck = {}
    if not ck.get("SESSDATA"):
        return {"trang_thai": "khong_sessdata", "ten": "", "mid": 0,
                "chi_tiet": "File cookies không có SESSDATA."}
    try:
        head = headers_bilibili(cookies_path)
        req = urllib.request.Request(
            "https://api.bilibili.com/x/web-interface/nav", headers=head)
        with mo_url_co_fallback_ssl(req, timeout=15) as resp:
            nav = json.loads(resp.read().decode("utf-8", "replace"))
        data = (nav or {}).get("data") or {}
        if data.get("isLogin"):
            return {"trang_thai": "song",
                    "ten": str(data.get("uname") or ""),
                    "mid": int(data.get("mid") or 0),
                    "chi_tiet": ""}
        return {"trang_thai": "chet", "ten": "", "mid": 0,
                "chi_tiet": "Bilibili báo chưa đăng nhập "
                            "(SESSDATA hết hạn)."}
    except Exception as e:
        return {"trang_thai": "chet", "ten": "", "mid": 0,
                "chi_tiet": "Không gọi được API kiểm tra: %s"
                            % _tom_tat_loi(e)}


def lam_sach_tieu_de_html(text):
    """Tieu de tu API tim kiem co the chua <em class="keyword">..
    </em> danh dau tu khoa — bo het tag HTML + giai thuc the."""
    if not text:
        return ""
    sach = re.sub(r"<[^>]+>", "", str(text))
    return html.unescape(sach).strip()


def doi_chuoi_thoi_luong_sang_giay(chuoi):
    """'12:34' / '1:02:03' (dang API tim kiem tra ve) -> so giay.
    Tra ve None neu khong doc duoc (de trong, khong doan)."""
    if chuoi is None:
        return None
    try:
        phan = str(chuoi).strip().split(":")
        if not phan or any(p == "" for p in phan):
            return None
        so = [int(p) for p in phan]
    except Exception:
        return None
    if len(so) == 2:
        return so[0] * 60 + so[1]
    if len(so) == 3:
        return so[0] * 3600 + so[1] * 60 + so[2]
    if len(so) == 1:
        return so[0]
    return None


def link_video_bilibili(bvid, page=None):
    """Link xem video; page > 1 thi them ?p=N (link tung phan)."""
    url = "https://www.bilibili.com/video/" + str(bvid or "")
    if page is not None:
        try:
            if int(page) > 1:
                url += "?p=%d" % int(page)
        except Exception:
            pass
    return url


def trich_bvid_tu_link(link):
    """Lay BV... tu link (co the kem ?p=N, /vi/, tham so theo doi)."""
    m = re.search(r"(BV[0-9A-Za-z]+)", link or "")
    return m.group(1) if m else ""


def trich_page_tu_link(link):
    """Lay so phan ?p=N tu link; khong co thi mac dinh phan 1."""
    m = re.search(r"[?&]p=(\d+)", link or "")
    try:
        return int(m.group(1)) if m else 1
    except Exception:
        return 1


def tim_kiem_bilibili(tu_khoa, page=1, page_size=DUYET_VIDEO_SO_KET_QUA,
                      cookies=None, log=None, doc_json=None,
                      lay_mixin=None, order="totalrank"):
    """Tim video Bilibili theo tu khoa qua API tim kiem cong khai.
    KHONG can dang nhap; co cookies.txt thi kem Cookie.
    order (v7.21): "totalrank" = lien quan nhat (mac dinh, nhu cu),
    "pubdate" = moi nhat theo thoi gian dang tai len Bilibili.
    Tra ve list {bvid, title, pic, duration, duration_giay, author,
    play, link, pubdate (epoch, 0 neu khong co)}. API tim kiem bat
    buoc ky WBI: lay mixin key qua nav API roi ky; khong lay duoc
    thi thu goi khong ky (co the bi -352). doc_json / lay_mixin: de
    test mock (mac dinh _doc_json_url / lay_wbi_mixin_key). Raise
    RuntimeError neu API tra loi."""
    tu_khoa = (tu_khoa or "").strip()
    if not tu_khoa:
        return []
    if order not in ("totalrank", "pubdate"):
        order = "totalrank"
    head = headers_bilibili(cookies)
    doc = doc_json or _doc_json_url
    lay = lay_mixin or lay_wbi_mixin_key
    params = {"keyword": tu_khoa, "search_type": "video",
              "page": int(page or 1), "page_size": int(page_size or 20),
              "order": order, "duration": 0, "tids": 0}
    url = DUYET_VIDEO_API_TIM_KIEM + "?" + urllib.parse.urlencode(params)
    try:
        mixin = lay(head, log)
    except Exception:
        mixin = ""
    if mixin:
        url = ky_url_wbi(url, mixin)
    elif log:
        try:
            log("Không lấy được mixin key WBI, thử tìm không ký...")
        except Exception:
            pass
    du_lieu = doc(url, head, log)
    if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
        msg = ""
        if isinstance(du_lieu, dict):
            msg = str(du_lieu.get("message") or du_lieu.get("code") or "")
        raise RuntimeError("Tìm kiếm Bilibili lỗi%s."
                           % ((" (" + msg + ")") if msg else ""))
    ket_qua = []
    for item in ((du_lieu.get("data") or {}).get("result") or []):
        if not isinstance(item, dict):
            continue
        bvid = item.get("bvid") or ""
        if not bvid:
            continue
        pic = item.get("pic") or ""
        if pic.startswith("//"):
            pic = "https:" + pic
        tg = item.get("duration") or ""
        try:
            pubdate = int(item.get("pubdate") or 0)
        except Exception:
            pubdate = 0
        ket_qua.append({
            "bvid": bvid,
            "title": lam_sach_tieu_de_html(item.get("title") or ""),
            "pic": pic,
            "duration": tg,
            "duration_giay": doi_chuoi_thoi_luong_sang_giay(tg),
            "author": item.get("author") or "",
            "play": item.get("play") or 0,
            "link": link_video_bilibili(bvid),
            "pubdate": pubdate,
        })
    return ket_qua


def lay_chi_tiet_video(bvid, cookies=None, log=None, doc_json=None,
                       lay_mixin=None):
    """Chi tiet 1 video qua view API: tieu de, tac gia, mo ta, anh
    bia, danh sach cac phan (pages: page/part/cid/duration/link).
    Thu goi khong ky WBI truoc (view API thuong khong bat ky); neu
    API tra loi thi thu lai co ky WBI. Raise neu ca 2 cach deu loi.
    Tra ve {bvid, title, author, desc, pic, duration, pages: [...]}."""
    bvid = (bvid or "").strip()
    if not bvid:
        raise RuntimeError("Thiếu mã video (BV...).")
    head = headers_bilibili(cookies)
    doc = doc_json or _doc_json_url
    url_goc = (DUYET_VIDEO_API_CHI_TIET + "?bvid="
               + urllib.parse.quote(bvid))
    du_lieu = doc(url_goc, head, log)
    if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
        lay = lay_mixin or lay_wbi_mixin_key
        try:
            mixin = lay(head, log)
        except Exception:
            mixin = ""
        if not mixin:
            raise RuntimeError("Không đọc được chi tiết video %s."
                               % bvid)
        du_lieu = doc(ky_url_wbi(url_goc, mixin), head, log)
        if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
            msg = ""
            if isinstance(du_lieu, dict):
                msg = str(du_lieu.get("message")
                          or du_lieu.get("code") or "")
            raise RuntimeError("Không đọc được chi tiết video %s%s."
                               % (bvid, (" (" + msg + ")") if msg else ""))
    data = du_lieu.get("data") or {}
    pages = []
    for p in data.get("pages") or []:
        if not isinstance(p, dict):
            continue
        try:
            so = int(p.get("page") or 1)
        except Exception:
            so = 1
        try:
            tg = int(p.get("duration") or 0)
        except Exception:
            tg = 0
        pages.append({
            "page": so,
            "part": p.get("part") or ("Phần %d" % so),
            "cid": p.get("cid"),
            "duration": tg,
            "link": link_video_bilibili(bvid, so),
        })
    pic = data.get("pic") or ""
    if pic.startswith("//"):
        pic = "https:" + pic
    chu = data.get("owner") or {}
    return {
        "bvid": bvid,
        "title": lam_sach_tieu_de_html(data.get("title") or ""),
        "author": (chu.get("name") or "") if isinstance(chu, dict) else "",
        "desc": data.get("desc") or "",
        "pic": pic,
        "duration": data.get("duration") or 0,
        "pages": pages,
    }


def lay_video_lien_quan(bvid, cookies=None, log=None, doc_json=None):
    """Video lien quan (cot phai Bilibili) qua archive/related API.
    Tra ve list cung dang voi tim_kiem_bilibili. Day la thong tin
    phu: API loi thi tra ve [] (khong doan, khong raise)."""
    bvid = (bvid or "").strip()
    if not bvid:
        return []
    head = headers_bilibili(cookies)
    doc = doc_json or _doc_json_url
    url = (DUYET_VIDEO_API_LIEN_QUAN + "?bvid="
           + urllib.parse.quote(bvid))
    try:
        du_lieu = doc(url, head, log)
    except Exception:
        return []
    if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
        return []
    ket_qua = []
    for item in du_lieu.get("data") or []:
        if not isinstance(item, dict):
            continue
        bv = item.get("bvid") or ""
        if not bv:
            continue
        pic = item.get("pic") or ""
        if pic.startswith("//"):
            pic = "https:" + pic
        try:
            tg_giay = int(item.get("duration") or 0)
        except Exception:
            tg_giay = 0
        chu = item.get("owner") or {}
        thong_ke = item.get("stat") or {}
        try:
            luot_xem = int((thong_ke or {}).get("view") or 0)
        except Exception:
            luot_xem = 0
        ket_qua.append({
            "bvid": bv,
            "title": lam_sach_tieu_de_html(item.get("title") or ""),
            "pic": pic,
            "duration": dinh_dang_thoi_luong(tg_giay),
            "duration_giay": tg_giay,
            "author": (chu.get("name") or "") if isinstance(chu, dict) else "",
            "play": luot_xem,
            "link": link_video_bilibili(bv),
        })
    return ket_qua


def lay_de_xuat_trang_chu(cookies=None, log=None, doc_json=None,
                           lay_mixin=None):
    """Video de xuat trang chu Bilibili qua API rcmd (giai doan 2).
    De xuat ca nhan hoa CAN dang nhap: co cookies.txt thi kem Cookie
    (de xuat dung gu CYAN); khong co cookies thi thu goi an danh —
    API khong tra (vd -101 chua dang nhap) hoac tra rong thi raise
    RuntimeError bao ro la can import cookies.txt (giao dien hien
    trong tab, khong crash). Thu goi khong ky WBI truoc, loi thi thu
    lai co ky WBI (giong lay_chi_tiet_video). Tra ve list cung dang
    voi tim_kiem_bilibili {bvid, title, pic, duration, duration_giay,
    author, play, link, pubdate (epoch, 0 neu khong co)} de dung
    chung luoi hien thi. (v7.21) Item rcmd CO pubdate (da kiem
    chung API that: 30/30 item) nen che do "Mới nhất" sap xep duoc
    phia client ma khong can goi lai API."""
    head = headers_bilibili(cookies)
    co_cookie = bool(head.get("Cookie"))
    doc = doc_json or _doc_json_url
    url = DUYET_VIDEO_API_DE_XUAT
    du_lieu = doc(url, head, log)
    if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
        lay = lay_mixin or lay_wbi_mixin_key
        try:
            mixin = lay(head, log)
        except Exception:
            mixin = ""
        if mixin:
            du_lieu = doc(ky_url_wbi(url, mixin), head, log)
        if not isinstance(du_lieu, dict) or du_lieu.get("code") != 0:
            code = (du_lieu.get("code")
                    if isinstance(du_lieu, dict) else "")
            if code == -101 or not co_cookie:
                raise RuntimeError(DUYET_VIDEO_LOI_CAN_COOKIE_DE_XUAT)
            msg = ""
            if isinstance(du_lieu, dict):
                msg = str(du_lieu.get("message") or code or "")
            raise RuntimeError("Không tải được đề xuất trang chủ%s."
                               % ((" (" + msg + ")") if msg else ""))
    muc = (du_lieu.get("data") or {}).get("item") or []
    if not muc and not co_cookie:
        raise RuntimeError(DUYET_VIDEO_LOI_CAN_COOKIE_DE_XUAT)
    ket_qua = []
    for item in muc:
        if not isinstance(item, dict):
            continue
        bvid = item.get("bvid") or ""
        if not bvid:
            continue
        pic = item.get("pic") or ""
        if pic.startswith("//"):
            pic = "https:" + pic
        try:
            tg_giay = int(item.get("duration") or 0)
        except Exception:
            tg_giay = 0
        chu = item.get("owner") or {}
        thong_ke = item.get("stat") or {}
        try:
            luot_xem = int((thong_ke or {}).get("view") or 0)
        except Exception:
            luot_xem = 0
        try:
            pubdate = int(item.get("pubdate") or 0)
        except Exception:
            pubdate = 0
        ket_qua.append({
            "bvid": bvid,
            "title": lam_sach_tieu_de_html(item.get("title") or ""),
            "pic": pic,
            "duration": dinh_dang_thoi_luong(tg_giay),
            "duration_giay": tg_giay,
            "author": (chu.get("name") or "") if isinstance(chu, dict) else "",
            "play": luot_xem,
            "link": link_video_bilibili(bvid),
            "pubdate": pubdate,
        })
    return ket_qua


def lay_job_da_tai(bvid, page=None, jobs=None):
    """Tim job da co trong lich su co link trung BV (+ so phan neu
    truyen page). Tra ve job dict hoac None. jobs=None thi doc
    doc_jobs(). Chi can link trung — job da tao la co trong lich
    su, giao dien danh dau 'Đã tải' (khong phan biet trang thai)."""
    if not bvid:
        return None
    if jobs is None:
        jobs = doc_jobs()
    for job in jobs or []:
        if not isinstance(job, dict):
            continue
        link = job.get("link") or ""
        if trich_bvid_tu_link(link) != bvid:
            continue
        if page is None:
            return job
        try:
            if trich_page_tu_link(link) == int(page):
                return job
        except Exception:
            continue
    return None


def tao_job_tu_link_duyet(link, title=""):
    """Tao job moi tu link phan da chon o tab Duyet video — GIONG
    HET job khi dan link o QuanLy.mo_cua_so_moi (cung truong, cung
    mac dinh), de mo bang mo_cua_so_job() chay luong tai/gop san
    co. Ham nay KHONG tai gi ca, chi tao job."""
    return {"id": str(uuid.uuid4())[:8], "title": title or "",
            "link": link or "", "status": "moi", "pct_tai": 0,
            "pct_gop": 0, "tu_gop": True, "xoa_goc": True,
            "giam_15": True, "tu_gop_ytdlp": True,
            "dich_ten": True, "tu_nhan_dien": True,
            "tu_dich_sau_lay_phu_de": False,
            "has_subtitle": None, "subtitle_langs": [],
            "subtitle_file": "", "subtitle_vi_file": "", "folder": ""}


def tai_anh_bia_bytes(url_anh, log=None):
    """Tai anh bia ve bytes (chi tai mang, an toan goi tu luong nen).
    Tra ve bytes hoac None neu loi / khong co anh."""
    url_anh = (url_anh or "").strip()
    if not url_anh:
        return None
    if url_anh.startswith("//"):
        url_anh = "https:" + url_anh
    try:
        req = urllib.request.Request(
            url_anh, headers={"User-Agent": UA_TRINH_DUYET,
                              "Referer": "https://www.bilibili.com/"})
        with mo_url_co_fallback_ssl(req, timeout=15,
                                    log_cb=log) as resp:
            return resp.read()
    except Exception:
        return None


def anh_bia_bytes_sang_photoimage(du_lieu, rong=160, cao=90, log=None):
    """Bytes anh -> tk.PhotoImage (rong x cao). Can Pillow (PIL):
    chua cai thi tra ve None — giao dien giu khung cho 'Anh bia'.
    CHI GOI O LUONG CHINH (PhotoImage khong an toan luong).
    (v7.21) Dung ImageOps.fit de anh LAP DAY khung (rong, cao) —
    thumbnail() cu chi thu nho, khong phong to nen anh nho khong
    bao gio phu het chieu rong cot; fit cat bot phan thua (giua)
    chu khong keo meo anh. Loi thi roi ve thumbnail cu."""
    if not du_lieu:
        return None
    try:
        from PIL import Image, ImageTk
    except Exception:
        if log:
            try:
                log("Chưa có Pillow nên không hiện được ảnh bìa "
                    "(cài: pip install pillow).")
            except Exception:
                pass
        return None
    try:
        anh = Image.open(io.BytesIO(du_lieu)).convert("RGB")
        try:
            from PIL import ImageOps
            anh = ImageOps.fit(anh, (int(rong), int(cao)))
        except Exception:
            anh.thumbnail((int(rong), int(cao)))
        return ImageTk.PhotoImage(anh)
    except Exception:
        return None


def tai_anh_bia_ve_photoimage(url_anh, rong=160, cao=90, log=None):
    """Tai anh bia ve tk.PhotoImage (thumbnail rong x cao). Chi goi
    o luong chinh (tai + doi anh deu o day). Tra ve None neu tai
    loi / khong co Pillow / khong co anh."""
    du_lieu = tai_anh_bia_bytes(url_anh, log)
    if not du_lieu:
        return None
    return anh_bia_bytes_sang_photoimage(du_lieu, rong, cao, log)


class ToolTip:
    """Tooltip don gian cho 1 widget: re chuot vao thi hien ghi chu
    sau ~0.6s, roi chuot / bam thi an. Chi dung cho ghi chu dai
    (vd gioi han cua cong tac tu bam IDM)."""

    def __init__(self, widget, text, cho_ms=600):
        self.widget = widget
        self.text = text
        self.cho_ms = cho_ms
        self._tip = None
        self._after_id = None
        widget.bind("<Enter>", self._vao, add="+")
        widget.bind("<Leave>", self._ra, add="+")
        widget.bind("<ButtonPress>", self._ra, add="+")

    def _vao(self, _event=None):
        self._ra()
        try:
            self._after_id = self.widget.after(self.cho_ms, self._hien)
        except Exception:
            self._after_id = None

    def _ra(self, _event=None):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        if self._tip is not None:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None

    def _hien(self):
        if self._tip is not None:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
            tip = tk.Toplevel(self.widget)
            tip.wm_overrideredirect(True)
            tip.wm_geometry("+%d+%d" % (x, y))
            tk.Label(tip, text=self.text, justify="left", relief="solid",
                     borderwidth=1, bg="#ffffe0", fg="black",
                     wraplength=420).pack()
            self._tip = tip
        except Exception:
            self._tip = None


class _ApiIDMWindows:
    """Goi Win32 user32 qua ctypes (chi Windows). API cong khai:
    liet_ke_cua_so() -> [(hwnd, tieu_de)] cua so IDM dang hien;
    cua_so_con(hwnd) -> [(hwnd_con, text)] nut/con cua cua so do;
    nut_bat(hwnd) / cua_so_con_song(hwnd) -> bool; bam_nut(hwnd).
    """

    def __init__(self):
        import ctypes
        from ctypes import wintypes
        self._ctypes = ctypes
        self._wintypes = wintypes
        self.user32 = ctypes.windll.user32
        self._WNDENUMPROC = ctypes.WINFUNCTYPE(
            ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        self.user32.EnumWindows.argtypes = [self._WNDENUMPROC,
                                            wintypes.LPARAM]
        self.user32.EnumWindows.restype = wintypes.BOOL
        self.user32.EnumChildWindows.argtypes = [wintypes.HWND,
                                                 self._WNDENUMPROC,
                                                 wintypes.LPARAM]
        self.user32.EnumChildWindows.restype = wintypes.BOOL
        self.user32.GetWindowTextW.argtypes = [wintypes.HWND,
                                               wintypes.LPWSTR,
                                               ctypes.c_int]
        self.user32.GetWindowTextW.restype = ctypes.c_int
        self.user32.IsWindowVisible.argtypes = [wintypes.HWND]
        self.user32.IsWindowVisible.restype = wintypes.BOOL
        self.user32.IsWindow.argtypes = [wintypes.HWND]
        self.user32.IsWindow.restype = wintypes.BOOL
        self.user32.IsWindowEnabled.argtypes = [wintypes.HWND]
        self.user32.IsWindowEnabled.restype = wintypes.BOOL
        self.user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT,
                                             wintypes.WPARAM,
                                             wintypes.LPARAM]
        self.user32.SendMessageW.restype = wintypes.LPARAM

    def _tieu_de(self, hwnd):
        buf = self._ctypes.create_unicode_buffer(512)
        n = self.user32.GetWindowTextW(hwnd, buf, 512)
        return buf.value if n > 0 else ""

    def liet_ke_cua_so(self):
        ket_qua = []
        user32 = self.user32

        def _goi(hwnd, _tham_so):
            try:
                if user32.IsWindowVisible(hwnd):
                    tieu_de = self._tieu_de(hwnd)
                    if IDM_TIEU_DE_CHUA in tieu_de:
                        ket_qua.append((hwnd, tieu_de))
            except Exception:
                pass
            return True

        user32.EnumWindows(self._WNDENUMPROC(_goi), 0)
        return ket_qua

    def cua_so_con(self, hwnd):
        ket_qua = []
        user32 = self.user32

        def _goi(con, _tham_so):
            try:
                ket_qua.append((con, self._tieu_de(con)))
            except Exception:
                pass
            return True

        user32.EnumChildWindows(hwnd, self._WNDENUMPROC(_goi), 0)
        return ket_qua

    def cua_so_con_song(self, hwnd):
        try:
            return bool(self.user32.IsWindow(hwnd))
        except Exception:
            return False

    def nut_bat(self, hwnd):
        try:
            return bool(self.user32.IsWindowEnabled(hwnd))
        except Exception:
            return False

    def bam_nut(self, hwnd):
        self.user32.SendMessageW(hwnd, IDM_BM_CLICK, 0, 0)


def tao_api_idm():
    """Tao API Win32 that de bam hop IDM. Tra ve None neu khong
    phai Windows hoac khong goi duoc user32 (vd ban chay tren Linux
    de test) — nguoi goi phai log ro roi bo qua, khong chet im."""
    if not sys.platform.startswith("win"):
        return None
    try:
        return _ApiIDMWindows()
    except Exception:
        return None


def liet_ke_cua_so_idm(api=None):
    """Chup tap hwnd cac cua so IDM dang mo (de loai tru cua so cu
    khi canh hop moi sau lan day link). Loi -> tra ve tap rong."""
    if api is None:
        api = tao_api_idm()
        if api is None:
            return set()
    try:
        return set(hw for hw, _td in api.liet_ke_cua_so())
    except Exception:
        return set()


def tim_nut_tiep_tuc(api, hwnd):
    """Tim nut 'Tiep tuc tai xuong' trong cua so IDM (ca dang co
    dem nguoc 'Tiep tuc tai xuong (4)'). Tra ve (hwnd_nut, enabled)
    hoac None neu chua thay nut. Chi khop nut nay, khong bao gio
    tra ve nut 'Mo trang web IDM' hay nut khac."""
    for con, text in api.cua_so_con(hwnd):
        if (text or "").strip().startswith(IDM_NUT_TIEP_TUC):
            return (con, bool(api.nut_bat(con)))
    return None


def canh_hop_idm_va_bam(log_cb=None, dung=None, hwnd_da_co=None,
                        api=None, toi_da_giay=IDM_TU_BAM_TOI_DA_GIAY,
                        chu_ky_giay=IDM_TU_BAM_CHU_KY_GIAY):
    """Luong nen: canh hop thoai IDM moi xuat hien sau lan day link,
    doi nut 'Tiep tuc tai xuong' sang (enabled) roi bam ho 1 lan
    duy nhat. Tra ve True neu da bam duoc, False neu khong
    (het gio / hop da dong do cau bam tay / loi). Moi truong hop
    deu log ro qua log_cb, khong chet im, khong hien hop thoai.
    hwnd_da_co: tap hwnd cua so IDM da co TRUOC khi day link (de
    chi xu ly cua so moi); dung: threading.Event de dung som."""
    def _log(s):
        if log_cb:
            try:
                log_cb(s)
            except Exception:
                pass

    if api is None:
        api = tao_api_idm()
        if api is None:
            _log("Tự bấm IDM: chỉ chạy trên Windows, bỏ qua.")
            return False
    da_co = set(hwnd_da_co or ())
    da_thay_hop = False
    bat_dau = time.monotonic()
    try:
        while True:
            if dung is not None and dung.is_set():
                _log("Tự bấm IDM: đã dừng theo yêu cầu.")
                return False
            if time.monotonic() - bat_dau > toi_da_giay:
                _log("Tự bấm IDM: hết %d giây mà không thấy hộp thoại "
                     "IDM, bỏ qua." % int(toi_da_giay))
                return False
            try:
                cua_so = [hw for hw, _td in api.liet_ke_cua_so()
                          if hw not in da_co]
            except Exception as e:
                _log("Tự bấm IDM: lỗi khi liệt kê cửa sổ: %s" % e)
                return False
            if not cua_so:
                if da_thay_hop:
                    # Hop da tung hien roi bien mat: cau bam tay
                    # truoc (hoac dong hop), dung, khong bam lai.
                    _log("Tự bấm IDM: hộp thoại IDM đã đóng (có thể "
                         "cậu đã bấm tay trước), dừng.")
                    return False
                time.sleep(chu_ky_giay)
                continue
            da_thay_hop = True
            hwnd = cua_so[0]
            if not api.cua_so_con_song(hwnd):
                time.sleep(chu_ky_giay)
                continue
            try:
                nut = tim_nut_tiep_tuc(api, hwnd)
            except Exception as e:
                _log("Tự bấm IDM: lỗi khi tìm nút: %s" % e)
                return False
            if nut is None:
                # Hop moi hien, nut chua kip ve (dang load) — doi tiep.
                time.sleep(chu_ky_giay)
                continue
            nut_hwnd, bat = nut
            if not bat:
                # Nut dang mo vi dem nguoc chua xong — doi no sang.
                time.sleep(chu_ky_giay)
                continue
            try:
                api.bam_nut(nut_hwnd)
            except Exception as e:
                _log("Tự bấm IDM: bấm nút lỗi: %s" % e)
                return False
            _log("Đã tự bấm 'Tiếp tục tải xuống' trên hộp thoại IDM.")
            return True
    except Exception as e:
        _log("Tự bấm IDM: lỗi không ngờ: %s" % e)
        return False


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


# ======================================================================
#  VieNeu-TTS — SNIPPET CHO ChipChipStudio v7.24 (CHUA CHEN VAO FILE CHINH)
#  File goc: ~/workspace/gop-video-bilibili/ChipChipStudio-GUI-v7.23-draft.py
#  File nay: /tmp/v724/vieneu_snippet.py — CHI DOC + CHEN TAY VAO v7.24.
#  KHONG sua file v7.23. Snippet nay phu thuoc 2 ham DA CO trong file goc:
#    * chay_ngam_kwargs()   (dong ~371: subprocess.CREATE_NO_WINDOW tren
#      Windows, de pip/ffmpeg chay ngam, khong nhap nhay console)
#    * tim_ffmpeg()         (dong ~622: tim ffmpeg.exe / ffmpeg trong PATH;
#      neu khong co thi snippet tu fallback sang shutil.which("ffmpeg"))
#  Neu chen vao file khac thi phai mang theo 2 ham tren (hoac sua lai).
#
#  ---------------- HUONG DAN CHEN (4 CHO) ----------------
#  (1) Sau dict GIONG (dong ~4389-4393, ngay truoc GIONG_MAC_DINH ~4395):
#        GIONG.update({ten: "vieneu:" + slug
#                      for ten, slug in VIENEU_PRESET.items()})
#      (25 preset SDK 3.8.5 — xem bang VIENEU_GIONG_BANG.)
#      GIONG chi la bang hien-thi -> id; id "vieneu:..." KHONG phai Edge
#      voice id, chi la co danh dau engine rieng. BAT BUOC them nhanh
#      re o moi cho goi doc: cac dong ~9290, ~9388, ~9677 trong
#      CuaSoDocPhuDe dang lam `voice = GIONG.get(cb_giong.get(), ...)`
#      roi dua thang vao doc_thanh_mp3() (Edge). Sua thanh:
#        if vieneu_giong_la_vieneu(ten_hien_thi):
#            vieneu_doc_mp3(text, ten_hien_thi, duong_dan_ra,
#                           toc_do=toc_do, log_cb=log_cb)
#        else:
#            doc_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra, ...)
#      TUYET DOI KHONG map Xuan Vinh / Pham Tuyen sang NamMinh/HoaiMy
#      Edge khi VieNeu loi — bao loi, de nguoi dung bam nut tai tai
#      nguyen (muc 3), khong doc bang giong khac.
#
#  (2) Config mac dinh moi — CHI DOI MAC DINH HIEN THI, KHONG XOA HoaiMy:
#      * Dong ~547 trong config mac dinh: "ytf_giong_vi": "HoaiMy (nữ)"
#        -> "ytf_giong_vi": VIENEU_GIONG_XUAN_VINH
#        ("Xuân Vĩnh (VieNeu, nam Bắc)") cho du an faceless.
#      * Dong ~11167: YTF_GIONG_MAC_DINH = {"en": ..., "vi": "HoaiMy (nữ)"}
#        -> {"en": "Helio (nam, Mỹ)", "vi": VIENEU_GIONG_XUAN_VINH}.
#      * Giong cu "HoaiMy (nữ)" VAN GIU trong YTF_GIONG_EDGE["vi"] va
#        trong GIONG — nguoi dung cu van chon duoc; config da luu truoc
#        day van giu gia tri cu cho toi khi reset/xoa config.
#
#  (3) Trong CuaSoDocPhuDe (class o dong ~8145; combobox giong o
#      dong ~8245-8248: self.cb_giong = ttk.Combobox(..., values=
#      list(GIONG.keys())) — tu dong co them 25 giong VieNeu (SDK
#      3.8.5) sau buoc
#      (1), khong can sua values): them ngay duoi hang combobox giong
#      1 nut + 1 label:
#        tk.Button(f2, text="Tải tài nguyên VieNeu",
#                  command=self._tai_tai_nguyen_vieneu).grid(...)
#        self.lb_vieneu = tk.Label(f2, text=vieneu_trang_thai()[2], ...)
#      va 1 method trong class:
#        def _tai_tai_nguyen_vieneu(self):
#            ok, msg = vieneu_tai_tai_nguyen(log_cb=self._log)  # _log tuy class
#            self.lb_vieneu.config(text=msg)
#            # (khuyen nghi) chay trong threading.Thread de khong dong UI
#            # vi pip install + tai model lan dau co the mat vai phut.
#      Nut nay CHI cai goi `vieneu` + tai model lan dau; khong doi giong
#      dang chon, khong tu doc thu.
#
#  (4) Trong CuaSoVoiceFaceless (class o dong ~13593; combobox giong
#      cot VI o dong ~14019-14028 lay values tu ytf_giong_theo_ngon_ngu):
#        YTF_GIONG_EDGE["vi"].update({ten: "vieneu:" + slug
#                                     for ten, slug in VIENEU_PRESET.items()})
#      Roi o cho xu ly cue cua cot VI (cho goi doc_thanh_mp3 / Edge theo
#      voice id lay tu ytf_giong_id_cua_ten): re nhanh truoc khi goi Edge:
#        if voice_id.startswith("vieneu:"):
#            vieneu_doc_mp3(text_cue, ten_giong_hien_thi, mp3_tam,
#                           toc_do=toc_do, log_cb=log_cb)
#        else:
#            ... (luong Edge cu, khong doi)
#      Luu y: ytf_giong_id_cua_ten() hien tra ve Edge id mac dinh khi
#      khong thay ten — voi id "vieneu:..." no tra dung vi ten da co
#      trong dict; NHUNG phai dam bao nhanh re nay chay TRUOC moi cho
#      dung voice id lam Edge voice (ke ca nut "Nghe thu" _nghe_thu_giong
#      va ham anh xa Helio/Aria — VieNeu khong di qua cac ham do).
#      Toc do mac dinh cua cot VI khi chon VieNeu: 0.95 (xem
#      VIENEU_TOC_DO_MAC_DINH) thay vi 1.0 cua Edge; slider van cho
#      chinh 0.5-1.35 nhu cu.
#
#  ---------------- TINH TRANG XAC MINH API (21/11/2026) ----------------
#  DA XAC MINH tu tai lieu chinh thuc (PyPI `vieneu` 3.8.5, 19/11/2026 va
#  README Hugging Face pnnbao-ump/VieNeu-TTS-v3-Turbo):
#    * pip install vieneu  (CPU mac dinh, torch-free, chay v3 Turbo
#      qua ONNX Runtime; GPU thi tu phat hien PyTorch neu da cai).
#    * from vieneu import Vieneu; tts = Vieneu()
#    * audio = tts.infer("Xin chào...", voice="Xuân Vĩnh")
#    * tts.save(audio, "output.wav")
#    * tts.list_preset_voices() -> list[(label, voice_id)]
#    * 23 preset v3 Turbo, trong do "Xuân Vĩnh" (Bac, nam, Natural) va
#      "Phạm Tuyên" (Bac, nam, Natural) la ten preset THAT — goi bang
#      TEN TIENG VIET CO DAU, khong phai slug.
#    * Model mac dinh: v3 Turbo, am thanh ra 48 kHz.
#  CHUA KIEM CHUNG (code duoi day tu phong thu, xem ghi chu tung cho):
#    * CHUA KIEM CHUNG API VieNeu that bang cach chay tong hop that
#      (chua chay infer() thanh cong o dau — VM nay chua cai vieneu,
#      may Windows cua CYAN cung chua cai; xem muc KIEM_CHUNG cuoi file).
#    * Slug "xuan-vinh" / "pham-tuyen": CHI duoc 1 nguon ben thu ba
#      (izzi-ai voice-studio) anh xa nhu vay; tai lieu chinh thuc cua
#      VieNeu chi dung ten co dau ("Xuân Vĩnh"). Vi vay code LUON thu
#      ten co dau TRUOC, slug chi la phuong an du phong, va co fallback
#      quet list_preset_voices() de khop ten that su co trong SDK.
#    * Ham infer() KHONG co tham so toc do trong tai lieu doc duoc
#      (khong thay `speed`/`rate`); vi vay toc do 0.95x duoc ap dung
#      bang ffmpeg `atempo` SAU khi tong hop (xem vieneu_doc_mp3).
#      Neu SDK sau nay them tham so toc do thi moi doi sang dung API.
#    * Duong dan cache/model tren may: CHUA xac minh — code chi doan
#      theo quy uoc (bien VIENEU_HOME neu nguoi dung dat, ~/.cache/
#      huggingface/hub, thu muc cau hinh ngoai o C: neu co). Bien
#      VIENEU_HOME KHONG phai bien chuan duoc tai lieu xac nhan; chi
#      la quy uoc do snippet nay dat ra. Tuyet doi khong hardcode C:
#      lam noi tai model; neu khong tim thay thu muc nao thi bao
#      "chua ro" chu khong doan duong dan C:.
#    * Phien ban SDK cu (1.x) dung kien truc khac (0.3B/0.5B GGUF,
#      mac dinh khac); code dung importlib/getattr dong + thu nhieu
#      signature de khong vo neu gap ban cu, nhung chi dam bao cho
#      SDK 3.x (v3 Turbo) theo tai lieu moi nhat.
# ======================================================================

import os
import subprocess
import sys

# --- Phu thuoc vao file goc (dong ~371): chay_ngam_kwargs() phai ton tai
# --- o pham vi global khi chen snippet vao file v7.24. Neu chay snippet
# --- doc lap (test), dinh nghia tam o duoi (xem khoi try o cuoi file).

# ======================================================================
# HANG SO
# ======================================================================

VIENEU_TOC_DO_MAC_DINH = 0.95

# (v7.24, SDK vieneu 3.8.5) BANG 25 PRESET THAT — doc tu file
# voices_v3_turbo.json trong goi SDK 3.8.5 (pip install vieneu==3.8.5;
# SDK pin "3.8.5", moi nhat tren PyPI). README SDK v3.7.1 chi liet ke
# 23 giong, mac dinh "Minh Quân" — DA LOI THOI: 3.8.5 them "Adam bựa",
# "Hải Đăng", "Quốc Tuấn", "Thiền Tâm Đức", "Thiện Minh" (Bac) va bo
# "Anh Khôi", "Minh Quân", "Mạnh Dũng" khoi preset chinh ("Minh Quân" /
# "Minh Quân Pro" chi con la alias -> "Hải Đăng", xem VIENEU_PRESET_ALIAS).
# Mac dinh cua SDK 3.8.5 la "Hải Đăng", nhung TOOL VAN GIU mac dinh
# "Xuân Vĩnh" (chinh) / "Phạm Tuyên" (du phong).
# Moi muc: (ten hien thi, ten preset goc co dau, slug, gioi tinh).
VIENEU_GIONG_BANG = [
    # Bac (15)
    ("Adam bựa (VieNeu, nam Bắc)", "Adam bựa", "adam-bua", "nam"),
    ("Hải Đăng (VieNeu, nam Bắc)", "Hải Đăng", "hai-dang", "nam"),
    ("Mai Anh (VieNeu, nữ Bắc)", "Mai Anh", "mai-anh", "nữ"),
    ("Minh Đức (VieNeu, nam Bắc)", "Minh Đức", "minh-duc", "nam"),
    ("Ngọc Huyền (VieNeu, nữ Bắc)", "Ngọc Huyền", "ngoc-huyen", "nữ"),
    ("Ngọc Linh (VieNeu, nữ Bắc)", "Ngọc Linh", "ngoc-linh", "nữ"),
    ("Phạm Tuyên (VieNeu, nam Bắc)", "Phạm Tuyên", "pham-tuyen", "nam"),
    ("Quốc Tuấn (VieNeu, nam Bắc)", "Quốc Tuấn", "quoc-tuan", "nam"),
    ("Quỳnh Anh (VieNeu, nữ Bắc)", "Quỳnh Anh", "quynh-anh", "nữ"),
    ("Thanh Bình (VieNeu, nam Bắc)", "Thanh Bình", "thanh-binh", "nam"),
    ("Thiền Tâm Đức (VieNeu, nam Bắc)", "Thiền Tâm Đức", "thien-tam-duc", "nam"),
    ("Thiện Minh (VieNeu, nam Bắc)", "Thiện Minh", "thien-minh", "nam"),
    ("Trúc Ly (VieNeu, nữ Bắc)", "Trúc Ly", "truc-ly", "nữ"),
    ("Xuân Vĩnh (VieNeu, nam Bắc)", "Xuân Vĩnh", "xuan-vinh", "nam"),
    ("Đoan Trang (VieNeu, nữ Bắc)", "Đoan Trang", "doan-trang", "nữ"),
    # Trung (2)
    ("Ngọc Trân (VieNeu, nữ Trung)", "Ngọc Trân", "ngoc-tran", "nữ"),
    ("Quang Sơn (VieNeu, nam Trung)", "Quang Sơn", "quang-son", "nam"),
    # Nam (8)
    ("Adam (VieNeu, nam Nam)", "Adam", "adam", "nam"),
    ("Kim Thanh (VieNeu, nữ Nam)", "Kim Thanh", "kim-thanh", "nữ"),
    ("Minh Triết (VieNeu, nam Nam)", "Minh Triết", "minh-triet", "nam"),
    ("Mỹ Duyên (VieNeu, nữ Nam)", "Mỹ Duyên", "my-duyen", "nữ"),
    ("Thái Sơn (VieNeu, nam Nam)", "Thái Sơn", "thai-son", "nam"),
    ("Thùy Dung (VieNeu, nữ Nam)", "Thùy Dung", "thuy-dung", "nữ"),
    ("Thục Đoan (VieNeu, nữ Nam)", "Thục Đoan", "thuc-doan", "nữ"),
    ("Đức Trí (VieNeu, nam Nam)", "Đức Trí", "duc-tri", "nam"),
]

VIENEU_GIONG_XUAN_VINH = "Xuân Vĩnh (VieNeu, nam Bắc)"
VIENEU_GIONG_PHAM_TUYEN = "Phạm Tuyên (VieNeu, nam Bắc)"
VIENEU_GIONG_HAI_DANG = "Hải Đăng (VieNeu, nam Bắc)"

# Anh xa ten hien thi trong tool -> slug preset cua VieNeu.
# GHI CHU QUAN TRONG: slug la PHONG DOAN theo ten giong (bo dau, noi
# bang "-"); ten preset DUOC XAC MINH trong SDK 3.8.5 la ten co dau.
# Code _vieneu_giai_quyet_preset() LUON thu ten co dau truoc, sau do
# moi thu slug, roi quet list_preset_voices() de khop that — neu khong
# khop cai nao thi bao loi ro rang, KHONG tu doan them, KHONG fallback
# sang giong Edge khac.
VIENEU_PRESET = {ten: slug for ten, _co_dau, slug, _gt
                 in VIENEU_GIONG_BANG}

# Ten preset co dau (DA XAC MINH tu SDK 3.8.5) — ung vien uu tien 1.
VIENEU_PRESET_TEN_CO_DAU = {ten: co_dau for ten, co_dau, _slug, _gt
                            in VIENEU_GIONG_BANG}

# Id dac biet dung trong GIONG / YTF_GIONG_EDGE["vi"] de danh dau engine
# VieNeu (xem huong dan chen muc 1 + 4). Khong phai Edge voice id.
VIENEU_ID_XUAN_VINH = "vieneu:xuan-vinh"
VIENEU_ID_PHAM_TUYEN = "vieneu:pham-tuyen"
VIENEU_ID_HAI_DANG = "vieneu:hai-dang"

# (v7.24, SDK 3.8.5) Ten cu chi con la alias trong SDK: "Minh Quân" /
# "Minh Quân Pro" van chay duoc nho alias ve preset mac dinh moi
# "Hải Đăng" — khong dua vao dropdown (khong phai preset chinh nua).
# Map: ten cu nguoi dung go / id cu -> ten preset co dau moi.
VIENEU_PRESET_ALIAS = {
    "Minh Quân": "Hải Đăng",
    "Minh Quân Pro": "Hải Đăng",
    "vieneu:minh-quan": "Hải Đăng",
    "vieneu:minh-quan-pro": "Hải Đăng",
}

# Sample rate goc cua VieNeu v3 Turbo (tai lieu chinh thuc: 48 kHz).
VIENEU_SAMPLE_RATE_GOC = 48000
# Chuan xuat MP3 cua ChipChipStudio (giong chuan voice HoaiMy):
# 44100 Hz, stereo, 192k, libmp3lame.
VIENEU_MP3_SAMPLE_RATE = 44100
VIENEU_MP3_BITRATE = "192k"


# ======================================================================
# TIEN ICH NOI BO
# ======================================================================

def _vieneu_log(log_cb, msg):
    """Ghi log qua callback cua tool (neu co); khong co thi bo qua."""
    if log_cb is not None:
        try:
            log_cb(msg)
        except Exception:
            pass


def _vieneu_ffmpeg():
    """Tim ffmpeg: uu tien tim_ffmpeg() cua file goc (dong ~622),
    fallback shutil.which. Tra ve duong dan hoac None."""
    try:
        fn = globals().get("tim_ffmpeg")
        if callable(fn):
            p = fn()
            if p:
                return p
    except Exception:
        pass
    import shutil
    return shutil.which("ffmpeg")


def _vieneu_chuoi_atempo(toc_do):
    """ffmpeg atempo chi nhan 0.5-2.0 moi lop; toc do ngoai khoang thi
    xau chuoi nhieu lop atempo (vd 0.4 = 0.5 * 0.8). Tra ve chuoi filter
    kieu 'atempo=0.950000' hoac 'atempo=...,atempo=...'. toc_do == 1.0
    thi tra ve '' (khong can filter)."""
    try:
        t = float(toc_do)
    except Exception:
        t = 1.0
    if t <= 0:
        t = 1.0
    if abs(t - 1.0) < 1e-6:
        return ""
    parts = []
    con_lai = t
    # Tach thua so ve trong [0.5, 2.0]; toi da 8 lop cho an toan.
    while (con_lai < 0.5 or con_lai > 2.0) and len(parts) < 8:
        if con_lai < 0.5:
            parts.append(0.5)
            con_lai = con_lai / 0.5
        else:
            parts.append(2.0)
            con_lai = con_lai / 2.0
    parts.append(round(con_lai, 6))
    return ",".join("atempo=%f" % p for p in parts)


def _vieneu_ghi_wav_thu_cong(audio, wav_path, sample_rate=VIENEU_SAMPLE_RATE_GOC):
    """Ghi numpy array float32 thanh WAV 16-bit neu tts.save() khong
    co san (ban SDK khac). Tra ve True neu ghi duoc."""
    try:
        import numpy as np
        import wave
        arr = np.asarray(audio, dtype=np.float32).reshape(-1)
        pcm = np.clip(arr, -1.0, 1.0)
        pcm = (pcm * 32767).astype(np.int16)
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(int(sample_rate))
            w.writeframes(pcm.tobytes())
        return True
    except Exception:
        return False


# ======================================================================
# TRANG THAI / CAI DAT
# ======================================================================

def _vieneu_thu_muc_model_ung_vien():
    """Cac noi CO THE chua model/cache VieNeu — chi la ung vien doan
    theo quy uoc, CHUA KIEM CHUNG duong dan that cua SDK.
    Tuyet doi khong hardcode C: lam noi tai model. Thu tu uu tien:
      1. Bien moi truong VIENEU_HOME (neu nguoi dung tu dat; quy uoc
         cua snippet nay, khong phai bien chuan cua SDK).
      2. Bien HF_HOME / HUGGINGFACE_HUB_CACHE neu co (chu cua HF hub).
      3. ~/.cache/huggingface/hub (mac dinh cua Hugging Face).
      4. Cac o dia khac ngoai C: neu ton tai (vd D: tren may CYAN —
         chi kiem tra su ton tai, khong tu tao thu muc, khong tai ve).
    Tra ve list duong dan (co the khong ton tai — ham goi tu loc)."""
    ung_vien = []
    home_env = os.environ.get("VIENEU_HOME", "").strip()
    if home_env:
        ung_vien.append(home_env)
    for k in ("HF_HOME", "HUGGINGFACE_HUB_CACHE"):
        v = os.environ.get(k, "").strip()
        if v:
            ung_vien.append(v)
    ung_vien.append(os.path.join(os.path.expanduser("~"), ".cache",
                                 "huggingface", "hub"))
    # O dia ngoai C: (Windows) — chi them neu o ton tai; khong tai gi
    # ve day neu nguoi dung chua chon.
    if sys.platform == "win32":
        for o in ("D", "E", "F"):
            thu_muc = "%s:\\VieNeu" % o
            if os.path.isdir("%s:\\" % o):
                ung_vien.append(thu_muc)
    return ung_vien


def _vieneu_tim_file_model():
    """Tim dau vet file model trong cac thu muc ung vien: thu muc/file
    co ten chua 'vieneu' hoac 'VieNeu', hoac file .onnx / .safetensors
    nam trong thu muc do. Tra ve duong dan dau tien tim thay, hoac None.
    Day la heuristic — khong thay khong co nghia la model chua tai
    (SDK co the luu ten khac); chi dung de hien thi trang thai."""
    khoa = ("vieneu", "VieNeu")
    for root in _vieneu_thu_muc_model_ung_vien():
        if not root or not os.path.isdir(root):
            continue
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # Cat nhanh: khong dao sau qua 4 cap tu goc ung vien.
                if dirpath.count(os.sep) - root.count(os.sep) > 4:
                    dirnames[:] = []
                    continue
                for d in dirnames:
                    if any(k in d for k in khoa):
                        return os.path.join(dirpath, d)
                for f in filenames:
                    if any(k in f for k in khoa) and f.lower().endswith(
                            (".onnx", ".safetensors", ".bin", ".gguf")):
                        return os.path.join(dirpath, f)
        except Exception:
            continue
    return None


def vieneu_trang_thai():
    """Kiem tra goi vieneu + model/cache.
    Tra ve (da_cai: bool, da_co_model: bool, thong_bao: str).
    Khong raise, khong tai gi ve, khong khoi tao model (nhanh)."""
    import importlib.util
    try:
        spec = importlib.util.find_spec("vieneu")
    except Exception:
        spec = None
    if spec is None:
        return (False, False,
                "VieNeu chưa cài — bấm nút “Tải tài nguyên VieNeu” để "
                "cài gói vieneu và tải model lần đầu (cần mạng).")
    duong_dan_model = _vieneu_tim_file_model()
    if duong_dan_model:
        return (True, True,
                "VieNeu đã cài, đã thấy model/cache tại: %s"
                % duong_dan_model)
    return (True, False,
            "VieNeu đã cài nhưng chưa thấy file model trong cache "
            "(~/.cache/huggingface/hub hoặc thư mục VIENEU_HOME nếu có). "
            "Model sẽ tự tải ở lần đọc đầu tiên (cần mạng).")


def _vieneu_khoi_tao_lan_dau(vieneu_mod, log_cb=None):
    """Khoi tao Vieneu() lan dau (SDK tu tai model neu chua co).
    Tra (thanh_cong, thong_bao) — dung chung cho ca 2 duong: exe
    bundling (frozen) va pip install (chay .py dev)."""
    lop = getattr(vieneu_mod, "Vieneu", None)
    if lop is None:
        return (False, "Đã có gói VieNeu nhưng không tìm thấy lớp Vieneu "
                       "trong gói này (phiên bản SDK lạ) — thử cập nhật "
                       "tool lên bản mới nhất.")
    try:
        tts = lop()
    except Exception as e:
        return (False, "Đã có gói VieNeu nhưng chưa tải/khởi tạo được model: "
                       "%s — kiểm tra mạng rồi bấm lại nút tải tài nguyên." % e)
    _vieneu_log(log_cb, "Model VieNeu đã sẵn sàng.")
    return (True, "Đã tải xong tài nguyên VieNeu — có thể chọn giọng "
                  "Xuân Vĩnh / Phạm Tuyên để đọc.")


def vieneu_tai_tai_nguyen(log_cb=None):
    """Lay tai nguyen VieNeu. Tra ve (thanh_cong: bool, thong_bao: str)
    — moi loi tra ve thong bao tieng Viet, KHONG raise, KHONG crash
    app. Nen goi trong thread rieng vi co the mat vai phut.
    (v7.26) Ban exe dong goi (frozen): KHONG pip install vieneu nua —
    exe PyInstaller khong thay site-packages cua Python he thong nen
    pip cai xong tool van import loi 'No module named vieneu'; goi
    vieneu phai BUNDLING trong exe (workflow: pip install
    vieneu==3.8.5 TRUOC onnxruntime-directml + --collect-all vieneu).
    Chi thu import trong tien trinh + khoi tao model lan dau (SDK tu
    tai model neu chua co); import loi thi bao cap nhat tool, KHONG
    bao loi mang, KHONG chay pip.
    Chay .py (dev, khong frozen): pip install qua _python_he_thong()
    (_python_he_thong() -m pip install vieneu, chay ngam bang
    chay_ngam_kwargs()) roi khoi tao model lan dau nhu cu."""
    if getattr(sys, "frozen", False):
        _vieneu_log(log_cb, "Đang kiểm tra gói VieNeu kèm trong tool...")
        try:
            import importlib
            vieneu_mod = importlib.import_module("vieneu")
        except Exception:
            return (False, "Bản tool này chưa kèm gói VieNeu — cập nhật "
                           "tool lên bản mới nhất (VieNeu sẽ kèm trong "
                           "bản cài).")
        return _vieneu_khoi_tao_lan_dau(vieneu_mod, log_cb)
    _vieneu_log(log_cb, "Đang cài gói vieneu bằng pip (có thể mất vài phút)...")
    try:
        kw = chay_ngam_kwargs()
    except Exception:
        kw = {}
    python = _python_he_thong()
    if not python:
        return (False, THIEU_PYTHON_THAT)
    try:
        kq = subprocess.run(
            [python, "-m", "pip", "install", "vieneu"],
            capture_output=True, text=True, timeout=900, **kw)
    except subprocess.TimeoutExpired:
        return (False, "Cài vieneu quá thời gian (15 phút) — kiểm tra mạng "
                       "rồi bấm lại nút “Tải tài nguyên VieNeu”.")
    except Exception as e:
        if _loi_thieu_python_that(e):
            return (False, THIEU_PYTHON_THAT)
        return (False, "Không chạy được pip để cài vieneu: %s" % e)
    if kq.returncode != 0:
        out_gop = (kq.stderr or "") + (kq.stdout or "")
        if _loi_thieu_python_that(out_gop):
            return (False, THIEU_PYTHON_THAT)
        loi = out_gop.strip().splitlines()
        dong_loi = loi[-1] if loi else "không rõ nguyên nhân"
        return (False, "Cài vieneu thất bại: %s — kiểm tra mạng rồi thử lại."
                % dong_loi)
    _vieneu_log(log_cb, "Đã cài xong gói vieneu, đang tải/kiểm tra model lần đầu...")
    try:
        import importlib
        vieneu_mod = importlib.import_module("vieneu")
    except Exception as e:
        return (False, "Đã cài gói vieneu nhưng chưa import được: "
                       "%s — kiểm tra mạng rồi bấm lại nút tải tài nguyên." % e)
    return _vieneu_khoi_tao_lan_dau(vieneu_mod, log_cb)


# ======================================================================
# DOC BANG VIENEU
# ======================================================================

def vieneu_giong_la_vieneu(ten_giong):
    """True neu ten hien thi / id giong thuoc VieNeu (khong phai Edge).
    Nhan ca ten hien thi ("Xuân Vĩnh (VieNeu, nam Bắc)") va id dac biet
    ("vieneu:xuan-vinh") va ten preset goc ("Xuân Vĩnh")."""
    if not ten_giong:
        return False
    t = str(ten_giong).strip()
    if t in VIENEU_PRESET or t in VIENEU_PRESET_TEN_CO_DAU.values():
        return True
    if t in VIENEU_PRESET_ALIAS:
        return True
    if t in (VIENEU_ID_XUAN_VINH, VIENEU_ID_PHAM_TUYEN,
             VIENEU_ID_HAI_DANG):
        return True
    if t.lower().startswith("vieneu:"):
        return True
    if "(VieNeu" in t:
        return True
    return False


def _vieneu_giai_quyet_preset(ten_giong_hien_thi):
    """Tra ve (ten_preset_de_goi, danh_sach_da_thu) de dua vao infer().
    Thu tu: (1) ten co dau DA XAC MINH ("Xuân Vĩnh"), (2) slug phong
    doan ("xuan-vinh"), (3) quet list_preset_voices() cua SDK that
    de khop theo ten (khong dau / co dau, hoa-thuong). Chi tra ve
    cai nao SDK that su co; neu SDK chua cai thi tra (None, [...])."""
    da_thu = []
    # (v7.24, SDK 3.8.5) Ten cu "Minh Quân"/"Minh Quân Pro" chi con
    # la alias -> preset mac dinh moi "Hải Đăng".
    if ten_giong_hien_thi in VIENEU_PRESET_ALIAS:
        ten_giong_hien_thi = VIENEU_GIONG_HAI_DANG
    ten_co_dau = VIENEU_PRESET_TEN_CO_DAU.get(ten_giong_hien_thi)
    if ten_co_dau:
        da_thu.append(ten_co_dau)
        return ten_co_dau, da_thu
    slug = VIENEU_PRESET.get(ten_giong_hien_thi)
    if slug:
        da_thu.append(slug)
    # Ten hien thi la id "vieneu:..." -> suy ra ten co dau tuong ung
    # (quet ca 25 preset, khong rieng 2 giong cu).
    for _ten_ht, _ten_cd in VIENEU_PRESET_TEN_CO_DAU.items():
        if ten_giong_hien_thi == "vieneu:" + VIENEU_PRESET[_ten_ht]:
            da_thu.insert(0, _ten_cd)
            return _ten_cd, da_thu
    # Ten hien thi tuong duong ten preset goc (vd nguoi dung go "Xuân Vĩnh").
    if ten_giong_hien_thi in VIENEU_PRESET_TEN_CO_DAU.values():
        da_thu.insert(0, ten_giong_hien_thi)
        return ten_giong_hien_thi, da_thu
    # Quet danh sach preset that cua SDK (neu cai roi) de khop.
    try:
        import importlib
        mod = importlib.import_module("vieneu")
        lop = getattr(mod, "Vieneu", None)
        if lop is not None:
            tts = lop()
            liet_ke = getattr(tts, "list_preset_voices", None)
            if callable(liet_ke):
                import unicodedata

                def _bo_dau(s):
                    s = unicodedata.normalize("NFKD", str(s))
                    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()
                muc_tieu = _bo_dau(ten_giong_hien_thi)
                for label, vid in liet_ke():
                    da_thu.append(str(label))
                    if _bo_dau(label) == muc_tieu or _bo_dau(vid) == muc_tieu:
                        return str(label), da_thu
    except Exception:
        pass
    return (da_thu[0] if da_thu else None), da_thu


def _vieneu_tao_tts():
    """Khoi tao Vieneu() bang importlib + getattr dong (de khong vo neu
    SDK doi ten lop o ban khac). Tra ve doi tuong tts. Raise RuntimeError
    tieng Viet neu khong khoi tao duoc."""
    try:
        import importlib
        mod = importlib.import_module("vieneu")
    except ImportError as e:
        raise RuntimeError(
            "Chưa cài tài nguyên VieNeu (%s). Bấm nút “Tải tài nguyên "
            "VieNeu” trong tab Đọc phụ đề để cài gói vieneu và tải model, "
            "rồi thử đọc lại." % e)
    lop = getattr(mod, "Vieneu", None)
    if lop is None:
        raise RuntimeError(
            "Gói vieneu đã cài nhưng không có lớp Vieneu (phiên bản SDK lạ). "
            "Thử cập nhật gói vieneu rồi đọc lại.")
    try:
        return lop()
    except Exception as e:
        raise RuntimeError(
            "Không khởi tạo được VieNeu (model có thể chưa tải xong hoặc "
            "thiếu bộ nhớ): %s — bấm nút “Tải tài nguyên VieNeu” để tải "
            "lại model rồi thử đọc lại." % e)


def _vieneu_infer(tts, text, ten_preset):
    """Goi tong hop bang nhieu signature ung vien (phong SDK doi API
    theo phien ban). Thu tu: infer(text, voice=ten), infer(text=text,
    voice=ten), infer(text) [chi khi ten la None], cac ten ham khac
    (synthesize/tts/generate) neu co. Tra ve audio (numpy float32 @
    48 kHz theo tai lieu v3 Turbo). Raise RuntimeError neu tat ca that bai.
    KHONG fallback sang Edge/NamMinh/HoaiMy o day — loi la loi."""
    loi_cuoi = ""
    # (1) API chuan da xac minh: infer(text, voice="<ten co dau>")
    for cach in ("kw", "pos_kw"):
        try:
            if cach == "kw":
                fn = getattr(tts, "infer", None)
                if not callable(fn):
                    break
                return fn(text, voice=ten_preset)
            else:
                fn = getattr(tts, "infer", None)
                if not callable(fn):
                    break
                return fn(text=text, voice=ten_preset)
        except TypeError as e:
            loi_cuoi = "infer(): %s" % e
            continue
        except Exception as e:
            # Loi tong hop that (model/voice) — khong thu signature khac
            # nua, bao thang loi goc de de doan benh.
            raise RuntimeError("VieNeu đọc lỗi với giọng “%s”: %s"
                               % (ten_preset, e))
    # (2) Ten ham khac (ban SDK cu / ban thu nghiem) — thu cho du.
    for ten_fn in ("synthesize", "tts", "generate", "speak"):
        fn = getattr(tts, ten_fn, None)
        if not callable(fn):
            continue
        try:
            return fn(text, voice=ten_preset)
        except TypeError:
            try:
                return fn(text)
            except Exception as e:
                loi_cuoi = "%s(): %s" % (ten_fn, e)
                continue
        except Exception as e:
            loi_cuoi = "%s(): %s" % (ten_fn, e)
            continue
    raise RuntimeError(
        "Không gọi được hàm tổng hợp của VieNeu (đã thử infer/synthesize/"
        "tts/generate; lỗi cuối: %s). Có thể phiên bản SDK đã đổi API — "
        "thử cập nhật gói vieneu rồi đọc lại." % (loi_cuoi or "không rõ"))


def _vieneu_luu_wav(tts, audio, wav_path):
    """Luu audio ra WAV: uu tien tts.save(audio, path) theo tai lieu;
    neu khong co thi ghi thu cong. Raise RuntimeError neu ca hai that bai."""
    luu = getattr(tts, "save", None)
    if callable(luu):
        try:
            luu(audio, wav_path)
            if os.path.isfile(wav_path) and os.path.getsize(wav_path) > 0:
                return
        except Exception:
            pass
    if _vieneu_ghi_wav_thu_cong(audio, wav_path):
        return
    raise RuntimeError("VieNeu đã đọc xong nhưng không lưu được file WAV tạm "
                       "tại %s — kiểm tra quyền ghi thư mục." % wav_path)


def vieneu_doc_mp3(text, ten_giong_hien_thi, duong_dan_ra, toc_do=VIENEU_TOC_DO_MAC_DINH,
                   log_cb=None):
    """Doc 1 doan text bang VieNeu local (ONNX) ra file MP3 chuan
    44100 Hz / stereo / 192k (libmp3lame).
    THAM SO (luu y: thu tu nay KHAC ban mo ta goc vi mo ta goc dat tham
    so co mac dinh (toc_do=0.95) truoc tham so bat buoc (duong_dan_ra)
    — cu phap do khong hop le trong Python — nen duong_dan_ra duoc
    dua len truoc toc_do; goi bang keyword toc_do=/duong_dan_ra= van
    dung nhu cu):
      text: cau can doc (tieng Viet co dau).
      ten_giong_hien_thi: ten hien thi trong 25 preset VieNeu
        (vd "Xuân Vĩnh (VieNeu, nam Bắc)") — nhan ca id
        "vieneu:xuan-vinh", ten preset goc "Xuân Vĩnh", va ten cu
        "Minh Quân"/"Minh Quân Pro" (alias -> "Hải Đăng", SDK 3.8.5).
      duong_dan_ra: file .mp3 dich.
      toc_do: he so nhan (mac dinh 0.95). API infer() cua VieNeu
        KHONG co tham so toc do trong tai lieu doc duoc, nen toc do
        duoc ap dung SAU khi tong hop bang ffmpeg `atempo` (vd 0.95x
        -> atempo=0.95; toc_do=1.0 thi bo qua filter). Giong goc
        khong doi, chi cham/nhanh nhịp doc.
      log_cb: callback log tuy chon.
    Tra ve duong_dan_ra khi xong. Raise RuntimeError (thong bao tieng
    Viet) khi: vieneu chua cai, preset khong khop, doc loi, thieu
    ffmpeg, ghi file loi. TUYET DOI KHONG doc bang giong Edge khac
    (NamMinh/HoaiMy) khi VieNeu loi — ham goi phai bao loi cho nguoi
    dung thay vi tu doi giong."""
    if not text or not str(text).strip():
        raise RuntimeError("Không có nội dung để đọc bằng VieNeu.")
    if not duong_dan_ra:
        raise RuntimeError("Chưa có đường dẫn file MP3 đích để VieNeu ghi ra.")
    ten_preset, da_thu = _vieneu_giai_quyet_preset(ten_giong_hien_thi)
    if not ten_preset:
        raise RuntimeError(
            "Không tìm thấy giọng VieNeu cho “%s” (đã thử: %s). Mở danh "
            "sách giọng của VieNeu (list_preset_voices) để kiểm tra tên "
            "preset thật rồi chọn lại giọng." % (
                ten_giong_hien_thi, ", ".join(da_thu) or "không có ứng viên"))
    ffmpeg = _vieneu_ffmpeg()
    if not ffmpeg:
        raise RuntimeError(
            "Thiếu ffmpeg nên VieNeu không chuyển được WAV sang MP3 chuẩn "
            "44100/stereo/192k — đặt ffmpeg.exe cạnh tool hoặc thêm ffmpeg "
            "vào PATH rồi thử đọc lại.")
    _vieneu_log(log_cb, "VieNeu đang đọc bằng giọng “%s” (tốc độ %.2fx)..."
                % (ten_preset, float(toc_do or VIENEU_TOC_DO_MAC_DINH)))
    tts = _vieneu_tao_tts()
    # Thu preset: ten co dau truoc; neu SDK bao khong co preset do thi
    # thu slug phong doan, roi bao loi ro neu van khong khop.
    audio = None
    loi_preset = ""
    ung_vien_preset = [ten_preset]
    slug = VIENEU_PRESET.get(ten_giong_hien_thi)
    if slug and slug != ten_preset:
        ung_vien_preset.append(slug)
    for preset in ung_vien_preset:
        try:
            audio = _vieneu_infer(tts, str(text), preset)
            ten_preset = preset
            break
        except RuntimeError as e:
            loi_preset = str(e)
            # Chi thu preset tiep theo neu loi noi ro preset khong ton
            # tai; loi khac (model, bo nho) thi dung ngay.
            msg = str(e).lower()
            if "voice" in msg or "preset" in msg or "không tìm" in msg:
                continue
            raise
    if audio is None:
        raise RuntimeError(
            "VieNeu không nhận giọng “%s” (đã thử preset: %s). Lỗi: %s — "
            "kiểm tra lại tên preset bằng list_preset_voices() rồi chọn "
            "lại giọng." % (ten_giong_hien_thi,
                            ", ".join(ung_vien_preset), loi_preset))
    import tempfile
    fd, wav_tam = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        _vieneu_luu_wav(tts, audio, wav_tam)
        # WAV (48 kHz goc) -> MP3 44100/stereo/192k, ap toc do bang atempo.
        atempo = _vieneu_chuoi_atempo(toc_do)
        lenh = [ffmpeg, "-y", "-i", wav_tam]
        if atempo:
            lenh += ["-af", atempo]
        lenh += ["-ar", str(VIENEU_MP3_SAMPLE_RATE), "-ac", "2",
                 "-codec:a", "libmp3lame", "-b:a", VIENEU_MP3_BITRATE,
                 duong_dan_ra]
        try:
            kw = chay_ngam_kwargs()
        except Exception:
            kw = {}
        kq = subprocess.run(lenh, capture_output=True, text=True,
                            timeout=300, **kw)
        if kq.returncode != 0:
            loi = (kq.stderr or "").strip().splitlines()
            raise RuntimeError("ffmpeg chuyển WAV VieNeu sang MP3 lỗi: %s"
                               % (loi[-1] if loi else "không rõ nguyên nhân"))
        if not os.path.isfile(duong_dan_ra) or os.path.getsize(duong_dan_ra) == 0:
            raise RuntimeError("ffmpeg chạy xong nhưng không tạo được file MP3 "
                               "tại %s." % duong_dan_ra)
    finally:
        try:
            if os.path.isfile(wav_tam):
                os.remove(wav_tam)
        except Exception:
            pass
    _vieneu_log(log_cb, "VieNeu đã đọc xong -> %s (giọng %s, %.2fx)."
                % (duong_dan_ra, ten_preset,
                   float(toc_do or VIENEU_TOC_DO_MAC_DINH)))
    return duong_dan_ra


# KIEM_CHUNG (ghi ngay 21/11/2026, gio VN, tren VM Linux nay)
# ======================================================================
# 1. py_compile: DA CHAY 21/11/2026 — `python3 -m py_compile
#    /tmp/v724/vieneu_snippet.py` -> PASS (khong loi cu phap).
#    Smoke test them (import snippet doc lap, chay cac ham khong can
#    model): vieneu_trang_thai() -> (False, False, "VieNeu chưa cài..."),
#    vieneu_giong_la_vieneu() dung ca 3 dang (ten hien thi / id
#    "vieneu:..." / ten preset), _vieneu_chuoi_atempo(0.95) ->
#    "atempo=0.950000", vieneu_doc_mp3() khi chua cai -> RuntimeError
#    tieng Viet dung nhu thiet ke ("Chưa cài tài nguyên VieNeu... bấm
#    nút Tải tài nguyên VieNeu..."). ffmpeg co san tren VM (/usr/bin/ffmpeg).
# 2. import vieneu tren VM nay: KHONG import duoc — `python3 -c
#    "import vieneu"` bao `ModuleNotFoundError: No module named 'vieneu'`
#    (Python 3.12.3, pip 24.0). Model chua tai (chua cai goi thi khong
#    the co model). Khong cai thu vieneu tren VM nay vi task chi yeu cau
#    viet snippet, khong cai dat.
# 3. API VieNeu: DA XAC MINH phan chinh tu tai lieu chinh thuc (PyPI
#    vieneu 3.8.5, 19/11/2026; README HF pnnbao-ump/VieNeu-TTS-v3-Turbo):
#    pip install vieneu; from vieneu import Vieneu; tts.infer(text,
#    voice="Xuân Vĩnh"); tts.save(audio, ...); list_preset_voices();
#    preset "Xuân Vĩnh" / "Phạm Tuyên" (Bac, nam, Natural) la that.
#    (21/11/2026, bo sung) Danh sach 25 preset DA XAC MINH that bang
#    cach cai SDK vieneu 3.8.5 va doc file voices_v3_turbo.json trong
#    package: README SDK v3.7.1 chi co 23 giong, mac dinh "Minh Quân"
#    — da loi thoi; 3.8.5 them "Adam bựa", "Hải Đăng", "Quốc Tuấn",
#    "Thiền Tâm Đức", "Thiện Minh" (Bac), bo "Anh Khôi", "Minh Quân",
#    "Mạnh Dũng" khoi preset chinh ("Minh Quân"/"Minh Quân Pro" chi
#    con la alias -> "Hải Đăng", mac dinh moi cua SDK). Tool VAN giu
#    mac dinh "Xuân Vĩnh" (chinh) / "Phạm Tuyên" (du phong).
# 4. CHUA KIEM CHUNG API VieNeu that bang cach chay tong hop that:
#    chua co lan infer() nao chay thanh cong (tren VM nay hay tren may
#    Windows cua CYAN); chua xac minh: toc do infer() co tham so toc do
#    khong (tai lieu khong thay — nen dung atempo), duong dan cache/model
#    that cua SDK, slug "xuan-vinh"/"pham-tuyen"/... (slug suy tu ten
#    preset bo dau, chi lam ung vien — ten co dau that luon duoc thu
#    truoc), hanh vi that cua Vieneu() lan dau (tai model
#    bao lau / bao nhieu dung luong), va toan bo luong chay tren Windows
#    (pip install, ffmpeg, chay ngam). CAN kiem chung tren may CYAN
#    truoc khi phat hanh v7.24: cai vieneu, bam nut tai tai nguyen, doc
#    thu 1 cau bang tung giong, kiem tra file MP3 bang ffprobe
#    (44100/stereo/192k) va nghe thu toc do 0.95x.
# ======================================================================

# (v7.24) VieNeu: them 25 preset (SDK 3.8.5) vao bang hien-thi -> id
# (id 'vieneu:...' la co danh dau engine rieng, KHONG phai Edge
# voice id). HoaiMy + NamMinh + giong may cu VAN GIU NGUYEN.
GIONG.update({ten: "vieneu:" + slug
              for ten, slug in VIENEU_PRESET.items()})


# (v7.8) Che do dung may chu Edge TTS / giong may local khi xuat MP3
# (dropdown trong khung "Toc do & goi song song", thay the checkbox
# "Cau loi qua so lan thi doc bang giong may local" cu). Key -> ten
# hien thi tren dropdown.
CHE_DO_MAY_CHU_LOCAL = {
    "chi_may_chu": "Chỉ máy chủ",
    "may_chu_local_ngay": "Máy chủ trước, lỗi → local ngay",
    "may_chu_goi_lai_sau": "Máy chủ trước, lỗi → gọi lại sau",
    "local_truoc": "Local trước, lỗi → máy chủ",
    "song_song_ca_hai": "Song song cả hai, lấy cái xong trước",
}
CHE_DO_MAY_CHU_LOCAL_MAC_DINH = "may_chu_goi_lai_sau"


# (v7.8) Che do xu ly cau tran slot khi gop file long tieng
# (dropdown trong khung "Toc do & goi song song"). Key -> ten hien
# thi tren dropdown. "cat" (mac dinh, hanh vi cu): cat duoi cau tran
# bang outpoint khi cau sau bat dau. "de": phan tran KHONG cat ma
# phat NHO (AM_LUONG_TRAN_DE) duoi dau cau sau — cau sau van bat
# dau dung moc gio voi am luong du, loi cau truoc chi nho di.
CAU_TRAN_CHE_DO = {
    "cat": "Cắt đuôi",
    "de": "Đè lên câu sau (câu sau to, câu trước nhỏ)",
}
CAU_TRAN_CHE_DO_MAC_DINH = "cat"
AM_LUONG_TRAN_DE = 0.35  # am luong phan tran khi de (0.0-1.0)


MAU_DOC_THU = "Xin chào, đây là giọng đọc thử."


DO_DAI_TOI_DA_MOT_LAN = 500  # ky tu; cau dai hon se tach nho
# (v7.8) Gioi han do dai van ban 1 lan goi Edge TTS khi gop batch:
# dung chung nguong tach cau dai (500 ky tu) de 1 lan goi batch
# khong qua dai gay timeout/loi.
DO_DAI_TOI_DA_MOT_LAN_GOP_BATCH = DO_DAI_TOI_DA_MOT_LAN
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
    # (v7.24) VieNeu: giong 'vieneu:...' thi doc bang VieNeu local, KHONG di qua Edge.
    if vieneu_giong_la_vieneu(voice):
        try:
            vieneu_doc_mp3(text, voice, duong_dan_ra, toc_do=toc_do, log_cb=log_cb)
            return True, False, ""
        except Exception as _e_vieneu:
            _xoa_file_quiet(duong_dan_ra)
            return False, False, str(_e_vieneu)
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
                text=True, encoding="utf-8", errors="replace",
                **chay_ngam_kwargs())
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
                          ffmpeg, dung=None):
    """Doc 1 doan ngan bang giong may ra file WAV tam, chuyen sang MP3.
    `dung` (threading.Event, tuy chon): nut Huy tat PowerShell ngay."""
    import tempfile
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        ok, ten_giong, loi = _chay_giong_may(text, toc_do, cao_do,
                                             wav_path, log_cb, dung)
        if not ok:
            return False, False, loi
        if log_cb and ten_giong:
            log_cb("  Giọng máy đang dùng: %s" % ten_giong)
        try:
            # (v7.12) Ep ve MP3 chuan 44100 Hz / stereo / 192k /
            # libmp3lame (WAV giong may SAPI thuong la 22050 Hz mono).
            r = subprocess.run([ffmpeg, "-y", "-i", wav_path,
                                "-ar", str(MP3_CHUAN_AR),
                                "-ac", str(MP3_CHUAN_AC),
                                "-c:a", "libmp3lame",
                                "-b:a", MP3_CHUAN_BITRATE,
                                duong_dan_ra],
                               capture_output=True, timeout=120,
                               **chay_ngam_kwargs())
        except Exception as e:
            return False, False, "lỗi chạy ffmpeg: %s" % e
        if (r.returncode != 0 or not os.path.isfile(duong_dan_ra)
                or os.path.getsize(duong_dan_ra) == 0):
            return False, False, "ffmpeg không chuyển được WAV sang MP3"
        return True, False, ""
    finally:
        _xoa_file_quiet(wav_path)


def doc_giong_may(text, toc_do, cao_do, duong_dan_ra, log_cb=None,
                  ffmpeg=None, dung=None):
    """Doc 1 cau bang giong may tren Windows thanh file MP3.
    Tra ve (thanh_cong, False, thong_bao_loi). Can ffmpeg de chuyen
    WAV sang MP3. `dung` (threading.Event, tuy chon): nut Huy tat
    PowerShell ngay ca khi dang doc."""
    if not sys.platform.startswith("win"):
        return False, False, "giọng máy chỉ dùng được trên Windows"
    if not ffmpeg:
        return False, False, ("cần ffmpeg để xuất MP3 bằng giọng máy "
                              "(đặt ffmpeg.exe cạnh tool hoặc thêm vào "
                              "PATH)")
    doan_list = tach_cau_dai(text)
    if len(doan_list) == 1:
        return _doc_giong_may_1_doan(text, toc_do, cao_do, duong_dan_ra,
                                     log_cb, ffmpeg, dung)
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
                                               tam_path, log_cb, ffmpeg,
                                               dung)
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
    # (v7.24) VieNeu: giong "vieneu:..." thi doc bang VieNeu local (ONNX), khong qua Edge/SAPI.
    if vieneu_giong_la_vieneu(voice):
        try:
            vieneu_doc_mp3(text, voice, duong_dan_ra, toc_do=toc_do, log_cb=log_cb)
            return True, False, ""
        except Exception as _e_vieneu:
            return False, False, str(_e_vieneu)
    if voice == "may":
        return doc_giong_may(text, toc_do, cao_do, duong_dan_ra, log_cb,
                             ffmpeg, dung)
    return doc_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra,
                         log_cb, ffmpeg=ffmpeg,
                         timeout_giay=timeout_giay, dung=dung)


async def _doc_batch_stream(text, voice, toc_do, cao_do, duong_dan_ra,
                            bo_xac_minh, proxy=None,
                            timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                            dung=None):
    """(v7.8) Doc 1 doan dai (nhieu cau gop lai) bang Edge TTS, vua ghi
    audio vua thu WordBoundary (moi tu: Offset/Duration theo don vi
    100ns + text). Tra ve danh sach ranh gioi [(offset_giay,
    do_dai_giay, tu), ...]. Giong _doc_mot_doan nhung dung stream()
    thay cho save() de lay duoc WordBoundary. `dung` (threading.Event):
    neu duoc dat giua chung thi ngat stream ngay (nut Huy/Tam dung
    khi goi song song) thay vi doi het timeout."""
    import edge_tts
    import edge_tts.communicate as _comm
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
        rate=_toc_do_sang_edge(toc_do),
        pitch=_dinh_dang_cao_do(cao_do),
        connector=_tao_connector(bo_xac_minh),
        proxy=proxy,
    )
    ranh_gioi = []

    async def _chay():
        da_huy = False
        stream = comm.stream()
        try:
            with open(duong_dan_ra, "wb") as f:
                async for chunk in stream:
                    if dung is not None and dung.is_set():
                        da_huy = True
                        break
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        d = chunk["data"]
                        try:
                            ranh_gioi.append((
                                float(d["Offset"]) / 10_000_000.0,
                                float(d["Duration"]) / 10_000_000.0,
                                d.get("text", "")))
                        except Exception:
                            pass
        finally:
            try:
                await stream.aclose()
            except Exception:
                pass
        return da_huy

    da_huy = await asyncio.wait_for(_chay(),
                                    timeout=max(10, float(timeout_giay)))
    if da_huy:
        raise RuntimeError("đã hủy")
    return ranh_gioi


def _doc_batch_co_failover(text, voice, toc_do, cao_do, duong_dan_ra,
                           log_cb=None,
                           timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                           dung=None):
    """(v7.8) Doc 1 batch (nhieu cau gop lai) thanh file MP3, co
    failover may chu giong Y HET _doc_mot_doan_co_failover (may chu
    goc SSL -> bo xac minh, roi may chu phu SSL -> bo xac minh; gap
    429 thi doi 3 giay truoc khi thu lai). Tra ve (thanh_cong,
    da_dung_bo_xac_minh, ranh_gioi, thong_bao_loi); ranh_gioi la danh
    sach WordBoundary [(offset_giay, do_dai_giay, tu), ...] (rong neu
    may chu khong tra — ben goi se fallback doc le tung cau)."""
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
            return False, False, [], "đã hủy"
        if may_chu == "phu":
            _chuyen_sang_may_chu_phu(log_cb)
            if i == 3:
                time.sleep(2)  # tranh 429 khi vua doi may chu
        ten_may = ("may chu goc" if may_chu == "goc"
                   else "may chu phu")
        try:
            _xoa_file_quiet(duong_dan_ra)
            ranh_gioi = asyncio.run(_doc_batch_stream(
                text, voice, toc_do, cao_do, duong_dan_ra, bo_xac_minh,
                proxy, timeout_giay=timeout_giay, dung=dung))
            if os.path.isfile(duong_dan_ra) and os.path.getsize(
                    duong_dan_ra) > 0:
                if log_cb and may_chu == "phu":
                    log_cb("  OK qua may chu phu api.msedgeservices.com")
                return True, bo_xac_minh, ranh_gioi, ""
            raise RuntimeError("file am thanh rong (0 byte)")
        except ImportError as e:
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
            return False, False, [], loi
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
    return False, False, [], loi_cuoi


def doc_batch_thanh_mp3(text, voice, toc_do, cao_do, duong_dan_ra,
                        log_cb=None, ffmpeg=None,
                        timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                        dung=None):
    """(v7.8) Doc 1 batch (nhieu cau gop lai) thanh file MP3 + thu
    WordBoundary. Chi dung cho Edge TTS (voice != 'may'); giong may
    local khong gop batch duoc (SAPI doc tung cau, khong bi chan 429).
    Tra ve (thanh_cong, da_dung_bo_xac_minh, ranh_gioi, thong_bao_loi).
    Doc loi thi XOA file dich (neu co) de khong de lai file MP3 hong."""
    # (v7.24) VieNeu: doc ca batch bang VieNeu, khong co WordBoundary (ranh_gioi=[]).
    # CHUA KIEM CHUNG: worker cat batch theo ranh gioi co the xu ly ca batch nhu 1 doan —
    # can kiem chung tren may CYAN khi xuat SRT bang giong Xuan Vinh o che do gop batch.
    if vieneu_giong_la_vieneu(voice):
        try:
            vieneu_doc_mp3(text, voice, duong_dan_ra, toc_do=toc_do, log_cb=log_cb)
            return True, False, [], ""
        except Exception as _e_vieneu:
            _xoa_file_quiet(duong_dan_ra)
            return False, False, [], str(_e_vieneu)
    if voice == "may":
        return False, False, [], (
            "gộp batch chỉ dùng cho Edge TTS (giọng máy local đọc "
            "lẻ từng câu)")
    ok, bo_xac_minh, ranh_gioi, loi = _doc_batch_co_failover(
        text, voice, toc_do, cao_do, duong_dan_ra, log_cb,
        timeout_giay=timeout_giay, dung=dung)
    if not ok:
        _xoa_file_quiet(duong_dan_ra)
    return ok, bo_xac_minh, ranh_gioi, loi


def _tach_tu_nho(tu):
    """(v7.9) Tach 1 tu thanh cac don vi nho de so khop voi
    WordBoundary: cat theo gach noi/gach cheo va giua chu-so khi co
    dau cham giua 2 chu so (vd '1-3' -> ['1', '3'], '1.5' ->
    ['1', '5'], 'tan-the' -> ['tan', 'the']). Edge TTS hay tach
    hoac gop khac voi cach tach theo khoang trang trong SRT."""
    import re
    tu = (tu or "").strip()
    if not tu:
        return []
    return [p for p in re.split(r"[-–—/]|(?<=\d)\.(?=\d)", tu) if p]


def _tach_ranh_gioi_cau(ranh_gioi, cac_text):
    """(v7.9) Tach danh sach WordBoundary thanh (bat_dau_giay,
    ket_thuc_giay) cho tung cau, KHOAN DUNG hon ban v7.8.

    Ban v7.8 doi khop TUYET DOI tung tu theo dung thu tu va tong so
    WordBoundary phai bang dung tong so tu — chi can Edge TTS tach
    ('1-3' thanh '1', '3'), gop ('25' + '63' thanh '2563'), them
    ranh gioi cho dau cau, hay bo qua 1 ky tu dac biet la ca batch
    bi huy, phai doc lai tung cau tu dau (doc 2 lan, vua cham vua
    de bi Microsoft chan).

    Ban nay: khop tham lam theo thu tu, cho phep gop/tach don vi
    nho (xem _tach_tu_nho), bo qua ranh gioi chi la dau cau, va neu
    1 cau lech thi chi cau do mat ranh gioi — cac cau khop van cat
    tu file batch, chi cau lech moi doc le lai.

    Tra ve list cung do dai cac_text, moi phan tu la (start, end)
    hoac None neu cau do khong khop du. Tra ve None chi khi khong
    co cau nao khop (ben goi fallback doc le toan bo nhu cu)."""
    import string
    dau_cau = string.punctuation + "“”\"''«»…"

    def _chuan_hoa(tu):
        return (tu or "").strip(dau_cau).lower()

    # Don vi ky vong: (chi_so_cau, don_vi_nho), theo dung thu tu.
    exp = []
    for idx_cau, text in enumerate(cac_text):
        for tu in (text or "").split():
            t = _chuan_hoa(tu)
            if not t:
                continue
            for nho in _tach_tu_nho(t):
                n = _chuan_hoa(nho)
                if n:
                    exp.append((idx_cau, n))
    # Don vi thuc te tu WordBoundary: (offset, dur, don_vi_nho).
    # Bo qua ranh gioi chi la dau cau (vd '!', '?', '...').
    bnd = []
    for off, dur, tu in (ranh_gioi or []):
        t = _chuan_hoa(tu)
        if not t:
            continue
        for nho in _tach_tu_nho(t):
            n = _chuan_hoa(nho)
            if n:
                bnd.append((off, dur, n))
    if not exp or not bnd:
        return None

    def _ghep(bnd_tu, bat_dau, toi_da=3):
        """Ghep toi da `toi_da` don vi lien tiep tu vi tri bat_dau
        thanh 1 chuoi de so voi 1 don vi ky vong. Tra ve
        (chuoi_ghep, so_don_vi) hoac None."""
        ghep = ""
        for k in range(toi_da):
            if bat_dau + k >= len(bnd_tu):
                return None
            ghep += bnd_tu[bat_dau + k]
            yield ghep, k + 1

    ket_qua = [None] * len(cac_text)
    # chi_so ranh gioi da khop cua tung cau (de lay offset dau/cuoi)
    matched_idx = [[] for _ in cac_text]
    i = 0  # con tro don vi ky vong
    j = 0  # con tro don vi WordBoundary
    cau_loi = set()
    while i < len(exp) and j < len(bnd):
        idx_cau, muon = exp[i]
        if idx_cau in cau_loi:
            i += 1
            continue
        if bnd[j][2] == muon:
            matched_idx[idx_cau].append(j)
            i += 1
            j += 1
            continue
        # Edge tach 1 tu thanh nhieu ranh gioi: ghep bnd lai.
        da_khop = False
        for ghep, so_luong in _ghep([b[2] for b in bnd], j):
            if ghep == muon:
                for t in range(so_luong):
                    matched_idx[idx_cau].append(j + t)
                i += 1
                j += so_luong
                da_khop = True
                break
        if da_khop:
            continue
        # Edge gop nhieu tu thanh 1 ranh gioi: ghep exp lai.
        ghep = ""
        for k in range(3):
            if i + k >= len(exp) or exp[i + k][0] != idx_cau:
                break
            ghep += exp[i + k][1]
            if ghep == bnd[j][2]:
                for t in range(k + 1):
                    matched_idx[idx_cau].append(j)
                i += k + 1
                j += 1
                da_khop = True
                break
        if da_khop:
            continue
        # Lech that: bo cau hien tai, dong bo lai o cau sau.
        cau_loi.add(idx_cau)
        matched_idx[idx_cau] = []
        while i < len(exp) and exp[i][0] == idx_cau:
            i += 1
        if i >= len(exp):
            break
        muc_tieu = exp[i][1]
        tim_thay = None
        for t in range(j, min(j + 30, len(bnd))):
            if bnd[t][2] == muc_tieu:
                tim_thay = t
                break
        if tim_thay is None:
            break
        j = tim_thay
    # Cau nao con don vi ky vong chua duyet thi cung la cau loi.
    while i < len(exp):
        cau_loi.add(exp[i][0])
        i += 1
    for idx_cau in range(len(cac_text)):
        if idx_cau in cau_loi or not matched_idx[idx_cau]:
            continue
        # Chi nhan cau khop TRON: so don vi khop phai bang so don
        # vi ky vong cua cau (khong nhan cau khop doan giua).
        tong_don_vi = sum(1 for c, _ in exp if c == idx_cau)
        if len(matched_idx[idx_cau]) < tong_don_vi:
            continue
        dau = matched_idx[idx_cau][0]
        cuoi = matched_idx[idx_cau][-1]
        bat_dau = bnd[dau][0]
        ket_thuc = bnd[cuoi][0] + bnd[cuoi][1]
        if ket_thuc > bat_dau:
            ket_qua[idx_cau] = (bat_dau, ket_thuc)
    # Chong lan giua 2 cau lien ke -> cau sau mat ranh gioi.
    for k in range(1, len(ket_qua)):
        if (ket_qua[k] is not None and ket_qua[k - 1] is not None
                and ket_qua[k][0] < ket_qua[k - 1][1] - 0.001):
            ket_qua[k] = None
    if all(x is None for x in ket_qua):
        return None
    return ket_qua


def _cat_mp3_theo_ranh_gioi(batch_file, bat_dau, ket_thuc, dich, ffmpeg,
                            dung=None):
    """(v7.8) Cat 1 doan MP3 [bat_dau, ket_thuc) tu file batch bang
    ffmpeg (-c copy, cat theo khung MP3, du chinh xac cho buoc gop
    sau vi _ap_dung_toc_do_tu_dong se do lai thoi luong that). Tra ve
    True neu file ra ton tai va > 0 byte."""
    if not ffmpeg or ket_thuc <= bat_dau:
        return False
    _xoa_file_quiet(dich)
    do_dai = max(0.05, ket_thuc - bat_dau)
    cmd = [ffmpeg, "-y", "-i", batch_file, "-ss", "%.3f" % bat_dau,
           "-t", "%.3f" % do_dai, "-c", "copy",
           "-avoid_negative_ts", "make_zero", dich]
    try:
        rc, _err = _chay_ffmpeg_co_gioi_han(cmd, 60, dung=dung,
                                            nhan="cắt câu từ batch")
    except Exception:
        return False
    try:
        return rc == 0 and os.path.isfile(dich) and os.path.getsize(
            dich) > 0
    except OSError:
        return False


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
                capture_output=True, text=True, timeout=30,
                **chay_ngam_kwargs())
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


# (v7.12) Dinh dang MP3 CHUAN cho moi file long tieng xuat ra:
# 44100 Hz, stereo, 192k, libmp3lame — de tuong thich rong voi moi
# phan mem dung video (vd Concat). File cau Edge TTS goc la
# 24000 Hz mono nen gop bang -c copy truoc day cho ra MP3 24k mono,
# ffmpeg cua Concat khong xu ly duoc khi chuyen sang M4A/AAC
# ("filter output failed ... Invalid argument").
MP3_CHUAN_AR = 44100
MP3_CHUAN_AC = 2
MP3_CHUAN_BITRATE = "192k"


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
                            "-ar", str(MP3_CHUAN_AR),
                            "-ac", str(MP3_CHUAN_AC),
                            "-c:a", "libmp3lame",
                            "-b:a", MP3_CHUAN_BITRATE, tam],
                           capture_output=True, timeout=120,
                           **chay_ngam_kwargs())
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
                                stderr=subprocess.DEVNULL,
                                **chay_ngam_kwargs())
        while proc.poll() is None:
            if dung is not None and dung.is_set():
                proc.kill()
                proc.wait()
                return False, "đã dừng nghe thử"
            time.sleep(0.1)
        return True, ""
    except Exception as e:
        return False, "không phát được audio trên hệ này: %s" % e


def _parse_mean_volume(stderr_text):
    """(v7.20) Doc mean_volume (dB) tu log volumedetect cua ffmpeg.
    Tra ve float; '-inf' -> float('-inf'); khong thay -> None."""
    if not stderr_text:
        return None
    m = re.search(r"mean_volume:\s*(-inf|[-0-9.]+)\s*dB", stderr_text)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


# ======================================================================
# (v7.21) TACH AI — MDX-Net (UVR-MDX-NET-Voc_FT) bang onnxruntime +
# numpy. Pipeline theo nomadkaraoke/python-audio-separator (MIT),
# class MDXSeparator + UVR model_data.json. KHONG dung torch (nang,
# build exe to), KHONG bundle model trong exe (64 MB, tai 1 lan o
# muc Tai nguyen AI). Thong so model: n_fft=7680, hop=1024,
# dim_f=3072, dim_t=256, overlap=0.25, compensate=1.021, 44100 Hz
# stereo. (v7.21) Chay CPU (onnxruntime) — khong can CUDA.
# (v7.22) Doi sang onnxruntime-directml: co card DirectX 12 thi
# chay GPU, khong thi tu ve CPU — van khong can cai CUDA.
#   - import onnxruntime CHI o trong ham (lazy): neu build exe
#     thieu onnxruntime thi tool van mo duoc, chi bao loi ro khi
#     bam Tach AI.
#   - tach_ai_mdx_file chay kieu STREAMING (memmap): file dai 2 tieng
#     cung khong doi RAM (ket qua + chia + mix chi nam tren dia).
# ======================================================================
# ======================================================================
# (v7.22) AUDIT GPU — CYAN hoi 21/11 01:42-01:45: "gpu them vao,
# cac chuc nang deu chia gpu vao lam" (tach, gop, SRT->voice) +
# "tool phai quet may truoc, thieu thu vien GPU thi cho tai trong
# tool" + "muc setup GPU cho TAT CA chuc nang lien quan". KET LUAN
# TRUNG THUC sau khi kiem tra tung pipeline trong draft:
#
#   1. TACH NEN AI (MDX-Net, UVR-MDX-NET-Voc_FT) — GPU DUOC.
#      Day la chuc nang DUY NHAT trong tool chay duoc tren GPU cua
#      may. Suy luan mang (Conv/MatMul/...) chay qua DirectML EP.
#      Thiet ke v7.22: doi build sang onnxruntime-directml (xem
#      ly do o duoi) + o chon thiet bi Tu dong / Chi CPU / Chi GPU.
#   2. GOP AM THANH (ffmpeg amix/concat + libmp3lame, atempo) —
#      GPU KHONG DUOC. ffmpeg xu ly am thanh HOAN TOAN bang CPU;
#      NVENC chi tang toc encode VIDEO, tool KHONG encode video
#      (chi xuat MP3/WAV/M4A audio). Voi lai gop audio von nhanh
#      hon realtime nhieu lan nen GPU cung khong giup gi dang ke.
#      -> KHONG co o chon GPU cho gop (khong lam o chon gia).
#   3. GOI SRT TAO VOICE (Edge TTS HoaiMy) — GPU KHONG DUOC.
#      Giong HoaiMy chay tren MAY CHU Microsoft (cloud, wss
#      api.msedgeservices.com): may chi gui text, nhan audio ve —
#      GPU cua may KHONG cham toi duoc. Cac buoc local kem theo
#      (atempo tang toc, concat re-encode MP3) deu la ffmpeg CPU
#      nhu muc 2. -> KHONG co o chon GPU cho long tieng.
#      HUONG TUONG LAI (KHONG lam trong v7.22): TTS local chay GPU
#      — can tai model giong moi (giong se KHONG con la HoaiMy,
#      nang them vai GB, can thu nghiem rieng). Chi ghi ra day de
#      sau nay CYAN hoi thi co san phuong an, khong tu lam them.
#   4. TAI BILIBILI / DICH PHU DE (Gemini/GPT/Claude/web AI) —
#      GPU KHONG DUOC: tai file + goi API cloud, khong co phep
#      tinh nang chay local.
#
#  => Muc "Cai dat GPU" trong tool chi co 1 chuc nang: Tach nen AI.
#     Cac chuc nang khac chi xuat hien trong bang audit nay (bao
#     cao) chu khong co o chon GPU gia trong giao dien.
#
#  THIET KE GPU (DirectML) — tai sao chon cach nay:
#   - onnxruntime va onnxruntime-directml CUNG ten goi import
#     'onnxruntime' (ca 2 wheel deu cai thu muc goc onnxruntime/
#     voi cung cac file capi/onnxruntime.dll, pybind11_state.pyd)
#     nen KHONG THE cai chung trong 1 exe — cai sau ghi de cai
#     truoc. Da kiem chung bang cach tai ca 2 wheel win_amd64
#     cp311 ve liet ke noi dung (21/11).
#   - onnxruntime-directml 1.24.4 la build ORT DAY DU: vua co
#     DmlExecutionProvider vua co CPUExecutionProvider (tai lieu
#     chinh thuc cua DirectML EP + tutorial kiem chung: danh
#     sach provider ky vong la ['DmlExecutionProvider',
#     'CPUExecutionProvider']). Doi build sang goi nay thi 1 goi
#     vua chay GPU vua fallback CPU, khong can cai CUDA Toolkit
#     (DirectML dung DirectX 12 co san tren Windows 10/11).
#   - Wheel directml 25,1 MB (cp311 win_amd64) so voi CPU 16,7 MB
#     -> file exe tang uoc ~8-10 MB (v7.21: 54,3 MB -> v7.22:
#     uoc ~62-64 MB). Wheel co san DirectML.dll 18,5 MB kem theo.
#   - Danh doi: directml moi nhat la 1.24.4, LAG so voi CPU 1.32.0
#     (Microsoft chuyen sang WinML nen directml chi bao tri).
#     Model MDX opset 13 (da kiem chung bang onnx 1.23.2), DirectML
#     ho tro toi opset 20, cac op (Conv/ConvTranspose/BatchNorm/
#     MatMul/Add/Mul/Relu/Transpose) deu duoc ho tro — khong anh
#     huong. API session dung trong tool on dinh qua cac ban.
#   - VI SAO KHONG tai runtime GPU rieng trong tool (nhu model):
#     runtime GPU CHINH LA goi onnxruntime-directml — muon co no
#     thi phai thay the goi onnxruntime dang chay trong tien trinh
#     (cung ten file .dll, Windows se tai dung .dll CPU da nap) nen
#     khong the tai them vao tool dang chay duoc; cach duy nhat
#     dung la CAP NHAT TOOL (ban cai moi da kem san runtime). Vi
#     vay hang "Thu vien GPU" o muc Tai nguyen AI hien trang thai
#     that + nut "Cap nhat tool" (goi luong kiem tra cap nhat san
#     co) khi ban tool dang chay thieu runtime — khong gia vo tai
#     duoc file .dll le.
#   - TAI LIEU DirectML EP (onnxruntime.ai, da doc 21/11): dung DML
#     thi SessionOptions PHAI dat execution_mode=ORT_SEQUENTIAL va
#     enable_mem_pattern=False neu khong tao session loi; DML
#     khong cho Run song song tren cung 1 session (tool chi goi
#     tuan tu tu 1 luong nen on). device_id theo thu tu liet ke
#     DXGI; device 0 thuong KHONG phai card manh nhat tren laptop
#     2 card (tai lieu canh bao ro) nen tool tu liet ke DXGI va
#     chon card co VRAM rieng lon nhat (RTX 3050 4 GB thang Intel
#     UHD). Kiem tra that bang sess.get_providers() — chi tin cai
#     nay, vi get_available_providers() bao AVAILABLE ca khi khong
#     chay duoc that.
# ======================================================================
GPU_TACH_AI_LUA_CHON = {
    "tu_dong": "Tự động (GPU nếu có, không thì CPU)",
    "cpu": "Chỉ CPU",
    "gpu": "Chỉ GPU",
}
GPU_TACH_AI_MAC_DINH = "tu_dong"


def _liet_ke_gpu_dxgi():
    """(v7.22) Liet ke card do hoa qua DXGI (Windows-only).
    Tra ve list [{index, ten, vram_mb}] sap xep theo VRAM rieng
    giam dan (card roi thuong co VRAM lon nhat). Khong phai Windows
    / goi loi -> [] (khong bao gio nem loi). Dung COM truc tiep qua
    ctypes (CreateDXGIFactory + IDXGIFactory::EnumAdapters (vtable
    7) + IDXGIAdapter::GetDesc (vtable 8)); that bai o bat ky buoc
    nao cung tra [] de phan con lai tu ve device_id 0."""
    try:
        if sys.platform != "win32":
            return []
        import ctypes
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [("Data1", wintypes.DWORD),
                        ("Data2", wintypes.WORD),
                        ("Data3", wintypes.WORD),
                        ("Data4", wintypes.BYTE * 8)]

        class LUID(ctypes.Structure):
            _fields_ = [("LowPart", wintypes.DWORD),
                        ("HighPart", wintypes.LONG)]

        class DXGI_ADAPTER_DESC(ctypes.Structure):
            _fields_ = [("Description", wintypes.WCHAR * 128),
                        ("VendorId", wintypes.UINT),
                        ("DeviceId", wintypes.UINT),
                        ("SubSysId", wintypes.UINT),
                        ("Revision", wintypes.UINT),
                        ("DedicatedVideoMemory", ctypes.c_size_t),
                        ("DedicatedSystemMemory", ctypes.c_size_t),
                        ("SharedSystemMemory", ctypes.c_size_t),
                        ("AdapterLuid", LUID)]

        # IID_IDXGIFactory {7B7166EC-21C7-44AE-B21A-C9AE321AE369}.
        iid = GUID(0x7b7166ec, 0x21c7, 0x44ae,
                   (wintypes.BYTE * 8)(0xb2, 0x1a, 0xc9, 0xae,
                                       0x32, 0x1a, 0xe3, 0x69))
        dxgi = ctypes.windll.dxgi
        factory = ctypes.c_void_p()
        hr = dxgi.CreateDXGIFactory(ctypes.byref(iid),
                                    ctypes.byref(factory))
        if hr != 0 or not factory.value:
            return []
        vtab = ctypes.cast(
            factory, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)))
        ket_qua = []
        try:
            enum_fn = ctypes.WINFUNCTYPE(
                ctypes.c_long, ctypes.c_void_p, ctypes.c_uint,
                ctypes.POINTER(ctypes.c_void_p))(vtab[0][7])
            idx = 0
            while idx <= 16:
                adapter = ctypes.c_void_p()
                hr = enum_fn(factory, idx, ctypes.byref(adapter))
                if hr != 0 or not adapter.value:
                    break
                try:
                    vtab_a = ctypes.cast(
                        adapter,
                        ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)))
                    getdesc = ctypes.WINFUNCTYPE(
                        ctypes.c_long, ctypes.c_void_p,
                        ctypes.POINTER(DXGI_ADAPTER_DESC))(vtab_a[0][8])
                    desc = DXGI_ADAPTER_DESC()
                    hr2 = getdesc(adapter, ctypes.byref(desc))
                    ten = (desc.Description or "").strip()
                    if hr2 == 0 and ten:
                        ket_qua.append({
                            "index": idx,
                            "ten": ten,
                            "vram_mb": int(
                                desc.DedicatedVideoMemory // 1048576),
                        })
                finally:
                    try:
                        rel = ctypes.WINFUNCTYPE(
                            ctypes.c_ulong,
                            ctypes.c_void_p)(vtab_a[0][2])
                        rel(adapter)
                    except Exception:
                        pass
                idx += 1
        finally:
            try:
                rel_f = ctypes.WINFUNCTYPE(
                    ctypes.c_ulong, ctypes.c_void_p)(vtab[0][2])
                rel_f(factory)
            except Exception:
                pass
        ket_qua.sort(key=lambda d: d["vram_mb"], reverse=True)
        return ket_qua
    except Exception:
        return []


def quet_gpu_directml(model_path=None):
    """(v7.22) Quet may: thu vien DirectML co khong, card nao, chay
    that duoc khong. Tra ve dict:
      co_thu_vien (bool): 'DmlExecutionProvider' co trong
          ort.get_available_providers() khong.
      co_gpu (True/False/None): True = tao duoc session DML that
          (da thu voi model neu co model_path); False = thu that
          loi / DML khong nhan model; None = chua thu that (chua co
          model de thu).
      ten_gpu / device_id: tu DXGI (card VRAM lon nhat); None neu
          khong liet ke duoc (KHONG tu ve 0 — device 0 tren laptop
          2 card thuong la card onboard, dung nham se chay sai card).
      loi (str|None): ly do ngan khi khong dung duoc.
      da_thu_voi_model (bool).
      khong_xac_dinh_card (bool, v7.23): True neu liet ke DXGI loi
          — khong biet card nao, phan tren phai quyet dinh ro.
    KHONG bao gio nem loi — loi thi tra dict voi co_thu_vien /
    co_gpu False + loi ghi ro."""
    ket_qua = {"co_thu_vien": False, "co_gpu": None, "ten_gpu": None,
               "device_id": None, "loi": None, "da_thu_voi_model": False,
               "khong_xac_dinh_card": False}
    try:
        import onnxruntime as ort
    except Exception as e:
        ket_qua["loi"] = ("chưa có thư viện onnxruntime trong tool "
                          "(cần cập nhật bản mới nhất): %s"
                          % _tom_tat_loi(e))
        return ket_qua
    try:
        ds = list(ort.get_available_providers() or [])
    except Exception as e:
        ket_qua["loi"] = ("không đọc được danh sách execution "
                          "provider: %s" % _tom_tat_loi(e))
        return ket_qua
    if "DmlExecutionProvider" not in ds:
        ket_qua["loi"] = ("bản tool này chưa có thư viện GPU "
                          "(DirectML) — cập nhật tool lên bản mới nhất "
                          "(thư viện GPU kèm trong bản cài).")
        return ket_qua
    ket_qua["co_thu_vien"] = True
    try:
        ds_card = _liet_ke_gpu_dxgi()
    except Exception:
        ds_card = []
    if ds_card:
        # Chon card co VRAM rieng lon nhat (khong phu thuoc thu tu
        # liet ke — DXGI co the tra card tich hop truoc card roi).
        chon = max(ds_card, key=lambda c: c.get("vram_mb") or 0)
        ket_qua["ten_gpu"] = chon["ten"]
        ket_qua["device_id"] = int(chon["index"])
    else:
        # (v7.23) KHONG tu ve device_id 0: device 0 tren laptop
        # 2 card thuong la card onboard (Intel UHD) — dung nham thi
        # DirectML chay tren card onboard trong khi Task Manager
        # hien RTX 3050 0%. De None + co bao de phan tren quyet
        # dinh ro (GPU: dung; Tu dong: ve CPU kem canh bao). Cung
        # KHONG thu session voi device 0 (se thu nham card).
        ket_qua["device_id"] = None
        ket_qua["khong_xac_dinh_card"] = True
        ket_qua["loi"] = ("không liệt kê được card đồ họa "
                          "(DXGI lỗi) — chưa xác định được card rời, "
                          "không dùng GPU để tránh chạy nhầm card "
                          "onboard. Kiểm tra driver card đồ họa.")
        return ket_qua
    if not model_path or not os.path.isfile(model_path):
        ket_qua["loi"] = ("thư viện GPU đã có — chưa thử với model "
                          "(chưa tải model), sẽ kiểm tra khi tách.")
        return ket_qua
    # Thu that: tao session DML voi model that, kiem tra
    # get_providers() (chi tin cai nay — get_available_providers
    # bao AVAILABLE ca khi khong chay duoc that).
    try:
        so = ort.SessionOptions()
        so.log_severity_level = 3
        try:
            so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        except Exception:
            pass
        try:
            so.enable_mem_pattern = False
        except Exception:
            pass
        prov = [(("DmlExecutionProvider",
                  {"device_id": int(ket_qua["device_id"])})),
                "CPUExecutionProvider"]
        sess = ort.InferenceSession(model_path, providers=prov,
                                    sess_options=so)
        dung = list(sess.get_providers() or [])
        ket_qua["da_thu_voi_model"] = True
        if "DmlExecutionProvider" in dung:
            ket_qua["co_gpu"] = True
            ket_qua["loi"] = None
        else:
            ket_qua["co_gpu"] = False
            ket_qua["loi"] = ("DirectML không nhận model này "
                              "(session chỉ dùng CPU) — sẽ dùng CPU.")
        try:
            del sess
        except Exception:
            pass
    except Exception as e:
        ket_qua["co_gpu"] = False
        ket_qua["da_thu_voi_model"] = True
        ket_qua["loi"] = "GPU không dùng được: %s" % _tom_tat_loi(e)
    return ket_qua


def van_ban_trang_thai_gpu(ket_qua, che_do="tu_dong"):
    """(v7.22) Dong trang thai GPU hien canh o chon thiet bi.
    ket_qua None = chua quet xong."""
    ten_che_do = {"tu_dong": "Tự động", "cpu": "Chỉ CPU",
                  "gpu": "Chỉ GPU"}.get(che_do or "tu_dong", "Tự động")
    if ket_qua is None:
        return ("Thiết bị tách AI: %s — GPU: đang quét máy..."
                % ten_che_do)
    if not ket_qua.get("co_thu_vien"):
        return ("Thiết bị tách AI: %s — GPU: chưa có thư viện "
                "DirectML trong bản tool này (vào mục 'Tài nguyên AI' "
                "bấm 'Cập nhật tool')." % ten_che_do)
    if ket_qua.get("khong_xac_dinh_card"):
        # (v7.23) Liet ke DXGI loi: bao ro, dung im lang dung
        # device 0 (co the la card onboard).
        return ("Thiết bị tách AI: %s — GPU: không xác định được "
                "card đồ họa (liệt kê DXGI lỗi) — chế độ 'Chỉ GPU' "
                "sẽ dừng, 'Tự động' sẽ dùng CPU để tránh chạy nhầm "
                "card onboard. Kiểm tra driver card đồ họa."
                % ten_che_do)
    ten = (ket_qua.get("ten_gpu") or "").strip()
    ten_hien = (" (%s)" % ten) if ten else ""
    if ket_qua.get("co_gpu") is True:
        return ("Thiết bị tách AI: %s — GPU%s (DirectML) — sẵn sàng."
                % (ten_che_do, ten_hien))
    if ket_qua.get("co_gpu") is False:
        return ("Thiết bị tách AI: %s — GPU%s không dùng được (%s) — "
                "sẽ dùng CPU." % (ten_che_do, ten_hien,
                                  ket_qua.get("loi") or "không rõ lý do"))
    return ("Thiết bị tách AI: %s — GPU: thư viện DirectML đã có, "
            "chưa thử với model (chưa tải model) — sẽ kiểm tra khi "
            "tách." % ten_che_do)


def giai_quyet_providers_tach_ai(che_do, ket_qua_quet):
    """(v7.22) Giai quyet providers theo che do thiet bi + ket qua
    quet. Tra ve (providers, device_id, loi, dung_gpu):
      - providers None nghia la DUNG LAI (khong tach), loi giai
        thich ro ly do (hien cho nguoi dung).
      - 'cpu' -> chi CPU, luon tach duoc.
      - 'gpu' -> chi GPU: thieu thu vien / GPU khong dung duoc thi
        DUNG, KHONG tu ve CPU trong im lang.
      - 'tu_dong' -> GPU neu quet thay dung duoc (hoac chua thu
        that thi cu thu GPU), khong thi CPU.
    ket_qua_quet None -> coi nhu chua quet: tu_dong ve CPU (an
    toan), gpu thi dung voi loi 'chua quet xong'."""
    che_do = (che_do or "tu_dong").strip().lower()
    if che_do not in ("tu_dong", "cpu", "gpu"):
        che_do = "tu_dong"
    if che_do == "cpu":
        return ["CPUExecutionProvider"], 0, None, False
    kq = ket_qua_quet or {}
    if not kq.get("co_thu_vien"):
        loi = (kq.get("loi")
               or "máy chưa có thư viện GPU (DirectML) — vào mục "
               "'Tài nguyên AI' bấm 'Cập nhật tool' để tải bản mới "
               "(thư viện GPU kèm trong bản cài).")
        if che_do == "gpu":
            return None, 0, loi, False
        return ["CPUExecutionProvider"], 0, None, False
    if kq.get("co_gpu") is False:
        loi = kq.get("loi") or "GPU không dùng được trên máy này."
        if che_do == "gpu":
            return None, 0, loi, False
        return ["CPUExecutionProvider"], 0, None, False
    did = kq.get("device_id")
    if did is None:
        # (v7.23) Khong biet card nao (DXGI loi): GPU thi DUNG —
        # KHONG doan device 0 (de chay nham card onboard); Tu dong
        # thi ve CPU (phan goi se log canh bao ro).
        if che_do == "gpu":
            return None, 0, (kq.get("loi")
                             or "không xác định được card đồ họa "
                             "(liệt kê DXGI lỗi) — không dùng GPU để "
                             "tránh chạy nhầm card onboard."), False
        return ["CPUExecutionProvider"], 0, None, False
    did = int(did)
    return [("DmlExecutionProvider", {"device_id": did}),
            "CPUExecutionProvider"], did, None, True


def tach_ai_mdx_file_voi_thiet_bi(nguon_f32, so_mau, model, model_path,
                                  dich_f32, che_do, ket_qua_quet,
                                  tien_trinh_cb=None, dung=None,
                                  log_cb=None, dich_giong_f32=None):
    """(v7.22) Tach AI theo che do thiet bi ('tu_dong'/'cpu'/'gpu').
    Tra ve (ok, loi, thiet_bi_da_dung) — thiet_bi_da_dung: 'gpu' /
    'cpu' / None (khong tach duoc). Quy tac:
      - 'gpu': thieu thu vien / GPU loi -> DUNG, tra loi ro, KHONG
        tu ve CPU.
      - 'tu_dong': thu GPU truoc; GPU loi (tao session / chay
        model) -> ghi log ro roi tach lai tu dau bang CPU 1 lan.
        Huy giua chung thi KHONG tach lai.
      - 'cpu': nhu cu.
    File tam ket qua duoc tao moi moi lan goi tach_ai_mdx_file nen
    tach lai tu dau la sach (khong dinh ket qua do cua lan GPU)."""
    def _log(s):
        if log_cb is not None:
            try:
                log_cb(s)
            except Exception:
                pass

    providers, did, loi_giai, dung_gpu = giai_quyet_providers_tach_ai(
        che_do, ket_qua_quet)
    if providers is None:
        return False, loi_giai, None
    ok, loi = tach_ai_mdx_file(
        nguon_f32, so_mau, model, model_path, dich_f32,
        tien_trinh_cb=tien_trinh_cb, dung=dung,
        providers=providers, device_id=did,
        dich_giong_f32=dich_giong_f32)
    if ok:
        return True, "", "gpu" if dung_gpu else "cpu"
    if (loi or "") == "đã hủy":
        return False, loi, None
    if (che_do or "tu_dong") == "tu_dong" and dung_gpu:
        _log("GPU lỗi (%s) — chuyển sang tách bằng CPU." % loi)
        ok2, loi2 = tach_ai_mdx_file(
            nguon_f32, so_mau, model, model_path, dich_f32,
            tien_trinh_cb=tien_trinh_cb, dung=dung,
            providers=["CPUExecutionProvider"], device_id=0,
            dich_giong_f32=dich_giong_f32)
        if ok2:
            return True, "", "cpu"
        return False, loi2, None
    if (che_do or "tu_dong") == "gpu":
        return False, ("GPU không dùng được: %s — kiểm tra driver "
                       "card đồ họa, hoặc chọn 'Tự động' để tool "
                       "tự về CPU." % loi), None
    return False, loi, None


def _do_am_luong_trung_binh_file(ffmpeg, duong, dung=None):
    """(v7.23) Am luong trung binh toan file (volumedetect) o cap
    module — dung cho ham tach dung chung (ca tab Xu ly am thanh
    lan luong tach truoc khi long). Tra ve float dB, None neu khong
    do duoc (bao gom ca Huy). Khong bao gio nem loi."""
    cmd = [ffmpeg, "-y", "-i", duong, "-map", "0:a",
           "-af", "volumedetect", "-f", "null", "-"]
    try:
        rc, err = _chay_ffmpeg_co_gioi_han(
            cmd, 1800, dung=dung, nhan="đo âm lượng file tách AI")
    except TimeoutError:
        return None
    if rc != 0:
        return None
    return _parse_mean_volume(err)


def tach_ai_tach_nen_va_giong(ffmpeg, goc, che_do_tb, ket_qua_quet,
                              bitrate, log_cb=None, tien_trinh_cb=None,
                              dung=None):
    """(v7.23) Tach AI DUNG CHUNG cho nut 'Tach nen' o tab Xu ly am
    thanh va pha 1 cua luong 'tach + long mot lan' o tab Doc phu de:
    giai ma file goc -> tach AI (streaming, bao % theo chunk) -> ma
    hoa CA 2 file MP3 (nen + giong goc, cung chuan 44.1k/stereo/
    bitrate da chon) -> cua chat luong + kiem tra cam.
    Tra ve (True, info, "") neu xong, (False, None, loi) neu loi /
    da huy. info = {"nen": path, "giong_goc": path, "thiet_bi":
    "gpu"/"cpu", "ten_card": str|None, "device_id": int|None,
    "thong_tin_nen": str, "thong_tin_giong": str,
    "vol_giong_goc": float|None}. log_cb(s) nhan log thuong;
    tien_trinh_cb(0-100) nhan % tach; dung (Event) de Huy.
    KHONG cham vao Tk — goi tu luong phu duoc. File tam f32 luon
    duoc xoa sau khi xong/loi/huy."""
    def _log(s):
        if log_cb is not None:
            try:
                log_cb(s)
            except Exception:
                pass

    model = AI_TACH_MODELS[0]
    trang_thai, duong_model = trang_thai_model_ai(model)
    if trang_thai == "thieu":
        return False, None, (
            "Chưa có model AI — mở mục 'Tài nguyên AI' rồi bấm "
            "'Tải' model, sau đó bấm lại 'Tách nền'.")
    if trang_thai == "sai":
        return False, None, (
            "Model AI bị sai — mở mục 'Tài nguyên AI' rồi bấm "
            "'Tải' để tải lại.")
    try:
        import onnxruntime  # noqa: F401 (lazy — bao loi ro neu thieu)
    except Exception as e:
        return False, None, (
            "Thiếu thư viện onnxruntime — cập nhật bản tool mới "
            "nhất rồi thử lại: %s" % _tom_tat_loi(e))
    ffprobe = tim_ffprobe(ffmpeg)
    tong_giay = lay_thoi_luong(ffprobe, goc) if ffprobe else None
    dich_nen = ten_file_nen_lam_viec(goc)
    dich_giong = ten_file_giong_goc_lam_viec(goc)
    thu_muc = os.path.dirname(dich_nen) or "."
    tam_f32 = os.path.join(thu_muc, "_ai-tach-tam-goc.f32")
    inst_f32 = os.path.join(thu_muc, "_ai-tach-tam-nen.f32")
    giong_f32 = os.path.join(thu_muc, "_ai-tach-tam-giong.f32")
    try:
        # (v7.22) Thiet bi doc 1 lan luc bat dau chay. (v7.23) Neu
        # khong xac dinh duoc card (DXGI loi) ma che do la Tu dong
        # thi ve CPU kem canh bao ro — khong im lang dung device 0
        # (de chay nham card onboard).
        if ((che_do_tb or "tu_dong") == "tu_dong"
                and isinstance(ket_qua_quet, dict)
                and ket_qua_quet.get("khong_xac_dinh_card")):
            _log("CẢNH BÁO: không xác định được card đồ họa (liệt kê "
                 "DXGI lỗi) — tách bằng CPU để tránh chạy nhầm card "
                 "onboard. Kiểm tra driver card đồ họa.")
        _prov, _did, _loi_gt, _dg = giai_quyet_providers_tach_ai(
            che_do_tb, ket_qua_quet)
        if _prov is None:
            return False, None, _loi_gt
        ten_card = None
        if isinstance(ket_qua_quet, dict):
            ten_card = (ket_qua_quet.get("ten_gpu") or "").strip() or None
        if che_do_tb == "gpu":
            _log("Đang tách AI bằng GPU (DirectML, model "
                 "UVR-MDX-NET-Voc_FT): %s" % goc)
        elif che_do_tb == "cpu":
            _log("Đang tách AI bằng CPU (model UVR-MDX-NET-Voc_FT): "
                 "%s" % goc)
        else:
            _log("Đang tách AI (Tự động — thử GPU trước, lỗi thì "
                 "về CPU; model UVR-MDX-NET-Voc_FT): %s" % goc)
        # 1. Giai ma goc ve f32le stereo 44100 Hz.
        cmd = [ffmpeg, "-y", "-i", goc, "-map", "0:a",
               "-ar", "44100", "-ac", "2", "-f", "f32le", tam_f32]
        timeout_giai_ma = (max(300, int(tong_giay) + 120)
                           if tong_giay else 600)
        try:
            rc, err = _chay_ffmpeg_co_gioi_han(
                cmd, timeout_giai_ma, dung=dung,
                nhan="giải mã cho tách AI")
        except TimeoutError:
            return False, None, "Giải mã file gốc hết thời gian chờ."
        if rc == -1:
            return False, None, "đã hủy"
        if rc != 0 or not os.path.isfile(tam_f32):
            tail = (err or "").strip()[-600:]
            return False, None, ("Giải mã file gốc lỗi (mã %s).%s"
                                 % (rc, ("\n" + tail) if tail else ""))
        so_mau = os.path.getsize(tam_f32) // 8
        if so_mau <= 0:
            return False, None, "File gốc không có âm thanh."
        # 2. Tach AI (streaming, bao % theo chunk, khong timeout).
        ok, loi, thiet_bi = tach_ai_mdx_file_voi_thiet_bi(
            tam_f32, so_mau, model, duong_model, inst_f32,
            che_do_tb, ket_qua_quet,
            tien_trinh_cb=tien_trinh_cb, dung=dung,
            log_cb=_log, dich_giong_f32=giong_f32)
        if not ok:
            if loi == "đã hủy":
                return False, None, "đã hủy"
            return False, None, "Tách AI lỗi: %s" % loi
        if not (os.path.isfile(inst_f32)
                and os.path.getsize(inst_f32) > 0):
            return False, None, "Tách AI xong nhưng không ra file nền."
        if not (os.path.isfile(giong_f32)
                and os.path.getsize(giong_f32) > 0):
            return False, None, "Tách AI xong nhưng không ra file giọng gốc."
        # 3. Ma hoa CA 2 file ve MP3 (chuan nhu tach ffmpeg).
        if tien_trinh_cb is not None:
            try:
                tien_trinh_cb(0.0)
            except Exception:
                pass
        timeout_ma_hoa = (max(300, int(tong_giay) + 120)
                          if tong_giay else 600)
        for f32_path, dich_mp3, nhan in (
                (inst_f32, dich_nen, "mã hóa nền AI"),
                (giong_f32, dich_giong, "mã hóa giọng gốc AI")):
            cmd = [ffmpeg, "-y", "-f", "f32le", "-ar", "44100",
                   "-ac", "2", "-i", f32_path, "-ar", "44100",
                   "-ac", "2", "-c:a", "libmp3lame", "-b:a", bitrate,
                   dich_mp3]
            try:
                rc, err = _chay_ffmpeg_co_gioi_han(
                    cmd, timeout_ma_hoa, dung=dung, nhan=nhan)
            except TimeoutError:
                return False, None, ("Mã hóa file %s hết thời gian chờ."
                                     % ("nền" if dich_mp3 == dich_nen
                                        else "giọng gốc"))
            if rc == -1:
                return False, None, "đã hủy"
            if rc != 0 or not (os.path.isfile(dich_mp3)
                               and os.path.getsize(dich_mp3) > 0):
                tail = (err or "").strip()[-600:]
                _ghi_log_loi_ffmpeg(os.path.dirname(dich_mp3) or ".",
                                    tail or "ffmpeg lỗi không rõ")
                return False, None, (
                    "ffmpeg mã hóa %s lỗi (mã %s).%s"
                    % ("nền" if dich_mp3 == dich_nen else "giọng gốc",
                       rc, ("\n" + tail) if tail else ""))
        # 4. Cua chat luong (v7.17) cho ca 2 file + kiem tra cam.
        ok, thong_tin_nen = _kiem_tra_chat_luong_am_thanh(
            dich_nen, ffmpeg, "mp3", bitrate)
        if not ok:
            return False, None, ("File nền tách AI ra không đạt chuẩn: %s"
                                 % thong_tin_nen)
        ok, thong_tin_giong = _kiem_tra_chat_luong_am_thanh(
            dich_giong, ffmpeg, "mp3", bitrate)
        if not ok:
            return False, None, (
                "File giọng gốc tách AI ra không đạt chuẩn: %s"
                % thong_tin_giong)
        vol_nen = _do_am_luong_trung_binh_file(ffmpeg, dich_nen, dung)
        if vol_nen is not None and vol_nen < -50.0:
            # Chi ket luan cam khi file goc nghe duoc (do duoc va
            # > -50 dB); probe do khong duoc thi khong chan viec
            # (theo thong le v7.20).
            vol_goc = _do_am_luong_trung_binh_file(ffmpeg, goc, dung)
            if vol_goc is not None and vol_goc > -50.0:
                for p in (dich_nen, dich_giong):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
                return False, None, (
                    "File nền tách AI ra gần như câm (%.1f dB) — "
                    "model không tách được nhạc trong file này. File "
                    "nền câm KHÔNG được dùng; thử tách bằng AI trong "
                    "CapCut rồi chọn chế độ 'Giữ nguyên, chỉ chỉnh "
                    "âm lượng'." % vol_nen)
        # (v7.23) Giong goc cam thi CHI CANH BAO, van giu file
        # (file goc co the khong co giong noi, hoac model khong tach
        # duoc giong) — tron voi am luong 0% thi khong anh huong gi.
        vol_giong = _do_am_luong_trung_binh_file(ffmpeg, dich_giong,
                                                dung)
        if vol_giong is not None and vol_giong < -50.0:
            vol_goc = _do_am_luong_trung_binh_file(ffmpeg, goc, dung)
            if vol_goc is not None and vol_goc > -50.0:
                _log("CẢNH BÁO: file giọng gốc tách AI ra gần như câm "
                     "(trung bình %.1f dB) — có thể file gốc không có "
                     "giọng nói, hoặc model không tách được giọng "
                     "trong file này. File giọng gốc vẫn giữ lại; "
                     "trộn với âm lượng 0%% sẽ không ảnh hưởng gì."
                     % vol_giong)
        return True, {"nen": dich_nen, "giong_goc": dich_giong,
                      "thiet_bi": thiet_bi, "ten_card": ten_card,
                      "device_id": _did,
                      "thong_tin_nen": thong_tin_nen,
                      "thong_tin_giong": thong_tin_giong,
                      "vol_giong_goc": vol_giong}, ""
    finally:
        _xoa_file_quiet(tam_f32)
        _xoa_file_quiet(inst_f32)
        _xoa_file_quiet(giong_f32)


AI_TACH_MODELS = [
    {"id": "voc_ft",
     "ten": "UVR-MDX-NET-Voc_FT (tách giọng)",
     "file": "UVR-MDX-NET-Voc_FT.onnx",
     "url": "https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR-MDX-NET-Voc_FT.onnx",
     "size": 66762490,
     "sha256": "534b2070fcc7df514b13ef660dc8cbb328679c2374d04354a5c42bb14ecce111",
     "n_fft": 7680, "hop": 1024, "dim_f": 3072, "dim_t": 256,
     "compensate": 1.021},
]


def thu_muc_tai_nguyen_ai_mac_dinh(cfg=None):
    """Thu muc tai nguyen AI mac dinh: <thu muc luu>/TaiNguyenAI.
    Thu muc luu la thu muc CYAN chon o tab Quan ly (config
    output_dir) — KHONG bao gio ep o C:."""
    try:
        cfg = cfg or doc_config()
        luu = (cfg.get("output_dir") or "").strip()
        if not luu or not os.path.isdir(luu):
            luu = mac_dinh_thu_muc_luu()
    except Exception:
        luu = mac_dinh_thu_muc_luu()
    return os.path.join(luu, "TaiNguyenAI")


def lay_thu_muc_tai_nguyen_ai(cfg=None):
    """Thu muc tai nguyen AI hien tai (config ai_tach_thu_muc, hoac
    mac dinh <thu muc luu>/TaiNguyenAI)."""
    try:
        cfg = cfg or doc_config()
        p = (cfg.get("ai_tach_thu_muc") or "").strip()
        if p:
            return p
    except Exception:
        pass
    return thu_muc_tai_nguyen_ai_mac_dinh(cfg)


def duong_dan_model_ai(model, thu_muc=None):
    thu_muc = thu_muc or lay_thu_muc_tai_nguyen_ai()
    return os.path.join(thu_muc, model["file"])


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def trang_thai_model_ai(model, thu_muc=None):
    """Tra ve ("co", duong_dan) / ("thieu", duong_dan) /
    ("sai", duong_dan): 'sai' = co file nhung sai kich thuoc/hash."""
    p = duong_dan_model_ai(model, thu_muc)
    if not os.path.isfile(p):
        return "thieu", p
    try:
        if os.path.getsize(p) != int(model["size"]):
            return "sai", p
        if _sha256_file(p) != str(model["sha256"]).lower():
            return "sai", p
    except Exception:
        return "sai", p
    return "co", p


def tai_file_co_tien_trinh(url, dich_tam, tien_trinh_cb=None, dung=None,
                           timeout=30):
    """Tai URL ve dich_tam (file tam), bao tien trinh qua
    cb(da_tai, tong). Tra ve (True, "") hoac (False, loi).
    Dung urllib (khong can requests)."""
    import urllib.request
    req = urllib.request.Request(
        url, headers={"User-Agent": "ChipChipStudio/7.22"})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except Exception as e:
        return False, "không mở được link tải: %s" % _tom_tat_loi(e)
    try:
        tong = resp.getheader("Content-Length")
        try:
            tong = int(tong) if tong else None
        except Exception:
            tong = None
        da = 0
        with open(dich_tam, "wb") as f:
            while True:
                if dung is not None and dung.is_set():
                    return False, "đã hủy"
                try:
                    khoi = resp.read(1024 * 1024)
                except Exception as e:
                    return False, "lỗi mạng khi tải: %s" % _tom_tat_loi(e)
                if not khoi:
                    break
                f.write(khoi)
                da += len(khoi)
                if tien_trinh_cb is not None:
                    try:
                        tien_trinh_cb(da, tong)
                    except Exception:
                        pass
        return True, ""
    finally:
        try:
            resp.close()
        except Exception:
            pass


def _mdx_hann_periodic(n):
    """Cua so Hann tuan hoan (nhu torch.hann_window(periodic=True))."""
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * np.arange(n) / n)


def _mdx_stft(wave, n_fft, hop):
    """STFT: wave (2, N) float64 -> complex (2, n_fft//2+1, frames).
    Cua so Hann tuan hoan, center=True (reflect pad n_fft//2)."""
    pad = n_fft // 2
    padded = np.pad(wave, ((0, 0), (pad, pad)), mode="reflect")
    win = _mdx_hann_periodic(n_fft)
    n_frames = 1 + (padded.shape[1] - n_fft) // hop
    shape = (2, n_frames, n_fft)
    strides = (padded.strides[0], hop * padded.strides[1],
               padded.strides[1])
    frames = np.lib.stride_tricks.as_strided(
        padded, shape=shape, strides=strides)
    return np.fft.rfft(frames * win, n=n_fft, axis=-1).transpose(0, 2, 1)


def _mdx_istft(spec, n_fft, hop, length):
    """iSTFT: spec (2, F, T) complex -> (2, length) float64.
    OLA chia cho tong binh phuong cua so, roi cat pad 2 dau."""
    win = _mdx_hann_periodic(n_fft)
    frames = spec.shape[2]
    y_len = (frames - 1) * hop + n_fft
    y = np.zeros((2, y_len), dtype=np.float64)
    denom = np.zeros(y_len, dtype=np.float64)
    win2 = win * win
    for t in range(frames):
        s = t * hop
        y[:, s:s + n_fft] += (np.fft.irfft(spec[:, :, t], n=n_fft,
                                          axis=-1) * win)
        denom[s:s + n_fft] += win2
    denom[denom < 1e-10] = 1.0
    y /= denom
    pad = n_fft // 2
    return y[:, pad:pad + length]


class _MDXTachAI:
    """Engine tach AI MDX-Net (1 model UVR-MDX-NET-Voc_FT).
    Pipeline giong audio-separator MDXSeparator.demix (overlap 0.25,
    chunk 261120 mau, trim 3840, cua so Hann, overlap-add)."""

    def __init__(self, model, providers=None, device_id=0):
        self.model = model
        # (v7.22) providers: None/mac dinh -> CPU (hanh vi cu v7.21).
        # GPU: [("DmlExecutionProvider", {"device_id": N}),
        #       "CPUExecutionProvider"] — DML truoc, CPU fallback
        # theo tung node (ORT tu chia node cho provider lam duoc).
        self.providers = (list(providers) if providers
                          else ["CPUExecutionProvider"])
        self.device_id = int(device_id or 0)
        self.providers_thuc_te = None  # get_providers() sau khi tao session
        self.n_fft = int(model["n_fft"])
        self.hop = int(model["hop"])
        self.dim_f = int(model["dim_f"])
        self.dim_t = int(model["dim_t"])
        self.compensate = float(model["compensate"])
        self.chunk_size = self.hop * (self.dim_t - 1)   # 261120
        self.trim = self.n_fft // 2                     # 3840
        self.gen_size = self.chunk_size - 2 * self.trim  # 253440
        self.step = int(0.75 * self.chunk_size)         # 195840
        self._sess = None

    def _session(self, model_path):
        if self._sess is None:
            import onnxruntime as ort
            so = ort.SessionOptions()
            so.log_severity_level = 3
            providers = list(self.providers)
            dung_dml = any(
                p == "DmlExecutionProvider"
                or (isinstance(p, (list, tuple)) and p
                    and p[0] == "DmlExecutionProvider")
                for p in providers)
            if dung_dml:
                # (v7.22) Tai lieu DirectML EP: dung DML thi
                # execution_mode PHAI ORT_SEQUENTIAL va
                # enable_mem_pattern PHAI False, khong thi tao
                # session loi. DML cung khong cho Run song song
                # tren cung 1 session — tool chi goi tuan tu tu
                # 1 luong nen on.
                try:
                    so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
                except Exception:
                    pass
                try:
                    so.enable_mem_pattern = False
                except Exception:
                    pass
            self._sess = ort.InferenceSession(
                model_path, providers=providers, sess_options=so)
            try:
                self.providers_thuc_te = list(
                    self._sess.get_providers() or [])
            except Exception:
                self.providers_thuc_te = None
        return self._sess

    def _chay_model_1_chunk(self, chunk, model_path):
        """chunk (2, 261120) float64 -> vocal chunk (2, 261120)."""
        spec = _mdx_stft(chunk, self.n_fft, self.hop)
        packed = np.stack([spec.real[0], spec.imag[0],
                           spec.real[1], spec.imag[1]], axis=0)
        packed = packed[None, :, :self.dim_f, :].astype(np.float32)
        packed[:, :, :3, :] = 0.0
        out = self._session(model_path).run(None, {"input": packed})[0]
        back = np.zeros((2, self.n_fft // 2 + 1, out.shape[3]),
                        dtype=np.complex128)
        back[0, :self.dim_f, :] = out[0, 0] + 1j * out[0, 1]
        back[1, :self.dim_f, :] = out[0, 2] + 1j * out[0, 3]
        return _mdx_istft(back, self.n_fft, self.hop, chunk.shape[1])


def tach_ai_mdx_file(nguon_f32, so_mau, model, model_path, dich_f32,
                     tien_trinh_cb=None, dung=None,
                     providers=None, device_id=0, dich_giong_f32=None):
    """Tach AI 1 file f32le stereo 44100 Hz (nguon_f32, so_mau mau).
    Ghi instrumental (nen) f32le ra dich_f32. (v7.23) Neu co
    dich_giong_f32 thi ghi them vocal (giong goc) f32le ra do:
    vocal = (ket_qua/chia) * (compensate/scale) — cung don vi voi
    instrumental nen nen + giong goc cong lai ~ file goc. Bao %
    (0-100) qua tien_trinh_cb. Tra ve (True, "") hoac (False, loi).
    Chay kieu STREAMING (memmap): file dai 2 tieng cung khong doi
    RAM — ket qua + chia + mix chi nam tren dia. Tam file ket qua
    duoc xoa trong finally."""
    import gc
    if np is None:
        return False, ("chưa có thư viện numpy trong tool "
                       "(cần cập nhật bản mới)")
    # (v7.22) providers None -> CPU (hanh vi cu v7.21); GPU thi
    # goi tach_ai_mdx_file_voi_thiet_bi de giai quyet che do truoc.
    eng = _MDXTachAI(model, providers=providers, device_id=device_id)
    n = int(so_mau)
    if n <= 0:
        return False, "file gốc không có mẫu âm thanh"
    mix_mm = None
    ket_qua = None
    chia = None
    dir_tam = os.path.dirname(os.path.abspath(dich_f32))
    ket_qua_path = os.path.join(dir_tam, "_ai-tach-tam-ketqua.f32")
    chia_path = os.path.join(dir_tam, "_ai-tach-tam-chia.f32")
    try:
        mix_mm = np.memmap(nguon_f32, dtype="<f4", mode="r",
                           shape=(n, 2))
        mix = mix_mm.T  # (2, N) strided view
        # 1. Peak toan file (doc theo khoi) -> he so chuan hoa.
        peak = 0.0
        khoi = 4 * 1024 * 1024
        for s in range(0, n, khoi):
            blk = np.asarray(mix[:, s:min(n, s + khoi)],
                             dtype=np.float64)
            if blk.size:
                peak = max(peak, float(np.abs(blk).max()))
        if peak > 0.9:
            scale = 0.9 / peak
        elif 0.0 < peak < 0.1:
            scale = 0.1 / peak
        else:
            scale = 1.0
        # 2. Memmap ket qua + chia (mixture = [zeros(trim), mix,
        #    zeros(pad)]).
        pad = eng.gen_size + eng.trim - (n % eng.gen_size)
        total_len = eng.trim + n + pad
        ket_qua = np.memmap(ket_qua_path, dtype="<f4", mode="w+",
                            shape=(2, total_len))
        chia = np.memmap(chia_path, dtype="<f4", mode="w+",
                         shape=(total_len,))
        total_chunks = (total_len + eng.step - 1) // eng.step
        done = 0
        for i in range(0, total_len, eng.step):
            if dung is not None and dung.is_set():
                return False, "đã hủy"
            start = i
            end = min(i + eng.chunk_size, total_len)
            actual = end - start
            chunk = np.zeros((2, eng.chunk_size), dtype=np.float64)
            a = start - eng.trim
            b = end - eng.trim
            lo = max(a, 0)
            hi = min(b, n)
            if hi > lo:
                chunk[:, lo - a:hi - a] = (
                    np.asarray(mix[:, lo:hi], dtype=np.float64) * scale)
            tar = eng._chay_model_1_chunk(chunk, model_path)
            tar = tar[None, :, :]
            window = np.hanning(actual)
            window = np.tile(window[None, None, :], (1, 2, 1))
            tar[..., :actual] *= window
            ket_qua[:, start:end] += tar[0, :, :actual].astype(np.float32)
            chia[start:end] += window[0, 0, :].astype(np.float32)
            done += 1
            if tien_trinh_cb is not None:
                try:
                    tien_trinh_cb(100.0 * done / max(1, total_chunks))
                except Exception:
                    pass
        # 3. Ghi instrumental ra dich_f32 theo khoi (+ vocal ra
        #    dich_giong_f32 neu co — v7.23: giong goc = vocal da
        #    bu compensate/scale, cung don vi voi instrumental).
        #    inst = mix - (ket_qua/chia) * (compensate/scale).
        f_giong = None
        try:
            if dich_giong_f32:
                f_giong = open(dich_giong_f32, "wb")
            with open(dich_f32, "wb") as f:
                for s in range(eng.trim, eng.trim + n, khoi):
                    e = min(eng.trim + n, s + khoi)
                    voc = (np.asarray(ket_qua[:, s:e], dtype=np.float64)
                           / np.maximum(np.asarray(chia[s:e],
                                                  dtype=np.float64), 1e-10))
                    voc = voc * (eng.compensate / scale)
                    inst = (np.asarray(mix[:, s - eng.trim:e - eng.trim],
                                       dtype=np.float64)
                            - voc)
                    f.write(np.ascontiguousarray(
                        inst.T).astype("<f4").tobytes())
                    if f_giong is not None:
                        f_giong.write(np.ascontiguousarray(
                            voc.T).astype("<f4").tobytes())
        finally:
            if f_giong is not None:
                try:
                    f_giong.close()
                except Exception:
                    pass
        return True, ""
    except ImportError as e:
        return False, ("chưa có thư viện onnxruntime trong tool "
                       "(cần cập nhật bản mới): %s" % _tom_tat_loi(e))
    except Exception as e:
        return False, _tom_tat_loi(e)
    finally:
        try:
            del ket_qua, chia, mix_mm
        except Exception:
            pass
        gc.collect()
        for p in (ket_qua_path, chia_path):
            try:
                os.remove(p)
            except Exception:
                pass


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
            capture_output=True, text=True, timeout=30,
            **chay_ngam_kwargs())
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
            capture_output=True, timeout=60, **chay_ngam_kwargs())
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


def _chay_ffmpeg_co_tien_trinh(cmd, timeout_giay, tong_giay,
                               tien_trinh_cb=None, dung=None,
                               log_cb=None, nhan="ffmpeg"):
    """(v7.20) Chay ffmpeg nhu _chay_ffmpeg_co_gioi_han nhung bao %
    tien trinh qua tien_trinh_cb: chen '-progress pipe:1 -nostats'
    truoc file dau ra (phan tu cuoi cua cmd) roi parse out_time_ms
    tren stdout so voi tong_giay (giay, do bang ffprobe truoc). Gọi
    tien_trinh_cb(float 0..99) khi % thay doi; goi tien_trinh_cb(None)
    1 lan luc bat dau neu tong_giay khong biet (<=0/None) de caller
    chuyen sang che do khong xac dinh thay vi hien % sai. Het gio thi
    kill va raise TimeoutError; bam Huy thi kill va tra (-1, "đã hủy").
    Tra ve (returncode, stderr_text). Chi dung cho cac lenh ma file
    dau ra la phan tu cuoi (lenh_* cua tab Xu ly am thanh)."""
    cmd = list(cmd)
    cmd[-1:-1] = ["-progress", "pipe:1", "-nostats"]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", bufsize=1,
        **chay_ngam_kwargs())
    hang = queue.Queue()
    out_ms_re = re.compile(r"out_time_ms=(\d+)")

    def _doc_stdout():
        try:
            for line in proc.stdout:
                hang.put(("out", line))
        except Exception:
            pass
        finally:
            hang.put(("het_stdout", None))

    def _doc_stderr():
        try:
            hang.put(("err", proc.stderr.read() or ""))
        except Exception:
            hang.put(("err", ""))

    threading.Thread(target=_doc_stdout, daemon=True).start()
    threading.Thread(target=_doc_stderr, daemon=True).start()
    if tien_trinh_cb is not None and not (tong_giay and tong_giay > 0):
        try:
            tien_trinh_cb(None)
        except Exception:
            pass
    bat_dau = time.monotonic()
    da_log = 0
    err_text = ""
    het_stdout = False
    da_gui = -1  # % da gui cuoi cung (tranh goi cb lap lai)

    def _xu_ly_dong_tien_trinh(dong):
        nonlocal da_gui
        m = out_ms_re.search(dong or "")
        if not m or not tong_giay or not tien_trinh_cb:
            return
        try:
            pct = int(int(m.group(1)) / (tong_giay * 1000.0) * 100)
        except Exception:
            return
        pct = max(0, min(99, pct))
        if pct != da_gui:
            da_gui = pct
            try:
                tien_trinh_cb(float(pct))
            except Exception:
                pass

    while True:
        try:
            loai, nd = hang.get(timeout=0.2)
        except queue.Empty:
            loai, nd = None, None
        if loai == "out":
            _xu_ly_dong_tien_trinh(nd)
        elif loai == "err":
            err_text = nd or ""
        elif loai == "het_stdout":
            het_stdout = True
        if dung is not None and dung.is_set():
            try:
                proc.kill()
            except Exception:
                pass
            try:
                proc.wait(timeout=5)
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
                proc.wait(timeout=5)
            except Exception:
                pass
            raise TimeoutError("%s chạy quá %ds"
                               % (nhan, int(timeout_giay)))
        if log_cb and da_cho - da_log >= 60:
            da_log = da_cho
            log_cb("  (%s đang chạy... đã chờ %ds)"
                   % (nhan, int(da_cho)))
        if proc.poll() is not None and het_stdout:
            # Xuc sach cac dong tien trinh con sot trong hang doi.
            try:
                while True:
                    loai, nd = hang.get_nowait()
                    if loai == "out":
                        _xu_ly_dong_tien_trinh(nd)
                    elif loai == "err":
                        err_text = nd or ""
            except queue.Empty:
                pass
            break
    # stderr co the ve cham hon stdout 1 chut sau khi tien trinh ket thuc.
    if not err_text:
        try:
            loai, nd = hang.get(timeout=2)
            if loai == "err":
                err_text = nd or ""
        except queue.Empty:
            pass
    try:
        proc.wait(timeout=5)
    except Exception:
        pass
    return proc.returncode, err_text


def _gop_mp3_concat(danh_sach_doan, dich, ffmpeg, log_cb=None, dung=None,
                    timeout_giay=None, log_loi_dir=None,
                    do_dai_mong_doi_ms=None):
    """(v7.7) Gop cac file MP3 thanh 1 file bang ffmpeg concat demuxer.
    danh_sach_doan: list (duong_dan, outpoint_giay_hoac_None) —
    outpoint de cat file khi audio dai hon slot SRT cua no; None thi
    lay het file. (v7.12) LUON re-encode ve MP3 chuan 44100 Hz /
    stereo / 192k / libmp3lame, KHONG dung -c copy nua: file cau
    Edge TTS goc la 24000 Hz mono nen -c copy cho ra MP3 24k mono,
    ffmpeg cua phan mem dung Concat khong xu ly duoc khi chuyen
    sang M4A/AAC ("filter output failed ... Invalid argument").
    Re-encode cung xu ly luon truong hop cac file cau khac thong so
    nhau (vd cau giong may local) ma -c copy se loi. Xong kiem tra
    do dai file ra bang ffprobe neu co do_dai_mong_doi_ms. Loi day
    du ghi vao ffmpeg-loi.log trong log_loi_dir. Tra ve (True, "")
    hoac (False, loi_ngan).
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
    # (v7.12) LUON re-encode ve MP3 chuan 44100 Hz / stereo / 192k /
    # libmp3lame (xem docstring o tren) — khong dung -c copy nua.
    cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0",
           "-i", txt_path, "-ar", str(MP3_CHUAN_AR),
           "-ac", str(MP3_CHUAN_AC),
           "-c:a", "libmp3lame", "-b:a", MP3_CHUAN_BITRATE, dich]
    try:
        rc, err = _chay_ffmpeg_co_gioi_han(
            cmd, timeout_giay, dung=dung, log_cb=log_cb,
            nhan="gộp MP3 (re-encode 44.1k stereo 192k)")
    except TimeoutError as e:
        if log_loi_dir:
            _ghi_log_loi_ffmpeg(
                log_loi_dir, "gop MP3 timeout: %s" % e)
        return False, "gộp MP3 hết thời gian chờ"
    if rc == -1:
        return False, "đã hủy khi đang gộp MP3"
    if rc == 0 and os.path.isfile(dich) and os.path.getsize(dich) > 0:
        if do_dai_mong_doi_ms:
            do_dai = _do_dai_mp3_ms(dich, ffmpeg)
            if (do_dai is not None
                    and abs(do_dai - do_dai_mong_doi_ms)
                    > max(2000, do_dai_mong_doi_ms // 50)):
                if log_cb:
                    log_cb("  (gộp MP3: file ra dài %.1fs, lệch "
                           "%.1fs so với mong đợi %.1fs)"
                           % (do_dai / 1000.0,
                              abs(do_dai - do_dai_mong_doi_ms)
                              / 1000.0,
                              do_dai_mong_doi_ms / 1000.0))
                return False, ("file gộp dài %.1fs, lệch nhiều so "
                               "với %.1fs mong đợi"
                               % (do_dai / 1000.0,
                                  do_dai_mong_doi_ms / 1000.0))
        return True, ""
    if log_cb:
        log_cb("  (gộp MP3 re-encode lỗi, mã %s)" % rc)
    if log_loi_dir:
        _ghi_log_loi_ffmpeg(
            log_loi_dir, "gop MP3 that bai (re-encode):\n%s" % err)
    return False, "ffmpeg gộp MP3 lỗi (xem chi tiết trong ffmpeg-loi.log)"


def _lap_danh_sach_concat_cat(cac_muc, file_im_lang, tong_ms):
    """(v7.7, tach tu GopDan.hoan_tat de dung chung cho ca che do cat
    va che do de) Xay danh sach concat (file, outpoint) theo moc gio
    SRT: cau tran slot thi cat bang outpoint; khoang trong giua cac
    cau thi chen file im lang. Tra ve (danh_sach_doan, con_troi_ms).
    `cac_muc`: list {cau, file, do_dai_ms} (se duoc sap theo
    bat_dau_ms)."""
    cac_cau = sorted(cac_muc, key=lambda d: d["cau"]["bat_dau_ms"])
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
    if tong_ms > con_troi and file_im_lang:
        _them_doan_im_lang(danh_sach_doan,
                           tong_ms - con_troi, file_im_lang)
        con_troi = tong_ms
    return danh_sach_doan, con_troi


def _gop_mp3_de(cac_muc, dich, ffmpeg, log_cb=None, dung=None,
                timeout_giay=None, log_loi_dir=None, tong_ms=0,
                thu_muc=None):
    """(v7.8) Gop file long tieng che do 'de': phan tran cua cau N
    KHONG cat ma phat NHO (AM_LUONG_TRAN_DE) duoi dau cau N+1 — cau
    sau van bat dau dung moc gio voi am luong du. Lam 3 buoc bang
    ffmpeg (khong dung pydub):
      1. Gop 'cat' nhu cu ra file tam (file nen: cau sau bat dau
         dung moc gio, phan tran bi cat).
      2. Cat phan tran cua tung cau tran thanh clip nho (volume
         AM_LUONG_TRAN_DE), ghep cac clip + khoang lang thanh 1
         'track tran' dai dung tong_ms bang concat demuxer.
      3. Tron file nen + track tran bang amix (normalize=0) ra file
         dich.
    Phan tran chi de duoi cau sau lien ke: neu tran dai toi moc bat
    dau cau N+2 thi cat phan con lai o do (log ro). Tra ve
    (trang_thai, do_dai_ms, loi, so_cau_de): trang_thai 'ok' /
    'loi' / 'huy'. 'loi' thi ben goi tu quay ve che do cat (khong
    crash, khong mat file); 'huy' thi dung han, khong gop bu."""
    if not ffmpeg:
        return "loi", 0, "không tìm thấy ffmpeg", 0
    if not cac_muc:
        return "loi", 0, "không có câu nào để gộp", 0
    if not tong_ms or tong_ms <= 0:
        return "loi", 0, "không rõ tổng thời lượng phim", 0
    thu_muc = thu_muc or os.path.dirname(dich) or "."
    cac_cau = sorted(cac_muc, key=lambda d: d["cau"]["bat_dau_ms"])
    sr, ch = 24000, 1
    thong_so = _ffprobe_thong_so_audio(cac_cau[0]["file"], ffmpeg)
    if thong_so:
        sr, ch = thong_so
    file_im_lang = _tao_file_im_lang_1s(ffmpeg, thu_muc, sr, ch)
    if file_im_lang is None:
        return "loi", 0, "không tạo được file im lặng", 0
    base_tam = dich + ".cat-tam.mp3"
    track_tam = dich + ".tran-tam.mp3"
    cac_clip = []  # (vi_tri_bat_dau_ms, duong_dan_clip, do_dai_ms)
    so_cau_de = 0
    try:
        # Buoc 1: file nen (cat nhu cu).
        danh_sach_cat, _con_troi = _lap_danh_sach_concat_cat(
            cac_cau, file_im_lang, tong_ms)
        ok, loi = _gop_mp3_concat(
            danh_sach_cat, base_tam, ffmpeg, log_cb=log_cb, dung=dung,
            timeout_giay=timeout_giay, log_loi_dir=log_loi_dir,
            do_dai_mong_doi_ms=tong_ms)
        if not ok:
            if dung is not None and dung.is_set():
                return "huy", 0, "đã hủy", 0
            return "loi", 0, "gộp file nền lỗi: %s" % loi, 0
        # Buoc 2: cat phan tran thanh clip nho.
        for idx, muc in enumerate(cac_cau):
            cau = muc["cau"]
            bat_dau = cau["bat_dau_ms"]
            if idx + 1 < len(cac_cau):
                ket_thuc_slot = cac_cau[idx + 1]["cau"]["bat_dau_ms"]
                chi_so_sau = cac_cau[idx + 1]["cau"]["chi_so"]
            else:
                ket_thuc_slot = cau["ket_thuc_ms"]
                chi_so_sau = None
            slot_ms = max(0, ket_thuc_slot - bat_dau)
            do_dai = muc["do_dai_ms"]
            if slot_ms <= 0 or chi_so_sau is None:
                continue  # cau cuoi: khong co cau sau de de
            if do_dai <= slot_ms + DUNG_SAI_TRAN_SLOT_MS:
                continue
            # Gioi han de: chi duoi cau sau lien ke, toi moc cau N+2.
            if idx + 2 < len(cac_cau):
                gioi_han_ms = cac_cau[idx + 2]["cau"]["bat_dau_ms"]
            else:
                gioi_han_ms = tong_ms
            cuoi_tran = bat_dau + do_dai
            if cuoi_tran > gioi_han_ms:
                if log_cb:
                    log_cb("  Câu %d tràn dài, đã cắt phần vượt quá câu "
                           "%d." % (cau["chi_so"], chi_so_sau))
                cuoi_tran = gioi_han_ms
            bat_dau_de = bat_dau + slot_ms
            do_dai_de = cuoi_tran - bat_dau_de
            if do_dai_de <= 50:
                continue
            clip = os.path.join(
                thu_muc, "_de-tran-%03d.mp3" % cau["chi_so"])
            cmd = [ffmpeg, "-y", "-i", muc["file"],
                   "-ss", "%.3f" % (slot_ms / 1000.0),
                   "-t", "%.3f" % (do_dai_de / 1000.0),
                   "-af", "volume=%.2f" % AM_LUONG_TRAN_DE,
                   "-ar", str(sr), "-ac", str(ch),
                   "-c:a", "libmp3lame", "-b:a", "128k", clip]
            try:
                rc, _err = _chay_ffmpeg_co_gioi_han(
                    cmd, 120, dung=dung, log_cb=log_cb,
                    nhan="cắt phần tràn câu %d" % cau["chi_so"])
            except TimeoutError:
                if log_cb:
                    log_cb("  Câu %d: cắt phần tràn hết thời gian chờ — "
                           "bỏ qua phần tràn này." % cau["chi_so"])
                continue
            if rc == -1:
                return "huy", 0, "đã hủy", 0
            if rc != 0 or not (os.path.isfile(clip)
                               and os.path.getsize(clip) > 0):
                if log_cb:
                    log_cb("  Câu %d: cắt phần tràn lỗi — bỏ qua phần "
                           "tràn này." % cau["chi_so"])
                continue
            cac_clip.append((bat_dau_de, clip, do_dai_de))
            so_cau_de += 1
            if log_cb:
                log_cb("  Câu %d: tràn %.1fs, đè nhỏ dưới câu %d."
                       % (cau["chi_so"], do_dai_de / 1000.0, chi_so_sau))
        if not cac_clip:
            # Khong cau nao de duoc: file nen chinh la ket qua.
            try:
                os.replace(_duong_dan_dai_win(base_tam),
                           _duong_dan_dai_win(dich))
            except OSError as e:
                return "loi", 0, "không chuyển được file nền: %s" % e, 0
            do_dai_ra = _do_dai_mp3_ms(dich, ffmpeg)
            return "ok", (do_dai_ra if do_dai_ra is not None
                          else tong_ms), "", so_cau_de
        # Ghep cac clip + khoang lang thanh track tran dai dung tong_ms.
        danh_sach_track = []
        con_troi = 0
        for vi_tri, clip, do_dai_clip in sorted(cac_clip):
            if vi_tri > con_troi:
                _them_doan_im_lang(danh_sach_track,
                                   vi_tri - con_troi, file_im_lang)
                con_troi = vi_tri
            danh_sach_track.append((clip, None))
            con_troi = max(con_troi, vi_tri + do_dai_clip)
        if tong_ms > con_troi:
            _them_doan_im_lang(danh_sach_track,
                               tong_ms - con_troi, file_im_lang)
        ok, loi = _gop_mp3_concat(
            danh_sach_track, track_tam, ffmpeg, log_cb=log_cb,
            dung=dung, timeout_giay=timeout_giay,
            log_loi_dir=log_loi_dir, do_dai_mong_doi_ms=tong_ms)
        if not ok:
            if dung is not None and dung.is_set():
                return "huy", 0, "đã hủy", 0
            return "loi", 0, "gộp track tràn lỗi: %s" % loi, 0
        # Buoc 3: tron file nen + track tran.
        # (v7.12) Ep ve MP3 chuan 44100 Hz / stereo / 192k.
        cmd_tron = [ffmpeg, "-y", "-i", base_tam, "-i", track_tam,
                    "-filter_complex",
                    "[0:a][1:a]amix=inputs=2:normalize=0:duration=first",
                    "-ar", str(MP3_CHUAN_AR),
                    "-ac", str(MP3_CHUAN_AC),
                    "-c:a", "libmp3lame", "-b:a", MP3_CHUAN_BITRATE,
                    dich]
        try:
            rc, _err = _chay_ffmpeg_co_gioi_han(
                cmd_tron, timeout_giay, dung=dung, log_cb=log_cb,
                nhan="trộn đè phần tràn")
        except TimeoutError:
            return "loi", 0, "trộn đè hết thời gian chờ", 0
        if rc == -1:
            return "huy", 0, "đã hủy", 0
        if rc != 0 or not (os.path.isfile(dich)
                           and os.path.getsize(dich) > 0):
            return "loi", 0, "ffmpeg trộn đè lỗi (mã %s)" % rc, 0
        do_dai_ra = _do_dai_mp3_ms(dich, ffmpeg)
        if (do_dai_ra is not None
                and abs(do_dai_ra - tong_ms)
                > max(2000, tong_ms // 50)):
            return "loi", 0, ("file trộn đè dài %.1fs, lệch nhiều so "
                              "với %.1fs mong đợi"
                              % (do_dai_ra / 1000.0, tong_ms / 1000.0)), 0
        return "ok", (do_dai_ra if do_dai_ra is not None
                      else tong_ms), "", so_cau_de
    finally:
        _xoa_file_quiet(base_tam)
        _xoa_file_quiet(track_tam)
        for _vi_tri, clip, _do_dai in cac_clip:
            _xoa_file_quiet(clip)


# ======================================================================
# (v7.17) GOP AM THANH: tron file voice HoaiMy + file nhac nen (da
# chuan bi san trong CapCut) thanh 1 file am thanh, KHONG kem video.
# Quy trinh that cua CYAN: tu tach nen + cho nho giong goc trong
# CapCut roi xuat file nen; file voice la MP3 HoaiMy do tab Doc phu
# de xuat ra; tool chi tron thang 2 file do (amix, KHONG sidechain
# ducking — nen da chinh san roi). Dau ra mac dinh MP3 128k / 44.1k /
# stereo / CBR — KHAC han chuan voice 192k cua v7.12, nen co hang
# rieng GOP_AM_THANH_BITRATE, TUYET DOI khong dung MP3_CHUAN_BITRATE
# o day. Khong co goi y am luong nao (CYAN bo de xuat 100%/20-30%).
# ======================================================================
GOP_AM_THANH_AR = 44100
GOP_AM_THANH_AC = 2
GOP_AM_THANH_BITRATE = "128k"  # RIENG cho gop am thanh, KHONG phai 192k
GOP_AM_THANH_DINH_DANG = ("mp3", "wav", "m4a")
# (v7.17) Bitrate MP3 cho xuat gop am thanh: 96k/128k/192k, mac dinh
# 128k — nhe, du nghe (CYAN chap nhan file nhe, khong day chat luong
# cao hon de doi dung luong). Hang RIENG, khong phai 192k chuan voice.
GOP_AM_THANH_BITRATE_LUA_CHON = ("96k", "128k", "192k")


def _hau_to_pan_stereo(ffmpeg, duong_dan):
    """(v7.17) Tra ',pan=stereo|c0=c0|c1=c0' neu file la MONO (de
    nhan doi kenh GIU NGUYEN muc am luong khi tron), '' neu stereo
    hoac do khong duoc so kenh. Ly do: ffmpeg tu chuyen mono->stereo
    (trong amix hay o -ac 2) theo kieu giu nang luong nen mat ~3 dB
    (do that: mono -27.5 dB -> -30.5 dB chi qua -ac 2)."""
    try:
        thong_so = _ffprobe_thong_so_audio(duong_dan, ffmpeg)
        if thong_so and thong_so[1] == 1:
            return ",pan=stereo|c0=c0|c1=c0"
    except Exception:
        pass
    return ""


def lenh_gop_am_thanh(ffmpeg, voice, nen, out_path, am_luong_voice=1.0,
                      am_luong_nen=1.0, dinh_dang="mp3", bitrate_mp3="128k",
                      giong_goc=None, am_luong_giong_goc=0.0):
    """(v7.17) Lenh ffmpeg tron 2 file am thanh (voice + nen) thanh 1
    file, KHONG kem video. Dung amix duration=longest (lay theo file
    dai hon, file ngan hon dem lang) + normalize=0 (giu nguyen muc
    am luong goc cua 2 file, khong tu chia doi nhu mac dinh cua
    amix). File mono duoc nhan doi kenh bang pan truoc khi tron de
    khong mat ~3 dB nhu cach ffmpeg tu chuyen. Dau ra ep dung chuan
    gop: 44100 Hz, stereo; MP3: libmp3lame 128k CBR; WAV: PCM 16-bit;
    M4A: AAC 128k. Tra ve list lenh (chua chay). am_luong_* la he so
    (1.0 = 100%).
    (v7.23) giong_goc (duong dan file giong goc tieng Trung, tuy
    chon): neu co file thi tron 3 track (voice + nen + giong goc)
    bang amix inputs=3; khong co thi tron 2 track nhu cu."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        raise ValueError("Định dạng đầu ra không hỗ trợ: %s "
                         "(chỉ mp3/wav/m4a)" % dinh_dang)
    co_giong_goc = bool(giong_goc and os.path.isfile(giong_goc))
    if co_giong_goc:
        fc = ("[0:a]volume=%.3f%s[voice];[1:a]volume=%.3f%s[nen];"
              "[2:a]volume=%.3f%s[giong];"
              "[voice][nen][giong]amix=inputs=3:duration=longest:"
              "normalize=0[aout]"
              % (float(am_luong_voice),
                 _hau_to_pan_stereo(ffmpeg, voice),
                 float(am_luong_nen),
                 _hau_to_pan_stereo(ffmpeg, nen),
                 float(am_luong_giong_goc),
                 _hau_to_pan_stereo(ffmpeg, giong_goc)))
        cmd = [ffmpeg, "-y", "-i", voice, "-i", nen, "-i", giong_goc,
               "-vn", "-filter_complex", fc, "-map", "[aout]",
               "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC)]
    else:
        fc = ("[0:a]volume=%.3f%s[voice];[1:a]volume=%.3f%s[nen];"
              "[voice][nen]amix=inputs=2:duration=longest:normalize=0[aout]"
              % (float(am_luong_voice),
                 _hau_to_pan_stereo(ffmpeg, voice),
                 float(am_luong_nen),
                 _hau_to_pan_stereo(ffmpeg, nen)))
        cmd = [ffmpeg, "-y", "-i", voice, "-i", nen, "-vn",
               "-filter_complex", fc, "-map", "[aout]",
               "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC)]
    cmd += _tham_so_codec_dau_ra_gop(dinh_dang, bitrate_mp3)
    cmd.append(out_path)
    return cmd


def _tham_so_codec_dau_ra_gop(dinh_dang, bitrate_mp3="128k"):
    """(v7.17) Tham so codec theo dinh dang xuat gop am thanh:
    MP3 -> libmp3lame <bitrate> CBR (96k/128k/192k, mac dinh 128k
    — nhe, du nghe); WAV -> PCM 16-bit (nang, khong nen); M4A ->
    AAC 128k. Dung chung cho ca gop voice+nen, luu nen, tach nen.
    Bitrate la hang RIENG GOP_AM_THANH_BITRATE, khong phai 192k
    cua chuan voice."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang == "wav":
        return ["-c:a", "pcm_s16le"]
    if dinh_dang == "m4a":
        return ["-c:a", "aac", "-b:a", GOP_AM_THANH_BITRATE]
    br = str(bitrate_mp3 or "128k").lower()
    if br not in GOP_AM_THANH_BITRATE_LUA_CHON:
        br = GOP_AM_THANH_BITRATE
    return ["-c:a", "libmp3lame", "-b:a", br]


def lenh_tach_giong_giua(ffmpeg, nguon, dich, bitrate_mp3="128k"):
    """(v7.17) Lenh ffmpeg tach giong giua (khu kenh giua) khoi file
    stereo: tru 2 kenh cho nhau — giong nam giua 2 kenh (hat deu 2
    ben) se bi triet tieu — roi bu am luong x2 vi tru kenh lam nho
    tieng di. Ra THANG MP3 (libmp3lame, bitrate da chon — mac dinh
    128k) 44.1k stereo, TRUNG chuan voi file voice HoaiMy de gop sau
    khong phai convert them pass nao. -map 0:a: chi lay luong tieng,
    bo track hinh neu file mp4 lo co kem hinh. LUu Y THANH THAT: day
    la tach bang ffmpeg, KHONG phai AI — giong lech trai/phai, hoac
    nhac co nhieu thanh phan o giua, se khong sach bang tach AI cua
    CapCut; chi la them 1 lua chon."""
    br = str(bitrate_mp3 or "128k").lower()
    if br not in GOP_AM_THANH_BITRATE_LUA_CHON:
        br = GOP_AM_THANH_BITRATE
    return [ffmpeg, "-y", "-i", nguon, "-map", "0:a",
            "-af", "pan=stereo|c0=c0-c1|c1=c1-c0,volume=2.0",
            "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC),
            "-c:a", "libmp3lame", "-b:a", br, dich]


def lenh_luu_nen(ffmpeg, nguon, dich, am_luong=1.0, dinh_dang="mp3",
                 bitrate_mp3="128k"):
    """(v7.17) Lenh ffmpeg luu file nen da tach/chinh: ap am luong
    (he so, 1.0 = 100%) roi xuat dung chuan gop (44.1k/stereo; MP3
    <bitrate> CBR / WAV PCM / M4A AAC 128k). -map 0:a: chi lay luong
    tieng, bo track hinh neu file mp4 lo co kem hinh."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        raise ValueError("Định dạng đầu ra không hỗ trợ: %s "
                         "(chỉ mp3/wav/m4a)" % dinh_dang)
    cmd = [ffmpeg, "-y", "-i", nguon, "-map", "0:a",
           "-af", "volume=%.3f%s" % (float(am_luong),
                                     _hau_to_pan_stereo(ffmpeg, nguon)),
           "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC)]
    cmd += _tham_so_codec_dau_ra_gop(dinh_dang, bitrate_mp3)
    cmd.append(dich)
    return cmd


def lenh_nghe_thu_gop(ffmpeg, voice, nen, dich_tam, bat_dau_giay=0.0,
                      do_dai_giay=30, am_luong_voice=1.0, am_luong_nen=1.0,
                      giong_goc=None, am_luong_giong_goc=0.0):
    """(v7.17) Lenh ffmpeg tron THU 1 doan (mac dinh 30 giay tu moc
    bat dau) cua voice + nen ra file tam WAV de nghe thu — khong tron
    ca file dai chi de nghe thu. Cung cach tron nhu gop that (amix
    duration=longest, normalize=0). (v7.23) Neu co giong_goc thi
    tron thu ca 3 track nhu gop that."""
    co_giong_goc = bool(giong_goc and os.path.isfile(giong_goc))
    if co_giong_goc:
        fc = ("[0:a]atrim=start=%.3f:duration=%.3f,asetpts=PTS-STARTPTS,"
              "volume=%.3f%s[v];[1:a]atrim=start=%.3f:duration=%.3f,"
              "asetpts=PTS-STARTPTS,volume=%.3f%s[n];"
              "[2:a]atrim=start=%.3f:duration=%.3f,"
              "asetpts=PTS-STARTPTS,volume=%.3f%s[g];"
              "[v][n][g]amix=inputs=3:duration=longest:normalize=0[aout]"
              % (float(bat_dau_giay), float(do_dai_giay),
                 float(am_luong_voice),
                 _hau_to_pan_stereo(ffmpeg, voice),
                 float(bat_dau_giay), float(do_dai_giay),
                 float(am_luong_nen), _hau_to_pan_stereo(ffmpeg, nen),
                 float(bat_dau_giay), float(do_dai_giay),
                 float(am_luong_giong_goc),
                 _hau_to_pan_stereo(ffmpeg, giong_goc)))
        return [ffmpeg, "-y", "-i", voice, "-i", nen, "-i", giong_goc,
                "-vn", "-filter_complex", fc, "-map", "[aout]",
                "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC),
                "-c:a", "pcm_s16le", dich_tam]
    fc = ("[0:a]atrim=start=%.3f:duration=%.3f,asetpts=PTS-STARTPTS,"
          "volume=%.3f%s[v];[1:a]atrim=start=%.3f:duration=%.3f,"
          "asetpts=PTS-STARTPTS,volume=%.3f%s[n];"
          "[v][n]amix=inputs=2:duration=longest:normalize=0[aout]"
          % (float(bat_dau_giay), float(do_dai_giay),
             float(am_luong_voice), _hau_to_pan_stereo(ffmpeg, voice),
             float(bat_dau_giay), float(do_dai_giay),
             float(am_luong_nen), _hau_to_pan_stereo(ffmpeg, nen)))
    return [ffmpeg, "-y", "-i", voice, "-i", nen, "-vn",
            "-filter_complex", fc, "-map", "[aout]",
            "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC),
            "-c:a", "pcm_s16le", dich_tam]


def lenh_nghe_thu_nen(ffmpeg, nen, dich_tam, bat_dau_giay=0.0,
                      do_dai_giay=30, am_luong_nen=1.0):
    """(v7.17) Lenh ffmpeg cat THU 1 doan (mac dinh 30 giay) cua file
    nen ra file tam WAV de nghe thu khi chua chon file voice."""
    return [ffmpeg, "-y", "-ss", "%.3f" % float(bat_dau_giay),
            "-i", nen, "-map", "0:a", "-t", "%.3f" % float(do_dai_giay),
            "-af", "volume=%.3f%s" % (float(am_luong_nen),
                                      _hau_to_pan_stereo(ffmpeg, nen)),
            "-ar", str(GOP_AM_THANH_AR), "-ac", str(GOP_AM_THANH_AC),
            "-c:a", "pcm_s16le", dich_tam]


def ten_file_nen_lam_viec(nguon):
    """(v7.17) Ten file nen tam sau khi tach: cung thu muc voi file
    goc, <ten goc>_nen-tach.mp3 (MP3 44.1k stereo, trung chuan voice
    HoaiMy). File lam viec nen ghi de moi lan tach lai (khong phai
    file goc)."""
    thu_muc = os.path.dirname(nguon) or "."
    ten_goc = os.path.splitext(os.path.basename(nguon))[0]
    return os.path.join(thu_muc, "%s_nen-tach.mp3" % ten_goc)


def ten_file_giong_goc_lam_viec(nguon):
    """(v7.23) Ten file giong goc sau khi tach AI: cung thu muc voi
    file goc, <ten goc>_giong-goc.mp3 (MP3 44.1k stereo, cung chuan
    voi file nen). Giong goc la vocal model tach ra — KHONG bi xoa
    nua, de tron lai voi am luong tuy chon."""
    thu_muc = os.path.dirname(nguon) or "."
    ten_goc = os.path.splitext(os.path.basename(nguon))[0]
    return os.path.join(thu_muc, "%s_giong-goc.mp3" % ten_goc)


def tim_file_giong_goc_tach(thu_muc):
    """(v7.23) Tim file giong goc da tach <ten>_giong-goc.mp3 trong
    thu muc phim (file tab Xu ly am thanh / luong tach truoc khi
    long tao ra). Tra ve duong dan dau tien tim thay (sap xep theo
    ten) hoac None."""
    if not thu_muc or not os.path.isdir(thu_muc):
        return None
    try:
        for ten in sorted(os.listdir(thu_muc)):
            if ten.lower().endswith("_giong-goc.mp3"):
                duong = os.path.join(thu_muc, ten)
                if os.path.isfile(duong):
                    return duong
    except OSError:
        return None
    return None


def ten_file_nen_da_luu(nguon, dinh_dang="mp3"):
    """(v7.17) Ten file nen da luu: cung thu muc voi file goc,
    <ten goc>_nen.<dinh_dang>; trung ten thi them (1), (2)..."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        dinh_dang = "mp3"
    thu_muc = os.path.dirname(nguon) or "."
    ten_goc = os.path.splitext(os.path.basename(nguon))[0]
    ten = "%s_nen.%s" % (ten_goc, dinh_dang)
    n = 1
    while os.path.exists(os.path.join(thu_muc, ten)):
        ten = "%s_nen(%d).%s" % (ten_goc, n, dinh_dang)
        n += 1
    return os.path.join(thu_muc, ten)


def tim_file_audio_du_an(thu_muc):
    """(v7.17) Tim file audio goc trong thu muc du an: uu tien file
    tieng rieng (*_tieng.mp4/_tieng.m4a), roi file am thanh (mp3/m4a/
    wav/flac/ogg), cuoi cung la file video (ffmpeg doc duoc tieng
    trong video). Tra ve duong dan hoac None."""
    if not thu_muc or not os.path.isdir(thu_muc):
        return None
    try:
        ds = sorted(os.listdir(thu_muc))
    except OSError:
        return None
    uu_tien = []
    am_thanh = []
    video = []
    for ten in ds:
        thap = ten.lower()
        duong = os.path.join(thu_muc, ten)
        if not os.path.isfile(duong):
            continue
        if "_tieng." in thap and thap.endswith((".mp4", ".m4a", ".mp3",
                                                ".wav")):
            uu_tien.append(duong)
        elif thap.endswith((".mp3", ".m4a", ".wav", ".flac", ".ogg",
                            ".aac", ".opus", ".wma")):
            am_thanh.append(duong)
        elif thap.endswith((".mp4", ".mkv", ".webm", ".mov")):
            video.append(duong)
    for nhom in (uu_tien, am_thanh, video):
        if nhom:
            return nhom[0]
    return None


def ten_file_gop_am_thanh(voice_path, dinh_dang="mp3"):
    """(v7.17) Ten file gop: cung thu muc voi file voice,
    <ten file voice>_gop.<dinh_dang>; trung ten thi them (1), (2)...
    Khong bao gio de len file goc."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        dinh_dang = "mp3"
    thu_muc = os.path.dirname(voice_path) or "."
    ten_goc = os.path.splitext(os.path.basename(voice_path))[0]
    ten = "%s_gop.%s" % (ten_goc, dinh_dang)
    n = 1
    while os.path.exists(os.path.join(thu_muc, ten)):
        ten = "%s_gop(%d).%s" % (ten_goc, n, dinh_dang)
        n += 1
    return os.path.join(thu_muc, ten)


def _kiem_tra_file_gop_am_thanh(duong_dan, ffmpeg, dinh_dang="mp3",
                                bitrate_mong=None):
    """(v7.17) Kiem tra file gop bang ffprobe: phai dung 44100 Hz,
    stereo, dung codec theo dinh dang (mp3/aac/pcm_s16le); MP3/M4A
    thi bitrate phai gan bitrate da chon (mac dinh 128k, cho sai le
    20k); thoi luong phai > 0. bitrate_mong: so bps (128000) hoac
    chuoi "128k"; None thi 128k cho mp3/m4a. Tra ve
    (True, "mp3, 44100 Hz, stereo, 128 kbps") hoac (False, ly do)."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    codec_mong = {"mp3": "mp3", "wav": "pcm_s16le",
                  "m4a": "aac"}.get(dinh_dang, "mp3")
    if bitrate_mong is None:
        br_mong = 128000
    elif isinstance(bitrate_mong, str):
        try:
            br_mong = int(bitrate_mong.lower().rstrip("k")) * 1000
        except Exception:
            br_mong = 128000
    else:
        br_mong = int(bitrate_mong)
    ffprobe = tim_ffprobe(ffmpeg) if ffmpeg else None
    if not ffprobe:
        return False, "không tìm thấy ffprobe để kiểm tra file ra"
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=codec_name,sample_rate,channels,"
             "bit_rate:format=duration", "-of", "json", duong_dan],
            capture_output=True, text=True, timeout=30,
            **chay_ngam_kwargs())
        if r.returncode != 0 or not r.stdout.strip():
            return False, "ffprobe không đọc được file ra"
        data = json.loads(r.stdout)
        streams = data.get("streams") or []
        if not streams:
            return False, "file ra không có luồng âm thanh"
        s = streams[0]
        codec = str(s.get("codec_name") or "")
        sr = int(s.get("sample_rate") or 0)
        ch = int(s.get("channels") or 0)
        if codec != codec_mong:
            return False, "codec ra là %s, mong đợi %s" % (codec,
                                                           codec_mong)
        if sr != GOP_AM_THANH_AR or ch != GOP_AM_THANH_AC:
            return False, ("file ra %d Hz / %d kênh, mong đợi "
                           "44100 Hz / stereo" % (sr, ch))
        try:
            do_dai = float((data.get("format") or {}).get("duration") or 0)
        except Exception:
            do_dai = 0
        if do_dai <= 0:
            return False, "file ra có thời lượng 0 (rỗng/lỗi)"
        br = 0
        if dinh_dang in ("mp3", "m4a"):
            try:
                br = int(s.get("bit_rate") or 0)
            except Exception:
                br = 0
            if br and abs(br - br_mong) > 20000:
                return False, ("bitrate ra %d kbps, mong đợi "
                               "~%d kbps" % (br // 1000,
                                            br_mong // 1000))
        return True, "%s, 44100 Hz, stereo%s" % (
            codec_mong,
            (", %d kbps" % (br // 1000) if dinh_dang in ("mp3", "m4a")
             else ", PCM 16-bit"))
    except Exception as e:
        return False, "lỗi khi kiểm tra file ra: %s" % e


def _giai_ma_thu_toan_bo(ffmpeg, duong_dan):
    """(v7.17) Giai ma thu TOAN BO file ve null: file phai phat duoc
    tu dau toi cuoi, khong loi giua chung, moi tinh la xong. Chi
    kiem tra exit code la CHUA DU (do that: file MP3 cat do chi con
    3000 byte van exit 0, nhung stderr co 'invalid new backstep').
    Tra (True, '') hoac (False, ly do)."""
    if not ffmpeg:
        return False, "không tìm thấy ffmpeg để giải mã thử"
    try:
        r = subprocess.run(
            [ffmpeg, "-v", "error", "-i", duong_dan, "-f", "null", "-"],
            capture_output=True, text=True, timeout=600,
            **chay_ngam_kwargs())
    except Exception as e:
        return False, "không giải mã thử được: %s" % e
    loi = (r.stderr or "").strip()
    if r.returncode != 0:
        return False, ("giải mã lỗi (ffmpeg exit %d)%s"
                       % (r.returncode,
                          (": " + loi[:200]) if loi else ""))
    if loi:
        return False, "giải mã có lỗi giữa chừng: %s" % loi[:200]
    return True, ""


def _kiem_tra_chat_luong_am_thanh(duong_dan, ffmpeg, dinh_dang="mp3",
                                  bitrate_mong=None):
    """(v7.17) Cua kiem tra chat luong CHO MOI file am thanh dau ra
    (nen MP3 sau tach, file nghe thu, file voice-sub sau gop):
    (1) ffprobe: dung dinh dang/codec/44100 Hz/stereo/bitrate da
    chon, thoi luong > 0; (2) giai ma thu TOAN BO file ve null.
    Chi ca 2 deu pass moi duoc bao thanh cong — KHONG bao thanh
    cong gia. Bai hoc v7.12: MP3 24k mono lam Concat loi, chi tin
    ffmpeg exit code la chua du."""
    ok, thong_tin = _kiem_tra_file_gop_am_thanh(
        duong_dan, ffmpeg, dinh_dang, bitrate_mong)
    if not ok:
        return False, thong_tin
    ok2, loi = _giai_ma_thu_toan_bo(ffmpeg, duong_dan)
    if not ok2:
        return False, "ffprobe đúng chuẩn nhưng %s" % loi
    return True, thong_tin


# ======================================================================
# (v7.18) NHAT KY LOI AM THANH RIENG BIET — chi ghi LOI tach nen /
# tron / nghe thu / luu nen (ca tab Xu ly am thanh lan tron tich hop
# trong tab Doc phu de), KHONG ghi loi long giong (TTS). Dung chung
# cho ca 2 tab: danh sach o cap module, o Text o tab Xu ly am thanh
# chi la 1 cach hien; nut Sao chep o ca 2 tab deu copy cung noi dung
# nay. Moi dong: [HH:MM:SS] [buoc] thong bao (file: ...) — loi ffmpeg
# thi kem dong loi cuoi cua stderr (cat ngan).
# ======================================================================
_LOI_AM_THANH = []
_LOI_AM_THANH_KHOA = threading.Lock()


def ghi_loi_am_thanh(buoc, thong_bao, file_lien_quan=None,
                     stderr_ffmpeg=None):
    """(v7.18) Ghi 1 dong loi am thanh vao nhat ky loi chung
    (thread-safe). Chi goi o duong loi cua tach nen / tron / nghe thu
    / luu nen — TUYET DOI khong goi o duong loi long giong (TTS).
    Tra ve dong vua ghi. Thong bao chi lay dong dau (cat ngan) de
    moi loi dung 1 dong — thong bao loi ffmpeg co the xuong dong."""
    thong_bao = str(thong_bao or "").strip().split("\n", 1)[0][:300]
    dong = "[%s] [%s] %s" % (time.strftime("%H:%M:%S"),
                             str(buoc or "?"), thong_bao)
    if file_lien_quan:
        dong += " (file: %s)" % file_lien_quan
    if stderr_ffmpeg:
        duoi = str(stderr_ffmpeg).strip().splitlines()
        duoi = duoi[-1] if duoi else ""
        if duoi:
            dong += " | ffmpeg: %s" % duoi[:300]
    with _LOI_AM_THANH_KHOA:
        _LOI_AM_THANH.append(dong)
    return dong


def lay_noi_dung_loi_am_thanh():
    """(v7.18) Toan bo nhat ky loi am thanh (chuoi, moi dong 1 loi)."""
    with _LOI_AM_THANH_KHOA:
        return "\n".join(_LOI_AM_THANH)


def xoa_loi_am_thanh():
    """(v7.18) Xoa sach nhat ky loi am thanh."""
    with _LOI_AM_THANH_KHOA:
        del _LOI_AM_THANH[:]


def tim_file_nen_tach(thu_muc):
    """(v7.18) Tim file nen da tach <ten>_nen-tach.mp3 trong thu muc
    phim (file tab Xu ly am thanh tao ra). Tra ve duong dan dau tien
    tim thay (sap xep theo ten) hoac None."""
    if not thu_muc or not os.path.isdir(thu_muc):
        return None
    try:
        for ten in sorted(os.listdir(thu_muc)):
            if ten.lower().endswith("_nen-tach.mp3"):
                duong = os.path.join(thu_muc, ten)
                if os.path.isfile(duong):
                    return duong
    except OSError:
        return None
    return None


def ten_file_voice_nen(voice_path, dinh_dang="mp3"):
    """(v7.18) Ten file voice + nhac nen: cung thu muc voi file voice,
    <ten file voice>_voice-nen.<dinh dang>; trung ten thi them (1),
    (2)... Khong bao gio de len file voice goc. (v7.23) dinh_dang
    theo lua chon xuat cuoi cua luong tach + long mot lan (mp3/wav/
    m4a); mac dinh mp3 nhu cu."""
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        dinh_dang = "mp3"
    thu_muc = os.path.dirname(voice_path) or "."
    ten_goc = os.path.splitext(os.path.basename(voice_path))[0]
    ten = "%s_voice-nen.%s" % (ten_goc, dinh_dang)
    n = 1
    while os.path.exists(os.path.join(thu_muc, ten)):
        ten = "%s_voice-nen(%d).%s" % (ten_goc, n, dinh_dang)
        n += 1
    return os.path.join(thu_muc, ten)


def chuan_hoa_am_luong_phan_tram(gia_tri):
    """(v7.18) Chuan hoa o am luong (%): la thi ve 100, kep 0-200."""
    try:
        n = float(str(gia_tri).strip())
    except Exception:
        n = 100.0
    return max(0.0, min(200.0, n))


def co_tron_nhac_sau_gop(can_gop, gop_da_xong, da_huy, ts):
    """(v7.18) Dieu kien tron nhac nen sau buoc gop cuoi: che do phai
    co file gop (khong phai "Tung cau rieng"), file gop da xong, khong
    bi huy, va cong tac tron dang BAT. TAT (mac dinh) thi khong sinh
    them file nao, khong them thoi gian."""
    return bool(can_gop and gop_da_xong and not da_huy
                and isinstance(ts, dict) and ts.get("tron_nhac"))


def tron_nhac_vao_voice(ffmpeg, voice, nen, dich, am_luong_voice=1.0,
                        am_luong_nen=1.0, bitrate_mp3="128k", dung=None,
                        log_cb=None, giong_goc=None,
                        am_luong_giong_goc=0.0, dinh_dang="mp3"):
    """(v7.18) Tron 1 lan file voice MP3 long tieng + file nhac nen
    thanh 1 file MP3 128k (44.1k/stereo) — dung sau buoc gop cuoi o
    tab Doc phu de. Dung lenh gop am thanh chung cua v7.17 (amix
    duration=longest, normalize=0, KHONG sidechain; file mono nhan
    doi kenh bang pan truoc khi tron de khong mat ~3 dB) + cua kiem
    tra chat luong (ffprobe + giai ma thu toan bo). Tra ve (True,
    thong_tin) neu xong, (False, thong_bao_loi) neu loi — KHONG xoa /
    khong dong vao file voice goc. Mọi lệnh ffmpeg/ffprobe ben trong
    deu chay ngam (chay_ngam_kwargs) qua cac helper cu.
    (v7.23) giong_goc (tuy chon): file giong goc tieng Trung de tron
    them track thu 3; dinh_dang (mp3/wav/m4a): dinh dang file tron
    cuoi — mac dinh mp3 128k nhu cu, WAV thi PCM khong nen (nang),
    M4A thi AAC 128k."""
    if not voice or not os.path.isfile(voice):
        return False, "Không tìm thấy file voice: %s" % voice
    if not nen or not os.path.isfile(nen):
        return False, "Không tìm thấy file nhạc nền: %s" % nen
    dinh_dang = str(dinh_dang or "mp3").lower()
    if dinh_dang not in GOP_AM_THANH_DINH_DANG:
        dinh_dang = "mp3"
    if giong_goc and not os.path.isfile(giong_goc):
        return False, "Không tìm thấy file giọng gốc: %s" % giong_goc
    try:
        ffprobe = tim_ffprobe(ffmpeg)
        tong_giay = 0
        if ffprobe:
            for f in (voice, nen) + ((giong_goc,) if giong_goc else ()):
                d = lay_thoi_luong(ffprobe, f)
                if d:
                    tong_giay = max(tong_giay, d)
        cmd = lenh_gop_am_thanh(ffmpeg, voice, nen, dich,
                                float(am_luong_voice), float(am_luong_nen),
                                dinh_dang, bitrate_mp3,
                                giong_goc, float(am_luong_giong_goc))
        timeout_giay = (max(300, int(tong_giay) * 3 + 120)
                        if tong_giay else 600)
        try:
            rc, err = _chay_ffmpeg_co_gioi_han(
                cmd, timeout_giay, dung=dung, log_cb=log_cb,
                nhan="trộn nhạc nền vào voice")
        except TimeoutError:
            return False, ("Trộn hết thời gian chờ (%ds)" % timeout_giay)
        if rc == -1:
            return False, "Đã hủy trộn."
        if rc != 0 or not (os.path.isfile(dich)
                           and os.path.getsize(dich) > 0):
            tail = (err or "").strip()[-600:]
            _ghi_log_loi_ffmpeg(os.path.dirname(dich) or ".",
                                tail or "ffmpeg lỗi không rõ")
            return False, ("ffmpeg trộn lỗi (mã %s)%s"
                           % (rc, (" — " + tail) if tail else ""))
        if dinh_dang == "wav":
            bitrate_mong = None
        elif dinh_dang == "m4a":
            bitrate_mong = 128000
        else:
            try:
                bitrate_mong = (int(str(bitrate_mp3).lower()
                                    .rstrip("k")) * 1000)
            except Exception:
                bitrate_mong = 128000
        ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
            dich, ffmpeg, dinh_dang, bitrate_mong)
        if not ok:
            return False, "File trộn ra không đạt chuẩn: %s" % thong_tin
        return True, thong_tin
    except Exception as e:
        return False, _tom_tat_loi(e)


class GopDan:
    """Gop MP3 theo moc thoi gian SRT bang ffmpeg concat demuxer
    (v7.7, VIET LAI — thay GopDan-WAV-tam cua v1.3/v7.5).
    Moi cau doc xong chi luu file MP3 rieng trong tung-cau (nhu tool
    cu da lam duoc); toi buoc hoan tat moi gop 1 lan: lap danh sach
    concat gom file tung cau xen ke file im lang 1s, dung moc gio
    SRT (cau nao doc dai hon slot thi cat bang outpoint), chay
    ffmpeg concat (v7.12: luon re-encode ve MP3 chuan 44100 Hz
    stereo 192k libmp3lame), kiem tra do dai file ra bang ffprobe.
    Loi ich so voi ban cu: khong con file WAV tam to bang tong thoi
    luong phim (voi 8156s thi vai tram MB den >1GB, truncate co the
    loi tren duong dan dai/o dia day), khong con timeout cung 600s
    o buoc chuyen WAV->MP3, loi ffmpeg ghi ro ra ffmpeg-loi.log.
    API giu nguyen nhu ban cu (them_cau / hoan_tat / so_cau /
    bo_qua / tran_slot / da_tao / do_dai_ms) de _chay khong phai
    doi logic goi."""

    def __init__(self, duong_dan_mp3, tong_ms=0, log_cb=None,
                 ffmpeg=None, thu_muc=None, che_do_tran="cat"):
        self.mp3 = duong_dan_mp3
        # tong_ms: moc ket thuc cua cau cuoi trong SRT - file gop phai
        # dai du den moc nay (du cau cuoi doc ngan hon slot cua no).
        self.tong_ms = tong_ms
        self.log_cb = log_cb
        self.ffmpeg = ffmpeg
        # thu_muc: cho file im lang + danh sach concat tam (mac dinh
        # la thu muc tung-cau, khong de rac thu muc du an).
        self.thu_muc = thu_muc or os.path.dirname(duong_dan_mp3) or "."
        # (v7.8) Che do cau tran slot: "cat" (mac dinh, cat duoi) /
        # "de" (phan tran phat nho duoi dau cau sau). Doc 1 lan luc
        # bat dau luot chay, dung suot luot do.
        self.che_do_tran = (che_do_tran if che_do_tran in CAU_TRAN_CHE_DO
                            else CAU_TRAN_CHE_DO_MAC_DINH)
        self.danh_sach = []  # list dict {cau, file, do_dai_ms}
        self.so_cau = 0       # so cau da ghi nhan
        self.bo_qua = 0       # so cau loi da bo qua (khong co audio)
        self.tran_slot = 0    # so cau doc dai hon slot cua no
        self.de_slot = 0      # so cau tran da de nho duoi cau sau
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
                if self.che_do_tran == "de":
                    self.log_cb("  Canh bao: cau %d doc het %.1fs nhung slot "
                                "chi co %.1fs (phan tran se phat nho duoi "
                                "dau cau sau)"
                                % (cau["chi_so"], do_dai / 1000.0,
                                   cho_trong / 1000.0))
                else:
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
        # Xay danh sach concat theo moc gio SRT (dung chung cho ca
        # che do cat va che do de).
        cac_cau = sorted(self.danh_sach,
                         key=lambda d: d["cau"]["bat_dau_ms"])
        danh_sach_doan, _con_troi = _lap_danh_sach_concat_cat(
            cac_cau, file_im_lang, self.tong_ms)
        if self.log_cb:
            self.log_cb("Đang gộp %d câu thành 1 file MP3 (ffmpeg "
                        "concat, đúng mốc giờ SRT)..." % self.so_cau)
        # (v7.7) Timeout ti le voi tong thoi luong phim (toi thieu
        # 600s), khong con timeout cung 600s cho moi phim nhu ban cu.
        timeout_giay = max(600, self.tong_ms // 1000 + 600)
        # (v7.8) Che do "de": thu tron phan tran nho duoi cau sau
        # truoc; tron loi thi tu quay ve cat duoi (khong crash,
        # khong mat file); bi Huy thi dung han, khong gop bu.
        if self.che_do_tran == "de":
            trang_thai_de, do_dai_de, loi_de, so_de = _gop_mp3_de(
                cac_cau, self.mp3, ffmpeg, log_cb=self.log_cb,
                dung=dung, timeout_giay=timeout_giay,
                log_loi_dir=os.path.dirname(self.mp3) or ".",
                tong_ms=self.tong_ms, thu_muc=self.thu_muc)
            if trang_thai_de == "ok":
                self.de_slot = so_de
                return True, do_dai_de
            if trang_thai_de == "huy":
                return False, 0
            if self.log_cb:
                self.log_cb("trộn đè lỗi (%s), đã gộp bằng cách cắt đuôi"
                            % (loi_de or "?"))
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
    """Ghi tien trinh xuat dang do vao thu_muc/tien-trinh.json.
    (v7.8) Ghi an toan: ghi ra file tam cung thu muc roi doi ten
    (os.replace) de neu crash/dong tool giua luc ghi thi file cu van
    nguyen ven, khong bao gio de lai file tien trinh ghi do."""
    try:
        os.makedirs(_duong_dan_dai_win(thu_muc), exist_ok=True)
        dich = os.path.join(thu_muc, TEN_FILE_TIEN_TRINH)
        tam = dich + ".tmp"
        with open(_duong_dan_dai_win(tam), "w",
                  encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(_duong_dan_dai_win(tam), _duong_dan_dai_win(dich))
        return True
    except Exception:
        try:
            _xoa_file_quiet(_duong_dan_dai_win(
                os.path.join(thu_muc, TEN_FILE_TIEN_TRINH + ".tmp")))
        except Exception:
            pass
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
        # (v7.8) Tam dung: worker dung lai sau cau dang doc (khong cat
        # ngang cau), luu tien trinh ngay; bam "Tiep tuc chay" thi chay
        # tiep dung cau ke tiep, khong doc lai cau nao.
        self._yeu_cau_tam_dung = threading.Event()  # co tam dung
        self._dang_tam_dung = False  # trang thai nut (luong chinh)
        # (v7.8) Anh chup tien trinh moi nhat de luong chinh luu duoc
        # ngay khi dong tool (worker cap nhat sau moi cau xong).
        # Khoa chung (RLock, cho phep goi long nhau) bao ve moi trang
        # thai chia se giua cac luong (tien trinh, dem cau xong, danh
        # sach loi, file gop): luong worker nao cung phai giu khoa khi
        # sua cac bien nay (xem _hoan_tat_cau, _luu_tien_trinh_ngay).
        self._khoa_chia_se = threading.RLock()
        self._anh_chup_tien_trinh = None
        self._ham_luu_tien_trinh = None  # closure trong _chay_thuc
        # (v7.8) Hang doi cau cho luong giong-may-local rieng (chi dung
        # khi goi song song + che do "local ngay"); None khi khong dung.
        self._hang_local = None
        # (v7.8) Khoa giong may local: toi da 1 luong doc bang SAPI
        # cung luc (PowerShell/SAPI chay noi tiep nhau cho chac).
        self._khoa_giong_may = threading.Lock()
        # (v7.8) Co tranh log "Da tam dung" lap lai khi nhieu luong
        # cung doi tam dung (chi log/luu 1 lan moi lan tam dung).
        self._da_log_tam_dung = False
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
        # (v7.24) VieNeu: nut tai tai nguyen + label trang thai (ngay duoi hang giong).
        tk.Button(f2, text="Tải tài nguyên VieNeu",
                  command=self._tai_tai_nguyen_vieneu).grid(row=0, column=2, sticky="w", padx=4)
        self.lb_vieneu = tk.Label(f2, text=vieneu_trang_thai()[2], wraplength=420, justify="left")
        self.lb_vieneu.grid(row=0, column=3, sticky="w")
        self.cb_giong.bind("<<ComboboxSelected>>",
                           lambda e: self._doi_giong_vieneu_mac_dinh(), add="+")

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

        # (v7.8) Khung "Toc do & goi song song": gom het setting toc do
        # (song song, gop batch, may chu/local) vao 1 cho de CYAN chinh
        # nhanh. Mac dinh moi setting deu la hanh vi cu (tuan tu, 1
        # cau/lan goi, may chu truoc + goi lai sau) de khong pha lan
        # chay hien tai; bat len khi can nhanh.
        f_toc_do = tk.LabelFrame(self, text=" Tốc độ & gọi song song ",
                                 padx=8, pady=6)
        f_toc_do.pack(fill="x", **pad)
        self.var_goi_song_song = tk.BooleanVar(
            value=bool(self.cfg.get("goi_song_song", False)))
        self.chk_goi_song_song = tk.Checkbutton(
            f_toc_do, text="Gọi song song nhiều câu cùng lúc",
            variable=self.var_goi_song_song,
            command=self._doi_goi_song_song)
        self.chk_goi_song_song.grid(row=0, column=0, sticky="w")
        ToolTip(self.chk_goi_song_song,
                "Gọi song song thì xong nhanh hơn, nhưng Microsoft dễ "
                "chặn 429 hơn (nhiều lần gọi cùng lúc). Câu nào lỗi thì "
                "Lượt 2 / gộp bù sẽ gọi lại sau, không mất câu.")
        tk.Label(f_toc_do, text="Số luồng song song:").grid(
            row=0, column=1, sticky="w", padx=(12, 0))
        self.var_so_luong = tk.StringVar(
            value=str(int(self.cfg.get("so_luong_song_song", 3))))
        self.e_so_luong = tk.Entry(f_toc_do,
                                   textvariable=self.var_so_luong, width=4)
        self.e_so_luong.grid(row=0, column=2, sticky="w")
        ToolTip(self.e_so_luong,
                "Mở trên 5 luồng thì Microsoft càng dễ chặn 429 "
                "(nhiều lần gọi cùng lúc), có thể chậm hơn chứ không "
                "nhanh hơn. Mở cao thì thử với file ngắn trước.")
        tk.Label(f_toc_do, text="(2-20, mặc định 3)").grid(
            row=0, column=3, sticky="w")
        tk.Label(f_toc_do, text="Số câu mỗi lần gọi:").grid(
            row=1, column=0, sticky="w")
        self.var_so_cau_gop = tk.StringVar(
            value=str(int(self.cfg.get("so_cau_gop_1_lan_goi", 1))))
        self.e_so_cau_gop = tk.Entry(f_toc_do,
                                     textvariable=self.var_so_cau_gop,
                                     width=4)
        self.e_so_cau_gop.grid(row=1, column=1, sticky="w")
        tk.Label(f_toc_do,
                 text="(1-10, 1 = gọi từng câu như cũ)").grid(
                     row=1, column=2, columnspan=2, sticky="w")
        ToolTip(self.e_so_cau_gop,
                "Gộp N câu thành 1 lần gọi Edge TTS cho đỡ bị Microsoft "
                "chặn 429. Audio trả về vẫn cắt đúng từng câu theo mốc "
                "giờ SRT (dùng WordBoundary). 1 lần gọi hỏng thì hỏng "
                "cả N câu, Lượt 2 sẽ đọc bù lẻ từng câu.")
        tk.Label(f_toc_do, text="Dùng máy chủ / local:").grid(
            row=2, column=0, sticky="w")
        # (v7.8) Dropdown thay the checkbox "Cau loi qua so lan thi doc
        # bang giong may local" cu. Chuyen tu config cu: checkbox cu
        # BAT thi ve "local ngay", TAT thi ve "goi lai sau".
        # LUU Y: doc_config() da setdefault khoa moi nen cfg luon co
        # key — phai doc FILE THO moi biet file cu co key moi hay
        # chua; neu chua co thi dung khoa cu de chon.
        che_do_luu = self.cfg.get("che_do_may_chu_local")
        co_khoa_moi = True
        try:
            with open(config_path(), "r", encoding="utf-8") as _f:
                _du_lieu_tho = json.load(_f)
            co_khoa_moi = ("che_do_may_chu_local"
                           in (_du_lieu_tho or {}))
        except Exception:
            co_khoa_moi = True
        if not co_khoa_moi:
            che_do_luu = ("may_chu_local_ngay"
                         if self.cfg.get("cau_loi_dung_giong_may", False)
                         else CHE_DO_MAY_CHU_LOCAL_MAC_DINH)
        elif che_do_luu not in CHE_DO_MAY_CHU_LOCAL:
            che_do_luu = CHE_DO_MAY_CHU_LOCAL_MAC_DINH
        self.var_che_do_may_chu_local = tk.StringVar(
            value=CHE_DO_MAY_CHU_LOCAL[che_do_luu])
        self.cb_che_do_may_chu_local = ttk.Combobox(
            f_toc_do, textvariable=self.var_che_do_may_chu_local,
            values=list(CHE_DO_MAY_CHU_LOCAL.values()),
            state="readonly", width=38)
        self.cb_che_do_may_chu_local.grid(row=2, column=1, columnspan=3,
                                          sticky="w")
        ToolTip(self.cb_che_do_may_chu_local,
                "'Chỉ máy chủ': chỉ Edge TTS, lỗi thì Lượt 2/gộp bù gọi "
                "lại sau. 'Máy chủ trước, lỗi → local ngay': Edge lỗi "
                "hết lượt thì chuyển ngay sang giọng máy local, không "
                "chờ Lượt 2. 'Máy chủ trước, lỗi → gọi lại sau': hành "
                "vi cũ. 'Local trước': thử giọng máy trước, lỗi thì gọi "
                "Edge. 'Song song cả hai': 1 câu gọi đồng thời cả Edge "
                "lẫn giọng máy, cái nào xong trước thì lấy — giọng máy "
                "thường xong trước (không cần mạng) nên hay cho ra "
                "giọng máy, chỉ dùng khi ưu tiên nhanh hơn chất giọng.")
        # (v7.8) Che do cau tran slot khi gop: cat duoi (mac dinh,
        # hanh vi cu) hoac de phan tran nho duoi dau cau sau.
        tk.Label(f_toc_do, text="Câu dài hơn khung giờ thì:").grid(
            row=3, column=0, sticky="w")
        che_do_tran_luu = self.cfg.get("cau_tran_che_do")
        if che_do_tran_luu not in CAU_TRAN_CHE_DO:
            che_do_tran_luu = CAU_TRAN_CHE_DO_MAC_DINH
        self.var_cau_tran = tk.StringVar(
            value=CAU_TRAN_CHE_DO[che_do_tran_luu])
        self.cb_cau_tran = ttk.Combobox(
            f_toc_do, textvariable=self.var_cau_tran,
            values=list(CAU_TRAN_CHE_DO.values()),
            state="readonly", width=38)
        self.cb_cau_tran.grid(row=3, column=1, columnspan=3, sticky="w")
        ToolTip(self.cb_cau_tran,
                "Chọn trước khi xuất — đổi giữa chừng không có tác dụng "
                "với lượt đang chạy (ô này bị khóa khi đang xuất, mở "
                "lại khi chạy xong / tạm dừng / hủy). 'Cắt đuôi': phần "
                "tràn bị cắt khi câu sau bắt đầu. 'Đè lên câu sau': "
                "phần đuôi tràn không bị cắt mà phát nhỏ dần (âm lượng "
                "0.35) dưới đầu câu sau — câu sau vẫn to, đúng mốc giờ.")
        if not self.var_goi_song_song.get():
            self.e_so_luong.configure(state="disabled")

        # (v7.8) Gop bu cau loi + fallback giong may local: 1 hang nho
        # ngay duoi chon Dau ra, khong lam roi giao dien.
        f3b = tk.Frame(self)
        f3b.pack(fill="x", **pad)
        self.var_gop_bu = tk.BooleanVar(
            value=bool(self.cfg.get("gop_bu_cau_loi", True)))
        self.chk_gop_bu = tk.Checkbutton(
            f3b, text="Tự gọi lại câu lỗi và gộp bù sau khi xuất xong",
            variable=self.var_gop_bu)
        self.chk_gop_bu.grid(row=0, column=0, sticky="w")
        ToolTip(self.chk_gop_bu,
                "Chỉ gọi lại câu lỗi sau khi gộp xong, đợi hết số giây "
                "đã đặt rồi mới gọi (để máy chủ hết chặn), rồi gộp lại "
                "file cuối — câu nào vẫn lỗi thì khung giờ đó giữ im "
                "lặng. Tối đa 1 vòng bù cho 1 lần xuất.")
        tk.Label(f3b, text="Đợi").grid(row=0, column=1, sticky="w",
                                       padx=(8, 0))
        self.var_gop_bu_doi = tk.StringVar(
            value=str(int(self.cfg.get("gop_bu_doi_giay", 60))))
        self.e_gop_bu_doi = tk.Entry(f3b, textvariable=self.var_gop_bu_doi,
                                     width=4)
        self.e_gop_bu_doi.grid(row=0, column=2, sticky="w")
        tk.Label(f3b, text="giây rồi mới gọi lại").grid(
            row=0, column=3, sticky="w")

        # (v7.18) Tron nhac nen khi doc: tuy chon, mac dinh TAT. BAT
        # thi sau buoc gop cuoi se tron them 1 lan file voice + nhac
        # nen (amix, khong sidechain) ra file <ten>_voice-nen.mp3 —
        # file voice goc giu nguyen. Tron 1 lan o cuoi cho ket qua
        # nghe giong het tron tung cau (amix tuyen tinh) nhung chi
        # encode 1 lan nen nhanh hon va it suy hao hon.
        f_tron = tk.LabelFrame(self, text=" Trộn nhạc nền khi đọc ",
                               padx=8, pady=6)
        f_tron.pack(fill="x", **pad)
        self.var_tron_nhac = tk.BooleanVar(
            value=bool(self.cfg.get("tron_nhac_khi_doc", False)))
        self.chk_tron_nhac = tk.Checkbutton(
            f_tron,
            text="Trộn nhạc nền vào file lồng tiếng sau khi đọc xong",
            variable=self.var_tron_nhac,
            command=self._doi_tron_nhac)
        self.chk_tron_nhac.grid(row=0, column=0, columnspan=2, sticky="w")
        ToolTip(self.chk_tron_nhac,
                "BẬT: sau khi gộp xong file voice MP3, tool trộn thêm 1 "
                "lần duy nhất voice + nhạc nền (amix, không nén giọng "
                "xuống khi nền lên) ra file <tên>_voice-nen.mp3 cạnh file "
                "voice — file voice gốc giữ nguyên, dùng file nào cũng "
                "được. TẮT (mặc định): chỉ ra file voice MP3 như cũ.")
        tk.Label(f_tron, text="File nhạc nền:").grid(row=1, column=0,
                                                     sticky="w")
        self.e_nen_tron = tk.Entry(f_tron, width=56)
        self.e_nen_tron.grid(row=1, column=1, sticky="we")
        self.btn_chon_nen_tron = tk.Button(
            f_tron, text="Chọn...", command=self._chon_file_nen_tron)
        self.btn_chon_nen_tron.grid(row=1, column=2)
        self.btn_lay_nen_tron = tk.Button(
            f_tron, text="Lấy file nền đã tách",
            command=self._dien_file_nen_tron_mac_dinh)
        self.btn_lay_nen_tron.grid(row=1, column=3, padx=4)
        tk.Label(f_tron, text="Âm lượng giọng đọc:").grid(
            row=2, column=0, sticky="w")
        self.var_tron_vol_voice = tk.StringVar(
            value=str(self.cfg.get("tron_nhac_vol_voice", 100)))
        self.e_tron_vol_voice = tk.Entry(
            f_tron, textvariable=self.var_tron_vol_voice, width=6)
        self.e_tron_vol_voice.grid(row=2, column=1, sticky="w", padx=4)
        tk.Label(f_tron, text="%").grid(row=2, column=2, sticky="w")
        tk.Label(f_tron, text="Âm lượng nhạc nền:").grid(
            row=3, column=0, sticky="w")
        self.var_tron_vol_nen = tk.StringVar(
            value=str(self.cfg.get("tron_nhac_vol_nen", 100)))
        self.e_tron_vol_nen = tk.Entry(
            f_tron, textvariable=self.var_tron_vol_nen, width=6)
        self.e_tron_vol_nen.grid(row=3, column=1, sticky="w", padx=4)
        tk.Label(f_tron, text="%").grid(row=3, column=2, sticky="w")
        tk.Button(f_tron, text="Sao chép log lỗi âm thanh",
                  command=self._sao_chep_loi_am_thanh).grid(
                      row=3, column=3, padx=4, sticky="w")
        # (v7.23) Tach + long mot lan: BAT thi 1 lan bam chay het
        # 3 pha (1) tach AI file goc -> nen + giong goc, (2) long
        # tieng SRT bang HoaiMy, (3) gop 3 track (giong long + nen +
        # giong goc) ra file cuoi. Chi sang khi muc tron nhac dang
        # BAT (tach truoc ma khong gop thi vo nghia — tach rieng
        # thuoc ve tab Xu ly am thanh).
        self.var_tach_nen_truoc = tk.BooleanVar(
            value=bool(self.cfg.get("tach_nen_truoc_khi_doc", False)))
        self.chk_tach_nen_truoc = tk.Checkbutton(
            f_tron,
            text="Tách nền AI trước khi lồng (1 lần bấm: tách → lồng → gộp)",
            variable=self.var_tach_nen_truoc,
            command=self._doi_tach_nen_truoc)
        self.chk_tach_nen_truoc.grid(row=4, column=0, columnspan=4,
                                     sticky="w")
        ToolTip(self.chk_tach_nen_truoc,
                "BẬT: bấm XUẤT là tool chạy liền 3 pha — tách AI file "
                "audio gốc ra nền + giọng gốc, lồng tiếng SRT bằng "
                "HoaiMy, rồi gộp 3 track ra file cuối trong thư mục "
                "project. Tách lỗi thì dừng, không lồng; lồng lỗi thì "
                "không gộp. TẮT (mặc định): lồng như cũ, trộn với "
                "file nhạc nền đã chọn ở trên.")
        tk.Label(f_tron, text="File audio gốc để tách:").grid(
            row=5, column=0, sticky="w")
        self.e_goc_tach_tron = tk.Entry(f_tron, width=56)
        self.e_goc_tach_tron.grid(row=5, column=1, sticky="we")
        self.btn_chon_goc_tach = tk.Button(
            f_tron, text="Chọn...",
            command=self._chon_file_goc_tach_tron)
        self.btn_chon_goc_tach.grid(row=5, column=2)
        self.btn_lay_goc_tach = tk.Button(
            f_tron, text="Lấy file _tieng của project",
            command=self._dien_file_goc_tach_tron_mac_dinh)
        self.btn_lay_goc_tach.grid(row=5, column=3, padx=4)
        tk.Label(f_tron, text="Âm lượng giọng gốc:").grid(
            row=6, column=0, sticky="w")
        self.var_tron_vol_giong_goc = tk.StringVar(
            value=str(self.cfg.get("tron_nhac_vol_giong_goc", 0)))
        self.e_tron_vol_giong_goc = tk.Entry(
            f_tron, textvariable=self.var_tron_vol_giong_goc, width=6)
        self.e_tron_vol_giong_goc.grid(row=6, column=1, sticky="w",
                                       padx=4)
        tk.Label(f_tron, text="%").grid(row=6, column=2, sticky="w")
        tk.Label(f_tron, text="Định dạng file gộp cuối:").grid(
            row=7, column=0, sticky="w")
        self.var_tron_dinh_dang = tk.StringVar(
            value=str(self.cfg.get("tron_nhac_dinh_dang", "MP3")))
        self.cb_tron_dinh_dang = ttk.Combobox(
            f_tron, textvariable=self.var_tron_dinh_dang,
            values=["MP3", "WAV", "M4A"], state="readonly", width=8)
        self.cb_tron_dinh_dang.grid(row=7, column=1, sticky="w", padx=4)
        tk.Label(
            f_tron,
            text="MP3 128k (mặc định); WAV nặng (không nén); M4A: AAC "
                 "128k. File voice lồng vẫn chuẩn MP3 44100/stereo/192k.",
            fg="gray", wraplength=700, justify="left",
            anchor="w").grid(row=7, column=2, columnspan=2, sticky="w")
        tk.Label(
            f_tron,
            text="Ô 'File audio gốc để tách' nhận file còn nguyên "
                 "giọng Trung + nền nhạc (VD file _tieng.mp4 của "
                 "project) — tool tự tách AI ra giọng gốc + nền rồi "
                 "mới lồng + gộp, không cần tách trước. Đã có sẵn "
                 "file nền đã tách thì tắt ô tách trước đi, chọn file "
                 "nền ở trên như cũ là được.",
            wraplength=700, justify="left", anchor="w",
            fg="gray").grid(row=8, column=0, columnspan=4, sticky="w")
        f_tron.columnconfigure(1, weight=1)
        self._doi_tron_nhac()

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
        self.file_voice_nen = None  # (v7.18) file voice + nhac nen

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
        # (v7.8) Nut Tam dung: chi bat khi dang chay; bam thi worker
        # dung sau cau dang doc, luu tien trinh ngay; bam lai ("Tiep
        # tuc chay") thi chay tiep dung cau ke tiep, khong doc lai.
        self.btn_tam_dung = tk.Button(f4, text="Tạm dừng",
                                      command=self._bam_tam_dung,
                                      state="disabled", padx=10, pady=4)
        self.btn_tam_dung.pack(side="left", padx=4)
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

    def _doi_goi_song_song(self):
        # (v7.8) Bat/tat goi song song: o "So luong song song" chi sang
        # khi checkbox dang BAT.
        if self.var_goi_song_song.get():
            self.e_so_luong.configure(state="normal")
        else:
            self.e_so_luong.configure(state="disabled")

    # ----- (v7.18) tron nhac nen khi doc -----
    def _doi_tron_nhac(self):
        # Bat/tat tron nhac: cac nut chon file + o am luong chi sang
        # khi checkbox dang BAT. O file nen van cho nhap tay de dan
        # duong dan bat cu luc nao; cong tac moi quyet co dung hay khong.
        trang_thai = "normal" if self.var_tron_nhac.get() else "disabled"
        for nut in (getattr(self, "btn_chon_nen_tron", None),
                    getattr(self, "btn_lay_nen_tron", None),
                    getattr(self, "chk_tach_nen_truoc", None)):
            try:
                if nut is not None:
                    nut.configure(state=trang_thai)
            except Exception:
                pass
        for o in (getattr(self, "e_tron_vol_voice", None),
                  getattr(self, "e_tron_vol_nen", None),
                  getattr(self, "e_tron_vol_giong_goc", None),
                  getattr(self, "cb_tron_dinh_dang", None)):
            try:
                if o is not None:
                    o.configure(state=trang_thai)
            except Exception:
                pass
        # (v7.23) O file goc + nut chon file goc chi sang khi ca 2
        # cong tac (tron nhac + tach truoc) deu BAT.
        try:
            self._doi_tach_nen_truoc()
        except Exception:
            pass

    def _doi_tach_nen_truoc(self):
        # (v7.23) Bat/tat tach truoc khi long: o file audio goc +
        # nut chon file chi sang khi ca tron nhac lan tach truoc deu
        # BAT. O am luong giong goc + o dinh dang thi chi can tron
        # nhac BAT (de tron voi file giong goc co san du tach truoc
        # co TAT).
        try:
            bat = bool(self.var_tron_nhac.get()
                       and self.var_tach_nen_truoc.get())
        except Exception:
            bat = False
        trang_thai = "normal" if bat else "disabled"
        for w in (getattr(self, "e_goc_tach_tron", None),
                  getattr(self, "btn_chon_goc_tach", None),
                  getattr(self, "btn_lay_goc_tach", None)):
            try:
                if w is not None:
                    w.configure(state=trang_thai)
            except Exception:
                pass

    def _chon_file_goc_tach_tron(self):
        # (v7.23) Chon file audio goc de tach AI (con nguyen giong
        # Trung + nen nhac, VD file _tieng.mp4 cua project).
        p = filedialog.askopenfilename(
            title="Chọn file audio gốc để tách AI",
            filetypes=[("Tất cả file", "*.*"),
                       ("Âm thanh", "*.mp3 *.wav *.m4a *.aac *.flac "
                                    "*.ogg *.opus *.wma *.mp4 *.mkv")])
        if p:
            self.e_goc_tach_tron.delete(0, "end")
            self.e_goc_tach_tron.insert(0, p)

    def _dien_file_goc_tach_tron_mac_dinh(self):
        # (v7.23) Dien san o file audio goc bang file audio cua du
        # an dang mo (uu tien file tieng rieng *_tieng.*). Chi dien
        # khi o dang trong hoac file cu khong con ton tai.
        hien = self.e_goc_tach_tron.get().strip()
        if hien and os.path.isfile(hien):
            return
        ung_vien = tim_file_audio_du_an(self._thu_muc_phim_hien_tai())
        if ung_vien:
            self.e_goc_tach_tron.delete(0, "end")
            self.e_goc_tach_tron.insert(0, ung_vien)

    def _dien_file_giong_goc_tron_mac_dinh(self):
        # (v7.23) Tim file giong goc di kem file nen da chon: cung
        # thu muc, cung ten goc (<ten>_giong-goc.mp3 doi voi
        # <ten>_nen-tach.mp3); khong co thi quet thu muc phim.
        # Tra ve duong dan hoac "".
        try:
            nen = self.e_nen_tron.get().strip()
            if nen:
                thu_muc = os.path.dirname(nen) or "."
                ten = os.path.splitext(os.path.basename(nen))[0]
                if ten.lower().endswith("_nen-tach"):
                    ten_goc = ten[:-len("_nen-tach")]
                    ung_vien = os.path.join(
                        thu_muc, "%s_giong-goc.mp3" % ten_goc)
                    if os.path.isfile(ung_vien):
                        return ung_vien
        except Exception:
            pass
        try:
            ung_vien = tim_file_giong_goc_tach(
                self._thu_muc_phim_hien_tai())
        except Exception:
            ung_vien = None
        return ung_vien or ""

    def _chon_file_nen_tron(self):
        # (v7.18) Chon file nhac nen: moi loai file am thanh, ke ca
        # .mp4 chi co tieng (ffmpeg doc luong tieng, bo track hinh).
        p = filedialog.askopenfilename(
            title="Chọn file nhạc nền",
            filetypes=[("Tất cả file", "*.*"),
                       ("Âm thanh", "*.mp3 *.wav *.m4a *.aac *.flac "
                                    "*.ogg *.opus *.wma *.mp4 *.mkv")])
        if p:
            self.e_nen_tron.delete(0, "end")
            self.e_nen_tron.insert(0, p)

    def _thu_muc_phim_hien_tai(self):
        # (v7.18) Thu muc phim cua SRT dang mo: <thu muc luu>/<ten file
        # SRT>; neu chua chon SRT thi dung thu muc ket qua cua luot
        # chay truoc (neu co).
        try:
            srt = self.e_srt.get().strip()
            if srt:
                ten_goc = os.path.splitext(os.path.basename(srt))[0]
                thu_muc_luu = (self.e_luu.get().strip()
                               or self.cfg.get("thu_muc_luu", ""))
                if thu_muc_luu and ten_goc:
                    duong = os.path.join(thu_muc_luu, ten_goc)
                    if os.path.isdir(duong):
                        return duong
        except Exception:
            pass
        try:
            thu_muc = getattr(self, "thu_muc_ket_qua", None)
            if thu_muc and os.path.isdir(thu_muc):
                return thu_muc
        except Exception:
            pass
        return None

    def _dien_file_nen_tron_mac_dinh(self):
        # (v7.18) Dien san o file nhac nen bang file nen da tach
        # <ten>_nen-tach.mp3 trong thu muc phim (neu co). Chi dien khi
        # o dang trong hoac file cu khong con ton tai — khong ghi de
        # file cau da chon tay.
        hien = self.e_nen_tron.get().strip()
        if hien and os.path.isfile(hien):
            return
        ung_vien = tim_file_nen_tach(self._thu_muc_phim_hien_tai())
        if ung_vien:
            self.e_nen_tron.delete(0, "end")
            self.e_nen_tron.insert(0, ung_vien)

    def _sao_chep_loi_am_thanh(self):
        # (v7.18) Copy toan bo nhat ky loi am thanh (chung 2 tab) vao
        # clipboard, 1 lan bam — dang o tab Doc phu de cung copy duoc
        # ngay, khong can chuyen tab.
        noi_dung = lay_noi_dung_loi_am_thanh()
        try:
            self.clipboard_clear()
            self.clipboard_append(noi_dung if noi_dung else
                                  "Chưa có lỗi âm thanh nào.")
            self._log("Đã sao chép log lỗi âm thanh (%d dòng)."
                      % (len(noi_dung.splitlines()) if noi_dung else 0))
        except Exception as e:
            messagebox.showerror(APP_TITLE,
                                 "Không sao chép được log lỗi: %s" % e)

    def _lay_che_do_may_chu_local(self):
        """Tra ve key che do may chu/local theo dropdown hien tai (vd
        'may_chu_goi_lai_sau'); gia tri la thi ve mac dinh."""
        hien = self.var_che_do_may_chu_local.get()
        for key, ten in CHE_DO_MAY_CHU_LOCAL.items():
            if ten == hien:
                return key
        return CHE_DO_MAY_CHU_LOCAL_MAC_DINH

    def _lay_cau_tran_che_do(self):
        """(v7.8) Tra ve key che do cau tran slot ('cat' / 'de') theo
        dropdown hien tai; gia tri la thi ve 'cat' (mac dinh)."""
        hien = self.var_cau_tran.get()
        for key, ten in CAU_TRAN_CHE_DO.items():
            if ten == hien:
                return key
        return CAU_TRAN_CHE_DO_MAC_DINH

    def _lay_so_cau_gop(self):
        """Tra ve so cau gop 1 lan goi (1-10, mac dinh 1); gia tri la
        thi ve 1."""
        try:
            n = int(float(str(self.var_so_cau_gop.get()).strip()))
        except Exception:
            n = 1
        return max(1, min(10, n))

    def _lay_so_luong_song_song(self):
        """Tra ve so luong song song (2-20, mac dinh 3); gia tri la thi
        ve 3."""
        try:
            n = int(float(str(self.var_so_luong.get()).strip()))
        except Exception:
            n = 3
        return max(2, min(20, n))

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
        # (v7.8) O chon che do cau tran cung bi khoa khi dang xuat:
        # gia tri chi doc 1 lan luc bat dau luot chay, doi giua
        # chung khong co tac dung voi luot dang chay.
        self.cb_cau_tran.configure(state="disabled")
        self.btn_huy.configure(state="normal" if cho_huy else "disabled")
        # (v7.8) Nut Tam dung chi co nghia khi dang xuat (cho_huy);
        # dang kiem tra giong thi tat.
        self.btn_tam_dung.configure(state="normal" if cho_huy
                                    else "disabled")

    def _mo_khoa_nut(self):
        """Bat lai cac nut sau khi xuat/kiem tra xong (hoac da huy).
        Nut Tiep tuc / Sub lai tu dau thi danh gia lai theo tien trinh
        da luu (co the vua duoc luu khi huy)."""
        for b in (self.btn_chon_srt, self.btn_chon_luu, self.btn_kiem_tra,
                  self.btn_cap_nhat, self.btn_bat_dau, self.btn_nghe_thu):
            b.configure(state="normal")
        self.btn_dung_nghe.configure(state="disabled")
        # (v7.8) Mo lai o chon che do cau tran (chay xong / da huy).
        self.cb_cau_tran.configure(state="readonly")
        self.btn_huy.configure(state="disabled")
        # (v7.8) Reset nut Tam dung ve trang thai ban dau.
        self.btn_tam_dung.configure(state="disabled", text="Tạm dừng")
        self._yeu_cau_tam_dung.clear()
        self._dang_tam_dung = False
        with self._khoa_chia_se:
            self._da_log_tam_dung = False
        self._ham_luu_tien_trinh = None
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
            if not xong:
                continue
            if len(xong) >= tong:
                # (v7.8) Da doc xong het cau nhung file gop chua co (gop
                # bi huy/loi giua chung): van cho 'Tiep tuc' de gop
                # lai. File gop da co = xuat xong tron ven, khong can
                # tiep tuc nua.
                file_gop = tt.get("file_gop")
                if file_gop and os.path.isfile(
                        _duong_dan_dai_win(file_gop)):
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
        # (v7.8) So giay doi truoc khi gop bu: chi nhan so, keo ve
        # 0..600 giay (0 = goi lai ngay, khong doi).
        try:
            doi_giay = int(float(str(
                self.var_gop_bu_doi.get()).strip()))
        except Exception:
            doi_giay = 60
        doi_giay = max(0, min(600, doi_giay))
        self.var_gop_bu_doi.set(str(doi_giay))
        # (v7.8) So cau gop / so luong song song: keo ve gioi han
        # (1-10 / 2-20), ghi lai dung gia tri da chuan hoa len o nhap.
        so_cau_gop = self._lay_so_cau_gop()
        self.var_so_cau_gop.set(str(so_cau_gop))
        so_luong = self._lay_so_luong_song_song()
        self.var_so_luong.set(str(so_luong))
        che_do_may_chu_local = self._lay_che_do_may_chu_local()
        cau_tran_che_do = self._lay_cau_tran_che_do()
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
            # (v7.8) Gop bu cau loi + fallback giong may local.
            "gop_bu_cau_loi": bool(self.var_gop_bu.get()),
            "gop_bu_doi_giay": doi_giay,
            # (v7.8) Toc do: gop batch, goi song song, che do may
            # chu/local (dropdown thay checkbox cu). Giu key cu
            # "cau_loi_dung_giong_may" dong bo theo dropdown de ban
            # cu doc duoc: BAT khi che do la "local ngay".
            "so_cau_gop_1_lan_goi": so_cau_gop,
            "goi_song_song": bool(self.var_goi_song_song.get()),
            "so_luong_song_song": so_luong,
            "che_do_may_chu_local": che_do_may_chu_local,
            "cau_loi_dung_giong_may": (
                che_do_may_chu_local == "may_chu_local_ngay"),
            # (v7.8) Che do cau tran slot khi gop ("cat"/"de").
            "cau_tran_che_do": cau_tran_che_do,
            # (v7.18) Tron nhac nen khi doc (mac dinh TAT) + am luong
            # giong doc / nhac nen (%, kep 0-200, KHONG goi y).
            "tron_nhac_khi_doc": bool(self.var_tron_nhac.get()),
            "tron_nhac_vol_voice": int(chuan_hoa_am_luong_phan_tram(
                self.var_tron_vol_voice.get())),
            "tron_nhac_vol_nen": int(chuan_hoa_am_luong_phan_tram(
                self.var_tron_vol_nen.get())),
            # (v7.23) Tach + long mot lan + am luong giong goc (mac
            # dinh 0%) + dinh dang file gop cuoi (mac dinh MP3).
            "tach_nen_truoc_khi_doc": bool(
                self.var_tach_nen_truoc.get()),
            "tron_nhac_vol_giong_goc": int(chuan_hoa_am_luong_phan_tram(
                self.var_tron_vol_giong_goc.get())),
            "tron_nhac_dinh_dang": (
                str(self.var_tron_dinh_dang.get() or "MP3").strip()
                .upper() if str(
                    self.var_tron_dinh_dang.get() or "MP3").strip()
                .upper() in ("MP3", "WAV", "M4A") else "MP3"),
        })
        luu_config(self.cfg)

    # (v7.24) VieNeu: tai tai nguyen trong thread rieng (pip install + tai model lan dau
    # co the mat vai phut, ~2-3GB, luu ngoai o C: theo luat cua CYAN).
    def _tai_tai_nguyen_vieneu(self):
        if getattr(self, "dang_chay", False):
            self._log("Đang chạy tác vụ khác, đợi xong rồi bấm lại nút tải VieNeu.")
            return
        self._log("Đang tải tài nguyên VieNeu (pip install vieneu + tải model lần đầu)...")
        def _chay():
            try:
                ok, msg = vieneu_tai_tai_nguyen(log_cb=self._log)
            except Exception as exc:
                ok, msg = False, "Lỗi tải tài nguyên VieNeu: %s" % exc
            try:
                self.lb_vieneu.config(text=msg)
            except Exception:
                pass
            self._log(msg)
        threading.Thread(target=_chay, daemon=True).start()

    def _doi_giong_vieneu_mac_dinh(self):
        # (v7.24) Chon giong VieNeu thi toc do mac dinh 0.95x cho du an faceless.
        try:
            if vieneu_giong_la_vieneu(self.cb_giong.get()):
                self.sl_toc_do.set(0.95)
                self.lb_toc_do.config(text="0.95x")
        except Exception:
            pass

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
        # (v7.24) VieNeu: kiem tra giong local, KHONG can edge-tts —
        # re thang sang doc_cau_thanh_mp3 (vieneu_doc_mp3), khong di
        # qua cua kiem tra edge-tts o duoi (thieu edge-tts khong duoc
        # bao loi sai cho giong VieNeu).
        if vieneu_giong_la_vieneu(voice):
            self._log("Kiểm tra giọng %s (VieNeu local, không cần "
                      "mạng)..." % ts["giong_hien_thi"])
            try:
                os.makedirs(ts["thu_muc"], exist_ok=True)
            except OSError as e:
                self._log("Lỗi tạo thư mục: %s" % e)
                self.hang_doi.put(("xong",))
                return
            dich = os.path.join(ts["thu_muc"], "doc-thu.mp3")
            ok, _bm, loi = doc_cau_thanh_mp3(
                MAU_DOC_THU, voice, ts["toc_do"], ts["cao_do"], dich,
                log_cb=self._log)
            if ok:
                self._log("OK! Đã tạo file đọc thử: %s" % dich)
            else:
                self._log("LỖI: không tạo được giọng VieNeu. %s" % loi)
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
        # (v7.8) Dang tam dung ma bam Huy thi worker thoat khoi vong
        # doi tam dung va dung han (khong cho bam "Tiep tuc chay" nua).
        self._yeu_cau_tam_dung.clear()
        self.btn_huy.configure(state="disabled")
        self.btn_tam_dung.configure(state="disabled")
        self._log("Đã bấm Hủy — sẽ dừng sau khi câu đang đọc xong...")

    def _bam_tam_dung(self):
        """Nut Tam dung / Tiep tuc chay (luong chinh): dat/bo co tam
        dung. Worker se dung sau khi cau dang doc xong (khong cat
        ngang cau) va luu tien trinh ngay; bam lai thi chay tiep dung
        cau ke tiep, khong doc lai cau nao."""
        if not self.dang_chay:
            return
        if not self._dang_tam_dung:
            self._yeu_cau_tam_dung.set()
            self._dang_tam_dung = True
            self.btn_tam_dung.configure(text="Tiếp tục chạy")
            # (v7.8) Tam dung xong thi mo lai o chon che do cau tran
            # de doi cho LUOT SAU (luot dang tam dung van dung gia tri
            # cu da doc luc bat dau, doi luc nay khong anh huong no).
            self.cb_cau_tran.configure(state="readonly")
            self._log("Đã bấm Tạm dừng — sẽ dừng sau khi câu đang đọc "
                      "xong...")
        else:
            self._yeu_cau_tam_dung.clear()
            self._dang_tam_dung = False
            with self._khoa_chia_se:
                self._da_log_tam_dung = False
            self.btn_tam_dung.configure(text="Tạm dừng")
            # (v7.8) Chay tiep thi khoa lai o chon che do cau tran.
            self.cb_cau_tran.configure(state="disabled")
            self._log("Tiếp tục chạy...")

    def _doi_tam_dung(self, so_xong, tong):
        """(v7.8) Worker: neu dang tam dung thi dung cho (0.2s/lan) cho
        toi khi bam 'Tiep tuc chay' hoac bam Huy. Khi vua tam dung thi
        luu tien trinh ngay. Tra ve True neu bi Huy trong luc cho.
        Nhieu luong cung doi thi chi log/luu 1 lan (co _da_log_tam_dung)."""
        if not self._yeu_cau_tam_dung.is_set():
            return False
        with self._khoa_chia_se:
            da_log = self._da_log_tam_dung
            if not da_log:
                self._da_log_tam_dung = True
        if not da_log:
            ham_luu = getattr(self, "_ham_luu_tien_trinh", None)
            if ham_luu is not None:
                try:
                    ham_luu()
                except Exception:
                    pass
            self._tien_trinh(
                int(so_xong * 100 / max(1, tong)),
                "Đã tạm dừng — đã xong %d/%d câu. Bấm 'Tiếp tục chạy' để "
                "chạy tiếp." % (so_xong, tong))
            self._log("Đã tạm dừng — đã xong %d/%d câu. Đã lưu tiến trình "
                      "(xong %d/%d câu)." % (so_xong, tong, so_xong, tong))
        while self._yeu_cau_tam_dung.is_set():
            if self._yeu_cau_huy.is_set():
                return True
            time.sleep(0.2)
        return self._yeu_cau_huy.is_set()

    def _lay_tien_trinh_hien_tai(self):
        """Tra ve (so cau da xong, tong cau) tu anh chup tien trinh moi
        nhat (worker cap nhat sau moi cau xong)."""
        with self._khoa_chia_se:
            snap = self._anh_chup_tien_trinh
        if not snap:
            return 0, 0
        try:
            return (len(snap.get("cau_da_xong", [])),
                    int(snap.get("tong_cau", 0)))
        except Exception:
            return 0, 0

    def _luu_anh_chup_hien_tai(self):
        """Luu ngay anh chup tien trinh moi nhat (goi tu luong chinh
        khi dong tool). Tra ve True neu da luu."""
        with self._khoa_chia_se:
            snap = (dict(self._anh_chup_tien_trinh)
                    if self._anh_chup_tien_trinh else None)
        if not snap or not snap.get("thu_muc"):
            return False
        return bool(_luu_tien_trinh(snap["thu_muc"], snap))

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
        # (v7.18) Dien san file nen da tach (neu co) truoc khi chay de
        # worker co duong dan dung ngay ca khi CYAN khong bam nut lay.
        self._dien_file_nen_tron_mac_dinh()
        # (v7.23) Dien san file audio goc de tach (neu co) truoc khi
        # chay — luong tach truoc khi long dung luon.
        self._dien_file_goc_tach_tron_mac_dinh()
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
            # (v7.8) Gop bu cau loi + toc do (gop batch, goi song song,
            # che do may chu/local — dropdown thay checkbox cu).
            "gop_bu": bool(self.var_gop_bu.get()),
            "gop_bu_doi_giay": int(self.cfg.get("gop_bu_doi_giay", 60)),
            "so_cau_gop_1_lan_goi": self._lay_so_cau_gop(),
            "goi_song_song": bool(self.var_goi_song_song.get()),
            "so_luong_song_song": self._lay_so_luong_song_song(),
            "che_do_may_chu_local": self._lay_che_do_may_chu_local(),
            # (v7.8) Che do cau tran slot: chi doc 1 lan luc BAT DAU
            # luot chay roi dung suot luot do; doi giua chung khong
            # co tac dung voi luot dang chay, luot sau (Tiep tuc /
            # chay moi) moi doc lai gia tri moi.
            "cau_tran_che_do": self._lay_cau_tran_che_do(),
            # (v7.18) Tron nhac nen khi doc: cong tac + file nen +
            # am luong giong doc / nhac nen (he so, 1.0 = 100%).
            "tron_nhac": bool(self.var_tron_nhac.get()),
            "tron_nhac_file_nen": self.e_nen_tron.get().strip(),
            "tron_nhac_vol_voice": (
                chuan_hoa_am_luong_phan_tram(
                    self.var_tron_vol_voice.get()) / 100.0),
            "tron_nhac_vol_nen": (
                chuan_hoa_am_luong_phan_tram(
                    self.var_tron_vol_nen.get()) / 100.0),
            # (v7.23) Tach + long mot lan: cong tac tach truoc +
            # file audio goc de tach + am luong giong goc + dinh
            # dang file gop cuoi. File giong goc de tron: tach truoc
            # thi pha 1 dien vao; khong tach truoc thi tim file
            # <ten>_giong-goc.mp3 di kem file nen da chon (neu co).
            "tach_nen_truoc": bool(self.var_tach_nen_truoc.get()),
            "tach_nen_file_goc": self.e_goc_tach_tron.get().strip(),
            "tron_nhac_file_giong_goc": (
                self._dien_file_giong_goc_tron_mac_dinh()),
            "tron_nhac_vol_giong_goc": (
                chuan_hoa_am_luong_phan_tram(
                    self.var_tron_vol_giong_goc.get()) / 100.0),
            "tron_nhac_dinh_dang": (
                str(self.var_tron_dinh_dang.get() or "MP3").strip()
                .lower() if str(
                    self.var_tron_dinh_dang.get() or "MP3").strip()
                .lower() in GOP_AM_THANH_DINH_DANG else "mp3"),
        }
        if ts["tach_nen_truoc"] and not ts["tron_nhac"]:
            # (v7.23) Tach truoc thi phai gop moi ra file cuoi — ep
            # tron BAT (UI da khoa tach truoc khi tron TAT, day chi
            # la phong thu khi config bat tach truoc san).
            ts["tron_nhac"] = True
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

    def _tach_truoc_khi_doc(self, ts, ffmpeg, thu_muc):
        # (v7.23) PHA 1 cua luong tach + long mot lan: tach AI file
        # audio goc ra nen + giong goc, dung dung che do thiet bi GPU
        # da chon trong muc Cai dat GPU (doc tu config). Tra ve
        # (True, "") neu xong — ts duoc dien file nen + giong goc
        # vua tach de pha 3 gop; (False, loi) neu loi / da huy
        # (loi = "đã hủy" khi bam Huy). KHONG xoa file da tach duoc
        # (de dung lai sau). Dung ham tach chung voi tab Xu ly am
        # thanh (tach_ai_tach_nen_va_giong) nen log + kiem tra chat
        # luong + ten card that giong het nhau.
        goc = (ts.get("tach_nen_file_goc") or "").strip()
        if not goc or not os.path.isfile(goc):
            return False, ("Chưa chọn file audio gốc để tách (hoặc file "
                           "không tồn tại).")
        if not ffmpeg:
            return False, "Không tìm thấy ffmpeg trên máy."
        try:
            che_do_tb = str(doc_config().get("ai_tach_thiet_bi")
                            or "tu_dong").strip().lower()
        except Exception:
            che_do_tb = "tu_dong"
        if che_do_tb not in ("tu_dong", "cpu", "gpu"):
            che_do_tb = "tu_dong"
        # Quet GPU moi truoc khi tach (thu that voi model) de biet
        # chac card nao se chay + ten card de log.
        _tt, duong_model = trang_thai_model_ai(AI_TACH_MODELS[0])
        ket_qua_quet = quet_gpu_directml(
            duong_model if _tt == "co" else None)
        ok, info, loi = tach_ai_tach_nen_va_giong(
            ffmpeg, goc, che_do_tb, ket_qua_quet, GOP_AM_THANH_BITRATE,
            log_cb=self._log,
            tien_trinh_cb=lambda pct: self._tien_trinh(
                pct, "Đang tách nền (1/3)..."),
            dung=self._yeu_cau_huy)
        if not ok:
            return False, loi
        ts["tron_nhac_file_nen"] = info["nen"]
        ts["tron_nhac_file_giong_goc"] = info["giong_goc"]
        ts["tron_nhac"] = True
        if info["thiet_bi"] == "gpu":
            thiet_bi_txt = ("GPU — %s" % info["ten_card"]
                            if info.get("ten_card") else "GPU")
        else:
            thiet_bi_txt = "CPU"
        self._log("Đã tách xong file nền bằng AI (%s): %s (%s); giọng "
                  "gốc: %s (%s)" % (thiet_bi_txt, info["nen"],
                                    info["thong_tin_nen"],
                                    info["giong_goc"],
                                    info["thong_tin_giong"]))
        return True, ""

    def _tron_nhac_sau_gop(self, ts, dich_gop, thu_muc, ffmpeg):
        # (v7.18) Tron nhac nen vao file voice vua gop xong (1 lan duy
        # nhat, sau ca gop bu neu co). Tra ve (duong_dan_file_tron,
        # None) neu xong, (None, thong_bao_loi) neu loi. Loi tron KHONG
        # lam hong luot doc: file voice goc giu nguyen, loi ghi rieng
        # vao nhat ky loi am thanh + hop thoai bao rieng.
        # (v7.23) Tron 3 track khi co file giong goc (voice HoaiMy +
        # nen + giong goc tieng Trung); file gop cuoi theo dinh dang
        # da chon (MP3/WAV/M4A) — file voice trung gian van chuan
        # MP3 44100/stereo/192k cua SRT Reader.
        nen = (ts.get("tron_nhac_file_nen") or "").strip()
        if not nen:
            msg = ("Bật trộn nhạc nền nhưng chưa chọn file nhạc nền — "
                   "chỉ xuất file voice MP3, không trộn.")
            self._log("LỖI trộn nhạc nền: " + msg)
            ghi_loi_am_thanh("trộn", msg, dich_gop)
            self.hang_doi.put(("loi_hop_thoai",
                               "Trộn nhạc nền: " + msg))
            return None, msg
        if not os.path.isfile(nen):
            msg = "Không tìm thấy file nhạc nền: %s" % nen
            self._log("LỖI trộn nhạc nền: " + msg)
            ghi_loi_am_thanh("trộn", msg, nen)
            self.hang_doi.put(("loi_hop_thoai",
                               "Trộn nhạc nền: " + msg))
            return None, msg
        dich_tron = ten_file_voice_nen(
            dich_gop, (ts.get("tron_nhac_dinh_dang") or "mp3").strip()
            .lower() if (ts.get("tron_nhac_dinh_dang") or "mp3").strip()
            .lower() in GOP_AM_THANH_DINH_DANG else "mp3")
        # (v7.23) Giong goc track thu 3 (neu co file hop le): tu pha
        # 1 tach truoc, hoac file <ten>_giong-goc.mp3 di kem file nen
        # da chon (dien san o _bat_dau_chung). Am luong mac dinh 0%.
        giong_goc = (ts.get("tron_nhac_file_giong_goc") or "").strip()
        if giong_goc and not os.path.isfile(giong_goc):
            giong_goc = ""
        vol_giong_goc = ts.get("tron_nhac_vol_giong_goc", 0.0)
        dinh_dang = (ts.get("tron_nhac_dinh_dang") or "mp3").strip().lower()
        if dinh_dang not in GOP_AM_THANH_DINH_DANG:
            dinh_dang = "mp3"
        nhan_pha = ("Đang gộp (3/3) — " if ts.get("tach_nen_truoc")
                    else "")
        self._log("%sĐang trộn nhạc nền vào file lồng tiếng: %s + %s%s"
                  % (nhan_pha, dich_gop, nen,
                     (" + giọng gốc: %s" % giong_goc)
                     if giong_goc else ""))
        self._tien_trinh(100, nhan_pha +
                         "Đang trộn nhạc nền vào file lồng tiếng...")
        ok, thong_tin = tron_nhac_vao_voice(
            ffmpeg, dich_gop, nen, dich_tron,
            ts.get("tron_nhac_vol_voice", 1.0),
            ts.get("tron_nhac_vol_nen", 1.0),
            "128k", dung=self._yeu_cau_huy,
            log_cb=lambda s: self._log(s),
            giong_goc=giong_goc or None,
            am_luong_giong_goc=vol_giong_goc,
            dinh_dang=dinh_dang)
        if ok:
            self.file_voice_nen = dich_tron
            self._log("XONG file voice + nhạc nền%s: %s (%s)"
                      % (" + giọng gốc" if giong_goc else "",
                         dich_tron, thong_tin))
            return dich_tron, None
        msg = "Trộn nhạc nền lỗi: %s" % thong_tin
        self._log("LỖI " + msg + " — giữ nguyên file voice MP3.")
        ghi_loi_am_thanh("trộn", thong_tin, nen)
        self.hang_doi.put(("loi_hop_thoai", msg))
        return None, msg

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
        # (v7.23) PHA 1 — TACH + LONG MOT LAN: tach AI file audio
        # goc truoc khi long (neu cong tac BAT). Tach xong moi long;
        # tach loi/huy thi DUNG LUON, khong long, khong gop. File
        # nen + giong goc vua tach duoc giu lai trong thu muc phim
        # de dung lai sau.
        if ts.get("tach_nen_truoc"):
            self._tien_trinh(0, "Đang tách nền (1/3)...")
            ok_tach, loi_tach = self._tach_truoc_khi_doc(
                ts, ffmpeg, thu_muc)
            if not ok_tach:
                if loi_tach == "đã hủy":
                    self._log("ĐÃ HỦY ở pha tách nền (1/3).")
                    self.hang_doi.put(
                        ("ket_qua", "ĐÃ HỦY ở pha tách nền (1/3)."))
                else:
                    self._log("LỖI tách nền (1/3): %s — dừng, không "
                              "lồng tiếng." % loi_tach)
                    ghi_loi_am_thanh("tách nền", loi_tach,
                                     ts.get("tach_nen_file_goc"))
                    self.hang_doi.put(
                        ("ket_qua", "LỖI tách nền (1/3): %s" % loi_tach))
                    self.hang_doi.put(
                        ("loi_hop_thoai",
                         "Tách nền trước khi lồng bị lỗi:\n%s\n\nKhông "
                         "lồng tiếng. Kiểm tra lại file audio gốc rồi "
                         "bấm XUẤT lại." % loi_tach))
                self.hang_doi.put(("xong",))
                return
            self._log("Đang lồng tiếng (2/3)...")
        # (v7.23) Nhan pha (2/3) gan vao nhan tien trinh tung cau
        # trong luong tach + long mot lan, de thay ro pha dang chay.
        nhan_pha_long = ("Đang lồng tiếng (2/3) — "
                         if ts.get("tach_nen_truoc") else "")
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
        # (v7.8) Che do may chu/local + gop batch + goi song song (doc
        # tu ts — gia tri giao dien da lay o luong chinh). Giong may
        # local doc le tung cau (khong gop batch); che do "local
        # truoc" / "song song ca hai" cung doc le tung cau vi 2 che do
        # nay xu ly rieng tung cau.
        che_do_local = ts.get("che_do_may_chu_local",
                              CHE_DO_MAY_CHU_LOCAL_MAC_DINH)
        so_cau_gop = ts.get("so_cau_gop_1_lan_goi", 1)
        try:
            so_cau_gop = int(so_cau_gop)
        except Exception:
            so_cau_gop = 1
        so_cau_gop = max(1, min(10, so_cau_gop))
        if voice == "may":
            if so_cau_gop > 1:
                self._log("Giọng máy local thì đọc lẻ từng câu "
                          "(không gộp batch).")
                so_cau_gop = 1
        elif che_do_local in ("local_truoc", "song_song_ca_hai"):
            if so_cau_gop > 1:
                self._log("Chế độ '%s' thì đọc lẻ từng câu "
                          "(không gộp batch)."
                          % CHE_DO_MAY_CHU_LOCAL.get(che_do_local,
                                                     che_do_local))
                so_cau_gop = 1
        if so_cau_gop > 1:
            self._log("Gộp %d câu vào 1 lần gọi Edge TTS (cắt lại từng "
                      "câu theo WordBoundary, đúng mốc giờ SRT) cho đỡ "
                      "bị chặn 429."
                      % so_cau_gop)
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
                thu_muc=thu_muc_rieng,
                # (v7.8) Che do cau tran: doc 1 lan tu ts (da chot
                # luc bat dau luot chay), dung suot luot do.
                che_do_tran=ts.get("cau_tran_che_do",
                                   CAU_TRAN_CHE_DO_MAC_DINH))
            self._log("Gộp cuối bằng ffmpeg concat: mỗi câu đọc xong "
                      "lưu file MP3 riêng trong tung-cau, xong hết mới "
                      "gộp thành 1 file lồng tiếng (đúng timestamp "
                      "SRT).")
        # (v7.8) TAM DUNG: luu tien trinh lien tuc sau moi cau xong (ghi
        # an toan qua _luu_tien_trinh) + anh chup de luong chinh luu
        # duoc ngay khi dong tool. Dung chung 1 ham cho ca luu giua
        # chung va luu cuoi luot chay (tranh lech cau truc du lieu).
        def _tao_du_lieu_tien_trinh():
            try:
                st = os.stat(_duong_dan_dai_win(srt))
            except OSError:
                return None
            return {
                "srt": srt,
                "srt_kich_thuoc": st.st_size,
                "srt_mtime": int(st.st_mtime),
                "tong_cau": tong,
                "cau_da_xong": sorted(cau_da_xong),
                "file_gop": dich_gop,
                "che_do": che_do,
                "giong": ts["giong_hien_thi"],
                "toc_do": float(toc_do),
                "toc_do_toi_da": float(toc_do_toi_da),
                "tu_dong_toc_do": bool(tu_dong_toc_do),
                "toc_do_cau": {str(k): float(v)
                               for k, v in toc_do_cau.items()},
                "cao_do": int(cao_do),
                "thu_muc": thu_muc,
                "thu_muc_rieng": thu_muc_rieng,
            }

        def _luu_tien_trinh_ngay():
            """Luu tien trinh hien tai (khi da xong it nhat 1 cau).
            Cap nhat anh chup de luong chinh luu duoc khi dong tool."""
            if so_cau_xong <= 0:
                return False
            du_lieu = _tao_du_lieu_tien_trinh()
            if du_lieu is None:
                return False
            with self._khoa_chia_se:
                self._anh_chup_tien_trinh = du_lieu
            return bool(_luu_tien_trinh(thu_muc, du_lieu))

        self._ham_luu_tien_trinh = _luu_tien_trinh_ngay
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

        def _ghi_loi_cau(chi_so):
            """Ghi 1 cau vao danh sach loi (khoa chung de goi song song
            an toan)."""
            with self._khoa_chia_se:
                loi_cau[chi_so] = True

        def _doc_local_khoa(text, dich, dung=None):
            """(v7.8) Doc 1 cau bang giong may local, toi da 1 luong
            cung luc (khoa chung _khoa_giong_may — SAPI/PowerShell chay
            noi tiep nhau cho chac). `dung`: co huy rieng (vd che do
            race) hoac None = co Huy chung. Tra ve (ok, loi)."""
            with self._khoa_giong_may:
                ok, _, loi = doc_giong_may(
                    text, toc_do, cao_do, dich,
                    log_cb=self._log, ffmpeg=ffmpeg,
                    dung=dung if dung is not None else self._yeu_cau_huy)
            return ok, loi

        def _hoan_tat_cau(cau, i, dich, bo_xac_minh=False,
                         dung_giong_may_roi=False):
            """(v7.8) Xu ly chung sau khi da co file audio 1 cau (du doc
            le, cat tu batch hay race): tinh toc do vua slot, cap nhat
            trang thai, ghep vao file gop, luu tien trinh. Tra ve True.
            An toan khi goi tu nhieu luong (trang thai chia se giu khoa
            chung _khoa_chia_se)."""
            nonlocal so_cau_xong
            # v1.4: toc do tu dong theo slot SRT - do thoi luong that
            # cua file vua tao roi dung ffmpeg atempo tang toc neu can
            # (khong goi lai API giong). Trang thai hien toc do thuc
            # cua cau (vd "Xong (1.60x)"). Buoc nay chi dung file
            # rieng cua cau nen khong can khoa.
            toc_do_thuc = _ap_dung_toc_do_tu_dong(
                dich, cau, toc_do, toc_do_toi_da, tu_dong_toc_do, ffmpeg,
                log_cb=self._log)
            with self._khoa_chia_se:
                toc_do_cau[cau["chi_so"]] = toc_do_thuc
                so_cau_xong += 1
                cau_da_xong.add(cau["chi_so"])
                # (v7.8) Cau doc bu bang giong may thi ghi ro trong trang
                # thai de CYAN biet doan nao khac giong HoaiMy.
                hau_to_giong_may = (" (giọng máy)"
                                    if dung_giong_may_roi else "")
                if tu_dong_toc_do:
                    self._dat_trang_thai_cau(
                        cau["chi_so"],
                        "Xong (%.2fx)%s" % (toc_do_thuc, hau_to_giong_may))
                else:
                    self._dat_trang_thai_cau(cau["chi_so"],
                                             "Xong" + hau_to_giong_may)
                # v1.3: ghep ngay cau vua xong vao file long tieng.
                if gop is not None:
                    gop.them_cau(cau, dich)
                # (v7.8) Luu tien trinh ngay sau moi cau xong de tam dung
                # / dong tool giua chung khong mat phan da chay.
                _luu_tien_trinh_ngay()
            if bo_xac_minh:
                self._log("  -> Xong (đã dùng chế độ bỏ xác minh SSL)")
            return True

        def _doc_race_1_cau(cau, dich):
            """(v7.8) Che do 'song song ca hai': chay Edge TTS va giong
            may local song song cho 1 cau, cai nao xong truoc thi lay
            file cua cai do; cai kia bi ngat (co huy rieng) va xoa file
            tam. Tra ve (ok, bo_xac_minh, dung_giong_may_roi, loi).
            Ben Edge dung doc_batch_thanh_mp3 (stream, ngat duoc giua
            chung) thay cho doc_cau_thanh_mp3 (save, khong ngat duoc).
            File tam phai co duoi .mp3 (.edge.mp3 / .may.mp3) de
            ffmpeg chon duoc muxer khi ghi (duoi .edge / .may tran
            thi ffmpeg bao 'Unable to choose an output format')."""
            tam_edge = dich + ".edge.mp3"
            tam_may = dich + ".may.mp3"
            ket_qua = {}
            khoa_race = threading.Lock()
            dung_edge = threading.Event()
            dung_may = threading.Event()

            def _chay_edge():
                try:
                    ok, bxm, _rb, loi = doc_batch_thanh_mp3(
                        cau["text"], voice, toc_do, cao_do, tam_edge,
                        log_cb=self._log, ffmpeg=ffmpeg,
                        timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                        dung=dung_edge)
                except Exception as e:
                    ok, bxm, loi = False, False, str(e)
                with khoa_race:
                    ket_qua["edge"] = (ok, bxm, loi, tam_edge)
                    if ok and "thang" not in ket_qua:
                        ket_qua["thang"] = "edge"
                if ket_qua.get("thang") not in (None, "edge"):
                    _xoa_file_quiet(tam_edge)

            def _chay_may():
                try:
                    ok, loi = _doc_local_khoa(cau["text"], tam_may,
                                               dung=dung_may)
                except Exception as e:
                    ok, loi = False, str(e)
                with khoa_race:
                    ket_qua["may"] = (ok, False, loi, tam_may)
                    if ok and "thang" not in ket_qua:
                        ket_qua["thang"] = "may"
                if ket_qua.get("thang") not in (None, "may"):
                    _xoa_file_quiet(tam_may)

            t_edge = threading.Thread(target=_chay_edge, daemon=True)
            t_may = threading.Thread(target=_chay_may, daemon=True)
            t_edge.start()
            t_may.start()
            while True:
                with khoa_race:
                    thang = ket_qua.get("thang")
                    ca_hai_xong = ("edge" in ket_qua
                                   and "may" in ket_qua)
                if thang or ca_hai_xong or self._yeu_cau_huy.is_set():
                    break
                time.sleep(0.05)
            # Ngat ben thua (neu thang da co).
            if thang == "edge":
                dung_may.set()
            elif thang == "may":
                dung_edge.set()
            t_edge.join(timeout=5)
            t_may.join(timeout=5)
            with khoa_race:
                thang = ket_qua.get("thang")
                kq_edge = ket_qua.get("edge")
                kq_may = ket_qua.get("may")
            if thang == "edge" and kq_edge and kq_edge[0]:
                try:
                    os.replace(_duong_dan_dai_win(tam_edge),
                               _duong_dan_dai_win(dich))
                except OSError:
                    return False, False, False, "không chuyển được file Edge"
                if not t_may.is_alive():
                    _xoa_file_quiet(tam_may)
                return True, kq_edge[1], False, ""
            if thang == "may" and kq_may and kq_may[0]:
                try:
                    os.replace(_duong_dan_dai_win(tam_may),
                               _duong_dan_dai_win(dich))
                except OSError:
                    return False, False, False, "không chuyển được file giọng máy"
                if not t_edge.is_alive():
                    _xoa_file_quiet(tam_edge)
                return True, False, True, ""
            _xoa_file_quiet(tam_edge)
            _xoa_file_quiet(tam_may)
            loi = ((kq_edge[2] if kq_edge else "")
                   or (kq_may[2] if kq_may else "") or "đã hủy")
            return False, False, False, loi

        def doc_1_cau(cau, i, dung_luong_local=False):
            """Doc 1 cau theo che do may chu/local
            (ts["che_do_may_chu_local"]), cap nhat tien trinh + trang
            thai trong danh sach. Cau xong thi GHEP NGAY vao file gop
            (neu che do gop).
            Tra ve True neu xong, False neu loi, "cho_local" neu cau da
            dua sang luong giong-may-local chay song song (chi khi goi
            song song + che do 'local ngay' — luong local se hoan tat
            hoac ghi loi cau nay sau, ben goi khong ghi loi nua).
            (v7.8) `dung_luong_local`: chi True o luong may chu khi goi
            song song; Luot 2 / gop bu / tuan tu thi doc bu local ngay
            tai cho (khoa _khoa_giong_may)."""
            dich = os.path.join(thu_muc_rieng, "%03d.mp3" % cau["chi_so"])
            self._tien_trinh(int((i - 1) * 100 / tong),
                             nhan_pha_long +
                             "Đang đọc câu %d/%d..." % (i, tong))
            self._dat_trang_thai_cau(cau["chi_so"], "Đang đọc...")
            self._log("Câu %d/%d (%.1fs): %s" % (
                i, tong, (cau["ket_thuc_ms"] - cau["bat_dau_ms"]) / 1000.0,
                cau["text"][:80]))
            # (v7.8) Che do "song song ca hai": race Edge vs local.
            if che_do_local == "song_song_ca_hai" and voice != "may":
                ok, bo_xac_minh, dung_may_roi, loi = _doc_race_1_cau(
                    cau, dich)
                if not ok:
                    if self._yeu_cau_huy.is_set():
                        return False
                    self._dat_trang_thai_cau(
                        cau["chi_so"], "Lỗi: " + (loi or "?")[:60])
                    self._log("  -> LỖI câu %d: %s" % (cau["chi_so"], loi))
                    return False
                return _hoan_tat_cau(cau, i, dich, bo_xac_minh,
                                     dung_may_roi)
            # (v7.8) Che do "local truoc": thu giong may truoc, loi thi
            # goi Edge TTS.
            if che_do_local == "local_truoc" and voice != "may":
                self._log("  Câu %d: thử giọng máy local trước..."
                          % cau["chi_so"])
                ok_may, loi_may = _doc_local_khoa(cau["text"], dich)
                if self._yeu_cau_huy.is_set():
                    return False
                if ok_may:
                    self._log("  Câu %d: đã đọc bằng giọng máy local."
                              % cau["chi_so"])
                    return _hoan_tat_cau(cau, i, dich, False, True)
                self._log("  Câu %d: giọng máy local lỗi (%s) — gọi "
                          "Edge TTS..." % (cau["chi_so"], loi_may or "?"))
            # (v7.7) Truyen co Huy + timeout giong: nut Huy dung duoc
            # ngay ca khi dang cho giong, het 120s thi failover luot
            # sau thay vi treo vo han o cau nay.
            ok, bo_xac_minh, loi = doc_cau_thanh_mp3(
                cau["text"], voice, toc_do, cao_do, dich,
                log_cb=self._log, ffmpeg=ffmpeg,
                timeout_giay=THOI_GIAN_TOI_DA_DOC_MOT_DOAN_GIAY,
                dung=self._yeu_cau_huy)
            if (not ok and not self._yeu_cau_huy.is_set()
                    and che_do_local == "may_chu_local_ngay"
                    and voice != "may"):
                if dung_luong_local and self._hang_local is not None:
                    # (v7.8) Go song song: dua cau sang luong
                    # giong-may-local rieng, khong chan luong may chu;
                    # luong local se hoan tat hoac ghi loi cau nay sau.
                    self._log("  Câu %d: Edge TTS lỗi, chuyển sang luồng "
                              "giọng máy local..." % cau["chi_so"])
                    self._hang_local.put((i, cau))
                    return "cho_local"
                # Tuan tu (hoac Luot 2 / gop bu): doc bu ngay bang
                # giong may local.
                self._log("  Câu %d: Edge TTS lỗi, thử đọc bù bằng "
                          "giọng máy local..." % cau["chi_so"])
                ok_may, loi_may = _doc_local_khoa(cau["text"], dich)
                if ok_may:
                    self._log("  Câu %d: Edge TTS lỗi, đã đọc bù bằng "
                              "giọng máy local." % cau["chi_so"])
                    return _hoan_tat_cau(cau, i, dich, False, True)
                if self._yeu_cau_huy.is_set():
                    return False
                loi_may = loi_may or "?"
                if ("Windows" in loi_may or "NO_VOICE" in loi_may
                        or "không có giọng" in loi_may):
                    self._log("  Câu %d: không có giọng máy local "
                              "(%s) — giữ im lặng."
                              % (cau["chi_so"], loi_may))
                else:
                    self._log("  Câu %d: giọng máy local cũng lỗi "
                              "(%s) — giữ im lặng."
                              % (cau["chi_so"], loi_may))
                self._dat_trang_thai_cau(
                    cau["chi_so"], "Lỗi: " + (loi or "?")[:60])
                self._log("  -> LỖI câu %d: %s" % (cau["chi_so"], loi))
                return False
            if not ok:
                if self._yeu_cau_huy.is_set():
                    # Huy giua cau dang doc: khong ghi "LỖI câu" nua,
                    # vong lap chinh se dung va bao "Đã hủy".
                    return False
                self._dat_trang_thai_cau(cau["chi_so"], "Lỗi: " + (loi or "?")[:60])
                self._log("  -> LỖI câu %d: %s" % (cau["chi_so"], loi))
                return False
            return _hoan_tat_cau(cau, i, dich, bo_xac_minh, False)

        # (v7.8) LUOT 1 theo don vi: moi don vi la 1 cau (mac dinh)
        # hoac 1 batch toi da N cau lien tiep (o "So cau gop 1 lan
        # goi"). Tuan tu thi xu ly tung don vi mot; goi song song thi
        # N luong worker cung lay don vi tu hang doi.
        def _lap_danh_sach_don_vi():
            """Chia cac cau chua xong thanh don vi (moi don vi toi da N
            cau lien tiep, tong van ban khong qua gioi han 1 lan goi
            Edge TTS). Tra ve list don vi, moi don vi la list [(i,
            cau)] (i = vi tri 1-based trong SRT)."""
            cac_don_vi = []
            don_vi_hien = []
            do_dai_hien = 0
            for i, cau in enumerate(cac_cau, 1):
                if cau["chi_so"] in cau_da_xong:
                    continue
                do_dai_cau = len(cau["text"])
                if don_vi_hien and (
                        len(don_vi_hien) >= so_cau_gop
                        or do_dai_hien + do_dai_cau + 1
                        > DO_DAI_TOI_DA_MOT_LAN_GOP_BATCH):
                    cac_don_vi.append(don_vi_hien)
                    don_vi_hien = []
                    do_dai_hien = 0
                don_vi_hien.append((i, cau))
                do_dai_hien += do_dai_cau + 1
            if don_vi_hien:
                cac_don_vi.append(don_vi_hien)
            return cac_don_vi

        def _doc_batch(don_vi, dung_luong_local=False):
            """(v7.8) Doc 1 batch N cau bang 1 lan goi Edge TTS roi cat
            thanh file rieng tung cau theo WordBoundary. Cau nao cat
            loi / goi batch loi thi ghi vao loi_cau de Luot 2 doc bu le
            tung cau. Neu khong tach duoc ranh gioi cau thi fallback
            doc le tung cau (log ro)."""
            chi_so_dau = don_vi[0][1]["chi_so"]
            chi_so_cuoi = don_vi[-1][1]["chi_so"]
            self._log("Đang đọc batch câu %d-%d (%d câu)..."
                      % (chi_so_dau, chi_so_cuoi, len(don_vi)))
            text_batch = "\n".join(cau["text"] for _i, cau in don_vi)
            batch_file = os.path.join(thu_muc_rieng, "_batch.mp3")
            timeout_batch = min(120 * len(don_vi), 600)
            try:
                ok, bo_xac_minh, ranh_gioi, loi = doc_batch_thanh_mp3(
                    text_batch, voice, toc_do, cao_do, batch_file,
                    log_cb=self._log, ffmpeg=ffmpeg,
                    timeout_giay=timeout_batch, dung=self._yeu_cau_huy)
            except Exception as e:
                ok, bo_xac_minh, ranh_gioi, loi = False, False, [], str(e)
            if self._yeu_cau_huy.is_set():
                # Huy giua luc goi batch: khong ghi loi, vong lap
                # chinh se dung va bao "Đã hủy".
                _xoa_file_quiet(batch_file)
                return
            if not ok:
                self._log("  Batch câu %d-%d lỗi: %s — các câu này sẽ "
                          "đọc bù lẻ ở Lượt 2."
                          % (chi_so_dau, chi_so_cuoi, loi or "?"))
                for _i, cau in don_vi:
                    self._dat_trang_thai_cau(
                        cau["chi_so"], "Lỗi: " + (loi or "?")[:60])
                    _ghi_loi_cau(cau["chi_so"])
                _xoa_file_quiet(batch_file)
                return
            ranh_gioi_cau = _tach_ranh_gioi_cau(
                ranh_gioi, [cau["text"] for _i, cau in don_vi])
            if ranh_gioi_cau is None:
                self._log("  Batch câu %d-%d: không tách được ranh giới "
                          "câu từ WordBoundary, đọc lẻ từng câu..."
                          % (chi_so_dau, chi_so_cuoi))
                _xoa_file_quiet(batch_file)
                for i, cau in don_vi:
                    if self._yeu_cau_huy.is_set():
                        return
                    if self._doi_tam_dung(so_cau_xong, tong):
                        return
                    ket_qua = doc_1_cau(
                        cau, i, dung_luong_local=dung_luong_local)
                    if ket_qua is False:
                        _ghi_loi_cau(cau["chi_so"])
                return
            # (v7.9) Cat tung cau khop duoc tu file batch; cau nao
            # khong khop ranh gioi (None) thi doc le lai rieng cau
            # do, khong bo ca batch nhu ban cu.
            so_cau_lech = sum(1 for x in ranh_gioi_cau if x is None)
            if so_cau_lech:
                self._log("  Batch câu %d-%d: %d/%d câu lệch ranh giới "
                          "WordBoundary, chỉ đọc lẻ lại %d câu đó."
                          % (chi_so_dau, chi_so_cuoi, so_cau_lech,
                             len(don_vi), so_cau_lech))
            for k, (i, cau) in enumerate(don_vi):
                if self._yeu_cau_huy.is_set():
                    break
                if ranh_gioi_cau[k] is None:
                    if self._doi_tam_dung(so_cau_xong, tong):
                        break
                    ket_qua = doc_1_cau(
                        cau, i, dung_luong_local=dung_luong_local)
                    if ket_qua is False:
                        _ghi_loi_cau(cau["chi_so"])
                    continue
                bat_dau, ket_thuc = ranh_gioi_cau[k]
                dich = os.path.join(thu_muc_rieng,
                                    "%03d.mp3" % cau["chi_so"])
                self._tien_trinh(int((i - 1) * 100 / tong),
                                 nhan_pha_long +
                                 "Đang đọc câu %d/%d..." % (i, tong))
                self._dat_trang_thai_cau(cau["chi_so"], "Đang đọc...")
                self._log("Câu %d/%d (%.1fs): %s"
                          % (i, tong,
                             (cau["ket_thuc_ms"] - cau["bat_dau_ms"])
                             / 1000.0, cau["text"][:80]))
                if _cat_mp3_theo_ranh_gioi(batch_file, bat_dau, ket_thuc,
                                           dich, ffmpeg,
                                           dung=self._yeu_cau_huy):
                    _hoan_tat_cau(cau, i, dich, bo_xac_minh, False)
                else:
                    self._dat_trang_thai_cau(
                        cau["chi_so"], "Lỗi: cắt audio batch lỗi")
                    self._log("  -> LỖI câu %d: cắt audio batch lỗi."
                              % cau["chi_so"])
                    _ghi_loi_cau(cau["chi_so"])
            _xoa_file_quiet(batch_file)

        def _xu_ly_don_vi(don_vi, dung_luong_local=False):
            """Xu ly 1 don vi (1 cau hoac 1 batch). Cau loi duoc ghi
            vao loi_cau (khoa chung); cau dua sang luong local thi
            khong ghi loi (luong local se hoan tat hoac ghi loi sau)."""
            if not don_vi:
                return
            if len(don_vi) == 1:
                i, cau = don_vi[0]
                ket_qua = doc_1_cau(cau, i,
                                    dung_luong_local=dung_luong_local)
                if ket_qua is False:
                    _ghi_loi_cau(cau["chi_so"])
                return
            _doc_batch(don_vi, dung_luong_local=dung_luong_local)

        def _chay_luot1_song_song(cac_don_vi, so_luong):
            """(v7.8) Luot 1 goi song song: N luong worker cung lay don
            vi (cau/batch) tu hang doi va doc. File MP3 tung cau luu
            rieng theo chi so cau nen thu tu gop cuoi khong doi. Che do
            'local ngay': cau nao Edge loi thi dua sang 1 luong
            giong-may-local rieng (hang_local), khong chan luong may
            chu. Tra ve (da_huy, cau_dung)."""
            hang_viec = queue.Queue()
            for don_vi in cac_don_vi:
                hang_viec.put(don_vi)
            for _ in range(so_luong):
                hang_viec.put(None)  # linh canh dung luong
            dung_luong_local = (
                che_do_local == "may_chu_local_ngay")
            self._hang_local = (queue.Queue()
                                if dung_luong_local else None)

            def _luong_may_chu():
                while True:
                    if self._yeu_cau_huy.is_set():
                        return
                    try:
                        don_vi = hang_viec.get(timeout=0.2)
                    except queue.Empty:
                        continue
                    try:
                        if don_vi is None:
                            return
                        if self._doi_tam_dung(so_cau_xong, tong):
                            return
                        _xu_ly_don_vi(
                            don_vi, dung_luong_local=dung_luong_local)
                    except Exception as e:
                        # 1 don vi loi bat ngo: ghi loi cac cau trong
                        # don vi de Luot 2 doc bu, khong de chet luong.
                        self._log("LỖI luồng xử lý đơn vị %s: %s"
                                  % ([c["chi_so"] for _i, c in don_vi],
                                     e))
                        for _i, cau in don_vi:
                            _ghi_loi_cau(cau["chi_so"])
                    finally:
                        hang_viec.task_done()

            def _luong_giong_may():
                while True:
                    if self._yeu_cau_huy.is_set():
                        return
                    try:
                        muc = self._hang_local.get(timeout=0.2)
                    except queue.Empty:
                        continue
                    try:
                        if muc is None:
                            return
                        i, cau = muc
                        if self._yeu_cau_huy.is_set():
                            _ghi_loi_cau(cau["chi_so"])
                            continue
                        if self._doi_tam_dung(so_cau_xong, tong):
                            _ghi_loi_cau(cau["chi_so"])
                            continue
                        dich = os.path.join(
                            thu_muc_rieng,
                            "%03d.mp3" % cau["chi_so"])
                        self._tien_trinh(
                            int((i - 1) * 100 / tong),
                            nhan_pha_long +
                            "Đang đọc câu %d/%d (giọng máy)..."
                            % (i, tong))
                        self._dat_trang_thai_cau(
                            cau["chi_so"], "Đang đọc (giọng máy)...")
                        ok_may, loi_may = _doc_local_khoa(cau["text"],
                                                          dich)
                        if self._yeu_cau_huy.is_set():
                            _ghi_loi_cau(cau["chi_so"])
                            continue
                        if ok_may:
                            self._log("  Câu %d: Edge TTS lỗi, đã đọc "
                                      "bù bằng giọng máy local."
                                      % cau["chi_so"])
                            _hoan_tat_cau(cau, i, dich, False, True)
                        else:
                            self._log("  Câu %d: giọng máy local cũng "
                                      "lỗi (%s) — giữ im lặng."
                                      % (cau["chi_so"], loi_may or "?"))
                            self._dat_trang_thai_cau(
                                cau["chi_so"],
                                "Lỗi: giọng máy local lỗi")
                            _ghi_loi_cau(cau["chi_so"])
                    except Exception as e:
                        try:
                            _ghi_loi_cau(muc[1]["chi_so"])
                        except Exception:
                            pass
                        self._log("LỖI luồng giọng máy local: %s" % e)
                    finally:
                        self._hang_local.task_done()

            luong_may_chu = []
            for _ in range(so_luong):
                t = threading.Thread(target=_luong_may_chu, daemon=True)
                t.start()
                luong_may_chu.append(t)
            luong_may = None
            if dung_luong_local:
                luong_may = threading.Thread(target=_luong_giong_may,
                                             daemon=True)
                luong_may.start()
            for t in luong_may_chu:
                t.join()
            if luong_may is not None:
                self._hang_local.put(None)
                luong_may.join()
            self._hang_local = None
            da_huy_ss = self._yeu_cau_huy.is_set()
            cau_dung_ss = 0
            if da_huy_ss:
                with self._khoa_chia_se:
                    xong = set(cau_da_xong)
                for i, cau in enumerate(cac_cau, 1):
                    if cau["chi_so"] not in xong:
                        cau_dung_ss = i
                        break
            return da_huy_ss, cau_dung_ss

        # Luot 1: doc het cac don vi (dung ngay khi bam Huy / tam
        # dung). Cau nao da xong o lan truoc (Tiep tuc) thi khong nam
        # trong danh sach don vi nen khong doc lai.
        cac_don_vi = _lap_danh_sach_don_vi()
        if ts.get("goi_song_song", False):
            so_luong = ts.get("so_luong_song_song", 3)
            try:
                so_luong = int(so_luong)
            except Exception:
                so_luong = 3
            so_luong = max(2, min(20, so_luong))
            self._log("Gọi song song: %d luồng cùng đọc %d đơn vị..."
                      % (so_luong, len(cac_don_vi)))
            da_huy, cau_dung = _chay_luot1_song_song(cac_don_vi, so_luong)
        else:
            for don_vi in cac_don_vi:
                if self._yeu_cau_huy.is_set():
                    da_huy = True
                    cau_dung = don_vi[0][0]
                    break
                # (v7.8) Tam dung: dung sau don vi dang xu ly, khong
                # cat ngang; bam Huy trong luc tam dung thi dung han.
                if self._doi_tam_dung(so_cau_xong, tong):
                    da_huy = True
                    cau_dung = don_vi[0][0]
                    break
                _xu_ly_don_vi(don_vi)
        # Luot 2: cau nao loi thi THU LAI 1 lan nua (loi mang thoang qua),
        # ghi ro ket qua tung cau, khong lang le bo qua. Bo qua neu da huy.
        # (v7.8) Che do may chu/local (ts["che_do_may_chu_local"]) quyet
        # dinh cau loi co duoc doc bu bang giong may local hay khong
        # (doc_1_cau tu xu ly theo che do, ke ca o Luot 2 / gop bu).
        if loi_cau and not da_huy:
            self._log("Thử lại %d câu lỗi%s: %s"
                      % (len(loi_cau),
                         " (câu nào Edge vẫn lỗi sẽ đọc bằng giọng máy "
                         "local)" if che_do_local == "may_chu_local_ngay"
                         else "",
                         sorted(loi_cau)))
            for i, cau in enumerate(cac_cau, 1):
                if self._yeu_cau_huy.is_set():
                    da_huy = True
                    cau_dung = i
                    break
                # (v7.8) Tam dung giua cac cau thu lai.
                if self._doi_tam_dung(so_cau_xong, tong):
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
        # (v7.8) Co ghi nho gop cuoi da xong chua: doc xong het cau
        # nhung gop chua xong (bi huy/loi khi gop) thi van luu tien
        # trinh de 'Tiep tuc' gop lai, khong xoa nhu truoc.
        gop_da_xong = False
        if can_gop and gop is not None and gop.so_cau > 0:
            self._log("Đang hoàn tất file lồng tiếng: %s" % dich_gop)
            try:
                ok_gop, tong_ms_gop = gop.hoan_tat(
                    ffmpeg, dung=self._yeu_cau_huy)
                if ok_gop:
                    gop_da_xong = True
                    self.file_gop = dich_gop
                    if gop.che_do_tran == "de" and gop.de_slot > 0:
                        self._log("XONG file gộp: %s (dài %.1fs, %d câu "
                                  "tràn đã đè nhỏ dưới câu sau, %d câu lỗi "
                                  "đã bỏ qua)"
                                  % (dich_gop, tong_ms_gop / 1000.0,
                                     gop.de_slot, gop.bo_qua))
                    else:
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
        # (v7.8) VONG GOP BU — toi da 1 vong cho 1 lan xuat: sau khi
        # gop xong ma van con cau loi thi doi cho may chu het chan
        # 429 roi goi lai CHI cau loi, gop lai file cuoi (cau ngon giu
        # nguyen file MP3 rieng, khong doc lai). Gop bu loi thi giu
        # nguyen file gop cu. Khong chay khi che do "Từng câu riêng"
        # (khong co file gop de bu) hay khi cong tac da TAT, hay khi
        # da huy truoc do.
        if (can_gop and gop is not None and loi_cau and not da_huy
                and ts.get("gop_bu", True)):
            doi_giay = ts.get("gop_bu_doi_giay", 60)
            try:
                doi_giay = int(doi_giay)
            except Exception:
                doi_giay = 60
            doi_giay = max(0, min(600, doi_giay))
            self._log("Còn %d câu lỗi: %s. Đợi %ds cho máy chủ hết chặn "
                      "rồi gọi lại chỉ các câu lỗi..."
                      % (len(loi_cau), sorted(loi_cau), doi_giay))
            # Doi co the huy: chia nho tung 0.5s, hien dem nguoc tren
            # thanh trang thai de CYAN biet tool dang doi chu khong treo.
            huy_trong_luc_doi = False
            con_lai = float(doi_giay)
            while con_lai > 0:
                if self._yeu_cau_huy.is_set():
                    huy_trong_luc_doi = True
                    break
                # (v7.8) Tam dung trong luc doi: dung doi, khong tru
                # thoi gian doi; Huy trong luc tam dung thi dung han.
                if self._yeu_cau_tam_dung.is_set():
                    if self._doi_tam_dung(so_cau_xong, tong):
                        huy_trong_luc_doi = True
                        break
                self._tien_trinh(100, "Đang đợi %ds để gọi lại câu lỗi..."
                                 % int(con_lai + 0.5))
                time.sleep(min(0.5, con_lai))
                con_lai -= 0.5
            if huy_trong_luc_doi:
                self._log("Đã hủy trong lúc đợi gọi lại câu lỗi — giữ "
                          "nguyên file gộp đã có, không gộp bù nữa.")
            else:
                vi_tri = {c["chi_so"]: idx + 1
                          for idx, c in enumerate(cac_cau)}
                con_loi_bu = sorted(loi_cau)
                da_bu_duoc = 0
                huy_trong_luc_bu = False
                for j, chi_so in enumerate(con_loi_bu, 1):
                    if self._yeu_cau_huy.is_set():
                        huy_trong_luc_bu = True
                        self._log("Đã hủy trong lúc gọi lại câu lỗi — "
                                  "giữ nguyên file gộp đã có, không gộp "
                                  "bù nữa.")
                        break
                    # (v7.8) Tam dung giua cac cau goi lai.
                    if self._doi_tam_dung(so_cau_xong, tong):
                        huy_trong_luc_bu = True
                        self._log("Đã hủy trong lúc gọi lại câu lỗi — "
                                  "giữ nguyên file gộp đã có, không gộp "
                                  "bù nữa.")
                        break
                    cau_bu = next((c for c in cac_cau
                                   if c["chi_so"] == chi_so), None)
                    if cau_bu is None:
                        continue
                    self._tien_trinh(
                        int((j - 1) * 100 / max(1, len(con_loi_bu))),
                        "Đang gọi lại câu lỗi %d/%d (câu %d)..."
                        % (j, len(con_loi_bu), chi_so))
                    self._log("Gọi lại câu lỗi %d (%d/%d)..."
                              % (chi_so, j, len(con_loi_bu)))
                    if doc_1_cau(cau_bu, vi_tri[chi_so]):
                        del loi_cau[chi_so]
                        da_bu_duoc += 1
                        self._log("  -> Câu %d đọc bù THÀNH CÔNG."
                                  % chi_so)
                    else:
                        self._log("  -> Câu %d vẫn lỗi sau khi gọi lại "
                                  "(gộp bù)." % chi_so)
                if da_bu_duoc > 0 and not huy_trong_luc_bu \
                        and not self._yeu_cau_huy.is_set():
                    # Sao luu file gop cu truoc khi gop lai: _gop_mp3_
                    # concat ghi de truc tiep len file dich nen gop bu
                    # loi co the lam hong file cu — co ban sao de khoi
                    # phuc thi moi dam gop lai.
                    ban_sao = None
                    if dich_gop and os.path.isfile(dich_gop):
                        ban_sao = dich_gop + ".cu"
                        try:
                            shutil.copyfile(dich_gop, ban_sao)
                        except OSError:
                            ban_sao = None
                    self._tien_trinh(100, "Đang gộp bù...")
                    self._log("Đang gộp bù %d câu vừa đọc được vào file "
                              "lồng tiếng..." % da_bu_duoc)
                    try:
                        ok_bu, tong_ms_bu = gop.hoan_tat(
                            ffmpeg, dung=self._yeu_cau_huy)
                    except Exception as e:
                        ok_bu, tong_ms_bu = False, 0
                        _ghi_log_loi_ffmpeg(thu_muc, traceback.format_exc())
                        self._log("LỖI gộp bù: %s" % _tom_tat_loi(e))
                    if ok_bu:
                        gop_da_xong = True
                        tong_ms_gop = tong_ms_bu
                        self.file_gop = dich_gop
                        if ban_sao:
                            _xoa_file_quiet(ban_sao)
                        if loi_cau:
                            self._log("Đã gộp bù: còn %d câu lỗi chưa "
                                      "đọc được: %s"
                                      % (len(loi_cau), sorted(loi_cau)))
                        else:
                            self._log("Đã gộp bù đủ hết, không còn câu "
                                      "lỗi.")
                    else:
                        if ban_sao and os.path.isfile(ban_sao):
                            try:
                                shutil.copyfile(ban_sao, dich_gop)
                                _xoa_file_quiet(ban_sao)
                            except OSError:
                                pass
                        self._log("LỖI gộp bù (xem chi tiết trong file "
                                  "ffmpeg-loi.log ở thư mục kết quả) — "
                                  "giữ nguyên file gộp cũ.")
                        _ghi_log_loi_ffmpeg(thu_muc, "gop_bu tra ve False")
                elif da_bu_duoc == 0 and not huy_trong_luc_bu:
                    self._log("Không câu lỗi nào đọc bù được — giữ "
                              "nguyên file gộp cũ.")
                so_xong = so_cau_xong
                self._tien_trinh(100, "Đã gộp bù xong: %d/%d câu."
                                 % (so_xong, tong))
        # (v7.18) TRON NHAC NEN KHI DOC — 1 lan tron duy nhat sau buoc
        # gop cuoi (ca gop bu, neu co): file voice MP3 + nhac nen
        # (amix, khong sidechain) ra file <ten>_voice-nen.mp3. Tron o
        # cuoi cho ket qua nghe giong het tron tung cau (amix tuyen
        # tinh) nhung chi encode 1 lan nen nhanh hon va it suy hao hon
        # — day chinh la "tao giong den dau chen xu ly luon o do" o
        # muc luot chay, khong can qua tab khac. Chi chay khi cong tac
        # BAT, file gop da xong, khong bi huy; che do "Tung cau rieng"
        # (khong co file gop) thi khong tron.
        file_voice_nen = None
        loi_tron = None
        if co_tron_nhac_sau_gop(can_gop, gop_da_xong, da_huy, ts):
            file_voice_nen, loi_tron = self._tron_nhac_sau_gop(
                ts, dich_gop, thu_muc, ffmpeg)
        # v1.3 - LUU/XOA tien trinh: con cau chua xong (huy giua chung
        # hoac loi) thi luu de bam 'Tiep tuc' doc not; (v7.8) doc xong
        # het cau nhung gop chua xong (bi huy/loi khi gop) thi VAN luu
        # de 'Tiep tuc' gop lai; xong tron ven 100% (ca gop) thi xoa.
        # Tien trinh da luu lien tuc sau moi cau xong nen o day chi luu
        # lai 1 lan cho chac (cung 1 ham _luu_tien_trinh_ngay).
        gop_chua_xong = (can_gop and so_xong >= tong
                         and not gop_da_xong)
        if (0 < so_xong < tong) or gop_chua_xong:
            if _luu_tien_trinh_ngay():
                if gop_chua_xong:
                    self._log("Đã lưu tiến trình (đã xong %d/%d câu, "
                              "file gộp chưa xong) - bấm 'Tiếp tục' để "
                              "gộp lại." % (so_xong, tong))
                else:
                    self._log("Đã lưu tiến trình (xong %d/%d câu) - bấm "
                              "'Tiếp tục' để đọc nốt các câu còn lại."
                              % (so_xong, tong))
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
            # (v7.18) Them thong tin file voice + nhac nen (neu co) /
            # loi tron (neu co) vao ket qua — file voice goc van giu.
            if file_voice_nen and os.path.isfile(file_voice_nen):
                ket_qua += ("\nFile voice + nhạc nền:\n%s"
                            % file_voice_nen)
            elif loi_tron:
                ket_qua += ("\n(Trộn nhạc nền lỗi: %s — file voice vẫn "
                            "giữ nguyên.)" % loi_tron)
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
        self._ham_luu_tien_trinh = None
        self.hang_doi.put(("xong",))

# =====================================================================
# (v7.13) VOICE FOR YOUTUBE FACELESS — ham thuan (khong tkinter),
# de test duoc ma khong can Edge TTS / mang / Windows.
# Format CHINH: DUAL JSON {en:{...}, vi:{...}}; fallback: JSON 1 ngon
# ngu {language, voice_settings, script_text, srt_cues} hoac bare
# srt_cues array, hoac file .srt.
# QUAN TRONG (CYAN 20/11): EN va VI la 2 kich ban DOC LAP, chi chung
# 1 key/chu de. Moi ban co script_text, srt_cues, thoi luong, chuong
# rieng, viet theo phong cach/nhip ke rieng cho khan gia tung nuoc.
# KHONG ep vi la ban dich tung cau cua en, KHONG ep timing 2 ban
# giong nhau. Tab xu ly tung ban doc lap, xuat file rieng tung ngon ngu.
# =====================================================================

YTF_TOC_DO_TOI_DA = 1.35
YTF_TOC_DO_MAC_DINH = 1.0
YTF_NGHI_GIUA_CUE_MS_MAC_DINH = 350

# (v7.14) CHE DO SONG SONG EN+VI — ham thuan, khong tkinter.
# Mac dinh TAT (tuan tu, an toan nhat). BAT: EN va VI la 2 job doc lap.
YTF_SONG_SONG_MAC_DINH = False
YTF_CHO_DUNG_GIONG_MAY_MAC_DINH = False  # (v7.16) local SAPI: mac dinh TAT
YTF_DONG_BO_TOI_DA_MAC_DINH = 2
YTF_SONG_SONG_TRE_VI_GIAY = 2.0  # VI lech 2s khi bat dong thoi (giam Edge rate-limit)


def ytf_tao_job(ngon_ngu):
    """Trang thai 1 job doc lap cho 1 ngon ngu. Khong dung chung
    state voi ngon ngu kia: dung/huy/loi 1 ben khong anh huong ben kia."""
    return {"language": ngon_ngu, "status": "cho", "tien_do": 0,
            "cue_hien_tai": 0, "tong_cue": 0, "loi": None,
            "da_xong": False, "da_huy": False, "files": {},
            # (v7.16) Danh sach cue Edge loi chua doc xong + cue da
            # doc bang giong may local (ghi ro de anh kiem tra lai).
            "chua_xu_ly": [], "so_cue_thanh_cong": 0, "da_dung_local": []}


def ytf_dung_job(job, ly_do="da_huy"):
    """Danh dau 1 job dung/huy. Chi tac dong job nay, khong cham job kia."""
    job["da_huy"] = True
    job["status"] = ly_do
    return job


def ytf_cap_nhat_tien_do(job, cue_hien_tai, tong_cue):
    job["cue_hien_tai"] = int(cue_hien_tai)
    job["tong_cue"] = int(tong_cue)
    job["tien_do"] = int(round(100.0 * cue_hien_tai / tong_cue)) if tong_cue else 0
    job["status"] = "dang_chay"
    return job


def ytf_job_con_chay(job):
    return job.get("status") == "dang_chay" and not job.get("da_huy")


def ytf_duong_ra_theo_ngon_ngu(thu_muc, slug, ngon_ngu):
    """Duong ra RIENG tung ngon ngu: thu muc tam rieng (tam_en/tam_vi)
    de 2 luong song song khong ghi de file cue cua nhau; file ra rieng
    <slug>_<lang>.mp3/.srt/.txt trong thu muc <slug>/ chung."""
    thu_muc_lang = os.path.join(thu_muc, slug)
    return {"thu_muc_lang": thu_muc_lang,
            "thu_muc_tam": os.path.join(thu_muc_lang, "tam_" + ngon_ngu),
            "mp3": os.path.join(thu_muc_lang, "%s_%s.mp3" % (slug, ngon_ngu)),
            "srt": os.path.join(thu_muc_lang, "%s_%s_final.srt" % (slug, ngon_ngu)),
            "txt": os.path.join(thu_muc_lang, "%s_%s.txt" % (slug, ngon_ngu))}


def ytf_ke_hoach_chay(cac_ngon_ngu, song_song, dong_bo_toi_da=2):
    """Ke hoach chay theo cong tac song song. Tra {"che_do", "luong"}:
    - TAT: {"che_do": "tuan_tu", "luong": [["en"], ["vi"]]} — chay lan
      luot, doi luong truoc xong moi chay luong sau.
    - BAT, toi_da>=2: {"che_do": "song_song", "luong": [["en", "vi"]]}
      — 1 dot, ca 2 cung chay, doc lap.
    - BAT, toi_da==1: {"che_do": "song_song", "luong": [["en"], ["vi"]]}
      — van 2 job doc lap, nhung chi 1 luong chay tai 1 thoi diem
      (semaphore), dung/huy 1 ben van khong anh huong ben kia.
    Moi luong trong "luong" la 1 dot bat dong thoi; cac dot chay tuan tu."""
    langs = [l for l in ("en", "vi") if l in (cac_ngon_ngu or [])]
    try:
        toi_da = int(dong_bo_toi_da)
    except Exception:
        toi_da = 2
    toi_da = 1 if toi_da < 1 else (2 if toi_da > 2 else toi_da)
    if not song_song or not langs:
        return {"che_do": "tuan_tu", "luong": [[l] for l in langs]}
    if toi_da >= 2:
        return {"che_do": "song_song", "luong": [langs]}
    return {"che_do": "song_song", "luong": [[l] for l in langs]}


# (v7.15) JSON TU NHAN MODE — ham thuan, khong tkinter.
# Tool doc JSON va TU BIET lam tieng Anh thoi, tieng Viet thoi hay
# ca hai; TU BAT/TAT cot tuong ung. Khong tick ngon ngu bang tay.
# Thu tu uu tien: truong "mode" > "languages" > "choice" > suy ra
# tu khoa en/vi co trong JSON. Mode trong JSON thang khoa phu.
def ytf_chuan_hoa_mode(data):
    """Tra {"mode", "languages", "nguon", "canh_bao"}.
    mode: "dual" | "en_only" | "vi_only". languages: ["en","vi"] /
    ["en"] / ["vi"] (theo thu tu en, vi)."""
    canh_bao = []
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            return {"mode": "en_only", "languages": ["en"], "nguon": "mac_dinh_en",
                    "canh_bao": ["Không parse được JSON — mặc định chỉ EN."]}
    if not isinstance(data, dict):
        return {"mode": "en_only", "languages": ["en"], "nguon": "mac_dinh_en",
                "canh_bao": ["JSON không phải object — mặc định chỉ EN."]}
    co_en = "en" in data and isinstance(data.get("en"), dict)
    co_vi = "vi" in data and isinstance(data.get("vi"), dict)
    # 1 ngon ngu don (khong co khoa en/vi): suy ra tu "language".
    if not co_en and not co_vi:
        lang = str(data.get("language") or "en").lower()[:2]
        lang = lang if lang in ("en", "vi") else "en"
        return {"mode": "en_only" if lang == "en" else "vi_only",
                "languages": [lang], "nguon": "suy_ra_tu_language",
                "canh_bao": []}
    suy_ra = ["en", "vi"] if (co_en and co_vi) else (["en"] if co_en else ["vi"])
    # Truong mode / languages / choice (uu tien theo thu tu nay).
    raw = data.get("mode") or data.get("choice") or ""
    raw = str(raw).strip().lower().replace(" ", "").replace("-", "_")
    langs_raw = data.get("languages")
    mode, nguon = None, None
    bang = {"dual": "dual", "both": "dual", "song_ngu": "dual",
            "songngu": "dual", "en+vi": "dual", "en,vi": "dual",
            "all": "dual", "en_only": "en_only", "en": "en_only",
            "english": "en_only", "vi_only": "vi_only", "vi": "vi_only",
            "vietnamese": "vi_only", "vn": "vi_only"}
    if raw in bang:
        mode, nguon = bang[raw], "truong_mode"
    elif isinstance(langs_raw, (list, tuple)):
        ls = [str(x).strip().lower()[:2] for x in langs_raw]
        ls = [l for l in ("en", "vi") if l in ls]
        if ls:
            mode = "dual" if len(ls) == 2 else ("en_only" if ls == ["en"] else "vi_only")
            nguon = "truong_languages"
    if mode is None:
        mode = "dual" if len(suy_ra) == 2 else ("en_only" if suy_ra == ["en"] else "vi_only")
        nguon = "suy_ra_tu_khoa_en_vi"
    langs = {"dual": ["en", "vi"], "en_only": ["en"], "vi_only": ["vi"]}[mode]
    # Xung dot mode vs khoa co that: mode thang, log canh bao, KHONG
    # tu tao ban thieu (dual ma chi co 1 ban thi chay ban co that).
    for l in langs:
        if l not in suy_ra:
            canh_bao.append("JSON nói %s nhưng thiếu bản %s — chỉ chạy bản có thật, không tự tạo bản thiếu." % (mode, l.upper()))
    for l in suy_ra:
        if l not in langs:
            canh_bao.append("JSON có bản %s nhưng mode=%s — bỏ qua bản %s, làm theo mode." % (l.upper(), mode, l.upper()))
    return {"mode": mode, "languages": [l for l in langs if l in suy_ra],
            "nguon": nguon, "canh_bao": canh_bao}


def ytf_cot_duoc_bat(du_lieu, meta):
    """Cot nao duoc BAT (cho chay) theo mode JSON + du lieu co that.
    Tra list con cua ["en", "vi"]. Vi du: mode en_only -> ["en"]
    du song song co BAT; dual day du -> ["en", "vi"]."""
    if not du_lieu:
        return []
    muon = (meta or {}).get("languages") or list(du_lieu.keys())
    return [l for l in ("en", "vi") if l in muon and l in du_lieu]


# Giong Edge TTS that (chay tren Windows). Ten hien thi -> voice_id.
YTF_GIONG_EDGE = {
    "en": {
        "Christopher (nam, Mỹ)": "en-US-ChristopherNeural",
        "Aria (nữ, Mỹ)": "en-US-AriaNeural",
        "Guy (nam, Mỹ)": "en-US-GuyNeural",
        "Jenny (nữ, Mỹ)": "en-US-JennyNeural",
        "Eric (nam, Mỹ)": "en-US-EricNeural",
        "Helio (nam, Mỹ)": "en-US-ChristopherNeural",
    },
    "vi": {
        "HoaiMy (nữ)": "vi-VN-HoaiMyNeural",
        "NamMinh (nam)": "vi-VN-NamMinhNeural",
        # (v7.24) VieNeu: 25 preset (SDK 3.8.5) them o ngay duoi
        # bang VIENEU_PRESET; id "vieneu:..." la co engine rieng,
        # khong phai Edge voice id.
    },
}
# (v7.24) VieNeu: them 25 preset vao cot VI cua tab Voice Faceless
# (ca v1 + v2 deu lay values tu ytf_giong_theo_ngon_ngu("vi")).
YTF_GIONG_EDGE["vi"].update({ten: "vieneu:" + slug
                             for ten, slug in VIENEU_PRESET.items()})
# Giong Muse noi bo (chi co trong chat Muse, KHONG chay native tren
# Windows): voice_id Muse -> voice Edge tuong duong de anh xa.
YTF_GIONG_MUSE = {
    "avocado_v2:MAI_03": ("Helio (nam, Mỹ)", "en-US-ChristopherNeural"),
    "avocado_v2:MAI_01": ("Aria (nữ, Mỹ)", "en-US-AriaNeural"),
}
YTF_GIONG_MAC_DINH = {"en": "Helio (nam, Mỹ)", "vi": "Xuân Vĩnh (VieNeu, nam Bắc)"}


def ytf_giong_theo_ngon_ngu(ngon_ngu):
    """Danh sach ten giong hien thi cho ngon ngu 'en'/'vi'."""
    return list(YTF_GIONG_EDGE.get(ngon_ngu, YTF_GIONG_EDGE["en"]).keys())


def ytf_anh_xa_giong_muse(voice_id):
    """Anh xa giong Muse -> Edge. Tra (ten_hien_thi, edge_id, la_giong_muse).

    Helio/Aria cua Muse KHONG chay native tren Windows: tab dung Edge
    tuong duong va PHai log ro viec anh xa nay. Audio Helio day du chi
    tao duoc trong chat Muse, khong phai trong file exe nay.
    """
    if voice_id in YTF_GIONG_MUSE:
        ten, edge = YTF_GIONG_MUSE[voice_id]
        return ten, edge, True
    for lang, ds in YTF_GIONG_EDGE.items():
        for ten, vid in ds.items():
            if vid == voice_id:
                return ten, vid, False
    return None, voice_id, False


def ytf_giong_id_cua_ten(ten, ngon_ngu):
    """Ten hien thi -> voice_id Edge (da anh xa Helio->Christopher)."""
    ds = YTF_GIONG_EDGE.get(ngon_ngu, YTF_GIONG_EDGE["en"])
    if ten in ds:
        return ds[ten]
    ten_muse, edge, _ = ytf_anh_xa_giong_muse(ten)
    if edge:
        return edge
    return YTF_GIONG_EDGE[ngon_ngu]["Christopher (nam, Mỹ)"] if ngon_ngu == "en" else YTF_GIONG_EDGE["vi"]["HoaiMy (nữ)"]


def ytf_slug_hoa(text):
    """Ten file an toan: bo dau/khoang trang/ky tu cam Windows."""
    import unicodedata
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^A-Za-z0-9\-_]+", "-", text).strip("-").lower()
    return text[:80] or "video"


def ytf_uoc_tinh_thoi_luong_giay(text, ngon_ngu):
    """Uoc tinh (GHI RO LA UOC TINH): EN ~150 tu/phut,
    VI ~170 tieng/phut. Tra ve so giay (float)."""
    if not text:
        return 0.0
    tu = len(text.split())
    if ngon_ngu == "vi":
        return tu / 170.0 * 60.0
    return tu / 150.0 * 60.0


def ytf_chia_cau_tu_script(script_text, ngon_ngu):
    """Tach script lien mach thanh cue theo cau (fallback khi JSON
    khong co srt_cues). Moi cue 1-2 cau, uoc tinh start/end theo toc
    do doc. Tra list {index, start, end, text} (giay, float)."""
    import re as _re
    text = (script_text or "").strip()
    if not text:
        return []
    cau = [c.strip() for c in _re.split(r"(?<=[.!?])\s+", text) if c.strip()]
    cues, t = [], 0.0
    for i, c in enumerate(cau, 1):
        d = ytf_uoc_tinh_thoi_luong_giay(c, ngon_ngu)
        d = max(d, 0.8)
        cues.append({"index": i, "start": round(t, 3), "end": round(t + d, 3), "text": c, "speaker": "A", "character": "", "gender": None})
        t += d + 0.35
    return cues


def ytf_chuan_hoa_speaker(v):
    """(v7.15, doi thoai Q&A) Chuan hoa speaker cua 1 cue ve "A"/"B".
    Chap nhan: "A"/"B", 1/2, "host"/"guest", "ask"/"answer", "q"/"a".
    Khong co / khong hieu -> "A" (giong chinh)."""
    if v is None:
        return "A"
    t = str(v).strip().lower()
    if t in ("b", "2", "guest", "answer", "a2", "tra_loi", "nguoi_tra_loi"):
        return "B"
    return "A"


def ytf_giong_cua_speaker(ban, speaker):
    """(v7.15, doi thoai; v7.16: GIOI TINH thang mac dinh) Voice_id
    cho speaker cua 1 cue. Thu tu: voice_id ghi ro trong JSON cho
    speaker do -> giong mac dinh theo GIOI TINH cua speaker do
    (nu: EN Aria / VI HoaiMy; nam: EN Christopher / VI NamMinh)
    -> mac dinh cu (EN A=Helio, B=Aria; VI A=HoaiMy, B=NamMinh).
    Vi du co gai hoi (A nu) / chang trai dap (B nam) thi A dung
    giong nu, B dung giong nam, du mac dinh cu la A nam / B nu.
    Tra (voice_id_dung, edge_id, la_giong_muse)."""
    info = ytf_speaker_info(ban, speaker)
    vid = str(info.get("voice_id") or "")
    if not vid:
        vid = ytf_giong_mac_dinh_theo_gioi_tinh(
            ban.get("language") or "en", info.get("gender"))
        if not vid:
            lang = ban.get("language") or "en"
            vid = ("avocado_v2:MAI_03" if (lang == "en" and speaker == "A")
                   else "en-US-AriaNeural" if lang == "en"
                   else "vi-VN-HoaiMyNeural" if speaker == "A"
                   else "vi-VN-NamMinhNeural")
    ten, edge, la_muse = ytf_anh_xa_giong_muse(vid)
    return (edge if la_muse else vid), edge, la_muse


# (v7.16) DOI THOAI CO GIOI TINH + DANH SACH "GIONG CHUA XU LY".
# Gioi tinh cua voice_id da biet (Edge + Muse). Gioi tinh trong JSON
# thang mac dinh: co gai hoi (A nu) / chang trai dap (B nam) thi A
# dung giong nu, B dung giong nam — khong ep theo mac dinh cu.
YTF_GIONG_GIOI_TINH = {
    "en-US-AriaNeural": "female", "en-US-JennyNeural": "female",
    "avocado_v2:MAI_01": "female",
    "en-US-ChristopherNeural": "male", "en-US-GuyNeural": "male",
    "en-US-EricNeural": "male", "avocado_v2:MAI_03": "male",
    "vi-VN-HoaiMyNeural": "female", "vi-VN-NamMinhNeural": "male",
}
# (v7.24) Gioi tinh cua 25 preset VieNeu (de doi thoai chon giong
# theo gioi tinh nhan vat).
YTF_GIONG_GIOI_TINH.update({
    "vieneu:" + slug: ("male" if gioi == "nam" else "female")
    for _ten, _cd, slug, gioi in VIENEU_GIONG_BANG
})
YTF_GIONG_MAC_DINH_THEO_GIOI_TINH = {
    "en": {"female": "en-US-AriaNeural", "male": "en-US-ChristopherNeural"},
    "vi": {"female": "vi-VN-HoaiMyNeural", "male": "vi-VN-NamMinhNeural"},
}


def ytf_chuan_hoa_gioi_tinh(v):
    """Chuan hoa gioi tinh ve "female"/"male"/None. Chap nhan:
    "female"/"male", "nu"/"nam", "F"/"M", "f"/"m", "woman"/"man",
    "girl"/"boy", "co gai"/"chang trai". Khong hieu -> None."""
    if v is None:
        return None
    t = str(v).strip().lower()
    if t in ("female", "nu", "nữ", "f", "woman", "girl", "co gai", "cô gái",
             "co_gai", "nu_gioi"):
        return "female"
    if t in ("male", "nam", "m", "man", "boy", "chang trai", "chàng trai",
             "changtrai", "nam_gioi"):
        return "male"
    return None


def ytf_gioi_tinh_cua_giong(voice_id):
    """Gioi tinh cua 1 voice_id da biet, None neu khong biet."""
    if not voice_id:
        return None
    return YTF_GIONG_GIOI_TINH.get(str(voice_id).strip())


def ytf_giong_mac_dinh_theo_gioi_tinh(ngon_ngu, gioi_tinh):
    """Giong mac dinh theo gioi tinh: nu -> EN Aria / VI HoaiMy;
    nam -> EN Christopher / VI NamMinh. Khong co gioi tinh -> ""."""
    if not gioi_tinh:
        return ""
    return YTF_GIONG_MAC_DINH_THEO_GIOI_TINH.get(ngon_ngu, {}).get(gioi_tinh, "")


def ytf_ten_giong_cua_id(voice_id, ngon_ngu):
    """voice_id -> ten hien thi trong dropdown cua ngon ngu do
    (de tool tu chon dung o combobox khi JSON chi ghi gioi tinh).
    Tra None neu khong co trong danh sach."""
    if not voice_id:
        return None
    vid = str(voice_id).strip()
    ten, _edge, _m = ytf_anh_xa_giong_muse(vid)
    if ten:
        return ten
    for _ten, _vid in YTF_GIONG_EDGE.get(ngon_ngu, {}).items():
        if _vid == vid:
            return _ten
    return None


def ytf_speaker_info(ban, speaker):
    """Thong tin 1 speaker trong 1 ban: {speaker, character, gender,
    voice_id, voice_name}. Nguon (theo thu tu): speakers[speaker],
    characters[speaker], voice_settings_b (B) / voice_settings (A),
    character/gender cap ban. Khong co thi character "" / gender None
    / voice_id "" — ham goi se tu chon mac dinh theo gioi tinh."""
    sp = ytf_chuan_hoa_speaker(speaker)
    ban = ban or {}
    nguon = {}
    sp_dict = ban.get("speakers") or {}
    if isinstance(sp_dict.get(sp), dict):
        nguon.update(sp_dict[sp])
    chars = ban.get("characters") or ban.get("nhan_vat") or {}
    if isinstance(chars, dict):
        if isinstance(chars.get(sp), dict):
            nguon.update(chars[sp])
        elif isinstance(chars.get(sp), str):
            nguon.setdefault("character", chars[sp])
    vs = ban.get("voice_settings_b") if sp == "B" else ban.get("voice_settings")
    if isinstance(vs, dict):
        for k in ("voice_id", "voice_name", "character", "gender"):
            if vs.get(k):
                nguon.setdefault(k, vs[k])
    if sp == "A" and ban.get("character"):
        nguon.setdefault("character", ban["character"])
    if ban.get("gender"):
        nguon.setdefault("gender", ban["gender"])
    return {"speaker": sp,
            "character": str(nguon.get("character") or nguon.get("ten_nhan_vat") or ""),
            "gender": ytf_chuan_hoa_gioi_tinh(nguon.get("gender")),
            "voice_id": str(nguon.get("voice_id") or ""),
            "voice_name": str(nguon.get("voice_name") or "")}


def ytf_chuan_hoa_voice_mode(data, phien_ban=None):
    """Chuan hoa "voice_mode" cap cao nhat cua JSON: "single" (1 giong)
    | "dialogue" (2 giong). Thu tu: truong "voice_mode" >
    "voice_count"/"so_giong" > suy ra tu cue co speaker B / co
    voice_settings_b. Tra {"voice_mode", "nguon", "canh_bao"}."""
    if isinstance(data, dict):
        raw = str(data.get("voice_mode") or data.get("voice") or
                  data.get("kieu_giong") or "").strip().lower().replace(" ", "").replace("-", "_")
        bang = {"single": "single", "1": "single", "1_giong": "single",
                "mot_giong": "single", "monologue": "single", "don_giong": "single",
                "dialogue": "dialogue", "2": "dialogue", "2_giong": "dialogue",
                "doi_thoai": "dialogue", "doithoai": "dialogue",
                "qa": "dialogue", "q_a": "dialogue", "hai_giong": "dialogue"}
        if raw in bang:
            return {"voice_mode": bang[raw], "nguon": "truong_voice_mode", "canh_bao": []}
        for k in ("voice_count", "so_giong", "num_voices"):
            try:
                n = int(data.get(k))
                if n in (1, 2):
                    return {"voice_mode": "single" if n == 1 else "dialogue",
                            "nguon": "truong_" + k, "canh_bao": []}
            except Exception:
                pass
    bans = {}
    if isinstance(phien_ban, dict):
        bans.update(phien_ban)
    if isinstance(data, dict):
        for l in ("en", "vi"):
            b = data.get(l)
            if isinstance(b, dict):
                bans.setdefault(l, b)
    co_b = False
    for b in (bans or {}).values():
        if not isinstance(b, dict):
            continue
        for c in (b.get("srt_cues") or b.get("cues") or []):
            if isinstance(c, dict) and ytf_chuan_hoa_speaker(c.get("speaker")) == "B":
                co_b = True
        sp = b.get("speakers") or {}
        if isinstance(sp, dict) and isinstance(sp.get("B"), dict) and sp["B"].get("voice_id"):
            co_b = True
        if isinstance(b.get("voice_settings_b"), dict) and b["voice_settings_b"].get("voice_id"):
            co_b = True
    return {"voice_mode": "dialogue" if co_b else "single",
            "nguon": "suy_ra_tu_cue_co_speaker_B" if co_b else "mac_dinh_single",
            "canh_bao": []}


def ytf_kiem_tra_gioi_tinh_giong(ban, speaker):
    """Kiem tra gioi tinh nhan vat co khop giong da chon khong.
    Tra (ok, canh_bao, gender, voice_gender). Khong khop -> canh
    bao, KHONG tu doi giong: tool giu dung giong trong JSON."""
    info = ytf_speaker_info(ban, speaker)
    gender = info.get("gender")
    vg = ytf_gioi_tinh_cua_giong(info.get("voice_id")) if info.get("voice_id") else None
    if gender and vg and gender != vg:
        return (False,
                "Speaker %s là %s (%s) nhưng voice %s là giọng %s — "
                "tool giữ đúng giọng trong JSON, không tự đổi. Kiểm tra "
                "lại JSON nếu muốn đổi giọng." % (
                    speaker, "nữ" if gender == "female" else "nam",
                    info.get("character") or "?",
                    info.get("voice_id"), "nữ" if vg == "female" else "nam"),
                gender, vg)
    return (True, None, gender, vg)


def ytf_tao_chua_xu_ly():
    """Danh sach "Giong chua xu ly" rong (1 list rieng tung cot)."""
    return []


def ytf_them_chua_xu_ly(ds, cue, lang, loi, da_dung_local=False):
    """Them 1 cue loi vao danh sach chua xu ly (ghi ro speaker /
    nhan vat / gioi tinh / loi / so lan thu). Cue da co thi chi
    cap nhat loi + tang so lan thu, KHONG them trung. Tra ds."""
    ds = ds if isinstance(ds, list) else []
    idx = int((cue or {}).get("index") or 0)
    for it in ds:
        if it.get("index") == idx:
            it["loi"] = str(loi or "")
            it["lan_thu"] = int(it.get("lan_thu") or 1) + 1
            it["da_dung_local"] = bool(da_dung_local or it.get("da_dung_local"))
            return ds
    ds.append({"index": idx, "speaker": ytf_chuan_hoa_speaker((cue or {}).get("speaker")),
               "character": str((cue or {}).get("character") or ""),
               "gender": ytf_chuan_hoa_gioi_tinh((cue or {}).get("gender")),
               "text": str((cue or {}).get("text") or ""),
               "voice_id": str((cue or {}).get("voice_id") or ""),
               "loi": str(loi or ""), "lan_thu": 1,
               "da_dung_local": bool(da_dung_local)})
    ds.sort(key=lambda x: x.get("index", 0))
    return ds


def ytf_cap_nhat_chua_xu_ly(ds, item):
    """Cap nhat 1 muc chua xu ly tu queue (thread doc -> UI):
    co roi thi cap nhat loi/lan thu, chua co thi them. Tra ds."""
    ds = ds if isinstance(ds, list) else []
    idx = int((item or {}).get("index") or 0)
    for it in ds:
        if it.get("index") == idx:
            it["loi"] = str(item.get("loi") or it.get("loi") or "")
            it["lan_thu"] = int(item.get("lan_thu") or it.get("lan_thu") or 1)
            it["da_dung_local"] = bool(item.get("da_dung_local") or it.get("da_dung_local"))
            return ds
    ds.append(dict(item))
    ds.sort(key=lambda x: x.get("index", 0))
    return ds


def ytf_xoa_chua_xu_ly(ds, index):
    """Xoa 1 cue khoi danh sach chua xu ly (da doc xong). Tra ds."""
    if not isinstance(ds, list):
        return []
    ds[:] = [x for x in ds if x.get("index") != int(index)]
    return ds


def ytf_tien_do_thanh_cong(tong_cue, so_cue_thanh_cong):
    """% tien do CHI tinh cue da doc THANH CONG (cue loi = 0%)."""
    if not tong_cue:
        return 0
    return int(round(100.0 * int(so_cue_thanh_cong) / int(tong_cue)))


def ytf_ban_da_xong(chua_xu_ly, tong_cue, so_cue_thanh_cong):
    """1 ban chi duoc goi la XONG khi danh sach chua xu ly RONG va
    so cue thanh cong = tong cue. Con cue chua xu ly thi file final
    KHONG duoc trinh bay la hoan chinh."""
    if not tong_cue:
        return False
    return (not chua_xu_ly) and int(so_cue_thanh_cong) >= int(tong_cue)


def _bo_sung_voice_mode(ra, raw_data):
    """Bo sung vao moi ban sau khi parse JSON: voice_mode (single /
    dialogue), speakers day du character/gender/voice_id, va canh
    bao gioi tinh. Khong doi script/cues. Tra ra (cung dict)."""
    vm = ytf_chuan_hoa_voice_mode(raw_data if isinstance(raw_data, dict) else {}, ra)
    for lang, b in (ra or {}).items():
        if not isinstance(b, dict):
            continue
        b["voice_mode"] = vm["voice_mode"]
        b["voice_mode_nguon"] = vm["nguon"]
        for sp in ("A", "B"):
            info = ytf_speaker_info(b, sp)
            sp_d = dict(b.get("speakers", {}).get(sp) or {})
            sp_d.setdefault("character", info["character"])
            sp_d.setdefault("gender", info["gender"])
            if not sp_d.get("voice_id"):
                _vid, _e, _m = ytf_giong_cua_speaker(b, sp)
                sp_d["voice_id"] = _vid
                if _m and info.get("voice_id"):
                    sp_d["voice_id_goc"] = info["voice_id"]
            b.setdefault("speakers", {})[sp] = sp_d
        b["canh_bao_gioi_tinh"] = []
        for sp in ("A", "B"):
            _ok, _cb, _g, _vg = ytf_kiem_tra_gioi_tinh_giong(b, sp)
            if not _ok and _cb:
                b["canh_bao_gioi_tinh"].append(_cb)
    return ra


def ytf_chuan_hoa_cues(cues, ngon_ngu):
    """Chuan hoa srt_cues tu JSON: chap nhan start/end dang giay
    (float) hoac dang 'HH:MM:SS,mmm' / ms. Tra list da sap xep."""
    ra = []
    for i, c in enumerate(cues or [], 1):
        if isinstance(c, str):
            c = {"text": c}
        if not isinstance(c, dict) or not str(c.get("text", "")).strip():
            continue
        def _sang_giay(v, mac_dinh):
            if v is None:
                return mac_dinh
            if isinstance(v, (int, float)):
                return float(v) / 1000.0 if float(v) > 3600 else float(v)
            m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", str(v))
            if m:
                return (int(m.group(1)) * 3600 + int(m.group(2)) * 60
                        + int(m.group(3)) + int(m.group(4)) / 1000.0)
            try:
                return float(v)
            except Exception:
                return mac_dinh
        bat = _sang_giay(c.get("start"), 0.0)
        ket = _sang_giay(c.get("end"), bat + ytf_uoc_tinh_thoi_luong_giay(c.get("text", ""), ngon_ngu))
        if ket <= bat:
            ket = bat + max(0.8, ytf_uoc_tinh_thoi_luong_giay(c.get("text", ""), ngon_ngu))
        ra.append({"index": int(c.get("index") or i), "start": round(float(bat), 3),
                   "end": round(float(ket), 3), "text": str(c.get("text", "")).strip(),
                   "speaker": ytf_chuan_hoa_speaker(c.get("speaker")),
                   "character": str(c.get("character") or c.get("nhan_vat") or c.get("speaker_name") or ""),
                   "gender": ytf_chuan_hoa_gioi_tinh(c.get("gender") or c.get("gioi_tinh"))})
    ra.sort(key=lambda x: x["start"])
    for i, c in enumerate(ra, 1):
        c["index"] = i
    return ra


def ytf_retime_cues(cues, thoi_luong_ms, nghi_ms=350):
    """CAN LAI SRT theo thoi luong THAT tung cue (ms, do bang ffprobe
    sau khi doc xong). Tra list cue moi: start = tong cac cue truoc
    + nghi giua cac cue; end = start + thoi luong that. Neu thieu
    thoi luong that thi giu uoc tinh cu (khong doan bua)."""
    ra, t = [], 0
    for i, c in enumerate(cues):
        d = None
        if thoi_luong_ms and i < len(thoi_luong_ms):
            try:
                d = int(thoi_luong_ms[i])
            except Exception:
                d = None
        if d is None or d <= 0:
            d = int(round((c["end"] - c["start"]) * 1000))
        ra.append({"index": i + 1, "start": round(t / 1000.0, 3),
                   "end": round((t + d) / 1000.0, 3), "text": c["text"],
                   "speaker": c.get("speaker", "A"),
                   "character": c.get("character", ""),
                   "gender": c.get("gender")})
        t += d + int(nghi_ms or 0)
    return ra


def ytf_srt_tu_cues(cues):
    """Cues -> noi dung file .srt (timestamp HH:MM:SS,mmm)."""
    dong = []
    for c in cues:
        dong.append(str(c["index"]))
        dong.append("%s --> %s" % (_dinh_dang_ms(int(round(c["start"] * 1000))),
                                    _dinh_dang_ms(int(round(c["end"] * 1000)))))
        dong.append(c["text"])
        dong.append("")
    return "\n".join(dong)


def ytf_parse_json(noi_dung):
    """Parse JSON dan vao tab. Tra (phien_ban, loi) voi phien_ban =
    {"en": {...}, "vi": {...}} (chi ngon ngu co du lieu) hoac
    (None, loi). Format CHINH la dual {en, vi}; fallback: JSON 1
    ngon ngu, bare srt_cues array, hoac noi dung .srt (text)."""
    if isinstance(noi_dung, dict):
        data = noi_dung
    else:
        txt = (noi_dung or "").strip()
        if not txt:
            return None, "JSON trống — dán JSON AI trả về rồi ấn Áp dụng JSON."
        # Fallback: noi dung .srt tho (bat dau bang so + timestamp).
        if re.match(r"^\s*\d+\s*\n\d+:\d+:\d+", txt):
            cau = doc_srt_text(txt)
            if not cau:
                return None, "Không parse được file SRT."
            cues = [{"index": c["chi_so"], "start": c["bat_dau_ms"] / 1000.0,
                     "end": c["ket_thuc_ms"] / 1000.0, "text": c["text"]} for c in cau]
            return _bo_sung_voice_mode({"en": {"language": "en", "voice_settings": {},
                           "script_text": " ".join(c["text"] for c in cues),
                           "srt_cues": cues, "chapters": []}}, {}), ""
        try:
            data = json.loads(txt)
        except Exception as e:
            return None, "JSON lỗi: %s" % e
    if isinstance(data, list):
        data = {"language": "en", "srt_cues": data}
    if not isinstance(data, dict):
        return None, "JSON phải là object {en:{...}, vi:{...}} hoặc 1 ngôn ngữ."

    def _chuan_hoa_1_ban(ban, lang_mac_dinh):
        if not isinstance(ban, dict):
            return None
        lang = str(ban.get("language") or lang_mac_dinh).lower()[:2]
        vs = ban.get("voice_settings") or {}
        if not isinstance(vs, dict):
            vs = {}
        script = str(ban.get("script_text") or ban.get("script") or "")
        cues = ytf_chuan_hoa_cues(ban.get("srt_cues") or ban.get("cues") or [], lang)
        if not cues and script:
            cues = ytf_chia_cau_tu_script(script, lang)
        if not script and cues:
            script = " ".join(c["text"] for c in cues)
        if not cues:
            return None
        # Anh xa giong Muse trong voice_settings (neu co) + log note.
        vid = str(vs.get("voice_id") or "")
        ten_muse, edge, la_muse = ytf_anh_xa_giong_muse(vid)
        vs = dict(vs)
        vs.setdefault("language", lang)
        if la_muse:
            vs["voice_id_goc"] = vid
            vs["voice_id"] = edge
            vs["ghi_chu_anh_xa"] = (
                "Giọng %s là giọng nội bộ của Muse, KHÔNG chạy native "
                "trên Windows — tab dùng Edge tương đương %s. Audio %s "
                "đầy đủ chỉ tạo được trong chat Muse." % (ten_muse, edge, ten_muse))
        try:
            toc_do = float(vs.get("speed") or vs.get("toc_do") or 1.0)
        except Exception:
            toc_do = 1.0
        vs["speed"] = max(0.5, min(YTF_TOC_DO_TOI_DA, toc_do))
        try:
            vs["pitch"] = int(vs.get("pitch") or vs.get("cao_do") or 0)
        except Exception:
            vs["pitch"] = 0
        vs["pitch"] = max(-10, min(10, vs["pitch"]))
        # (v7.15, doi thoai; v7.16: GOP thay vi thay the) speakers:
        # A = voice_settings GOP them character/gender tu speakers.A,
        # B = voice_settings_b GOP them character/gender tu speakers.B.
        # v7.15 thay the han (mat voice_id / mat character/gender);
        # v7.16 gop de gioi tinh + giong deu con nguyen.
        vs_b = ban.get("voice_settings_b") or {}
        sp_raw = ban.get("speakers") or {}
        if not isinstance(vs_b, dict):
            vs_b = {}
        if isinstance(sp_raw, dict):
            _sp_a = sp_raw.get("A") or sp_raw.get("a") or {}
            if isinstance(_sp_a, dict):
                vs = dict(vs)
                for _k in ("voice_id", "voice_name", "character", "gender", "speed", "pitch"):
                    if _sp_a.get(_k):
                        vs[_k] = _sp_a[_k]
            _sp_b = sp_raw.get("B") or sp_raw.get("b") or {}
            if isinstance(_sp_b, dict):
                vs_b = dict(vs_b)
                for _k in ("voice_id", "voice_name", "character", "gender", "speed", "pitch"):
                    if _sp_b.get(_k):
                        vs_b[_k] = _sp_b[_k]
        vs_b = dict(vs_b)
        if vs_b.get("voice_id"):
            _t, _e, _m = ytf_anh_xa_giong_muse(str(vs_b["voice_id"]))
            if _m:
                vs_b["voice_id_goc"] = str(vs_b["voice_id"])
                vs_b["voice_id"] = _e
        # (v7.16) Chuan hoa gioi tinh ngay tu luc parse (nu/nam/F/M).
        for _d in (vs, vs_b):
            if _d.get("gender"):
                _g = ytf_chuan_hoa_gioi_tinh(_d.get("gender"))
                if _g:
                    _d["gender"] = _g
        speakers = {"A": vs, "B": vs_b}
        return {"language": lang, "voice_settings": vs, "voice_settings_b": vs_b,
                "speakers": speakers,
                "script_text": script,
                "srt_cues": cues, "chapters": ban.get("chapters") or ban.get("chuong") or [],
                "title": ban.get("title") or ban.get("tieu_de") or ""}

    # Dual chinh: {en:{...}, vi:{...}} — LOC THEO MODE JSON (v7.15).
    # Mode trong JSON thang khoa phu: en_only ma co ca vi thi bo vi.
    if "en" in data or "vi" in data:
        meta = ytf_chuan_hoa_mode(data)
        ra = {}
        for lang in meta["languages"]:
            if lang in data:
                b = _chuan_hoa_1_ban(data[lang], lang)
                if b:
                    ra[lang] = b
        if ra:
            return _bo_sung_voice_mode(ra, data), ""
        return None, "JSON mode=%s nhưng không có bản nào hợp lệ (thiếu srt_cues/script_text)." % meta["mode"]
    b = _chuan_hoa_1_ban(data, str(data.get("language") or "en").lower()[:2])
    if b:
        return _bo_sung_voice_mode({b["language"]: b}, data), ""
    return None, "JSON thiếu srt_cues và script_text — AI phải trả srt_cues theo từng câu."


class CuaSoXuLyAmThanh(tk.Frame):  # (v7.17) Frame trong Notebook, khong Toplevel
    """Tab 'Xu ly am thanh': bo xu ly am thanh doc lap (KHONG kem
    video), theo dung thu tu CYAN lam viec:
      1. Chon file audio goc (tu dien file audio cua du an dang mo).
      2. Tach nen: 'Tach giong giua (khu kenh giua, ffmpeg)' hoac
         'Giu nguyen, chi chinh am luong'. Tach trong tool dung
         ffmpeg, KHONG phai AI — chat luong khong bang tach AI cua
         CapCut; tool chi la them 1 lua chon, khong bat buoc.
      3. Chinh am luong voice/nen (mac dinh 100/100, khong goi y).
      4. Nghe thu: tron thu 30 giay roi phat ra loa.
      5. Luu nen ra file rieng.
      6. Gop nen da chinh + voice HoaiMy thanh file voice-sub
         (amix, khong sidechain ducking).
    Dinh dang xuat chon duoc: MP3 (128k/44.1k/stereo/CBR, mac dinh),
    WAV (PCM 16-bit), M4A (AAC 128k)."""
    CHE_DO_TACH = {
        "tach_giua": "Tách giọng giữa (khử kênh giữa, ffmpeg)",
        "giu_nguyen": "Giữ nguyên, chỉ chỉnh âm lượng",
        # (v7.21) Tach AI: nhan dien giong bang model MDX-Net
        # (onnxruntime, chay CPU). (v7.22) Doi sang
        # onnxruntime-directml: co card DirectX 12 thi chay GPU,
        # khong thi tu ve CPU (chon o muc "Cài đặt GPU" ben duoi).
        # Tach duoc ca audio mono / 2 kenh giong het nhau ma khu
        # kenh giua bo tay. Model tai 1 lan o muc "Tài nguyên AI"
        # ben duoi, dung lai mai.
        "tach_ai": "Tách AI (nhận diện giọng bằng AI)",
    }
    CHE_DO_TACH_MAC_DINH = "tach_giua"

    def __init__(self, quan_ly, parent=None):
        super().__init__(parent if parent is not None else quan_ly)
        self.quan_ly = quan_ly
        self.cfg = doc_config()
        self.hang_doi = queue.Queue()
        self.dang_chay = False
        self._yeu_cau_huy = threading.Event()
        self.file_goc = None
        self.file_nen_lam_viec = None
        self.file_giong_goc_lam_viec = None  # (v7.23) file giong goc
        # vua tach AI (<ten>_giong-goc.mp3)
        self.file_ket_qua = None
        self.nen_tach_bitrate = None  # (v7.17) bitrate MP3 cua file
        # nen vua tach (de "Luu nen" copy thang khi khong can encode lai)
        self._ket_qua_quet_gpu = None  # (v7.22) ket qua quet GPU gan nhat
        self._dang_quet_gpu = False
        self.var_trang_thai_gpu = tk.StringVar(
            value="GPU: đang quét máy...")
        self._dung_ui()
        self._dien_mac_dinh()
        self.after(200, self._xu_ly_hang_doi)
        # (v7.18) Dong bo o loi am thanh dinh ky (moi 200ms) — chay
        # tren luong chinh nen an toan voi tkinter.
        self.after(200, self._dong_bo_o_loi_am_thanh_dinh_ky)
        # (v7.22) Quet GPU sau khi mo tab (luong phu, UI khong dong).
        self.after(500, self._quet_gpu_nen)

    # ----- giao dien -----
    def _dung_ui(self):
        pad = {"padx": 8, "pady": 4}
        # (v7.24, H2-sua) Boc TOAN BO tab trong khung cuon doc (Canvas +
        # Scrollbar, cung mau _tao_khung_cuon cua tab Voice Faceless
        # v7.19): truoc day txt_log (pack fill="both", expand=True)
        # chiem het cho, day o "Loi am thanh" ra khoi man hinh
        # (khong map, rong=1) o 1920x1080 — noi dung cao hon vung
        # hien ~113px. Gio moi widget pack vao noi_dung (frame trong
        # canvas); cuon chuot xuong la toi o loi. Giu nguyen moi
        # control, ten bien, logic — chi doi khung chua.
        self._khung_cuon_ngoai, noi_dung = self._tao_khung_cuon(self)
        self._khung_cuon_ngoai.pack(fill="both", expand=True)
        self._khung_noi_dung = noi_dung
        # (v7.24, H2) Luoi 3 cot x 2 hang thay vi xep doc 1 cot:
        # hang 1 = [1. File goc] [2. Tach nen] [3. Am luong],
        # hang 2 = [2a. GPU + 2b. Tai nguyen AI] [4. Nghe thu]
        # [5. Luu nen / 6. Gop]. Chi doi bo cuc — moi nut, o nhap,
        # thanh tien trinh + % va logic tung muc giu nguyen.
        luoi = tk.Frame(noi_dung)
        luoi.pack(fill="both", expand=True, padx=4, pady=2)
        for _c in range(3):
            luoi.grid_columnconfigure(_c, weight=1, uniform="cot_am_thanh")
        # (1) File audio goc
        f1 = tk.LabelFrame(luoi, text=" 1. File audio gốc ", padx=8, pady=6)
        f1.grid(row=0, column=0, sticky="nsew", **pad)
        tk.Label(f1, text="File audio gốc:").grid(row=0, column=0,
                                                   sticky="w")
        self.e_goc = tk.Entry(f1, width=56)
        self.e_goc.grid(row=0, column=1, sticky="we")
        tk.Button(f1, text="Chọn...",
                  command=self._chon_goc).grid(row=0, column=2)
        tk.Button(f1, text="Lấy file audio dự án đang chọn",
                  command=self._dien_audio_goc_mac_dinh).grid(
                      row=1, column=0, columnspan=3, sticky="w",
                      pady=(4, 0))
        f1.columnconfigure(1, weight=1)
        # (2) Tach nen
        f2 = tk.LabelFrame(luoi, text=" 2. Tách nền ", padx=8, pady=6)
        f2.grid(row=0, column=1, sticky="nsew", **pad)
        tk.Label(f2, text="Cách tách:").grid(row=0, column=0, sticky="w")
        self.var_che_do_tach = tk.StringVar(
            value=self.CHE_DO_TACH[self.CHE_DO_TACH_MAC_DINH])
        self.cb_che_do_tach = ttk.Combobox(
            f2, textvariable=self.var_che_do_tach,
            values=list(self.CHE_DO_TACH.values()),
            state="readonly", width=38)
        self.cb_che_do_tach.grid(row=0, column=1, sticky="w", padx=4)
        # (v7.23) Doi che do tach thi cap nhat khoa/mo o giong goc
        # (khu kenh giua khong co file giong goc de tron).
        self.cb_che_do_tach.bind(
            "<<ComboboxSelected>>", self._doi_che_do_tach)
        self.btn_tach = tk.Button(f2, text="Tách nền",
                                  command=self._bam_tach_nen)
        self.btn_tach.grid(row=0, column=2, padx=4)
        tk.Label(
            f2,
            text="Tách trong tool dùng ffmpeg, không phải AI — chất "
                 "lượng không bằng tách AI của CapCut. Tách bằng tool "
                 "này HOẶC tách trong CapCut đều được, tool chỉ là "
                 "thêm 1 lựa chọn. Chế độ 'Tách AI' dùng model AI "
                 "trong tool (mục Tài nguyên AI bên dưới), tách được "
                 "cả audio mono / 2 kênh giống hệt nhau.",
            wraplength=560, justify="left", anchor="w",
            fg="gray").grid(row=1, column=0, columnspan=3, sticky="w")
        self.lb_nen_hien_tai = tk.Label(f2, text="Chưa có file nền.",
                                        anchor="w", fg="gray")
        self.lb_nen_hien_tai.grid(row=2, column=0, columnspan=3,
                                  sticky="w")
        # (v7.22) Dong trang thai thiet bi tach AI (dung chung
        # StringVar voi muc Cai dat GPU ben duoi).
        self.lb_thiet_bi_tach_ai = tk.Label(
            f2, textvariable=self.var_trang_thai_gpu, anchor="w",
            fg="gray", wraplength=560, justify="left")
        self.lb_thiet_bi_tach_ai.grid(row=3, column=0, columnspan=3,
                                      sticky="w")
        # (v7.22) Cai dat GPU: chi liet ke chuc nang DUNG DUOC GPU
        # theo audit (hien chi co Tach nen AI). Moi chuc nang co o
        # chon thiet bi rieng, luu config rieng. Chuc nang khong
        # dung duoc GPU (gop am thanh ffmpeg, long tieng HoaiMy
        # cloud) KHONG co o chon GPU gia — chi ghi chu o day.
        khung_gpu_ai = tk.Frame(luoi)
        khung_gpu_ai.grid(row=1, column=0, sticky="nsew", **pad)
        f2a = tk.LabelFrame(khung_gpu_ai, text=" 2a. Cài đặt GPU ",
                            padx=8, pady=6)
        f2a.pack(fill="x")
        tk.Label(f2a, text="Tách nền AI (MDX-Net):").grid(
            row=0, column=0, sticky="w")
        self.var_thiet_bi_tach_ai = tk.StringVar(
            value=self._ten_thiet_bi_tach_ai(
                self._lay_thiet_bi_tach_ai()))
        self.cb_thiet_bi_tach_ai = ttk.Combobox(
            f2a, textvariable=self.var_thiet_bi_tach_ai,
            values=list(GPU_TACH_AI_LUA_CHON.values()),
            state="readonly", width=38)
        self.cb_thiet_bi_tach_ai.grid(row=0, column=1, sticky="w",
                                      padx=4)
        self.cb_thiet_bi_tach_ai.bind(
            "<<ComboboxSelected>>", self._doi_thiet_bi_tach_ai)
        tk.Button(f2a, text="Quét lại",
                  command=self._quet_gpu_nen).grid(
                      row=0, column=2, padx=4)
        self.lb_gpu_trang_thai = tk.Label(
            f2a, textvariable=self.var_trang_thai_gpu, anchor="w",
            fg="gray", wraplength=560, justify="left")
        self.lb_gpu_trang_thai.grid(row=1, column=0, columnspan=3,
                                    sticky="w")
        tk.Label(
            f2a,
            text="Chỉ liệt kê chức năng dùng được GPU. Gộp âm thanh "
                 "(ffmpeg) và lồng tiếng HoaiMy (máy chủ Microsoft) "
                 "không chạy trên GPU của máy — xem ghi chú bản cập "
                 "nhật.",
            wraplength=560, justify="left", anchor="w",
            fg="gray").grid(row=2, column=0, columnspan=3, sticky="w")
        # (v7.21) Tai nguyen AI (model tach giong): 1 cua so duy nhat,
        # KHONG Toplevel. Hien trang thai model + nut Tai + thanh
        # tien trinh tai xuong + thu muc chua model.
        f2b = tk.LabelFrame(khung_gpu_ai,
                            text=" 2b. Tài nguyên AI (model tách giọng) ",
                            padx=8, pady=6)
        f2b.pack(fill="x", pady=(8, 0))
        tk.Label(f2b, text="Thư mục tài nguyên:").grid(
            row=0, column=0, sticky="w")
        self.var_thu_muc_ai = tk.StringVar(
            value=self._lay_thu_muc_tai_nguyen_ai())
        self.e_thu_muc_ai = tk.Entry(f2b, textvariable=self.var_thu_muc_ai,
                                     width=34, state="readonly")
        self.e_thu_muc_ai.grid(row=0, column=1, sticky="we")
        tk.Button(f2b, text="Chọn thư mục...",
                  command=self._chon_thu_muc_tai_nguyen_ai).grid(
                      row=0, column=2, padx=4)
        tk.Button(f2b, text="Mở thư mục",
                  command=self._mo_thu_muc_tai_nguyen_ai).grid(
                      row=0, column=3, padx=4)
        f2b.columnconfigure(1, weight=1)
        self._ai_model_widgets = {}
        self._dang_tai_model = False
        self._yeu_cau_huy_tai = threading.Event()
        for hang, model in enumerate(AI_TACH_MODELS):
            ten = "%s (%.1f MB)" % (model["ten"],
                                    model["size"] / 1048576.0)
            tk.Label(f2b, text=ten).grid(row=1 + hang, column=0,
                                         columnspan=2, sticky="w")
            lb_tt = tk.Label(f2b, text="Đang kiểm tra...", fg="gray")
            lb_tt.grid(row=1 + hang, column=2, sticky="w", padx=4)
            btn = tk.Button(
                f2b, text="Tải",
                command=lambda m=model: self._bam_tai_model_ai(m))
            btn.grid(row=1 + hang, column=3, padx=4)
            self._ai_model_widgets[model["id"]] = (lb_tt, btn)
        # (v7.22) Thu vien GPU (DirectML): kem trong ban cai tu
        # v7.22 (onnxruntime-directml), KHONG tai rieng nhu model —
        # vi onnxruntime va onnxruntime-directml cung 1 ten goi
        # 'onnxruntime' nen khong the cai chung trong 1 tool; muon
        # co GPU thi cap nhat tool (nut ben canh goi kiem tra cap
        # nhat, tai ban cai moi ve). Trang thai cap nhat theo ket
        # qua quet GPU.
        hang_gpu = 1 + len(AI_TACH_MODELS)
        tk.Label(f2b, text="Thư viện GPU (DirectML)").grid(
            row=hang_gpu, column=0, columnspan=2, sticky="w")
        self.lb_gpu_thu_vien = tk.Label(f2b, text="Đang quét...",
                                        fg="gray")
        self.lb_gpu_thu_vien.grid(row=hang_gpu, column=2, sticky="w",
                                  padx=4)
        self.btn_gpu_cap_nhat = tk.Button(
            f2b, text="Cập nhật tool",
            command=self._bam_cap_nhat_tool_gpu, state="disabled")
        self.btn_gpu_cap_nhat.grid(row=hang_gpu, column=3, padx=4)
        f_tai = tk.Frame(f2b)
        f_tai.grid(row=2 + len(AI_TACH_MODELS), column=0, columnspan=4,
                   sticky="we", pady=(4, 0))
        self.thanh_tien_trinh_tai = ttk.Progressbar(
            f_tai, orient="horizontal", mode="determinate", maximum=100)
        self.thanh_tien_trinh_tai.pack(side="left", fill="x", expand=True)
        self.lb_phan_tram_tai = tk.Label(f_tai, text="", width=6,
                                         anchor="w")
        self.lb_phan_tram_tai.pack(side="left", padx=(6, 0))
        self.btn_huy_tai = tk.Button(f_tai, text="Hủy",
                                     state="disabled",
                                     command=self._huy_tai_model_ai)
        self.btn_huy_tai.pack(side="left", padx=(6, 0))
        self.lb_trang_thai_tai = tk.Label(
            f2b, text="", anchor="w", fg="gray", wraplength=560,
            justify="left")
        self.lb_trang_thai_tai.grid(row=3 + len(AI_TACH_MODELS),
                                    column=0, columnspan=4, sticky="w")
        tk.Label(
            f2b,
            text="Tách AI dùng onnxruntime-directml (kèm trong bản cài "
                 "từ v7.22): có card DirectX 12 thì chạy GPU, không "
                 "có thì tự về CPU, không cần cài CUDA. Model tải "
                 "1 lần, dùng lại mãi — tải xong dùng luôn, không cần "
                 "khởi động lại tool. File dài sẽ chạy lâu, cứ để "
                 "tool chạy nền, thanh % ở trên sẽ cho biết tới đâu.",
            wraplength=560, justify="left", anchor="w",
            fg="gray").grid(row=4 + len(AI_TACH_MODELS), column=0,
                            columnspan=4, sticky="w")
        self._cap_nhat_trang_thai_tai_nguyen_ai()
        # (3) Chinh am luong
        # (v7.24, H3) Dung 3 hang am luong RIENG, moi hang 1 o %
        # chinh doc lap: voice HoaiMy 100% / nen 100% / giong goc 0%.
        # (v7.24, H1) O file giong goc: che do Tach AI thi CHI DOC
        # (tu dien sau khi tach, KHONG co nut Chon...); nut Chon...
        # CHI hien o che do Giu nguyen; khu kenh giua thi khoa nhu cu.
        f3 = tk.LabelFrame(luoi, text=" 3. Chỉnh âm lượng ", padx=8, pady=6)
        f3.grid(row=0, column=2, sticky="nsew", **pad)
        tk.Label(f3, text="Âm lượng voice HoaiMy:").grid(
            row=0, column=0, sticky="w")
        self.var_vol_voice = tk.StringVar(value="100")
        self.ent_vol_voice = tk.Entry(f3, textvariable=self.var_vol_voice,
                                      width=6)
        self.ent_vol_voice.grid(row=0, column=1, sticky="w", padx=4)
        tk.Label(f3, text="%").grid(row=0, column=2, sticky="w")
        tk.Label(f3, text="Âm lượng nền:").grid(row=1, column=0,
                                                 sticky="w", pady=(6, 0))
        self.var_vol_nen = tk.StringVar(value="100")
        self.ent_vol_nen = tk.Entry(f3, textvariable=self.var_vol_nen,
                                    width=6)
        self.ent_vol_nen.grid(row=1, column=1, sticky="w", padx=4,
                              pady=(6, 0))
        tk.Label(f3, text="%").grid(row=1, column=2, sticky="w",
                                    pady=(6, 0))
        # (v7.23) Giong goc (tieng Trung) — track thu 3: file giong
        # goc model AI tach ra (tu dien sau khi tach AI xong), am
        # luong mac dinh 0% = khong tron giong goc (giu hanh vi cu).
        tk.Label(f3, text="Giọng gốc (tiếng Trung):").grid(
            row=2, column=0, sticky="w", pady=(6, 0))
        self.e_giong_goc = tk.Entry(f3, width=30)
        self.e_giong_goc.grid(row=2, column=1, sticky="we", padx=4,
                              pady=(6, 0))
        self.btn_chon_giong_goc = tk.Button(
            f3, text="Chọn...", command=self._chon_giong_goc)
        self.btn_chon_giong_goc.grid(row=2, column=2, sticky="w",
                                     pady=(6, 0))
        tk.Label(f3, text="Âm lượng giọng gốc (tiếng Trung, sau khi "
                          "tách nền):").grid(row=3, column=0, columnspan=3,
                                             sticky="w", pady=(6, 0))
        self.var_vol_giong_goc = tk.StringVar(value="0")
        self.ent_vol_giong_goc = tk.Entry(
            f3, textvariable=self.var_vol_giong_goc, width=6)
        self.ent_vol_giong_goc.grid(row=4, column=0, sticky="w", padx=4,
                                    pady=(2, 0))
        tk.Label(f3, text="%").grid(row=4, column=1, sticky="w",
                                    pady=(2, 0))
        self.lb_ghi_chu_giong_goc = tk.Label(
            f3, text="Mặc định 0% = không trộn giọng gốc (giữ hành vi "
                     "cũ). Tách AI xong sẽ tự điền file giọng gốc vừa "
                     "tách vào đây.",
            fg="gray", wraplength=560, justify="left", anchor="w")
        self.lb_ghi_chu_giong_goc.grid(row=5, column=0, columnspan=3,
                                       sticky="w")
        f3.columnconfigure(1, weight=1)
        # (4) Nghe thu
        f4 = tk.LabelFrame(luoi, text=" 4. Nghe thử (30 giây) ",
                           padx=8, pady=6)
        f4.grid(row=1, column=1, sticky="nsew", **pad)
        self.btn_nghe_thu = tk.Button(f4, text="▶ Nghe thử",
                                      command=self._bam_nghe_thu)
        self.btn_nghe_thu.grid(row=0, column=0, padx=4)
        tk.Label(f4, text="Bắt đầu từ (giây):").grid(
            row=0, column=1, sticky="w", padx=(8, 0))
        self.var_nghe_tu = tk.StringVar(value="0")
        tk.Entry(f4, textvariable=self.var_nghe_tu,
                 width=8).grid(row=0, column=2, sticky="w", padx=4)
        tk.Label(
            f4,
            text="Chỉ trộn thử 30 giây rồi phát ra loa, không trộn cả "
                 "file dài.", wraplength=460, justify="left").grid(
                     row=0, column=3, sticky="w")
        # (5)+(6) Luu nen + Gop voi voice
        f5 = tk.LabelFrame(luoi,
                           text=" 5. Lưu nền / 6. Gộp với voice ",
                           padx=8, pady=6)
        f5.grid(row=1, column=2, sticky="nsew", **pad)
        tk.Label(f5, text="Định dạng đầu ra:").grid(row=0, column=0,
                                                     sticky="w")
        self.var_dinh_dang = tk.StringVar(value="MP3")
        self.cb_dinh_dang = ttk.Combobox(
            f5, textvariable=self.var_dinh_dang,
            values=["MP3", "WAV", "M4A"], state="readonly", width=8)
        self.cb_dinh_dang.grid(row=0, column=1, sticky="w", padx=4)
        self.cb_dinh_dang.bind(
            "<<ComboboxSelected>>",
            lambda e: self._cap_nhat_ghi_chu_dinh_dang())
        tk.Label(f5, text="Bitrate MP3:").grid(row=0, column=2,
                                               sticky="w", padx=(12, 0))
        self.var_bitrate = tk.StringVar(value="128k")
        self.cb_bitrate = ttk.Combobox(
            f5, textvariable=self.var_bitrate,
            values=list(GOP_AM_THANH_BITRATE_LUA_CHON),
            state="readonly", width=7)
        self.cb_bitrate.grid(row=0, column=3, sticky="w", padx=4)
        self.cb_bitrate.bind(
            "<<ComboboxSelected>>",
            lambda e: self._cap_nhat_ghi_chu_dinh_dang())
        self.lb_ghi_chu_dinh_dang = tk.Label(
            f5, text="", fg="gray", wraplength=560, justify="left",
            anchor="w")
        self.lb_ghi_chu_dinh_dang.grid(row=1, column=0, columnspan=4,
                                       sticky="w")
        self.btn_luu_nen = tk.Button(f5, text="Lưu nền",
                                     command=self._bam_luu_nen)
        self.btn_luu_nen.grid(row=2, column=0, padx=4, pady=4, sticky="w")
        tk.Label(f5, text="File voice HoaiMy:").grid(row=2, column=1,
                                                      sticky="w")
        self.e_voice = tk.Entry(f5, width=38)
        self.e_voice.grid(row=2, column=2, sticky="we")
        tk.Button(f5, text="Chọn...",
                  command=self._chon_voice).grid(row=2, column=3)
        self.btn_gop = tk.Button(
            f5, text="Gộp thành file voice-sub",
            command=self._bam_gop, font=("TkDefaultFont", 10, "bold"))
        self.btn_gop.grid(row=3, column=0, columnspan=2, padx=4, pady=4,
                          sticky="w")
        tk.Label(
            f5,
            text="File ra: <tên file voice>_gop.<mp3/wav/m4a>, cùng "
                 "thư mục với file voice.").grid(row=3, column=2,
                                                 columnspan=2, sticky="w")
        f5.columnconfigure(2, weight=1)
        self._cap_nhat_ghi_chu_dinh_dang()
        # Nut chung + trang thai + log
        f6 = tk.Frame(noi_dung)
        f6.pack(fill="x", **pad)
        self.btn_huy = tk.Button(f6, text="Hủy", command=self._bam_huy,
                                 state="disabled", padx=10, pady=4)
        self.btn_huy.pack(side="left", padx=4)
        tk.Button(f6, text="Mở thư mục kết quả",
                  command=self._mo_thu_muc_ket_qua).pack(side="left",
                                                         padx=4)
        self.lb_trang_thai = tk.Label(noi_dung, text="Chưa chạy.")
        self.lb_trang_thai.pack(fill="x", padx=8)
        # (v7.20) Thanh tien trinh truc tiep + % cho cac tac vu ffmpeg
        # dai (tach nen / gop / luu nen): worker chi day % vao hang doi,
        # chi luong chinh moi cham vao Tk (qua _xu_ly_hang_doi).
        f_tt = tk.Frame(noi_dung)
        f_tt.pack(fill="x", padx=8, pady=(2, 0))
        self.thanh_tien_trinh = ttk.Progressbar(
            f_tt, orient="horizontal", mode="determinate", maximum=100)
        self.thanh_tien_trinh.pack(side="left", fill="x", expand=True)
        self.lb_phan_tram = tk.Label(f_tt, text="0%", width=5, anchor="w")
        self.lb_phan_tram.pack(side="left", padx=(6, 0))
        self.lb_ket_qua = tk.Label(noi_dung, text="", anchor="w",
                                   wraplength=680, justify="left",
                                   fg="green")
        self.lb_ket_qua.pack(fill="x", padx=8)
        tk.Label(noi_dung, text="Nhật ký:").pack(anchor="w", padx=8)
        # (v7.24, H2) Log ngan lai (10 -> 6 -> 5 dong): tab da co
        # khung cuon doc nen log khong can chiem het cho nua; 5 dong
        # van du doc, phan con lai cuon xuong.
        self.txt_log = tk.Text(noi_dung, height=5, wrap="word")
        self.txt_log.pack(fill="both", expand=True, padx=8, pady=4)
        # (v7.18) O log loi am thanh RIENG BIET: chi ghi LOI tach nen /
        # tron / nghe thu / luu nen (kem gio), de CYAN copy xu ly som.
        # Loi long giong (TTS) KHONG vao day. Noi dung lay tu nhat ky
        # loi chung (2 tab dung chung) nen loi tron o tab Doc phu de
        # cung hien o day.
        tk.Label(noi_dung, text="Lỗi âm thanh (chỉ lỗi tách nền / trộn / nghe thử / lưu nền — kèm giờ, bấm Sao chép để copy):").pack(anchor="w", padx=8)
        self.txt_loi_am_thanh = tk.Text(noi_dung, height=4, wrap="word",
                                        state="disabled")
        self.txt_loi_am_thanh.pack(fill="x", padx=8, pady=4)
        f_loi = tk.Frame(noi_dung)
        f_loi.pack(fill="x", padx=8, pady=2)
        tk.Button(f_loi, text="Sao chép log lỗi",
                  command=self._sao_chep_loi_am_thanh).pack(
                      side="left", padx=4)
        tk.Button(f_loi, text="Xóa log lỗi",
                  command=self._xoa_loi_am_thanh).pack(side="left", padx=4)
        self._so_dong_loi_am_thanh_da_hien = 0
        self._dong_bo_o_loi_am_thanh()
        # (v7.23) Cap nhat khoa/mo o giong goc theo che do tach hien
        # tai (goi cuoi _dung_ui — luc nay moi widget da co).
        self._doi_che_do_tach()

    def _tao_khung_cuon(self, parent):
        """(v7.24, H2-sua) Khung cuon doc (Canvas + Scrollbar + Frame
        trong), mirror _tao_khung_cuon cua tab Voice Faceless (v7.19)
        trong cung file. Lan chuot tren moi vung noi dung (tru o
        Text/Listbox/Scrollbar — cac o do tu cuon rieng) deu cuon ca
        tab, de keo xuong toi o "Loi am thanh" cuoi tab tren man hinh
        1080p."""
        khung_ngoai = tk.Frame(parent)
        canvas = tk.Canvas(khung_ngoai, highlightthickness=0)
        sb = ttk.Scrollbar(khung_ngoai, orient="vertical",
                           command=canvas.yview)
        khung_trong = tk.Frame(canvas)
        cua_so = canvas.create_window((0, 0), window=khung_trong,
                                      anchor="nw")
        khung_trong.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cua_so, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _cuon(event):
            try:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
                else:
                    canvas.yview_scroll(int(-event.delta / 120), "units")
            except Exception:
                pass

        canvas.bind("<MouseWheel>", _cuon)
        canvas.bind("<Button-4>", _cuon)
        canvas.bind("<Button-5>", _cuon)

        def _gan_cuon(w):
            # Gan lan chuot cho widget con (de quy). Bo qua Text,
            # Listbox, Scrollbar: cac o do giu cuon rieng cua no.
            try:
                if isinstance(w, (tk.Text, tk.Listbox, ttk.Scrollbar,
                                  tk.Scrollbar)):
                    return
                w.bind("<MouseWheel>", _cuon)
                w.bind("<Button-4>", _cuon)
                w.bind("<Button-5>", _cuon)
            except Exception:
                pass
            try:
                for ch in w.winfo_children():
                    _gan_cuon(ch)
            except Exception:
                pass

        # Moi lan khung trong doi kich thuoc (them widget moi) thi
        # gan lai lan chuot cho cac widget con moi xuat hien.
        khung_trong.bind("<Configure>", lambda e: _gan_cuon(khung_trong),
                         add="+")
        self._canvas_cuon = canvas
        self._sb_cuon = sb
        return khung_ngoai, khung_trong

    # ----- (v7.20) thanh tien trinh -----
    def _dat_tien_trinh(self, pct):
        # Chi goi tren luong chinh (tu _xu_ly_hang_doi).
        try:
            pct = max(0.0, min(100.0, float(pct)))
        except Exception:
            pct = 0.0
        try:
            if str(self.thanh_tien_trinh["mode"]) != "determinate":
                self.thanh_tien_trinh.stop()
                self.thanh_tien_trinh.configure(mode="determinate")
            self.thanh_tien_trinh["value"] = pct
            self.lb_phan_tram.configure(text="%d%%" % int(round(pct)))
        except Exception:
            pass

    def _tien_trinh_khong_ro(self):
        # Chi goi tren luong chinh: khong biet tong thoi luong thi chay
        # kieu khong xac dinh thay vi hien % sai.
        try:
            if str(self.thanh_tien_trinh["mode"]) != "indeterminate":
                self.thanh_tien_trinh.configure(mode="indeterminate")
            self.thanh_tien_trinh.start(200)
            self.lb_phan_tram.configure(text="…")
        except Exception:
            pass

    def _dat_lai_tien_trinh(self):
        # Chi goi tren luong chinh: dung animation (neu co), ve 0%.
        try:
            try:
                self.thanh_tien_trinh.stop()
            except Exception:
                pass
            self.thanh_tien_trinh.configure(mode="determinate")
            self.thanh_tien_trinh["value"] = 0
            self.lb_phan_tram.configure(text="0%")
        except Exception:
            pass

    def _bao_tien_trinh(self, pct):
        # (v7.20) Gọi được từ luồng phụ (callback cua runner):
        # chi đẩy vào hàng đợi, KHÔNG chạm Tk. pct=None = không
        # biết tổng thời lượng -> chế độ không xác định.
        if pct is None:
            self.hang_doi.put(("tien_trinh", "khong_ro", None))
        else:
            self.hang_doi.put(("tien_trinh", "dat", pct))

    def _reset_tien_trinh(self):
        # (v7.20) Gọi được từ luồng phụ: đặt lại 0% qua hàng đợi.
        self.hang_doi.put(("tien_trinh", "reset", None))

    # ----- (v7.18) o log loi am thanh rieng biet -----
    def _dong_bo_o_loi_am_thanh(self):
        # Dong bo cac dong loi am thanh moi (tu nhat ky loi chung) vao
        # o Text. Chi chay tren luong chinh (goi tu vong lap after
        # 200ms) nen an toan voi tkinter. Neu danh sach chung ngan
        # lai so voi so dong da hien (bi xoa o noi khac) thi xoa sach
        # o hien roi hien lai tu dau — tranh dong cu sot lai.
        try:
            with _LOI_AM_THANH_KHOA:
                tong = len(_LOI_AM_THANH)
                da_hien = self._so_dong_loi_am_thanh_da_hien
                if tong < da_hien:
                    da_hien = 0
                moi = list(_LOI_AM_THANH[da_hien:])
            bi_xoa_ngoai = (da_hien == 0
                            and self._so_dong_loi_am_thanh_da_hien != 0)
            self.txt_loi_am_thanh.configure(state="normal")
            if bi_xoa_ngoai:
                self.txt_loi_am_thanh.delete("1.0", "end")
            for dong in moi:
                self.txt_loi_am_thanh.insert("end", dong + "\n")
            if moi:
                self.txt_loi_am_thanh.see("end")
            self.txt_loi_am_thanh.configure(state="disabled")
            self._so_dong_loi_am_thanh_da_hien = tong
        except Exception:
            pass

    def _dong_bo_o_loi_am_thanh_dinh_ky(self):
        # Vong lap dong bo o loi am thanh moi 200ms.
        self._dong_bo_o_loi_am_thanh()
        try:
            self.after(200, self._dong_bo_o_loi_am_thanh_dinh_ky)
        except Exception:
            pass

    def _sao_chep_loi_am_thanh(self):
        # (v7.18) Copy toan bo nhat ky loi am thanh (chung 2 tab) vao
        # clipboard, 1 lan bam.
        noi_dung = lay_noi_dung_loi_am_thanh()
        try:
            self.clipboard_clear()
            self.clipboard_append(noi_dung if noi_dung else
                                  "Chưa có lỗi âm thanh nào.")
            self.lb_trang_thai.configure(
                text="Đã sao chép log lỗi âm thanh (%d dòng)."
                     % (len(noi_dung.splitlines()) if noi_dung else 0))
        except Exception as e:
            self.lb_trang_thai.configure(
                text="Không sao chép được log lỗi: %s" % e)

    def _xoa_loi_am_thanh(self):
        # (v7.18) Xoa sach nhat ky loi am thanh (chung) + o hien.
        xoa_loi_am_thanh()
        try:
            self.txt_loi_am_thanh.configure(state="normal")
            self.txt_loi_am_thanh.delete("1.0", "end")
            self.txt_loi_am_thanh.configure(state="disabled")
        except Exception:
            pass
        self._so_dong_loi_am_thanh_da_hien = 0
        self.lb_trang_thai.configure(text="Đã xóa log lỗi âm thanh.")

    # ----- chon file / dien mac dinh -----
    def _chon_goc(self):
        # Hop thoai chon file goc KHONG gioi han duoi: mac dinh hien
        # tat ca file, chon duoc bat cu loai file am thanh nao.
        p = filedialog.askopenfilename(
            title="Chọn file audio gốc",
            filetypes=[("Tất cả file", "*.*"),
                       ("Âm thanh", "*.mp3 *.wav *.m4a *.aac *.flac "
                                    "*.ogg *.opus *.wma *.mp4 *.mkv")])
        if p:
            self.e_goc.delete(0, "end")
            self.e_goc.insert(0, p)
            self.file_goc = p
            self.file_nen_lam_viec = None
            self.file_giong_goc_lam_viec = None  # (v7.23) doi file
            # goc thi file giong goc cu khong con dung nua
            self.nen_tach_bitrate = None
            self.lb_nen_hien_tai.configure(text="Chưa có file nền.")
            # (v7.24, H1) Doi file goc thi file giong goc cu khong
            # con dung nua: xoa o bang helper (o chi doc bo qua
            # delete truc tiep) + ghi chu ve dung che do hien tai.
            self._dien_o_giong_goc("")

    def _chon_voice(self):
        p = filedialog.askopenfilename(
            title="Chọn file voice (giọng HoaiMy)",
            filetypes=[("Tất cả file", "*.*"),
                       ("Âm thanh", "*.mp3 *.wav *.m4a *.aac *.flac "
                                    "*.ogg *.opus *.wma")])
        if p:
            self.e_voice.delete(0, "end")
            self.e_voice.insert(0, p)

    def _chon_giong_goc(self):
        # (v7.23) Chon file giong goc (tieng Trung) de tron them
        # track thu 3: moi loai file am thanh.
        p = filedialog.askopenfilename(
            title="Chọn file giọng gốc (tiếng Trung)",
            filetypes=[("Tất cả file", "*.*"),
                       ("Âm thanh", "*.mp3 *.wav *.m4a *.aac *.flac "
                                    "*.ogg *.opus *.wma")])
        if p:
            self._dien_o_giong_goc(p)

    def _lay_file_giong_goc(self):
        """(v7.23) File giong goc hien tai de tron: o nhap neu file
        ton tai; khong co / khong ton tai thi None (gop 2 track nhu
        cu)."""
        try:
            p = self.e_giong_goc.get().strip()
        except Exception:
            p = ""
        if p and os.path.isfile(p):
            return p
        return None

    def _dien_o_giong_goc(self, duong_dan):
        """(v7.24, H1) Dien o file giong goc bang code: o CHI DOC
        (che do Tach AI) BO QUA lenh delete/insert IM LANG (Tk
        khong bao loi, cung khong doi noi dung) nen phai mo tam ve
        normal, dien xong thi tra lai trang thai theo che do hien
        tai. Tra True neu da dien xong."""
        try:
            self.e_giong_goc.configure(state="normal")
            self.e_giong_goc.delete(0, "end")
            if duong_dan:
                self.e_giong_goc.insert(0, duong_dan)
        except Exception:
            return False
        try:
            self._doi_che_do_tach()
        except Exception:
            pass
        return True

    def _doi_che_do_tach(self, _event=None):
        """(v7.23, sua v7.24 H1) Doi che do tach — khoa/mo hang giong goc:
        * 'Tach AI': o file CHI DOC (tu dien file _giong-goc.mp3 sau
          khi tach xong), KHONG co nut Chon...; o am luong mo.
        * 'Giu nguyen': o file nhap tay + nut Chon... HIEN (chon file
          giong goc rieng, VD tu CapCut); o am luong mo.
        * 'Tach giua' (ffmpeg, khu kenh giua): triet tieu giong goc
          nen KHONG co file giong goc — khoa o file + o am luong +
          AN nut Chon... nhu cu."""
        try:
            che_do = self._lay_che_do_tach()
        except Exception:
            che_do = self.CHE_DO_TACH_MAC_DINH
        try:
            if che_do == "tach_ai":
                self.e_giong_goc.configure(state="readonly")
                self.ent_vol_giong_goc.configure(state="normal")
                self.btn_chon_giong_goc.grid_remove()
                hien = self.e_giong_goc.get().strip()
                if hien and os.path.isfile(hien):
                    ghi_chu = ("Đã tách xong — file giọng gốc vừa tách: %s"
                               % os.path.basename(hien))
                else:
                    ghi_chu = ("Chưa tách — bấm 'Tách nền' ở mục 2, file "
                               "sẽ tự điền vào đây.")
            elif che_do == "giu_nguyen":
                self.e_giong_goc.configure(state="normal")
                self.ent_vol_giong_goc.configure(state="normal")
                self.btn_chon_giong_goc.grid()
                ghi_chu = ("Chọn file giọng gốc riêng (nếu có, VD từ "
                           "CapCut) — bấm nút “Chọn...” để chọn file. "
                           "Để trống = không trộn giọng gốc (mặc định 0%).")
            else:  # tach_giua
                self.e_giong_goc.configure(state="disabled")
                self.ent_vol_giong_goc.configure(state="disabled")
                self.btn_chon_giong_goc.grid_remove()
                ghi_chu = ("Chế độ khử kênh giữa đã triệt tiêu giọng gốc "
                           "nên không có file giọng gốc để trộn — chọn "
                           "chế độ 'Tách AI' để giữ lại giọng gốc.")
            self.lb_ghi_chu_giong_goc.configure(text=ghi_chu)
        except Exception:
            pass

    def _lay_thu_muc_du_an_hien_tai(self):
        """Thu muc du an dang mo: job dang chon o tab Quan ly, neu
        khong thi thu muc ket qua cua tab Doc phu de."""
        try:
            job = self.quan_ly._lay_job_da_chon()
            if job:
                folder = (job.get("folder") or "").strip()
                if folder and os.path.isdir(folder):
                    return folder
        except Exception:
            pass
        try:
            panel_doc = getattr(self.quan_ly, "panel_doc", None)
            thu_muc = getattr(panel_doc, "thu_muc_ket_qua", None)
            if thu_muc and os.path.isdir(thu_muc):
                return thu_muc
        except Exception:
            pass
        return None

    def _dien_audio_goc_mac_dinh(self):
        """Dien san o file audio goc bang file audio cua du an dang
        mo (uu tien file tieng rieng *_tieng.*). Chi dien khi o dang
        trong hoac file cu khong con ton tai."""
        hien = self.e_goc.get().strip()
        if hien and os.path.isfile(hien):
            return
        ung_vien = tim_file_audio_du_an(self._lay_thu_muc_du_an_hien_tai())
        if ung_vien:
            self.e_goc.delete(0, "end")
            self.e_goc.insert(0, ung_vien)
            self.file_goc = ung_vien

    def _dien_voice_mac_dinh(self):
        """Dien san o file voice bang file MP3 HoaiMy vua xuat o tab
        Doc phu de (neu co). Chi dien khi o dang trong hoac file cu
        khong con ton tai — khong ghi de file cau da chon tay."""
        hien = self.e_voice.get().strip()
        if hien and os.path.isfile(hien):
            return
        ung_vien = None
        try:
            panel_doc = getattr(self.quan_ly, "panel_doc", None)
            if panel_doc is not None:
                fg = getattr(panel_doc, "file_gop", None)
                if fg and os.path.isfile(fg):
                    ung_vien = fg
                if not ung_vien:
                    thu_muc = getattr(panel_doc, "thu_muc_ket_qua", None)
                    if thu_muc and os.path.isdir(thu_muc):
                        ung_vien = tim_file_long_tieng(thu_muc)
        except Exception:
            ung_vien = None
        if ung_vien:
            self.e_voice.delete(0, "end")
            self.e_voice.insert(0, ung_vien)

    def _dien_mac_dinh(self):
        self._dien_audio_goc_mac_dinh()
        self._dien_voice_mac_dinh()

    def _lay_am_luong(self, var):
        """Doc o am luong (so %): la thi ve 100, kep 0-200."""
        try:
            n = float(str(var.get()).strip())
        except Exception:
            n = 100.0
        return max(0.0, min(200.0, n))

    def _lay_che_do_tach(self):
        """Tra ve key che do tach ('tach_giua' / 'giu_nguyen' /
        'tach_ai' (v7.21))."""
        hien = self.var_che_do_tach.get()
        for key, ten in self.CHE_DO_TACH.items():
            if ten == hien:
                return key
        return self.CHE_DO_TACH_MAC_DINH

    def _lay_dinh_dang(self):
        dinh_dang = self.var_dinh_dang.get().strip().lower()
        if dinh_dang not in GOP_AM_THANH_DINH_DANG:
            dinh_dang = "mp3"
        return dinh_dang

    def _lay_bitrate_mp3(self):
        """(v7.17) Bitrate MP3 da chon (96k/128k/192k); mac dinh 128k
        — nhe, du nghe."""
        br = (self.var_bitrate.get() or "128k").strip().lower()
        return (br if br in GOP_AM_THANH_BITRATE_LUA_CHON
                else GOP_AM_THANH_BITRATE)

    def _lay_bitrate_mong_bps(self):
        """(v7.17) Bitrate mong doi (bps) de kiem tra file ra: MP3
        thi theo muc da chon; M4A thi 128k; WAV thi None (khong nen)."""
        dd = self._lay_dinh_dang()
        if dd == "mp3":
            return int(self._lay_bitrate_mp3().rstrip("k")) * 1000
        if dd == "m4a":
            return 128000
        return None

    def _cap_nhat_ghi_chu_dinh_dang(self):
        """(v7.17) Ghi chu theo dinh dang + bitrate da chon; bitrate
        chi co tac dung voi MP3 (WAV/M4A thi o bitrate mo di)."""
        dd = self._lay_dinh_dang()
        br = self._lay_bitrate_mp3()
        try:
            self.cb_bitrate.configure(
                state="readonly" if dd == "mp3" else "disabled")
        except Exception:
            pass
        if dd == "wav":
            ghi = ("WAV: PCM 16-bit / 44.1 kHz / Stereo — nặng, không "
                   "nén (chỉ dùng khi cần file gốc không nén).")
        elif dd == "m4a":
            ghi = "M4A: AAC 128 kbps / 44.1 kHz / Stereo."
        elif br == "96k":
            ghi = ("MP3: 96 kbps / 44.1 kHz / Stereo / CBR — nhẹ nhất, "
                   "đủ nghe giọng nói.")
        elif br == "192k":
            ghi = ("MP3: 192 kbps / 44.1 kHz / Stereo / CBR — nặng hơn, "
                   "rõ hơn.")
        else:
            ghi = ("MP3: 128 kbps / 44.1 kHz / Stereo / CBR — mặc định, "
                   "nhẹ, đủ nghe.")
        try:
            self.lb_ghi_chu_dinh_dang.configure(text=ghi)
        except Exception:
            pass

    def _lay_file_nen(self):
        """File nen hien tai de dung: file da tach, neu chua tach ma
        che do la 'giu nguyen' thi dung luon file goc."""
        if self.file_nen_lam_viec and os.path.isfile(
                self.file_nen_lam_viec):
            return self.file_nen_lam_viec
        if self._lay_che_do_tach() == "giu_nguyen":
            goc = self.e_goc.get().strip()
            if goc and os.path.isfile(goc):
                return goc
        return None

    def _khoa_nut(self, khoa):
        trang_thai = "disabled" if khoa else "normal"
        for btn in (self.btn_tach, self.btn_nghe_thu, self.btn_luu_nen,
                    self.btn_gop):
            try:
                btn.configure(state=trang_thai)
            except Exception:
                pass
        try:
            self.btn_huy.configure(state=("normal" if khoa
                                          else "disabled"))
        except Exception:
            pass

    def _bat_dau_tac_vu(self, ten):
        self.dang_chay = True
        self._yeu_cau_huy.clear()
        self._khoa_nut(True)
        self.lb_trang_thai.configure(text=ten + "...")
        self.lb_ket_qua.configure(text="")
        self._dat_lai_tien_trinh()  # (v7.20) moi tac vu bat dau tu 0%

    # ----- (2) tach nen -----
    def _bam_tach_nen(self):
        if self.dang_chay:
            return
        goc = self.e_goc.get().strip()
        if not goc or not os.path.isfile(goc):
            messagebox.showerror(
                APP_TITLE,
                "Chưa chọn file audio gốc (hoặc file không tồn tại).")
            return
        self.file_goc = goc
        self._bat_dau_tac_vu("Đang tách nền")
        t = threading.Thread(target=self._chay_tach_nen, daemon=True)
        t.start()

    def _do_thu_tach_10s(self, ffmpeg, goc):
        """(v7.20) Do thu 10 giay dau bang volumedetect: am luong trung
        binh cua file goc va cua ban sau khi khu kenh giua (cung filter
        pan nhu tach that). Tra ve (vol_goc, vol_tach, da_huy) — vol la
        float dB ('-inf' neu cam), None neu khong do duoc; da_huy True
        neu CYAN bam Huy giua chung. Loi probe thi tra (None, None,
        False) de worker tach binh thuong (khong chan viec vi probe)."""
        def _do_1(af):
            cmd = [ffmpeg, "-y", "-i", goc, "-map", "0:a", "-t", "10",
                   "-af", af, "-f", "null", "-"]
            try:
                rc, err = _chay_ffmpeg_co_gioi_han(
                    cmd, 60, dung=self._yeu_cau_huy,
                    nhan="đo thử tách nền")
            except TimeoutError:
                return None, False
            if rc == -1:
                return None, True
            if rc != 0:
                return None, False
            return _parse_mean_volume(err), False
        vol_goc, huy = _do_1("volumedetect")
        if huy:
            return None, None, True
        vol_tach, huy = _do_1(
            "pan=stereo|c0=c0-c1|c1=c1-c0,volume=2.0,volumedetect")
        if huy:
            return None, None, True
        return vol_goc, vol_tach, False

    def _chay_tach_nen(self):
        def log(s):
            self.hang_doi.put(("log", s))
            # (v7.18) Loi am thanh rieng biet: dong bat dau bang LOI /
            # CANH BAO thi ghi them vao nhat ky loi am thanh (kem gio)
            # de CYAN copy xu ly som. Chi ghi loi, khong ghi log
            # thuong; bam Huy (khong phai loi) thi khong ghi.
            if s.startswith(("LỖI", "CẢNH BÁO")):
                dong_dau = s.split("\n", 1)[0]
                duoi = s.split("\n", 1)[1] if "\n" in s else ""
                ghi_loi_am_thanh("tách nền", dong_dau,
                                 getattr(self, "file_goc", None), duoi)
        try:
            ffmpeg = tim_ffmpeg()
            if not ffmpeg:
                log("LỖI: không tìm thấy ffmpeg trên máy.")
                self.hang_doi.put(("xong", False,
                                   "Không tìm thấy ffmpeg."))
                return
            goc = self.file_goc
            che_do = self._lay_che_do_tach()
            if che_do == "giu_nguyen":
                self.file_nen_lam_viec = goc
                self.nen_tach_bitrate = None
                log("Giữ nguyên file gốc làm nền (không tách): %s" % goc)
                self.hang_doi.put(("nen_xong", True, goc))
                return
            if che_do == "tach_ai":
                # (v7.21) Tach AI: khong chay kiem tra mono / do thu
                # 10 giay (AI tach duoc ca mono / 2 kenh giong nhau).
                self._tach_nen_bang_ai(ffmpeg, goc, log)
                return
            thong_so = _ffprobe_thong_so_audio(goc, ffmpeg)
            if not thong_so:
                log("LỖI: không đọc được thông số file gốc.")
                self.hang_doi.put(("xong", False,
                                   "Không đọc được file gốc."))
                return
            _sr, ch = thong_so
            if ch < 2:
                # (v7.20) Mono: giong + nhac deu nam giua nen khu kenh
                # giua se ra file cam — dung ngay, huong dan cach khac.
                log("LỖI: file gốc chỉ có 1 kênh (mono) — giọng và nhạc "
                    "đều nằm giữa nên khử kênh giữa sẽ ra file câm. "
                    "Thử chế độ 'Tách AI' trong tool, hoặc tách nền "
                    "bằng AI trong CapCut rồi chọn chế độ 'Giữ nguyên, "
                    "chỉ chỉnh âm lượng'.")
                self.hang_doi.put(
                    ("xong", False,
                     "File gốc là mono — khử kênh giữa sẽ ra file câm. "
                     "Thử chế độ 'Tách AI' trong tool, hoặc tách nền "
                     "bằng AI trong CapCut rồi chọn chế độ 'Giữ nguyên, "
                     "chỉ chỉnh âm lượng'."))
                return
            # (v7.20) Kiem tra that: file stereo nhung 2 kenh giong het
            # nhau (giong + nhac deu nam giua — rat hay gap o phim AI)
            # thi tru kenh cung ra 0, tuc file nen cam. Do thu 10 giay
            # dau: goc nghe duoc ma sau khi khu kenh giua gan nhu cam
            # thi DUNG tach, huong dan tach bang AI trong CapCut.
            vol_goc, vol_tach, da_huy = self._do_thu_tach_10s(
                ffmpeg, goc)
            if da_huy:
                log("Đã hủy tách nền.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if (vol_tach is not None and vol_tach < -50.0
                    and (vol_goc is None or vol_goc > -50.0)):
                def _hien_db(v):
                    return "-inf dB" if v == float("-inf") else \
                        "%.1f dB" % v
                log("CẢNH BÁO: tách thử 10 giây đầu: file gốc nghe được "
                    "(trung bình %s) nhưng sau khi khử kênh giữa chỉ còn "
                    "%s — giọng và nhạc đều nằm giữa (2 kênh giống hệt "
                    "nhau) nên tách ra sẽ câm. DỪNG tách: thử chế độ "
                    "'Tách AI' trong tool, hoặc tách nền bằng AI trong "
                    "CapCut rồi chọn chế độ 'Giữ nguyên, chỉ chỉnh âm "
                    "lượng'." % (
                        _hien_db(vol_goc)
                        if vol_goc is not None else "không đo được",
                        _hien_db(vol_tach)))
                self.hang_doi.put(
                    ("xong", False,
                     "Tách thử 10 giây: giọng + nhạc đều nằm giữa (2 kênh "
                     "giống hệt nhau) nên khử kênh giữa ra file câm. "
                     "Thử chế độ 'Tách AI' trong tool, hoặc tách nền "
                     "bằng AI trong CapCut rồi chọn chế độ 'Giữ nguyên, "
                     "chỉ chỉnh âm lượng'."))
                return
            dich = ten_file_nen_lam_viec(goc)
            ffprobe = tim_ffprobe(ffmpeg)
            tong_giay = lay_thoi_luong(ffprobe, goc) if ffprobe else None
            timeout_giay = (max(300, int(tong_giay) * 3 + 120)
                            if tong_giay else 600)
            log("Đang tách giọng giữa: %s" % goc)
            bitrate = self._lay_bitrate_mp3()
            cmd = lenh_tach_giong_giua(ffmpeg, goc, dich, bitrate)
            try:
                rc, err = _chay_ffmpeg_co_tien_trinh(
                    cmd, timeout_giay, tong_giay,
                    tien_trinh_cb=self._bao_tien_trinh,
                    dung=self._yeu_cau_huy, nhan="tách nền")
            except TimeoutError:
                log("LỖI: tách nền hết thời gian chờ (%ds)."
                    % timeout_giay)
                self.hang_doi.put(("xong", False,
                                   "Tách nền hết thời gian chờ."))
                return
            if rc == -1:
                log("Đã hủy tách nền.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if rc != 0 or not (os.path.isfile(dich)
                               and os.path.getsize(dich) > 0):
                tail = (err or "").strip()[-600:]
                _ghi_log_loi_ffmpeg(os.path.dirname(dich) or ".",
                                    tail or "ffmpeg lỗi không rõ")
                log("LỖI: ffmpeg tách nền lỗi (mã %s).%s"
                    % (rc, ("\n" + tail) if tail else ""))
                self.hang_doi.put(
                    ("xong", False,
                     "ffmpeg tách nền lỗi (mã %s), xem ffmpeg-loi.log."
                     % rc))
                return
            # (v7.17) Cua chat luong: file nen MP3 sau tach phai dung
            # chuan (ffprobe + giai ma thu toan bo) moi duoc bao xong.
            ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
                dich, ffmpeg, "mp3", bitrate)
            if not ok:
                log("CẢNH BÁO: file nền tách ra không đạt chuẩn: %s"
                    % thong_tin)
                self.hang_doi.put(
                    ("xong", False,
                     "File nền tách ra không đạt chuẩn: %s" % thong_tin))
                return
            self.file_nen_lam_viec = dich
            self.nen_tach_bitrate = bitrate
            log("Đã tách xong file nền: %s (%s)" % (dich, thong_tin))
            self.hang_doi.put(("nen_xong", True, dich))
        except Exception as e:
            log("LỖI tách nền: %s" % _tom_tat_loi(e))
            self.hang_doi.put(("xong", False,
                               "Lỗi: %s" % _tom_tat_loi(e)))

    # ----- (v7.21) tach AI + tai nguyen AI -----
    def _tach_nen_bang_ai(self, ffmpeg, goc, log):
        """(v7.21) Tach nen bang AI (MDX-Net, onnxruntime).
        (v7.22) Them thiet bi: doc che do 1 lan luc bat dau chay
        (Tu dong / Chi CPU / Chi GPU, muc Cai dat GPU); Tu dong thu
        GPU truoc, loi thi ve CPU; Chi GPU thi thieu/loi la DUNG
        voi thong bao ro, KHONG tu ve CPU.
        (v7.23) Lop boc mong quanh ham tach dung chung
        tach_ai_tach_nen_va_giong (cung dung cho luong tach truoc
        khi long o tab Doc phu de): luu CA 2 file (nen + giong goc),
        log ghi ro ten card GPU that da dung.
        Chay tu worker _chay_tach_nen (luong phu). KHONG gioi han
        thoi gian (file 2 tieng chay CPU co the mat vai tieng) —
        chi co Huy (self._yeu_cau_huy) moi dung duoc. Model duoc
        kiem tra NGAY LUC TACH (khong phai chi luc mo tool) nen tai
        xong dung luon, khong can khoi dong lai tool."""
        # (v7.22) Quet GPU neu chua quet kip khi mo tab: quet day du
        # ngay tai day (thu that voi model) de biet chac GPU dung
        # duoc khong truoc khi giai ma file dai. Day len hang doi de
        # luong chinh cap nhat dong trang thai (worker KHONG cham
        # truc tiep vao Tk).
        che_do_tb = self._lay_thiet_bi_tach_ai()
        ket_qua_quet = getattr(self, "_ket_qua_quet_gpu", None)
        if ket_qua_quet is None:
            _tt, duong_model = trang_thai_model_ai(AI_TACH_MODELS[0])
            ket_qua_quet = quet_gpu_directml(
                duong_model if _tt == "co" else None)
            self._ket_qua_quet_gpu = ket_qua_quet
            self.hang_doi.put(("gpu_quet", ket_qua_quet))
        bitrate = self._lay_bitrate_mp3()
        ok, info, loi = tach_ai_tach_nen_va_giong(
            ffmpeg, goc, che_do_tb, ket_qua_quet, bitrate,
            log_cb=log, tien_trinh_cb=self._bao_tien_trinh,
            dung=self._yeu_cau_huy)
        if not ok:
            if loi == "đã hủy":
                log("Đã hủy tách nền.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if loi.startswith("Chưa có model AI"):
                log("LỖI: chưa có model AI để tách. Mở mục 'Tài nguyên "
                    "AI' ở ngay dưới phần Tách nền rồi bấm 'Tải' "
                    "(model ~64 MB, tải 1 lần dùng lại mãi). Tải xong "
                    "bấm lại 'Tách nền' — không cần khởi động lại tool.")
                self.hang_doi.put(
                    ("xong", False,
                     "Chưa có model AI — mở mục 'Tài nguyên AI' rồi bấm "
                     "'Tải' model, sau đó bấm lại 'Tách nền'."))
                self.hang_doi.put(("tai_nguyen", "cap_nhat", None))
                return
            if loi.startswith("Model AI bị sai"):
                log("LỖI: model AI bị sai (thiếu/sai nội dung). Mở mục "
                    "'Tài nguyên AI' rồi bấm 'Tải' để tải lại.")
                self.hang_doi.put(
                    ("xong", False,
                     "Model AI bị sai — mở mục 'Tài nguyên AI' rồi bấm "
                     "'Tải' để tải lại."))
                self.hang_doi.put(("tai_nguyen", "cap_nhat", None))
                return
            log("LỖI: %s" % loi)
            self.hang_doi.put(("xong", False, loi))
            return
        self.file_nen_lam_viec = info["nen"]
        self.file_giong_goc_lam_viec = info["giong_goc"]
        self.nen_tach_bitrate = bitrate
        if info["thiet_bi"] == "gpu":
            thiet_bi_txt = ("GPU — %s" % info["ten_card"]
                            if info.get("ten_card") else "GPU")
        else:
            thiet_bi_txt = "CPU"
        log("Đã tách xong file nền bằng AI (%s): %s (%s); giọng gốc: "
            "%s (%s)" % (thiet_bi_txt, info["nen"],
                         info["thong_tin_nen"], info["giong_goc"],
                         info["thong_tin_giong"]))
        self.hang_doi.put(("nen_xong", True, info["nen"]))
        self.hang_doi.put(("giong_goc_xong", True, info["giong_goc"]))

    def _do_am_luong_trung_binh(self, ffmpeg, duong):
        """(v7.21) Am luong trung binh toan file (volumedetect) — dung
        kiem tra file nen AI co cam khong. Tra ve float dB, None neu
        khong do duoc (bao gom ca Huy). Khong bao gio nem loi."""
        cmd = [ffmpeg, "-y", "-i", duong, "-map", "0:a",
               "-af", "volumedetect", "-f", "null", "-"]
        try:
            rc, err = _chay_ffmpeg_co_gioi_han(
                cmd, 1800, dung=self._yeu_cau_huy,
                nhan="đo âm lượng nền AI")
        except TimeoutError:
            return None
        if rc != 0:
            return None
        return _parse_mean_volume(err)

    # ----- (v7.22) thiet bi tach AI + quet GPU -----
    def _lay_thiet_bi_tach_ai(self):
        """Tra ve key thiet bi tach AI ('tu_dong'/'cpu'/'gpu'):
        doc tu combobox neu co, khong thi tu config."""
        try:
            hien = self.var_thiet_bi_tach_ai.get()
            for key, ten in GPU_TACH_AI_LUA_CHON.items():
                if ten == hien:
                    return key
        except Exception:
            pass
        try:
            che_do = (doc_config().get("ai_tach_thiet_bi")
                      or GPU_TACH_AI_MAC_DINH)
            if che_do in GPU_TACH_AI_LUA_CHON:
                return che_do
        except Exception:
            pass
        return GPU_TACH_AI_MAC_DINH

    def _ten_thiet_bi_tach_ai(self, key):
        return GPU_TACH_AI_LUA_CHON.get(
            key, GPU_TACH_AI_LUA_CHON[GPU_TACH_AI_MAC_DINH])

    def _doi_thiet_bi_tach_ai(self, _event=None):
        # (v7.22) Doi thiet bi tach AI: luu config ngay + cap nhat
        # dong trang thai (khong can quet lai — quet chi kiem tra
        # may, khong phu thuoc lua chon).
        try:
            luu_config(
                {"ai_tach_thiet_bi": self._lay_thiet_bi_tach_ai()})
        except Exception:
            pass
        try:
            self._cap_nhat_hien_thi_gpu(
                getattr(self, "_ket_qua_quet_gpu", None))
        except Exception:
            pass

    def _quet_gpu_nen(self):
        # (v7.22) Quet GPU o luong phu (UI khong dong): kiem tra thu
        # vien DirectML + card + thu that voi model neu da co.
        if getattr(self, "_dang_quet_gpu", False):
            return
        self._dang_quet_gpu = True
        try:
            self.var_trang_thai_gpu.set("GPU: đang quét máy...")
        except Exception:
            pass
        t = threading.Thread(target=self._chay_quet_gpu, daemon=True)
        t.start()

    def _chay_quet_gpu(self):
        try:
            model = AI_TACH_MODELS[0]
            _tt, duong_model = trang_thai_model_ai(model)
            ket_qua = quet_gpu_directml(
                duong_model if _tt == "co" else None)
        except Exception as e:
            ket_qua = {"co_thu_vien": False, "co_gpu": False,
                       "ten_gpu": None, "device_id": None,
                       "loi": "lỗi quét GPU: %s" % _tom_tat_loi(e),
                       "da_thu_voi_model": False}
        self.hang_doi.put(("gpu_quet", ket_qua))

    def _cap_nhat_hien_thi_gpu(self, ket_qua):
        # (v7.22) CHI goi tren luong chinh: cap nhat dong trang
        # thai GPU (ca o muc Tach nen lan muc Cai dat GPU dung
        # chung 1 StringVar).
        try:
            self.var_trang_thai_gpu.set(
                van_ban_trang_thai_gpu(
                    ket_qua, self._lay_thiet_bi_tach_ai()))
        except Exception:
            pass

    def _bam_cap_nhat_tool_gpu(self):
        # (v7.22) Thu vien GPU kem trong ban cai moi: bam thi chay
        # luong kiem tra cap nhat san co cua tool (tai ban Setup
        # moi ve) — khong tai rieng file .dll nao vao tool dang
        # chay (khong the, vi onnxruntime-directml cung ten goi
        # 'onnxruntime' voi ban CPU dang chay).
        try:
            if hasattr(self.quan_ly, "bam_kiem_tra_cap_nhat"):
                self.quan_ly.bam_kiem_tra_cap_nhat()
        except Exception:
            pass

    def _lay_thu_muc_tai_nguyen_ai(self):
        # (v7.21) Thu muc tai nguyen AI: config ai_tach_thu_muc, neu
        # chua chon thi <thu muc luu>\TaiNguyenAI.
        try:
            cfg = doc_config()
            p = (cfg.get("ai_tach_thu_muc") or "").strip()
            if p:
                return p
        except Exception:
            pass
        return thu_muc_tai_nguyen_ai_mac_dinh()

    def _cap_nhat_trang_thai_tai_nguyen_ai(self):
        # (v7.21) Chi goi tren luong chinh: hien "Đã có / Chưa có /
        # Sai" + bat/tat nut Tai cho tung model.
        try:
            thu_muc = self._lay_thu_muc_tai_nguyen_ai()
            for model in AI_TACH_MODELS:
                lb_tt, btn = self._ai_model_widgets[model["id"]]
                tt, _p = trang_thai_model_ai(model, thu_muc)
                if tt == "co":
                    lb_tt.configure(text="Đã có", fg="green")
                    btn.configure(state="disabled")
                elif tt == "sai":
                    lb_tt.configure(text="Sai — bấm Tải lại",
                                    fg="orange")
                    btn.configure(
                        state="normal" if not self._dang_tai_model
                        else "disabled")
                else:
                    lb_tt.configure(text="Chưa có", fg="red")
                    btn.configure(
                        state="normal" if not self._dang_tai_model
                        else "disabled")
            # (v7.22) Hang thu vien GPU: trang thai theo ket qua
            # quet (chua quet xong thi "Đang quét...").
            try:
                ket_qua = getattr(self, "_ket_qua_quet_gpu", None)
                if ket_qua is None:
                    self.lb_gpu_thu_vien.configure(
                        text="Đang quét...", fg="gray")
                    self.btn_gpu_cap_nhat.configure(state="disabled")
                elif ket_qua.get("co_thu_vien"):
                    self.lb_gpu_thu_vien.configure(
                        text="Đã có (kèm trong tool)", fg="green")
                    self.btn_gpu_cap_nhat.configure(state="disabled")
                else:
                    self.lb_gpu_thu_vien.configure(
                        text="Chưa có — cần cập nhật tool", fg="red")
                    self.btn_gpu_cap_nhat.configure(state="normal")
            except Exception:
                pass
            if hasattr(self, "var_thu_muc_ai"):
                self.var_thu_muc_ai.set(thu_muc)
        except Exception:
            pass

    def _chon_thu_muc_tai_nguyen_ai(self):
        # (v7.21) Chon thu muc chua model AI (luu config, khong ep C:).
        from tkinter import filedialog
        thu_muc = filedialog.askdirectory(
            title="Chọn thư mục tài nguyên AI",
            initialdir=self._lay_thu_muc_tai_nguyen_ai())
        if not thu_muc:
            return
        try:
            cfg = doc_config()
            cfg["ai_tach_thu_muc"] = thu_muc
            luu_config(cfg)
        except Exception:
            pass
        self._cap_nhat_trang_thai_tai_nguyen_ai()
        self.hang_doi.put(("log", "Thư mục tài nguyên AI: %s" % thu_muc))

    def _mo_thu_muc_tai_nguyen_ai(self):
        # (v7.21) Mo thu muc tai nguyen AI bang trinh quan ly file.
        thu_muc = self._lay_thu_muc_tai_nguyen_ai()
        try:
            os.makedirs(thu_muc, exist_ok=True)
        except Exception:
            pass
        if os.path.isdir(thu_muc):
            mo_thu_muc(thu_muc)
        else:
            messagebox.showinfo(APP_TITLE,
                                "Thư mục tài nguyên AI:\n" + thu_muc)

    def _huy_tai_model_ai(self):
        # (v7.21) Huy tai model AI (su kien rieng — khong dung chung
        # _yeu_cau_huy cua tac vu tach/gop de khong huy lan nhau).
        try:
            self._yeu_cau_huy_tai.set()
        except Exception:
            pass

    def _bam_tai_model_ai(self, model):
        # (v7.21) Bam Tai: chay tai xuong o luong phu (UI khong dong),
        # tien trinh bao ve thanh rieng o muc Tai nguyen AI.
        if getattr(self, "_dang_tai_model", False):
            return
        self._dang_tai_model = True
        try:
            self._yeu_cau_huy_tai.clear()
        except Exception:
            pass
        self._cap_nhat_trang_thai_tai_nguyen_ai()
        try:
            self.btn_huy_tai.configure(state="normal")
        except Exception:
            pass
        self.hang_doi.put(("tai_nguyen", "trang_thai",
                           "Đang chuẩn bị tải %s..." % model["ten"]))
        t = threading.Thread(target=self._chay_tai_model_ai,
                             args=(model,), daemon=True)
        t.start()

    def _chay_tai_model_ai(self, model):
        # (v7.21) Worker tai model: toi da 2 lan thu (tai lai 1 lan
        # neu loi), kiem tra kich thuoc + sha256 roi moi doi ten ve
        # file chinh (atomic). Tai xong dung luon — KHONG can khoi
        # dong lai tool (model duoc kiem tra ngay luc tach).
        def bao_trang_thai(s):
            self.hang_doi.put(("tai_nguyen", "trang_thai", s))

        def bao_tien_trinh(pct):
            self.hang_doi.put(("tai_nguyen", "tien_trinh", pct))

        try:
            thu_muc = self._lay_thu_muc_tai_nguyen_ai()
            try:
                os.makedirs(thu_muc, exist_ok=True)
            except Exception as e:
                bao_trang_thai("LỖI: không tạo được thư mục tài nguyên: %s"
                               % _tom_tat_loi(e))
                self.hang_doi.put(("tai_nguyen", "xong", False,
                                   "Không tạo được thư mục tài nguyên."))
                return
            dich = duong_dan_model_ai(model, thu_muc)
            tam = dich + ".tmp"
            tt, _p = trang_thai_model_ai(model, thu_muc)
            if tt == "co":
                bao_trang_thai("Model đã có sẵn, không cần tải lại.")
                self.hang_doi.put(("tai_nguyen", "xong", True,
                                   "Model đã có sẵn."))
                return
            for lan in (1, 2):
                bao_trang_thai("Đang tải %s (lần %d/2)..."
                               % (model["ten"], lan))
                bao_tien_trinh(0.0)

                def cb(da, tong):
                    if tong:
                        bao_tien_trinh(100.0 * da / tong)
                    else:
                        bao_tien_trinh(None)

                ok, loi = tai_file_co_tien_trinh(
                    model["url"], tam, tien_trinh_cb=cb,
                    dung=self._yeu_cau_huy_tai)
                if not ok:
                    if loi == "đã hủy":
                        bao_trang_thai("Đã hủy tải model.")
                        self.hang_doi.put(("tai_nguyen", "xong", False,
                                           "Đã hủy tải model."))
                        return
                    _xoa_file_quiet(tam)
                    if lan == 1:
                        bao_trang_thai("Tải lỗi (%s) — thử lại lần 2..."
                                       % loi)
                        continue
                    bao_trang_thai("LỖI: tải model thất bại sau 2 lần: %s"
                                   % loi)
                    self.hang_doi.put(("tai_nguyen", "xong", False,
                                       "Tải model thất bại: %s" % loi))
                    return
                # Kiem tra kich thuoc + hash truoc khi doi ten.
                try:
                    if os.path.getsize(tam) != int(model["size"]):
                        raise ValueError(
                            "sai kích thước (được %d, cần %d)"
                            % (os.path.getsize(tam),
                               int(model["size"])))
                    if _sha256_file(tam) != str(model["sha256"]).lower():
                        raise ValueError("sai nội dung (sha256 không khớp)")
                except Exception as e:
                    _xoa_file_quiet(tam)
                    if lan == 1:
                        bao_trang_thai("File tải về bị sai (%s) — "
                                       "tải lại lần 2..."
                                       % _tom_tat_loi(e))
                        continue
                    bao_trang_thai("LỖI: file tải về bị sai sau 2 lần: %s"
                                   % _tom_tat_loi(e))
                    self.hang_doi.put(("tai_nguyen", "xong", False,
                                       "File tải về bị sai: %s"
                                       % _tom_tat_loi(e)))
                    return
                try:
                    os.replace(tam, dich)
                except Exception as e:
                    _xoa_file_quiet(tam)
                    bao_trang_thai("LỖI: không lưu được model: %s"
                                   % _tom_tat_loi(e))
                    self.hang_doi.put(("tai_nguyen", "xong", False,
                                       "Không lưu được model: %s"
                                       % _tom_tat_loi(e)))
                    return
                bao_tien_trinh(100.0)
                bao_trang_thai("Đã tải xong %s (%.1f MB) — dùng được "
                               "ngay, không cần khởi động lại tool."
                               % (model["ten"],
                                  model["size"] / 1048576.0))
                self.hang_doi.put(("tai_nguyen", "xong", True,
                                   "Đã tải xong %s." % model["ten"]))
                return
        except Exception as e:
            # Loi khong luong truoc: van bao "xong" de mo lai nut Tai
            # (co nay chi ha o handler "xong" tren luong chinh).
            bao_trang_thai("LỖI: tải model lỗi không lường trước: %s"
                           % _tom_tat_loi(e))
            self.hang_doi.put(("tai_nguyen", "xong", False,
                               "Tải model lỗi: %s" % _tom_tat_loi(e)))
        finally:
            self.hang_doi.put(("tai_nguyen", "cap_nhat", None))

    # ----- (4) nghe thu -----
    def _bam_nghe_thu(self):
        if self.dang_chay:
            return
        nen = self._lay_file_nen()
        if not nen:
            messagebox.showerror(
                APP_TITLE,
                "Chưa có file nền — bấm 'Tách nền' trước (hoặc chọn "
                "chế độ 'Giữ nguyên, chỉ chỉnh âm lượng' rồi bấm "
                "'Tách nền').")
            return
        try:
            bat_dau = float(str(self.var_nghe_tu.get()).strip())
        except Exception:
            bat_dau = 0.0
        bat_dau = max(0.0, bat_dau)
        self._bat_dau_tac_vu("Đang nghe thử (30 giây)")
        t = threading.Thread(target=self._chay_nghe_thu,
                             args=(nen, bat_dau), daemon=True)
        t.start()

    def _chay_nghe_thu(self, nen, bat_dau):
        def log(s):
            self.hang_doi.put(("log", s))
            # (v7.18) Loi am thanh rieng biet (xem _chay_tach_nen).
            if s.startswith(("LỖI", "CẢNH BÁO")):
                dong_dau = s.split("\n", 1)[0]
                duoi = s.split("\n", 1)[1] if "\n" in s else ""
                ghi_loi_am_thanh("nghe thử", dong_dau, nen, duoi)
        tam = None
        try:
            ffmpeg = tim_ffmpeg()
            if not ffmpeg:
                log("LỖI: không tìm thấy ffmpeg trên máy.")
                self.hang_doi.put(("xong", False,
                                   "Không tìm thấy ffmpeg."))
                return
            voice = self.e_voice.get().strip()
            co_voice = bool(voice and os.path.isfile(voice))
            vol_voice = self._lay_am_luong(self.var_vol_voice) / 100.0
            vol_nen = self._lay_am_luong(self.var_vol_nen) / 100.0
            # (v7.23) Giong goc track thu 3 (neu co file).
            giong_goc = self._lay_file_giong_goc()
            vol_giong_goc = (self._lay_am_luong(self.var_vol_giong_goc)
                             / 100.0)
            tam = os.path.join(os.path.dirname(nen) or ".",
                               "_nghe-thu-gop.wav")
            if co_voice:
                if giong_goc:
                    log("Đang trộn thử 30 giây (từ %.1fs): voice + nền "
                        "+ giọng gốc..." % bat_dau)
                else:
                    log("Đang trộn thử 30 giây (từ %.1fs): voice + nền..."
                        % bat_dau)
                cmd = lenh_nghe_thu_gop(ffmpeg, voice, nen, tam, bat_dau,
                                        30, vol_voice, vol_nen,
                                        giong_goc, vol_giong_goc)
            else:
                log("Chưa chọn file voice — chỉ nghe thử nền 30 giây "
                    "(từ %.1fs)..." % bat_dau)
                cmd = lenh_nghe_thu_nen(ffmpeg, nen, tam, bat_dau, 30,
                                        vol_nen)
            try:
                rc, err = _chay_ffmpeg_co_gioi_han(
                    cmd, 120, dung=self._yeu_cau_huy, nhan="nghe thử")
            except TimeoutError:
                log("LỖI: trộn thử hết thời gian chờ.")
                self.hang_doi.put(("xong", False,
                                   "Trộn thử hết thời gian chờ."))
                return
            if rc == -1:
                log("Đã hủy nghe thử.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if rc != 0 or not (os.path.isfile(tam)
                               and os.path.getsize(tam) > 0):
                tail = (err or "").strip()[-600:]
                log("LỖI: trộn thử lỗi (mã %s).%s"
                    % (rc, ("\n" + tail) if tail else ""))
                self.hang_doi.put(("xong", False,
                                   "Trộn thử lỗi (mã %s)." % rc))
                return
            # (v7.17) Cua chat luong: file nghe thu phai giai ma duoc
            # tron ven moi phat ra loa (khong phat file loi).
            ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
                tam, ffmpeg, "wav")
            if not ok:
                log("CẢNH BÁO: file nghe thử không đạt chuẩn: %s"
                    % thong_tin)
                self.hang_doi.put(("xong", False,
                                   "File nghe thử không đạt chuẩn: %s"
                                   % thong_tin))
                return
            log("Đang phát thử ra loa (30 giây)...")
            ok, loi = _phat_mp3(tam, dung=self._yeu_cau_huy)
            if not ok:
                log("LỖI phát thử: %s" % loi)
                self.hang_doi.put(("xong", False,
                                   "Không phát được: %s" % loi))
                return
            log("Đã nghe thử xong.")
            self.hang_doi.put(("xong", True,
                               "Đã nghe thử xong (30 giây)."))
        except Exception as e:
            log("LỖI nghe thử: %s" % _tom_tat_loi(e))
            self.hang_doi.put(("xong", False,
                               "Lỗi: %s" % _tom_tat_loi(e)))
        finally:
            if tam:
                _xoa_file_quiet(tam)

    # ----- (5) luu nen -----
    def _bam_luu_nen(self):
        if self.dang_chay:
            return
        nen = self._lay_file_nen()
        if not nen:
            messagebox.showerror(
                APP_TITLE,
                "Chưa có file nền — bấm 'Tách nền' trước (hoặc chọn "
                "chế độ 'Giữ nguyên, chỉ chỉnh âm lượng' rồi bấm "
                "'Tách nền').")
            return
        self._bat_dau_tac_vu("Đang lưu nền")
        t = threading.Thread(target=self._chay_luu_nen, args=(nen,),
                             daemon=True)
        t.start()

    def _chay_luu_nen(self, nen):
        def log(s):
            self.hang_doi.put(("log", s))
            # (v7.18) Loi am thanh rieng biet (xem _chay_tach_nen).
            if s.startswith(("LỖI", "CẢNH BÁO")):
                dong_dau = s.split("\n", 1)[0]
                duoi = s.split("\n", 1)[1] if "\n" in s else ""
                ghi_loi_am_thanh("lưu nền", dong_dau, nen, duoi)
        try:
            ffmpeg = tim_ffmpeg()
            if not ffmpeg:
                log("LỖI: không tìm thấy ffmpeg trên máy.")
                self.hang_doi.put(("xong", False,
                                   "Không tìm thấy ffmpeg."))
                return
            dinh_dang = self._lay_dinh_dang()
            vol_nen = self._lay_am_luong(self.var_vol_nen) / 100.0
            goc = self.file_goc or nen
            out_path = ten_file_nen_da_luu(goc, dinh_dang)
            bitrate = self._lay_bitrate_mp3()
            # (v7.17) Nen lam viec da la MP3 tach san, dung bitrate da
            # chon, dinh dang MP3, am luong 100% thi COPY thang (khong
            # encode lai them 1 pass vo ich); con lai encode qua
            # lenh_luu_nen de ap am luong/dinh dang.
            copy_thang = (dinh_dang == "mp3"
                          and abs(vol_nen - 1.0) < 0.001
                          and str(nen).endswith("_nen-tach.mp3")
                          and bitrate == (self.nen_tach_bitrate or ""))
            if copy_thang:
                log("Lưu nền: copy thẳng file nền MP3 đã tách "
                    "(không encode lại).")
                try:
                    shutil.copy2(nen, out_path)
                except Exception as e:
                    log("LỖI: không copy được file nền: %s" % e)
                    self.hang_doi.put(
                        ("xong", False,
                         "Không copy được file nền: %s" % e))
                    return
                ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
                    out_path, ffmpeg, dinh_dang,
                    self._lay_bitrate_mong_bps())
                if not ok:
                    log("CẢNH BÁO: file nền ra không đúng chuẩn: %s"
                        % thong_tin)
                    self.hang_doi.put(("xong", False,
                                       "File nền ra không đúng chuẩn: %s"
                                       % thong_tin))
                    return
                self.file_ket_qua = out_path
                log("XONG: đã lưu nền: %s (%s)" % (out_path, thong_tin))
                self.hang_doi.put(("xong", True, out_path))
                return
            ffprobe = tim_ffprobe(ffmpeg)
            tong_giay = lay_thoi_luong(ffprobe, nen) if ffprobe else None
            timeout_giay = (max(300, int(tong_giay) * 3 + 120)
                            if tong_giay else 600)
            log("Đang lưu nền (âm lượng nền %.0f%%): %s"
                % (vol_nen * 100, out_path))
            cmd = lenh_luu_nen(ffmpeg, nen, out_path, vol_nen, dinh_dang,
                               bitrate)
            try:
                rc, err = _chay_ffmpeg_co_tien_trinh(
                    cmd, timeout_giay, tong_giay,
                    tien_trinh_cb=self._bao_tien_trinh,
                    dung=self._yeu_cau_huy, nhan="lưu nền")
            except TimeoutError:
                log("LỖI: lưu nền hết thời gian chờ (%ds)." % timeout_giay)
                self.hang_doi.put(("xong", False,
                                   "Lưu nền hết thời gian chờ."))
                return
            if rc == -1:
                log("Đã hủy lưu nền.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if rc != 0 or not (os.path.isfile(out_path)
                               and os.path.getsize(out_path) > 0):
                tail = (err or "").strip()[-600:]
                _ghi_log_loi_ffmpeg(os.path.dirname(out_path) or ".",
                                    tail or "ffmpeg lỗi không rõ")
                log("LỖI: ffmpeg lưu nền lỗi (mã %s).%s"
                    % (rc, ("\n" + tail) if tail else ""))
                self.hang_doi.put(
                    ("xong", False,
                     "ffmpeg lưu nền lỗi (mã %s), xem ffmpeg-loi.log."
                     % rc))
                return
            ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
                out_path, ffmpeg, dinh_dang,
                self._lay_bitrate_mong_bps())
            if not ok:
                log("CẢNH BÁO: file nền ra không đúng chuẩn: %s"
                    % thong_tin)
                self.hang_doi.put(("xong", False,
                                   "File nền ra không đúng chuẩn: %s"
                                   % thong_tin))
                return
            self.file_ket_qua = out_path
            log("XONG: đã lưu nền: %s (%s)" % (out_path, thong_tin))
            self.hang_doi.put(("xong", True, out_path))
        except Exception as e:
            log("LỖI lưu nền: %s" % _tom_tat_loi(e))
            self.hang_doi.put(("xong", False,
                               "Lỗi: %s" % _tom_tat_loi(e)))

    # ----- (6) gop voi voice -----
    def _bam_gop(self):
        if self.dang_chay:
            return
        nen = self._lay_file_nen()
        if not nen:
            messagebox.showerror(
                APP_TITLE,
                "Chưa có file nền — bấm 'Tách nền' trước (hoặc chọn "
                "chế độ 'Giữ nguyên, chỉ chỉnh âm lượng' rồi bấm "
                "'Tách nền').")
            return
        voice = self.e_voice.get().strip()
        if not voice or not os.path.isfile(voice):
            messagebox.showerror(
                APP_TITLE,
                "Chưa chọn file voice HoaiMy (hoặc file không tồn "
                "tại).")
            return
        self._bat_dau_tac_vu("Đang gộp thành file voice-sub")
        t = threading.Thread(target=self._chay_gop, args=(nen, voice),
                             daemon=True)
        t.start()

    def _chay_gop(self, nen, voice):
        def log(s):
            self.hang_doi.put(("log", s))
            # (v7.18) Loi am thanh rieng biet (xem _chay_tach_nen).
            if s.startswith(("LỖI", "CẢNH BÁO")):
                dong_dau = s.split("\n", 1)[0]
                duoi = s.split("\n", 1)[1] if "\n" in s else ""
                ghi_loi_am_thanh("trộn", dong_dau, voice, duoi)
        try:
            ffmpeg = tim_ffmpeg()
            if not ffmpeg:
                log("LỖI: không tìm thấy ffmpeg trên máy.")
                self.hang_doi.put(("xong", False,
                                   "Không tìm thấy ffmpeg."))
                return
            dinh_dang = self._lay_dinh_dang()
            vol_voice = self._lay_am_luong(self.var_vol_voice) / 100.0
            vol_nen = self._lay_am_luong(self.var_vol_nen) / 100.0
            # (v7.23) Giong goc track thu 3 (neu co file).
            giong_goc = self._lay_file_giong_goc()
            vol_giong_goc = (self._lay_am_luong(self.var_vol_giong_goc)
                             / 100.0)
            out_path = ten_file_gop_am_thanh(voice, dinh_dang)
            ffprobe = tim_ffprobe(ffmpeg)
            tong_giay = 0
            if ffprobe:
                for f in (voice, nen) + ((giong_goc,)
                                         if giong_goc else ()):
                    d = lay_thoi_luong(ffprobe, f)
                    if d:
                        tong_giay = max(tong_giay, d)
            log("Voice: %s" % voice)
            log("Nền: %s" % nen)
            if giong_goc:
                log("Giọng gốc: %s" % giong_goc)
            if tong_giay:
                log("Thời lượng dài nhất: %.1fs" % tong_giay)
            log("Âm lượng: voice %.0f%%, nền %.0f%%"
                % (vol_voice * 100, vol_nen * 100))
            if giong_goc:
                log("Âm lượng giọng gốc: %.0f%%"
                    % (vol_giong_goc * 100))
            cmd = lenh_gop_am_thanh(ffmpeg, voice, nen, out_path,
                                    vol_voice, vol_nen, dinh_dang,
                                    self._lay_bitrate_mp3(),
                                    giong_goc, vol_giong_goc)
            timeout_giay = (max(300, int(tong_giay) * 3 + 120)
                            if tong_giay else 600)
            try:
                rc, err = _chay_ffmpeg_co_tien_trinh(
                    cmd, timeout_giay, tong_giay,
                    tien_trinh_cb=self._bao_tien_trinh,
                    dung=self._yeu_cau_huy, nhan="gộp voice-sub")
            except TimeoutError:
                log("LỖI: gộp hết thời gian chờ (%ds)." % timeout_giay)
                self.hang_doi.put(("xong", False,
                                   "Gộp hết thời gian chờ."))
                return
            if rc == -1:
                log("Đã hủy gộp.")
                self.hang_doi.put(("xong", False, "Đã hủy."))
                return
            if rc != 0 or not (os.path.isfile(out_path)
                               and os.path.getsize(out_path) > 0):
                tail = (err or "").strip()[-600:]
                _ghi_log_loi_ffmpeg(os.path.dirname(out_path) or ".",
                                    tail or "ffmpeg lỗi không rõ")
                log("LỖI: ffmpeg gộp lỗi (mã %s).%s"
                    % (rc, ("\n" + tail) if tail else ""))
                self.hang_doi.put(
                    ("xong", False,
                     "ffmpeg gộp lỗi (mã %s), xem ffmpeg-loi.log." % rc))
                return
            ok, thong_tin = _kiem_tra_chat_luong_am_thanh(
                out_path, ffmpeg, dinh_dang,
                self._lay_bitrate_mong_bps())
            if not ok:
                log("CẢNH BÁO: file ra không đúng chuẩn gộp: %s"
                    % thong_tin)
                self.hang_doi.put(("xong", False,
                                   "File ra không đúng chuẩn: %s"
                                   % thong_tin))
                return
            do_dai = (lay_thoi_luong(ffprobe, out_path)
                      if ffprobe else None)
            self.file_ket_qua = out_path
            log("XONG: %s (%s%s)"
                % (out_path, thong_tin,
                   (", dài %.1fs" % do_dai) if do_dai else ""))
            self.hang_doi.put(("xong", True, out_path))
        except Exception as e:
            log("LỖI gộp: %s" % _tom_tat_loi(e))
            self.hang_doi.put(("xong", False,
                               "Lỗi: %s" % _tom_tat_loi(e)))

    # ----- hang doi / huy / mo thu muc -----
    def _xu_ly_hang_doi(self):
        try:
            while True:
                muc = self.hang_doi.get_nowait()
                if muc[0] == "log":
                    self.txt_log.insert("end", muc[1] + "\n")
                    self.txt_log.see("end")
                elif muc[0] == "tien_trinh":
                    # (v7.20) Cap nhat thanh tien trinh (luong chinh).
                    if muc[1] == "dat":
                        self._dat_tien_trinh(muc[2])
                    elif muc[1] == "khong_ro":
                        self._tien_trinh_khong_ro()
                    elif muc[1] == "reset":
                        self._dat_lai_tien_trinh()
                elif muc[0] == "nen_xong":
                    self.dang_chay = False
                    self._khoa_nut(False)
                    if muc[1]:
                        self.lb_nen_hien_tai.configure(
                            text="File nền hiện tại: " + muc[2])
                        self.lb_trang_thai.configure(
                            text="Đã có file nền.")
                        self._dat_tien_trinh(100.0)  # (v7.20)
                    else:
                        self.lb_trang_thai.configure(text=muc[2])
                        self._dat_lai_tien_trinh()  # (v7.20)
                elif muc[0] == "giong_goc_xong":
                    # (v7.23) Tach AI xong: tu dien file giong goc
                    # vua tach vao o nhap (chi dien khi o dang trong
                    # hoac file cu khong con — khong ghi de file cau
                    # da chon tay).
                    if muc[1]:
                        try:
                            hien = self.e_giong_goc.get().strip()
                        except Exception:
                            hien = ""
                        if not hien or not os.path.isfile(hien):
                            # (v7.24, H1) Dien bang helper: o chi doc
                            # bo qua delete/insert truc tiep im lang;
                            # helper mo tam, dien xong tra lai readonly
                            # + cap nhat ghi chu ("Đã tách xong — ...").
                            self._dien_o_giong_goc(muc[2])
                elif muc[0] == "xong":
                    self.dang_chay = False
                    self._khoa_nut(False)
                    if muc[1]:
                        self.lb_trang_thai.configure(text="Đã xong.")
                        self.lb_ket_qua.configure(
                            text="File đã tạo: " + muc[2])
                        self._dat_tien_trinh(100.0)  # (v7.20)
                    else:
                        self.lb_trang_thai.configure(text=muc[2])
                        self._dat_lai_tien_trinh()  # (v7.20)
                elif muc[0] == "gpu_quet":
                    # (v7.22) Ket qua quet GPU (luong phu gui ve):
                    # luu lai + cap nhat dong trang thai + hang thu
                    # vien GPU. Chi chay tren luong chinh.
                    self._ket_qua_quet_gpu = muc[1]
                    self._dang_quet_gpu = False
                    self._cap_nhat_hien_thi_gpu(muc[1])
                    self._cap_nhat_trang_thai_tai_nguyen_ai()
                elif muc[0] == "tai_nguyen":
                    # (v7.21) Tai model AI: chi chay tren luong chinh.
                    if muc[1] == "tien_trinh":
                        pct = muc[2]
                        try:
                            if pct is None:
                                if str(self.thanh_tien_trinh_tai["mode"]) \
                                        != "indeterminate":
                                    self.thanh_tien_trinh_tai.configure(
                                        mode="indeterminate")
                                self.thanh_tien_trinh_tai.start(200)
                                self.lb_phan_tram_tai.configure(text="…")
                            else:
                                p = max(0.0, min(100.0, float(pct)))
                                if str(self.thanh_tien_trinh_tai["mode"]) \
                                        != "determinate":
                                    self.thanh_tien_trinh_tai.stop()
                                    self.thanh_tien_trinh_tai.configure(
                                        mode="determinate")
                                self.thanh_tien_trinh_tai["value"] = p
                                self.lb_phan_tram_tai.configure(
                                    text="%d%%" % int(round(p)))
                        except Exception:
                            pass
                    elif muc[1] == "trang_thai":
                        try:
                            self.lb_trang_thai_tai.configure(text=muc[2])
                        except Exception:
                            pass
                    elif muc[1] == "xong":
                        # (v7.21) Co "xong" moi ha co _dang_tai_model
                        # (chay tren luong chinh, cung luc cap nhat
                        # thanh/nhan) — tranh truong hop luong phu ha co
                        # truoc khi hang doi duoc xu ly, UI chua kip
                        # doi ma test/nguoi dung da thay "xong".
                        self._dang_tai_model = False
                        try:
                            self.thanh_tien_trinh_tai.stop()
                        except Exception:
                            pass
                        try:
                            self.thanh_tien_trinh_tai.configure(
                                mode="determinate")
                            self.thanh_tien_trinh_tai["value"] = (
                                100.0 if muc[2] else 0.0)
                            self.lb_phan_tram_tai.configure(
                                text="100%" if muc[2] else "0%")
                            self.btn_huy_tai.configure(state="disabled")
                        except Exception:
                            pass
                        if muc[2]:
                            try:
                                self.lb_trang_thai_tai.configure(
                                    text=muc[3])
                            except Exception:
                                pass
                        if muc[2]:
                            # (v7.22) Tai xong model -> quet lai GPU
                            # de thu that voi model (cap nhat trang
                            # thai "san sang" neu card chay duoc).
                            self._quet_gpu_nen()
                    elif muc[1] == "cap_nhat":
                        self._cap_nhat_trang_thai_tai_nguyen_ai()
        except queue.Empty:
            pass
        self.after(200, self._xu_ly_hang_doi)

    def _bam_huy(self):
        self._yeu_cau_huy.set()

    def _mo_thu_muc_ket_qua(self):
        thu_muc = None
        if self.file_ket_qua:
            thu_muc = os.path.dirname(self.file_ket_qua)
        if not thu_muc:
            v = self.e_goc.get().strip()
            if v:
                thu_muc = os.path.dirname(v)
        if thu_muc and os.path.isdir(thu_muc):
            mo_thu_muc(thu_muc)


class CuaSoVoiceFaceless(tk.Frame):  # (v7.13) Frame trong Notebook, khong Toplevel
    """Tab 'Voice for YouTube Faceless': dan 1 JSON (CHINH: dual
    {en, vi}, fallback: 1 ngon ngu / bare cues / file .srt) -> tool
    tu set giong/toc do, doc tung cue SRT bang Edge TTS (giong
    Muse Helio/Aria duoc anh xa sang Edge tuong duong va log ro),
    do thoi luong that tung cue roi can lai SRT, gop MP3 ve chuan
    44100/stereo/192k/libmp3lame. Thumbnail KHONG lam o day."""

    def __init__(self, quan_ly, parent=None):
        super().__init__(parent if parent is not None else quan_ly)
        self.quan_ly = quan_ly
        self.cfg = doc_config()
        self.du_lieu = {}  # {en:{...}, vi:{...}} sau khi parse JSON
        self.che_do_json = {"mode": "chua_co", "languages": [], "nguon": "chua_co", "canh_bao": []}
        self.cot_duoc_bat = []  # cot nao duoc BAT theo mode JSON
        self.col = {}  # (v7.15) setting/tien do/log RIENG tung cot {en, vi}
        self.dang_chay = False
        self._yeu_cau_huy = threading.Event()
        # (v7.14) Job doc lap tung ngon ngu: state rieng, stop rieng,
        # thread rieng. Dung/huy/loi EN khong cham VI va nguoc lai.
        self.jobs = {lang: ytf_tao_job(lang) for lang in ("en", "vi")}
        self._stop_events = {lang: threading.Event() for lang in ("en", "vi")}
        self._threads = {}
        self._retry_chi = {}  # (v7.16) cue chi goi lai theo ngon ngu {lang: {index}}
        self._nghe_thu_token = 0  # (v7.19) phien nghe thu giong gan nhat
        self._nghe_thu_dung = None  # (v7.19) Event dung preview dang chay
        self.hang_doi = queue.Queue()
        self._dung_ui()
        self.after(200, self._xu_ly_hang_doi)

    # ----- giao dien -----
    def _dung_ui(self):
        pad = {"padx": 8, "pady": 4}
        # (v7.19) Boc TOAN BO tab trong khung cuon doc (Canvas +
        # Scrollbar, cung mau _tao_khung_cuon cua tab Duyet video):
        # man hinh 1080p van lan chuot / keo thanh cuon xuong toi
        # o log cuoi tab. Moi widget ben duoi pack vao noi_dung.
        self._khung_cuon_ngoai, noi_dung = self._tao_khung_cuon(self)
        self._khung_cuon_ngoai.pack(fill="both", expand=True)
        self._khung_noi_dung = noi_dung
        tk.Label(noi_dung, text="Voice for YouTube Faceless — dán 1 JSON (dual EN+VI là chính) rồi ấn Áp dụng JSON. Tool đọc từng cue SRT, không đọc một hơi.",
                 wraplength=980, justify="left").pack(fill="x", **pad)
        tk.Label(noi_dung, text="LƯU Ý GIỌNG MUSE: Helio (avocado_v2:MAI_03) và Aria (avocado_v2:MAI_01) là giọng nội bộ của Muse, KHÔNG chạy native trên Windows. Trong tab này Helio → en-US-ChristopherNeural, Aria (Muse) → en-US-AriaNeural (Edge) và tool log rõ việc ánh xạ. Audio Helio đầy đủ chỉ tạo được trong chat Muse.",
                 wraplength=980, justify="left", fg="red").pack(fill="x", **pad)
        tk.Label(noi_dung, text="SONG NGỮ ĐỘC LẬP: bản Anh và bản Việt trong cùng 1 JSON KHÔNG phải dịch y hệt nhau. Mỗi bản là 1 kịch bản riêng — phong cách, nhịp kể, chương và thời lượng riêng cho khán giả từng nước, chỉ chung 1 key/chủ đề. Tab xử lý 2 bản độc lập, xuất MP3 + SRT final riêng từng ngôn ngữ; video dựng từ 2 voice này cũng khác nhau, chỉ dùng chung kiểu người que Stickman 2D.",
                 wraplength=980, justify="left").pack(fill="x", **pad)

        # (v7.15) Hang dung: che do JSON tu nhan + cong tac song song.
        f0 = tk.Frame(noi_dung)
        f0.pack(fill="x", **pad)
        self.lb_che_do = tk.Label(f0, text="Chế độ JSON: chưa có — dán JSON rồi ấn Áp dụng JSON, tool tự nhận mode (dual / chỉ EN / chỉ VI) và tự bật/tắt cột.",
                                  wraplength=980, justify="left", fg="blue")
        self.lb_che_do.pack(side="left", padx=4)
        tk.Label(f0, text="Xem kịch bản:").pack(side="left", padx=4)
        self.cb_ngon_ngu = ttk.Combobox(f0, values=["en", "vi"], state="readonly", width=6)
        self.cb_ngon_ngu.set(self.cfg.get("ytf_ngon_ngu", "en"))
        self.cb_ngon_ngu.pack(side="left", padx=4)
        self.cb_ngon_ngu.bind("<<ComboboxSelected>>", lambda e: self._doi_ngon_ngu())
        self.var_song_song = tk.BooleanVar(value=bool(self.cfg.get("ytf_song_song", YTF_SONG_SONG_MAC_DINH)))
        tk.Checkbutton(f0, text="Song song EN+VI: BẬT = 2 luồng độc lập, TẮT = tuần tự",
                       variable=self.var_song_song, command=self._doi_song_song).pack(side="left", padx=4)
        tk.Label(f0, text="Số luồng tối đa:").pack(side="left", padx=4)
        self.cb_dong_bo = ttk.Combobox(f0, values=["1", "2"], state="readonly", width=4)
        self.cb_dong_bo.set(str(int(self.cfg.get("ytf_dong_bo_toi_da", YTF_DONG_BO_TOI_DA_MAC_DINH))))
        self.cb_dong_bo.pack(side="left", padx=4)
        self.cb_dong_bo.bind("<<ComboboxSelected>>", lambda e: self._luu_cau_hinh())

        # (v7.19) O DAN JSON LEN TREN CUNG: ngay duoi hang che do,
        # truoc ca 2 cot EN/VI — mo tab la thay ngay, khong can cuon.
        self.lb_json = tk.Label(noi_dung, text="JSON AI trả về (dual {en, vi} là chính; 1 ngôn ngữ / bare cues / .srt vẫn nhận):")
        self.lb_json.pack(fill="x", **pad)
        self.txt_json = scrolledtext.ScrolledText(noi_dung, height=8)
        self.txt_json.pack(fill="x", **pad)
        f3 = tk.Frame(noi_dung)
        f3.pack(fill="x", **pad)
        tk.Button(f3, text="Áp dụng JSON", command=self._ap_dung_json).pack(side="left", padx=4)
        tk.Button(f3, text="Dán từ clipboard rồi áp dụng", command=self._dan_clipboard).pack(side="left", padx=4)
        tk.Button(f3, text="Mở file .srt", command=self._mo_file_srt).pack(side="left", padx=4)
        tk.Button(f3, text="Tạo audio (EN+VI nếu có)", command=self._tao_audio).pack(side="left", padx=4)
        tk.Button(f3, text="Hủy (cả 2)", command=self._huy).pack(side="left", padx=4)
        tk.Button(f3, text="Mở thư mục kết quả", command=self._mo_thu_muc_ket_qua).pack(side="left", padx=4)
        # (v7.19) So nhiem vu cua JSON — dong bo voi dong Che do JSON
        # ben tren (cung nguon cot_duoc_bat): dual -> 2 nhiem vu,
        # 1 ngon ngu -> 1 nhiem vu. Chua co JSON thi ghi ro.
        f_nv = tk.Frame(noi_dung)
        f_nv.pack(fill="x", **pad)
        tk.Label(f_nv, text="Nhiệm vụ:", fg="blue").pack(side="left", padx=4)
        self.lb_nhiem_vu = tk.Label(f_nv, text="chưa có JSON", fg="blue")
        self.lb_nhiem_vu.pack(side="left", padx=4)

        # (v7.15) LUON 2 COT SONG SONG: EN trai, VI phai. Moi cot co
        # setting rieng giong tab SRT Reader (giong/toc do/cao do/
        # nghi giua cue/re-time/tu dong toc do) + tien do % + cue
        # hien tai + file ra + log rieng. Cot VI mac dinh HoaiMy,
        # cot EN mac dinh Helio (map sang Christopher tren Windows).
        khung_cot = tk.Frame(noi_dung)
        khung_cot.pack(fill="x", **pad)
        khung_cot.columnconfigure(0, weight=1)
        khung_cot.columnconfigure(1, weight=1)
        self.col["en"] = self._dung_cot(khung_cot, "en", "EN — Tiếng Anh (nước ngoài)", 0)
        self.col["vi"] = self._dung_cot(khung_cot, "vi", "VI — Tiếng Việt", 1)
        # Alias tuong thich code cu (doc shared): lay cot EN lam mac dinh.
        self.cb_giong = self.col["en"]["cb_giong"]
        self.cb_giong_b = self.col["en"]["cb_giong_b"]
        self.sl_toc_do = self.col["en"]["sl_toc_do"]
        self.lb_toc_do = self.col["en"]["lb_toc_do"]
        self.sl_cao_do = self.col["en"]["sl_cao_do"]
        self.e_nghi = self.col["en"]["e_nghi"]
        self.var_retime = self.col["en"]["var_retime"]
        self.var_tu_dong_toc_do = self.col["en"]["var_tu_dong_toc_do"]
        self.lb_trang_thai_lang = {l: self.col[l]["lb_trang_thai"] for l in ("en", "vi")}
        self.pb_lang = {l: self.col[l]["pb"] for l in ("en", "vi")}


        tk.Label(noi_dung, text="Kịch bản (chỉ đọc):").pack(fill="x", **pad)
        self.txt_script = scrolledtext.ScrolledText(noi_dung, height=8, state="disabled")
        self.txt_script.pack(fill="x", **pad)
        self.lb_thong_tin = tk.Label(noi_dung, text="Chưa có dữ liệu — dán JSON rồi ấn Áp dụng JSON.", justify="left", wraplength=980)
        self.lb_thong_tin.pack(fill="x", **pad)
        tk.Label(noi_dung, text="Log:").pack(fill="x", **pad)
        self.txt_log = scrolledtext.ScrolledText(noi_dung, height=8, state="disabled")
        self.txt_log.pack(fill="both", expand=True, **pad)
        self.thu_muc_ket_qua = self.cfg.get("ytf_thu_muc_luu") or mac_dinh_thu_muc_luu_srt()

    def _tao_khung_cuon(self, parent):
        """(v7.19) Khung cuon doc (Canvas + Scrollbar + Frame trong),
        cung mau _tao_khung_cuon cua tab Duyet video (helper goc nam
        o lop do, khong phai o QuanLy nen tab nay co ban sao rieng).
        Them so voi ban goc: lan chuot tren moi vung noi dung (tru o
        Text/Listbox/Scrollbar — cac o do tu cuon rieng) deu cuon ca
        tab, de keo xuong toi o log cuoi tab tren man hinh 1080p."""
        khung_ngoai = tk.Frame(parent)
        canvas = tk.Canvas(khung_ngoai, highlightthickness=0)
        sb = ttk.Scrollbar(khung_ngoai, orient="vertical",
                           command=canvas.yview)
        khung_trong = tk.Frame(canvas)
        cua_so = canvas.create_window((0, 0), window=khung_trong,
                                      anchor="nw")
        khung_trong.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cua_so, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _cuon(event):
            try:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
                else:
                    canvas.yview_scroll(int(-event.delta / 120), "units")
            except Exception:
                pass

        canvas.bind("<MouseWheel>", _cuon)
        canvas.bind("<Button-4>", _cuon)
        canvas.bind("<Button-5>", _cuon)

        def _gan_cuon(w):
            # Gan lan chuot cho widget con (de quy). Bo qua Text,
            # Listbox, Scrollbar: cac o do giu cuon rieng cua no.
            try:
                if isinstance(w, (tk.Text, tk.Listbox, ttk.Scrollbar,
                                  tk.Scrollbar)):
                    return
                w.bind("<MouseWheel>", _cuon)
                w.bind("<Button-4>", _cuon)
                w.bind("<Button-5>", _cuon)
            except Exception:
                pass
            try:
                for ch in w.winfo_children():
                    _gan_cuon(ch)
            except Exception:
                pass

        # Moi lan khung trong doi kich thuoc (them widget moi) thi
        # gan lai lan chuot cho cac widget con moi xuat hien.
        khung_trong.bind("<Configure>", lambda e: _gan_cuon(khung_trong),
                         add="+")
        self._canvas_cuon = canvas
        self._sb_cuon = sb
        return khung_ngoai, khung_trong

    def _cap_nhat_nhiem_vu(self):
        """(v7.19) Cap nhat label so nhiem vu ben duoi o dan JSON.
        Cung nguon cot_duoc_bat nhu dong 'Che do JSON' nen 2 cho
        khong bao gio lech nhau. Chua co JSON -> 'chưa có JSON'."""
        if not self.du_lieu:
            txt = "chưa có JSON"
        else:
            bat = list(self.cot_duoc_bat or [])
            if len(bat) >= 2:
                txt = "2 nhiệm vụ (EN + VI)"
            elif bat == ["en"]:
                txt = "1 nhiệm vụ (chỉ EN)"
            elif bat == ["vi"]:
                txt = "1 nhiệm vụ (chỉ VI)"
            else:
                txt = "chưa có JSON"
        try:
            self.lb_nhiem_vu.configure(text=txt)
        except Exception:
            pass

    # (v7.19) Cau mau co dinh de nghe thu giong.
    YTF_CAU_MAU = {"en": "Hello, this is a preview of this voice.",
                   "vi": "Xin chào, đây là giọng đọc thử."}

    def _nghe_thu_giong(self, lang, loai):
        """(v7.19) Nut 'Nghe thử' canh o chon giong: doc thu 1 cau mau
        ngan bang dung giong da chon (da anh xa Helio->Christopher nhu
        khi doc that), dung toc do + cao do dang chinh o cot do. Chay
        thread nen (UI khong do); chi 1 preview tai 1 thoi diem — bam
        preview khac thi dung ffplay dang phat."""
        c = self.col.get(lang) or {}
        cb = c.get("cb_giong") if loai == "a" else c.get("cb_giong_b")
        ten = cb.get() if cb is not None else ""
        voice = ytf_giong_id_cua_ten(ten, lang)
        try:
            toc_do = float(c["sl_toc_do"].get())
        except Exception:
            toc_do = 1.0
        toc_do = max(0.5, min(1.35, toc_do))
        try:
            cao_do = int(c["sl_cao_do"].get())
        except Exception:
            cao_do = 0
        # Chi 1 preview tai 1 thoi diem: tang token + bao thread cu dung.
        self._nghe_thu_token += 1
        token = self._nghe_thu_token
        cu = self._nghe_thu_dung
        if cu is not None:
            try:
                cu.set()
            except Exception:
                pass
        dung = threading.Event()
        self._nghe_thu_dung = dung
        t = threading.Thread(
            target=self._chay_nghe_thu,
            args=(lang, ten, voice, toc_do, cao_do, token, dung),
            daemon=True)
        t.start()

    def _chay_nghe_thu(self, lang, ten, voice, toc_do, cao_do, token,
                       dung):
        """Thread nen cua _nghe_thu_giong: goi Edge TTS 1 cau mau ra
        file tam roi phat bang _phat_mp3 (ffplay an, giong tab Xu ly
        am thanh v7.17). Moi loi chi log + dialog, khong crash tab.
        KHONG them lenh subprocess moi — tai dung _phat_mp3 san co."""
        cau = None
        # (v7.19) Thread nen KHONG goi truc tiep ham Tk (after/_
        # log_cot/messagebox tu thread phu se loi 'main thread is not
        # in main loop' khi main thread khong o trong mainloop) — chi
        # day vao hang_doi, main thread xu ly qua _xu_ly_hang_doi.
        self.hang_doi.put(("log_cot", (lang, "Đang đọc thử giọng %s (%s)..."
                                        % (ten, voice))))
        tam = None
        try:
            cau = self.YTF_CAU_MAU.get(lang, self.YTF_CAU_MAU["en"])
            import tempfile
            tam = os.path.join(tempfile.gettempdir(),
                               "_nghe-thu-faceless-%d.mp3" % token)
            ok, _bo, loi = _doc_mot_doan_co_failover(
                cau, voice, toc_do, cao_do, tam, log_cb=None,
                timeout_giay=60, dung=dung)
            if not ok:
                # Bi preview moi hon huy giua chung thi im lang.
                if dung.is_set() or token != self._nghe_thu_token:
                    return
                msg = ("Không đọc thử được giọng %s: %s"
                       % (ten, loi or "lỗi Edge TTS"))
                self.hang_doi.put(("log_cot", (lang, "LỖI nghe thử: " + msg)))
                self.hang_doi.put(("loi_nghe_thu", msg))
                return
            if dung.is_set() or token != self._nghe_thu_token:
                return  # da co preview moi hon — khong phat file cu
            ok_ph, loi_ph = _phat_mp3(tam, dung=dung)
            if not ok_ph:
                if dung.is_set() or token != self._nghe_thu_token:
                    return
                msg = ("Không phát được file nghe thử: %s"
                       % (loi_ph or "?"))
                self.hang_doi.put(("log_cot", (lang, "LỖI nghe thử: " + msg)))
                self.hang_doi.put(("loi_nghe_thu", msg))
                return
            self.hang_doi.put(("log_cot", (lang, "Đã phát thử giọng %s." % ten)))
        except Exception as e:
            msg = "Không đọc thử được giọng %s: %s" % (ten, e)
            self.hang_doi.put(("log_cot", (lang, "LỖI nghe thử: " + msg)))
            self.hang_doi.put(("loi_nghe_thu", msg))
        finally:
            try:
                if tam and os.path.isfile(tam):
                    os.remove(tam)
            except Exception:
                pass

    def _log(self, msg):
        try:
            self.txt_log.configure(state="normal")
            self.txt_log.insert("end", str(msg) + "\n")
            self.txt_log.see("end")
            self.txt_log.configure(state="disabled")
        except Exception:
            pass

    def _xu_ly_hang_doi(self):
        try:
            while True:
                loai, nd = self.hang_doi.get_nowait()
                if loai == "log":
                    self._log(nd)
                elif loai == "log_cot":
                    # (v7.19) Nghe thu giong: log rieng cot, gui tu
                    # thread nen qua hang_doi (main thread xu ly).
                    try:
                        self._log_cot(nd[0], nd[1])
                    except Exception:
                        pass
                elif loai == "loi_nghe_thu":
                    # (v7.19) Nghe thu giong: dialog loi, hien tren
                    # main thread (khong goi messagebox tu thread nen).
                    try:
                        messagebox.showerror(APP_TITLE, nd)
                    except Exception:
                        pass
                elif loai == "tien_do":
                    _lang, _pct, _cue, _tong = nd
                    _job = self.jobs.get(_lang)
                    if _job is not None:
                        ytf_cap_nhat_tien_do(_job, _cue, _tong)
                    if _lang in self.pb_lang:
                        self.pb_lang[_lang]["value"] = int(_pct or 0)
                    if _lang in self.lb_trang_thai_lang:
                        self.lb_trang_thai_lang[_lang].configure(
                            text="Đang chạy: cue %d/%d (%d%%)." % (_cue, _tong, int(_pct or 0)))
                    _c = self.col.get(_lang, {})
                    if _c.get("lb_cue") is not None:
                        _c["lb_cue"].configure(text="Cue: %d / %d (%d%%)" % (_cue, _tong, int(_pct or 0)))
                elif loai == "job_xong":
                    _lang = nd
                    _job = self.jobs.get(_lang)
                    if _job is not None:
                        # (v7.16) Con cue chua xu ly thi KHONG duoc
                        # goi la xong, du _tao_audio_1_ban tra True.
                        if (_job.get("chua_xu_ly") or []):
                            _job["da_xong"] = False
                            _job["status"] = "chua_xong"
                        else:
                            _job["da_xong"] = True
                            _job["status"] = "xong"
                    if _lang in self.lb_trang_thai_lang:
                        if _job is not None and (_job.get("chua_xu_ly") or []):
                            self.lb_trang_thai_lang[_lang].configure(
                                text="Chưa xong: %d cue chưa xử lý — ấn 'Gọi lại chỗ chưa xử lý'." % len(_job["chua_xu_ly"]))
                        else:
                            self.lb_trang_thai_lang[_lang].configure(text="Xong.")
                    _c = self.col.get(_lang, {})
                    _f = (self.jobs.get(_lang, {}).get("files") or {})
                    if _c.get("lb_file") is not None and _f.get("mp3"):
                        _c["lb_file"].configure(text="File ra: %s" % os.path.basename(_f["mp3"]))
                    if _c.get("lb_cue") is not None:
                        _c["lb_cue"].configure(text="Cue: xong %d/%d" % (_job.get("tong_cue", 0), _job.get("tong_cue", 0)))
                    self._kiem_tra_het_job()
                elif loai == "job_loi":
                    _lang, _loi = nd
                    _job = self.jobs.get(_lang)
                    if _job is not None:
                        _job["status"] = "loi"
                        _job["loi"] = str(_loi)
                        _job["da_xong"] = True
                    if _lang in self.lb_trang_thai_lang:
                        self.lb_trang_thai_lang[_lang].configure(text="Lỗi — bên kia vẫn chạy.")
                    self._log("Lỗi %s: %s (bên kia vẫn chạy, không bị ảnh hưởng)." % (_lang, _loi))
                    self._kiem_tra_het_job()
                elif loai == "chua_xu_ly":
                    # (v7.16) Thread doc vua ghi them 1 cue loi: chi
                    # ve lai danh sach cot (job da cap nhat san).
                    self._cap_nhat_list_chua(nd[0])
                elif loai == "da_xu_ly":
                    # (v7.16) 1 cue vua doc xong sau khi goi lai:
                    # xoa khoi danh sach chua xu ly, ve lai cot.
                    self._cap_nhat_list_chua(nd[0])
                elif loai == "chua_xong":
                    # (v7.16) Luong ket thuc nhung con cue chua xu ly:
                    # KHONG phai loi fatal, KHONG dung ben kia, file
                    # final chua xuat — cho anh goi lai.
                    _lang = nd
                    _job = self.jobs.get(_lang)
                    _n = len((_job or {}).get("chua_xu_ly") or [])
                    if _job is not None:
                        _job["status"] = "chua_xong"
                        _job["da_xong"] = False
                        _job["loi"] = "Chưa xong: %d cue chưa xử lý." % _n
                    if _lang in self.lb_trang_thai_lang:
                        self.lb_trang_thai_lang[_lang].configure(
                            text="Chưa xong: %d cue chưa xử lý — ấn 'Gọi lại chỗ chưa xử lý'." % _n)
                    self._cap_nhat_list_chua(_lang)
                    self._log("Chưa xong %s: %d cue chưa xử lý (file final chưa xuất — chỉ xuất khi danh sách rỗng)." % (_lang.upper(), _n))
                    self._kiem_tra_het_job()
                elif loai == "xong":
                    self.dang_chay = False
                    self._log("Xong.")
        except queue.Empty:
            pass
        self.after(200, self._xu_ly_hang_doi)

    def _dung_cot(self, parent, lang, tieu_de, cot):
        """1 cot doc lap (EN hoac VI), giong tab SRT Reader: setting
        rieng + tien do % + cue hien tai + file ra + log rieng.
        Mac dinh: EN = Helio (nam, My), VI = HoaiMy (nu) — giu
        nguyen nhu v7.13/v7.14, khong doi sang giong khac."""
        fr = tk.LabelFrame(parent, text=" " + tieu_de + " ")
        fr.grid(row=0, column=cot, sticky="nsew", padx=4, pady=2)
        d = {"lang": lang, "frame": fr}
        d["lb_trang_thai"] = tk.Label(fr, text="Chờ — chưa có JSON.", anchor="w")
        d["lb_trang_thai"].pack(fill="x", padx=4, pady=2)
        tk.Label(fr, text="Giọng đọc:").pack(anchor="w", padx=4)
        f_giong = tk.Frame(fr)
        f_giong.pack(fill="x", padx=4, pady=2)
        d["cb_giong"] = ttk.Combobox(f_giong, state="readonly", width=26)
        d["cb_giong"]["values"] = ytf_giong_theo_ngon_ngu(lang)
        mac_dinh = self.cfg.get("ytf_giong_en" if lang == "en" else "ytf_giong_vi",
                                YTF_GIONG_MAC_DINH[lang])
        d["cb_giong"].set(mac_dinh if mac_dinh in d["cb_giong"]["values"] else d["cb_giong"]["values"][0])
        d["cb_giong"].pack(side="left")
        d["btn_nghe_thu"] = tk.Button(f_giong, text="Nghe thử",
                                      command=lambda l=lang: self._nghe_thu_giong(l, "a"))
        d["btn_nghe_thu"].pack(side="left", padx=4)
        d["cb_giong"].bind("<<ComboboxSelected>>", lambda e: self._luu_cau_hinh())
        # (v7.15, doi thoai Q&A) Giong 2 (nguoi tra loi / phu).
        # Mac dinh: EN = Aria (nu, My), VI = NamMinh (nam).
        tk.Label(fr, text="Giọng 2 (người trả lời / phụ):").pack(anchor="w", padx=4)
        f_giong_b = tk.Frame(fr)
        f_giong_b.pack(fill="x", padx=4, pady=2)
        d["cb_giong_b"] = ttk.Combobox(f_giong_b, state="readonly", width=26)
        d["cb_giong_b"]["values"] = ytf_giong_theo_ngon_ngu(lang)
        mac_dinh_b = self.cfg.get("ytf_giong_b_en" if lang == "en" else "ytf_giong_b_vi",
                                  "Aria (nữ, Mỹ)" if lang == "en" else "NamMinh (nam)")
        d["cb_giong_b"].set(mac_dinh_b if mac_dinh_b in d["cb_giong_b"]["values"] else d["cb_giong_b"]["values"][0])
        d["cb_giong_b"].pack(side="left")
        d["btn_nghe_thu_b"] = tk.Button(f_giong_b, text="Nghe thử",
                                        command=lambda l=lang: self._nghe_thu_giong(l, "b"))
        d["btn_nghe_thu_b"].pack(side="left", padx=4)
        d["cb_giong_b"].bind("<<ComboboxSelected>>", lambda e: self._luu_cau_hinh())
        nguon = ("Nguồn: Muse Helio → Edge Christopher trên Windows (log rõ khi áp dụng JSON)."
                 if lang == "en" else "Nguồn: Edge TTS — vi-VN-HoaiMyNeural (nữ).")
        d["lb_nguon"] = tk.Label(fr, text=nguon, wraplength=420, justify="left", fg="gray")
        d["lb_nguon"].pack(fill="x", padx=4)
        tk.Label(fr, text="Tốc độ (0.5–1.35x, mặc định 1.0x):").pack(anchor="w", padx=4)
        d["sl_toc_do"] = tk.Scale(fr, from_=0.5, to=1.35, resolution=0.01, orient="horizontal", length=220)
        d["sl_toc_do"].set(max(0.5, min(1.35, float(self.cfg.get(
            "ytf_toc_do_en" if lang == "en" else "ytf_toc_do_vi",
            self.cfg.get("ytf_toc_do", 1.0))))))
        d["sl_toc_do"].pack(anchor="w", padx=4)
        d["lb_toc_do"] = tk.Label(fr, text="%.2fx" % float(d["sl_toc_do"].get()))
        d["lb_toc_do"].pack(anchor="w", padx=4)
        d["sl_toc_do"].configure(command=lambda v, _d=d: _d["lb_toc_do"].configure(text="%.2fx" % float(v)))
        tk.Label(fr, text="Cao độ (-10..+10):").pack(anchor="w", padx=4)
        d["sl_cao_do"] = tk.Scale(fr, from_=-10, to=10, orient="horizontal", length=180)
        d["sl_cao_do"].set(int(self.cfg.get(
            "ytf_cao_do_en" if lang == "en" else "ytf_cao_do_vi",
            self.cfg.get("ytf_cao_do", 0))))
        d["sl_cao_do"].pack(anchor="w", padx=4)
        f_nghi = tk.Frame(fr)
        f_nghi.pack(fill="x", padx=4, pady=2)
        tk.Label(f_nghi, text="Nghỉ giữa cue (ms):").pack(side="left")
        d["e_nghi"] = tk.Entry(f_nghi, width=6)
        d["e_nghi"].insert(0, str(int(self.cfg.get(
            "ytf_nghi_en_ms" if lang == "en" else "ytf_nghi_vi_ms",
            self.cfg.get("ytf_nghi_giua_cue_ms", 350)))))
        d["e_nghi"].pack(side="left", padx=4)
        d["var_retime"] = tk.BooleanVar(value=bool(self.cfg.get(
            "ytf_retime_en" if lang == "en" else "ytf_retime_vi",
            self.cfg.get("ytf_tu_dong_retime", True))))
        tk.Checkbutton(fr, text="Tự động căn lại SRT theo audio thật",
                       variable=d["var_retime"]).pack(anchor="w", padx=4)
        d["var_tu_dong_toc_do"] = tk.BooleanVar(value=bool(self.cfg.get(
            "ytf_tu_dong_toc_do_en" if lang == "en" else "ytf_tu_dong_toc_do_vi",
            self.cfg.get("ytf_tu_dong_toc_do", True))))
        tk.Checkbutton(fr, text="Tự động chỉnh tốc độ từng câu (tối đa 1.35x)",
                       variable=d["var_tu_dong_toc_do"]).pack(anchor="w", padx=4)
        # (v7.16) Giong may local CHI khi anh BAT tay cong tac nay
        # (mac dinh TAT). TAT: cau loi chi goi lai bang Edge, khong
        # tu doi giong. BAT: cau loi sau khi goi lai Edge moi duoc
        # doc bang giong may SAPI va se ghi ro trong log + danh sach.
        d["var_local"] = tk.BooleanVar(value=bool(self.cfg.get(
            "ytf_cho_dung_giong_may_en" if lang == "en" else "ytf_cho_dung_giong_may_vi",
            YTF_CHO_DUNG_GIONG_MAY_MAC_DINH)))
        tk.Checkbutton(fr, text="Cho dùng giọng máy local (SAPI) khi Edge lỗi",
                       variable=d["var_local"]).pack(anchor="w", padx=4)
        tk.Label(fr, text="Mặc định TẮT: câu lỗi chỉ gọi lại bằng Edge, không tự đổi giọng. BẬT: câu lỗi sau khi gọi lại Edge mới được đọc bằng giọng máy local và sẽ ghi rõ.",
                 wraplength=420, justify="left", fg="gray").pack(fill="x", padx=4)
        # (v7.16) Danh sach "Giong chua xu ly" rieng cot nay.
        tk.Label(fr, text="Giọng chưa xử lý:").pack(anchor="w", padx=4)
        d["list_chua"] = tk.Listbox(fr, height=4)
        d["list_chua"].pack(fill="x", padx=4, pady=2)
        d["lb_chua"] = tk.Label(fr, text="Giọng chưa xử lý: 0 cue.", anchor="w")
        d["lb_chua"].pack(fill="x", padx=4)
        f_chua = tk.Frame(fr)
        f_chua.pack(fill="x", padx=4, pady=2)
        tk.Button(f_chua, text="Gọi lại chỗ chưa xử lý",
                  command=lambda l=lang: self._goi_lai_chua_xu_ly(l)).pack(side="left", padx=2)
        tk.Button(f_chua, text="Gọi lại 1 cue đã chọn",
                  command=lambda l=lang: self._goi_lai_1_cue(l)).pack(side="left", padx=2)
        d["chua_hien"] = []  # [("chua"|"local", index)] theo thu tu listbox
        d["pb"] = ttk.Progressbar(fr, length=220, maximum=100)
        d["pb"].pack(fill="x", padx=4, pady=2)
        d["lb_cue"] = tk.Label(fr, text="Cue: — / —", anchor="w")
        d["lb_cue"].pack(fill="x", padx=4)
        d["lb_file"] = tk.Label(fr, text="File ra: chưa có.", anchor="w", wraplength=420, justify="left")
        d["lb_file"].pack(fill="x", padx=4)
        f_btn = tk.Frame(fr)
        f_btn.pack(fill="x", padx=4, pady=2)
        tk.Button(f_btn, text="Tạo audio " + lang.upper(),
                  command=lambda l=lang: self._tao_audio_lang(l)).pack(side="left", padx=2)
        tk.Button(f_btn, text="Dừng " + lang.upper(),
                  command=lambda l=lang: self._dung_lang(l)).pack(side="left", padx=2)
        tk.Button(f_btn, text="Hủy " + lang.upper(),
                  command=lambda l=lang: self._huy_lang(l)).pack(side="left", padx=2)
        tk.Button(f_btn, text="Mở thư mục",
                  command=lambda l=lang: self._mo_thu_muc_lang(l)).pack(side="left", padx=2)
        d["txt_log"] = scrolledtext.ScrolledText(fr, height=5, state="disabled")
        d["txt_log"].pack(fill="both", expand=True, padx=4, pady=2)
        d["enabled"] = True
        return d

    def _log_cot(self, lang, msg):
        """Log rieng cot + log chung (tien to [EN]/[VI])."""
        try:
            c = self.col.get(lang, {})
            t = c.get("txt_log")
            if t is not None:
                t.configure(state="normal")
                t.insert("end", str(msg) + "\n")
                t.see("end")
                t.configure(state="disabled")
        except Exception:
            pass
        self._log("[%s] %s" % (lang.upper(), msg))

    def _cap_nhat_list_chua(self, lang):
        """(v7.16) Ve lai danh sach "Giong chua xu ly" cua 1 cot tu
        job cua cot do (cue loi + cue da doc bang giong may local,
        ghi ro). Dong thoi cap nhat nhan trang thai cot."""
        c = self.col.get(lang, {})
        lb = c.get("list_chua")
        lbl = c.get("lb_chua")
        _job = self.jobs.get(lang, {}) or {}
        ds = _job.get("chua_xu_ly") or []
        _local = _job.get("da_dung_local") or []
        c["chua_hien"] = ([("chua", int(it["index"])) for it in ds]
                          + [("local", int(it["index"])) for it in _local])
        if lb is not None:
            try:
                lb.delete(0, "end")
                for it in ds:
                    lb.insert("end", "Cue %d [%s %s] (%s) — lỗi: %s (đã thử %d lần)" % (
                        it["index"], it.get("speaker", "A"), (it.get("character") or ""),
                        it.get("gender") or "?", (it.get("loi") or "")[:60],
                        int(it.get("lan_thu") or 1)))
                for it in _local:
                    lb.insert("end", "Cue %d [%s %s] — ĐÃ ĐỌC BẰNG GIỌNG MÁY LOCAL" % (
                        it["index"], it.get("speaker", "A"), (it.get("character") or "")))
            except Exception:
                pass
        if lbl is not None:
            lbl.configure(text="Giọng chưa xử lý: %d cue.%s" % (
                len(ds), (" %d cue đã đọc bằng giọng máy local." % len(_local)) if _local else ""))
        if ds and lang in self.lb_trang_thai_lang:
            self.lb_trang_thai_lang[lang].configure(
                text="Chưa xong: %d cue chưa xử lý — ấn 'Gọi lại chỗ chưa xử lý'." % len(ds))

    def _goi_lai_chua_xu_ly(self, lang):
        """(v7.16) Nut 'Goi lai cho chua xu ly': goi lai CHI cac cue
        dang nam trong danh sach chua xu ly cua cot nay, dung dung
        giong/gioi tinh goc cua tung cue."""
        ds = (self.jobs.get(lang, {}) or {}).get("chua_xu_ly") or []
        if not ds:
            self._log_cot(lang, "Không có cue nào chưa xử lý.")
            return
        self._chay_retry_lang(lang, {int(it["index"]) for it in ds})

    def _goi_lai_1_cue(self, lang):
        """(v7.16) Nut 'Goi lai 1 cue da chon': goi lai dung 1 cue
        dang chon trong danh sach 'Giong chua xu ly'."""
        c = self.col.get(lang, {})
        lb = c.get("list_chua")
        ds = (self.jobs.get(lang, {}) or {}).get("chua_xu_ly") or []
        if not ds or lb is None:
            self._log_cot(lang, "Không có cue nào chưa xử lý để gọi lại.")
            return
        sel = lb.curselection()
        if not sel:
            self._log_cot(lang, "Chọn 1 cue trong danh sách 'Giọng chưa xử lý' rồi ấn lại.")
            return
        _hien = c.get("chua_hien") or []
        if int(sel[0]) >= len(_hien):
            return
        _kind, idx = _hien[int(sel[0])]
        if _kind != "chua":
            self._log_cot(lang, "Cue %d đã đọc xong bằng giọng máy local — không cần gọi lại." % idx)
            return
        self._chay_retry_lang(lang, {idx})

    def _chay_retry_lang(self, lang, chi_cac_cue):
        """(v7.16) Chay goi lai cho 1 cot: chi doc cac cue trong
        chi_cac_cue, cue da xong truoc do thi dung lai file tam.
        Khong cham cot kia, khong xoa danh sach chua xu ly."""
        if lang not in self.du_lieu:
            return
        if ytf_job_con_chay(self.jobs.get(lang, {})):
            self._log_cot(lang, "%s đang chạy rồi — chờ xong rồi gọi lại." % lang.upper())
            return
        self._luu_cau_hinh()
        self._stop_events[lang].clear()
        job = self.jobs[lang]
        job["status"] = "dang_chay"
        job["da_huy"] = False
        job["da_xong"] = False
        self._retry_chi = getattr(self, "_retry_chi", {})
        self._retry_chi[lang] = set(chi_cac_cue)
        self._song_song_sem = threading.Semaphore(2)
        slug = ytf_slug_hoa(next(iter(self.du_lieu.values())).get("title") or "video-faceless")
        threading.Thread(target=self._tao_audio_1_luong,
                         args=(lang, self.du_lieu[lang], self.thu_muc_ket_qua, slug),
                         daemon=True).start()
        self._log_cot(lang, "Gọi lại %d cue chưa xử lý: %s" % (len(chi_cac_cue), sorted(chi_cac_cue)))

    def _dat_trang_thai_cot(self, lang, bat, ly_do=""):
        """BAT/TAT 1 cot theo mode JSON. Tat = mo (greyed) chu khong
        xoa cot: van thay cot, khong chay duoc."""
        c = self.col.get(lang)
        if not c:
            return
        c["enabled"] = bool(bat)
        def _dat(w, state):
            try:
                w.configure(state=state)
            except Exception:
                pass
        for k in ("cb_giong", "cb_giong_b", "sl_toc_do", "sl_cao_do", "e_nghi"):
            _dat(c[k], "normal" if bat else "disabled")
        if bat:
            c["lb_trang_thai"].configure(text="Bật — sẵn sàng chạy." + (" " + ly_do if ly_do else ""))
        else:
            c["lb_trang_thai"].configure(text="Đã tắt — JSON không làm bản này. " + ly_do)
            c["pb"]["value"] = 0
            c["lb_cue"].configure(text="Cue: — / —")

    def _cap_nhat_cot_bat_tat(self):
        """Ap mode JSON vao 2 cot: cot trong mode thi BAT, cot ngoai
        mode thi TAT (mo). Khong co JSON thi ca 2 cot deu BAT."""
        if not self.du_lieu:
            for l in ("en", "vi"):
                self._dat_trang_thai_cot(l, True)
            self.cot_duoc_bat = ["en", "vi"]
            return
        self.cot_duoc_bat = ytf_cot_duoc_bat(self.du_lieu, self.che_do_json)
        for l in ("en", "vi"):
            self._dat_trang_thai_cot(l, l in self.cot_duoc_bat,
                                     "" if l in self.cot_duoc_bat else
                                     "(mode JSON=%s)" % self.che_do_json.get("mode"))

    def _mo_thu_muc_lang(self, lang):
        """Mo thu muc ket qua cua rieng 1 cot (neu co file thi mo
        thu muc chua file do, khong thi mo thu muc ket qua chung)."""
        try:
            duong = (self.jobs.get(lang, {}).get("files") or {}).get("mp3")
            thu_muc = os.path.dirname(duong) if duong else self.thu_muc_ket_qua
            os.makedirs(thu_muc, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(thu_muc)
            else:
                self._log("Thư mục %s: %s" % (lang.upper(), thu_muc))
        except Exception as e:
            self._log("Không mở được thư mục %s: %s" % (lang.upper(), e))

    def _cap_nhat_giong(self):
        """Cap nhat danh sach giong RIENG tung cot (EN chi giong EN,
        VI chi giong VI). Mac dinh: EN = Helio, VI = HoaiMy."""
        for lang in ("en", "vi"):
            c = self.col.get(lang)
            if not c:
                continue
            ds = ytf_giong_theo_ngon_ngu(lang)
            c["cb_giong"]["values"] = ds
            mac_dinh = self.cfg.get("ytf_giong_en" if lang == "en" else "ytf_giong_vi",
                                    YTF_GIONG_MAC_DINH[lang])
            if c["cb_giong"].get() not in ds:
                c["cb_giong"].set(mac_dinh if mac_dinh in ds else ds[0])
            mac_dinh_b = self.cfg.get("ytf_giong_b_en" if lang == "en" else "ytf_giong_b_vi",
                                      "Aria (nữ, Mỹ)" if lang == "en" else "NamMinh (nam)")
            c["cb_giong_b"]["values"] = ds
            if c["cb_giong_b"].get() not in ds:
                c["cb_giong_b"].set(mac_dinh_b if mac_dinh_b in ds else ds[0])

    def _doi_ngon_ngu(self):
        self._cap_nhat_giong()
        self._hien_du_lieu()

    def _doi_song_song(self):
        """Cong tac song song doi -> luu config + log ro che do."""
        self._luu_cau_hinh()
        if self.var_song_song.get():
            self._log("Chế độ song song EN+VI: BẬT — EN và VI chạy 2 luồng độc lập, "
                      "dừng/hủy/lỗi 1 bên không ảnh hưởng bên kia. Số luồng tối đa: %s."
                      % self.cb_dong_bo.get())
        else:
            self._log("Chế độ song song EN+VI: TẮT — làm tuần tự EN rồi VI (mặc định, an toàn nhất).")

    def _kiem_tra_het_job(self):
        """Chi tat co dang_chay khi MOI ngon ngu co trong du_lieu da
        ket thuc (xong / loi / huy) — 1 ben xong khong tat ben kia."""
        if not self.du_lieu:
            self.dang_chay = False
            return
        # (v7.16) Ben "chua_xong" (con cue chua xu ly) khong con
        # dang chay nua nhung cung chua xong: chi doi ben dang_chay.
        con = [l for l in self.du_lieu
               if self.jobs.get(l, {}).get("status") == "dang_chay"]
        if not con:
            self.dang_chay = False
            _chua = [l for l in self.du_lieu if (self.jobs.get(l, {}).get("chua_xu_ly") or [])]
            if _chua:
                self._log("Cả 2 luồng đã kết thúc — còn %s chưa xong (có cue chưa xử lý, ấn 'Gọi lại chỗ chưa xử lý')."
                          % ", ".join(l.upper() for l in _chua))
            else:
                self._log("Cả 2 luồng đã kết thúc (mỗi bên độc lập).")

    def _dung_lang(self, lang):
        """Dung 1 ngon ngu: chi set stop cua ben do."""
        self._stop_events[lang].set()
        ytf_dung_job(self.jobs[lang], "da_huy")
        if lang in self.lb_trang_thai_lang:
            self.lb_trang_thai_lang[lang].configure(text="Đã dừng — bên kia vẫn chạy.")
        self._log("Đã yêu cầu dừng %s sau cue đang đọc — %s vẫn chạy bình thường."
                  % (lang.upper(), "VI" if lang == "en" else "EN"))

    def _huy_lang(self, lang):
        self._dung_lang(lang)
        self._log("Đã hủy %s (chỉ bên %s)." % (lang.upper(), lang.upper()))

    def _luu_cau_hinh(self):
        """Luu setting RIENG tung cot (EN/VI doc lap) + cong tac song song."""
        cfg = {"ytf_ngon_ngu": self.cb_ngon_ngu.get(),
               "ytf_thu_muc_luu": self.thu_muc_ket_qua,
               "ytf_song_song": bool(self.var_song_song.get()),
               "ytf_dong_bo_toi_da": int(self.cb_dong_bo.get() or 2)}
        for lang in ("en", "vi"):
            c = self.col.get(lang)
            if not c:
                continue
            cfg["ytf_giong_" + lang] = c["cb_giong"].get()
            cfg["ytf_giong_b_" + lang] = c["cb_giong_b"].get()
            cfg["ytf_toc_do_" + lang] = float(c["sl_toc_do"].get())
            cfg["ytf_cao_do_" + lang] = int(c["sl_cao_do"].get())
            try:
                cfg["ytf_nghi_" + lang + "_ms"] = int(c["e_nghi"].get() or 350)
            except Exception:
                cfg["ytf_nghi_" + lang + "_ms"] = 350
            cfg["ytf_retime_" + lang] = bool(c["var_retime"].get())
            cfg["ytf_tu_dong_toc_do_" + lang] = bool(c["var_tu_dong_toc_do"].get())
            cfg["ytf_cho_dung_giong_may_" + lang] = bool(
                c["var_local"].get()) if c.get("var_local") is not None else False
        # Giu key cu (cot EN) de ban cu doc duoc.
        cfg["ytf_toc_do"] = cfg.get("ytf_toc_do_en", 1.0)
        cfg["ytf_cao_do"] = cfg.get("ytf_cao_do_en", 0)
        cfg["ytf_tu_dong_retime"] = cfg.get("ytf_retime_en", True)
        cfg["ytf_tu_dong_toc_do"] = cfg.get("ytf_tu_dong_toc_do_en", True)
        cfg["ytf_nghi_giua_cue_ms"] = cfg.get("ytf_nghi_en_ms", 350)
        luu_config(cfg)

    def _ap_dung_json(self, noi_dung=None):
        """(v7.15) Dan 1 JSON -> TU NHAN mode (dual/en_only/vi_only)
        tu truong mode/languages/choice hoac suy ra tu khoa en/vi,
        TU BAT/TAT cot tuong ung, TU DIEN setting RIENG tung cot
        (giong 1 + giong 2 doi thoai, toc do, cao do). Khong tick tay."""
        txt = noi_dung if noi_dung is not None else self.txt_json.get("1.0", "end")
        try:
            raw = json.loads(txt) if isinstance(txt, str) else txt
        except Exception:
            raw = {}
        meta = ytf_chuan_hoa_mode(raw if isinstance(raw, dict) else {})
        phien_ban, loi = ytf_parse_json(txt)
        if not phien_ban:
            self._log("Lỗi JSON: " + loi)
            messagebox.showerror("JSON lỗi", loi)
            return False
        # SRT tho / bare cues: khong co mode -> mac dinh EN.
        if not isinstance(raw, dict) or ("en" not in raw and "vi" not in raw):
            meta = {"mode": "en_only" if "en" in phien_ban else "vi_only",
                    "languages": list(phien_ban.keys()),
                    "nguon": "suy_ra_tu_du_lieu_co_that", "canh_bao": []}
        self.che_do_json = meta
        self.du_lieu = phien_ban
        # (v7.16) JSON moi -> xoa danh sach "Giong chua xu ly" cu.
        for _l in ("en", "vi"):
            self.jobs[_l]["chua_xu_ly"] = []
            self.jobs[_l]["so_cue_thanh_cong"] = 0
            self.jobs[_l]["da_dung_local"] = []
            self._cap_nhat_list_chua(_l)
        lang_dau = "en" if "en" in phien_ban else "vi"
        self.cb_ngon_ngu.set(lang_dau)
        self._cap_nhat_giong()
        # Dien setting RIENG tung cot tu voice_settings cua ban do.
        for lang, ban in phien_ban.items():
            c = self.col.get(lang)
            if not c:
                continue
            sp = ban.get("speakers") or {}
            vs_a = sp.get("A") or ban.get("voice_settings") or {}
            vs_b = sp.get("B") or {}
            for _vs, _key in ((vs_a, "cb_giong"), (vs_b, "cb_giong_b")):
                if _vs.get("voice_id"):
                    ten, _edge, la_muse = ytf_anh_xa_giong_muse(str(_vs["voice_id"]))
                    if ten and ten in c[_key]["values"]:
                        c[_key].set(ten)
                    if la_muse:
                        self._log_cot(lang, _vs.get("ghi_chu_anh_xa", ""))
                else:
                    # (v7.16) JSON chi ghi gioi tinh, khong ghi voice_id:
                    # chon giong mac dinh theo gioi tinh do.
                    _info_sp = ytf_speaker_info(ban, "A" if _key == "cb_giong" else "B")
                    if _info_sp.get("gender"):
                        _ten_gd = ytf_ten_giong_cua_id(
                            ytf_giong_mac_dinh_theo_gioi_tinh(lang, _info_sp.get("gender")), lang)
                        if _ten_gd and _ten_gd in c[_key]["values"]:
                            c[_key].set(_ten_gd)
            if vs_a.get("speed"):
                c["sl_toc_do"].set(max(0.5, min(1.35, float(vs_a["speed"]))))
                c["lb_toc_do"].configure(text="%.2fx" % float(c["sl_toc_do"].get()))
            if vs_a.get("pitch") is not None:
                c["sl_cao_do"].set(max(-10, min(10, int(vs_a["pitch"]))))
        self._cap_nhat_cot_bat_tat()
        self._luu_cau_hinh()
        self._hien_du_lieu()
        self.lb_che_do.configure(
            text="Chế độ JSON: %s — làm %s (từ %s). Cột ngoài chế độ đã tự tắt."
            % (meta["mode"], "+".join(x.upper() for x in self.cot_duoc_bat) or "—",
               {"truong_mode": "trường mode", "truong_languages": "trường languages",
                "truong_choice": "trường choice",
                "suy_ra_tu_khoa_en_vi": "suy ra từ khóa en/vi có trong JSON",
                "suy_ra_tu_language": "suy ra từ trường language",
                "suy_ra_tu_du_lieu_co_that": "dữ liệu có thật trong JSON"}.get(meta["nguon"], meta["nguon"])))
        self._cap_nhat_nhiem_vu()  # (v7.19) dong bo so nhiem vu
        self._log("JSON: mode=%s (từ %s) — cột bật: %s."
                  % (meta["mode"], meta["nguon"], ", ".join(self.cot_duoc_bat) or "—"))
        for _cb in meta.get("canh_bao") or []:
            self._log("CẢNH BÁO JSON: " + _cb)
        self._log("Đã áp dụng JSON: " + ", ".join(
            "%s (%d cue)" % (k, len(v["srt_cues"])) for k, v in phien_ban.items()))
        if len(phien_ban) == 2:
            self._log("Song ngữ độc lập: EN và VI là 2 kịch bản riêng (chỉ chung key/chủ đề), không ép dịch từng câu, không ép timing giống nhau — xử lý và xuất file riêng từng bản.")
        if any("speaker" in cue and cue.get("speaker") == "B" for v in phien_ban.values() for cue in v["srt_cues"]):
            self._log("Đối thoại Q&A: có cue speaker B — cue A dùng Giọng 1, cue B dùng Giọng 2 (mỗi cột).")
        # (v7.16) Log ro phien 1 hay 2 giong + gioi tinh tung speaker
        # + canh bao neu gioi tinh khong khop giong da chon.
        for _lang, _ban in phien_ban.items():
            _vm = _ban.get("voice_mode") or "single"
            self._log_cot(_lang, "Phiên làm việc: %s (nguồn: %s)." % (
                "2 giọng (đối thoại)" if _vm == "dialogue" else "1 giọng",
                _ban.get("voice_mode_nguon") or "?"))
            for _cb in _ban.get("canh_bao_gioi_tinh") or []:
                self._log_cot(_lang, "CẢNH BÁO GIỚI TÍNH: " + _cb)
            for _sp in ("A", "B"):
                _info = ytf_speaker_info(_ban, _sp)
                if _info.get("character") or _info.get("gender"):
                    self._log_cot(_lang, "Speaker %s: %s (%s) — giọng %s." % (
                        _sp, _info.get("character") or "?",
                        "nữ" if _info.get("gender") == "female" else ("nam" if _info.get("gender") == "male" else "?"),
                        _info.get("voice_id") or "?"))
        return True

    def _dan_clipboard(self):
        try:
            txt = self.clipboard_get()
        except Exception as e:
            self._log("Không đọc được clipboard: %s" % e)
            return
        self.txt_json.delete("1.0", "end")
        self.txt_json.insert("1.0", txt)
        self._ap_dung_json(txt)

    def _mo_file_srt(self):
        duong = filedialog.askopenfilename(filetypes=[("SRT", "*.srt"), ("Tất cả", "*.*")])
        if not duong:
            return
        try:
            with open(duong, "r", encoding="utf-8-sig", errors="replace") as f:
                self.txt_json.delete("1.0", "end")
                self.txt_json.insert("1.0", f.read())
            self._ap_dung_json()
        except Exception as e:
            self._log("Không mở được file SRT: %s" % e)

    def _hien_du_lieu(self):
        lang = self.cb_ngon_ngu.get() or "en"
        ban = self.du_lieu.get(lang) or (next(iter(self.du_lieu.values())) if self.du_lieu else None)
        self.txt_script.configure(state="normal")
        self.txt_script.delete("1.0", "end")
        if not ban:
            self.txt_script.configure(state="disabled")
            self.lb_thong_tin.configure(text="Chưa có dữ liệu — dán JSON rồi ấn Áp dụng JSON.")
            return
        self.txt_script.insert("1.0", ban.get("script_text", ""))
        self.txt_script.configure(state="disabled")
        tu = len(ban.get("script_text", "").split())
        uoc = ytf_uoc_tinh_thoi_luong_giay(ban.get("script_text", ""), ban["language"])
        chuong = ban.get("chapters") or []
        self.lb_thong_tin.configure(text=(
            "Ngôn ngữ: %s | Từ: %d | Thời lượng ước tính: %.1f phút (ước tính, EN ~150 từ/phút, VI ~170 tiếng/phút) | Cue: %d | Chương: %s | Tiêu đề: %s"
            % (ban["language"], tu, uoc / 60.0, len(ban["srt_cues"]),
               ", ".join(str(c) for c in chuong) if chuong else "(không có)",
               ban.get("title") or "(không có)")))

    def _huy(self):
        """Huy CA 2 ben (nut 'Huy (cả 2)'): set stop rieng tung ben + co chung."""
        self._yeu_cau_huy.set()
        for _lang in ("en", "vi"):
            self._stop_events[_lang].set()
            ytf_dung_job(self.jobs[_lang], "da_huy")
        self._log("Đã yêu cầu hủy cả 2 bên (EN + VI) sau cue đang đọc.")

    def _mo_thu_muc_ket_qua(self):
        try:
            os.makedirs(self.thu_muc_ket_qua, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(self.thu_muc_ket_qua)
            else:
                self._log("Thư mục kết quả: %s" % self.thu_muc_ket_qua)
        except Exception as e:
            self._log("Không mở được thư mục: %s" % e)

    def _tao_audio(self):
        """Nut chung 'Tao audio (EN+VI)': tuy cong tac song song.
        TAT: 1 thread tuan tu EN roi VI (hanh vi v7.13).
        BAT: moi ngon ngu 1 thread doc lap, cung bat (gioi han boi
        semaphore = so luong toi da)."""
        if not self.du_lieu:
            messagebox.showwarning("Chưa có dữ liệu", "Dán JSON rồi ấn Áp dụng JSON trước.")
            return
        if self.dang_chay:
            self._log("Đang chạy — chờ xong hoặc hủy từng bên rồi chạy lại.")
            return
        self._luu_cau_hinh()
        thu_muc = filedialog.askdirectory(initialdir=self.thu_muc_ket_qua) or self.thu_muc_ket_qua
        self.thu_muc_ket_qua = thu_muc
        self._bat_dau_chay(dict(self.du_lieu), thu_muc)

    def _bat_dau_chay(self, du_lieu, thu_muc):
        """Khoi dong chay theo ke hoach ytf_ke_hoach_chay()."""
        # (v7.15) Mode JSON thang cong tac song song: en_only thi chi
        # chay EN du song song co BAT; cot VI da tat thi khong chay.
        langs = [l for l in self.cot_duoc_bat if l in du_lieu] or [l for l in ("en", "vi") if l in du_lieu]
        ke_hoach = ytf_ke_hoach_chay(langs, bool(self.var_song_song.get()),
                                     int(self.cb_dong_bo.get() or 2))
        self.dang_chay = True
        self._yeu_cau_huy.clear()
        for lang in langs:
            self._stop_events[lang].clear()
            self.jobs[lang] = ytf_tao_job(lang)
            self.jobs[lang]["tong_cue"] = len(du_lieu[lang]["srt_cues"])
            if lang in self.pb_lang:
                self.pb_lang[lang]["value"] = 0
            if lang in self.lb_trang_thai_lang:
                self.lb_trang_thai_lang[lang].configure(text="Chờ chạy...")
        self._song_song_sem = threading.Semaphore(
            int(self.cb_dong_bo.get() or 2) if self.var_song_song.get() else 1)
        self._log("Chế độ: %s — kế hoạch %s." % (ke_hoach["che_do"], ke_hoach["luong"]))
        if ke_hoach["che_do"] == "song_song" and len(ke_hoach["luong"]) == 1 and len(langs) == 2:
            self._log("Song song BẬT: EN và VI chạy cùng lúc, độc lập — "
                      "lỗi/dừng/hủy 1 bên không ảnh hưởng bên kia. VI lệch 2 giây "
                      "để giảm nguy cơ Edge TTS bị giới hạn tốc độ (chưa kiểm chứng "
                      "giới hạn thật của Edge).")
        threading.Thread(target=self._chay_theo_ke_hoach,
                         args=(du_lieu, thu_muc, ke_hoach), daemon=True).start()

    def _chay_theo_ke_hoach(self, du_lieu, thu_muc, ke_hoach):
        """Chay cac dot trong ke hoach: moi dot = cac ngon ngu bat dong
        thoi; cac dot chay tuan tu. Moi ngon ngu 1 thread rieng."""
        slug = ytf_slug_hoa(next(iter(du_lieu.values())).get("title") or "video-faceless")
        for dot in ke_hoach["luong"]:
            threads = []
            for lang in dot:
                t = threading.Thread(
                    target=self._tao_audio_1_luong,
                    args=(lang, du_lieu[lang], thu_muc, slug), daemon=True)
                t.start()
                threads.append(t)
                self._threads[lang] = t
            for t in threads:
                t.join()
            if self._yeu_cau_huy.is_set():
                break
        # Neu dot cuoi la tuan tu thi _tao_audio_1_luong da gui job_xong
        # tung ben; dam bao co thong bao ket thuc chung.
        self.hang_doi.put(("xong", None))

    def _tao_audio_lang(self, lang):
        """Nut rieng 'Tao audio EN' / 'Tao audio VI': chi chay 1 ben,
        khong cham ben kia (ke ca khi ben kia dang chay)."""
        if lang not in self.du_lieu:
            messagebox.showwarning("Chưa có dữ liệu %s" % lang.upper(),
                                   "JSON chưa có bản %s — dán JSON dual rồi ấn Áp dụng JSON." % lang.upper())
            return
        if self.cot_duoc_bat and lang not in self.cot_duoc_bat:
            messagebox.showwarning("Cột %s đã tắt" % lang.upper(),
                                   "JSON mode=%s nên cột %s đã tự tắt — không chạy bản này." % (self.che_do_json.get("mode"), lang.upper()))
            return
        if ytf_job_con_chay(self.jobs.get(lang, {})):
            self._log("%s đang chạy rồi." % lang.upper())
            return
        self._luu_cau_hinh()
        thu_muc = self.thu_muc_ket_qua
        self._stop_events[lang].clear()
        self.jobs[lang] = ytf_tao_job(lang)
        self.jobs[lang]["tong_cue"] = len(self.du_lieu[lang]["srt_cues"])
        self.dang_chay = True
        # (v7.14) Nut rieng 1 ben cung can semaphore (mac dinh 2) de
        # _tao_audio_1_luong khong loi khi chua qua _bat_dau_chay.
        self._song_song_sem = threading.Semaphore(2)
        slug = ytf_slug_hoa(next(iter(self.du_lieu.values())).get("title") or "video-faceless")
        threading.Thread(target=self._tao_audio_1_luong,
                         args=(lang, self.du_lieu[lang], thu_muc, slug),
                         daemon=True).start()

    def _tao_audio_1_luong(self, lang, ban, thu_muc, slug):
        """1 luong doc lap cho 1 ngon ngu. Chi doc stop_event + job cua
        chinh no; loi o day chi gui job_loi cho ben nay, khong dung ben kia."""
        stop = self._stop_events[lang]
        job = self.jobs[lang]
        try:
            # (v7.14) Lech 2 giay cho VI khi song song ca 2 cung bat:
            # giam dot goi Edge TTS dong thoi. Chi lech khi che do
            # song song BAT va ca 2 ban deu co trong du_lieu.
            if (self.var_song_song.get() and lang == "vi" and "en" in self.du_lieu
                    and ytf_job_con_chay(self.jobs.get("en", {}))):
                time.sleep(YTF_SONG_SONG_TRE_VI_GIAY)
            _sem = getattr(self, "_song_song_sem", None)
            if _sem is None:
                ok = self._tao_audio_1_ban(lang, ban, thu_muc, slug, stop, job)
            else:
                with _sem:
                    ok = self._tao_audio_1_ban(lang, ban, thu_muc, slug, stop, job)
        except Exception as e:
            ok = False
            self.hang_doi.put(("log", "Lỗi %s (ngoại lệ, bên kia vẫn chạy): %s" % (lang.upper(), e)))
        if stop.is_set() or job.get("da_huy"):
            job["da_xong"] = True
            job["status"] = "da_huy"
            self.hang_doi.put(("log", "%s đã dừng/hủy — bên kia không bị ảnh hưởng." % lang.upper()))
            self.hang_doi.put(("job_xong", lang))
        elif ok:
            self.hang_doi.put(("job_xong", lang))
        elif (job.get("chua_xu_ly") or []):
            # (v7.16) Con cue chua xu ly: khong phai loi fatal — bao
            # "chua_xong" de anh goi lai, ben kia van chay binh thuong.
            self.hang_doi.put(("chua_xong", lang))
        else:
            self.hang_doi.put(("job_loi", (lang, job.get("loi") or "gộp MP3 lỗi")))
        getattr(self, "_retry_chi", {}).pop(lang, None)


    def _tao_audio_worker(self, du_lieu, thu_muc):
        """TUAN TU (cong tac song song TAT — hanh vi v7.13): chay EN roi
        VI trong 1 thread, dung co chung _yeu_cau_huy. Goi lai core
        _tao_audio_1_ban tung ben (state rieng tung ben)."""
        slug = ytf_slug_hoa(next(iter(du_lieu.values())).get("title") or "video-faceless")
        for lang, ban in du_lieu.items():
            if self._yeu_cau_huy.is_set() or self._stop_events[lang].is_set():
                break
            self._tao_audio_1_ban(lang, ban, thu_muc, slug,
                                  self._stop_events[lang], self.jobs[lang])
            self.hang_doi.put(("job_xong", lang))
        self.hang_doi.put(("log", "Thư mục kết quả: %s" % thu_muc))
        self.hang_doi.put(("xong", None))

    def _tao_audio_1_ban(self, lang, ban, thu_muc, slug, stop_event, job):
        """CORE 1 BAN (dung chung cho ca tuan tu va song song): doc tung
        cue SRT bang Edge TTS, nghi ngan giua cue, do thoi luong that,
        re-time SRT, gop MP3 ve chuan 44100/stereo/192k. CHI dung
        stop_event/job/duong ra cua chinh ngon ngu nay — khong dung
        state chung, nen 2 luong song song khong ghi de nhau.
        Tra True neu xong (ke ca khi 1 vai cue loi da bo qua), False
        neu gop MP3 loi hoac bi huy giua chung."""
        ffmpeg = tim_ffmpeg()
        if not ffmpeg:
            job["loi"] = "Không tìm thấy ffmpeg — không tạo được audio."
            self.hang_doi.put(("log", job["loi"]))
            return False
        _retry_chi = getattr(self, "_retry_chi", {}).get(lang)
        if _retry_chi is None:
            job["chua_xu_ly"] = []
            job["so_cue_thanh_cong"] = 0
        # (v7.15) Setting RIENG cot nay (khong dung setting chung).
        _col = self.col.get(lang, {}) if hasattr(self, "col") else {}
        try:
            nghi_ms = int((_col.get("e_nghi").get() if _col.get("e_nghi") is not None else self.e_nghi.get()) or 350)
        except Exception:
            nghi_ms = 350
        duong = ytf_duong_ra_theo_ngon_ngu(thu_muc, slug, lang)
        thu_muc_lang = duong["thu_muc_lang"]
        thu_muc_tam = duong["thu_muc_tam"]
        os.makedirs(thu_muc_tam, exist_ok=True)
        os.makedirs(thu_muc_lang, exist_ok=True)
        self.hang_doi.put(("log", "Đang tạo audio %s: %d cue..." % (lang, len(ban["srt_cues"]))))
        # (v7.16) Giong theo speaker: voice_id ghi ro trong JSON
        # thang; khong co thi giong mac dinh theo GIOI TINH cua
        # speaker do; cuoi cung moi dung giong dang chon o cot (UI).
        _col_cb = _col.get("cb_giong")
        _col_cb_b = _col.get("cb_giong_b")
        _ui_a = ytf_giong_id_cua_ten(_col_cb.get() if _col_cb is not None else YTF_GIONG_MAC_DINH[lang], lang)
        _ui_b = ytf_giong_id_cua_ten(_col_cb_b.get() if _col_cb_b is not None else YTF_GIONG_MAC_DINH[lang], lang)
        _info_a = ytf_speaker_info(ban, "A")
        _info_b = ytf_speaker_info(ban, "B")
        voice_id_a = ((_info_a.get("voice_id") and ytf_giong_cua_speaker(ban, "A")[0])
                      or ytf_giong_mac_dinh_theo_gioi_tinh(lang, _info_a.get("gender")) or _ui_a)
        voice_id_b = ((_info_b.get("voice_id") and ytf_giong_cua_speaker(ban, "B")[0])
                      or ytf_giong_mac_dinh_theo_gioi_tinh(lang, _info_b.get("gender")) or _ui_b)
        toc_do = float((_col.get("sl_toc_do").get() if _col.get("sl_toc_do") is not None else self.sl_toc_do.get()))
        # (v7.24) VieNeu: giong UI (Xuân Vĩnh/Phạm Tuyên) thắng giọng mặc định theo giới tính;
        # tốc độ mặc định 0.95x khi người dùng để 1.0.
        if str(_ui_a).startswith("vieneu:"):
            voice_id_a = _ui_a
        if str(_ui_b).startswith("vieneu:"):
            voice_id_b = _ui_b
        if toc_do == 1.0 and (str(voice_id_a).startswith("vieneu:") or str(voice_id_b).startswith("vieneu:")):
            toc_do = VIENEU_TOC_DO_MAC_DINH
        cao_do = int((_col.get("sl_cao_do").get() if _col.get("sl_cao_do") is not None else self.sl_cao_do.get()))
        cac_file, cue_durs = [], []
        _speaker_truoc = None
        _cho_local = bool((_col.get("var_local").get() if _col.get("var_local") is not None else False))
        _thanh_cong = 0
        _tong = len(ban["srt_cues"])
        for cue in ban["srt_cues"]:
            if stop_event.is_set() or self._yeu_cau_huy.is_set():
                return False
            _spk = cue.get("speaker", "A")
            voice_id = voice_id_b if _spk == "B" else voice_id_a
            if _spk != _speaker_truoc:
                _nhan = ""
                if cue.get("character") or cue.get("gender"):
                    _nhan = " — %s (%s)" % (cue.get("character") or "?",
                                             cue.get("gender") or "?")
                self.hang_doi.put(("log", "Cue %d (%s): dùng giọng %s (speaker %s%s)."
                                   % (cue["index"], lang, "2 (trả lời/phụ)" if _spk == "B" else "1 (hỏi/chính)", _spk, _nhan)))
                _speaker_truoc = _spk
            tam = os.path.join(thu_muc_tam, "_cue_%03d.mp3" % cue["index"])
            _can_doc = True
            if _retry_chi is not None and cue["index"] not in _retry_chi:
                # (v7.16) Goi lai chi cac cue loi: cue da xong truoc
                # do thi dung lai file tam, khong doc lai.
                if os.path.isfile(tam):
                    d = _do_dai_mp3_ms(tam, ffmpeg)
                    if d is None:
                        d = int(round((cue["end"] - cue["start"]) * 1000))
                    cue_durs.append(d)
                    cac_file.append((tam, None))
                    _thanh_cong += 1
                    job["so_cue_thanh_cong"] = _thanh_cong
                    self.hang_doi.put(("tien_do", (lang, ytf_tien_do_thanh_cong(_tong, _thanh_cong), _thanh_cong, _tong)))
                    _can_doc = False
                else:
                    ytf_them_chua_xu_ly(job.setdefault("chua_xu_ly", []), cue, lang,
                                        "Thiếu file tạm của cue đã xong trước đó — gọi lại cue này.")
                    self.hang_doi.put(("chua_xu_ly", (lang, dict(job["chua_xu_ly"][-1]))))
                    _can_doc = False
            if _can_doc:
                ok, _x, loi = doc_cau_thanh_mp3(cue["text"], voice_id, toc_do, cao_do, tam, log_cb=None, ffmpeg=ffmpeg)
                _da_local = False
                if not ok and _cho_local:
                    # (v7.16) Local CHI khi anh BAT tay cong tac:
                    # Edge loi roi moi doc bang giong may SAPI, va
                    # ghi ro trong log + danh sach.
                    self.hang_doi.put(("log", "Cue %d (%s) Edge lỗi (%s) — công tắc giọng máy local đang BẬT nên đọc lại bằng giọng máy local." % (cue["index"], lang, loi)))
                    ok, _x, loi = doc_cau_thanh_mp3(cue["text"], "may", toc_do, cao_do, tam, log_cb=None, ffmpeg=ffmpeg)
                    _da_local = bool(ok)
                if not ok:
                    ytf_them_chua_xu_ly(job.setdefault("chua_xu_ly", []), cue, lang,
                                        loi or "Edge TTS lỗi")
                    self.hang_doi.put(("chua_xu_ly", (lang, dict(job["chua_xu_ly"][-1]))))
                    self.hang_doi.put(("log", "Cue %d (%s) lỗi, GHI VÀO 'Giọng chưa xử lý' (không bỏ qua, không tự dùng giọng máy): %s" % (cue["index"], lang, loi)))
                    continue
                if _da_local:
                    _muc_local = {"index": cue["index"], "speaker": _spk,
                                  "character": cue.get("character", ""),
                                  "gender": cue.get("gender"),
                                  "text": cue.get("text", ""),
                                  "voice_id": "may",
                                  "loi": "Đã đọc bằng giọng máy local.",
                                  "lan_thu": 1, "da_dung_local": True}
                    _ds_local = job.setdefault("da_dung_local", [])
                    if not any(x.get("index") == cue["index"] for x in _ds_local):
                        _ds_local.append(_muc_local)
                    self.hang_doi.put(("log", "Cue %d (%s): ĐÃ ĐỌC BẰNG GIỌNG MÁY LOCAL (giọng sẽ khác giọng Edge) — kiểm tra lại trước khi dùng." % (cue["index"], lang)))
                    self.hang_doi.put(("chua_xu_ly", (lang, dict(_muc_local))))
                ytf_xoa_chua_xu_ly(job.setdefault("chua_xu_ly", []), cue["index"])
                self.hang_doi.put(("da_xu_ly", (lang, cue["index"])))
                d = _do_dai_mp3_ms(tam, ffmpeg)
                if d is None:
                    d = int(round((cue["end"] - cue["start"]) * 1000))
                cue_durs.append(d)
                cac_file.append((tam, None))
                _thanh_cong += 1
                job["so_cue_thanh_cong"] = _thanh_cong
                self.hang_doi.put(("tien_do", (lang, ytf_tien_do_thanh_cong(_tong, _thanh_cong), _thanh_cong, _tong)))
            if cue["index"] < len(ban["srt_cues"]):
                im = os.path.join(thu_muc_tam, "_nghi_%03d.mp3" % cue["index"])
                try:
                    subprocess.run([ffmpeg, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                                    "-t", "%.3f" % (nghi_ms / 1000.0), "-c:a", "libmp3lame",
                                    "-b:a", MP3_CHUAN_BITRATE, im],
                                   capture_output=True, timeout=30, **chay_ngam_kwargs())
                    cac_file.append((im, None))
                except Exception:
                    pass
        if stop_event.is_set() or self._yeu_cau_huy.is_set():
            return False
        # (v7.16) Chua xong het thi KHONG gop/xuat file final: MP3/SRT
        # chi duoc goi la xong khi danh sach chua xu ly rong.
        if job.get("chua_xu_ly"):
            job["loi"] = "Chưa xong: %d/%d cue chưa xử lý — ấn 'Gọi lại chỗ chưa xử lý'." % (len(job["chua_xu_ly"]), _tong)
            self.hang_doi.put(("log", job["loi"]))
            return False
        dich_mp3 = duong["mp3"]
        ok, loi = _gop_mp3_concat(cac_file, dich_mp3, ffmpeg, log_cb=None)
        if not ok:
            job["loi"] = "Gộp MP3 %s lỗi: %s" % (lang, loi)
            self.hang_doi.put(("log", job["loi"]))
            return False
        cues_final = ban["srt_cues"]
        if bool((_col.get("var_retime").get() if _col.get("var_retime") is not None else self.var_retime.get())):
            ds = [cue_durs[i] + (nghi_ms if i < len(ban["srt_cues"]) - 1 else 0)
                  for i in range(len(ban["srt_cues"]))]
            cues_final = ytf_retime_cues(ban["srt_cues"], ds, nghi_ms=0)
        with open(duong["srt"], "w", encoding="utf-8") as f:
            f.write(ytf_srt_tu_cues(cues_final))
        with open(duong["txt"], "w", encoding="utf-8") as f:
            f.write(ban.get("script_text", ""))
        job["files"] = {"mp3": dich_mp3, "srt": duong["srt"], "txt": duong["txt"]}
        self.hang_doi.put(("log", "Xong %s: %s (+ %s_final.srt, %s.txt) — MP3 chuẩn 44100/stereo/192k."
                           % (lang, dich_mp3, lang, lang)))
        return True


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
        # (v7.8) Hien thi tieu de tieng Viet duoi dong tieu de goc:
        # _tieu_de_viet=None: khong hien dong Viet; "DANG_DICH": dang
        # dich; chuoi khac: ten da dich / "(không dịch được)".
        # _ma_dich_tieu_de tang moi lan doi tieu de / xoa thong bao de
        # bo ket qua dich cu (luong nen ve tre).
        self._tieu_de_goc = ""
        self._tieu_de_viet = None
        self._dong_phu_tieu_de = ""
        self._ma_dich_tieu_de = 0
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
        # (v7.8) Tu bam nut "Tiep tuc tai xuong" tren hop thoai IDM:
        # MAC DINH TAT, luu config chung (khong theo job). Chi bam
        # ho nut doi dem nguoc, KHONG sua duoc loi IDM bi hong.
        self.idm_tu_bam_var = tk.BooleanVar(
            value=bool(cfg.get("idm_tu_bam_tiep_tuc", False)))
        # Tap hwnd cua so IDM da co truoc khi day link (chup o
        # bam_idm) + co dung luong canh IDM, de chi xu ly hop moi.
        self.idm_hwnd_da_co = set()
        self._idm_canh_dung = None

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
            # (v7.8) Hien ca ten Viet da luu (neu co), khong thi dich
            # o luong nen, khong phu thuoc cong tac dich_ten.
            self._dich_va_hien_tieu_de_viet(job["title"])
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
        # (v7.8) Tu bam nut "Tiep tuc tai xuong" tren hop IDM (IDM
        # bao file chay chinh bi hong, bat doi dem nguoc vai giay):
        # MAC DINH TAT, luu config chung (khong theo job). Tooltip
        # ghi ro gioi han: chi bam ho nut doi, khong sua loi IDM.
        self.chk_idm_tu_bam = tk.Checkbutton(
            f_auto, text="Tự bấm 'Tiếp tục tải xuống' trên hộp thoại IDM — mặc định TẮT",
            variable=self.idm_tu_bam_var,
            command=self._luu_idm_tu_bam)
        self.chk_idm_tu_bam.pack(anchor="w")
        ToolTip(self.chk_idm_tu_bam,
                "Sau khi đẩy link sang IDM, tool tự bấm hộ nút "
                "'Tiếp tục tải xuống' khi nó sáng lên sau đếm ngược "
                "(tối đa 60 giây). Chỉ bấm hộ nút chờ này, KHÔNG sửa "
                "được lỗi IDM báo file chạy chính bị hỏng — muốn hết "
                "hẳn thì tải bản IDM mới nhất về cài đè lên.")
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

    # ---------- (v7.8) tieu de tieng Viet duoi dong tieu de goc ----------
    def _hien_tieu_de(self):
        """Ghep dong 'Tieu de: ...' + dong 'Tieu de (Viet): ...' (neu co)
        + dong phu (thoi luong / chat luong) vao info_var."""
        if not self.con_song():
            return
        dong = []
        if self._tieu_de_goc:
            dong.append("Tiêu đề: %s" % self._tieu_de_goc)
        if self._tieu_de_viet == "DANG_DICH":
            dong.append("Tiêu đề (Việt): đang dịch...")
        elif self._tieu_de_viet:
            dong.append("Tiêu đề (Việt): %s" % self._tieu_de_viet)
        if self._dong_phu_tieu_de:
            dong.append(self._dong_phu_tieu_de)
        if dong:
            self.info_var.set("\n".join(dong))

    def _xoa_tieu_de(self):
        """Xoa trang thai tieu de + huy ket qua dich dang cho (tang ma)."""
        self._ma_dich_tieu_de += 1
        self._tieu_de_goc = ""
        self._tieu_de_viet = None
        self._dong_phu_tieu_de = ""

    def _dat_thong_bao_info(self, text):
        """Hien 1 dong thong bao (khong phai tieu de) len info_var, dong
        thoi huy ket qua dich tieu de dang cho."""
        self._xoa_tieu_de()
        self.info_var.set(text)

    def _dich_va_hien_tieu_de_viet(self, ten_goc):
        """Hien tieu de goc + dich sang tieng Viet o luong nen (khong do
        giao dien). KHONG phu thuoc cong tac dich_ten (cong tac do chi
        quyet dinh ten thu muc / ten file). Ten goc da la tieng Viet thi
        khong hien dong Viet thua. Dich loi thi hien '(không dịch được)'."""
        ten_goc = (ten_goc or "").strip()
        self._ma_dich_tieu_de += 1
        ma = self._ma_dich_tieu_de
        self._tieu_de_goc = ten_goc
        self._tieu_de_viet = None
        if not ten_goc:
            self._hien_tieu_de()
            return
        # Da co ten Viet luu trong job cho dung ten goc nay -> hien luon,
        # khong goi dich lai.
        ten_viet_luu = (self.job.get("title_vi") or "").strip()
        goc_luu = (self.job.get("title_vi_goc") or "").strip()
        if ten_viet_luu and goc_luu == ten_goc and ten_viet_luu != ten_goc:
            self._tieu_de_viet = ten_viet_luu
            self._hien_tieu_de()
            return
        # Ten goc khong co chu Trung -> da la tieng Viet / khong can dich.
        if not re.search(r"[\u4e00-\u9fff]", ten_goc):
            self._hien_tieu_de()
            return
        self._tieu_de_viet = "DANG_DICH"
        self._hien_tieu_de()
        threading.Thread(target=self._dich_tieu_de_worker,
                         args=(ma, ten_goc), daemon=True).start()

    def _dich_tieu_de_worker(self, ma, ten_goc):
        try:
            ket = ten_phim_tieng_viet(ten_goc, dich=True)
        except Exception:
            ket = ten_goc
        self.after_an_toan(0, self._dich_tieu_de_xong, ma, ten_goc, ket)

    def _dich_tieu_de_xong(self, ma, ten_goc, ket):
        if not self.con_song():
            return
        if ma != self._ma_dich_tieu_de or ten_goc != self._tieu_de_goc:
            return  # ket qua cu (da doi link / dong cua) -> bo qua
        ket = (ket or "").strip()
        if not ket or ket == sanitize_ten(ten_goc):
            # Dich tra ve y nguyen ten goc -> khong dich duoc (loi mang...).
            self._tieu_de_viet = "(không dịch được)"
        else:
            self._tieu_de_viet = ket
            try:
                self.job["title_vi"] = ket
                self.job["title_vi_goc"] = ten_goc
            except Exception:
                pass
            self.luu_job_hien_tai()
        self._hien_tieu_de()

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

    def _luu_idm_tu_bam(self):
        """(v7.8) Luu cong tac tu bam IDM vao config chung (mac dinh
        TAT). Chi luu key nay, khong dong den key khac (luu_config
        merge theo kieu GOP)."""
        try:
            luu_config({"idm_tu_bam_tiep_tuc":
                        bool(self.idm_tu_bam_var.get())})
        except Exception:
            pass

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
        # (v7.8) Huy ket qua dich tieu de dang cho (luong nen ve tre se
        # tu bo qua nho kiem tra ma + con_song()).
        self._ma_dich_tieu_de += 1
        self.dang_theo_doi_idm = False
        # (v7.8) Dung luong canh hop IDM (neu dang chay).
        try:
            if self._idm_canh_dung is not None:
                self._idm_canh_dung.set()
        except Exception:
            pass
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
        .srt roi thang vao thu muc goc (outdir).
        (v7.8) Ten thu muc + ten file phu de deu qua dung cong tac
        dich ten (ten_phim_tieng_viet): BAT thi dung ten tieng Viet
        da dich, TAT thi giu nguyen ten goc — truoc day ham nay dung
        thang job["title"] (ten goc tho) nen lech voi duong tai
        video. Viec tinh ten + tao thu muc chay trong luong nen
        (_tai_phu_de_worker) vi dich ten goi Google Translate (toi
        da 10s), khong duoc dong giao dien."""
        if not self.link_info:
            messagebox.showerror("Chưa kiểm tra", "Bấm Kiểm tra link trước đã.")
            return
        threading.Thread(target=self._tai_phu_de_worker,
                         args=(self.link_var.get().strip(),
                               self.cookies_var.get().strip(),
                               # (v7.8) Doc cac bien tkinter TREN LUONG
                               # CHINH roi truyen vao worker: doc
                               # StringVar tu luong nen khong an toan
                               # (co ban Tk se loi "main thread is not
                               # in main loop").
                               (self.job.get("title") or "").strip(),
                               bool(self.dich_ten_var.get()),
                               self.video_var.get().strip(),
                               self.outdir_var.get().strip(),
                               getattr(self, "thu_muc_phim", "")),
                         daemon=True).start()

    def _tai_phu_de_dat_thu_muc(self, folder):
        """(v7.8) Luong nen vua xac dinh xong thu muc phim (tao moi
        hoac dung lai thu muc da co — v7.10): cap nhat vao job tren
        luong chinh, luu job, ghi log."""
        self.thu_muc_phim = folder
        self.job["folder"] = folder
        self.luu_job_hien_tai()
        self.ghi_log("Thư mục phim: " + folder)

    def _tai_phu_de_worker(self, url, cookies, tieu_de_goc="", dich_ten=True,
                           video_file="", outdir="", folder_cu=""):
        try:
            if tieu_de_goc:
                ten_viet = ten_phim_tieng_viet(tieu_de_goc, dich=dich_ten)
            elif video_file:
                ten_viet = ten_phim_tu_ten_file(video_file, dich=dich_ten)
            else:
                ten_viet = "video"
            # (v7.10) 1 thu muc duy nhat cho 1 phim: dung lai thu muc
            # job da co / thu muc cung ten da co trong outdir, doi ten
            # thu muc ten goc sang ten Viet neu duoc — khong tao thu
            # muc thu 2 khi dich loi o buoc truoc.
            folder, _da_tao = _thu_muc_phim_duy_nhat(
                outdir, ten_viet, tieu_de_goc, job=self.job, url=url,
                log=self.log_threadsafe)
            if folder != folder_cu:
                self.after_an_toan(0, self._tai_phu_de_dat_thu_muc, folder)
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
        self._dat_thong_bao_info("Đã dán link, bấm Kiểm tra link để đọc thông tin.")
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
                self._dat_thong_bao_info("Đang tải yt-dlp tự động, chờ một chút...")
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
        self._dat_thong_bao_info("Đang đọc thông tin video, chờ một chút...")
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
        self._dat_thong_bao_info("Tải yt-dlp thất bại: " + msg)
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
        # (v7.8) Hien tieu de goc + dich tieu de Viet o luong nen.
        self._dong_phu_tieu_de = ("Thời lượng: %s | Chất lượng có: %s"
                                  % (dinh_dang_thoi_luong(info["duration"]),
                                     ", ".join(o["label"] for o in options)))
        self._dich_va_hien_tieu_de_viet(info["title"])
        self.btn_tai.config(state="normal")
        self.btn_idm.config(state="normal")
        self.ghi_log("Đã đọc link: %s" % info["title"])
        self.luu_job_hien_tai(status="da_kiem_tra")

    def _kiem_tra_loi(self, msg):
        self._dat_thong_bao_info("Lỗi: " + msg)
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
            # (v7.8) Ten thu muc (co the da dich theo cong tac dich_ten)
            # van hien them dong tieu de Viet neu ten goc la tieng Trung.
            self._dong_phu_tieu_de = ""
            self._dich_va_hien_tieu_de_viet(ten_viet)
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
        # (v7.8) Xem ghi chu o nhanh chi tai rieng phia tren.
        self._dong_phu_tieu_de = ""
        self._dich_va_hien_tieu_de_viet(ten_viet)
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
        # (v7.8) Chup truoc tap hwnd cua so IDM dang mo, de luong
        # canh sau nay chi xu ly hop MOI xuat hien sau lan day link
        # (khong bam nham hop IDM cu cua lan tai truoc).
        self.idm_hwnd_da_co = liet_ke_cua_so_idm()
        self.btn_idm.config(state="disabled")
        self.status_var.set("Đang đẩy link sang IDM...")
        threading.Thread(target=self._idm_worker,
                         args=(url, option, cookies, outdir),
                         daemon=True).start()

    def _bat_dau_canh_idm(self):
        """(v7.8) Neu cong tac tu bam IDM dang BAT thi chay luong nen
        canh hop thoai IDM trong 60s (doi nut 'Tiep tuc tai xuong'
        sang roi bam ho 1 lan). Chi chay 1 lan cho 1 lan day link;
        cong tac TAT thi khong lam gi. Luong nen khong chan UI."""
        try:
            if not self.idm_tu_bam_var.get():
                return
        except Exception:
            return
        try:
            if self._idm_canh_dung is not None:
                self._idm_canh_dung.set()
            self._idm_canh_dung = threading.Event()
            threading.Thread(
                target=canh_hop_idm_va_bam,
                kwargs={"log_cb": self.log_threadsafe,
                        "dung": self._idm_canh_dung,
                        "hwnd_da_co": set(
                            getattr(self, "idm_hwnd_da_co", set()))},
                daemon=True).start()
        except Exception as e:
            self.log_threadsafe(
                "Tự bấm IDM: không khởi động được luồng canh: %s" % e)

    def _idm_worker(self, url, option, cookies, outdir):
        try:
            folder, ten_video, ten_audio, tong_dung_luong = tai_bang_idm(
                url, option, cookies, outdir, self.log_threadsafe,
                dich_ten=self.dich_ten_var.get())
            # (v7.8) Day link xong: bat dau canh hop IDM ngay (khong
            # doi hop "Da day sang IDM" duoc bam OK, vi hop IDM co
            # the da dem nguoc xong trong luc do).
            self._bat_dau_canh_idm()
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
                os.makedirs(folder, exist_ok=True)
                luu_link_phim(folder, self.link_var.get().strip())
            else:
                # (v7.10) 1 thu muc duy nhat cho 1 phim (xem
                # _thu_muc_phim_duy_nhat): dung lai / doi ten thay
                # vi tao moi.
                folder, _da_tao = _thu_muc_phim_duy_nhat(
                    outdir, ten_viet,
                    ten_phim_tu_ten_file(video, dich=False),
                    job=self.job, url=self.link_var.get().strip(),
                    log=self.log_threadsafe)
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
        # (v7.8) Ten file thanh pham (co the da dich theo cong tac
        # dich_ten) van hien them dong tieu de Viet neu ten goc la
        # tieng Trung.
        self._dong_phu_tieu_de = ""
        self._dich_va_hien_tieu_de_viet(ten_viet)
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
                os.makedirs(folder, exist_ok=True)
                luu_link_phim(folder, self.link_var.get().strip())
            else:
                # (v7.10) 1 thu muc duy nhat cho 1 phim (xem
                # _thu_muc_phim_duy_nhat): dung lai / doi ten thay
                # vi tao moi.
                folder, _da_tao = _thu_muc_phim_duy_nhat(
                    outdir, ten_viet,
                    ten_phim_tu_ten_file(video, dich=False),
                    job=self.job, url=self.link_var.get().strip(),
                    log=self.log_threadsafe)
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
        # (v7.8) Ten file xuat theo dung cong tac dich ten (truoc day
        # goi khong truyen dich -> mac dinh True, lech khi cong tac
        # dang TAT: ten file nen / ten file giong khong khop ten file
        # phu de va file MP3 HoaiMy).
        ten_viet = ten_phim_tu_ten_file(nguon_ten,
                                        dich=self.dich_ten_var.get())
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
        # (v7.17) Dich bang web AI: mo trang Gemini ngay trong tool,
        # xem no chay truc tiep. Tool KHONG tu dinh kem file SRT duoc
        # (trinh duyet chan script tu set o chon file vi bao mat).
        khung_web = tk.LabelFrame(
            self, text=" Dịch bằng web AI (mở trang Gemini ngay trong tool) ",
            padx=8, pady=6)
        khung_web.grid(row=16, column=0, columnspan=3, sticky="nsew", **pad)
        tk.Label(khung_web, text=(
            "Cách dùng: bấm Sao chép prompt, rồi bấm Mở web AI — trang "
            "Gemini mở ngay trong tool (đăng nhập Google 1 lần, lần sau vẫn "
            "còn). Trên trang Gemini, bấm nút đính kèm, chọn file SRT, dán "
            "prompt (đã copy sẵn), bấm gửi rồi xem nó chạy. Lỗi thì bấm nút "
            "Hủy trong cửa sổ web (đóng cửa sổ, dừng luôn). Xong thì tải "
            "file kết quả từ trang Gemini, hoặc copy nội dung về dùng nút "
            "Nhập bản dịch về ở trên.\n"
            "Lưu ý: tool không tự đính kèm file SRT vào trang web được "
            "(trình duyệt chặn vì bảo mật) — cần 1 thao tác đính kèm bằng tay."),
            fg="gray", wraplength=640, justify="left").pack(anchor="w")
        # (v7.17) Che do web AI: thu cong / dung cookie (file cookies
        # RIENG cua trang web AI — KHAC file cookies Bilibili).
        self.che_do_web_ai_var = tk.StringVar(value="thu_cong")
        self.cookies_web_ai_var = tk.StringVar(value="")
        hang_che_do = tk.Frame(khung_web)
        hang_che_do.pack(fill="x", pady=(6, 0))
        tk.Label(hang_che_do, text="Chế độ:").pack(side="left")
        tk.Radiobutton(hang_che_do,
                       text="Thủ công (tự đăng nhập trong cửa sổ web)",
                       variable=self.che_do_web_ai_var, value="thu_cong",
                       command=self._cap_nhat_che_do_web_ai).pack(side="left")
        tk.Radiobutton(hang_che_do,
                       text="Dùng cookie (đăng nhập sẵn)",
                       variable=self.che_do_web_ai_var, value="cookie",
                       command=self._cap_nhat_che_do_web_ai).pack(side="left")
        self.hang_cookie_web = tk.Frame(khung_web)
        self.hang_cookie_web.pack(fill="x")
        tk.Label(self.hang_cookie_web,
                 text="Cookies web AI:").pack(side="left")
        self.e_cookies_web_ai = tk.Entry(
            self.hang_cookie_web, textvariable=self.cookies_web_ai_var,
            width=48)
        self.e_cookies_web_ai.pack(side="left", fill="x", expand=True,
                                   padx=4)
        self.btn_chon_cookies_web_ai = tk.Button(
            self.hang_cookie_web, text="Chọn cookies.txt...",
            command=self._chon_cookies_web_ai)
        self.btn_chon_cookies_web_ai.pack(side="left")
        tk.Label(khung_web, text=(
            "File cookies của TRANG WEB AI (vd gemini.google.com) — "
            "export bằng Get cookies.txt LOCALLY trên Chrome. KHÁC file "
            "cookies Bilibili."),
            fg="gray", wraplength=640, justify="left").pack(anchor="w")
        tk.Label(khung_web, text="Prompt dịch (sửa được):").pack(anchor="w")
        self.txt_prompt_web = scrolledtext.ScrolledText(khung_web, height=6)
        self.txt_prompt_web.pack(fill="both", expand=True)
        hang_web = tk.Frame(khung_web)
        hang_web.pack(fill="x", pady=(6, 0))
        tk.Button(hang_web, text="Sao chép prompt",
                  command=self._sao_chep_prompt_web_ai).pack(side="left", padx=4)
        tk.Button(hang_web, text="Khôi phục prompt gốc",
                  command=self._khoi_phuc_prompt_web_ai_goc).pack(side="left", padx=4)
        tk.Button(hang_web, text="Mở web AI", font=("", 11, "bold"),
                  command=self._mo_web_ai).pack(side="left", padx=4)
        self._nap_prompt_web_ai()
        self._nap_web_ai_che_do()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(14, weight=1)
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
        goi_y = {"Gemini": [MODEL_TU_DONG, MODEL_GEMINI_MAC_DINH,
                            MODEL_GEMINI_DU_PHONG],
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

    def _nap_prompt_web_ai(self):
        """(v7.17) Nap prompt web AI: uu tien ban da sua luu local
        (config 'prompt_dich_web_ai'), khong co thi dung prompt chuan."""
        try:
            cfg = doc_config()
            prompt = (cfg.get("prompt_dich_web_ai") or "").strip()
        except Exception:
            prompt = ""
        if not prompt:
            prompt = PROMPT_DICH_WEB_AI_MAC_DINH
        try:
            self.txt_prompt_web.delete("1.0", "end")
            self.txt_prompt_web.insert("1.0", prompt)
        except Exception:
            pass

    def _lay_prompt_web_ai(self):
        try:
            return self.txt_prompt_web.get("1.0", "end").strip()
        except Exception:
            return PROMPT_DICH_WEB_AI_MAC_DINH

    def _sao_chep_prompt_web_ai(self):
        """(v7.17) Copy prompt vao clipboard + luu ban da sua (local)
        de lan sau mo lai van la ban do."""
        prompt = self._lay_prompt_web_ai()
        if not prompt:
            messagebox.showerror(
                "Thiếu prompt",
                "Ô prompt đang trống — bấm Khôi phục prompt gốc để lấy "
                "lại prompt chuẩn.")
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(prompt)
            self.update()
        except Exception as e:
            messagebox.showerror("Không copy được", str(e))
            return
        try:
            cfg = doc_config()
            cfg["prompt_dich_web_ai"] = prompt
            luu_config(cfg)
        except Exception:
            pass
        self.status_var.set(
            "Đã sao chép prompt dịch vào clipboard (đã lưu bản này).")

    def _khoi_phuc_prompt_web_ai_goc(self):
        """(v7.17) Tra o prompt ve prompt chuan + xoa ban sua local."""
        try:
            cfg = doc_config()
            cfg.pop("prompt_dich_web_ai", None)
            luu_config(cfg)
        except Exception:
            pass
        try:
            self.txt_prompt_web.delete("1.0", "end")
            self.txt_prompt_web.insert("1.0", PROMPT_DICH_WEB_AI_MAC_DINH)
        except Exception:
            pass
        self.status_var.set("Đã khôi phục prompt gốc (prompt chuẩn dịch phim).")

    def _cap_nhat_che_do_web_ai(self):
        """(v7.17) Bat/tat hang chon cookies theo che do web AI."""
        la_cookie = (self.che_do_web_ai_var.get() or "") == "cookie"
        trang_thai = "normal" if la_cookie else "disabled"
        for w in (getattr(self, "e_cookies_web_ai", None),
                  getattr(self, "btn_chon_cookies_web_ai", None)):
            try:
                if w is not None:
                    w.configure(state=trang_thai)
            except Exception:
                pass

    def _nap_web_ai_che_do(self):
        """(v7.17) Nap che do + file cookies web AI da luu (local)."""
        try:
            cfg = doc_config()
            che_do = (cfg.get("web_ai_che_do") or "thu_cong").strip()
            if che_do not in ("thu_cong", "cookie"):
                che_do = "thu_cong"
            self.che_do_web_ai_var.set(che_do)
            self.cookies_web_ai_var.set(cfg.get("web_ai_cookies") or "")
        except Exception:
            pass
        self._cap_nhat_che_do_web_ai()

    def _luu_web_ai_che_do(self):
        """(v7.17) Luu che do + file cookies web AI (local)."""
        try:
            cfg = doc_config()
            cfg["web_ai_che_do"] = self.che_do_web_ai_var.get()
            cfg["web_ai_cookies"] = self.cookies_web_ai_var.get().strip()
            luu_config(cfg)
        except Exception:
            pass

    def _chon_cookies_web_ai(self):
        """(v7.17) Chon file cookies.txt RIENG cua trang web AI
        (KHAC file cookies Bilibili)."""
        p = filedialog.askopenfilename(
            title="Chọn file cookies.txt của trang web AI",
            filetypes=[("Cookies txt", "*.txt"), ("Mọi file", "*.*")])
        if p:
            self.cookies_web_ai_var.set(p)
            self._luu_web_ai_che_do()
            try:
                so = len(doc_cookies_txt_web_ai(p))
                self.status_var.set(
                    "Đã chọn cookies web AI: %s (%d cookie)."
                    % (os.path.basename(p), so))
            except Exception as e:
                self.status_var.set(
                    "Đã chọn cookies web AI (chưa đọc được: %s)." % e)

    def _mo_web_ai(self):
        """(v7.17) Mo trang Gemini ngay trong tool (pywebview /
        Edge WebView2, chi co tren ban Windows). Profile rieng luu ben
        trong thu muc tool -> dang nhap Google 1 lan, lan sau van con.
        2 che do: 'thu_cong' (tu dang nhap/dan prompt/dinh kem file
        SRT trong cua so web); 'cookie' (ap file cookies.txt RIENG
        cua trang web AI — KHAC file cookies Bilibili — qua
        CookieManager cua WebView2 de mo ra da dang nhap; ap khong
        duoc thi bao ro va de dang nhap tay 1 lan). Nut Huy trong
        cua so web dong cua so, dung luon."""
        if _pywebview is None:
            messagebox.showinfo(
                "Mở web AI — cần bản Windows",
                "Cửa sổ web AI dùng pywebview (Edge WebView2 có sẵn trên "
                "Windows 10/11) nên chỉ mở được trên bản Windows của tool.\n\n"
                "Trên máy này chưa có pywebview — mở tạm trang Gemini "
                "bằng trình duyệt:\n%s\n\n"
                "Trên bản Windows, bấm nút này sẽ mở cửa sổ web ngay trong "
                "tool, đăng nhập Google 1 lần rồi lần sau vẫn còn."
                % GEMINI_WEB_URL)
            return
        self._luu_web_ai_che_do()
        che_do = self.che_do_web_ai_var.get()
        cac_cookie = []
        if che_do == "cookie":
            p = self.cookies_web_ai_var.get().strip()
            if not p or not os.path.isfile(p):
                messagebox.showerror(
                    "Thiếu file cookies",
                    "Chế độ 'Dùng cookie' cần file cookies.txt của "
                    "TRANG WEB AI (vd gemini.google.com).\n\n"
                    "Mở Chrome, vào trang web AI, export bằng "
                    "Get cookies.txt LOCALLY rồi bấm 'Chọn "
                    "cookies.txt...'.\n\n"
                    "File này KHÁC file cookies Bilibili.")
                return
            try:
                cac_cookie = doc_cookies_txt_web_ai(p)
            except Exception as e:
                messagebox.showerror("Lỗi đọc cookies", str(e))
                return
            if not cac_cookie:
                messagebox.showerror(
                    "File cookies rỗng",
                    "Không đọc được cookie nào trong file đã chọn. "
                    "Kiểm tra lại file cookies.txt export từ Chrome.")
                return
            self.status_var.set(
                "Đã nạp %d cookie web AI — đang mở cửa sổ web..."
                % len(cac_cookie))
        else:
            self.status_var.set("Đang mở cửa sổ web AI (Gemini)...")
        try:
            thu_muc_profile = os.path.join(app_dir(), "web-ai-profile")
            os.makedirs(thu_muc_profile, exist_ok=True)
            os.environ["WEBVIEW2_USER_DATA_FOLDER"] = thu_muc_profile
        except Exception:
            pass

        def _chay():
            da_ap = {"xong": False}

            def _khi_tai():
                try:
                    _them_nut_huy_web_ai(win)
                except Exception:
                    pass
                if cac_cookie and not da_ap["xong"]:
                    da_ap["xong"] = True
                    dem, loi = _ap_cookie_web_ai(win, cac_cookie)
                    if dem > 0:
                        try:
                            self.after(0, lambda: self.status_var.set(
                                "Đã áp %d cookie web AI — đang tải lại "
                                "trang..." % dem))
                        except Exception:
                            pass
                        try:
                            win.evaluate_js("location.reload();")
                        except Exception:
                            pass
                    else:
                        try:
                            _dat_cookie_js_web_ai(win, cac_cookie)
                        except Exception:
                            pass
                        msg = ("Không áp được cookies vào cửa sổ web AI"
                               + ((" (%s)" % loi) if loi else "")
                               + ".\n\nĐăng nhập tay trong cửa sổ này 1 "
                                 "lần, lần sau mở lại vẫn còn (profile "
                                 "đã lưu trong thư mục tool).")

                        def _bao(m=msg):
                            messagebox.showinfo(
                                "Cookies chưa áp được — đăng nhập tay", m)
                        try:
                            self.after(0, _bao)
                        except Exception:
                            pass
            try:
                api = _ApiWebAI()
                win = _pywebview.create_window(
                    "Dịch bằng web AI — Gemini (trong tool)",
                    GEMINI_WEB_URL, width=1100, height=750, js_api=api)
                api.cua_so = win
                try:
                    win.events.loaded += _khi_tai
                except Exception:
                    pass
                _pywebview.start()
            except Exception as e:
                try:
                    self.after(0, lambda: self.status_var.set(
                        "Không mở được cửa sổ web AI: %s" % e))
                except Exception:
                    pass
        threading.Thread(target=_chay, daemon=True).start()

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

class CuaSoDuyetVideo(tk.Frame):  # (v7.9) Frame trong Notebook, giai doan 1+2: tim tu khoa + de xuat trang chu
    """Tab Duyet video (giai doan 1+2): tim phim Bilibili theo tu khoa
    hoac xem de xuat trang chu (chuyen che do o hang tim kiem).
    Giai doan 1: tim qua API tim kiem cong khai (khong can dang nhap;
    co cookies.txt thi kem Cookie, khong co van tim an danh).
    Giai doan 2: de xuat trang chu qua API rcmd — de xuat dung gu
    CAN cookies.txt da dang nhap; khong co cookies thi thu an danh,
    khong duoc thi bao ro trong tab la can import cookies.txt.
    Ket qua hien anh bia + tieu de; icon phu de nam SAU ten phim
    + tieu de; icon phu de nam SAU ten phim nhung CHI kiem tra khi
    CYAN bam vao video do (khong quet ca luoi). (v7.21) Ket qua dang
    THE DOC: anh bia 16:9 full chieu rong cot o tren, chu o duoi;
    re vao tieu de/link hien tooltip day du; bam phai sao chep
    link/ten phim; bam trai mo chi tiet nhu cu. (v7.21) Sap xep
    "Liên quan nhất"/"Mới nhất" (order=totalrank/pubdate); nut
    "Đẩy sang tab tải" tren the + chi tiet (dien link 1-mach +
    chuyen tab Quan ly); yeu thich ☆/★ luu video-yeu-thich.json
    + loc "Chỉ hiện video yêu thích"; kiem tra cookie Bilibili
    (nut o ca 2 tab + canh bao do khi cookie chet / API -101). Bam 1 video thi hien
    chi tiet: cac phan (chon phan can tai), cot de xuat ben phai nhu
    Bilibili. Phan da chon duoc mo bang CuaSoJob nhu dan link (luong
    tai/gop san co, khong lam luong tai rieng). Moi goi mang chay
    luong nen, cap nhat giao dien qua after() — khong hien console."""

    def __init__(self, quan_ly, parent=None):
        super().__init__(parent)
        self.quan_ly = quan_ly
        self.ket_qua = []
        # (v7.21) Thu tu goc cua API de xuat (de tra ve "Liên quan
        # nhất" sau khi da sap "Mới nhất" phia client).
        self.ket_qua_goc = []
        # (v7.21) Video yeu thich: doc tu video-yeu-thich.json luc
        # mo tab (khoi dong lai tool van con); danh dau theo bvid
        # nen tim lai/tim moi van giu dau ★.
        self._yeu_thich = doc_video_yeu_thich()
        self.trang_hien_tai = 1
        self.tu_khoa_hien_tai = ""
        self.video_da_chon = None
        self.chi_tiet = None
        self.lien_quan = []
        self.phu_de_hien_tai = None
        self._ma_tim = 0
        self._ma_chi_tiet = 0
        self._anh_bia = {}
        # (v7.21) The doc: bytes anh goc theo bvid (de fit lai khi cot
        # doi rong) + chieu rong anh dang dung + id lich fit
        # (debounce). Khoi tao o day (khong chi o _hien_ket_qua) vi
        # <Configure> cua cot co the kich fit ngay khi mo tab, truoc
        # ca lan tim dau tien.
        self._anh_bia_bytes = {}
        self._rong_anh_bia_hien_tai = 0
        self._fit_anh_id = None
        self._hang_ket_qua = {}
        self._hang_dang_chon = None
        self._phan_vars = {}
        self._hang_phan = {}
        # (v7.21) Trang thai cookie da kiem tra (None = chua biet):
        # "song"/"chet"/"khong_sessdata"/"khong_file". Doi file
        # cookies thi reset ve None de kiem tra lai khi tim sau.
        self._cookie_trang_thai = None
        self._dang_kiem_tra_cookie_nen = False
        try:
            self.quan_ly.cookies_var.trace_add(
                "write", self._cookie_doi_file)
        except Exception:
            pass

        cfg = doc_config()
        self.tu_khoa_var = tk.StringVar(value="")
        self.che_do_var = tk.StringVar(value="tu_khoa")
        self.trang_var = tk.StringVar(value="Trang 1")
        self.trang_thai_var = tk.StringVar(
            value="Gõ từ khóa rồi bấm Tìm — vd: hệ thống, tu tiên, mạt thế sinh tồn.")
        self.tu_tai_anh_bia_var = tk.BooleanVar(
            value=bool(cfg.get("duyet_video_tu_tai_anh_bia", True)))

        pad = {"padx": 6, "pady": 4}

        # ---- Hang tim kiem ----
        hang_tim = tk.Frame(self)
        hang_tim.pack(fill="x", **pad)
        tk.Label(hang_tim, text="Từ khóa:").pack(side="left")
        self.ent_tu_khoa = tk.Entry(hang_tim, textvariable=self.tu_khoa_var,
                                    width=42)
        self.ent_tu_khoa.pack(side="left", padx=4)
        self.ent_tu_khoa.bind("<Return>", lambda e: self._bam_tim())
        self.btn_tim = tk.Button(hang_tim, text="Tìm", font=("", 11, "bold"),
                                 command=self._bam_tim)
        self.btn_tim.pack(side="left", padx=4)
        self.btn_truoc = tk.Button(hang_tim, text="◀ Trước",
                                   command=self._trang_truoc)
        self.btn_truoc.pack(side="left", padx=4)
        self.btn_sau = tk.Button(hang_tim, text="Sau ▶",
                                 command=self._trang_sau)
        self.btn_sau.pack(side="left", padx=4)
        tk.Label(hang_tim, textvariable=self.trang_var, fg="gray").pack(
            side="left", padx=4)
        # (v7.9 giai doan 2) Cong tac che do: tim tu khoa / de xuat
        # trang chu (cung tab, cung luoi ket qua + chi tiet).
        self.rad_tu_khoa = tk.Radiobutton(
            hang_tim, text="Tìm theo từ khóa", variable=self.che_do_var,
            value="tu_khoa", command=self._doi_che_do)
        self.rad_tu_khoa.pack(side="left", padx=4)
        self.rad_de_xuat = tk.Radiobutton(
            hang_tim, text="Đề xuất trang chủ", variable=self.che_do_var,
            value="de_xuat", command=self._doi_che_do)
        self.rad_de_xuat.pack(side="left", padx=4)
        # (v7.21) Sap xep ket qua: "Liên quan nhất" (order=totalrank,
        # mac dinh, nhu cu) / "Mới nhất" (order=pubdate — moi nhat
        # theo thoi gian dang tai len Bilibili). O che do de xuat,
        # rcmd co san pubdate nen sap xep phia client (khong goi
        # lai API); o che do tu khoa thi tim lai ngay voi order moi.
        tk.Label(hang_tim, text="Sắp xếp:").pack(side="left", padx=(8, 2))
        self.sap_xep_var = tk.StringVar(value="Liên quan nhất")
        self.menu_sap_xep = tk.OptionMenu(
            hang_tim, self.sap_xep_var, "Liên quan nhất", "Mới nhất",
            command=lambda _v: self._doi_sap_xep())
        self.menu_sap_xep.pack(side="left")
        # (v7.21) Loc chi-yeu-thich: bat thi danh sach chi hien video
        # da luu (doc tu video-yeu-thich.json, khong phu thuoc tu
        # khoa); tat thi ve lai ket qua tim kiem/de xuat binh thuong
        # (van giu dau ★). Lam viec cung sap xep "Mới nhất".
        self.chi_yeu_thich_var = tk.BooleanVar(value=False)
        self.chk_chi_yeu_thich = tk.Checkbutton(
            hang_tim, text="Chỉ hiện video yêu thích",
            variable=self.chi_yeu_thich_var,
            command=self._doi_loc_yeu_thich)
        self.chk_chi_yeu_thich.pack(side="left", padx=8)
        self.chk_anh_bia = tk.Checkbutton(
            hang_tim, text="Tự tải ảnh bìa",
            variable=self.tu_tai_anh_bia_var,
            command=self._luu_tu_tai_anh_bia)
        self.chk_anh_bia.pack(side="left", padx=8)
        ToolTip(self.chk_anh_bia,
                "Bỏ tích thì không tải ảnh bìa (chỉ hiện khung chờ). "
                "Hiện ảnh bìa cần thư viện Pillow (pip install pillow); "
                "chưa có thì vẫn tìm + tải bình thường.")

        # (v7.21) Hang cookies: dung CHUNG cookies_var cua QuanLy (cung
        # file cookies.txt voi tab Quan ly + cua so job) — khong tao
        # bien/file cookie rieng. Chua co cookies thi Bilibili chi cho
        # 480p/360p va kiem tra phu de co the khong thay phu de AI.
        hang_cookie = tk.Frame(self)
        hang_cookie.pack(fill="x", **pad)
        tk.Label(hang_cookie,
                 text="File cookies.txt (để tải 1080p):").pack(side="left")
        self.ent_cookies = tk.Entry(
            hang_cookie, textvariable=self.quan_ly.cookies_var, width=52)
        self.ent_cookies.pack(side="left", padx=4, fill="x", expand=True)
        tk.Button(hang_cookie, text="Chọn...",
                  command=self.quan_ly.chon_cookies).pack(side="left",
                                                          padx=4)
        # (v7.21) Kiem tra cookie: chay o luong nen, ket qua hien
        # ngay canh nut; cookie chet thi hien them canh bao do ben
        # duoi (khong chan tim kiem an danh).
        tk.Button(hang_cookie, text="Kiểm tra cookie",
                  command=self._bam_kiem_tra_cookie).pack(side="left",
                                                          padx=4)
        self.lbl_ket_qua_cookie = tk.Label(
            hang_cookie, text="", fg="gray", wraplength=320,
            justify="left", anchor="w")
        self.lbl_ket_qua_cookie.pack(side="left", padx=4)
        tk.Label(self,
                 text="Chưa có cookies thì chỉ thấy 480p và có thể "
                      "không thấy phụ đề AI.",
                 fg="gray", anchor="w").pack(fill="x", **pad)
        # (v7.21) Canh bao cookie chet: an mac dinh, chi hien khi
        # kiem tra thay cookie het han hoac API tra -101.
        self.lbl_canh_bao_cookie = tk.Label(
            self, text="", fg="red", wraplength=980, justify="left",
            anchor="w")
        self.lbl_canh_bao_cookie.pack(fill="x", **pad)

        tk.Label(self, text="Bấm 1 video để xem các phần + kiểm tra phụ đề "
                 "(chỉ kiểm tra video đã bấm, không quét cả lưới kết quả).",
                 fg="gray", anchor="w").pack(fill="x", **pad)

        # ---- 2 cot: trai = ket qua, phai = chi tiet ----
        panel = tk.PanedWindow(self, orient="horizontal", sashrelief="raised")
        panel.pack(fill="both", expand=True, **pad)
        khung_trai = tk.Frame(panel)
        self.lbl_tieu_de_trai = tk.Label(
            khung_trai, text="Kết quả tìm kiếm",
            font=("", 11, "bold"), anchor="w")
        self.lbl_tieu_de_trai.pack(fill="x")
        self.khung_ket_qua_ngoai, self.khung_ket_qua = self._tao_khung_cuon(
            khung_trai)
        self.khung_ket_qua_ngoai.pack(fill="both", expand=True)
        # (v7.21) Cot doi rong (cua so phong to / keo sash) thi fit lai
        # anh bia cho phu het chieu rong moi (debounce 150ms).
        self.khung_ket_qua.bind("<Configure>",
                                self._len_lich_fit_anh_bia, add="+")
        # (v7.21) Goi y sao chep bang chuot phai.
        tk.Label(khung_trai,
                 text="Bấm phải vào 1 video để sao chép link / tên phim",
                 fg="gray", anchor="w").pack(fill="x")
        panel.add(khung_trai, minsize=380)
        khung_phai = tk.Frame(panel)
        tk.Label(khung_phai, text="Chi tiết video (bấm 1 video bên trái)",
                 font=("", 11, "bold"), anchor="w").pack(fill="x")
        self.khung_chi_tiet_ngoai, self.khung_chi_tiet = self._tao_khung_cuon(
            khung_phai)
        self.khung_chi_tiet_ngoai.pack(fill="both", expand=True)
        panel.add(khung_phai, minsize=380)

        # ---- Duoi: trang thai + log ----
        tk.Label(self, textvariable=self.trang_thai_var, fg="gray",
                 wraplength=980, justify="left", anchor="w").pack(fill="x", **pad)
        self.log = scrolledtext.ScrolledText(self, height=4, state="disabled")
        self.log.pack(fill="x", **pad)

    # ---------- tien ich khung / log ----------

    def con_song(self):
        try:
            return bool(self.winfo_exists())
        except Exception:
            return False

    def _after_an_toan(self, ms, func, *args):
        if not self.con_song():
            return
        try:
            self.after(ms, func, *args)
        except Exception:
            pass

    def _ghi_log(self, s):
        try:
            self.after(0, lambda: self._ghi_log_truc_tiep(s))
        except Exception:
            pass

    def _ghi_log_truc_tiep(self, s):
        if not self.con_song():
            return
        try:
            self.log.config(state="normal")
            self.log.insert("end", s + "\n")
            self.log.see("end")
            self.log.config(state="disabled")
        except Exception:
            pass

    def _dat_trang_thai(self, s):
        if not self.con_song():
            return
        try:
            self.trang_thai_var.set(s)
        except Exception:
            pass

    def _lay_cookies(self):
        try:
            return (self.quan_ly.cookies_var.get() or "").strip()
        except Exception:
            return ""

    # ---------- (v7.21) kiem tra + canh bao cookie ----------
    CANH_BAO_COOKIE_CHET = (
        "Cookie Bilibili đã hết hạn — xuất lại cookies.txt từ Chrome "
        "(đăng nhập Bilibili trước) rồi import lại; hiện tại chỉ xem "
        "được 480p và có thể không thấy phụ đề AI.")

    def _cookie_doi_file(self, *_args):
        """File cookies doi (chon file moi / sua o nhap) thi quen
        ket qua kiem tra cu de lan tim sau kiem tra lai."""
        self._cookie_trang_thai = None
        self._hien_canh_bao_cookie_chet(False)

    def _hien_canh_bao_cookie_chet(self, hien=True):
        try:
            self.lbl_canh_bao_cookie.configure(
                text=self.CANH_BAO_COOKIE_CHET if hien else "")
        except Exception:
            pass

    def _bam_kiem_tra_cookie(self):
        """Nut 'Kiểm tra cookie' o tab Duyet video: dung chung ham
        cua QuanLy; xong thi cap nhat them canh bao cookie chet
        trong tab."""
        try:
            self.quan_ly.kiem_tra_cookie(
                self.lbl_ket_qua_cookie,
                khi_xong=self._sau_khi_kiem_tra_cookie)
        except Exception:
            pass

    def _sau_khi_kiem_tra_cookie(self, kq):
        """Callback sau khi kiem tra cookie xong (luong chinh):
        luu trang thai + hien/an canh bao cookie chet."""
        try:
            self._cookie_trang_thai = (kq or {}).get("trang_thai")
        except Exception:
            pass
        tt = self._cookie_trang_thai
        self._hien_canh_bao_cookie_chet(
            tt in ("chet", "khong_sessdata"))

    def _kiem_tra_cookie_nen(self):
        """(v7.21) Kiem tra cookie NGAM truoc khi tim/chi tiet neu
        co file cookies ma chua biet trang thai: chay nav API o
        luong nen; cookie chet thi hien canh bao do (khong chan
        tim kiem an danh). Chi kiem tra 1 lan cho den khi doi file
        (cache _cookie_trang_thai)."""
        if self._dang_kiem_tra_cookie_nen:
            return
        if self._cookie_trang_thai is not None:
            return
        if not self._lay_cookies():
            return  # khong co file -> chi hien ghi chu xam, khong goi API
        self._dang_kiem_tra_cookie_nen = True

        def _chay():
            kq = kiem_tra_cookie_bilibili(self._lay_cookies())

            def _hien():
                self._dang_kiem_tra_cookie_nen = False
                self._sau_khi_kiem_tra_cookie(kq)
            try:
                self.after(0, _hien)
            except Exception:
                self._dang_kiem_tra_cookie_nen = False

        threading.Thread(target=_chay, daemon=True).start()

    def _co_the_cookie_chet(self, msg):
        """(v7.21) Loi API co dau hieu cookie chet (-101 / loi can
        cookie de xuat) thi hien canh bao do trong tab."""
        try:
            s = str(msg or "")
        except Exception:
            return
        if ("-101" in s
                or DUYET_VIDEO_LOI_CAN_COOKIE_DE_XUAT in s
                or "yêu cầu đăng nhập" in s):
            self._hien_canh_bao_cookie_chet(True)
            self._cookie_trang_thai = "chet"

    def _tao_khung_cuon(self, parent):
        """Khung cuon doc (Canvas + Scrollbar + Frame trong): tra ve
        (khung_ngoai, khung_trong). Dung cho danh sach ket qua va
        panel chi tiet (so hang thay doi theo ket qua tim kiem)."""
        khung_ngoai = tk.Frame(parent)
        canvas = tk.Canvas(khung_ngoai, highlightthickness=0)
        sb = ttk.Scrollbar(khung_ngoai, orient="vertical",
                           command=canvas.yview)
        khung_trong = tk.Frame(canvas)
        cua_so = canvas.create_window((0, 0), window=khung_trong,
                                      anchor="nw")
        khung_trong.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cua_so, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _cuon(event):
            try:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
                else:
                    canvas.yview_scroll(int(-event.delta / 120), "units")
            except Exception:
                pass

        canvas.bind("<MouseWheel>", _cuon)
        canvas.bind("<Button-4>", _cuon)
        canvas.bind("<Button-5>", _cuon)
        return khung_ngoai, khung_trong

    @staticmethod
    def _dinh_dang_luot_xem(gia_tri):
        try:
            return "{:,}".format(int(gia_tri or 0))
        except Exception:
            return str(gia_tri or 0)

    def _luu_tu_tai_anh_bia(self):
        try:
            luu_config({"duyet_video_tu_tai_anh_bia":
                        bool(self.tu_tai_anh_bia_var.get())})
        except Exception:
            pass

    # ---------- tim kiem ----------

    def _bam_tim(self):
        # Nut chung 2 che do: tu khoa -> tim trang 1; de xuat -> tai
        # de xuat trang chu (khong can tu khoa).
        if self.che_do_var.get() == "de_xuat":
            self._tai_de_xuat()
        else:
            self._tim_trang(1)

    def _trang_truoc(self):
        if self.che_do_var.get() != "tu_khoa":
            return  # de xuat trang chu khong co phan trang
        if self.trang_hien_tai > 1 and self.tu_khoa_hien_tai:
            self._tim_trang(self.trang_hien_tai - 1)

    def _trang_sau(self):
        if self.che_do_var.get() != "tu_khoa":
            return  # de xuat trang chu khong co phan trang
        if self.tu_khoa_hien_tai:
            self._tim_trang(self.trang_hien_tai + 1)

    def _tim_trang(self, page):
        tu_khoa = self.tu_khoa_var.get().strip()
        if not tu_khoa:
            messagebox.showerror("Thiếu từ khóa",
                                 "Gõ từ khóa cần tìm trước đã.")
            return
        self._kiem_tra_cookie_nen()  # (v7.21) cookie chet -> canh bao do
        self.tu_khoa_hien_tai = tu_khoa
        self.trang_hien_tai = int(page or 1)
        self._ma_tim += 1
        ma = self._ma_tim
        self._dat_trang_thai("Đang tìm '%s' (trang %d)..."
                             % (tu_khoa, self.trang_hien_tai))
        self.btn_tim.config(state="disabled")
        self.btn_truoc.config(state="disabled")
        self.btn_sau.config(state="disabled")
        threading.Thread(target=self._tim_worker,
                         args=(ma, tu_khoa, self.trang_hien_tai),
                         daemon=True).start()

    def _tim_worker(self, ma, tu_khoa, page):
        try:
            ket_qua = tim_kiem_bilibili(
                tu_khoa, page=page, cookies=self._lay_cookies(),
                log=self._ghi_log, order=self._lay_order_tim_kiem())
            self._after_an_toan(0, self._tim_xong, ma, ket_qua, page)
        except Exception as e:
            self._after_an_toan(0, self._tim_loi, ma, str(e))

    def _tim_xong(self, ma, ket_qua, page):
        if ma != self._ma_tim or not self.con_song():
            return
        self.ket_qua = ket_qua or []
        self._hien_ket_qua()
        self.trang_var.set("Trang %d" % page)
        self.btn_tim.config(state="normal")
        self.btn_truoc.config(state="normal")
        self.btn_sau.config(state="normal")
        if not self.ket_qua:
            self._dat_trang_thai("Không tìm thấy video nào cho '%s' "
                                 "(trang %d)."
                                 % (self.tu_khoa_hien_tai, page))
        else:
            self._dat_trang_thai("Tìm thấy %d video (trang %d) — bấm 1 "
                                 "video để xem các phần."
                                 % (len(self.ket_qua), page))

    def _tim_loi(self, msg):
        if not self.con_song():
            return
        self._co_the_cookie_chet(msg)  # (v7.21) -101 -> canh bao do
        self.btn_tim.config(state="normal")
        self.btn_truoc.config(state="normal")
        self.btn_sau.config(state="normal")
        self._dat_trang_thai("Tìm kiếm lỗi: " + msg)
        self._ghi_log("Tìm kiếm LỖI: " + msg)
        messagebox.showerror("Tìm kiếm lỗi", msg)

    # ---------- (v7.21) sap xep + day sang tab tai ----------
    def _lay_order_tim_kiem(self):
        """Dropdown sap xep -> order cho API tim kiem: "Mới nhất"
        = pubdate, con lai = totalrank (lien quan nhat)."""
        try:
            return ("pubdate" if self.sap_xep_var.get() == "Mới nhất"
                    else "totalrank")
        except Exception:
            return "totalrank"

    def _ap_dung_sap_xep_hien_tai(self):
        """Sap xep phia client cho danh sach hien co (chi dung o
        che do de xuat — che do tu khoa API da sap san): "Mới nhất"
        thi sap theo pubdate giam dan; "Liên quan nhất" thi tra ve
        thu tu goc cua API (da luu o ket_qua_goc)."""
        if self.che_do_var.get() != "de_xuat":
            return
        try:
            if self.sap_xep_var.get() == "Mới nhất":
                self.ket_qua.sort(key=lambda v: (v.get("pubdate") or 0),
                                  reverse=True)
            elif getattr(self, "ket_qua_goc", None):
                self.ket_qua = list(self.ket_qua_goc)
        except Exception:
            pass

    def _doi_sap_xep(self):
        """Doi lua chon sap xep: che do tu khoa -> tim lai ngay voi
        order moi (cung tu khoa + trang hien tai); che do de xuat
        -> sap xep lai danh sach hien co theo pubdate (khong goi
        lai API)."""
        if self.che_do_var.get() == "de_xuat":
            self._ap_dung_sap_xep_hien_tai()
            self._hien_ket_qua()
            return
        if self.tu_khoa_hien_tai:
            self._tim_trang(self.trang_hien_tai)

    def _day_sang_tab_tai(self, video):
        """(v7.21) Dien link video vao o link 1-mach cua tab Quan ly
        roi chuyen ngay sang tab Quan ly de CYAN bam tai tiep. CHI
        dien link + chuyen tab, KHONG tu chay tai. Duong tai cu
        (TẢI CÁC PHẦN ĐÃ CHỌN, mo cua so job theo tung phan) van
        giu nguyen."""
        link = (video or {}).get("link") or ""
        if not link:
            return
        try:
            self.quan_ly.link_1mach_var.set(link)
            self.quan_ly.notebook.select(self.quan_ly.tab_quan_ly)
        except Exception:
            pass

    # ---------- (v7.21) video yeu thich ----------
    def _cap_nhat_nut_yeu_thich(self, bvid):
        """Cap nhat nut ☆/★ + chu 'YÊU THÍCH' tren the theo dict
        yeu thich hien tai (tim lai/tim moi van giu dau)."""
        info = self._hang_ket_qua.get(bvid or "")
        if not info:
            return
        danh_dau = (bvid or "") in self._yeu_thich
        try:
            info["btn_yeu_thich"].config(
                text="★" if danh_dau else "☆",
                fg="red" if danh_dau else "black")
            info["yeu_thich"].config(
                text="★ YÊU THÍCH" if danh_dau else "")
        except Exception:
            pass

    def _doi_yeu_thich(self, video):
        """Bam ☆/★: bat/tat yeu thich cho video (theo bvid), luu
        ngay vao video-yeu-thich.json (ghi atomic). Dang loc
        chi-yeu-thich ma bo dau thi the bien khoi danh sach."""
        bvid = (video or {}).get("bvid") or ""
        if not bvid:
            return
        if bvid in self._yeu_thich:
            del self._yeu_thich[bvid]
            da_xoa = True
        else:
            self._yeu_thich[bvid] = {
                "bvid": bvid,
                "title": video.get("title") or "",
                "author": video.get("author") or "",
                "link": video.get("link") or "",
                "pic": video.get("pic") or "",
                "duration": video.get("duration") or "",
                "play": video.get("play") or 0,
                "pubdate": video.get("pubdate") or 0,
                "ngay_danh_dau": time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.localtime()),
            }
            da_xoa = False
        luu_video_yeu_thich(self._yeu_thich)
        self._cap_nhat_nut_yeu_thich(bvid)
        self._cap_nhat_nut_yeu_thich_chi_tiet()
        if self.chi_yeu_thich_var.get() and da_xoa:
            self._hien_ket_qua()  # bo dau -> bien khoi danh sach loc

    def _doi_yeu_thich_chi_tiet(self):
        """Nut yeu thich o khung chi tiet: doi dau cho video dang
        xem (cung ham voi nut tren the)."""
        if self.video_da_chon:
            self._doi_yeu_thich(self.video_da_chon)

    def _cap_nhat_nut_yeu_thich_chi_tiet(self):
        """Cap nhat nut yeu thich o khung chi tiet theo video dang
        xem (khong co video / chua ve xong thi bo qua)."""
        try:
            btn = getattr(self, "btn_yeu_thich_chi_tiet", None)
            if btn is None:
                return
            bvid = (self.video_da_chon or {}).get("bvid") or ""
            danh_dau = bool(bvid) and bvid in self._yeu_thich
            btn.config(text="★ Đã thích" if danh_dau else "☆ Yêu thích",
                       fg="red" if danh_dau else "black")
        except Exception:
            pass

    def _lay_danh_sach_hien_thi(self):
        """Danh sach de hien: loc chi-yeu-thich BAT thi chi cac video
        da luu (tu file JSON, khong phu thuoc tu khoa); sap theo
        ngay danh dau moi nhat, hoac theo pubdate khi chon 'Mới
        nhất'. Tat thi tra ve ket qua tim kiem/de xuat binh thuong."""
        if not self.chi_yeu_thich_var.get():
            return list(self.ket_qua)
        ds = [dict(m) for m in self._yeu_thich.values()]
        try:
            if self.sap_xep_var.get() == "Mới nhất":
                ds.sort(key=lambda v: (v.get("pubdate") or 0), reverse=True)
            else:
                ds.sort(key=lambda v: v.get("ngay_danh_dau") or "",
                        reverse=True)
        except Exception:
            pass
        return ds

    def _doi_loc_yeu_thich(self):
        """Bat/tat loc chi-yeu-thich: bat thi chi hien video da luu;
        tat thi ve lai ket qua tim kiem/de xuat binh thuong (van
        giu dau ★)."""
        self._hien_ket_qua()
        if self.chi_yeu_thich_var.get():
            self._dat_trang_thai(
                "Đang hiện %d video yêu thích — tắt 'Chỉ hiện video "
                "yêu thích' để về lại kết quả tìm kiếm."
                % len(self._yeu_thich))
        else:
            self._dat_trang_thai(
                "Đã tắt lọc yêu thích — hiện kết quả tìm kiếm/đề xuất "
                "(%d video)." % len(self.ket_qua))

    # ---------- de xuat trang chu (giai doan 2) ----------

    def _doi_che_do(self):
        """Doi che do Tim tu khoa / De xuat trang chu: xoa sach ket
        qua + chi tiet cu (khong lan ket qua cu), doi nhan nut Tim,
        bat/tat o tu khoa va phan trang. Ket qua cu ve tre bi bo qua
        nho tang _ma_tim (worker cu goi _tim_xong/_de_xuat_xong voi
        ma cu se bi chan)."""
        che_do = self.che_do_var.get()
        self._ma_tim += 1
        self.ket_qua = []
        self.ket_qua_goc = []  # (v7.21) doi che do thi quen thu tu goc
        self.tu_khoa_hien_tai = ""
        self.trang_hien_tai = 1
        self.video_da_chon = None
        self.chi_tiet = None
        self.lien_quan = []
        self.phu_de_hien_tai = None
        self._phan_vars = {}
        self._hang_phan = {}
        self._hien_ket_qua()
        for w in list(self.khung_chi_tiet.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        try:
            self.trang_var.set("Trang 1")
        except Exception:
            pass
        if che_do == "de_xuat":
            try:
                self.ent_tu_khoa.config(state="disabled")
                self.btn_tim.config(text="Tải đề xuất", state="normal")
                self.btn_truoc.config(state="disabled")
                self.btn_sau.config(state="disabled")
                self.lbl_tieu_de_trai.config(text="Đề xuất trang chủ")
            except Exception:
                pass
            self._dat_trang_thai(
                "Chế độ Đề xuất trang chủ — bấm 'Tải đề xuất' để xem "
                "video Bilibili gợi ý (đề xuất đúng gu cần cookies.txt "
                "đã đăng nhập).")
        else:
            try:
                self.ent_tu_khoa.config(state="normal")
                self.btn_tim.config(text="Tìm", state="normal")
                self.btn_truoc.config(state="normal")
                self.btn_sau.config(state="normal")
                self.lbl_tieu_de_trai.config(text="Kết quả tìm kiếm")
            except Exception:
                pass
            self._dat_trang_thai(
                "Gõ từ khóa rồi bấm Tìm — vd: hệ thống, tu tiên, "
                "mạt thế sinh tồn.")

    def _tai_de_xuat(self):
        self._ma_tim += 1
        ma = self._ma_tim
        self._kiem_tra_cookie_nen()  # (v7.21) cookie chet -> canh bao do
        self._dat_trang_thai("Đang tải đề xuất trang chủ...")
        self.btn_tim.config(state="disabled")
        self.btn_truoc.config(state="disabled")
        self.btn_sau.config(state="disabled")
        threading.Thread(target=self._de_xuat_worker, args=(ma,),
                         daemon=True).start()

    def _de_xuat_worker(self, ma):
        try:
            ket_qua = lay_de_xuat_trang_chu(
                cookies=self._lay_cookies(), log=self._ghi_log)
            self._after_an_toan(0, self._de_xuat_xong, ma, ket_qua)
        except Exception as e:
            self._after_an_toan(0, self._de_xuat_loi, ma, str(e))

    def _de_xuat_xong(self, ma, ket_qua):
        if ma != self._ma_tim or not self.con_song():
            return
        self.ket_qua = ket_qua or []
        # (v7.21) Luu thu tu goc cua API + ap sap xep hien tai
        # ("Mới nhất" thi sap client theo pubdate).
        self.ket_qua_goc = list(self.ket_qua)
        self._ap_dung_sap_xep_hien_tai()
        self._hien_ket_qua()
        try:
            self.trang_var.set("")
        except Exception:
            pass
        self.btn_tim.config(state="normal")
        self.btn_truoc.config(state="disabled")
        self.btn_sau.config(state="disabled")
        if not self.ket_qua:
            self._dat_trang_thai(
                "Không có video đề xuất nào — thử lại sau.")
        else:
            self._dat_trang_thai(
                "Đã tải %d video đề xuất trang chủ — bấm 1 video để "
                "xem các phần." % len(self.ket_qua))

    def _de_xuat_loi(self, ma, msg):
        if ma != self._ma_tim or not self.con_song():
            return
        self._co_the_cookie_chet(msg)  # (v7.21) -101 -> canh bao do
        self.btn_tim.config(state="normal")
        self.btn_truoc.config(state="disabled")
        self.btn_sau.config(state="disabled")
        self._dat_trang_thai("Đề xuất lỗi: " + msg)
        self._ghi_log("Đề xuất trang chủ LỖI: " + msg)
        messagebox.showerror("Đề xuất trang chủ lỗi", msg)

    # ---------- danh sach ket qua ----------

    def _hien_ket_qua(self):
        for w in list(self.khung_ket_qua.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        self._hang_ket_qua = {}
        self._hang_dang_chon = None
        self._anh_bia = {}
        # (v7.21) The doc: bytes anh goc theo bvid (de fit lai khi cot
        # doi rong) + chieu rong anh dang dung + id lich fit (debounce).
        self._anh_bia_bytes = {}
        self._rong_anh_bia_hien_tai = 0
        self._fit_anh_id = None
        # (v7.21) Tieu de cot trai doi theo loc: loc yeu thich thi
        # hien so video yeu thich dang hien.
        try:
            if self.chi_yeu_thich_var.get():
                self.lbl_tieu_de_trai.config(
                    text="Video yêu thích (%d)" % len(self._yeu_thich))
            else:
                self.lbl_tieu_de_trai.config(text="Kết quả tìm kiếm")
        except Exception:
            pass
        for video in self._lay_danh_sach_hien_thi():
            self._them_hang_ket_qua(video)

    def _bind_click_hang(self, widget, video):
        try:
            widget.bind("<Button-1>",
                        lambda e, v=video: self._mo_chi_tiet(v))
        except Exception:
            pass

    def _them_hang_ket_qua(self, video):
        # (v7.21) THE DOC: anh bia 16:9 nam TREN CUNG, phu full chieu
        # rong cot ket qua; tieu de/meta/link nam DUOI anh. Re chuot
        # vao tieu de/link thi tooltip hien DAY DU (tieu de hien thi
        # van cat ngan "..."); bam phai vao tieu de/link thi menu sao
        # chep link / ten phim; bam trai van mo chi tiet nhu cu.
        bvid = video.get("bvid") or ""
        hang = tk.Frame(self.khung_ket_qua, relief="groove", bd=1)
        hang.pack(fill="x", padx=2, pady=2)
        rong_cho = self._rong_anh_bia_muc_tieu()
        cao_cho = max(90, rong_cho * 9 // 16)
        anh_cho = tk.PhotoImage(width=rong_cho, height=cao_cho)
        lbl_anh = tk.Label(hang, image=anh_cho, text="Ảnh bìa",
                           compound="center", bg="#dddddd")
        lbl_anh.image = anh_cho  # giu tham chieu khoi bi GC
        lbl_anh.pack(fill="x", padx=4, pady=(4, 2))
        self._rong_anh_bia_hien_tai = rong_cho
        khung_chu = tk.Frame(hang)
        khung_chu.pack(fill="x", padx=4, pady=(0, 4))
        hang_tieu_de = tk.Frame(khung_chu)
        hang_tieu_de.pack(fill="x")
        lbl_tieu_de = tk.Label(
            hang_tieu_de,
            text=rut_gon_chu(video.get("title") or "Video", 55),
            font=("", 10, "bold"), anchor="w")
        lbl_tieu_de.pack(side="left")
        # (v7.9) Icon phu de nam SAU ten phim: "…" = chua kiem tra;
        # chi kiem tra khi bam vao video (mo chi tiet), khong quet ca luoi.
        lbl_phu_de = tk.Label(hang_tieu_de, text="…", fg="gray")
        lbl_phu_de.pack(side="left", padx=6)
        # (v7.21) Dau yeu thich: "★ YÊU THÍCH" (do, dam) khi video
        # da duoc danh dau; rong khi chua danh dau.
        lbl_yeu_thich = tk.Label(hang_tieu_de, text="", fg="red",
                                 font=("", 10, "bold"))
        lbl_yeu_thich.pack(side="left", padx=6)
        meta = "%s | %s | %s lượt xem" % (
            video.get("author") or "?",
            video.get("duration") or "?",
            self._dinh_dang_luot_xem(video.get("play")))
        if lay_job_da_tai(bvid) is not None:
            meta += " • ĐÃ TẢI"
        lbl_meta = tk.Label(khung_chu, text=meta, fg="gray", anchor="w")
        lbl_meta.pack(fill="x")
        lbl_link = tk.Label(khung_chu, text=video.get("link") or "",
                            fg="#5555aa", anchor="w")
        lbl_link.pack(fill="x")
        # (v7.21) Hang nut hanh dong cua the: day link sang tab tai
        # (dien o link 1-mach + chuyen tab Quan ly, khong tu chay
        # tai). Nut la Button rieng nen bam no KHONG mo chi tiet.
        hang_nut = tk.Frame(khung_chu)
        hang_nut.pack(fill="x", pady=(2, 0))
        tk.Button(hang_nut, text="Đẩy sang tab tải",
                  command=lambda v=video: self._day_sang_tab_tai(v)).pack(
                      side="left")
        # (v7.21) Nut yeu thich ☆/★: bam de bat/tat (theo bvid), luu
        # ngay vao video-yeu-thich.json. La Button rieng nen bam no
        # KHONG mo chi tiet (khong lan click ra the).
        btn_yeu_thich = tk.Button(
            hang_nut, text="☆",
            command=lambda v=video: self._doi_yeu_thich(v))
        btn_yeu_thich.pack(side="left", padx=4)
        # (v7.21) Tooltip day du + menu chuot phai sao chep.
        ToolTip(lbl_tieu_de, video.get("title") or "")
        ToolTip(lbl_link, video.get("link") or "")
        for w in (lbl_tieu_de, lbl_link):
            w.bind("<Button-3>",
                   lambda e, v=video: self._menu_chuot_phai_ket_qua(e, v))
        self._hang_ket_qua[bvid] = {
            "hang": hang, "anh": lbl_anh, "tieu_de": lbl_tieu_de,
            "phu_de": lbl_phu_de, "meta": lbl_meta, "link": lbl_link,
            "nut": hang_nut, "yeu_thich": lbl_yeu_thich,
            "btn_yeu_thich": btn_yeu_thich, "video": video,
            "cac_widget": [hang, lbl_anh, khung_chu, hang_tieu_de,
                           lbl_tieu_de, lbl_phu_de, lbl_meta, lbl_link,
                           hang_nut],
        }
        for w in (hang, lbl_anh, khung_chu, hang_tieu_de, lbl_tieu_de,
                  lbl_phu_de, lbl_meta, lbl_link, hang_nut):
            self._bind_click_hang(w, video)
        # (v7.21) The vua tao: hien dau ★ ngay neu video da duoc
        # danh dau tu truoc (tim lai/tim moi van giu dau).
        self._cap_nhat_nut_yeu_thich(bvid)
        if self.tu_tai_anh_bia_var.get() and video.get("pic"):
            threading.Thread(target=self._tai_anh_bia_worker,
                             args=(bvid, video.get("pic"), lbl_anh),
                             daemon=True).start()

    def _menu_chuot_phai_ket_qua(self, event, video):
        """(v7.21) Menu chuot phai tren tieu de/link: sao chep link /
        ten phim DAY DU (khong phai ban cat ngan hien thi)."""
        try:
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label="Sao chép link",
                command=lambda v=video: self._sao_chep_ket_qua(v, "link"))
            menu.add_command(
                label="Sao chép tên phim",
                command=lambda v=video: self._sao_chep_ket_qua(v, "ten"))
            self._menu_chuot_phai = menu  # giu tham chieu (test + GC)
            menu.tk_popup(event.x_root, event.y_root)
        except Exception:
            pass
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    def _sao_chep_ket_qua(self, video, loai):
        """(v7.21) Copy link / ten phim DAY DU vao clipboard + bao
        trang thai. Tra ve True neu copy duoc."""
        text = ((video or {}).get("link") or ""
                if loai == "link"
                else (video or {}).get("title") or "")
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._dat_trang_thai("Đã sao chép %s."
                                 % ("link" if loai == "link"
                                    else "tên phim"))
            return True
        except Exception:
            return False

    def _tai_anh_bia_worker(self, bvid, pic, lbl_anh):
        du_lieu = tai_anh_bia_bytes(pic, self._ghi_log)
        if not du_lieu:
            return
        self._after_an_toan(0, self._gan_anh_bia, bvid, lbl_anh, du_lieu)

    def _rong_anh_bia_muc_tieu(self):
        """(v7.21) Chieu rong muc tieu cho anh bia: full chieu rong
        cot ket qua (tru padding), toi da 640, toi thieu 160. Chua
        do duoc (moi tao the, chua layout) thi mac dinh 480."""
        try:
            rong = self.khung_ket_qua.winfo_width() - 16
        except Exception:
            rong = 0
        if rong < 160:
            rong = 480
        return max(160, min(640, int(rong)))

    def _gan_anh_bia(self, bvid, lbl_anh, du_lieu):
        # (v7.21) Anh bia full chieu rong cot (16:9), toi da 640px.
        # Luu bytes goc de fit lai khi cot doi rong.
        if not self.con_song():
            return
        if bvid not in self._hang_ket_qua:
            return  # ket qua da doi (tim moi) -> bo anh cu
        self._anh_bia_bytes[bvid] = du_lieu
        rong = self._rong_anh_bia_muc_tieu()
        cao = max(90, rong * 9 // 16)
        photo = anh_bia_bytes_sang_photoimage(du_lieu, rong, cao,
                                              self._ghi_log)
        if photo is None:
            return
        try:
            lbl_anh.config(image=photo, text="")
            lbl_anh.image = photo
            self._anh_bia[bvid] = photo
            self._rong_anh_bia_hien_tai = rong
        except Exception:
            pass

    def _len_lich_fit_anh_bia(self, _event=None):
        """(v7.21) Cot ket qua doi kich thuoc -> len lich fit lai anh
        sau 150ms (debounce, tranh fit lien tuc khi keo cua so)."""
        try:
            if self._fit_anh_id:
                self.after_cancel(self._fit_anh_id)
        except Exception:
            pass
        try:
            self._fit_anh_id = self.after(150, self._fit_lai_anh_bia)
        except Exception:
            self._fit_anh_id = None

    def _fit_lai_anh_bia(self):
        """(v7.21) Fit lai tat ca anh bia theo chieu rong cot hien
        tai. Chi chay khi rong doi >= 10px (doi cao don thuan thi
        khong fit lai). The chua co anh (placeholder) cung duoc fit
        lai ve dung kich thuoc pixel (16:9) de khong nhay layout
        khi anh ve, va de tat checkbox 'Tu tai anh bia' van thay
        placeholder dung kich thuoc."""
        self._fit_anh_id = None
        if not self.con_song():
            return
        try:
            rong = self._rong_anh_bia_muc_tieu()
        except Exception:
            return
        if abs(rong - self._rong_anh_bia_hien_tai) < 10:
            return
        cao = max(90, rong * 9 // 16)
        for bvid, info in list(self._hang_ket_qua.items()):
            du_lieu = self._anh_bia_bytes.get(bvid)
            lbl_anh = info.get("anh")
            if lbl_anh is None:
                continue
            if du_lieu:
                self._gan_anh_bia(bvid, lbl_anh, du_lieu)
            else:
                # Placeholder: giu dung kich thuoc pixel (16:9).
                try:
                    anh_cho = tk.PhotoImage(width=rong, height=cao)
                    lbl_anh.config(image=anh_cho, text="Ảnh bìa")
                    lbl_anh.image = anh_cho
                except Exception:
                    pass
        self._rong_anh_bia_hien_tai = rong

    # ---------- chi tiet video ----------

    def _danh_dau_hang_dang_chon(self, bvid):
        cu = self._hang_dang_chon
        if cu and cu in self._hang_ket_qua:
            for w in self._hang_ket_qua[cu].get("cac_widget", []):
                try:
                    w.config(bg="")
                except Exception:
                    pass
        self._hang_dang_chon = bvid
        hang_moi = self._hang_ket_qua.get(bvid)
        if hang_moi:
            for w in hang_moi.get("cac_widget", []):
                try:
                    w.config(bg="#e8f0fe")
                except Exception:
                    pass

    def _mo_chi_tiet(self, video):
        bvid = (video or {}).get("bvid") or ""
        if not bvid:
            return
        self._kiem_tra_cookie_nen()  # (v7.21) cookie chet -> canh bao do
        self._danh_dau_hang_dang_chon(bvid)
        self.video_da_chon = video
        self.chi_tiet = None
        self.lien_quan = []
        self.phu_de_hien_tai = None
        self._phan_vars = {}
        self._hang_phan = {}
        for w in list(self.khung_chi_tiet.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        tk.Label(self.khung_chi_tiet,
                 text="Đang tải chi tiết: %s ..."
                 % (video.get("title") or bvid),
                 fg="gray", wraplength=420, justify="left").pack(
                     anchor="w", padx=4, pady=4)
        self._ma_chi_tiet += 1
        ma = self._ma_chi_tiet
        threading.Thread(target=self._chi_tiet_worker,
                         args=(ma, video), daemon=True).start()

    def _chi_tiet_worker(self, ma, video):
        bvid = video.get("bvid") or ""
        cookies = self._lay_cookies()
        try:
            chi_tiet = lay_chi_tiet_video(bvid, cookies, log=self._ghi_log)
        except Exception as e:
            self._after_an_toan(0, self._chi_tiet_loi, ma, video, str(e))
            return
        try:
            lien_quan = lay_video_lien_quan(bvid, cookies, log=self._ghi_log)
        except Exception:
            lien_quan = []
        # (v7.9) Chi kiem tra phu de KHI bam vao video (khong quet ca
        # luoi): dung kiem_tra_phu_de san co (yt-dlp --list-subs).
        try:
            phu_de = kiem_tra_phu_de(video.get("link") or "", cookies)
        except Exception:
            phu_de = {"has_subtitle": False, "languages": []}
        self._after_an_toan(0, self._mo_chi_tiet_xong, ma, video,
                            chi_tiet, lien_quan, phu_de)

    def _chi_tiet_loi(self, ma, video, msg):
        if ma != self._ma_chi_tiet or not self.con_song():
            return
        self._co_the_cookie_chet(msg)  # (v7.21) -101 -> canh bao do
        for w in list(self.khung_chi_tiet.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        tk.Label(self.khung_chi_tiet,
                 text="Không đọc được chi tiết video: " + msg,
                 fg="red", wraplength=420, justify="left").pack(
                     anchor="w", padx=4, pady=4)
        self._ghi_log("Chi tiết video LỖI: " + msg)

    def _mo_chi_tiet_xong(self, ma, video, chi_tiet, lien_quan, phu_de):
        if ma != self._ma_chi_tiet or not self.con_song():
            return
        self.video_da_chon = video
        self.chi_tiet = chi_tiet
        self.lien_quan = lien_quan or []
        self.phu_de_hien_tai = phu_de or {}
        video["has_subtitle"] = bool((phu_de or {}).get("has_subtitle"))
        video["subtitle_langs"] = list((phu_de or {}).get("languages") or [])
        # Cap nhat icon phu de SAU ten phim o hang ket qua.
        hang = self._hang_ket_qua.get(video.get("bvid") or "")
        if hang:
            try:
                if video["has_subtitle"]:
                    hang["phu_de"].config(text="✓ Có phụ đề", fg="green")
                else:
                    hang["phu_de"].config(text="✗ Không có phụ đề",
                                          fg="gray")
            except Exception:
                pass
        self._ve_chi_tiet()
        self._ghi_log("Đã mở chi tiết: %s (%d phần)"
                      % (chi_tiet.get("title") or "",
                         len(chi_tiet.get("pages") or [])))

    def _ve_chi_tiet(self):
        for w in list(self.khung_chi_tiet.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        ct = self.chi_tiet or {}
        video = self.video_da_chon or {}
        bvid = ct.get("bvid") or video.get("bvid") or ""
        tk.Label(self.khung_chi_tiet, text=ct.get("title") or "",
                 font=("", 11, "bold"), wraplength=420, justify="left",
                 anchor="w").pack(fill="x", padx=4, pady=2)
        tk.Label(self.khung_chi_tiet,
                 text="Tác giả: %s | Tổng: %s | %s"
                 % (ct.get("author") or "?",
                    dinh_dang_thoi_luong(ct.get("duration") or 0), bvid),
                 fg="gray", wraplength=420, justify="left",
                 anchor="w").pack(fill="x", padx=4)
        # Phu de (da kiem tra khi bam vao video).
        phu_de = self.phu_de_hien_tai or {}
        if phu_de.get("has_subtitle"):
            nhan_pd = "Phụ đề: ✓ Có (%s)" % ", ".join(
                phu_de.get("languages") or [])
        else:
            nhan_pd = "Phụ đề: ✗ Không có phụ đề"
        hang_pd = tk.Frame(self.khung_chi_tiet)
        hang_pd.pack(fill="x", padx=4, pady=2)
        self.lbl_phu_de_chi_tiet = tk.Label(hang_pd, text=nhan_pd, anchor="w")
        self.lbl_phu_de_chi_tiet.pack(side="left")
        tk.Button(hang_pd, text="Kiểm tra lại phụ đề",
                  command=self._kiem_tra_lai_phu_de).pack(side="left", padx=6)
        # (v7.21) Nut yeu thich o khung chi tiet (cung ham voi nut
        # ☆/★ tren the): bam de bat/tat, luu vao video-yeu-thich.json.
        self.btn_yeu_thich_chi_tiet = tk.Button(
            hang_pd, text="☆ Yêu thích",
            command=self._doi_yeu_thich_chi_tiet)
        self.btn_yeu_thich_chi_tiet.pack(side="left", padx=6)
        # Cac phan.
        pages = ct.get("pages") or []
        hang_tieu_de_phan = tk.Frame(self.khung_chi_tiet)
        hang_tieu_de_phan.pack(fill="x", padx=4, pady=4)
        tk.Label(hang_tieu_de_phan,
                 text="Các phần (%d):" % len(pages),
                 font=("", 10, "bold")).pack(side="left")
        tk.Button(hang_tieu_de_phan, text="Chọn tất cả",
                  command=self._chon_tat_ca_phan).pack(side="left", padx=4)
        tk.Button(hang_tieu_de_phan, text="Bỏ chọn hết",
                  command=self._bo_chon_tat_ca_phan).pack(side="left", padx=4)
        self.btn_tai_phan = tk.Button(
            self.khung_chi_tiet, text="TẢI CÁC PHẦN ĐÃ CHỌN",
            font=("", 11, "bold"), command=self._tai_cac_phan_da_chon)
        self.btn_tai_phan.pack(fill="x", padx=4, pady=2)
        # (v7.21) Day link sang tab tai: dien o link 1-mach cua tab
        # Quan ly + chuyen tab (khong tu chay tai). Duong tai cu
        # (TẢI CÁC PHẦN ĐÃ CHỌN) van giu nguyen.
        self.btn_day_sang_tab_tai = tk.Button(
            self.khung_chi_tiet, text="Đẩy sang tab tải",
            command=lambda: self._day_sang_tab_tai(self.video_da_chon))
        self.btn_day_sang_tab_tai.pack(fill="x", padx=4, pady=2)
        for phan in pages:
            self._them_hang_phan(bvid, phan)
        # Video lien quan (cot phai nhu Bilibili).
        tk.Label(self.khung_chi_tiet, text="Video liên quan:",
                 font=("", 10, "bold"), anchor="w").pack(
                     fill="x", padx=4, pady=(8, 2))
        if not self.lien_quan:
            tk.Label(self.khung_chi_tiet,
                     text="(Không tải được danh sách liên quan.)",
                     fg="gray", anchor="w").pack(fill="x", padx=4)
        for v in self.lien_quan:
            self._them_hang_lien_quan(v)
        # (v7.21) Nut yeu thich o chi tiet: hien ★ ngay neu video
        # dang xem da duoc danh dau tu truoc.
        self._cap_nhat_nut_yeu_thich_chi_tiet()

    def _them_hang_phan(self, bvid, phan):
        so = phan.get("page") or 1
        hang = tk.Frame(self.khung_chi_tiet, relief="groove", bd=1)
        hang.pack(fill="x", padx=4, pady=2)
        var = tk.BooleanVar(value=False)
        self._phan_vars[so] = var
        tk.Checkbutton(hang, variable=var).pack(side="left")
        tk.Label(hang, text="P%d · %s (%s)" % (
            so, rut_gon_chu(phan.get("part") or "", 40),
            dinh_dang_thoi_luong(phan.get("duration") or 0)),
            anchor="w").pack(side="left", fill="x", expand=True)
        da_tai = lay_job_da_tai(bvid, so) is not None
        lbl_tai = tk.Label(hang, text="Đã tải" if da_tai else "",
                           fg="green", anchor="w")
        lbl_tai.pack(side="left", padx=4)
        lbl_tt = tk.Label(hang, text="", fg="gray", anchor="w")
        lbl_tt.pack(side="left", padx=4)
        btn = tk.Button(hang, text="Kiểm tra",
                        command=lambda s=so: self._kiem_tra_phan(s))
        btn.pack(side="right", padx=4)
        self._hang_phan[so] = {"hang": hang, "tai": lbl_tai,
                               "trang_thai": lbl_tt, "nut": btn,
                               "phan": phan}

    def _them_hang_lien_quan(self, video):
        hang = tk.Frame(self.khung_chi_tiet, relief="groove", bd=1)
        hang.pack(fill="x", padx=4, pady=2)
        tk.Label(hang, text=rut_gon_chu(video.get("title") or "", 50),
                 font=("", 10), anchor="w").pack(fill="x", padx=2)
        tk.Label(hang, text="%s | %s | %s lượt xem" % (
            video.get("author") or "?",
            video.get("duration") or "?",
            self._dinh_dang_luot_xem(video.get("play"))),
            fg="gray", anchor="w").pack(fill="x", padx=2)
        self._bind_click_hang(hang, video)
        for w in hang.winfo_children():
            self._bind_click_hang(w, video)

    # ---------- kiem tra tung link phan ----------

    def _kiem_tra_phan(self, so):
        hang = self._hang_phan.get(so)
        if not hang:
            return
        phan = hang.get("phan") or {}
        link = phan.get("link") or ""
        if not link:
            return
        try:
            hang["nut"].config(state="disabled")
            hang["trang_thai"].config(text="Đang kiểm tra...")
        except Exception:
            pass
        threading.Thread(target=self._kiem_tra_phan_worker,
                         args=(so, link), daemon=True).start()

    def _kiem_tra_phan_worker(self, so, link):
        try:
            info = kiem_tra_link(link, self._lay_cookies())
            nhan = "%s | %s" % (
                dinh_dang_thoi_luong(info.get("duration")),
                ", ".join(o.get("label") or ""
                          for o in info.get("options") or []))
            self._after_an_toan(0, self._kiem_tra_phan_xong, so, nhan)
        except Exception as e:
            self._after_an_toan(0, self._kiem_tra_phan_xong, so,
                                "Lỗi: " + str(e))

    def _kiem_tra_phan_xong(self, so, nhan):
        hang = self._hang_phan.get(so)
        if not hang or not self.con_song():
            return
        try:
            hang["trang_thai"].config(text=nhan)
            hang["nut"].config(state="normal")
        except Exception:
            pass

    def _kiem_tra_lai_phu_de(self):
        video = self.video_da_chon or {}
        if not video.get("bvid"):
            return
        try:
            self.lbl_phu_de_chi_tiet.config(text="Phụ đề: đang kiểm tra...")
        except Exception:
            pass
        threading.Thread(target=self._kiem_tra_lai_phu_de_worker,
                         args=(video,), daemon=True).start()

    def _kiem_tra_lai_phu_de_worker(self, video):
        try:
            pd = kiem_tra_phu_de(video.get("link") or "", self._lay_cookies())
        except Exception:
            pd = {"has_subtitle": False, "languages": []}
        self._after_an_toan(0, self._kiem_tra_lai_phu_de_xong, video, pd)

    def _kiem_tra_lai_phu_de_xong(self, video, pd):
        if not self.con_song():
            return
        self.phu_de_hien_tai = pd or {}
        video["has_subtitle"] = bool((pd or {}).get("has_subtitle"))
        video["subtitle_langs"] = list((pd or {}).get("languages") or [])
        try:
            if video["has_subtitle"]:
                self.lbl_phu_de_chi_tiet.config(
                    text="Phụ đề: ✓ Có (%s)"
                    % ", ".join(video["subtitle_langs"]))
            else:
                self.lbl_phu_de_chi_tiet.config(
                    text="Phụ đề: ✗ Không có phụ đề")
        except Exception:
            pass
        hang = self._hang_ket_qua.get(video.get("bvid") or "")
        if hang:
            try:
                hang["phu_de"].config(
                    text=("✓ Có phụ đề" if video["has_subtitle"]
                          else "✗ Không có phụ đề"),
                    fg="green" if video["has_subtitle"] else "gray")
            except Exception:
                pass

    # ---------- chon phan + dua vao luong tai san co ----------

    def _chon_tat_ca_phan(self):
        for var in self._phan_vars.values():
            try:
                var.set(True)
            except Exception:
                pass

    def _bo_chon_tat_ca_phan(self):
        for var in self._phan_vars.values():
            try:
                var.set(False)
            except Exception:
                pass

    def _tai_cac_phan_da_chon(self):
        ct = self.chi_tiet or {}
        pages = ct.get("pages") or []
        chon = []
        for p in pages:
            so = p.get("page") or 1
            var = self._phan_vars.get(so)
            if var is not None:
                try:
                    if var.get():
                        chon.append(p)
                except Exception:
                    pass
        if not chon:
            messagebox.showinfo("Chưa chọn phần",
                                "Tick chọn ít nhất 1 phần cần tải trước đã.")
            return
        ten_phim = (ct.get("title")
                    or (self.video_da_chon or {}).get("title") or "")
        da_mo = 0
        for phan in chon:
            so = phan.get("page") or 1
            tieu_de = "%s - P%d %s" % (ten_phim, so, phan.get("part") or "")
            job = tao_job_tu_link_duyet(phan.get("link") or "",
                                        tieu_de[:100])
            try:
                self.quan_ly.cap_nhat_job(job)
                self.quan_ly.mo_cua_so_job(job)
                da_mo += 1
            except Exception as e:
                self._ghi_log("Mở cửa sổ tải lỗi (P%d): %s" % (so, e))
        self._ghi_log("Đã mở %d cửa sổ tải cho các phần đã chọn." % da_mo)
        self._dat_trang_thai("Đã mở %d cửa sổ tải — mỗi phần 1 cửa sổ "
                             "như dán link." % da_mo)
        # Cap nhat lai dau "Đã tải" o cac hang phan vua mo.
        for phan in chon:
            so = phan.get("page") or 1
            hang = self._hang_phan.get(so)
            if hang:
                try:
                    hang["tai"].config(text="Đã tải")
                except Exception:
                    pass


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
        # (v7.17) Hang nut chi con thao tac job: 4 nut chuyen tab
        # ("Xu ly phu de", "Doc phu de (HoaiMy)", "Voice Faceless",
        # "Gop am thanh") da XOA — chung chi la phim tat chuyen tab
        # nen trung ten voi tab Notebook, lam tab Duyet video bi chim
        # (CYAN bao). Muon sang tab nao thi bam thang tab do.
        tk.Button(hang_nut, text="Kiểm tra cập nhật", font=("", 11, "bold"),
                  command=self.bam_kiem_tra_cap_nhat).pack(side="right", padx=4)
        ttk.Separator(hang_nut, orient="vertical").pack(side="right", fill="y", padx=8)

        # ---- (v7.4) 1 cua so duy nhat: ttk.Notebook 6 tab (v7.17:
        # them Xu ly am thanh). Moi chuc nang chi co dung 1 tab,
        # khong nut to trung ten nua. Cac tab la Frame nhung trong
        # Notebook, khong con Toplevel mo rieng chong nhau.
        # (v7.17) Tab TO va ro hon: font 11 dam, padding rong — tat
        # ca tab deu nhau, de nhin, de bam.
        _style_tab = ttk.Style(self)
        _style_tab.configure("TNotebook.Tab", font=("", 11, "bold"),
                             padding=[14, 8])
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=4, pady=4)
        self.tab_quan_ly = tk.Frame(self.notebook)
        self.tab_xu_ly = tk.Frame(self.notebook)
        self.tab_doc = tk.Frame(self.notebook)
        self.tab_duyet = tk.Frame(self.notebook)
        self.tab_xu_ly_am_thanh = tk.Frame(self.notebook)
        self.tab_voice = tk.Frame(self.notebook)
        self.tab_postman = tk.Frame(self.notebook)
        self.tab_tao_nhan_vat = tk.Frame(self.notebook)
        self.notebook.add(self.tab_quan_ly, text="Quản lý")
        self.notebook.add(self.tab_xu_ly, text="Xử lý phụ đề")
        self.notebook.add(self.tab_doc, text="Đọc phụ đề (HoaiMy)")
        self.notebook.add(self.tab_duyet, text="Duyệt video")
        self.notebook.add(self.tab_xu_ly_am_thanh, text="Xử lý âm thanh")
        self.notebook.add(self.tab_voice, text="Voice for YouTube Faceless")
        self.notebook.add(self.tab_postman, text="Postman 2D")
        self.notebook.add(self.tab_tao_nhan_vat, text="Tạo nhân vật")
        self.panel_voice = CuaSoVoiceFaceless(self, parent=self.tab_voice)
        self.panel_voice.pack(fill="both", expand=True)
        self.panel_xu_ly = CuaSoXuLyPhuDe(self, parent=self.tab_xu_ly)
        self.panel_xu_ly.pack(fill="both", expand=True)
        self.panel_doc = CuaSoDocPhuDe(self, parent=self.tab_doc)
        self.panel_doc.pack(fill="both", expand=True)
        self.panel_duyet = CuaSoDuyetVideo(self, parent=self.tab_duyet)
        self.panel_duyet.pack(fill="both", expand=True)
        self.panel_xu_ly_am_thanh = CuaSoXuLyAmThanh(
            self, parent=self.tab_xu_ly_am_thanh)
        self.panel_xu_ly_am_thanh.pack(fill="both", expand=True)
        # (v7.24) Tab Postman 2D — import lười: thiếu postman2d.py
        # thì chỉ tab này không mở được, các tab cũ vẫn chạy.
        try:
            import postman2d as _pm2d
            self.panel_postman = _pm2d.tao_tab_postman(
                self.tab_postman, self)
            self.panel_postman.pack(fill="both", expand=True)
        except Exception as _e_pm:
            tk.Label(self.tab_postman,
                     text=("Tab Postman 2D chưa mở được: %s\n"
                           "Cần file postman2d.py cùng thư mục với "
                           "file .py/.exe này." % _e_pm),
                     wraplength=800, justify="left",
                     fg="red").pack(fill="x", padx=8, pady=8)
            self.panel_postman = None
        # (v7.24) Tab Tạo nhân vật — cùng module postman2d.py,
        # chung chỗ lưu nhan_vat_postman.json với tab Postman 2D.
        try:
            import postman2d as _pm2d2
            self.panel_tao_nhan_vat = _pm2d2.tao_tab_tao_nhan_vat(
                self.tab_tao_nhan_vat, self)
            self.panel_tao_nhan_vat.pack(fill="both", expand=True)
        except Exception as _e_nv:
            tk.Label(self.tab_tao_nhan_vat,
                     text=("Tab Tạo nhân vật chưa mở được: %s\n"
                           "Cần file postman2d.py cùng thư mục với "
                           "file .py/.exe này." % _e_nv),
                     wraplength=800, justify="left",
                     fg="red").pack(fill="x", padx=8, pady=8)
            self.panel_tao_nhan_vat = None
        # (v7.17) Chuyen tab thi dien lai file mac dinh cho tab Xu ly
        # am thanh (file audio du an + file voice HoaiMy vua xuat,
        # neu co).
        self.notebook.bind("<<NotebookTabChanged>>", self._khi_doi_tab)

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
        # (v7.8) TAT CA cot deu stretch=NO: cot "ten" truoc day la
        # cot duy nhat stretch=YES nen khi cua so rong (1920px) no
        # an het phan thua va rong toi ~1220px, day cac cot sau ra
        # ngoai man hinh. Cot co dinh width/minwidth, noi dung dai
        # van rut gon bang "…" (rut_gon_*), xem day du o label chi
        # tiet duoi bang. Luu y: o cua ttk.Treeview KHONG xuong dong
        # va KHONG cuon rieng trong o (gioi han cua Tk) — muon xem
        # day du thi dung label chi tiet, keo gian cot bang tay o
        # header, hoac thanh cuon ngang duoi bang.
        self.tree_du_an.column("ten", width=260, minwidth=180,
                               stretch=tk.NO, anchor="w")
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
        # (v7.21) Kiem tra cookie: chay o luong nen, ket qua hien
        # ngay canh nut (xanh = con song + ten tai khoan, do = het
        # han / khong co SESSDATA + huong dan xuat lai).
        tk.Button(self.tab_quan_ly, text="Kiểm tra cookie",
                  command=lambda: self.kiem_tra_cookie(
                      self.lbl_ket_qua_cookie)).grid(row=3, column=3, **pad)
        self.lbl_ket_qua_cookie = tk.Label(
            self.tab_quan_ly, text="", fg="gray", wraplength=300,
            justify="left", anchor="w")
        self.lbl_ket_qua_cookie.grid(row=3, column=4, sticky="w", **pad)
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
        # (v7.24, CYAN 21/11 ~21:30) BỎ HẲN tự mở lại cửa sổ cũ khi
        # khởi động: mở tool chỉ mở 1 cửa sổ chính duy nhất.
        # (Trước đây: vòng lặp doc_jobs() + mo_cua_so_job(job) cho
        # mọi job dang_tai_idm/cho_gop/dang_gop/da_kiem_tra — ĐÃ XÓA,
        # không thêm toggle.) Muốn mở lại job thì mở tay: nút
        # "+ Mở cửa sổ mới" / "Mở lại job đã chọn" / bấm đúp dòng
        # lịch sử / "TẢI CÁC PHẦN ĐÃ CHỌN".

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
        chi tiet + nut hanh dong. KHONG xay lai bang.
        (v7.8) Dong dang chon la job CU chua co thu muc phim ma file
        .srt dang nam thang o goc thu muc luu -> don ve thu muc phim
        tren luong nen (ten thu muc can dich Google Translate, toi
        da 10s — khong duoc dong giao dien), xong thi ve lai bang."""
        tree = getattr(self, "tree_du_an", None)
        if tree is None:
            return
        chon = tree.selection()
        if not chon:
            return
        self.job_da_chon_id = chon[0]
        self._hien_chi_tiet_du_an(self._lay_job_da_chon())
        self._cap_nhat_nut_hanh_dong()
        job = self._lay_job_da_chon()
        if job is not None and not job.get("folder") and (
                job.get("subtitle_file") or job.get("subtitle_vi_file")):
            # (v7.8) outdir cua CHINH job nay duoc uu tien (file .srt
            # dang nam o do); thu muc luu mac dinh trong config chi
            # la du phong. Doc tren luong chinh roi truyen vao
            # worker — khong doc StringVar tu luong nen.
            outdir_job = ((job.get("outdir") or "").strip()
                          or self.outdir_var.get().strip() or "")
            threading.Thread(target=self._don_job_cu_worker,
                             args=(job, outdir_job), daemon=True).start()

    def _don_job_cu_worker(self, job, outdir=""):
        """(v7.8) Luong nen don job cu (xem don_phu_de_ve_thu_muc_phim):
        xong thi bao ve luong chinh ve lai bang."""
        try:
            da_don = don_phu_de_ve_thu_muc_phim(
                job, outdir=outdir, log=self._ghi_log_1_mach)
        except Exception:
            da_don = False
        if da_don:
            try:
                self.after(0, self._don_job_cu_xong)
            except Exception:
                pass

    def _don_job_cu_xong(self):
        """(v7.8) Don job cu xong: ve lai bang de hien thu muc moi
        thay cho "(chưa có thư mục)" (_xay_bang_du_an tu khoi phuc
        dong dang chon + vi tri cuon)."""
        try:
            self.cap_nhat_bang()
        except Exception:
            pass

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

    def _khi_doi_tab(self, event=None):
        """(v7.17) Chuyen sang tab Xu ly am thanh thi dien lai file
        mac dinh (file audio du an + file voice HoaiMy vua xuat o tab
        Doc phu de, neu co) — khong ghi de file cau da chon tay."""
        try:
            chon = self.notebook.select()
            if chon == str(self.tab_xu_ly_am_thanh):
                panel = getattr(self, "panel_xu_ly_am_thanh", None)
                if panel is not None:
                    panel._dien_mac_dinh()
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
            # (v7.10) 1 thu muc duy nhat cho 1 phim (xem
            # _thu_muc_phim_duy_nhat): dung lai thu muc da co, doi
            # ten thu muc ten goc sang ten Viet neu duoc. link.txt
            # luon duoc ghi vao thu muc tra ve (ca khi tai phu de
            # that bai / khong co phu de).
            folder, _da_tao = _thu_muc_phim_duy_nhat(
                outdir, ten_viet, info.get("title") or "video",
                job=job, url=url, log=log)
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

    def kiem_tra_cookie(self, lbl_ket_qua, khi_xong=None):
        """(v7.21) Bam 'Kiểm tra cookie': chay
        kiem_tra_cookie_bilibili o luong nen (UI khong dung),
        hien ket qua len lbl_ket_qua ngay canh nut: xanh = con
        song + ten tai khoan; do = het han / khong co SESSDATA /
        khong co file + huong dan xuat lai. khi_xong (neu co) duoc
        goi o luong chinh voi dict ket qua (tab Duyet video dung
        de hien/them canh bao cookie chet)."""
        try:
            lbl_ket_qua.configure(text="Đang kiểm tra...", fg="gray")
        except Exception:
            pass

        def _chay():
            kq = kiem_tra_cookie_bilibili(
                (self.cookies_var.get() or "").strip())

            def _hien():
                try:
                    tt = kq.get("trang_thai")
                    if tt == "song":
                        lbl_ket_qua.configure(
                            text="✓ Còn sống — %s" % (kq.get("ten") or "?"),
                            fg="green")
                    elif tt == "khong_file":
                        lbl_ket_qua.configure(
                            text="✗ Chưa có file cookies.txt — import file "
                                 "cookies.txt rồi bấm lại.",
                            fg="red")
                    elif tt == "khong_sessdata":
                        lbl_ket_qua.configure(
                            text="✗ File cookies không có SESSDATA — xuất "
                                 "lại từ Chrome (đăng nhập Bilibili trước).",
                            fg="red")
                    else:
                        lbl_ket_qua.configure(
                            text="✗ Cookie đã hết hạn — xuất lại "
                                 "cookies.txt từ Chrome (đăng nhập Bilibili "
                                 "trước) rồi import lại.%s"
                                 % ((" " + kq.get("chi_tiet"))
                                    if kq.get("chi_tiet") else ""),
                            fg="red")
                except Exception:
                    pass
                if khi_xong is not None:
                    try:
                        khi_xong(kq)
                    except Exception:
                        pass
            try:
                lbl_ket_qua.after(0, _hien)
            except Exception:
                pass

        threading.Thread(target=_chay, daemon=True).start()

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
        # (v7.8) Tam dung khi dong tool giua chung: neu tab HoaiMy dang
        # xuat thi hoi xac nhan, luu tien trinh ngay roi moi dong (mo
        # lai bam 'Tiep tuc' la chay tiep). Doi worker dung toi da ~5s;
        # qua gio thi cu dong vi tien trinh da luu roi (ghi an toan
        # bang _luu_tien_trinh nen khong so file ghi do).
        panel_doc = getattr(self, "panel_doc", None)
        if panel_doc is not None and getattr(panel_doc, "dang_chay", False):
            so_xong, tong = panel_doc._lay_tien_trinh_hien_tai()
            if tong > 0:
                cau_hoi = ("Đang xuất MP3 ở câu %d/%d. Đóng tool sẽ tạm "
                           "dừng tại đây, mở lại bấm 'Tiếp tục' để chạy "
                           "tiếp. Đóng không?" % (so_xong, tong))
            else:
                cau_hoi = ("Đang xuất MP3 (mới bắt đầu, chưa xong câu "
                           "nào). Đóng tool sẽ tạm dừng tại đây, mở lại "
                           "bấm 'Tiếp tục' để chạy tiếp. Đóng không?")
            if not messagebox.askyesno("Đang xuất MP3", cau_hoi):
                return
            panel_doc._yeu_cau_huy.set()
            panel_doc._yeu_cau_tam_dung.clear()
            panel_doc._luu_anh_chup_hien_tai()
            for _ in range(50):
                if not panel_doc.dang_chay:
                    break
                self.update()
                time.sleep(0.1)
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


# ======================================================================
# (v7.25) KHÓA SINGLE-INSTANCE — tool chỉ chạy 1 bản duy nhất.
# Lệnh CYAN 22/11 ~00:44: "tool chỉ chạy độc lập 1 lần. k cho
# chuyện bấm mở là mở thêm 1 bản khác". Cơ chế: Windows dùng mutex
# kernel32.CreateMutexW (tên "Chipchipdownload-SingleInstance");
# GetLastError()==183 (ERROR_ALREADY_EXISTS) nghĩa là đã có 1 bản
# đang chạy -> báo rồi thoát, KHÔNG tạo thêm cửa sổ. Handle mutex
# giữ suốt thời gian process sống (không đóng sớm). Không phải
# Windows: lock file trong thư mục tạm (best-effort, ghi PID vào
# file; file cũ mà PID đã chết thì coi như hết hạn và lấy lại).
# Nếu tự tạo khóa mà lỗi -> ghi log và CHO CHẠY TIẾP (không được
# crash lúc khởi động vì cái khóa này).
# ======================================================================
_TEN_MUTEX_DON_PHIEN_BAN = "Chipchipdownload-SingleInstance"
_KHOA_DON_PHIEN_BAN_HANDLE = None
_KHOA_DON_PHIEN_BAN_LOCKFILE = None


def _khoa_don_phien_ban(lock_path=None):
    """Thử giữ khóa single-instance. Trả True nếu giữ được (bản
    duy nhất), False nếu đã có 1 bản đang chạy. Lỗi khi tự tạo
    khóa -> trả True (cho chạy tiếp)."""
    global _KHOA_DON_PHIEN_BAN_HANDLE, _KHOA_DON_PHIEN_BAN_LOCKFILE
    try:
        if sys.platform.startswith("win"):
            import ctypes
            k32 = ctypes.windll.kernel32
            try:
                k32.CreateMutexW.restype = ctypes.c_void_p
                k32.CreateMutexW.argtypes = [ctypes.c_void_p,
                                             ctypes.c_bool,
                                             ctypes.c_wchar_p]
                k32.CloseHandle.restype = ctypes.c_bool
                k32.CloseHandle.argtypes = [ctypes.c_void_p]
            except Exception:
                pass
            h = k32.CreateMutexW(None, False,
                                 _TEN_MUTEX_DON_PHIEN_BAN)
            if not h:
                # Tạo mutex lỗi -> cho chạy tiếp.
                return True
            try:
                da_co = (ctypes.get_last_error() == 183)
            except Exception:
                da_co = False
            if da_co:
                try:
                    k32.CloseHandle(h)
                except Exception:
                    pass
                return False
            _KHOA_DON_PHIEN_BAN_HANDLE = h
            return True
        # Không phải Windows: lock file best-effort.
        import tempfile
        if lock_path is None:
            lock_path = os.path.join(
                tempfile.gettempdir(),
                "chipchipdownload-single-instance.lock")
        try:
            fd = os.open(lock_path,
                         os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            # File đã có: đọc PID cũ, nếu process đó đã chết thì
            # lấy lại khóa; còn sống thì đây là bản thứ 2.
            try:
                with open(lock_path, "r", encoding="utf-8",
                          errors="ignore") as f:
                    pid_cu = int(f.read().strip())
                os.kill(pid_cu, 0)
                return False  # process cũ vẫn sống
            except Exception:
                try:
                    os.remove(lock_path)
                except Exception:
                    return False
                try:
                    fd = os.open(lock_path,
                                 os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                except Exception:
                    return True  # không khóa được -> cho chạy tiếp
        try:
            os.write(fd, str(os.getpid()).encode("utf-8"))
        except Exception:
            pass
        _KHOA_DON_PHIEN_BAN_LOCKFILE = (lock_path, fd)
        return True
    except Exception as e:
        try:
            print("[single-instance] không tạo được khóa: %s" % e)
        except Exception:
            pass
        return True


def _mo_khoa_don_phien_ban():
    """Nhả khóa single-instance (chỉ dùng khi dọn dẹp/test;
    app chính KHÔNG gọi — handle/file sống theo process)."""
    global _KHOA_DON_PHIEN_BAN_HANDLE, _KHOA_DON_PHIEN_BAN_LOCKFILE
    try:
        if _KHOA_DON_PHIEN_BAN_HANDLE is not None:
            try:
                import ctypes
                ctypes.windll.kernel32.CloseHandle(
                    _KHOA_DON_PHIEN_BAN_HANDLE)
            except Exception:
                pass
            _KHOA_DON_PHIEN_BAN_HANDLE = None
        if _KHOA_DON_PHIEN_BAN_LOCKFILE is not None:
            lock_path, fd = _KHOA_DON_PHIEN_BAN_LOCKFILE
            try:
                os.close(fd)
            except Exception:
                pass
            try:
                os.remove(lock_path)
            except Exception:
                pass
            _KHOA_DON_PHIEN_BAN_LOCKFILE = None
    except Exception:
        pass


if __name__ == "__main__":
    if not _khoa_don_phien_ban():
        try:
            messagebox.showinfo(
                "Tool đang chạy rồi",
                "ChipChipStudio chỉ chạy 1 bản duy nhất, bấm mở thêm "
                "sẽ không mở bản mới.")
        except Exception:
            pass
        sys.exit(0)
    QuanLy().mainloop()

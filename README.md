# Chipchipdownload

Tool tải + gộp video Bilibili thành 1 video hoàn chỉnh có cả hình lẫn tiếng,
để đưa vào iContent làm tiếp. Tên hiển thị: **Chipchipdownload** (v6.2).
File nguồn vẫn là `Gop-Video-Bilibili-GUI.py` trong repo này.

## Cài đặt

Chạy file `Chipchipdownload-Setup-vX.Y.exe` (build từ GitHub Actions):
cài vào `C:\Program Files\Chipchipdownload`, tạo shortcut Desktop +
Start Menu tên **Chipchipdownload** (icon gà con). Cũng có thể chạy trực
tiếp file `Chipchipdownload.exe` (bản portable, không cần cài).

Gỡ cài đặt sẽ xóa luôn các thư viện tool đã tự tải về khi chạy
(`yt-dlp.exe`, `ffmpeg.exe`, `ffprobe.exe`, `config.json`, `jobs.json`)
vì chúng nằm cùng thư mục cài đặt.

## 1. Tải video từ Bilibili

Mở cửa sổ quản lý, bấm **+ Mở cửa sổ mới** — mỗi cửa sổ xử lý 1 video.

1. Dán link Bilibili (BV...) vào ô link, bấm **Kiểm tra link**.
2. Chọn chất lượng (1080p / 720p / 480p...).
3. Bấm **TẢI XUỐNG + GỘP LUÔN** để tải bằng yt-dlp rồi tự gộp, hoặc bấm
   **TẢI BẰNG IDM (nhanh, nhiều luồng)** để đẩy link hình + link tiếng sang
   IDM tải nhanh. Tool hiện **% tải** ở thanh tiến độ (quét dung lượng mọi
   file media trong thư mục, kể cả `.m4s`), tải xong **tự nhận diện cặp
   file rồi TỰ GỘP luôn**, không cần bấm tay. Gộp xong tự xóa 2 file gốc
   cho nhẹ ổ (có thể tắt ở ô tick trong cửa sổ job).
4. Lịch sử job lưu vào `jobs.json` — lần sau mở tool, các job chưa xong
   sẽ tự mở lại cửa sổ để tiếp tục.

### Vì sao phần tải IDM làm được (và lệnh IDM thường thì không)

Link stream video Bilibili bắt buộc phải có header Referer mới tải được
(đã test thật: có Referer + User-Agent trình duyệt = 206, không Referer =
403). Lệnh dòng lệnh của IDM (`IDMan.exe /d ...`) không gửi được Referer
nên dán link Bilibili vào IDM là tải lỗi 403. Vì vậy tool dùng **COM API
chính thức của IDM** (`SendLinkToIDM2`) — đúng cơ chế extension trình
duyệt đẩy link sang IDM: gửi kèm link + Referer (trang video Bilibili) +
cookie (đọc từ file cookies.txt) nên IDM tải được, nhanh nhiều luồng.

## 2. Gộp 2 file đã có (tải bằng IDM)

Bilibili tách hình/tiếng thành 2 luồng DASH nên IDM tải về 2 file riêng
(1 file chỉ có hình + 1 file chỉ có tiếng). Chọn 2 file đó (hoặc bấm **Chọn
thư mục chứa 2 file** để tool tự nhận diện), bấm **GỘP VIDEO**. Gộp xong
thì bấm **XEM THÀNH QUẢ** để mở video vừa gộp ra xem. Thanh **% gộp**
hiện tiến độ từng cửa sổ.

## Cập nhật

Nút **Kiểm tra cập nhật** ở cửa sổ Quản lý: tool kiểm tra bản mới trên
GitHub Releases của repo `Cyandeptrai/gop-video-bilibili`, nếu có bản mới
thì tải exe mới về và **vá lên bản đang dùng** (không cần cài lại, giữ
nguyên lịch sử job + cài đặt). File exe đang chạy bị Windows khóa nên tool
dùng script phụ `capnhat.bat`: chờ tool thoát rồi thay exe cũ bằng exe mới
và tự mở lại tool.

Lưu ý: repo là **private** nên tự cập nhật cần 1 token GitHub **chỉ đọc**
repo này (fine-grained token, quyền Contents: Read-only). Nhập token 1 lần
khi tool hỏi, token chỉ lưu ở `config.json` cạnh exe, không nhúng trong
code. Không có token thì nút Update chỉ hiện phiên bản hiện tại + hướng dẫn
tải bản mới bằng tay tại trang Releases của repo.

## Thư mục lưu

Video hoàn thiện lưu vào `<thư mục lưu>\<tên video>\<tên video>.mp4`
(thư mục lưu mặc định: `Desktop\Video-Da-Gop`, nhớ lựa chọn lần sau).
Ví dụ: `Desktop\Video-Da-Gop\Thanh Dong\Thanh Dong.mp4`.

## Thư viện thiếu thì tool tự tải

- `yt-dlp` + `ffmpeg` trên máy. Tool tự tìm (cùng thư mục với `.exe`,
  PATH, `C:\ffmpeg`, `C:\iContent`...). Nếu không thấy, tool hỏi và **tự
  tải về** (yt-dlp từ GitHub, ffmpeg bản essentials từ gyan.dev) thay vì
  chỉ báo link tải tay.
- File `cookies.txt` của Bilibili (để tải 1080p). Không có cookies thì thường
  chỉ tải được 480p. Tool tự nhận file ở
  `Desktop\Cookiebili\cookies.txt` nếu có, hoặc bấm Chọn để chỉ đường dẫn.

## Vì sao không bấm nút tải của Cốc Cốc tự động

Nút tải video của Cốc Cốc là nút của **giao diện trình duyệt**, không phải
nút trên trang web, nên tool không bấm được bằng cách điều khiển trang
(CDP/Selenium chỉ chạm được nội dung trang). Bấm theo tọa độ màn hình thì
dễ lệch, không ổn định. Vì vậy tool đẩy link **thẳng sang IDM** bằng COM
API (cùng Referer + cookie mà Cốc Cốc gửi) nên tốc độ tải nhanh như nhau,
không cần mở Cốc Cốc.

## Build

GitHub Actions tự build trên Windows mỗi lần push lên `main` hoặc tag `v*`
(`.github/workflows/build-exe.yml`):
- Job `build`: PyInstaller `--onefile --windowed --name Chipchipdownload
  --icon chipchipdownload.ico` → artifact `Chipchipdownload-exe`.
- Job `installer`: cài Inno Setup (choco), build `installer.iss` →
  artifact `Chipchipdownload-Setup` (`Chipchipdownload-Setup-vX.Y.exe`).
- Job `release` (chỉ khi push tag `v*`): tạo GitHub Release, đính kèm exe
  + file cài đặt (để nút Kiểm tra cập nhật trong tool tải về).

Cần thêm thư viện `comtypes` (để gọi COM API của IDM) — đã có trong
workflow (`pip install pyinstaller comtypes`).

## Bản console

`Gop-Video-Bilibili.py` + `Gop-Video-Bilibili.bat` (bản cũ, không giao diện,
chỉ gộp file) đang lưu ở máy Gà Con, không nằm trong repo này.

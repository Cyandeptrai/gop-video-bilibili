# Gộp Video Bilibili

Tool gộp video Bilibili thành 1 video hoàn chỉnh có cả hình lẫn tiếng, để đưa
vào iContent làm tiếp. Có 2 chức năng:

## 1. Tải video từ Bilibili

1. Dán link Bilibili (BV...) vào ô link, bấm **Kiểm tra link**.
2. Chọn chất lượng (1080p / 720p / 480p...).
3. Bấm **TẢI XUỐNG + GỘP LUÔN** để tải bằng yt-dlp rồi tự gộp, hoặc bấm
   **TẢI BẰNG IDM (nhanh, nhiều luồng)** để đẩy link hình + link tiếng sang
   IDM tải nhanh, xong thì gộp ở mục 3.

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
thư mục chứa 2 file** để tool tự nhận diện), bấm **GỘP VIDEO**.

## Thư mục lưu

Video hoàn thiện lưu vào `<thư mục lưu>\<tên video>\<tên video>.mp4`
(thư mục lưu mặc định: `Desktop\Video-Da-Gop`, nhớ lựa chọn lần sau).
Ví dụ: `Desktop\Video-Da-Gop\Thanh Dong\Thanh Dong.mp4`.

## Yêu cầu

- `ffmpeg` + `yt-dlp` trên máy. Tool tự tìm (cùng thư mục với `.exe`, PATH,
  `C:\ffmpeg`, `C:\iContent`...). Nếu không thấy, tool báo link tải:
  - ffmpeg: https://www.gyan.dev/ffmpeg/builds/
  - yt-dlp: https://github.com/yt-dlp/yt-dlp/releases (file `yt-dlp.exe`)
- File `cookies.txt` của Bilibili (để tải 1080p). Không có cookies thì thường
  chỉ tải được 480p. Tool tự nhận file ở
  `Desktop\Cookiebili\cookies.txt` nếu có, hoặc bấm Chọn để chỉ đường dẫn.

## Vì sao phần tải không dùng lệnh IDM thường

Xem mục 1 ở trên: lệnh dòng lệnh của IDM không gửi được Referer nên tải
link Bilibili bị 403; tool v3 dùng COM API của IDM để gửi kèm Referer +
cookie nên tải được.

## Build

GitHub Actions tự build `.exe` trên Windows mỗi lần push lên `main`
(`.github/workflows/build-exe.yml`, PyInstaller `--onefile --windowed`).
Cần thêm thư viện `comtypes` (để gọi COM API của IDM) — đã có trong
workflow (`pip install pyinstaller comtypes`).

## Bản console

`Gop-Video-Bilibili.py` + `Gop-Video-Bilibili.bat` (bản cũ, không giao diện,
chỉ gộp file) đang lưu ở máy Gà Con, không nằm trong repo này.

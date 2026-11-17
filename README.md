# Gộp Video Bilibili

Tool gộp 2 file video Bilibili tải bằng IDM (1 file chỉ có hình + 1 file chỉ có
tiếng, do Bilibili tách hình/tiếng thành 2 luồng DASH) thành 1 video hoàn chỉnh
có cả hình lẫn tiếng, để đưa vào iContent làm tiếp.

## Cách dùng (bản .exe)

1. Tải file `Gop-Video-Bilibili.exe` ở mục Releases (hoặc Actions -> Artifacts).
2. Bấm đúp file `.exe`.
3. Chọn file Video (hình) + file Audio (tiếng), hoặc bấm **"Chọn thư mục chứa
   2 file"** để tool tự nhận diện (dùng ffprobe xem file nào thật sự có hình,
   không đọc được thì đoán theo cỡ file).
4. Chọn thư mục lưu mặc định (mặc định: `Desktop\Video-Da-Gop`, nhớ lựa chọn
   lần sau).
5. Bấm **GỘP VIDEO**. Tool tự tạo thư mục con tên như video trong thư mục lưu
   và lưu video hoàn thiện vào đó, ví dụ:
   `Desktop\Video-Da-Gop\Thanh Dong\Thanh Dong.mp4`.

## Yêu cầu

- Cần `ffmpeg` trên máy. Tool tự tìm ffmpeg (cùng thư mục với `.exe`, PATH,
  `C:\ffmpeg`, `C:\iContent`...). Nếu không thấy, tool báo link tải:
  https://www.gyan.dev/ffmpeg/builds/ — giải nén, copy `ffmpeg.exe` vào cùng
  thư mục với tool là chạy.

## Build

GitHub Actions tự build `.exe` trên Windows mỗi lần push lên `main`
(`.github/workflows/build-exe.yml`, PyInstaller `--onefile --windowed`).

## Bản console

`Gop-Video-Bilibili.py` + `Gop-Video-Bilibili.bat` (bản cũ, không giao diện)
đang lưu ở máy Gà Con, không nằm trong repo này.

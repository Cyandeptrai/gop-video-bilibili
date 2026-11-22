# -*- coding: utf-8 -*-
"""
postman2d.py — PostmanStudio 2D (module mới cho ChipChipStudio v7.26)
====================================================================
Mục đích (theo lệnh CYAN 21/11 ~21:29): làm video YouTube faceless
bằng tool của CYAN thay vì iCast — vẽ nhân vật que 2D bằng code,
voice VieNeu, JSON kịch bản dán 1 lần là tool tự nhận cảnh + SRT.

CÁI GÌ ĐÃ XÁC MINH / CÁI GÌ CHƯA:
- "PostmanStudio 2D" KHÔNG tìm thấy trên web công khai (quét
  21/11/2026): đây là tên CYAN đặt cho module mới trong ChipChipStudio,
  KHÔNG phải tool ngoài đã có sẵn. Luồng vẽ bằng code xây trên 2
  engine đã có trong workspace: skill `2d` (skia-python, engine/)
  và skill `cyan-2d` (H2 Studio, kit/packs/*/nguoi.js — CAST nhân
  vật + POSES). Renderer ở đây là bản Pillow tối giản, vẽ đúng
  nhân vật đã khóa của kênh Thích Bạn Từ Xa; chưa phải engine H2
  đầy đủ (cần Node + Chromium). Nếu CYAN muốn đúng engine H2 thì
  bước sau là nối `kit/` của cyan-2d vào thay cho renderer Pillow.
- VieNeu ĐÃ xác minh bằng SDK thật (21/11/2026, pip install
  vieneu==3.8.5, đọc voices_v3_turbo.json trong package):
  `pip install vieneu`, v3 Turbo 48 kHz, SDK 3.8.5 có 25 giọng
  preset (README cũ v3.7.1 ghi 23 giọng, default Minh Quân —
  3.8.5 đổi default thành Hải Đăng, alias giữ tên cũ chạy được),
  gọi bằng `Vieneu().infer(text, voice="Xuân Vĩnh")`, Apache-2.0,
  dùng thương mại được. Xuân Vĩnh = Bắc / nam / Natural,
  Phạm Tuyên = Bắc / nam / Natural, Ngọc Huyền = Bắc / nữ /
  Natural. Dung lượng model KHÔNG ghi trong README —
  KHÔNG khẳng định "2-3 GB" khi chưa tải thật trên máy CYAN; lần
  tải đầu sẽ đo và log dung lượng thật.
- Nhân vật: chỉ gọi bằng ID (cau_ay, him, nguoi_ay, me, minh,
  ba_ban_xoi, co_hanh), KHÔNG mô tả lại ngoại hình trong prompt
  từng cảnh — ngoại hình khóa nằm ở registry dưới đây. Ảnh mẫu
  đã khóa chỉ có cho cau_ay / him / nguoi_ay (4 ảnh mỗi người,
  trong workspace/user/media_library/image/). Mẹ, Minh, Bà bán xôi,
  Cô Hạnh CHƯA có ảnh mẫu đã khóa — registry ghi rõ
  has_reference_image=False; các nhân vật này hiện chỉ vẽ bằng
  code theo spec (áo/khăn/đồ cầm), CYAN cần gửi ảnh mẫu hoặc
  duyệt bản vẽ code trước khi khóa.
- Chưa kiểm chứng trên máy Windows của CYAN: chưa chạy VieNeu
  thật, chưa render MP4 cuối thật trên máy cậu, chưa build exe.
  Mọi test dưới đây chạy trên Linux (sandbox) — xem __main__.

Luồng (đúng lệnh CYAN):
  JSON kịch bản (dán vào tab Postman 2D)
    -> parse_postman_json(): tự nhận scenes, tự chia cảnh
       (mỗi scene = 1 cảnh nhỏ; nút "+ Thêm cảnh" thêm 1 scene rỗng)
    -> mỗi scene có: prompt_video_postman (ô điền riêng),
       characters (chọn từ registry đã lưu), narration, image_prompt,
       motion_prompt (EN+VI)
    -> JSON đồng thời chứa srt_cues: voice tạo từ SRT, đồng nhất
       voice với cảnh (cue i <-> scene i, timing cộng dồn).
    -> VieNeu đọc từng cue (Xuân Vĩnh chính, Phạm Tuyên dự phòng)
    -> renderer vẽ từng cảnh bằng code -> MP4 từng cảnh
       -> ffmpeg nối các cảnh -> MP4 cuối 16:9.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

VERSION_POSTMAN = "1.5"  # module Postman 2D, dùng trong ChipChipStudio v7.31


def _chay_ngam_kwargs():
    """Mọi subprocess (ffmpeg/ffprobe/pip/node/python) đều chạy
    ngầm, không để cửa sổ console nhấp nháy (luật CYAN 19-20/11).
    Ngoại lệ duy nhất: lệnh mở file/thư mục có chủ đích
    (os.startfile / xdg-open) thì không dùng hàm này."""
    if sys.platform.startswith("win"):
        import subprocess as _sp
        _si = _sp.STARTUPINFO()
        _si.dwFlags |= _sp.STARTF_USESHOWWINDOW
        _si.wShowWindow = _sp.SW_HIDE
        return {"startupinfo": _si,
                "creationflags": _sp.CREATE_NO_WINDOW}
    return {}


def _python_he_thong():
    """(v7.25, SỬA LỖI GỐC nhân bản vô hạn; v7.26 KIỂM CHỨNG ứng
    viên) Trả đường dẫn Python hệ thống để chạy pip / engine
    skia, KHÔNG BAO GIỜ dùng sys.executable khi đã đóng gói:
    trong bản exe PyInstaller, sys.executable CHÍNH LÀ
    Chipchipdownload.exe — chạy [sys.executable, "-m", ...] sẽ
    mở thêm 1 bản tool thay vì chạy Python (khởi động gọi
    model_ve_mac_dinh() -> kiem_tra_tai_nguyen_ve() ->
    [sys.executable, "-c", "import skia"] nên tool tự nhân vô
    hạn trên máy CYAN).
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
        kw = _chay_ngam_kwargs()
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


def _do_dai_audio_giay(path):
    """Đo thời lượng thật của 1 file audio bằng ffprobe.
    Trả số giây (float) hoặc None nếu đo không được."""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=30,
            **_chay_ngam_kwargs())
        d = float((r.stdout or "").strip())
        return d if d > 0 else None
    except Exception:
        return None

# ------------------------------------------------------------------
# 1. Registry nhân vật — CHỈ GỌI TÊN (ID), KHÔNG MÔ TẢ LẠI
# ------------------------------------------------------------------
# Quy tắc khóa (21/11): đầu tròn không mặt, KHÔNG mắt/lông mi,
# chân 1 nét, tay đơn giản không ngón, phân biệt bằng LOẠI KHĂN +
# ĐỒ CẦM, không phân biệt bằng màu. Số đếm ngược: khung NHỎ,
# bay lơ lửng phía TRÊN đầu, có khoảng cách rõ với đầu, KHÔNG
# chạm đầu, KHÔNG đè lên đầu, KHÔNG quá to.
MEDIA_DIR = "workspace/user/media_library/image"

CHARACTERS = {
    "cau_ay": {
        "id": "cau_ay", "ten": "Cậu Ấy",
        "vai_tro": "Nhân vật chính, người kể chuyện, 18 tuổi, lớp 12",
        "khan": "khăn quàng đỏ thắt nơ (kiểu học sinh VN)",
        "mau_khan": "#c1272d", "mau_ao": "#1a1a1a",
        "nen": "trắng", "do_cam_mac_dinh": "sách",
        "giong": "Xuân Vĩnh", "has_reference_image": True,
        "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét",
        "anh_mau": [
            "cau-ay-white-red-exact-angle-book.webp",
            "cau-ay-white-red-exact-full.webp",
            "cau-ay-white-red-exact-hold-book.webp",
            "cau-ay-white-red-exact-portrait.webp",
        ],
    },
    "him": {
        "id": "him", "ten": "Him",
        "vai_tro": "Nhân vật chính kênh EN, nam, nhiều bối cảnh",
        "khan": "khăn len xanh navy đậm quấn cổ thả xuống",
        "mau_khan": "#1b2a52", "mau_ao": "#1a1a1a",
        "nen": "xám nhạt", "do_cam_mac_dinh": "ly cà phê",
        "giong": "Xuân Vĩnh", "has_reference_image": True,
        "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét",
        "anh_mau": [
            "media-generation-him-grey-angle-coffee-0-7e5ebad1-3cad-4b14-978e-dc61d2e395a9.webp",
            "media-generation-him-grey-full-empty-0-fa1c27e9-fa6b-4cde-9d3d-317033f103a4.webp",
            "media-generation-him-grey-full-coffee-0-3d796832-308c-4a06-a6a1-44ec936fdef7.webp",
            "him-grey-bg-coffee-exact.webp",
        ],
    },
    "nguoi_ay": {
        "id": "nguoi_ay", "ten": "Người Ấy",
        "vai_tro": "Người được thích thầm, 18 tuổi, lớp 12",
        "khan": "khăn len xám quấn cổ thả xuống 2 bên (KHÔNG thắt nơ)",
        "mau_khan": "#8a8a8a", "mau_ao": "#1a1a1a",
        "nen": "trắng", "do_cam_mac_dinh": "sách (ôm thấp ở thắt lưng)",
        "giong": "Xuân Vĩnh (nhẹ hơn khi thoại)",
        "hao_quang": "vàng ấm + sao lấp lánh",
        "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét",
        "has_reference_image": True,
        "anh_mau": [
            "ng__i__y_3.webp", "ng__i__y_1.webp",
            "ng__i__y_2.webp", "ch_n_dung_ng__i__yy.webp",
        ],
    },
    "me": {
        "id": "me", "ten": "Mẹ",
        "vai_tro": "Mẹ của Cậu Ấy (phụ, chỉ trong video này)",
        "khan": "tạp dề", "mau_khan": "#c98fa6", "mau_ao": "#c98fa6",
        "nen": "nhà bếp", "do_cam_mac_dinh": "xoong / khăn lau",
        "giong": "Xuân Vĩnh", "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét", "has_reference_image": False,
        "anh_mau": [],
        "ghi_chu": "CHƯA có ảnh mẫu đã khóa — vẽ bằng code, cần CYAN duyệt.",
    },
    "minh": {
        "id": "minh", "ten": "Minh",
        "vai_tro": "Bạn thân của Cậu Ấy, 18 tuổi (phụ)",
        "khan": "khăn quàng xanh lá", "mau_khan": "#2e7d32",
        "mau_ao": "#2e7d32", "nen": "sân trường / căng tin",
        "do_cam_mac_dinh": "chai nước",
        "giong": "Xuân Vĩnh (nhanh, hài)", "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét", "has_reference_image": False,
        "anh_mau": [],
        "ghi_chu": "CHƯA có ảnh mẫu đã khóa — vẽ bằng code, cần CYAN duyệt.",
    },
    "ba_ban_xoi": {
        "id": "ba_ban_xoi", "ten": "Bà Tư (bà bán xôi)",
        "vai_tro": "Bà bán xôi vỉa hè, 65 tuổi (phụ)",
        "khan": "khăn nâu", "mau_khan": "#7a5c3e", "mau_ao": "#7a5c3e",
        "nen": "quán xôi vỉa hè", "do_cam_mac_dinh": "rổ xôi / gói xôi",
        "giong": "Xuân Vĩnh (chậm, ấm)", "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét", "has_reference_image": False,
        "anh_mau": [],
        "ghi_chu": "CHƯA có ảnh mẫu đã khóa — vẽ bằng code, cần CYAN duyệt.",
    },
    "co_hanh": {
        "id": "co_hanh", "ten": "Cô Hạnh",
        "vai_tro": "Cô giáo chủ nhiệm, 40 tuổi (phụ)",
        "khan": "khăn tím", "mau_khan": "#7b5ea7", "mau_ao": "#7b5ea7",
        "nen": "lớp học", "do_cam_mac_dinh": "sổ điểm / cốc trà",
        "giong": "Xuân Vĩnh (chậm, ấm)", "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét", "has_reference_image": False,
        "anh_mau": [],
        "ghi_chu": "CHƯA có ảnh mẫu đã khóa — vẽ bằng code, cần CYAN duyệt.",
    },
}


# ------------------------------------------------------------------
# 1b. Lưu nhân vật theo tên — dùng chung tab Postman 2D + tab
# "Tạo nhân vật" (bổ sung CYAN 21/11 ~21:33).
# Draft v7.23 CHƯA có hạ tầng tạo/lưu nhân vật nào (nhan_vat trong
# code cũ mới chỉ là tên trong prompt dịch và JSON tab Faceless) —
# đây là chỗ lưu mới, 1 file JSON cạnh postman2d.py:
# nhan_vat_postman.json — {id: {thông số code đã lưu}}.
# Tab Postman 2D chỉ gọi tên (id) ra dùng, không mô tả lại.
# ------------------------------------------------------------------
NHAN_VAT_FILE = os.environ.get(
    "POSTMAN_NHAN_VAT_FILE") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "nhan_vat_postman.json")


def duong_dan_nhan_vat():
    return NHAN_VAT_FILE


def doc_nhan_vat_da_luu():
    """Đọc file nhan_vat_postman.json -> {id: spec}. Lỗi/thiếu -> {}."""
    try:
        with open(duong_dan_nhan_vat(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


# ------------------------------------------------------------------
# 1b2. Nhân vật có sẵn theo pack (mục F, CYAN 21/11 ~21:33).
# Trích đúng từ file gốc trong plugin-goc (đã đối chiếu CAST bằng
# regex ngày 21/11 ~23:26 — KHÔNG bịa thêm nhân vật nào):
#   Chíp 16, Nguệch 18, Giáo Sư 22, skia mẫu 4 (marshmallow).
# Nhân vật gốc KHÔNG sửa trực tiếp — bấm vào là nạp toàn bộ
# thông số vào khung chỉnh, sửa rồi lưu dưới tên cậu. Khi dựng
# bằng H2 pack đó mới đúng kiểu; xem nhanh Pillow chỉ xem tạm
# (khăn vẽ cùng màu áo). Tag @Tên chỉ gọi nhân vật đã lưu —
# muốn dùng gốc bằng tag thì lưu nó dưới 1 tên trước.
# ------------------------------------------------------------------
TEN_PACK = {"chip": "Chíp", "nguech": "Nguệch",
            "giaosu": "Giáo Sư", "skia": "Skia mẫu"}
# Tên thư mục pack trong kit H2 (config.json "pack").
PACK_ID_H2 = {"chip": "chipsieunang", "nguech": "nguechngoac",
              "giaosu": "giaosubut"}

NHAN_VAT_CO_SAN = {
    "chip": {
        "ban":      {"ao": "hoodie", "mau": "#f08a1e", "toc": "xu"},
        "bankhong": {"ao": "hoodie", "mau": "#f08a1e"},
        "me":       {"ao": "cardigan", "mau": "#c8b6d6", "toc": "bui"},
        "ba":       {"ao": "somi", "mau": "#7d8aa6", "toc": "ngan"},
        "banthan":  {"ao": "hoodie", "mau": "#5f6f8a", "toc": "xu"},
        "crush":    {"ao": "hoodie", "mau": "#e8c6d0", "toc": "dai"},
        "cobanxoi": {"ao": "cardigan", "mau": "#b89a6a", "toc": "bui",
                     "non": "nonla"},
        "cogiao":   {"ao": "aodai", "mau": "#b8c9dc", "toc": "bui",
                     "kinh": True},
        "thay":     {"ao": "somi", "mau": "#e9e6df", "toc": "ngan",
                     "kinh": True},
        "bacsi":    {"ao": "blouse", "mau": "#f1efe9", "kinh": True},
        "em":       {"ao": "hoodie", "mau": "#6fb0d8", "toc": "xu",
                     "kid": True},
        "nguoila":  {"ao": "hoodie", "mau": "#8f9aa6"},
        "qua1":     {"ao": "hoodie", "mau": "#8a8478"},
        "qua2":     {"ao": "hoodie", "mau": "#6f7a86"},
        "qua3":     {"ao": "hoodie", "mau": "#9a8a8e"},
        "qua4":     {"ao": "hoodie", "mau": "#7a8a76"},
    },
    "nguech": {
        "ban":      {"ao": "hoodie", "mau": "#e4552f"},
        "banxu":    {"ao": "hoodie", "mau": "#e4552f", "toc": "xu"},
        "me":       {"ao": "hoodie", "mau": "#d8a640", "toc": "bui"},
        "ba":       {"ao": "somi", "mau": "#7d8aa6", "toc": "ngan"},
        "ban2":     {"ao": "hoodie", "mau": "#3a9e7a"},
        "crush":    {"ao": "hoodie", "mau": "#8e7ad8", "toc": "dai"},
        "em":       {"ao": "hoodie", "mau": "#4fa3d8", "kid": True},
        "ong":      {"ao": "cardigan", "mau": "#8a7f70", "toc": "hoi",
                     "kinh": True},
        "trongtai": {"ao": "somi", "mau": "#1e1e26"},
        "vdv1":     {"ao": "hoodie", "mau": "#2f6fd0"},
        "vdv2":     {"ao": "hoodie", "mau": "#3aa86a"},
        "vdv3":     {"ao": "hoodie", "mau": "#8a5ad0"},
        "bacsi":    {"ao": "blouse", "mau": "#f1efe9"},
        "nguoila":  {"ao": "hoodie", "mau": "#7d7488"},
        "qua1":     {"ao": "hoodie", "mau": "#6d6280"},
        "qua2":     {"ao": "hoodie", "mau": "#5f6f86"},
        "qua3":     {"ao": "hoodie", "mau": "#8a6a78"},
        "qua4":     {"ao": "hoodie", "mau": "#5f7a6c"},
    },
    "giaosu": {
        "ban":      {"ao": "hoodie", "mau": "#2f5fe0"},
        "banxu":    {"ao": "hoodie", "mau": "#2f5fe0", "toc": "xu"},
        "crush":    {"ao": "hoodie", "mau": "#f2b230", "toc": "duoi",
                     "buoc": "#f2b230"},
        "bangai":   {"ao": "hoodie", "mau": "#8b5cf6", "toc": "dai"},
        "banthan":  {"ao": "hoodie", "mau": "#e8732f", "toc": "xu"},
        "me":       {"ao": "cardigan", "mau": "#c98fa6", "toc": "bui"},
        "ba":       {"ao": "somi", "mau": "#7f8fa8", "toc": "ngan"},
        "ong":      {"ao": "cardigan", "mau": "#8a7f70", "toc": "hoi",
                     "kinh": True},
        "ba_ngoai": {"ao": "cardigan", "mau": "#8e6f8a", "toc": "bui",
                     "kinh": True},
        "em":       {"ao": "hoodie", "mau": "#3fb6a8", "kid": True},
        "emgai":    {"ao": "hoodie", "mau": "#ef7fa0", "toc": "bim",
                     "kid": True},
        "thay":     {"ao": "somi", "mau": "#e9e6df", "toc": "ngan",
                     "kinh": True},
        "cogiao":   {"ao": "aodai", "mau": "#b8c9dc", "toc": "bui",
                     "kinh": True},
        "bacsi":    {"ao": "blouse", "mau": "#f1efe9", "kinh": True},
        "baoho":    {"ao": "blouse", "mau": "#e8e2cf"},
        "congan":   {"ao": "somi", "mau": "#6f8a5a", "non": "kepi"},
        "kexau":    {"ao": "hoodie", "mau": "#3c3d48",
                     "non": "luoitrai", "nonMau": "#26262e"},
        "nguoila":  {"ao": "hoodie", "mau": "#8f9aa6"},
        "qua1":     {"ao": "hoodie", "mau": "#6d6a7e"},
        "qua2":     {"ao": "hoodie", "mau": "#5f6f86"},
        "qua3":     {"ao": "hoodie", "mau": "#7e6a78"},
        "qua4":     {"ao": "hoodie", "mau": "#5f7a6c"},
    },
    # Skia mẫu (skill 2d, examples/marshmallow/story.json cast):
    # mia/doc/sam/rex — spec skia: skin/outfit/color/shirt/tie/
    # hair/hair_col/glasses/moustache/beard/hat/hat_col.
    "skia": {
        "mia": {"skin": "fair", "outfit": "dress", "color": "#F2C14E",
                "hair": "bun", "hair_col": "#6B4A2A"},
        "doc": {"skin": "light", "outfit": "suit", "color": "#5B5B66",
                "tie": "#2F6B4E", "hair": "short",
                "hair_col": "#8A8A92", "glasses": True, "beard": True},
        "sam": {"skin": "brown", "outfit": "hoodie", "color": "#2F7A5A",
                "shirt": "#E8E0D0", "hair": "curly",
                "hair_col": "#1C1B22"},
        "rex": {"skin": "tan", "outfit": "tshirt", "color": "#C8242C",
                "hair": "slick", "hair_col": "#2A1E16", "hat": "cap",
                "hat_col": "#2B2D3C"},
    },
}


def danh_sach_nhan_vat_co_san():
    """[(pack, code, mô_tả)] cho mục 'Nhân vật có sẵn' ở tab
    Tạo nhân vật. Mô tả ghi rõ áo + màu gốc của pack."""
    ds = []
    for pack in ("chip", "nguech", "giaosu", "skia"):
        for code, spec in NHAN_VAT_CO_SAN[pack].items():
            if pack == "skia":
                mo_ta = "%s %s (%s)" % (
                    spec.get("outfit", ""), spec.get("color", ""),
                    spec.get("hair", ""))
            else:
                mo_ta = "%s %s%s%s" % (
                    spec.get("ao", ""), spec.get("mau", ""),
                    (" tóc %s" % spec["toc"]) if spec.get("toc") else "",
                    " (trẻ em)" if spec.get("kid") else "")
            ds.append((pack, code, mo_ta.strip()))
    return ds


def nap_nhan_vat_co_san(pack, code):
    """Nạp nhân vật gốc (pack, code) thành spec theo định dạng
    chung của tool (để khung chỉnh hiển thị + lưu dưới tên cậu).
    Trả None nếu pack/code không có. Nhân vật gốc KHÔNG sửa
    trực tiếp — spec này là BẢN SAO để chỉnh rồi lưu tên mới."""
    bang = NHAN_VAT_CO_SAN.get(pack)
    if not bang or code not in bang:
        return None
    goc = bang[code]
    ten_pack = TEN_PACK.get(pack, pack)
    spec = {
        "id": "co_san:%s:%s" % (pack, code),
        "ten": "%s (gốc %s)" % (code, ten_pack),
        "vai_tro": "Nhân vật gốc của pack %s" % ten_pack,
        "khan": ("không khăn — áo %s %s"
                 % (goc.get("ao", ""), goc.get("mau", "")))
        if pack != "skia" else ("không khăn — %s %s"
                                % (goc.get("outfit", ""),
                                   goc.get("color", ""))),
        "mau_khan": goc.get("mau") or goc.get("color") or "#888888",
        "mau_ao": goc.get("mau") or goc.get("color") or "#888888",
        "nen": "theo set của pack %s" % ten_pack,
        "do_cam_mac_dinh": "",
        "giong": "Xuân Vĩnh",
        "ti_le_dau": 0.22, "do_day_net": 1.0, "kieu_chan": "1 nét",
        "has_reference_image": False, "anh_mau": [],
        "ghi_chu": ("Nhân vật gốc của pack %s — vẽ theo kiểu của "
                    "pack đó, không phải kiểu stickman nét mảnh "
                    "đã khóa. Xem nhanh Pillow chỉ xem tạm "
                    "(khăn cùng màu áo); dựng bằng H2/Skia pack "
                    "%s mới đúng kiểu." % (ten_pack, ten_pack)),
        "pack_goc": pack, "code_goc": code,
    }
    if pack == "skia":
        spec["skia_cast"] = dict(goc)
    else:
        spec.update({"ao_goc": goc.get("ao"), "toc_goc": goc.get("toc"),
                     "kinh_goc": bool(goc.get("kinh")),
                     "non_goc": goc.get("non"),
                     "nonMau_goc": goc.get("nonMau"),
                     "kid_goc": bool(goc.get("kid")),
                     "buoc_goc": goc.get("buoc")})
    return spec


def danh_sach_nhan_vat_chon():
    """Danh sách cho ô chọn nhân vật ở tab Postman: nhân vật đã
    lưu (khóa + CYAN lưu thêm) + nhân vật có sẵn theo pack
    (ghi rõ bộ, vd 'Chíp: ban'). Trả [(id, nhãn)]. Chọn là
    dùng ngay — nhân vật gốc dùng id 'co_san:<pack>:<code>'."""
    ds = []
    for cid, nhan in danh_sach_nhan_vat_day_du():
        ds.append((cid, nhan))
    for pack, code, _mo_ta in danh_sach_nhan_vat_co_san():
        ds.append(("co_san:%s:%s" % (pack, code),
                   "%s: %s" % (TEN_PACK.get(pack, pack), code)))
    return ds


def lay_nhan_vat_hieu_luc(char_id):
    """Spec hiệu lực = mặc định khóa trong CHARACTERS + phần đã lưu
    (đã lưu thắng mặc định). Nhân vật mới chỉ có phần đã lưu.
    Id 'co_san:<pack>:<code>' -> nhân vật gốc của pack (mục F),
    vẽ theo kiểu của pack đó, không phải kiểu stickman đã khóa."""
    cid = str(char_id or "").strip()
    if cid.startswith("co_san:"):
        try:
            _, pack, code = cid.split(":", 2)
        except ValueError:
            return None
        return nap_nhan_vat_co_san(pack, code)
    mac_dinh = CHARACTERS.get(cid, {})
    da_luu = doc_nhan_vat_da_luu().get(cid, {})
    hop = dict(mac_dinh)
    hop.update(da_luu)
    hop["id"] = cid
    return hop if hop else None


def luu_nhan_vat(spec):
    """Lưu 1 nhân vật theo tên (id). spec phải có id + ten.
    Trả (ok, loi). Ghi đè phần đã lưu của id đó, không đụng id khác."""
    if not isinstance(spec, dict):
        return False, "Spec nhân vật phải là dict."
    cid = str(spec.get("id") or "").strip()
    ten = str(spec.get("ten") or "").strip()
    if not cid or not ten:
        return False, "Nhân vật cần có id và tên (vd id='minh', tên='Minh')."
    if not re.match(r"^[a-z0-9_]+$", cid):
        return False, ("id chỉ dùng chữ thường, số, gạch dưới "
                       "(vd 'ba_ban_xoi'), không dấu/khoảng trắng.")
    data = doc_nhan_vat_da_luu()
    giu = dict(spec)
    giu["id"] = cid
    data[cid] = giu
    try:
        with open(duong_dan_nhan_vat(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, ""
    except Exception as e:
        return False, "Không lưu được file nhân vật: %s" % e


def xoa_nhan_vat_da_luu(char_id):
    """Xóa phần đã lưu của 1 id (nhân vật khóa vẫn còn bản mặc định
    trong CHARACTERS; nhân vật mới thì mất hẳn)."""
    data = doc_nhan_vat_da_luu()
    if str(char_id) not in data:
        return False, "Nhân vật này chưa có bản lưu riêng."
    del data[str(char_id)]
    try:
        with open(duong_dan_nhan_vat(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, ""
    except Exception as e:
        return False, "Không xóa được: %s" % e


def danh_sach_nhan_vat_day_du():
    """Tất cả id có thể gọi tên trong Postman: khóa + đã lưu mới."""
    ids = list(CHARACTERS.keys())
    for cid in doc_nhan_vat_da_luu().keys():
        if cid not in ids:
            ids.append(cid)
    out = []
    for cid in ids:
        c = lay_nhan_vat_hieu_luc(cid) or {}
        out.append((cid, "%s (%s)" % (c.get("ten") or cid, cid)))
    return out

# Giọng VieNeu — ĐÃ XÁC MINH bằng SDK thật (21/11/2026):
# pip show: vieneu mới nhất trên PyPI = 3.8.5 -> PIN 3.8.5
# (chú thích cũ ghi "SDK v3.7.1" là README cũ, đã sửa).
# Đọc thẳng file voices_v3_turbo.json trong package 3.8.5:
# 25 preset (KHÔNG phải 23 như README v3.7.1), default của SDK
# đổi thành "Hải Đăng" (3.7.1 là "Minh Quân"); alias giữ tên cũ
# chạy được: "Minh Quân"/"Minh Quân Pro" -> "Hải Đăng".
# Xuân Vĩnh = Bắc / nam / Natural (chính), Phạm Tuyên = Bắc /
# nam / Natural (dự phòng). Ngọc Huyền = Bắc / nữ / Natural.
# Giọng mặc định của SDK là Hải Đăng — KHÔNG dùng làm mặc định
# ở đây, vì CYAN chốt Xuân Vĩnh. Danh sách chạy lấy động từ
# tts.list_preset_voices() khi đã tải model; bảng dưới là
# fallback khi chưa tải (dùng để kiểm tra tên giọng trong JSON).
VIENEU_VOICES = {
    # Bắc (15)
    "Adam bựa": {"region": "Bắc", "sex": "nam", "character": "Natural"},
    "Hải Đăng": {"region": "Bắc", "sex": "nam", "character": "Natural"},
    "Mai Anh": {"region": "Bắc", "sex": "nữ", "character": "News"},
    "Minh Đức": {"region": "Bắc", "sex": "nam", "character": "News"},
    "Ngọc Huyền": {"region": "Bắc", "sex": "nữ", "character": "Natural"},
    "Ngọc Linh": {"region": "Bắc", "sex": "nữ", "character": "Storytelling"},
    "Phạm Tuyên": {"region": "Bắc", "sex": "nam", "character": "Natural"},
    "Quốc Tuấn": {"region": "Bắc", "sex": "nam", "character": "Natural"},
    "Quỳnh Anh": {"region": "Bắc", "sex": "nữ", "character": "Storytelling"},
    "Thanh Bình": {"region": "Bắc", "sex": "nam", "character": "Storytelling"},
    "Thiền Tâm Đức": {"region": "Bắc", "sex": "nam", "character": "Storytelling"},
    "Thiện Minh": {"region": "Bắc", "sex": "nam", "character": "Storytelling"},
    "Trúc Ly": {"region": "Bắc", "sex": "nữ", "character": "Natural"},
    "Xuân Vĩnh": {"region": "Bắc", "sex": "nam", "character": "Natural"},
    "Đoan Trang": {"region": "Bắc", "sex": "nữ", "character": "Natural"},
    # Trung (2)
    "Ngọc Trân": {"region": "Trung", "sex": "nữ", "character": "Natural"},
    "Quang Sơn": {"region": "Trung", "sex": "nam", "character": "Natural"},
    # Nam (8)
    "Adam": {"region": "Nam", "sex": "nam", "character": "Natural"},
    "Kim Thanh": {"region": "Nam", "sex": "nữ", "character": "Storytelling"},
    "Minh Triết": {"region": "Nam", "sex": "nam", "character": "News"},
    "Mỹ Duyên": {"region": "Nam", "sex": "nữ", "character": "Storytelling"},
    "Thái Sơn": {"region": "Nam", "sex": "nam", "character": "Storytelling"},
    "Thùy Dung": {"region": "Nam", "sex": "nữ", "character": "News"},
    "Thục Đoan": {"region": "Nam", "sex": "nữ", "character": "Storytelling"},
    "Đức Trí": {"region": "Nam", "sex": "nam", "character": "Storytelling"},
}
# Tên giọng cũ (SDK <=3.7.1) vẫn chạy được nhờ alias của SDK.
VIENEU_ALIAS = {"Minh Quân": "Hải Đăng", "Minh Quân Pro": "Hải Đăng"}
VIENEU_VOICE_CHINH = "Xuân Vĩnh"
VIENEU_VOICE_DU_PHONG = "Phạm Tuyên"
VIENEU_SDK_VERSION = "3.8.5"
VIENEU_MODEL_HF = "pnnbao-ump/VieNeu-TTS-v3-Turbo"
VIENEU_SAMPLE_RATE = 48000  # v3 Turbo 48 kHz


def danh_sach_giong_vieneu():
    """Danh sách preset VieNeu: lấy động từ SDK đã cài (đã tải
    model) nếu được, không thì trả bảng fallback 25 giọng ở trên.
    Trả [tên preset] đã sắp xếp (Xuân Vĩnh + Phạm Tuyên lên đầu
    để dropdown mặc định đúng giọng CYAN đã chốt)."""
    ds = []
    try:
        from vieneu import Vieneu
        tts = Vieneu()
        for item in tts.list_preset_voices():
            ten = item[0] if isinstance(item, (list, tuple)) else item
            if ten and ten not in ds:
                ds.append(str(ten))
    except Exception:
        ds = []
    if not ds:
        ds = list(VIENEU_VOICES.keys())
    uu_tien = [VIENEU_VOICE_CHINH, VIENEU_VOICE_DU_PHONG]
    ds = [g for g in uu_tien if g in ds] + sorted(
        [g for g in ds if g not in uu_tien])
    return ds


def ten_hien_thi_giong(ten):
    """'Xuân Vĩnh' -> 'Xuân Vĩnh (Bắc, nam, Natural)' để hiện
    trong dropdown. Không có trong bảng 25 thì trả nguyên tên."""
    v = VIENEU_VOICES.get(ten)
    if not v:
        return ten
    return "%s (%s, %s, %s)" % (ten, v.get("region", "?"),
                                v.get("sex", "?"),
                                v.get("character", "?"))


def giong_tu_hien_thi(hien_thi):
    """'Xuân Vĩnh (Bắc, nam, Natural)' -> 'Xuân Vĩnh'."""
    if isinstance(hien_thi, str) and " (" in hien_thi:
        return hien_thi.split(" (", 1)[0].strip()
    return (hien_thi or "").strip()


def _slug_giong(ten):
    """'Ngọc Huyền' -> 'ngoc-huyen' (để khớp id 'vieneu:ngoc-huyen'
    mà tab Faceless/Doc phụ đề dùng)."""
    import unicodedata
    t = unicodedata.normalize("NFD", (ten or "").strip().lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("đ", "d").replace(" ", "-")
    return t


def giai_quyet_giong_vieneu(ten):
    """Tên giọng trong JSON/config -> (preset_thật, cảnh_báo).
    Alias cũ (Minh Quân) map sang Hải Đăng kèm cảnh báo.
    Nhận cả id 'vieneu:<slug>' (vd 'vieneu:ngoc-huyen').
    Tên lạ -> (None, thông báo lỗi rõ ràng) — KHÔNG tự ép về
    Xuân Vĩnh im lặng. LƯU Ý: chỉ gọi danh_sach_giong_vieneu()
    (khởi tạo Vieneu, nạp model) khi model ĐÃ tải — không thì
    dùng bảng fallback 25 preset, tránh tự tải model chỉ vì
    1 tên giọng lạ trong JSON."""
    t = (ten or "").strip()
    if not t:
        return None, "Chưa chọn giọng VieNeu."
    if t in VIENEU_ALIAS:
        moi = VIENEU_ALIAS[t]
        return moi, ("Giọng '%s' là tên cũ (SDK <=3.7.1) — đã map "
                     "sang '%s' (SDK 3.8.5)." % (t, moi))
    if t in VIENEU_VOICES:
        return t, ""
    ds = (danh_sach_giong_vieneu() if vieneu_model_da_tai()
          else list(VIENEU_VOICES.keys()))
    if t in ds:
        return t, ""
    if t.lower().startswith("vieneu:"):
        slug = t.split(":", 1)[1].strip().lower()
        for ten_preset in ds:
            if _slug_giong(ten_preset) == slug:
                return ten_preset, ""
    return None, ("Giọng '%s' không có trong VieNeu (SDK %s, %d "
                  "preset) — kiểm tra lại tên giọng trong JSON."
                  % (t, VIENEU_SDK_VERSION, len(ds)))

# Chuẩn voice xuất (giữ chuẩn đã chốt trong ChipChipStudio):
# MP3 44100 Hz, stereo, 192k, libmp3lame.
VOICE_MP3 = {"sample_rate": 44100, "channels": 2, "bitrate": "192k"}


def danh_sach_nhan_vat():
    """[(id, tên hiển thị)] cho combobox chọn nhân vật tham chiếu."""
    return [(c["id"], "%s (%s)" % (c["ten"], c["id"]))
            for c in CHARACTERS.values()]


def lay_nhan_vat(char_id):
    return lay_nhan_vat_hieu_luc(char_id)



# ------------------------------------------------------------------
# 1c. Thẻ tag nhân vật trong prompt — gõ @Tên là tool lấy đúng
# nhân vật đã lưu (bổ sung CYAN 21/11 ~21:33).
# Tag dùng chung nguồn tên với tab "Tạo nhân vật": gõ tên là khớp
# (theo trường "ten" của nhân vật đã lưu/khóa). Tag chưa có nhân
# vật thì BÁO RÕ, KHÔNG tự bịa. Khi gửi prompt cho Postman thì
# tool thay tag bằng mô tả nhân vật đã lưu TRƯỚC khi gửi.
# Draft v7.23 chưa có hệ thống tag nào (@ trong code cũ mới chỉ
# là @echo và cú pháp mảng PowerShell).
# ------------------------------------------------------------------
# Tên gọi khác của nhân vật khi gõ tag (vd CYAN gọi @Bà bán xôi
# nhưng tên lưu là "Bà Tư"). Tag khớp tên dài trước nên alias
# dài không bị tên ngắn hơn nuốt mất.
TAG_ALIAS = {
    "Bà bán xôi": "ba_ban_xoi",
    "Bà Tư": "ba_ban_xoi",
    "Cô Hạnh": "co_hanh",
}


def bang_tag_nhan_vat():
    """{tên hiển thị: id} — từ registry khóa + nhân vật đã lưu mới
    + alias. Gõ @Bà bán xôi, @Bà Tư đều ra ba_ban_xoi."""
    bang = dict(TAG_ALIAS)
    for cid, ten_hien in danh_sach_nhan_vat_day_du():
        c = lay_nhan_vat_hieu_luc(cid) or {}
        bang[c.get("ten") or ten_hien] = cid
    return bang


def tim_tag_trong_prompt(text):
    """Tìm @Tên trong prompt. Trả [(tên, id_or_None)] theo thứ tự
    xuất hiện. Tên dài khớp trước (vd 'Người Ấy' trước 'Ấy')."""
    bang = bang_tag_nhan_vat()
    ten_da_sap = sorted(bang.keys(), key=len, reverse=True)
    ket_qua = []
    if not text:
        return ket_qua
    # Quét thủ công để @Bà bán xôi (có khoảng trắng) vẫn khớp.
    i = 0
    while i < len(text):
        if text[i] == "@":
            khop = None
            for ten in ten_da_sap:
                if text[i + 1:i + 1 + len(ten)] == ten:
                    khop = ten
                    break
            if khop:
                ket_qua.append((khop, bang[khop]))
                i += 1 + len(khop)
                continue
            # @... không khớp tên nào: ghi lại tới khoảng trắng.
            j = i + 1
            while j < len(text) and text[j] not in " ,.;:\n\t":
                j += 1
            ket_qua.append((text[i + 1:j], None))
            i = j
            continue
        i += 1
    return ket_qua


def thay_tag_bang_mo_ta(text):
    """Thay @Tên bằng mô tả nhân vật đã lưu (để gửi cho Postman).
    Trả (text_moi, tag_la): tag_la = [tên chưa có nhân vật]."""
    bang = bang_tag_nhan_vat()
    tag_la = []
    out = text or ""
    for ten, cid in tim_tag_trong_prompt(text or ""):
        if cid is None:
            if ten and ten not in tag_la:
                tag_la.append(ten)
            continue
        c = lay_nhan_vat_hieu_luc(cid) or {}
        mo_ta = ("[Nhân vật: %s — %s, %s, màu khăn %s, "
                 "đồ cầm: %s, đầu tròn không mặt, chân 1 nét]"
                 % (c.get("ten") or cid, c.get("vai_tro") or "",
                    c.get("khan") or "", c.get("mau_khan") or "",
                    c.get("do_cam_mac_dinh") or ""))
        out = out.replace("@" + ten, mo_ta, 1)
    return out, tag_la

# ------------------------------------------------------------------
# 2. JSON kịch bản Postman — parse + SRT (đồng nhất voice <-> cảnh)
# ------------------------------------------------------------------
def _slug(text):
    t = unicodedata.normalize("NFKD", text or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^A-Za-z0-9\-_]+", "-", t).strip("-").lower()
    return t[:80] or "video"


def uoc_tinh_thoi_luong_giay(text, toc_do=0.95):
    """VI ~170 tiếng/phút (chuẩn skill 2d). Tốc độ 0,95x -> lâu hơn.
    Đây là ƯỚC TÍNH — thời lượng thật đo lại sau khi VieNeu đọc."""
    tu = len((text or "").split())
    if tu == 0:
        return 0.0
    return tu / 170.0 * 60.0 / max(0.5, float(toc_do or 0.95))


def build_srt_cues(scenes, toc_do=0.95, nghi_giua_cue_ms=5):
    """Tạo srt_cues từ narration: cue i <-> scene i, timing cộng dồn.
    start/end tính bằng giây, làm tròn 3 chữ số.
    (v7.31) Khoảng chờ giữa cue mặc định 5ms — CYAN chốt 22/11,
    thay 350ms chung trước đây (1 cue = 1 đoạn lời kể hoàn chỉnh)."""
    cues, t = [], 0.0
    for i, sc in enumerate(scenes, 1):
        text = (sc.get("narration") or sc.get("loi_ke") or "").strip()
        d = max(uoc_tinh_thoi_luong_giay(text, toc_do), 0.8)
        cues.append({
            "index": i,
            "scene_id": sc.get("id") or ("scene_%d" % i),
            "start": round(t, 3), "end": round(t + d, 3),
            "text": text,
            "speaker": "A",
            "character": (sc.get("characters") or ["cau_ay"])[0],
            "gender": "male",
        })
        t += d + nghi_giua_cue_ms / 1000.0
    return cues


# (v7.30) Nhịp nghỉ sau mỗi cue khi tự căn SRT theo voice thật
# (CYAN chốt 22/11 ~16:01, thay cho 350ms chung trước đây):
# dấu phẩy 100ms, dấu chấm 175ms, dấu hỏi 200ms.
NGHI_SAU_DAU_PHAY_GIAY = 0.100
NGHI_SAU_DAU_CHAM_GIAY = 0.175
NGHI_SAU_DAU_HOI_GIAY = 0.200
# Cue đọc dở câu (không có dấu câu cuối): nghỉ tối thiểu như dấu
# phẩy để không cắt đuôi giọng (đuôi MP3 có padding ~50ms).
NGHI_SAU_CAU_MAC_DINH_GIAY = 0.100


def _nghi_sau_cau_giay(text):
    """Nhịp nghỉ sau 1 cue, tính từ dấu câu cuối của lời kể:
    phẩy / hai chấm / chấm phẩy / gạch ngang -> 100ms; chấm /
    chấm than / ba chấm -> 175ms; hỏi -> 200ms; không có dấu
    cuối câu (đọc dở) -> 100ms."""
    t = (text or "").strip()
    if not t:
        return NGHI_SAU_CAU_MAC_DINH_GIAY
    cuoi = t[-1]
    if cuoi in (",", ":", ";", "—", "–"):
        return NGHI_SAU_DAU_PHAY_GIAY
    if cuoi in (".", "!", "…", "。"):
        return NGHI_SAU_DAU_CHAM_GIAY
    if cuoi == "?":
        return NGHI_SAU_DAU_HOI_GIAY
    return NGHI_SAU_CAU_MAC_DINH_GIAY


def retime_cues_theo_voice(scenes, cues_goc, nghi_giua_cue_ms=5):
    """Viết lại srt_cues theo thời lượng voice thật (đã đo bằng
    ffprobe, lưu ở scene["duration_s"]): cue nào kết thúc đúng lúc
    giọng đọc xong đoạn đó, cue tiếp theo bắt đầu sau đúng khoảng
    chờ nghi_giua_cue_ms (mặc định 5ms — CYAN chốt 22/11, lấy từ
    JSON voice.pause_between_cues_ms khi có).
    (v7.31) THAY ĐỔI CÓ CHỦ Ý so với v7.30: v7.30 dùng nhịp dấu câu
    cuối lời kể làm khoảng chờ (phẩy 100ms / chấm 175ms / hỏi
    200ms); từ v7.31 khoảng chờ giữa cue là 5ms CỐ ĐỊNH cho cả
    project — nhịp dấu câu chỉ còn là nhịp tự nhiên trong lúc
    VieNeu đọc cả cue 1 lần (1 cue = 1 đoạn hoàn chỉnh, không ngắt
    ở dấu chấm), tool không chèn im lặng trong cue.
    Mỗi cue ghi thêm "nghi_sau_giay" để bước nối voice.wav dùng
    đúng nhịp, khỏi lệch với mốc SRT. Trả (cues_moi, tong_giay)."""
    cues_that = []
    t = 0.0
    try:
        gap = max(float(nghi_giua_cue_ms or 5), 0.0) / 1000.0
    except Exception:
        gap = 0.005
    for i, sc in enumerate(scenes, 1):
        d = max(float(sc.get("duration_s") or 1.0), 0.8)
        cu0 = cues_goc[i - 1] if i - 1 < len(cues_goc) else {}
        text = sc.get("narration") or ""
        nghi = gap if i < len(scenes) else 0.0
        cues_that.append({
            "index": i, "scene_id": sc.get("id") or ("scene_%d" % i),
            "start": round(t, 3), "end": round(t + d, 3),
            "text": text,
            "speaker": cu0.get("speaker") or "A",
            "character": cu0.get("character") or (
                (sc.get("characters") or ["cau_ay"])[0]),
            "gender": cu0.get("gender") or "male",
            "nghi_sau_giay": round(nghi, 3),
        })
        t += d + nghi
    return cues_that, round(t, 3)


def _srt_time(sec):
    ms = int(round(float(sec) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def write_srt(cues, path):
    lines = []
    for c in cues:
        lines.append(str(c["index"]))
        lines.append("%s --> %s" % (_srt_time(c["start"]),
                                    _srt_time(c["end"])))
        lines.append(c["text"])
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


# ------------------------------------------------------------------
# 2c. SFX kèm kịch bản (v7.31, CYAN chốt 22/11)
# SFX chèn GIỮA CUE, đúng lúc lời đọc nhắc tới nó — vd cue 1 chuông
# báo thức reo ngay SAU cụm "sáu giờ bốn mươi", rồi giọng mới đọc
# tiếp "bạn thức dậy". TUYỆT ĐỐI KHÔNG chèn ở đầu cue, KHÔNG chèn
# ở khoảng chuyển cảnh (bản thử key1_voice_sfx.mp3 bên đoạn Lập kế
# hoạch chèn overlay ở đầu cue nên chuông reo ở giây 0 — SAI chỗ
# CYAN dặn, đừng lặp lại).
# VieNeu KHÔNG trả mốc từ (WordBoundary) nên mốc SFX giữa cue chỉ
# là ƯỚC TÍNH theo vị trí chữ (sai số ~0,3-0,5s) — UI + báo cáo
# phải ghi rõ, không được nói là đo chính xác từng từ.
# ------------------------------------------------------------------
SFX_AM_LUONG_MAC_DINH = 0.55
SFX_FILE_HO_TRO = (".mp3", ".wav", ".m4a", ".ogg", ".flac")
KHOANG_CHO_GIUA_CUE_MS_MAC_DINH = 5  # CYAN chốt 22/11
# Tên nhân vật trong JSON ShotBuilder -> id nhân vật Postman.
TEN_NHAN_VAT_SHOTBUILDER = {
    "Nam Đen": "cau_ay", "Cậu Ấy": "cau_ay", "Cau Ay": "cau_ay",
    "Him": "him", "Người Ấy": "nguoi_ay", "Nguoi Ay": "nguoi_ay",
    "Mẹ": "me", "Me": "me", "Minh": "minh",
    "Bà Tư": "ba_ban_xoi", "Ba Tu": "ba_ban_xoi",
    "Bà bán xôi": "ba_ban_xoi", "Ba ban xoi": "ba_ban_xoi",
    "Cô Hạnh": "co_hanh", "Co Hanh": "co_hanh",
}


def _chuan_hoa_chuoi_neo(s):
    """Chuẩn hóa để khớp cụm neo: lowercase + gộp khoảng trắng."""
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def chuan_hoa_sfx_canh(scene):
    """Chuẩn hóa SFX của 1 scene về list dict:
    {ten, file, neo_vao_cum, moc_giay, cach_chen ("chen"|"chong"),
     am_luong, thoi_luong_giay, nguon, thieu_file}.
    Ưu tiên: sfx_list (mới) > sfx_chuyen_canh (cũ, chỉ tên/mô tả)
    > sfx chuỗi (cũ). Trả (ds_sfx, canh_bao)."""
    ds, cb = [], []
    raw_list = scene.get("sfx_list")
    if isinstance(raw_list, list) and raw_list:
        for j, e in enumerate(raw_list, 1):
            if not isinstance(e, dict):
                cb.append("SFX #%d không phải object — bỏ qua." % j)
                continue
            ten = str(e.get("ten") or e.get("name")
                      or ("SFX %d" % j)).strip()
            cach = str(e.get("cach_chen") or "chen").strip().lower()
            if cach not in ("chen", "chong"):
                cb.append("SFX '%s': cách chèn '%s' không hiểu — "
                          "dùng 'chen'." % (ten, cach))
                cach = "chen"
            try:
                am = float(e.get("am_luong", SFX_AM_LUONG_MAC_DINH))
            except Exception:
                am = SFX_AM_LUONG_MAC_DINH
            am = max(0.0, min(1.0, am))
            moc = e.get("moc_giay")
            try:
                moc = float(moc) if moc is not None else None
            except Exception:
                moc = None
            tl = e.get("thoi_luong_giay")
            try:
                tl = float(tl) if tl is not None else None
            except Exception:
                tl = None
            ds.append({"ten": ten,
                       "file": str(e.get("file") or "").strip(),
                       "neo_vao_cum": str(
                           e.get("neo_vao_cum") or "").strip(),
                       "moc_giay": moc, "cach_chen": cach,
                       "am_luong": am, "thoi_luong_giay": tl,
                       "nguon": "sfx_list", "thieu_file": False})
        return ds, cb
    # Tương thích ngược: sfx_chuyen_canh cũ (chỉ tên/mô tả, không
    # có file) — coi là SFX thiếu file, báo rõ, không tự bịa audio.
    cc = scene.get("sfx_chuyen_canh")
    if isinstance(cc, dict) and (cc.get("ten") or "").strip():
        ten = str(cc["ten"]).strip()
        ds.append({"ten": ten, "file": "", "neo_vao_cum": "",
                   "moc_giay": None, "cach_chen": "chen",
                   "am_luong": SFX_AM_LUONG_MAC_DINH,
                   "thoi_luong_giay": None, "nguon": "sfx_chuyen_canh",
                   "thieu_file": True})
        cb.append("SFX '%s' chỉ có tên trong sfx_chuyen_canh, chưa "
                  "có file — thêm trường file vào sfx_list để chèn "
                  "được." % ten)
        return ds, cb
    # sfx chuỗi cũ (vd "nhạc nền nhẹ" / "không").
    s = scene.get("sfx")
    if isinstance(s, str) and s.strip() \
            and s.strip().lower() not in ("không", "khong", "none",
                                          "no", ""):
        ten = s.strip()
        ds.append({"ten": ten, "file": "", "neo_vao_cum": "",
                   "moc_giay": None, "cach_chen": "chong",
                   "am_luong": SFX_AM_LUONG_MAC_DINH,
                   "thoi_luong_giay": None, "nguon": "sfx",
                   "thieu_file": True})
        cb.append("SFX '%s' chỉ có tên (sfx chuỗi cũ), chưa có "
                  "file." % ten)
    return ds, cb


def tim_file_sfx(thu_muc_sfx, ten_file):
    """Tìm file SFX theo tên trong thư mục SFX (kèm thư mục con).
    Chấp nhận tên file trần, đường dẫn tương đối, hoặc đường dẫn
    tuyệt đối có thật. Trả đường dẫn đầy đủ hoặc None."""
    if not ten_file:
        return None
    if os.path.isabs(ten_file) and os.path.isfile(ten_file):
        return ten_file
    if not thu_muc_sfx or not os.path.isdir(thu_muc_sfx):
        return None
    p = os.path.join(thu_muc_sfx, ten_file)
    if os.path.isfile(p):
        return p
    base = os.path.basename(ten_file)
    for goc, _ds, files in os.walk(thu_muc_sfx):
        if base in files:
            return os.path.join(goc, base)
    return None


def dem_file_sfx(thu_muc_sfx):
    """Đếm file SFX (đuôi hỗ trợ) trong thư mục, để hiện trạng
    thái ở UI."""
    if not thu_muc_sfx or not os.path.isdir(thu_muc_sfx):
        return 0
    n = 0
    for _g, _d, files in os.walk(thu_muc_sfx):
        n += sum(1 for f in files
                 if f.lower().endswith(SFX_FILE_HO_TRO))
    return n


def _moc_tu_giay(moc_giay, thoi_luong_that, thoi_luong_uoc_tinh=None):
    """Mốc giây trong cue từ moc_giay có sẵn (co giãn theo tỉ lệ
    thật/ước tính khi có). Trả (moc_giay_final, cach_tinh)."""
    d = max(float(thoi_luong_that or 0), 0.0)
    try:
        m = float(moc_giay)
    except Exception:
        return 0.0, "mac_dinh_0"
    if thoi_luong_uoc_tinh:
        try:
            u = float(thoi_luong_uoc_tinh)
            if u > 0:
                m = m * d / u
        except Exception:
            pass
    return min(max(m, 0.0), d), "moc_giay"


def tinh_moc_neo_giay(text_cue, neo, moc_giay, thoi_luong_that,
                      thoi_luong_uoc_tinh=None):
    """Mốc SFX trong cue (giây).
    - Có cụm neo: mốc = (vị trí CUỐI cụm / độ dài cue) × thời lượng
      voice thật. Đây là ƯỚC TÍNH theo vị trí chữ (sai số
      ~0,3-0,5s) vì VieNeu không trả mốc từng từ.
    - Không thấy cụm: dùng moc_giay (co giãn thật/ước tính),
      không có nữa thì 0.0 + cảnh báo.
    Trả (moc_giay_final, cach_tinh, canh_bao); cach_tinh thuộc
    {"neo", "moc_giay", "mac_dinh_0"}."""
    d = max(float(thoi_luong_that or 0), 0.0)
    neo_norm = _chuan_hoa_chuoi_neo(neo)
    if neo_norm:
        text_norm = _chuan_hoa_chuoi_neo(text_cue)
        idx = text_norm.find(neo_norm)
        if idx >= 0 and len(text_norm) > 0:
            moc = (idx + len(neo_norm)) / float(len(text_norm)) * d
            return min(max(moc, 0.0), d), "neo", ""
        cb = "Không thấy cụm neo '%s' trong lời kể — " % neo
        if moc_giay is not None:
            m, _ct = _moc_tu_giay(moc_giay, d, thoi_luong_uoc_tinh)
            return m, "moc_giay", cb + "dùng mốc giây có sẵn."
        return 0.0, "mac_dinh_0", cb + "chèn ở đầu cue (0,0s)."
    if moc_giay is not None:
        m, _ct = _moc_tu_giay(moc_giay, d, thoi_luong_uoc_tinh)
        return m, "moc_giay", ""
    return 0.0, "mac_dinh_0", ("SFX không có cụm neo lẫn mốc giây — "
                               "chèn ở đầu cue (0,0s).")


def _chuan_hoa_mp3(duong_dan_vao, duong_dan_ra, am_luong=None):
    """Đổi 1 file audio bất kỳ về MP3 chuẩn 44100/stereo/192k
    (áp âm lượng nếu có). Trả True/False."""
    cmd = ["ffmpeg", "-y", "-i", duong_dan_vao]
    if am_luong is not None:
        try:
            cmd += ["-af", "volume=%.3f"
                    % max(0.0, min(1.0, float(am_luong)))]
        except Exception:
            pass
    cmd += ["-ar", "44100", "-ac", "2", "-b:a", "192k", duong_dan_ra]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                       **_chay_ngam_kwargs())
    return r.returncode == 0 and os.path.isfile(duong_dan_ra) \
        and os.path.getsize(duong_dan_ra) > 0


def _noi_mp3(danh_sach, out_path, tam_dir=None):
    """Nối nhiều MP3 thành 1 MP3 chuẩn 44100/stereo/192k (ffmpeg
    concat demuxer + re-encode). Bỏ qua file rỗng/không tồn tại.
    1 file thì chỉ chuẩn hóa. Trả True/False."""
    ds = [p for p in danh_sach
          if p and os.path.isfile(p) and os.path.getsize(p) > 0]
    if not ds:
        return False
    if len(ds) == 1:
        return _chuan_hoa_mp3(ds[0], out_path)
    lst = os.path.join(tam_dir or os.path.dirname(out_path) or ".",
                       "noi_mp3_%d.txt" % os.getpid())
    try:
        with open(lst, "w", encoding="utf-8") as f:
            for p in ds:
                f.write("file '%s'\n" % p.replace("'", "'\\''"))
        r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe",
                            "0", "-i", lst, "-ar", "44100", "-ac", "2",
                            "-b:a", "192k", out_path],
                           capture_output=True, text=True, timeout=600,
                           **_chay_ngam_kwargs())
        return r.returncode == 0 and os.path.isfile(out_path) \
            and os.path.getsize(out_path) > 0
    finally:
        try:
            os.remove(lst)
        except Exception:
            pass


def _cat_voice_chen_sfx(voice_mp3, sfx_mp3, moc_giay, d_voice,
                        out_path, tam_dir):
    """Chèn SFX vào giữa voice: [voice :moc][SFX][voice moc:].
    Giọng dừng trong lúc SFX reo rồi đọc tiếp; thời lượng cue tăng
    thêm đúng thời lượng SFX. Trả True/False."""
    if moc_giay <= 0.05:
        return _noi_mp3([sfx_mp3, voice_mp3], out_path, tam_dir)
    if moc_giay >= max(float(d_voice or 0) - 0.05, 0.0):
        return _noi_mp3([voice_mp3, sfx_mp3], out_path, tam_dir)
    p1 = os.path.join(tam_dir, "chen_p1.mp3")
    p2 = os.path.join(tam_dir, "chen_p2.mp3")
    r1 = subprocess.run(["ffmpeg", "-y", "-i", voice_mp3,
                         "-t", "%.3f" % moc_giay,
                         "-ar", "44100", "-ac", "2", "-b:a", "192k",
                         p1], capture_output=True, text=True,
                        timeout=120, **_chay_ngam_kwargs())
    r2 = subprocess.run(["ffmpeg", "-y", "-ss", "%.3f" % moc_giay,
                         "-i", voice_mp3,
                         "-ar", "44100", "-ac", "2", "-b:a", "192k",
                         p2], capture_output=True, text=True,
                        timeout=120, **_chay_ngam_kwargs())
    if r1.returncode != 0 or r2.returncode != 0:
        return False
    return _noi_mp3([p1, sfx_mp3, p2], out_path, tam_dir)


def _chong_sfx_len_voice(voice_mp3, sfx_mp3, moc_giay, am_luong,
                         out_path):
    """Trộn SFX đè lên voice tại mốc neo (amix, giọng đọc tiếp
    không dừng). Thời lượng ra = thời lượng voice. Trả True/False."""
    try:
        am = max(0.0, min(1.0, float(am_luong)))
    except Exception:
        am = SFX_AM_LUONG_MAC_DINH
    ms = int(round(float(moc_giay or 0) * 1000))
    fc = ("[1:a]adelay=%d|%d,volume=%.3f[sfx];"
          "[0:a][sfx]amix=inputs=2:duration=first:normalize=0[out]"
          % (ms, ms, am))
    r = subprocess.run(["ffmpeg", "-y", "-i", voice_mp3, "-i", sfx_mp3,
                        "-filter_complex", fc, "-map", "[out]",
                        "-ar", "44100", "-ac", "2", "-b:a", "192k",
                        out_path],
                       capture_output=True, text=True, timeout=300,
                       **_chay_ngam_kwargs())
    return r.returncode == 0 and os.path.isfile(out_path) \
        and os.path.getsize(out_path) > 0


def chen_sfx_vao_cue(voice_mp3, text_cue, ds_sfx, thu_muc_sfx,
                     out_path, log_cb=None, thoi_luong_uoc_tinh=None):
    """Chèn SFX vào 1 file voice cue theo sfx_list đã chuẩn hóa.
    Xử lý theo mốc neo tăng dần, cộng dồn độ dời (chen chèn thêm
    thời lượng sau mốc) để mốc sau không lệch. Trả (ok,
    duong_dan_ra, bao_cao, thieu): bao_cao = list dict {ten, file,
    moc_giay_trong_cue, cach_chen, am_luong, thoi_luong_giay,
    trang_thai ("da_chen"/"thieu_file"/"loi_chen"/"loi_chuyen_doi")};
    thieu = list tên SFX thiếu file/lỗi (để báo cáo cuối)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    bao_cao, thieu = [], []
    if not ds_sfx:
        return True, voice_mp3, bao_cao, thieu
    d_that = _do_dai_audio_giay(voice_mp3)
    if not d_that:
        return False, voice_mp3, bao_cao, thieu
    # Giải quyết file + mốc neo cho từng SFX.
    muc = []
    for e in ds_sfx:
        duong = tim_file_sfx(thu_muc_sfx, e.get("file") or "")
        if not duong:
            thieu.append(e.get("ten") or "SFX")
            bao_cao.append(dict(e, moc_giay_trong_cue=None,
                                thoi_luong_giay=None,
                                trang_thai="thieu_file"))
            continue
        moc, _ct, cb = tinh_moc_neo_giay(
            text_cue, e.get("neo_vao_cum") or "", e.get("moc_giay"),
            d_that, thoi_luong_uoc_tinh)
        if cb:
            _log("CẢNH BÁO SFX '%s': %s" % (e.get("ten"), cb))
        muc.append((moc, e, duong))
    if not muc:
        return True, voice_mp3, bao_cao, thieu
    # Mốc tăng dần + cộng dồn độ dời do "chen" chèn thêm.
    muc.sort(key=lambda x: x[0])
    hien_tai = voice_mp3
    d_hien_tai = d_that
    doi = 0.0
    dich_tam = None
    try:
        dich_tam = tempfile.mkdtemp(prefix="postman-sfx-")
        for moc, e, duong in muc:
            moc_hieu_luc = min(max(moc + doi, 0.0), d_hien_tai)
            # Chuẩn hóa SFX về MP3 44100/stereo/192k. "chen" áp âm
            # lượng luôn lúc chuẩn hóa (SFX reo 1 mình); "chong"
            # áp trong amix (không áp 2 lần).
            sfx_mp3 = os.path.join(
                dich_tam, "sfx_%s.mp3" % _slug(e.get("ten") or "sfx"))
            am_chuan = (e.get("am_luong") if e.get("cach_chen") == "chen"
                        else None)
            if not _chuan_hoa_mp3(duong, sfx_mp3, am_chuan):
                _log("CẢNH BÁO SFX '%s': không đổi được file %s "
                     "sang MP3 — bỏ qua." % (e.get("ten"), duong))
                bao_cao.append(dict(e, moc_giay_trong_cue=None,
                                    thoi_luong_giay=None,
                                    trang_thai="loi_chuyen_doi"))
                thieu.append(e.get("ten") or "SFX")
                continue
            d_sfx = _do_dai_audio_giay(sfx_mp3) or 0.0
            tam_ra = os.path.join(dich_tam, "cue_sfx.mp3")
            if e.get("cach_chen") == "chong":
                ok = _chong_sfx_len_voice(hien_tai, sfx_mp3,
                                          moc_hieu_luc,
                                          e.get("am_luong"), tam_ra)
            else:
                ok = _cat_voice_chen_sfx(hien_tai, sfx_mp3,
                                         moc_hieu_luc, d_hien_tai,
                                         tam_ra, dich_tam)
            if not ok:
                _log("CẢNH BÁO SFX '%s': chèn lỗi — bỏ qua."
                     % e.get("ten"))
                bao_cao.append(dict(e, moc_giay_trong_cue=None,
                                    thoi_luong_giay=None,
                                    trang_thai="loi_chen"))
                thieu.append(e.get("ten") or "SFX")
                continue
            moi = os.path.join(dich_tam, "cue_hien_tai.mp3")
            shutil.copyfile(tam_ra, moi)
            hien_tai = moi
            if e.get("cach_chen") == "chen":
                doi += d_sfx
                d_hien_tai += d_sfx
            bao_cao.append(dict(
                e, moc_giay_trong_cue=round(moc_hieu_luc, 3),
                thoi_luong_giay=round(d_sfx, 3),
                trang_thai="da_chen"))
        if hien_tai != voice_mp3:
            if not _chuan_hoa_mp3(hien_tai, out_path):
                return False, voice_mp3, bao_cao, thieu
            return True, out_path, bao_cao, thieu
        return True, voice_mp3, bao_cao, thieu
    finally:
        if dich_tam:
            shutil.rmtree(dich_tam, ignore_errors=True)


def _slug_ten_file(du_lieu):
    """Tên file xuất voice+SFX: slug(title/key) hoặc 'postman'."""
    ten = (du_lieu.get("title") or du_lieu.get("key") or "postman")
    return _slug(str(ten)) or "postman"


def xu_ly_sfx_sau_voice(du_lieu, outdir, cue_files, log_cb=None,
                        thu_muc_sfx=None, chen_sfx=True,
                        tu_can_srt=True):
    """Giai đoạn SFX sau khi đã có voice từng cue (dùng chung cho
    nút 'Tạo voice' và 'Dựng video'):
    - chen_sfx BẬT + có SFX + tự căn BẬT: chèn SFX vào từng cue MP3
      (neo giữa cue), đo lại thời lượng thật, căn SRT (khoảng chờ
      5ms), xuất <slug>_voice-sfx.mp3/.srt/.json.
    - TẮT tự căn: giữ mốc SRT ước tính, KHÔNG chèn SFX theo mốc
      thật (báo rõ).
    - Thư mục SFX chưa chọn mà JSON có SFX: báo rõ, bỏ qua SFX,
      vẫn căn SRT + dựng tiếp bằng voice thường (UI chặn trước khi
      chạy; đây là lưới an toàn cho hàm gọi trực tiếp).
    Trả (ok, ket_qua, loi): ket_qua = {cue_files, cues_that,
    bao_cao_sfx, sfx_thieu, sfx_bo_qua, voice_sfx_mp3,
    voice_sfx_srt, postman_sfx_json}."""
    def _log(s):
        if log_cb:
            log_cb(s)
    scenes = du_lieu.get("scenes") or []
    cues_goc = du_lieu.get("srt_cues") or []
    gap_ms = du_lieu.get("khoang_cho_giua_cue_ms",
                         KHOANG_CHO_GIUA_CUE_MS_MAC_DINH)
    ket_qua = {"cue_files": list(cue_files), "cues_that": cues_goc,
               "bao_cao_sfx": [], "sfx_thieu": [], "sfx_bo_qua": "",
               "voice_sfx_mp3": None, "voice_sfx_srt": None,
               "postman_sfx_json": None}
    if not tu_can_srt:
        ket_qua["sfx_bo_qua"] = ("Tắt tự căn SRT: giữ nguyên mốc SRT "
                                 "ước tính cũ, không chèn SFX theo "
                                 "mốc thật.")
        _log(ket_qua["sfx_bo_qua"])
        return True, ket_qua, ""
    # Chuẩn hóa SFX từng cảnh (kèm cảnh báo field cũ thiếu file).
    ds_theo_canh = []
    co_sfx = False
    for sc in scenes:
        ds, cb = chuan_hoa_sfx_canh(sc)
        sc["sfx_list"] = ds
        for c in cb:
            _log("CẢNH BÁO SFX cảnh %s: %s" % (sc.get("id"), c))
        if ds:
            co_sfx = True
        ds_theo_canh.append(ds)
    if chen_sfx and co_sfx:
        thu_muc = (thu_muc_sfx or du_lieu.get("thu_muc_sfx") or "")
        if not thu_muc or not os.path.isdir(thu_muc):
            ket_qua["sfx_bo_qua"] = ("Chưa chọn thư mục SFX — chọn "
                                     "thư mục SFX rồi chạy lại, lần "
                                     "này dựng bằng voice thường "
                                     "(không SFX).")
            _log("SFX: " + ket_qua["sfx_bo_qua"])
        else:
            cue_files_moi = []
            bao_cao_all, thieu_all = [], []
            for i, sc in enumerate(scenes, 1):
                mp3 = cue_files[i - 1] if i - 1 < len(cue_files) \
                    else None
                ds = ds_theo_canh[i - 1]
                if not mp3 or not ds:
                    cue_files_moi.append(mp3)
                    continue
                uoc = None
                if i - 1 < len(cues_goc):
                    try:
                        uoc = float(cues_goc[i - 1].get("end", 0)) \
                            - float(cues_goc[i - 1].get("start", 0))
                    except Exception:
                        uoc = None
                ra = os.path.join(outdir, "cue_%02d_sfx.mp3" % i)
                ok, moi, bc, th = chen_sfx_vao_cue(
                    mp3, sc.get("narration") or "", ds, thu_muc, ra,
                    _log, thoi_luong_uoc_tinh=uoc)
                if not ok:
                    _log("CẢNH BÁO SFX cảnh %s: chèn lỗi (%s) — "
                         "giữ voice thường." % (sc.get("id"), moi))
                    cue_files_moi.append(mp3)
                    continue
                for b in bc:
                    b["cue"] = i
                    b["scene_id"] = sc.get("id")
                bao_cao_all.extend(bc)
                thieu_all.extend(th)
                cue_files_moi.append(moi)
                d_moi = _do_dai_audio_giay(moi)
                if d_moi:
                    sc["duration_s"] = round(d_moi, 2)
            ket_qua["cue_files"] = cue_files_moi
            ket_qua["bao_cao_sfx"] = bao_cao_all
            ket_qua["sfx_thieu"] = thieu_all
    # Căn lại SRT theo thời lượng thật (khoảng chờ 5ms) + ghi mốc
    # tuyệt đối từng SFX để bên dựng video khớp hình đúng mốc.
    cues_that, tong = retime_cues_theo_voice(
        scenes, cues_goc, gap_ms)
    du_lieu["srt_cues"] = cues_that
    du_lieu["tong_thoi_luong_that_giay"] = tong
    ket_qua["cues_that"] = cues_that
    da_chen = [b for b in ket_qua["bao_cao_sfx"]
               if b.get("trang_thai") == "da_chen"
               and b.get("moc_giay_trong_cue") is not None]
    for b in da_chen:
        i = int(b.get("cue") or 1)
        bat_dau = cues_that[i - 1]["start"] if i - 1 < len(cues_that) \
            else 0.0
        b["sfx_moc_giay"] = round(
            bat_dau + float(b["moc_giay_trong_cue"]), 3)
        b["sfx_ket_thuc_giay"] = round(
            b["sfx_moc_giay"] + float(b.get("thoi_luong_giay") or 0),
            3)
        # Ghi mốc tuyệt đối vào sfx_list của cảnh (JSON xuất ra).
        for e in scenes[i - 1].get("sfx_list") or []:
            if e.get("ten") == b.get("ten"):
                e["sfx_moc_giay"] = b["sfx_moc_giay"]
                e["sfx_ket_thuc_giay"] = b["sfx_ket_thuc_giay"]
    du_lieu["bao_cao_sfx"] = ket_qua["bao_cao_sfx"]
    du_lieu["sfx_thieu"] = ket_qua["sfx_thieu"]
    if da_chen:
        slug = _slug_ten_file(du_lieu)
        # Gộp voice+SFX: nối cue (đã chèn SFX) + im lặng 5ms.
        ds_noi, loi_noi = _danh_sach_noi_voice(
            outdir, ket_qua["cue_files"], cues_that)
        if ds_noi is None:
            _log("CẢNH BÁO: không gộp được file voice+SFX: %s"
                 % loi_noi)
        else:
            mp3_ra = os.path.join(outdir, "%s_voice-sfx.mp3" % slug)
            if _noi_mp3(ds_noi, mp3_ra, outdir):
                ket_qua["voice_sfx_mp3"] = mp3_ra
                srt_ra = os.path.join(outdir, "%s_voice-sfx.srt"
                                      % slug)
                write_srt(cues_that, srt_ra)
                ket_qua["voice_sfx_srt"] = srt_ra
                json_ra = os.path.join(outdir, "%s_postman_sfx.json"
                                       % slug)
                try:
                    with open(json_ra, "w",
                              encoding="utf-8") as f:
                        json.dump(du_lieu, f, ensure_ascii=False,
                                  indent=1)
                    ket_qua["postman_sfx_json"] = json_ra
                except Exception as e:
                    _log("CẢNH BÁO: không ghi được JSON SFX: %s" % e)
                _log("Đã xuất voice+SFX: %d SFX đã chèn, tổng %.1fs "
                     "(khoảng chờ giữa cue 5ms)."
                     % (len(da_chen), tong))
            else:
                _log("CẢNH BÁO: gộp file voice+SFX lỗi — vẫn giữ "
                     "từng file cue riêng.")
    if ket_qua["sfx_thieu"]:
        _log("SFX thiếu file (%d): %s — đã bỏ qua, chạy tiếp."
             % (len(ket_qua["sfx_thieu"]),
                ", ".join(sorted(set(ket_qua["sfx_thieu"])))))
    return True, ket_qua, ""


def parse_postman_json(noi_dung):
    """Dán 1 JSON -> tự nhận scenes + SRT. Chấp nhận:
    - {"postman": {...}} / {"scenes": [...]} / {"canh": [...]}
    - bare list scenes / {"vi": {"srt_cues": [...]}} (tương thích
      JSON Voice Faceless cũ: lấy srt_cues làm scenes).
    Trả (du_lieu, loi): du_lieu = dict đã chuẩn hóa, loi = "" nếu ok.
    Chuẩn hóa mỗi scene về: id, narration, image_prompt,
    motion_prompt {en, vi}, prompt_video_postman, characters [id],
    props {char_id: đồ cầm}, number {value, character_id},
    setting, camera, duration_s (ước tính).
    """
    try:
        raw = json.loads(noi_dung) if isinstance(noi_dung, str) else noi_dung
    except Exception as e:
        return None, "JSON lỗi: %s" % e
    if isinstance(raw, list):
        raw = {"scenes": raw}
    if not isinstance(raw, dict):
        return None, "JSON phải là object hoặc list các cảnh."
    # Tương thích JSON Voice Faceless cũ: {vi: {srt_cues: [...]}}.
    scenes_raw = None
    for key in ("scenes", "canh", "canh_nho", "shots"):
        if raw.get(key):
            scenes_raw = raw[key]
            break
    if scenes_raw is None and raw.get("postman", {}).get("scenes"):
        scenes_raw = raw["postman"]["scenes"]
    if scenes_raw is None:
        for lang in ("vi", "en"):
            ban = raw.get(lang) or {}
            if ban.get("srt_cues"):
                scenes_raw = [{
                    "id": "scene_%d" % c.get("index", i + 1),
                    "narration": c.get("text", ""),
                } for i, c in enumerate(ban["srt_cues"])]
                break
    if not scenes_raw:
        return None, ("JSON không có scenes nào — cần trường 'scenes' "
                      "là list các cảnh (xem mẫu POSTMAN_KEY1_CANH1.json).")
    meta = raw.get("postman") or raw.get("meta") or {}
    # (v7.31) JSON ShotBuilder dùng khóa "voice" (không phải
    # "voice_settings"): engine/voice/voice_du_phong/speed/
    # pause_between_cues_ms.
    voice = (raw.get("voice_settings") or meta.get("voice_settings")
             or raw.get("voice") or {})
    toc_do = float(voice.get("speed") or meta.get("toc_do") or 0.95)
    toc_do = max(0.5, min(1.35, toc_do))
    try:
        khoang_cho_ms = int(voice.get("pause_between_cues_ms",
                                      KHOANG_CHO_GIUA_CUE_MS_MAC_DINH))
    except Exception:
        khoang_cho_ms = KHOANG_CHO_GIUA_CUE_MS_MAC_DINH
    khoang_cho_ms = max(0, min(5000, khoang_cho_ms))
    giong = (voice.get("voice") or voice.get("voice_vi")
            or voice.get("voice_id") or VIENEU_VOICE_CHINH)
    # (v7.24-merge) Ten day du "Xuân Vĩnh (VieNeu, nam Bắc)" trong
    # SCRIPT_CANH1_POSTMAN.json -> boc ve ten preset goc "Xuân Vĩnh".
    if isinstance(giong, str) and " (" in giong:
        giong = giong.split(" (", 1)[0].strip()
    # Giọng chính + giọng dự phòng: giải quyết qua bảng 25 preset
    # (kèm alias tên cũ). Tên lạ -> báo rõ, KHÔNG tự ép im lặng.
    giong, canh_bao_giong = giai_quyet_giong_vieneu(giong)
    if not giong:
        canh_bao_giong = (canh_bao_giong + " Dùng tạm %s."
                          % VIENEU_VOICE_CHINH)
        giong = VIENEU_VOICE_CHINH
    giong_du_phong = (voice.get("voice_du_phong")
                      or voice.get("backup_voice")
                      or voice.get("voice_backup")
                      or VIENEU_VOICE_DU_PHONG)
    if isinstance(giong_du_phong, str) and " (" in giong_du_phong:
        giong_du_phong = giong_du_phong.split(" (", 1)[0].strip()
    giong_du_phong, cb_dp = giai_quyet_giong_vieneu(giong_du_phong)
    if not giong_du_phong:
        if cb_dp:
            canh_bao_giong = ((canh_bao_giong + " " + cb_dp).strip()
                              + " Dùng tạm %s." % VIENEU_VOICE_DU_PHONG)
        giong_du_phong = VIENEU_VOICE_DU_PHONG
    elif cb_dp:
        canh_bao_giong = (canh_bao_giong + " " + cb_dp).strip()
    scenes, loi = [], []
    for i, s in enumerate(scenes_raw, 1):
        if not isinstance(s, dict):
            loi.append("Cảnh %d không phải object — bỏ qua." % i)
            continue
        sid = str(s.get("id") or s.get("stt")
                  or ("scene_%d" % i))
        # (v7.31) JSON ShotBuilder: lời kể ở "line", nhân vật ở
        # "actors" (chuỗi "Nam Đen, Mẹ"), thời lượng ước tính ở
        # "duration_s".
        narration = (s.get("narration") or s.get("loi_ke")
                     or s.get("line") or s.get("text") or "").strip()
        chars = s.get("characters") or s.get("nhan_vat")
        if not chars and s.get("actors"):
            chars = []
            for _ten in str(s.get("actors")).split(","):
                _ten = _ten.strip()
                if not _ten:
                    continue
                chars.append(TEN_NHAN_VAT_SHOTBUILDER.get(_ten, _ten))
        if not chars:
            chars = ["cau_ay"]
        try:
            _dur = float(s.get("duration_s") or 0)
        except Exception:
            _dur = 0
        if _dur <= 0:
            _dur = uoc_tinh_thoi_luong_giay(narration, toc_do)
        if isinstance(chars, str):
            chars = [chars]
        chars_hop_le, chars_la = [], []
        for ch in chars:
            if lay_nhan_vat(ch):
                chars_hop_le.append(ch)
            else:
                chars_la.append(ch)
        if chars_la:
            loi.append("Cảnh %s: nhân vật chưa có trong registry: %s"
                       % (sid, ", ".join(chars_la)))
        if not chars_hop_le:
            chars_hop_le = ["cau_ay"]
        # (v7.24-merge) Field tieng Viet cua SCRIPT_CANH1_POSTMAN.json.
        _img = s.get("image_prompt") or s.get("prompt_anh") or ""
        motion = s.get("motion_prompt") or {}
        if isinstance(motion, str):
            motion = {"en": motion, "vi": motion}
        if not motion:
            motion = {"en": s.get("prompt_chuyen_dong_en") or "",
                      "vi": s.get("prompt_chuyen_dong_vi") or ""}
        _tags = tim_tag_trong_prompt(
            (s.get("prompt_video_postman") or "")
            + " " + _img)
        _tag_la = [ten for ten, cid in _tags if cid is None]
        if _tag_la:
            loi.append("Cảnh %s: tag chưa có nhân vật: %s — "
                       "tạo nhân vật ở tab 'Tạo nhân vật' trước, "
                       "không tự bịa." % (sid, ", ".join(
                           "@" + x for x in _tag_la)))
        _prompt_exp, _ = thay_tag_bang_mo_ta(
            s.get("prompt_video_postman") or s.get("prompt_video") or "")
        scenes.append({
            "id": sid,
            "tags": [{"ten": ten, "id": cid} for ten, cid in _tags],
            "prompt_video_postman_expanded": _prompt_exp,
            "title": s.get("title") or s.get("ten") or sid,
            "narration": narration,
            "image_prompt": _img,
            # prompt_video_postman: ô điền riêng từng cảnh — nếu JSON
            # chưa có thì tự điền = image_prompt + motion_prompt (EN).
            "prompt_video_postman": (
                s.get("prompt_video_postman")
                or s.get("prompt_video")
                or ((_img)
                    + (" Motion: " + motion.get("en", "")
                       if motion.get("en") else ""))),
            "motion_prompt": {"en": motion.get("en", ""),
                              "vi": motion.get("vi", "")},
            "characters": chars_hop_le,
            "props": s.get("props") or s.get("do_cam") or {},
            # so_tren_dau dang {"me": 312} / {"minh": 89, "ba_ban_xoi": 41}:
            # render_scene_image da ho tro number[character_id].
            "number": s.get("number") or s.get("so_tren_dau") or {},
            "setting": s.get("setting") or s.get("boi_canh") or "",
            "camera": s.get("camera") or s.get("goc_may") or "",
            "duration_s": round(_dur, 2),
        })
        # (v7.31) SFX của cảnh: chuẩn hóa sfx_list (mới) hoặc field
        # cũ (sfx_chuyen_canh / sfx chuỗi) — cảnh báo field cũ thiếu
        # file để CYAN thêm file vào sfx_list.
        _ds_sfx, _cb_sfx = chuan_hoa_sfx_canh(s)
        scenes[-1]["sfx_list"] = _ds_sfx
        for _c in _cb_sfx:
            loi.append("Cảnh %s (SFX): %s" % (sid, _c))
    if not scenes:
        return None, "Không có cảnh hợp lệ nào trong JSON."
    # SRT có mốc giây từ JSON (CYAN chốt 21/11 ~22:28): đoạn thoại
    # nào cũng có start/end kèm theo — tool lấy mốc đó làm chuẩn,
    # KHÔNG ước tính lại từ độ dài chữ. Chỉ khi JSON không có
    # srt_cues hợp lệ mới ước tính bằng build_srt_cues().
    cues_json, co_moc_that = _srt_cues_tu_json(raw, scenes, toc_do)
    if co_moc_that:
        for _sc, _cu in zip(scenes, cues_json):
            _sc["duration_s"] = round(max(_cu["end"] - _cu["start"],
                                          0.8), 2)
    du_lieu = {
        "format": "postman2d",
        "version": VERSION_POSTMAN,
        "title": (meta.get("title") or raw.get("title")
                  or raw.get("title_vi") or ""),
        "title_en": meta.get("title_en") or raw.get("title_en") or "",
        "key": meta.get("key") or raw.get("key") or "",
        "voice_settings": {
            "engine": "vieneu",
            "voice": giong,
            "voice_goc": giong,
            "voice_du_phong": giong_du_phong,
            "speed": toc_do, "pitch": int(voice.get("pitch") or 0),
        },
        # (v7.31) Khoảng chờ giữa cue (ms) + thư mục SFX + cờ chèn
        # SFX — đọc từ JSON khi có, lưu theo dự án.
        "khoang_cho_giua_cue_ms": khoang_cho_ms,
        "thu_muc_sfx": (raw.get("thu_muc_sfx")
                        or meta.get("thu_muc_sfx") or ""),
        "chen_sfx_theo_json": bool(raw.get("chen_sfx_theo_json",
                                           meta.get("chen_sfx_theo_json",
                                                    True))),
        "scenes": scenes,
        "srt_cues": cues_json,
        "srt_tu_json": co_moc_that,
        "canh_bao": [c for c in [canh_bao_giong] if c] + loi,
        "tong_thoi_luong_uoc_tinh_giay": round(
            sum(s["duration_s"] for s in scenes)
            + (khoang_cho_ms / 1000.0) * max(0, len(scenes) - 1), 2),
    }
    return du_lieu, ""


def _srt_giay(v):
    """Đọc mốc giây từ số (start_s/end_s) hoặc chuỗi SRT
    "HH:MM:SS,mmm" / "MM:SS.mmm". Trả float hoặc None."""
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        pass
    try:
        s = str(v).strip().replace(",", ".")
        parts = s.split(":")
        if len(parts) == 3:
            h, m, sec = parts
            return int(h) * 3600 + int(m) * 60 + float(sec)
        if len(parts) == 2:
            m, sec = parts
            return int(m) * 60 + float(sec)
    except Exception:
        pass
    return None


def _srt_cues_tu_json(raw, scenes, toc_do=0.95):
    """Lấy srt_cues kèm mốc giây trong JSON (raw['srt_cues'] hoặc
    trong postman/meta/voice_settings). Trả (cues, co_moc_that):
    co_moc_that=True khi JSON có đủ cue hợp lệ (start/end số,
    end>start, khớp số cảnh) — lúc đó tool dùng mốc này làm chuẩn.
    Không có -> build_srt_cues() ước tính, co_moc_that=False."""
    nguon = None
    for noi in (raw, raw.get("postman") or {}, raw.get("meta") or {},
                raw.get("voice_settings") or {}):
        if isinstance(noi, dict) and isinstance(noi.get("srt_cues"), list):
            nguon = noi["srt_cues"]
            break
    if not nguon or len(nguon) < len(scenes):
        return build_srt_cues(scenes, toc_do), False
    cues = []
    for i, (sc, cu) in enumerate(zip(scenes, nguon), 1):
        if not isinstance(cu, dict):
            return build_srt_cues(scenes, toc_do), False
        # (v7.31) JSON ShotBuilder: mốc ở start_s/end_s (số) hoặc
        # chuỗi "HH:MM:SS,mmm" — không chỉ float(start/end).
        st = _srt_giay(cu.get("start_s") if cu.get("start_s") is not None
                       else cu.get("start"))
        en = _srt_giay(cu.get("end_s") if cu.get("end_s") is not None
                       else cu.get("end"))
        if st is None or en is None:
            return build_srt_cues(scenes, toc_do), False
        if en <= st or st < 0:
            return build_srt_cues(scenes, toc_do), False
        cues.append({
            "index": int(cu.get("index") or i),
            "scene_id": sc.get("id") or ("scene_%d" % i),
            "start": round(st, 3), "end": round(en, 3),
            "text": (cu.get("text") or sc.get("narration") or ""),
            "speaker": cu.get("speaker") or "A",
            "character": (cu.get("character")
                          or (sc.get("characters") or ["cau_ay"])[0]),
            "gender": cu.get("gender") or "male",
        })
    return cues, True


def them_canh(scenes, sau_id=None):
    """Nút '+ Thêm cảnh': thêm 1 scene rỗng (mặc định Cậu Ấy).
    Trả list scenes mới (không sửa list gốc)."""
    moi = list(scenes or [])
    n = len(moi) + 1
    scene_moi = {
        "id": "scene_%d" % n, "title": "Cảnh mới %d" % n,
        "narration": "", "image_prompt": "",
        "prompt_video_postman": "", "motion_prompt": {"en": "", "vi": ""},
        "characters": ["cau_ay"], "props": {}, "number": {},
        "setting": "", "camera": "", "duration_s": 0.0,
    }
    if sau_id:
        for i, s in enumerate(moi):
            if s.get("id") == sau_id:
                moi.insert(i + 1, scene_moi)
                break
        else:
            moi.append(scene_moi)
    else:
        moi.append(scene_moi)
    # Đánh lại id trùng (nếu có) để cue <-> scene không lệch.
    thay = set()
    for s in moi:
        while s["id"] in thay:
            s["id"] = s["id"] + "_b"
        thay.add(s["id"])
    return moi


# ------------------------------------------------------------------
# 3. VieNeu — kiểm tra / tải tài nguyên / đọc voice
# ------------------------------------------------------------------
def vieneu_model_da_tai():
    """Model VieNeu v3 Turbo đã tải về máy chưa? Kiểm tra NHẸ
    qua HF cache (models--pnnbao-ump--VieNeu-TTS-v3-Turbo có
    model.safetensors hoặc file .onnx) — KHÔNG khởi tạo Vieneu()
    (init sẽ nạp model vào RAM, chậm), KHÔNG tải gì. Dùng để
    quyết định dropdown giọng có liệt kê đủ 25 preset hay chỉ
    hiện 'ấn Tải tài nguyên trước' (mục C)."""
    goc_cache = os.environ.get("HF_HOME") or os.path.join(
        os.path.expanduser("~"), ".cache", "huggingface", "hub")
    thu_muc = os.path.join(
        goc_cache, "models--pnnbao-ump--VieNeu-TTS-v3-Turbo")
    try:
        for root, _ds, files in os.walk(thu_muc):
            if "model.safetensors" in files:
                return True
            if any(f.endswith(".onnx") for f in files):
                return True
    except Exception:
        return False
    return False


def kiem_tra_vieneu():
    """Trả dict: installed, version, voices (nếu import được),
    loi. Không tải gì ở bước này."""
    try:
        import vieneu  # noqa: F401
        ver = getattr(vieneu, "__version__", "?")
    except Exception as e:
        return {"installed": False, "version": None, "voices": [],
                "loi": "Chưa cài vieneu: %s" % e}
    try:
        from vieneu import Vieneu
        tts = Vieneu()
        voices = [v[0] for v in tts.list_preset_voices()]
        return {"installed": True, "version": str(ver), "voices": voices,
                "loi": "",
                "co_xuan_vinh": "Xuân Vĩnh" in voices,
                "co_pham_tuyen": "Phạm Tuyên" in voices}
    except Exception as e:
        # Import được nhưng khởi tạo lỗi (thường là chưa tải model) —
        # vẫn tính là "đã cài, chưa có model".
        return {"installed": True, "version": str(ver), "voices": [],
                "loi": "Đã cài vieneu nhưng chưa khởi tạo được "
                       "(thường là chưa tải model): %s" % e}


def _vieneu_khoi_tao_lan_dau(log_cb=None):
    """Khởi tạo Vieneu() lần đầu (SDK tự tải model nếu chưa có).
    Trả (ok, thong_bao) — dùng chung cho cả 2 đường: exe bundling
    (frozen) và pip install (chạy .py dev)."""
    try:
        from vieneu import Vieneu
        tts = Vieneu()  # lần đầu: tải model từ HuggingFace
        voices = [v[0] for v in tts.list_preset_voices()]
        ok_xv = "Xuân Vĩnh" in voices
        ok_pt = "Phạm Tuyên" in voices
        return True, ("Đã tải xong VieNeu. Giọng có sẵn: %d giọng. "
                      "Xuân Vĩnh: %s. Phạm Tuyên: %s."
                      % (len(voices), "có" if ok_xv else "KHÔNG CÓ",
                         "có" if ok_pt else "KHÔNG CÓ"))
    except Exception as e:
        return False, "Đã có gói VieNeu nhưng tải model lỗi: %s" % e


def tai_tai_nguyen_vieneu(log_cb=None):
    """Nút 'Tải tài nguyên' trong tab Postman 2D.
    (v7.26) Bản exe đóng gói (frozen): KHÔNG pip install vieneu nữa
    — exe không thấy site-packages của Python hệ thống nên pip cài
    xong tool vẫn import lỗi 'No module named vieneu'; gói vieneu
    phải BUNDLING trong exe (workflow: vieneu==3.8.5 +
    --collect-all vieneu). Chỉ thử import trong tiến trình + khởi
    tạo model lần đầu (SDK tự tải model nếu chưa có); import lỗi
    thì báo cập nhật tool, KHÔNG báo lỗi mạng, KHÔNG chạy pip.
    Chạy .py (dev): 1) pip install vieneu (SDK 3.8.5 đã pin,
    torch-free CPU/ONNX mặc định); 2) Vieneu() lần đầu để SDK tải
    model từ HuggingFace (pnnbao-ump/VieNeu-TTS-v3-Turbo) — đo dung
    lượng thư mục cache trước/sau và log con số thật, KHÔNG đoán
    trước. Trả (ok, thong_bao). Chạy thread nền trong UI
    (không block)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    if getattr(sys, "frozen", False):
        _log("Đang kiểm tra gói VieNeu kèm trong tool...")
        try:
            import importlib
            importlib.import_module("vieneu")
        except Exception:
            return False, ("Bản tool này chưa kèm gói VieNeu — cập nhật "
                           "tool lên bản mới nhất (VieNeu sẽ kèm trong "
                           "bản cài).")
        return _vieneu_khoi_tao_lan_dau(log_cb)
    # (v7.25) Đã đóng gói thì sys.executable là exe của tool, KHÔNG
    # phải Python — dùng _python_he_thong(), không có thì báo rõ.
    python = _python_he_thong()
    if not python:
        return False, THIEU_PYTHON_THAT
    try:
        r = subprocess.run(
            [python, "-m", "pip", "install",
             "vieneu==%s" % VIENEU_SDK_VERSION],
            capture_output=True, text=True, timeout=1800,
            **_chay_ngam_kwargs())
        if r.returncode != 0:
            out_gop = (r.stderr or "") + (r.stdout or "")
            if _loi_thieu_python_that(out_gop):
                return False, THIEU_PYTHON_THAT
            return False, ("pip install vieneu lỗi: %s"
                           % out_gop[-500:])
        _log("Đã cài vieneu %s. Đang tải model VieNeu lần đầu..."
             % VIENEU_SDK_VERSION)
    except Exception as e:
        if _loi_thieu_python_that(e):
            return False, THIEU_PYTHON_THAT
        return False, "pip install vieneu lỗi: %s" % e
    return _vieneu_khoi_tao_lan_dau(log_cb)


def _ffmpeg_co_san():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True,
                       timeout=10, **_chay_ngam_kwargs())
        return True
    except Exception:
        return False


def doc_voice_vieneu(text, voice=VIENEU_VOICE_CHINH, toc_do=0.95,
                     duong_dan_ra=None, log_cb=None,
                     giong_du_phong=VIENEU_VOICE_DU_PHONG):
    """Đọc 1 cue bằng VieNeu -> MP3 chuẩn 44100/stereo/192k.
    VieNeu không có tham số tốc độ — tốc độ 0,95x làm bằng
    ffmpeg atempo=0.95 (giữ nguyên cao độ), giống cách tab SRT
    Reader đã làm. Fallback: giọng dự phòng (mặc định Phạm Tuyên,
    đổi được qua giong_du_phong) nếu giọng chính lỗi; nếu cả 2 lỗi
    thì trả lỗi (KHÔNG tự đổi sang HoaiMy/Edge im lặng — UI phải
    log rõ). Tên giọng lạ (không có trong 25 preset) thì báo rõ
    ngay, không tự ép về Xuân Vĩnh.
    Trả (ok, duong_dan_mp3, loi)."""
    if not text or not text.strip():
        return False, None, "Text rỗng."
    giong_chinh, cb = giai_quyet_giong_vieneu(voice)
    if not giong_chinh:
        return False, None, cb
    if cb and log_cb:
        log_cb("CẢNH BÁO giọng: " + cb)
    giong_phong, cb2 = giai_quyet_giong_vieneu(giong_du_phong)
    if not giong_phong:
        giong_phong = VIENEU_VOICE_DU_PHONG
    if not duong_dan_ra:
        import tempfile
        duong_dan_ra = os.path.join(tempfile.gettempdir(),
                                    "postman-voice.mp3")
    for thu, giong in enumerate([giong_chinh, giong_phong]):
        if thu > 0 and giong == giong_chinh:
            continue
        try:
            from vieneu import Vieneu
            tts = Vieneu()
            audio = tts.infer(text, voice=giong)
            wav_tam = duong_dan_ra + ".tam.wav"
            tts.save(audio, wav_tam)  # 48 kHz wav (v3 Turbo)
            if not _ffmpeg_co_san():
                return False, None, ("Không tìm thấy ffmpeg — "
                                     "cần ffmpeg để đổi sang MP3 chuẩn.")
            # atempo 0.95x + chuẩn MP3 44100/stereo/192k.
            cmd = ["ffmpeg", "-y", "-i", wav_tam,
                   "-af", "atempo=%.3f" % float(toc_do),
                   "-ar", "44100", "-ac", "2", "-b:a", "192k",
                   duong_dan_ra]
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=300, **_chay_ngam_kwargs())
            try:
                os.remove(wav_tam)
            except Exception:
                pass
            if r.returncode == 0 and os.path.isfile(duong_dan_ra):
                if log_cb and thu > 0:
                    log_cb("Giọng %s lỗi — đã fallback sang %s."
                           % (giong_chinh, giong))
                return True, duong_dan_ra, ""
            if log_cb:
                log_cb("Giọng %s lỗi khi encode MP3 — thử giọng dự phòng."
                       % giong)
        except Exception as e:
            if log_cb:
                log_cb("Giọng %s lỗi: %s" % (giong, e))
            continue
    return False, None, ("VieNeu lỗi cả giọng chính (%s) và dự phòng "
                         "(%s) — kiểm tra model đã tải chưa (nút "
                         "'Tải tài nguyên')." % (giong_chinh, giong_phong))


# ------------------------------------------------------------------
# 4. Renderer Postman 2D — vẽ bằng code (Pillow + ffmpeg)
# ------------------------------------------------------------------
# Phong cách khóa: nét mảnh 2D, đầu tròn KHÔNG mặt, chân 1 nét,
# tay đơn giản không ngón, màu giới hạn đen/trắng + màu khăn.
# Số: khung NHỎ, bay lơ lửng phía TRÊN đầu, cách đầu một khoảng
# rõ (KHÔNG chạm đầu, KHÔNG đè lên đầu).
INK = (24, 22, 27)
WHITE = (255, 255, 255)
BG_SETS = {
    "bedroom": (245, 240, 228), "phong_ngu": (245, 240, 228),
    "canteen": (250, 244, 224), "cang_tin": (250, 244, 224),
    "library": (238, 232, 214), "thu_vien": (238, 232, 214),
    "hallway": (240, 238, 232), "hanh_lang": (240, 238, 232),
    "schoolyard": (235, 242, 228), "san_truong": (235, 242, 228),
    "classroom": (242, 238, 226), "lop_hoc": (242, 238, 226),
    "home_kitchen": (248, 242, 230), "bep": (248, 242, 230),
    "gate": (238, 240, 235), "cong_truong": (238, 240, 235),
    "": (255, 255, 255),
}


def _hex_to_rgb(h):
    h = (h or "#1a1a1a").lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _ve_nhan_vat(draw, char_id, x, y_dat, cao, pose="stand",
                 prop=None, number=None, glow=False):
    """Vẽ 1 nhân vật que bằng code. (x, y_dat) = điểm chạm đất
    giữa 2 chân, cao = chiều cao px từ chân tới đỉnh đầu.
    pose: stand | sit | lie | walk | think | wave | hold.
    number: số đếm ngược (int/str) -> khung NHỎ phía trên đầu,
    cách đầu 18% chiều cao đầu, KHÔNG chạm đầu."""
    from PIL import ImageDraw  # noqa: F401  (giữ import cục bộ cho test)
    c = lay_nhan_vat(char_id) or CHARACTERS["cau_ay"]
    R = cao * float(c.get("ti_le_dau") or 0.22)  # bán kính đầu
    dau_y = y_dat - cao + R
    if pose == "lie":
        # Nằm trên giường: đầu hạ xuống gần mặt giường (không
        # ở độ cao đứng), thân ngang sang phải.
        dau_y = y_dat - int(R * 1.3)
    # --- hào quang (Người Ấy) ---
    if glow or c.get("hao_quang"):
        for r, a in ((R * 2.2, 30), (R * 1.8, 45), (R * 1.5, 60)):
            draw.ellipse([x - r, dau_y - r, x + r, dau_y + r],
                         outline=(240, 200, 90), width=3)
    # --- đầu tròn, KHÔNG mặt ---
    draw.ellipse([x - R, dau_y - R, x + R, dau_y + R],
                 outline=INK, width=5, fill=WHITE)
    # --- khăn ---
    khan = _hex_to_rgb(c["mau_khan"])
    co_y = dau_y + R
    if char_id == "cau_ay":
        # Khăn quàng đỏ thắt nơ: nơ nhỏ ở cổ.
        draw.ellipse([x - R * 0.45, co_y - 4, x + R * 0.45, co_y + 14],
                     fill=khan)
        draw.polygon([(x, co_y + 6), (x - R * 0.5, co_y + 34),
                      (x + R * 0.5, co_y + 34)], fill=khan)
    else:
        # Khăn len quấn cổ thả xuống 2 bên (Him / Người Ấy / phụ).
        draw.rectangle([x - R * 0.7, co_y - 4, x + R * 0.7, co_y + 16],
                       fill=khan)
        draw.rectangle([x - R * 0.55, co_y + 12, x - R * 0.15,
                        co_y + R * 1.5], fill=khan)
        draw.rectangle([x + R * 0.15, co_y + 12, x + R * 0.55,
                        co_y + R * 1.5], fill=khan)
    # --- thân: 1 nét dọc ---
    than_top = co_y + R * 0.9
    chan_top = y_dat - cao * 0.28
    if pose == "lie":
        # Nằm: đầu ở trái (đã vẽ ở trên, dịch sang trái), thân
        # ngang ở giữa, chân duỗi ngang sang phải, sát mặt giường.
        # (Đầu đã vẽ tại (x, dau_y) — dịch lại bằng cách vẽ thêm
        # thân nối từ đầu sang phải; không vẽ thân dọc.)
        giuong_y = y_dat - R * 0.5
        draw.line([(x, dau_y + R * 0.5), (x + cao * 0.45, giuong_y)],
                  fill=INK, width=5)
        draw.line([(x + cao * 0.45, giuong_y),
                   (x + cao * 0.62, giuong_y)], fill=INK, width=5)
        draw.line([(x + cao * 0.45, giuong_y),
                   (x + cao * 0.60, giuong_y + R * 0.35)],
                  fill=INK, width=5)
        # Số (nếu có) vẫn vẽ phía trên đầu như thường.
        if number is not None and str(number) != "":
            txt = str(number)
            khoang_cach = int(R * 0.45)
            khung_w, khung_h = max(54, len(txt) * 26 + 18), 40
            kx0 = x - khung_w // 2
            ky1 = dau_y - R - khoang_cach
            ky0 = ky1 - khung_h
            draw.rectangle([kx0, ky0, kx0 + khung_w, ky1],
                           outline=(193, 39, 45), width=3, fill=WHITE)
            try:
                from PIL import ImageFont
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
            except Exception:
                font = None
            draw.text((x, (ky0 + ky1) // 2), txt, fill=(193, 39, 45),
                      font=font, anchor="mm")
        return
    draw.line([(x, than_top), (x, chan_top)], fill=INK, width=6)
    # --- tay: 1 nét mỗi bên, không ngón ---
    if pose in ("hold", "sit"):
        # Ôm đồ trước ngực.
        draw.line([(x, than_top + 10), (x + R * 0.7, than_top + R * 0.9)],
                  fill=INK, width=5)
        draw.line([(x, than_top + 10), (x - R * 0.7, than_top + R * 0.9)],
                  fill=INK, width=5)
    elif pose == "wave":
        draw.line([(x, than_top + 10), (x + R * 0.8, than_top - R * 0.6)],
                  fill=INK, width=5)
        draw.line([(x, than_top + 10), (x - R * 0.6, than_top + R * 0.8)],
                  fill=INK, width=5)
    elif pose == "think":
        draw.line([(x, than_top + 10), (x + R * 0.5, dau_y + R * 0.4)],
                  fill=INK, width=5)
        draw.line([(x, than_top + 10), (x - R * 0.6, than_top + R * 0.8)],
                  fill=INK, width=5)
    else:  # stand / walk
        draw.line([(x, than_top + 10), (x + R * 0.65, than_top + R * 0.9)],
                  fill=INK, width=5)
        draw.line([(x, than_top + 10), (x - R * 0.65, than_top + R * 0.9)],
                  fill=INK, width=5)
    # --- chân: 1 NÉT mỗi chân, không khoảng trống trong chân ---
    if pose == "sit":
        draw.line([(x, chan_top), (x + R * 0.7, y_dat)], fill=INK, width=5)
        draw.line([(x, chan_top), (x + R * 0.5, y_dat)], fill=INK, width=5)
    elif pose == "walk":
        draw.line([(x, chan_top), (x + R * 0.55, y_dat)], fill=INK, width=5)
        draw.line([(x, chan_top), (x - R * 0.55, y_dat - R * 0.3)],
                  fill=INK, width=5)
    else:
        draw.line([(x, chan_top), (x + R * 0.28, y_dat)], fill=INK, width=5)
        draw.line([(x, chan_top), (x - R * 0.28, y_dat)], fill=INK, width=5)
    # --- đồ cầm (prop) — vẽ đơn giản ở tay ---
    if prop:
        px, py = x + R * 0.75, than_top + R * 0.95
        draw.rectangle([px - 14, py - 10, px + 14, py + 10],
                       outline=INK, width=3, fill=WHITE)
    # --- số đếm ngược: khung NHỎ phía TRÊN đầu, CÁCH đầu rõ ---
    if number is not None and str(number) != "":
        txt = str(number)
        khoang_cach = int(R * 0.45)  # khoảng trống giữa đầu và khung
        khung_w, khung_h = max(54, len(txt) * 26 + 18), 40
        kx0 = x - khung_w // 2
        ky1 = dau_y - R - khoang_cach
        ky0 = ky1 - khung_h
        draw.rectangle([kx0, ky0, kx0 + khung_w, ky1],
                       outline=(193, 39, 45), width=3, fill=WHITE)
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
        except Exception:
            font = None
        draw.text((x, (ky0 + ky1) // 2), txt, fill=(193, 39, 45),
                  font=font, anchor="mm")


def _camera(motion_en, t_frac):
    """Chuyển động camera từ motion_prompt (EN): chỉ lia/zoom NHẸ,
    nhân vật giữ nguyên tư thế (đúng luật Ảnh + lời kể).
    Trả (scale, dx, dy) áp lên frame gốc."""
    m = (motion_en or "").lower()
    if "zoom out" in m or "pull back" in m or "pulls back" in m:
        scale = 1.08 - 0.08 * t_frac
    elif "zoom" in m or "push" in m or "pushes in" in m:
        scale = 1.0 + 0.08 * t_frac
    else:
        scale = 1.02
    if "pan" in m or "pan shot" in m:
        dx = (t_frac - 0.5) * 40
    else:
        dx = 0.0
    dy = -6 * t_frac if "tilt down" in m else 0.0
    return scale, dx, dy


def render_scene_image(scene, rong=1280, cao=720, out_path=None):
    """Vẽ 1 frame tĩnh cho 1 cảnh (để xem trước / sheet).
    Trả đường dẫn file PNG."""
    from PIL import Image, ImageDraw
    bg = BG_SETS.get((scene.get("setting") or "").lower(),
                     (255, 255, 255))
    img = Image.new("RGB", (rong, cao), bg)
    draw = ImageDraw.Draw(img)
    # Nền đơn giản theo setting: đường chân trời + sàn.
    draw.rectangle([0, cao - 90, rong, cao], fill=(235, 232, 224))
    draw.line([(0, cao - 90), (rong, cao - 90)], fill=INK, width=3)
    if "lying in bed" in (scene.get("image_prompt") or ""):
        # Giường: khung chữ nhật dưới nhân vật nằm (bên trái).
        bx0, bx1 = int(rong * 0.08), int(rong * 0.48)
        by0 = cao - 90 - int(cao * 0.16)
        draw.rectangle([bx0, by0, bx1, cao - 90], outline=INK, width=4,
                       fill=(250, 246, 236))
        draw.rectangle([bx0, by0 - 26, bx0 + 90, by0],
                       outline=INK, width=3, fill=WHITE)  # gối
    chars = scene.get("characters") or ["cau_ay"]
    props = scene.get("props") or {}
    number = scene.get("number") or {}
    poses = scene.get("poses") or {}
    prompt = scene.get("image_prompt") or ""
    n = len(chars)
    for i, cid in enumerate(chars):
        x = int(rong * (0.5 if n == 1 else 0.32 + 0.36 * i / max(1, n - 1)))
        h = int(cao * 0.52)
        # Số: ưu tiên number.numbers = [{character_id, value}]
        # (1 cảnh có thể có 2 số, vd 1.2: Minh 89, Bà Tư 41),
        # rồi mới tới number[character_id] == nhân vật này.
        num = None
        if isinstance(number, dict):
            for _it in (number.get("numbers") or []):
                if isinstance(_it, dict) and _it.get("character_id") == cid:
                    num = _it.get("value")
                    break
            if num is None:
                if number.get("character_id") == cid:
                    num = number.get("value")
                elif cid in number:
                    num = number.get(cid)
                elif n == 1:
                    num = number.get("value")
        elif number:
            num = number
        # Pose theo TỪNG nhân vật (không áp 1 pose cho cả cảnh):
        # vd 1.1 chỉ Cậu Ấy nằm, Mẹ đứng ở cửa.
        if cid in poses:
            pose = poses[cid]
        elif cid == "cau_ay" and "lying in bed" in prompt:
            pose = "lie"
        elif "sitting" in prompt:
            pose = "sit"
        elif cid == "nguoi_ay":
            pose = "hold"
        else:
            pose = "stand"
        _ve_nhan_vat(draw, cid, x, cao - 90, h, pose=pose,
                     prop=props.get(cid), number=num,
                     glow=(cid == "nguoi_ay"))
    if out_path:
        img.save(out_path)
    return out_path, img


def render_scene_video(scene, voice_mp3=None, out_path=None,
                       rong=1280, cao=720, fps=30):
    """Dựng MP4 1 cảnh: ảnh tĩnh + Ken Burns nhẹ (theo motion),
    ghép voice của đúng cue đó (đồng nhất voice <-> cảnh).
    Cần ffmpeg. Trả (ok, duong_dan, loi)."""
    import tempfile
    from PIL import Image
    if not _ffmpeg_co_san():
        return False, None, "Không tìm thấy ffmpeg."
    dur = max(1.0, float(scene.get("duration_s") or 5.0))
    tmpdir = tempfile.mkdtemp(prefix="postman-scene-")
    _, img = render_scene_image(scene, rong, cao)
    n_frames = int(dur * fps)
    motion = (scene.get("motion_prompt") or {}).get("en", "")
    for f in range(n_frames):
        scale, dx, dy = _camera(motion, f / max(1, n_frames - 1))
        w2, h2 = int(rong * scale), int(cao * scale)
        fr = img.resize((w2, h2), Image.LANCZOS)
        left = max(0, (w2 - rong) // 2 + int(dx))
        top = max(0, (h2 - cao) // 2 + int(dy))
        fr = fr.crop((left, top, left + rong, top + cao))
        fr.save(os.path.join(tmpdir, "f%05d.png" % f))
    if not out_path:
        out_path = os.path.join(tmpdir, "scene.mp4")
    video_tam = os.path.join(tmpdir, "silent.mp4")
    r = subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(fps), "-i",
         os.path.join(tmpdir, "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
         video_tam], capture_output=True, text=True, timeout=900,
        **_chay_ngam_kwargs())
    if r.returncode != 0:
        return False, None, "ffmpeg render lỗi: %s" % r.stderr[-400:]
    if voice_mp3 and os.path.isfile(voice_mp3):
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", video_tam, "-i", voice_mp3,
             "-c:v", "copy", "-c:a", "aac", "-shortest", out_path],
            capture_output=True, text=True, timeout=300,
            **_chay_ngam_kwargs())
        if r.returncode != 0:
            return False, None, "ffmpeg ghép voice lỗi: %s" % r.stderr[-400:]
    else:
        import shutil
        shutil.copy(video_tam, out_path)
    return True, out_path, ""


def viet_words_json(cues):
    """Timeline từng từ cho engine H2/skia: mỗi cue chia đều các
    từ trong khoảng [start, end] của nó (mốc từng từ ước tính
    theo số từ — engine H2 dùng prep_voice.py đo lại bằng khoảng
    lặng khi có voice thật; skia dùng ASR khi có model).
    Trả list [{w, t, e}] — khớp định dạng timeline/words.json
    của kit H2. Dùng khi không chạy được prep_voice/ASR."""
    words = []
    for cu in (cues or []):
        text = (cu.get("text") or "").strip()
        st, en = float(cu.get("start") or 0), float(cu.get("end") or 0)
        if not text or en <= st:
            continue
        ds_tu = text.split()
        if not ds_tu:
            continue
        moi_tu = (en - st) / len(ds_tu)
        t = st
        for w in ds_tu:
            words.append({"w": w, "t": round(t, 3),
                          "e": round(t + moi_tu, 3)})
            t += moi_tu
    return words


def render_project(du_lieu, outdir, rong=1280, cao=720, log_cb=None,
                   model_ve="pillow", phong_cach="nhan_vat_khoa",
                   tu_can_srt_theo_voice=True, thu_muc_sfx=None,
                   chen_sfx=True):
    """Dựng cả project: voice trước (từng cảnh 1 MP3), rồi mới
    dựng video DỰA TRÊN file voice đó — thời lượng cảnh lấy theo
    file voice thật (ffprobe) + mốc SRT, KHÔNG ước tính từ chữ.
    (v7.31) Sau voice: chèn SFX vào từng cue (neo giữa cue) rồi
    mới dựng video; video dùng file cue đã chèn SFX.
    model_ve: "pillow" (mặc định, renderer tối giản) | "skia"
    | "h2". Model H2/skia thiếu tài nguyên thì BÁO LỖI RÕ (bấm
    Tải tài nguyên), KHÔNG tự render sai bằng Pillow im lặng.
    Trả (ok, {final_mp4, srt, scenes_mp4, voice_sfx_mp3,
    voice_sfx_srt, postman_sfx_json, bao_cao_sfx, sfx_thieu},
    loi)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    scenes = du_lieu.get("scenes") or []
    if not scenes:
        return False, {}, "Không có cảnh nào."
    os.makedirs(outdir, exist_ok=True)
    voice = du_lieu["voice_settings"]
    toc_do = voice.get("speed") or 0.95
    cues = (du_lieu.get("srt_cues")
            or build_srt_cues(scenes, toc_do))
    write_srt(cues, os.path.join(outdir, "postman.srt"))
    # --- GIAI ĐOẠN 1: tạo giọng VieNeu cho TỪNG CẢNH trước ---
    cue_files = []
    for i, sc in enumerate(scenes, 1):
        _log("Cảnh %d/%d (%s): đang đọc voice %s..."
             % (i, len(scenes), sc["id"], voice["voice"]))
        cue_mp3 = os.path.join(outdir, "cue_%02d.mp3" % i)
        ok, _, loi = doc_voice_vieneu(
            sc["narration"], voice["voice"], toc_do, cue_mp3, _log,
            giong_du_phong=voice.get("voice_du_phong")
            or VIENEU_VOICE_DU_PHONG)
        if not ok:
            return False, {}, "Cảnh %s đọc voice lỗi: %s" % (sc["id"], loi)
        # Thời lượng thật: đo file voice vừa tạo (ffprobe), KHÔNG
        # dùng ước tính từ độ dài chữ nữa.
        d_that = _do_dai_audio_giay(cue_mp3)
        if d_that:
            sc["duration_s"] = round(d_that, 2)
            _log("Cảnh %s: voice thật %.2fs (ước tính %.2fs)."
                 % (sc["id"], d_that,
                    float(cues[i - 1].get("end", 0))
                    - float(cues[i - 1].get("start", 0))
                    if i - 1 < len(cues) else 0))
        cue_files.append(cue_mp3)
    # (v7.31) SFX + tự căn lại SRT theo voice thật (mặc định BẬT):
    # chèn SFX vào từng cue (neo giữa cue), đo lại, căn SRT với
    # khoảng chờ 5ms (CYAN chốt 22/11), xuất voice+SFX. TẮT thì
    # giữ nguyên SRT ước tính cũ (postman.srt đã ghi ở đầu hàm)
    # và không chèn SFX theo mốc thật.
    _ok_sfx, kq_sfx, _loi_sfx = xu_ly_sfx_sau_voice(
        du_lieu, outdir, cue_files, _log, thu_muc_sfx, chen_sfx,
        tu_can_srt_theo_voice)
    cues_that = kq_sfx["cues_that"]
    cue_files = kq_sfx["cue_files"]
    if tu_can_srt_theo_voice:
        tong_that = du_lieu.get("tong_thoi_luong_that_giay", 0)
        write_srt(cues_that, os.path.join(outdir, "postman.srt"))
        _log("Đã căn lại SRT theo voice thật: %d cue, tổng %.1fs "
             "(khoảng chờ giữa cue 5ms — CYAN chốt 22/11)."
             % (len(scenes), tong_that))
    else:
        _log("Tắt tự căn SRT: giữ nguyên mốc SRT ước tính cũ.")
    _log("Đã tạo xong voice %d cảnh." % len(scenes))
    # --- GIAI ĐOẠN 2: dựng video theo model đã chọn ---
    model_ve = (model_ve or "pillow").strip().lower()
    if model_ve == "h2":
        return render_bang_h2(du_lieu, outdir, cue_files, cues_that,
                              phong_cach, rong, cao, log_cb)
    if model_ve == "skia":
        return render_bang_skia(du_lieu, outdir, cue_files, cues_that,
                                rong, cao, log_cb)
    if model_ve != "pillow":
        return False, {}, ("Model vẽ '%s' không hỗ trợ — chọn Pillow, "
                           "Skia 2D hoặc H2." % model_ve)
    mp4s = []
    for i, sc in enumerate(scenes, 1):
        _log("Cảnh %d/%d: đang vẽ + dựng video (Pillow)..."
             % (i, len(scenes)))
        mp4 = os.path.join(outdir, "scene_%02d.mp4" % i)
        ok, _, loi = render_scene_video(sc, cue_files[i - 1], mp4,
                                        rong, cao)
        if not ok:
            return False, {}, "Cảnh %s dựng video lỗi: %s" % (sc["id"], loi)
        mp4s.append(mp4)
    # Nối các cảnh bằng ffmpeg concat.
    lst = os.path.join(outdir, "concat.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for p in mp4s:
            f.write("file '%s'\n" % p.replace("'", "'\\''"))
    final = os.path.join(outdir, "postman-final.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", final],
                       capture_output=True, text=True, timeout=600,
                       **_chay_ngam_kwargs())
    if r.returncode != 0:
        return False, {}, "Nối cảnh lỗi: %s" % r.stderr[-400:]
    return True, {"final_mp4": final,
                  "srt": os.path.join(outdir, "postman.srt"),
                  "scenes_mp4": mp4s,
                  "voice_sfx_mp3": kq_sfx.get("voice_sfx_mp3"),
                  "voice_sfx_srt": kq_sfx.get("voice_sfx_srt"),
                  "postman_sfx_json": kq_sfx.get("postman_sfx_json"),
                  "bao_cao_sfx": kq_sfx.get("bao_cao_sfx") or [],
                  "sfx_thieu": kq_sfx.get("sfx_thieu") or [],
                  "sfx_bo_qua": kq_sfx.get("sfx_bo_qua") or ""}, ""



# ------------------------------------------------------------------
# 4b. Tab "Tạo nhân vật" (bổ sung CYAN 21/11 ~21:33)
# Nhập/chỉnh thông số code của nhân vật (đầu tròn không mặt, khăn,
# màu, tay chân 1 nét, tỉ lệ, nét mảnh), khung xem trước cập nhật
# ngay khi sửa thông số, lưu nhân vật theo tên để tab Postman 2D
# chỉ cần gọi tên ra dùng. Dùng chung cách vẽ Stickman bằng code
# với tab Postman 2D và chung 1 chỗ lưu (nhan_vat_postman.json).
# ------------------------------------------------------------------
KHAN_LUA_CHON = [
    "khăn quàng đỏ thắt nơ (kiểu học sinh VN)",
    "khăn len xám quấn cổ thả xuống 2 bên (KHÔNG thắt nơ)",
    "khăn len xanh navy đậm quấn cổ thả xuống",
    "khăn quàng xanh lá",
    "khăn nâu",
    "khăn tím",
    "tạp dề",
    "không khăn",
]


# ------------------------------------------------------------------
# 3b. Model vẽ + engine H2/Skia (mục D + E, CYAN 21/11 ~21:33).
# Nguồn gốc file: ~/workspace/gop-video-bilibili/plugin-goc/
#   2d-long-form-src/ (skia, skill 2d), h2-doi-thuong/,
#   h2-khoa-hoc/, h2-tinh-cam/ (3 plugin H2, skill cyan-2d).
# ĐÃ ĐỐI CHIẾU 21/11 ~23:24: render.mjs, engine/, tools/,
# audio/ BYTE-IDENTICAL giữa 3 plugin H2 (diff -r không khác
# gì) — chỉ packs/* khác nhau (nguoi.js/templates.js/pack.js).
# Vì vậy kit H2 dùng 1 bản engine duy nhất (lấy từ h2-doi-thuong)
# + 3 pack gốc + pack thứ 4 "nhanvatkhoa" (bible/template riêng
# cho nhân vật đã khóa của CYAN — KHÔNG dùng nguoi.js 3 pack).
# H2/skia KHÔNG bundle vào exe: nằm ở thư mục tài nguyên riêng
# (kiểu mục "Tài nguyên AI"), kiểm tra + nút tải/cài, đường dẫn
# lưu vào config, gọi node render.mjs bằng subprocess ẩn console.
# File .plugin gốc và giấy phép h2dev.ai KHÔNG đưa vào release.
# ĐÁNH GIÁ skia vs H2 (bằng chứng): skia draw_char vẽ puppet
# thân đầy (áo/tóc/râu/kính, KHÔNG có tham số khăn) — không vẽ
# được stickman nét mảnh + khăn là dấu nhận diện của CYAN; H2
# pack 4 vẽ được đúng kiểu (nguoi.js riêng, nét mảnh, khăn đỏ/
# navy/xám, đầu tròn không mặt, hào quang Người Ấy). Kết luận:
# H2 là model mặc định cho kênh này; skia chỉ là lựa chọn phụ
# khi CYAN muốn kiểu puppet đầy.
# ------------------------------------------------------------------
MODEL_VE = {"pillow": "Pillow (xem nhanh)",
            "skia": "Skia 2D",
            "h2": "H2 (Node + Chromium)"}
PHONG_CACH_H2 = {"nhan_vat_khoa": "Nhân vật đã khóa",
                 "chip": "Chíp Siêu Năng",
                 "nguech": "Nguệch Ngoạc",
                 "giaosu": "Giáo Sư Bút"}


def duong_dan_plugin_goc():
    """Thư mục plugin-goc cạnh postman2d.py (file gốc CYAN gửi)."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "plugin-goc")


def duong_dan_h2():
    """Thư mục làm việc H2 (riêng, không trong exe)."""
    return os.environ.get("H2_2D_STUDIO_DIR") or os.path.join(
        os.path.expanduser("~"), "h2-2d-studio")


def duong_dan_skia():
    """Thư mục làm việc skia (riêng, không trong exe)."""
    return os.environ.get("SKIA_2D_STUDIO_DIR") or os.path.join(
        os.path.expanduser("~"), "skia-2d-studio")


def kiem_tra_tai_nguyen_ve():
    """Kiểm tra tài nguyên từng model vẽ.
    Trả {model: {"co_san": bool, "chi_tiet": str, "thieu": [str]}}.
    Pillow: PIL import được. H2: kit/render.mjs + node + playwright
    + chromium + ffmpeg. Skia: engine + import skia được."""
    kq = {}
    try:
        import PIL  # noqa: F401
        kq["pillow"] = {"co_san": True,
                        "chi_tiet": "Pillow có sẵn (xem nhanh).",
                        "thieu": []}
    except Exception:
        kq["pillow"] = {"co_san": False,
                        "chi_tiet": "Thiếu Pillow.",
                        "thieu": ["pip install pillow"]}
    # --- H2 ---
    kit = os.path.join(duong_dan_h2(), "kit")
    thieu_h2, chi_h2 = [], []
    if not os.path.isfile(os.path.join(kit, "render.mjs")):
        thieu_h2.append("kit H2 chưa tải (render.mjs)")
    else:
        chi_h2.append("kit H2 có sẵn")
    for ten_pack in ("chipsieunang", "nguechngoac", "giaosubut",
                     "nhanvatkhoa"):
        if not os.path.isfile(os.path.join(
                kit, "packs", ten_pack, "pack.js")):
            thieu_h2.append("pack %s chưa có" % ten_pack)
    try:
        r = subprocess.run(["node", "--version"], capture_output=True,
                           text=True, timeout=15, **_chay_ngam_kwargs())
        chi_h2.append("Node %s" % (r.stdout or "?").strip()
                      if r.returncode == 0 else "Node lỗi")
        if r.returncode != 0:
            thieu_h2.append("Node 22+ chưa cài")
    except Exception:
        thieu_h2.append("Node 22+ chưa cài")
    if not os.path.isdir(os.path.join(kit, "node_modules",
                                      "playwright")):
        thieu_h2.append("node_modules/playwright chưa npm install")
    else:
        chi_h2.append("playwright đã npm install")
    cache_pw = os.path.join(os.path.expanduser("~"), ".cache",
                            "ms-playwright")
    if os.path.isdir(cache_pw) and os.listdir(cache_pw):
        chi_h2.append("Chromium (Playwright) đã tải")
    else:
        thieu_h2.append("Chromium (Playwright) chưa tải")
    if not _ffmpeg_co_san():
        thieu_h2.append("ffmpeg chưa có")
    kq["h2"] = {"co_san": not thieu_h2,
                "chi_tiet": "; ".join(chi_h2) if chi_h2 else
                "Chưa có tài nguyên H2.",
                "thieu": thieu_h2}
    # --- Skia ---
    eng = os.path.join(duong_dan_skia(), "engine")
    thieu_sk, chi_sk = [], []
    if not os.path.isfile(os.path.join(eng, "__main__.py")):
        thieu_sk.append("engine skia chưa tải")
    else:
        chi_sk.append("engine skia có sẵn")
    # (v7.25) Đã đóng gói mà máy không có Python hệ thống thì KHÔNG
    # spawn gì (sys.executable lúc này là exe của tool — đây chính là
    # chỗ gây nhân bản vô hạn lúc khởi động ở v7.24).
    python = _python_he_thong()
    if not python:
        thieu_sk.append("không kiểm tra được thư viện skia "
                        "(chưa có Python thật trên máy — tải ở "
                        "python.org/downloads, nhớ tick "
                        "'Add Python to PATH')")
    else:
        try:
            r = subprocess.run([python, "-c", "import skia"],
                               capture_output=True, text=True, timeout=20,
                               **_chay_ngam_kwargs())
            if r.returncode == 0:
                chi_sk.append("thư viện skia đã cài")
            else:
                thieu_sk.append("thư viện skia chưa pip install")
        except Exception:
            thieu_sk.append("không kiểm tra được thư viện skia")
    kq["skia"] = {"co_san": not thieu_sk,
                  "chi_tiet": "; ".join(chi_sk) if chi_sk else
                  "Chưa có tài nguyên skia.",
                  "thieu": thieu_sk}
    return kq


def model_ve_mac_dinh():
    """Model mặc định: H2 nếu đủ tài nguyên, không thì Pillow
    (kèm ghi chú 'ấn Tải tài nguyên' ở UI)."""
    tt = kiem_tra_tai_nguyen_ve()
    return "h2" if tt.get("h2", {}).get("co_san") else "pillow"


# --- Pack 4 "nhanvatkhoa": nguoi.js + pack.js (bible riêng) ---
NGUOI_JS_NHAN_VAT_KHOA = r'''// nguoi.js — pack "nhanvatkhoa": nhân vật ĐÃ KHÓA của CYAN.
// Stickman nét mảnh, đầu tròn KHÔNG mặt (không mắt, không mi,
// không miệng), chân tay 1 nét, khăn là dấu nhận diện.
// Interface giống hệt packs/*/nguoi.js của 3 pack gốc:
// nguoi(g, x, y, h, o) với o={who,outfit,t,seed,facing,pose,face,
// look,hold,tears,sweat,blush,mouth,alpha,ghost,rim,noShadow,
// walk,run,leg}. face/mouth/blush/tears/sweat bị BỎ QUA có chủ
// đích — nhân vật đã khóa không có mặt. ghost chưa hỗ trợ
// (vẽ bình thường thay vì tàng hình).
// CAST: cau_ay (khăn quàng đỏ thắt nơ, nền trắng, cầm sách),
// him (khăn len navy, nền xám nhạt, cầm cà phê),
// nguoi_ay (khăn len xám, ôm sách, hào quang vàng + sao),
// me, minh, ba_ban_xoi, co_hanh (phụ — chưa khóa ảnh mẫu,
// vẽ bằng code, cần CYAN duyệt).
// 'ban' là alias kỹ thuật = cau_ay (template mặc định dùng 'ban').
import { E, clamp, lerp, ease, alpha, shade } from '/engine/core.js';
import { PAL, oval, line, rrect } from './ink.js';

export const CAST = {
  cau_ay:     { khan: 'no_do', mau_khan: '#d43a2e', mau_ao: '#f7f5f0', nen: '#ffffff', do_cam: 'sach', giong: 'Xuân Vĩnh' },
  him:        { khan: 'len_navy', mau_khan: '#23395d', mau_ao: '#f7f5f0', nen: '#e8e8e8', do_cam: 'ca_phe', giong: 'Xuân Vĩnh' },
  nguoi_ay:   { khan: 'len_xam', mau_khan: '#9a9a9a', mau_ao: '#f7f5f0', nen: '#ffffff', do_cam: 'sach', giong: 'Ngọc Huyền', hao_quang: true },
  me:         { khan: 'khong', mau_khan: '#8a6a4a', mau_ao: '#8a6a4a', nen: '#ffffff', do_cam: '', giong: 'Ngọc Huyền' },
  minh:       { khan: 'khong', mau_khan: '#3a5a8a', mau_ao: '#f7f5f0', nen: '#ffffff', do_cam: '', giong: 'Xuân Vĩnh' },
  ba_ban_xoi: { khan: 'khong', mau_khan: '#b89a6a', mau_ao: '#b89a6a', nen: '#ffffff', do_cam: '', giong: 'Ngọc Huyền', non: 'nonla' },
  co_hanh:    { khan: 'khong', mau_khan: '#7b5ea7', mau_ao: '#7b5ea7', nen: '#ffffff', do_cam: '', giong: 'Ngọc Huyền' },
};
CAST.ban = CAST.cau_ay;  // alias kỹ thuật cho template mặc định

export const RIM = { color: '#f2a050', side: 1 };
export function setRim(c, side) { if (c) RIM.color = c; if (side) RIM.side = side; }
export let LEGK = 1.5; export function setLeg(v) { LEGK = v; }

// ---------- tư thế (hình học chung, copy từ pack gốc)
const L0 = { l1: [0.24, 0.55, 0.28, 1.1], l2: [-0.24, 0.55, -0.28, 1.1] };
const sym = (e, h) => ({ a1: [e[0], e[1], h[0], h[1]], a2: [-e[0], e[1], -h[0], h[1]] });
export const POSES = {
  stand:   { ...sym([0.66, -0.52], [0.66, -0.08]), ...L0 },
  relax:   { ...sym([0.62, -0.5], [0.52, -0.06]), l1: [0.3, 0.55, 0.4, 1.1], l2: [-0.3, 0.55, -0.4, 1.1] },
  wave:    { a1: [1.0, -1.25, 1.12, -1.85], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
  point:   { a1: [1.05, -0.95, 1.6, -1.05], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
  pointUp: { a1: [0.95, -1.35, 1.05, -1.95], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
  cheer:   { ...sym([0.95, -1.35], [1.1, -1.95]), l1: [0.3, 0.5, 0.36, 1.1], l2: [-0.3, 0.5, -0.36, 1.1] },
  hold:    { ...sym([0.72, -0.5], [0.34, -0.62]), ...L0 },
  holdUp:  { a1: [0.85, -1.1, 0.9, -1.7], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
  think:   { a1: [0.78, -0.62, 0.3, -1.2], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
  shrug:   { ...sym([0.95, -0.72], [1.15, -1.12]), ...L0 },
  hips:    { ...sym([1.02, -0.62], [0.58, -0.22]), l1: [0.32, 0.55, 0.42, 1.1], l2: [-0.32, 0.55, -0.42, 1.1] },
  head:    { ...sym([1.05, -1.35], [0.62, -1.95]), ...L0 },
  faceH:   { ...sym([0.8, -0.82], [0.38, -1.45]), ...L0 },
  clap:    { ...sym([0.78, -0.72], [0.08, -0.95]), ...L0 },
  push:    { ...sym([0.95, -0.72], [1.35, -0.72]), l1: [0.36, 0.5, 0.52, 1.1], l2: [-0.3, 0.6, -0.5, 1.1], lean: 0.18 },
  reach:   { a1: [1.05, -1.15, 1.6, -1.45], a2: [-0.66, -0.52, -0.7, -0.1], ...L0 },
  sad:     { ...sym([0.55, -0.45], [0.36, -0.02]), ...L0, droop: 0.12 },
  crouch:  { ...sym([0.8, -0.3], [0.62, 0.15]), l1: [0.55, 0.15, 0.4, 0.62], l2: [-0.5, 0.15, -0.4, 0.62], sink: 0.48 },
  sit:     { ...sym([0.7, -0.45], [0.75, -0.02]), l1: [0.7, 0.02, 0.72, 0.62], l2: [0.48, 0.02, 0.5, 0.62], sink: 0.48 },
  jump:    { ...sym([1.0, -1.25], [1.1, -1.85]), l1: [0.4, 0.35, 0.3, 0.8], l2: [-0.4, 0.35, -0.3, 0.8], sink: -0.35 },
  breath:  { ...sym([0.66, -0.55], [0.5, -0.2]), ...L0, puff: 1 },
  lie:     { ...sym([0.66, -0.52], [0.66, -0.08]), ...L0, lie: true },
  phone:   { a1: [0.62, -0.5, 0.36, -0.85], a2: [-0.66, -0.52, -0.66, -0.08], ...L0 },
};
const asPose = (p) => (typeof p === 'string' ? (POSES[p] || POSES.stand) : p || POSES.stand);
const lerpArr = (a, b, k) => a.map((v, i) => lerp(v, b[i], k));
export function blendPose(a, b, k) { a = asPose(a); b = asPose(b); return { ...b, a1: lerpArr(a.a1, b.a1, k), a2: lerpArr(a.a2, b.a2, k), l1: lerpArr(a.l1, b.l1, k), l2: lerpArr(a.l2, b.l2, k), lean: lerp(a.lean || 0, b.lean || 0, k), sink: lerp(a.sink || 0, b.sink || 0, k), droop: lerp(a.droop || 0, b.droop || 0, k), puff: lerp(a.puff || 0, b.puff || 0, k), lie: k > 0.5 ? b.lie : a.lie }; }
export function poseAt(lt, list, def = 'stand', blend = 0.25) {
  if (!list || !list.length) return asPose(def);
  let cur = asPose(def);
  for (const [ti, p] of list) if (lt >= ti) cur = blendPose(cur, p, ease.inOut(clamp((lt - ti) / blend)));
  return cur;
}
function walkPose(ph, run) {
  const s = Math.sin(ph), A = run ? 1.5 : 1;
  const leg = (sg) => { const sw = s * sg * 0.32 * A, lift = Math.max(0, Math.sin(ph + (sg > 0 ? 0 : Math.PI))) * 0.22 * A; return [sw * 0.6 + 0.12 * sg * 0.3, 0.55 - lift, sw, 1.1 - lift * 0.9]; };
  const arm = (sg) => { const sw = -s * sg * 0.35 * A; return [0.62 * sg + sw * 0.4, -0.55, 0.6 * sg + sw, -0.1 - Math.abs(sw) * 0.3]; };
  return { a1: arm(1), a2: arm(-1), l1: leg(1), l2: leg(-1), lean: run ? 0.16 : 0.04, bounce: Math.abs(Math.cos(ph)) * (run ? 0.12 : 0.05) };
}

// ---------- mặt: nhân vật đã khóa KHÔNG có mặt — giữ hàm cho đủ interface
export function face(g, cx, cy, R, o = {}) { /* đầu tròn không mặt */ }
export function star(g, x, y, r, c) { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r; g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.closePath(); g.fillStyle = c; g.fill(); }

// ---------- vẽ
export function nguoi(g, x, y, h, o = {}) {
  const out = { ...(CAST[o.who] || CAST.ban), ...(o.outfit || {}) };
  const LEG = o.leg ?? LEGK, R = h / 5.2, t = o.t || 0, f = o.facing ?? 1;
  let P = asPose(o.pose);
  if (o.walk || o.run) P = { ...walkPose(t * Math.PI * 2 * (o.run ? 1.6 : 1.0) * (o.run || o.walk || 1), !!o.run), droop: 0 };
  const lie = P.lie;
  const info = { head: [x, y - h + R], R, x, y };
  g.save(); g.globalAlpha *= o.alpha ?? 1;
  drawBody(g, x, y, R, P, out, o, f, t, lie);
  g.restore();
  const bounce = (P.bounce || 0) * R, sink = (P.sink || 0) * R;
  info.head = lie ? [x - 1.9 * R * f, y - R * 0.95] : [x + (P.lean || 0) * R * 1.4 * f, y - 0.95 * R * LEG + sink - bounce - 2.3 * R];
  return info;
}

function drawBody(g, x, y, R, P, out, o, f, t, lie) {
  const LEG = o._leg || LEGK;
  const bounce = (P.bounce || 0) * R, sink = (P.sink || 0) * R, lean = P.lean || 0, droop = P.droop || 0;
  const breath = Math.sin(t * 2.3 + (o.seed || 0)) * R * 0.018;
  const ink = '#22222a', NET = R * 0.09;  // nét mảnh
  if (!o.noShadow && !lie) { g.save(); g.fillStyle = 'rgba(40,25,30,0.18)'; g.beginPath(); g.ellipse(x, y + R * 0.04, R * 1.05, R * 0.16, 0, 0, Math.PI * 2); g.fill(); g.restore(); }
  g.save(); g.translate(x, y);
  if (lie) { g.translate(0, -R * 0.6); g.rotate(-Math.PI / 2 * f); g.translate(0, R * 0.2); }
  g.scale(f, 1);
  const hipY = -0.95 * R * LEG + sink - bounce, X = (v) => v * R, Y = (v) => hipY + v * R, YA = (v) => hipY + v * R * 1.4, YL = (v) => hipY + v * R * 0.86 * LEG;
  const lean0 = lean * R * 1.4;
  const sh1 = [X(0.1) + lean0 * 0.8, YA(-0.98) + breath], sh2 = [X(-0.1) + lean0 * 0.8, YA(-0.98) + breath];
  const headC = [lean0, YA(-1.0) - 0.9 * R + breath * 1.5 + droop * R], hr = R * 1.02;
  // hào quang Người Ấy (vẽ trước, sau lưng nhân vật)
  if (out.hao_quang) {
    const grad = g.createRadialGradient(headC[0], headC[1], hr * 0.2, headC[0], headC[1], hr * 3.2);
    grad.addColorStop(0, 'rgba(255,214,90,0.45)'); grad.addColorStop(1, 'rgba(255,214,90,0)');
    g.save(); g.fillStyle = grad; g.beginPath(); g.arc(headC[0], headC[1], hr * 3.2, 0, Math.PI * 2); g.fill(); g.restore();
    const tw = 0.5 + 0.5 * Math.sin(t * 3);
    star(g, headC[0] - hr * 1.9, headC[1] - hr * 1.2, hr * 0.22 * (0.7 + 0.3 * tw), '#ffd34d');
    star(g, headC[0] + hr * 1.7, headC[1] - hr * 0.6, hr * 0.18 * (0.7 + 0.3 * tw), '#ffd34d');
    star(g, headC[0] + hr * 1.3, headC[1] + hr * 1.5, hr * 0.15, '#ffd34d');
  }
  // chân 1 nét
  for (const L of [P.l2, P.l1]) { const hip = [X(L === P.l1 ? 0.22 : -0.22), Y(0)], k = [X(L[0]), YL(L[1])], ft = [X(L[2]), YL(L[3])]; line(g, [hip, k, ft], NET, ink); }
  // thân 1 nét
  line(g, [[lean0, Y(0.1)], [lean0 * 0.8, YA(-0.98) + breath]], NET, ink);
  // đồ cầm (vẽ trước tay để tay đè lên)
  if (o.hold) holdProp(g, o.hold, P, X, YA, lean0, R, t);
  // tay 1 nét (vai -> khuỷu -> tay) + chấm tay tròn nhỏ
  for (const [A, sh] of [[P.a2, sh2], [P.a1, sh1]]) {
    const el = [X(A[0] * 1.08) + lean0 * 0.5, YA(A[1])], hd = [X(A[2] * 1.08) + lean0 * 0.4, YA(A[3])];
    line(g, [sh, el, hd], NET, ink);
    oval(g, hd[0], hd[1], R * 0.09, R * 0.09, ink);
  }
  // đầu tròn không mặt: chỉ viền nét mảnh
  g.save(); g.lineWidth = NET; g.strokeStyle = ink; g.beginPath(); g.arc(headC[0], headC[1], hr, 0, Math.PI * 2); g.stroke(); g.restore();
  // nón lá (bà bán xôi)
  if (out.non === 'nonla') {
    g.save(); g.fillStyle = '#e8d29a'; g.strokeStyle = ink; g.lineWidth = NET * 0.8;
    g.beginPath(); g.moveTo(headC[0] - hr * 1.7, headC[1] - hr * 0.35); g.lineTo(headC[0], headC[1] - hr * 1.65); g.lineTo(headC[0] + hr * 1.7, headC[1] - hr * 0.35); g.closePath(); g.fill(); g.stroke(); g.restore();
  }
  // khăn (dấu nhận diện)
  scarf(g, headC, hr, out, R);
  g.restore();
}

function scarf(g, headC, hr, out, R) {
  const mau = out.mau_khan || '#d43a2e', W = R * 0.16;
  g.save(); g.lineCap = 'round';
  if (out.khan === 'no_do') {
    // vòng cổ + nơ thắt trước cổ + 2 đầu ngắn
    g.lineWidth = W; g.strokeStyle = mau;
    g.beginPath(); g.arc(headC[0], headC[1] + hr * 0.95, hr * 0.55, 0.15 * Math.PI, 0.85 * Math.PI); g.stroke();
    g.fillStyle = mau;
    const bx = headC[0], by = headC[1] + hr * 1.05;
    g.beginPath(); g.moveTo(bx, by); g.lineTo(bx - R * 0.42, by - R * 0.22); g.lineTo(bx - R * 0.42, by + R * 0.22); g.closePath(); g.fill();
    g.beginPath(); g.moveTo(bx, by); g.lineTo(bx + R * 0.42, by - R * 0.22); g.lineTo(bx + R * 0.42, by + R * 0.22); g.closePath(); g.fill();
    line(g, [[bx - R * 0.1, by + R * 0.1], [bx - R * 0.28, by + R * 0.75]], W * 0.8, mau);
    line(g, [[bx + R * 0.1, by + R * 0.1], [bx + R * 0.3, by + R * 0.7]], W * 0.8, mau);
  } else if (out.khan === 'len_navy' || out.khan === 'len_xam') {
    // quấn cổ 2 vòng + 2 đầu thả xuống ngực (KHÔNG thắt nơ)
    g.lineWidth = W; g.strokeStyle = mau;
    g.beginPath(); g.arc(headC[0], headC[1] + hr * 0.9, hr * 0.62, 0.1 * Math.PI, 0.9 * Math.PI); g.stroke();
    g.beginPath(); g.arc(headC[0], headC[1] + hr * 1.08, hr * 0.6, 0.15 * Math.PI, 0.85 * Math.PI); g.stroke();
    line(g, [[headC[0] - R * 0.35, headC[1] + hr * 1.15], [headC[0] - R * 0.5, headC[1] + hr * 2.6]], W * 0.85, mau);
    line(g, [[headC[0] + R * 0.35, headC[1] + hr * 1.15], [headC[0] + R * 0.55, headC[1] + hr * 2.45]], W * 0.85, mau);
  }
  g.restore();
}

// đồ cầm: sach (sách) | ca_phe (cốc cà phê) | hoa
function holdProp(g, name, P, X, Y, lean0, R, t) {
  const A = P.a1, hx = X(A[2]) + lean0 * 0.4, hy = Y(A[3]);
  g.save(); g.translate(hx, hy);
  if (name === 'sach') {
    rrect(g, -R * 0.42, -R * 0.55, R * 0.84, R * 1.1, R * 0.06, '#f7f5f0');
    g.lineWidth = R * 0.05; g.strokeStyle = '#22222a'; g.strokeRect(-R * 0.42, -R * 0.55, R * 0.84, R * 1.1);
    line(g, [[0, -R * 0.55], [0, R * 0.55]], R * 0.04, '#22222a');
  } else if (name === 'ca_phe') {
    rrect(g, -R * 0.28, -R * 0.3, R * 0.56, R * 0.6, R * 0.08, '#f7f5f0');
    g.lineWidth = R * 0.05; g.strokeStyle = '#22222a'; g.strokeRect(-R * 0.28, -R * 0.3, R * 0.56, R * 0.6);
    g.beginPath(); g.arc(R * 0.28, 0, R * 0.16, -Math.PI / 2, Math.PI / 2); g.stroke();
    line(g, [[-R * 0.12, -R * 0.5], [-R * 0.12, -R * 0.72]], R * 0.04, '#999999');
    line(g, [[R * 0.1, -R * 0.5], [R * 0.1, -R * 0.7]], R * 0.04, '#999999');
  } else if (name === 'hoa') {
    line(g, [[0, 0], [0, R * 0.7]], R * 0.06, '#3f7a46');
    for (let i = 0; i < 5; i++) { const a = i * Math.PI * 2 / 5; oval(g, Math.cos(a) * R * 0.16, -R * 0.16 + Math.sin(a) * R * 0.16, R * 0.14, R * 0.14, '#ff8a9a'); }
    oval(g, 0, -R * 0.16, R * 0.12, R * 0.12, '#ffd34d');
  }
  g.restore();
}
'''

PACK_JS_NHAN_VAT_KHOA = r'''// pack.js — bộ phong cách "nhanvatkhoa": nhân vật đã khóa của CYAN
// (stickman nét mảnh, đầu tròn không mặt, khăn là dấu nhận diện),
// nền trắng/xám nhạt, không vignette, không grade phim ấm.
// config.json: "pack": "nhanvatkhoa", "style": "phim", "captions": true
import { E, STYLES } from '/engine/core.js';
import './templates.js';
import './gsb.js';
import './chip.js';
import { karaoke, watermark } from './ink.js';
export * from './ink.js';
export * from './nguoi.js';
export * from './sets.js';
export * from './templates.js';
export * from './gsb.js';
export * from './chip.js';
export { thumb, thumbText, thumbTag, sparkle } from './thumb.js';
export { img, E, registerShot } from '/engine/core.js';

function css(href) { return new Promise((r) => { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; l.onload = r; l.onerror = r; document.head.appendChild(l); }); }
export async function init(E) {
  await Promise.all(['be-vietnam-pro/700.css', 'be-vietnam-pro/800.css', 'baloo-2/800.css', 'patrick-hand/400.css', 'anton/400.css'].map((f) => css('/node_modules/@fontsource/' + f)));
  await Promise.all([document.fonts.load('400 40px "Anton"', 'THẤY ĐƯỢC TƯƠNG LAI Ộ Ữ'), document.fonts.load('800 40px "Baloo 2"', 'NẾU BẠN ĐỨNG HÌNH'), document.fonts.load('700 40px "Be Vietnam Pro"', 'Chuyện này là thật'), document.fonts.load('800 40px "Be Vietnam Pro"', 'Chuyện này là thật')]);
  // phong cách đã khóa: trắng/xám, không grade ấm, không vignette
  STYLES.phim = { name: 'Nhân vật đã khóa (trắng/xám)', tint: null, grade: { lift: [0, 0, 0], gain: [255, 255, 255], contrast: 1.0, sat: 1.0, vignette: 0, grain: 0 } };
  STYLES.dem = { name: 'Đêm xanh', tint: null, grade: { lift: [10, 12, 22], gain: [226, 232, 250], contrast: 1.05, sat: 0.92, vignette: 0.5, grain: 0.05 } };
  if (!E.cfg.style || E.cfg.style === 'dusk' || E.cfg.style === 'toi') E.cfg.style = 'phim';
  if (E.cfg.captions === undefined) E.cfg.captions = true;
  if (E.cfg.bars === null || E.cfg.bars === undefined) E.cfg.bars = 'none';
  if (!E.cfg.captionStyle) E.cfg.captionStyle = 'karaoke';
}
export function captions(g, ws, idx, t) { karaoke(g, ws, idx, t); }
export { watermark };
'''


def viet_pack_nhan_vat_khoa(kit_dir, log_cb=None):
    """Ghi pack thứ 4 'nhanvatkhoa' vào kit_dir/packs/:
    copy toàn bộ file của pack chipsieunang (ink/sets/templates/
    gsb/chip/thumb — engine dùng chung, đã đối chiếu giống hệt
    giữa 3 plugin) rồi GHI ĐÈ nguoi.js + pack.js bằng bản riêng
    cho nhân vật đã khóa. Trả (ok, duong_dan_pack, loi)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    nguon = os.path.join(duong_dan_plugin_goc(), "h2-doi-thuong",
                         "skills", "lam-video-chipsieunang", "kit",
                         "packs", "chipsieunang")
    if not os.path.isdir(nguon):
        return False, None, ("Không tìm thấy pack gốc chipsieunang "
                             "trong plugin-goc — kiểm tra lại file "
                             "gốc CYAN gửi.")
    dich = os.path.join(kit_dir, "packs", "nhanvatkhoa")
    os.makedirs(dich, exist_ok=True)
    try:
        for ten in os.listdir(nguon):
            if ten in ("nguoi.js", "pack.js"):
                continue
            src = os.path.join(nguon, ten)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(dich, ten))
        with open(os.path.join(dich, "nguoi.js"), "w",
                  encoding="utf-8") as f:
            f.write(NGUOI_JS_NHAN_VAT_KHOA)
        with open(os.path.join(dich, "pack.js"), "w",
                  encoding="utf-8") as f:
            f.write(PACK_JS_NHAN_VAT_KHOA)
    except Exception as e:
        return False, None, "Ghi pack nhanvatkhoa lỗi: %s" % e
    _log("Đã ghi pack 'nhanvatkhoa' (nhân vật đã khóa) vào kit.")
    return True, dich, ""


def tai_tai_nguyen_h2(log_cb=None):
    """Tải/cài tài nguyên H2 vào thư mục làm việc riêng
    (~/h2-2d-studio): copy kit engine (bản duy nhất, lấy từ
    h2-doi-thuong — đã đối chiếu giống hệt 3 plugin) + 3 pack gốc
    + pack 4 nhanvatkhoa, rồi npm install + playwright install
    chromium. Cần Node 22 + npm + mạng. Chạy lâu (~400 MB).
    Trả (ok, loi)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    goc = duong_dan_plugin_goc()
    kit_goc = os.path.join(goc, "h2-doi-thuong", "skills",
                           "lam-video-chipsieunang", "kit")
    if not os.path.isdir(kit_goc):
        return False, ("Không tìm thấy kit H2 gốc trong plugin-goc — "
                       "kiểm tra lại file gốc CYAN gửi.")
    h2_dir = duong_dan_h2()
    kit_dir = os.path.join(h2_dir, "kit")
    os.makedirs(h2_dir, exist_ok=True)
    _log("Đang copy kit H2 vào %s ..." % kit_dir)
    try:
        if os.path.isdir(kit_dir):
            shutil.rmtree(kit_dir)
        shutil.copytree(kit_goc, kit_dir,
                        ignore=shutil.ignore_patterns(
                            "node_modules", "__pycache__",
                            "projects", "dist"))
        # 2 pack còn lại (chỉ lấy thư mục packs của từng kit).
        for ten_kit, ten_pack in (
                ("h2-khoa-hoc", "nguechngoac"),
                ("h2-tinh-cam", "giaosubut")):
            src_pack = os.path.join(
                goc, ten_kit, "skills",
                ("lam-video-nguechngoac" if ten_kit == "h2-khoa-hoc"
                 else "lam-video-giaosubut"), "kit", "packs", ten_pack)
            if os.path.isdir(src_pack):
                shutil.copytree(src_pack, os.path.join(
                    kit_dir, "packs", ten_pack), dirs_exist_ok=True)
                _log("Đã copy pack %s." % ten_pack)
        ok, _, loi = viet_pack_nhan_vat_khoa(kit_dir, log_cb)
        if not ok:
            return False, loi
    except Exception as e:
        return False, "Copy kit H2 lỗi: %s" % e
    _log("Đang npm install (kit H2, ~400 MB, chờ vài phút)...")
    try:
        r = subprocess.run(["npm", "install", "--no-audit",
                            "--no-fund"], cwd=kit_dir,
                           capture_output=True, text=True, timeout=1800,
                           **_chay_ngam_kwargs())
        if r.returncode != 0:
            return False, ("npm install lỗi: %s"
                           % (r.stderr or r.stdout)[-500:])
        _log("npm install xong. Đang tải Chromium (Playwright)...")
        r = subprocess.run(["npx", "playwright", "install",
                            "chromium"], cwd=kit_dir,
                           capture_output=True, text=True, timeout=1800,
                           **_chay_ngam_kwargs())
        if r.returncode != 0:
            return False, ("Tải Chromium lỗi: %s"
                           % (r.stderr or r.stdout)[-500:])
    except Exception as e:
        return False, "Cài H2 lỗi: %s" % e
    _log("Đã cài xong tài nguyên H2 tại %s." % h2_dir)
    return True, ""


def viet_du_an_h2(du_lieu, outdir, phong_cach, cue_files, cues,
                  bo_qua_voice=False):
    """Ghi project H2 vào outdir/h2-project/: config.json
    (pack = nhanvatkhoa hoặc pack đã chọn), story/shots.json
    (1 shot/cảnh, start/end theo voice thật), timeline/words.json
    (từng từ) + lines.json, voice.wav (nối các cue MP3, nghỉ đúng
    nhịp sau mỗi cue — khớp mốc SRT đã căn theo voice thật). bo_qua_voice=True khi
    chỉ xem sheet (chưa cần voice). Trả (ok, duong_dan, loi).
    CẢNH BÁO: nếu chọn pack Chíp/Nguệch/Giáo Sư mà cảnh vẫn dùng
    nhân vật đã khóa (cau_ay/him/nguoi_ay) thì H2 vẽ họ bằng
    nhân vật 'ban' của pack đó (template mặc định) — muốn đúng
    kiểu pack thì chọn nhân vật gốc trong ô chọn nhân vật."""
    scenes = du_lieu.get("scenes") or []
    if not scenes:
        return False, None, "Không có cảnh nào."
    proj = os.path.join(outdir, "h2-project")
    os.makedirs(os.path.join(proj, "story"), exist_ok=True)
    os.makedirs(os.path.join(proj, "timeline"), exist_ok=True)
    pack_id = ("nhanvatkhoa" if phong_cach == "nhan_vat_khoa"
               else PACK_ID_H2.get(phong_cach, "nhanvatkhoa"))
    cfg = {"title": du_lieu.get("title") or "Postman 2D",
           "aspect": "16:9", "resolution": "1080p", "fps": 24,
           "style": "phim", "captions": True,
           "captionStyle": "karaoke", "bars": "none",
           "fadeIn": 0.4, "fadeOut": 0.8, "pack": pack_id,
           "lang": "vi", "music": {"enabled": False},
           "sfx": {"enabled": False}, "loudness": -14,
           "channel": ""}
    with open(os.path.join(proj, "config.json"), "w",
              encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)
    shots, canh_bao = [], []
    for i, sc in enumerate(scenes, 1):
        cu = cues[i - 1] if i - 1 < len(cues) else {}
        actors = []
        chars = sc.get("characters") or ["cau_ay"]
        for j, cid in enumerate(chars):
            if isinstance(cid, str) and cid.startswith("co_san:"):
                who = cid.split(":", 2)[2]
            else:
                who = cid
                if phong_cach != "nhan_vat_khoa" and cid in CHARACTERS:
                    canh_bao.append(
                        "Cảnh %s: nhân vật đã khóa '%s' dùng với "
                        "pack %s — H2 sẽ vẽ bằng nhân vật 'ban' "
                        "của pack (muốn đúng kiểu pack thì chọn "
                        "nhân vật gốc trong ô chọn nhân vật)."
                        % (sc.get("id"), cid,
                           PHONG_CACH_H2.get(phong_cach, phong_cach)))
            n = max(len(chars), 1)
            x = 0.5 if n == 1 else 0.5 + (j - (n - 1) / 2) * 0.24
            actors.append({"who": who, "x": round(x, 3),
                           "pose": (sc.get("pose") or "stand"),
                           "face": "thuong"})
        shots.append({"id": "s%03d" % i,
                      "start": float(cu.get("start", 0)),
                      "end": float(cu.get("end", 0)),
                      "tpl": "canh",
                      "args": {"set": sc.get("set") or "phong",
                               "actors": actors},
                      "line": sc.get("narration") or ""})
    tong = float(cues[-1].get("end", 0)) if cues else 0.0
    with open(os.path.join(proj, "story", "shots.json"), "w",
              encoding="utf-8") as f:
        json.dump({"duration": round(tong, 3), "shots": shots}, f,
                  ensure_ascii=False, indent=1)
    with open(os.path.join(proj, "timeline", "words.json"), "w",
              encoding="utf-8") as f:
        json.dump(viet_words_json(cues), f, ensure_ascii=False)
    with open(os.path.join(proj, "timeline", "lines.json"), "w",
              encoding="utf-8") as f:
        json.dump([{"text": (c.get("text") or ""),
                    "start": c.get("start"), "end": c.get("end")}
                   for c in cues], f, ensure_ascii=False, indent=1)
    # voice.wav: nối các cue MP3, chèn im lặng giữa các cue đúng
    # nhịp đã ghi trong cues (nghi_sau_giay — SRT căn theo voice
    # thật; mặc định 0.35s khi SRT còn là ước tính). Bỏ qua khi chỉ
    # xem sheet (bo_qua_voice=True).
    if bo_qua_voice:
        return True, proj, "; ".join(canh_bao)
    try:
        ds, loi_noi = _danh_sach_noi_voice(outdir, cue_files, cues)
        if ds is None:
            return False, None, loi_noi
        lst = os.path.join(outdir, "voice-concat.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in ds:
                f.write("file '%s'\n" % p.replace("'", "'\\''"))
        voice_wav = os.path.join(proj, "voice.wav")
        r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe",
                            "0", "-i", lst, "-ar", "48000", "-ac",
                            "2", voice_wav],
                           capture_output=True, text=True, timeout=600,
                           **_chay_ngam_kwargs())
        if r.returncode != 0:
            return False, None, ("Nối voice.wav lỗi: %s"
                                 % r.stderr[-400:])
    except Exception as e:
        return False, None, "Nối voice.wav lỗi: %s" % e
    return True, proj, "; ".join(canh_bao)


def _file_im_lang_ms(outdir, ms):
    """Tạo (hoặc dùng lại) file im lặng dài ms (MP3 44100/stereo/
    192k) để chèn giữa các cue khi nối voice. Trả đường dẫn hoặc
    None nếu tạo lỗi."""
    path = os.path.join(outdir, "im-lang-%dms.mp3" % int(ms))
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        return path
    r = subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                        "anullsrc=r=44100:cl=stereo",
                        "-t", "%.3f" % (ms / 1000.0),
                        "-c:a", "libmp3lame", "-b:a", "192k",
                        path], capture_output=True, timeout=60,
                       **_chay_ngam_kwargs())
    if r.returncode == 0 and os.path.isfile(path):
        return path
    return None


def _danh_sach_noi_voice(outdir, cue_files, cues):
    """Danh sách file để nối voice.wav: cue1, im lặng (nhịp sau
    cue1), cue2, ... Nhịp lấy từ cues[i]["nghi_sau_giay"] (SRT đã
    căn theo voice thật); cue không có nhịp thì mặc định 0.35s để
    khớp SRT ước tính cũ. Trả (danh_sach, loi)."""
    ds = []
    for k, mp3 in enumerate(cue_files):
        ds.append(mp3)
        if k < len(cue_files) - 1:
            cu = cues[k] if k < len(cues) else {}
            nghi = float(cu.get("nghi_sau_giay") or 0.35)
            if nghi > 0:
                im = _file_im_lang_ms(outdir, round(nghi * 1000))
                if im is None:
                    return None, ("Không tạo được file im lặng "
                                  "%.0fms để nối voice." % (nghi * 1000))
                ds.append(im)
    return ds, ""


def render_bang_h2(du_lieu, outdir, cue_files, cues, phong_cach,
                   rong=1280, cao=720, log_cb=None):
    """Dựng video bằng H2: ghi project rồi gọi
    `node render.mjs --project <dir> --mix` (render + trộn voice
    trong 1 lệnh). Trả (ok, {final_mp4, srt, scenes_mp4}, loi).
    Thiếu tài nguyên -> BÁO LỖI RÕ (bấm Tải tài nguyên), KHÔNG
    tự render sai bằng Pillow im lặng. CHƯA kiểm chứng end-to-end
    trên máy CYAN (chỉ test render mẫu trên VM này)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    tt = kiem_tra_tai_nguyen_ve()["h2"]
    if not tt["co_san"]:
        return False, {}, ("Chưa đủ tài nguyên H2: %s — ấn nút "
                           "'Tải tài nguyên H2' ở tab Postman rồi "
                           "thử lại." % "; ".join(tt["thieu"]))
    ok, proj, cb = viet_du_an_h2(du_lieu, outdir, phong_cach,
                                 cue_files, cues)
    if not ok:
        return False, {}, cb
    if cb:
        _log("CẢNH BÁO H2: " + cb)
    kit_dir = os.path.join(duong_dan_h2(), "kit")
    _log("Đang render H2 (Node + Chromium, pack %s)..."
         % PHONG_CACH_H2.get(phong_cach, phong_cach))
    try:
        r = subprocess.run(["node", "render.mjs", "--project", proj,
                            "--mix"], cwd=kit_dir,
                           capture_output=True, text=True, timeout=3600,
                           **_chay_ngam_kwargs())
    except Exception as e:
        return False, {}, "Chạy render.mjs lỗi: %s" % e
    if r.returncode != 0:
        return False, {}, ("render.mjs lỗi: %s"
                           % (r.stderr or r.stdout)[-800:])
    # Tìm file final: render.mjs ghi ra thư mục project/out
    # (hoặc project/final.mp4) — lấy file MP4 mới nhất.
    ung_vien = []
    for noi in (os.path.join(proj, "out"), proj,
                os.path.join(proj, "dist")):
        if os.path.isdir(noi):
            for ten in os.listdir(noi):
                if ten.lower().endswith(".mp4"):
                    ung_vien.append(os.path.join(noi, ten))
    if not ung_vien:
        return False, {}, ("render.mjs chạy xong nhưng không tìm "
                           "thấy file MP4 final trong project H2 — "
                           "log: %s" % (r.stdout or "")[-400:])
    final = max(ung_vien, key=os.path.getmtime)
    _log("Render H2 xong: %s" % final)
def tai_tai_nguyen_skia(log_cb=None):
    """Tải/cài tài nguyên skia vào thư mục làm việc riêng
    (~/skia-2d-studio): copy engine từ file gốc trong plugin-goc
    (2d-long-form-src) hoặc từ skill 2d nếu không có, rồi
    pip install skia-python. Model ASR tiếng Việt (sherpa-onnx)
    nếu có setup.sh thì chạy để tải; không có thì engine dùng
    fallback đo khoảng lặng. Trả (ok, loi)."""
    def _log(s):
        if log_cb:
            log_cb(s)
    nguon = None
    for co_the in (os.path.join(duong_dan_plugin_goc(),
                                "2d-long-form-src"),
                   os.path.join(os.path.expanduser("~"), "workspace",
                                "custom-skills", "2d")):
        for root, _ds, files in os.walk(co_the):
            if "__main__.py" in files and os.path.basename(root) == \
                    "engine":
                nguon = os.path.dirname(root)
                break
        if nguon:
            break
    if not nguon:
        return False, ("Không tìm thấy engine skia trong plugin-goc "
                       "hay skill 2d — kiểm tra lại file gốc.")
    sk_dir = duong_dan_skia()
    os.makedirs(sk_dir, exist_ok=True)
    _log("Đang copy engine skia từ %s ..." % nguon)
    try:
        for ten in ("engine", "scripts"):
            src = os.path.join(nguon, ten)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(sk_dir, ten),
                                dirs_exist_ok=True)
        # (v7.25) Đã đóng gói thì sys.executable là exe của tool,
        # KHÔNG phải Python — dùng _python_he_thong().
        python = _python_he_thong()
        if not python:
            return False, THIEU_PYTHON_THAT
        r = subprocess.run([python, "-m", "pip", "install",
                            "skia-python"], capture_output=True,
                           text=True, timeout=900,
                           **_chay_ngam_kwargs())
        if r.returncode != 0:
            out_gop = (r.stderr or "") + (r.stdout or "")
            if _loi_thieu_python_that(out_gop):
                return False, THIEU_PYTHON_THAT
            return False, ("pip install skia-python lỗi: %s"
                           % out_gop[-400:])
    except Exception as e:
        return False, "Cài skia lỗi: %s" % e
    _log("Đã cài xong tài nguyên skia tại %s." % sk_dir)
    return True, ""


# Map nhân vật đã khóa -> cast skia (draw_char: skin/outfit/
# color/shirt/tie/hair/hair_col/glasses/moustache/beard/hat).
# GIỚI HẠN: skia KHÔNG có tham số khăn — màu áo lấy theo màu
# khăn để phân biệt nhân vật; nón lá cũng không có trong skia
# nên Bà bán xôi mất nón khi dựng bằng skia (xem đánh giá ở
# đầu mục 3b). Muốn đúng kiểu đã khóa thì dùng H2 pack 4.
CAST_SKIA_KHOA = {
    "cau_ay": {"skin": "fair", "outfit": "hoodie", "color": "#d43a2e",
               "shirt": "#f7f5f0", "hair": "short",
               "hair_col": "#22222a"},
    "him": {"skin": "fair", "outfit": "hoodie", "color": "#23395d",
            "shirt": "#f7f5f0", "hair": "short",
            "hair_col": "#22222a"},
    "nguoi_ay": {"skin": "fair", "outfit": "hoodie",
                 "color": "#9a9a9a", "shirt": "#f7f5f0",
                 "hair": "long", "hair_col": "#22222a"},
    "me": {"skin": "fair", "outfit": "dress", "color": "#8a6a4a",
           "hair": "bun", "hair_col": "#22222a"},
    "minh": {"skin": "fair", "outfit": "tshirt", "color": "#3a5a8a",
             "hair": "short", "hair_col": "#22222a"},
    "ba_ban_xoi": {"skin": "tan", "outfit": "dress",
                   "color": "#b89a6a", "hair": "bun",
                   "hair_col": "#888888"},
    "co_hanh": {"skin": "fair", "outfit": "dress",
                "color": "#7b5ea7", "hair": "bun",
                "hair_col": "#22222a"},
}


def _cast_skia_cho_nhan_vat(cid):
    """Spec cast skia cho 1 nhân vật (id đã lưu/khóa/có sẵn)."""
    if isinstance(cid, str) and cid.startswith("co_san:"):
        try:
            _, pack, code = cid.split(":", 2)
        except ValueError:
            return None
        if pack == "skia":
            return dict(NHAN_VAT_CO_SAN["skia"].get(code, {}))
        goc = NHAN_VAT_CO_SAN.get(pack, {}).get(code, {})
        ao = {"hoodie": "hoodie", "cardigan": "hoodie",
              "somi": "suit", "aodai": "dress",
              "blouse": "dress"}.get(goc.get("ao"), "hoodie")
        return {"skin": "fair", "outfit": ao,
                "color": goc.get("mau", "#888888"),
                "hair": {"xu": "short", "dai": "long", "bui": "bun",
                         "ngan": "short", "hoi": "short",
                         "duoi": "long", "bim": "curly"}.get(
                             goc.get("toc"), "short"),
                "hair_col": "#22222a",
                "kid": bool(goc.get("kid"))}
    if cid in CAST_SKIA_KHOA:
        return dict(CAST_SKIA_KHOA[cid])
    nv = lay_nhan_vat_hieu_luc(cid) or {}
    return {"skin": "fair", "outfit": "hoodie",
            "color": nv.get("mau_ao") or "#888888",
            "hair": "short", "hair_col": "#22222a"}


def viet_du_an_skia(du_lieu, outdir, cue_files, cues,
                    bo_qua_voice=False):
    """Ghi project skia vào outdir/skia-project/: lang.txt,
    script.txt (1 câu/cue), voice.mp3 (nối cue, nghỉ đúng nhịp
    sau mỗi cue), story.json (cast + shots, s = chỉ số câu). bo_qua_voice=True
    khi chỉ xem sheet. Trả (ok, dir, loi)."""
    scenes = du_lieu.get("scenes") or []
    if not scenes:
        return False, None, "Không có cảnh nào."
    proj = os.path.join(outdir, "skia-project")
    os.makedirs(proj, exist_ok=True)
    with open(os.path.join(proj, "lang.txt"), "w",
              encoding="utf-8") as f:
        f.write("vi\n")
    with open(os.path.join(proj, "script.txt"), "w",
              encoding="utf-8") as f:
        for sc in scenes:
            f.write((sc.get("narration") or "").strip() + "\n")
    cast, shots = {}, []
    for i, sc in enumerate(scenes, 1):
        chars = sc.get("characters") or ["cau_ay"]
        ds_char = []
        for j, cid in enumerate(chars):
            if cid not in cast:
                cast[cid] = _cast_skia_cho_nhan_vat(cid) or {}
            n = max(len(chars), 1)
            x = 960 + (j - (n - 1) / 2) * 420
            ds_char.append({"id": cid, "x": int(x), "s": 0.8,
                            "emotion": "neutral",
                            "pose": sc.get("pose") or "stand",
                            "face": 0.6})
        shots.append({"kind": "wide", "s": [i - 1],
                      "set": sc.get("set") or "home",
                      "time": sc.get("time") or "day",
                      "chars": ds_char, "props": []})
    with open(os.path.join(proj, "story.json"), "w",
              encoding="utf-8") as f:
        json.dump({"cast": cast, "shots": shots}, f,
                  ensure_ascii=False, indent=1)
    if bo_qua_voice:
        return True, proj, ""
    try:
        ds, loi_noi = _danh_sach_noi_voice(outdir, cue_files, cues)
        if ds is None:
            return False, None, loi_noi
        lst = os.path.join(outdir, "voice-concat-skia.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in ds:
                f.write("file '%s'\n" % p.replace("'", "'\\''"))
        r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe",
                            "0", "-i", lst,
                            os.path.join(proj, "voice.mp3")],
                           capture_output=True, text=True, timeout=600,
                           **_chay_ngam_kwargs())
        if r.returncode != 0:
            return False, None, ("Nối voice.mp3 lỗi: %s"
                                 % r.stderr[-400:])
    except Exception as e:
        return False, None, "Nối voice.mp3 lỗi: %s" % e
    return True, proj, ""


def render_bang_skia(du_lieu, outdir, cue_files, cues,
                     rong=1280, cao=720, log_cb=None):
    """Dựng video bằng skia: ghi project rồi chạy
    `python3 -m engine all <project>` (align voice -> timing,
    plan, stills, render, audio, final). Trả (ok, {...}, loi).
    Thiếu tài nguyên -> BÁO LỖI RÕ, không render sai lặng lẽ.
    CHƯA kiểm chứng end-to-end trên máy CYAN."""
    def _log(s):
        if log_cb:
            log_cb(s)
    tt = kiem_tra_tai_nguyen_ve()["skia"]
    if not tt["co_san"]:
        return False, {}, ("Chưa đủ tài nguyên skia: %s — ấn nút "
                           "'Tải tài nguyên Skia' ở tab Postman rồi "
                           "thử lại." % "; ".join(tt["thieu"]))
    ok, proj, loi = viet_du_an_skia(du_lieu, outdir, cue_files, cues)
    if not ok:
        return False, {}, loi
    _log("Đang render skia (engine all, project %s)..." % proj)
    env = dict(os.environ)
    env["PYTHONPATH"] = (duong_dan_skia() + os.pathsep
                         + env.get("PYTHONPATH", ""))
    # (v7.25) Đã đóng gói thì sys.executable là exe của tool,
    # KHÔNG phải Python — dùng _python_he_thong(), cwd là thư
    # mục engine skia.
    python = _python_he_thong()
    if not python:
        return False, {}, THIEU_PYTHON_THAT
    try:
        r = subprocess.run([python, "-m", "engine", "all",
                            proj], cwd=duong_dan_skia(), env=env,
                           capture_output=True, text=True, timeout=3600,
                           **_chay_ngam_kwargs())
    except Exception as e:
        return False, {}, "Chạy engine skia lỗi: %s" % e
    if r.returncode != 0:
        return False, {}, ("engine skia lỗi: %s"
                           % (r.stderr or r.stdout)[-800:])
    ung_vien = []
    for noi in (os.path.join(proj, "out"), proj):
        if os.path.isdir(noi):
            for ten in os.listdir(noi):
                if ten.lower().endswith(".mp4"):
                    ung_vien.append(os.path.join(noi, ten))
    if not ung_vien:
        return False, {}, ("engine skia chạy xong nhưng không tìm "
                           "thấy file MP4 final — log: %s"
                           % (r.stdout or "")[-400:])
    final = max(ung_vien, key=os.path.getmtime)
    _log("Render skia xong: %s" % final)
    return True, {"final_mp4": final,
                  "srt": os.path.join(outdir, "postman.srt"),
                  "scenes_mp4": [],
                  "skia_project": proj}, ""


def tao_tab_tao_nhan_vat(parent, quan_ly):
    """Tạo tab 'Tạo nhân vật' — Frame tkinter trong Notebook."""
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog

    class CuaSoTaoNhanVat(tk.Frame):
        def __init__(self, ql, parent=None):
            super().__init__(parent if parent is not None else ql)
            self.quan_ly = ql
            self._anh_preview = None
            self._dung_ui()
            self._nap_danh_sach()

        def _dung_ui(self):
            pad = {"padx": 8, "pady": 4}
            tk.Label(self, text=(
                "Tạo nhân vật — chỉnh thông số code, xem trước cập "
                "nhật ngay, lưu theo tên. Tab Postman 2D chỉ cần gõ "
                "@Tên (vd @Cậu Ấy, @Người Ấy) là lấy đúng nhân vật "
                "này ra dùng, không mô tả lại."),
                wraplength=980, justify="left").pack(fill="x", **pad)
            khung = tk.Frame(self)
            khung.pack(fill="both", expand=True, **pad)
            # Trái: danh sách nhân vật.
            trai = tk.Frame(khung)
            trai.pack(side="left", fill="y", padx=4)
            tk.Label(trai, text="Nhân vật đã lưu:").pack(anchor="w")
            self.list_nv = tk.Listbox(trai, width=26, height=18)
            self.list_nv.pack(fill="y")
            self.list_nv.bind("<<ListboxSelect>>", self._chon_nv)
            tk.Button(trai, text="+ Nhân vật mới",
                      command=self._nv_moi).pack(fill="x", pady=4)
            # Nhân vật có sẵn theo pack (mục F): bấm vào là nạp
            # toàn bộ thông số vào khung chỉnh, sửa rồi lưu dưới
            # tên cậu; nhân vật gốc không sửa trực tiếp.
            tk.Label(trai, text="Nhân vật có sẵn (theo pack):").pack(
                anchor="w", pady=(10, 0))
            tk.Label(trai, text=("Bấm vào là nạp thông số vào khung "
                                 "chỉnh — sửa rồi lưu dưới tên cậu. "
                                 "Nhân vật gốc vẽ theo kiểu của pack "
                                 "đó, không phải kiểu stickman nét "
                                 "mảnh đã khóa."),
                     wraplength=200, justify="left", fg="blue").pack(
                         anchor="w")
            self.list_co_san = tk.Listbox(trai, width=26, height=12)
            self.list_co_san.pack(fill="y")
            self.list_co_san.bind("<<ListboxSelect>>",
                                  self._chon_co_san)
            self._ds_co_san = []
            for pack, code, mo_ta in danh_sach_nhan_vat_co_san():
                self._ds_co_san.append((pack, code))
                self.list_co_san.insert(
                    "end", "%s: %s — %s" % (TEN_PACK.get(pack, pack),
                                            code, mo_ta))
            # Phải: form thông số + xem trước.
            phai = tk.Frame(khung)
            phai.pack(side="left", fill="both", expand=True)
            self.e_id = self._o(phai, "ID (chữ thường, không dấu):", "cau_ay")
            self.e_ten = self._o(phai, "Tên hiển thị (dùng cho tag @Tên):",
                                 "Cậu Ấy")
            self.cb_khan = ttk.Combobox(phai, values=KHAN_LUA_CHON,
                                        state="readonly", width=50)
            tk.Label(phai, text="Loại khăn:").pack(anchor="w")
            self.cb_khan.pack(anchor="w")
            self.cb_khan.set(KHAN_LUA_CHON[0])
            self.cb_khan.bind("<<ComboboxSelected>>",
                              lambda e: self._cap_nhat_xem_truoc())
            self.e_mau_khan = self._o(phai, "Màu khăn (hex):", "#c1272d")
            self.e_mau_ao = self._o(phai, "Màu áo (hex):", "#1a1a1a")
            self.e_nen = self._o(phai, "Nền mặc định:", "trắng")
            self.e_do_cam = self._o(phai, "Đồ cầm mặc định:", "sách")
            tk.Label(phai, text="Tỉ lệ đầu (bán kính đầu / chiều cao):"
                     ).pack(anchor="w")
            self.sl_ti_le = tk.Scale(phai, from_=0.15, to=0.30,
                                     resolution=0.01, orient="horizontal",
                                     length=240,
                                     command=lambda v: self._cap_nhat_xem_truoc())
            self.sl_ti_le.set(0.22)
            self.sl_ti_le.pack(anchor="w")
            tk.Label(phai, text="Độ dày nét (1.0 = chuẩn, nét mảnh):"
                     ).pack(anchor="w")
            self.sl_net = tk.Scale(phai, from_=0.5, to=2.0, resolution=0.1,
                                   orient="horizontal", length=240,
                                   command=lambda v: self._cap_nhat_xem_truoc())
            self.sl_net.set(1.0)
            self.sl_net.pack(anchor="w")
            self.var_glow = tk.BooleanVar(value=False)
            tk.Checkbutton(phai, text="Hào quang vàng ấm + sao lấp lánh",
                           variable=self.var_glow,
                           command=self._cap_nhat_xem_truoc).pack(anchor="w")
            self.e_anh = self._o(phai, "Ảnh mẫu (tùy chọn, đường dẫn):", "")
            tk.Button(phai, text="Chọn ảnh mẫu...",
                      command=self._chon_anh).pack(anchor="w")
            f_btn = tk.Frame(phai)
            f_btn.pack(fill="x", pady=6)
            tk.Button(f_btn, text="Xem trước",
                      command=self._cap_nhat_xem_truoc).pack(side="left", padx=4)
            tk.Button(f_btn, text="Lưu nhân vật",
                      command=self._luu).pack(side="left", padx=4)
            tk.Button(f_btn, text="Xóa bản lưu",
                      command=self._xoa).pack(side="left", padx=4)
            self.lb_tag = tk.Label(phai, text="Tag: @Cậu Ấy", fg="blue")
            self.lb_tag.pack(anchor="w")
            tk.Label(phai, text="Xem trước (cập nhật ngay khi sửa "
                     "thông số):").pack(anchor="w")
            self.lb_preview = tk.Label(phai, text="Chưa xem trước.",
                                       width=60, height=12, bg="white",
                                       relief="sunken")
            self.lb_preview.pack(anchor="w")

        def _o(self, parent, label, mac_dinh=""):
            import tkinter as tk
            tk.Label(parent, text=label).pack(anchor="w")
            e = tk.Entry(parent, width=52)
            e.insert(0, mac_dinh)
            e.pack(anchor="w")
            e.bind("<FocusOut>", lambda ev: self._cap_nhat_xem_truoc())
            return e

        def _nap_danh_sach(self):
            self.list_nv.delete(0, "end")
            self._ds = danh_sach_nhan_vat_day_du()
            for _cid, ten in self._ds:
                self.list_nv.insert("end", ten)

        def _chon_nv(self, _e=None):
            sel = self.list_nv.curselection()
            if not sel:
                return
            cid = self._ds[int(sel[0])][0]
            c = lay_nhan_vat_hieu_luc(cid) or {}
            self._nap_form(cid, c)

        def _chon_co_san(self, _e=None):
            """Chọn 1 nhân vật gốc theo pack: nạp toàn bộ thông số
            vào khung chỉnh (id gợi ý '<code>_<pack>' để lưu dưới
            tên cậu — muốn dùng bằng tag @Tên thì lưu trước đã)."""
            sel = self.list_co_san.curselection()
            if not sel:
                return
            pack, code = self._ds_co_san[int(sel[0])]
            c = nap_nhan_vat_co_san(pack, code)
            if not c:
                return
            self._nap_form("%s_%s" % (code, pack), c)
            self.lb_tag.configure(
                text="Tag: lưu dưới tên cậu trước, rồi gõ @%s"
                     % (c.get("ten") or code))

        def _nap_form(self, cid, c):
            """Nạp 1 spec vào khung chỉnh + cập nhật xem trước."""
            self.e_id.delete(0, "end")
            self.e_id.insert(0, cid)
            self.e_ten.delete(0, "end")
            self.e_ten.insert(0, c.get("ten") or cid)
            khan = c.get("khan") or ""
            if khan in KHAN_LUA_CHON:
                self.cb_khan.set(khan)
            for e, k in ((self.e_mau_khan, "mau_khan"),
                         (self.e_mau_ao, "mau_ao"),
                         (self.e_nen, "nen"),
                         (self.e_do_cam, "do_cam_mac_dinh")):
                e.delete(0, "end")
                e.insert(0, c.get(k) or "")
            self.sl_ti_le.set(float(c.get("ti_le_dau") or 0.22))
            self.sl_net.set(float(c.get("do_day_net") or 1.0))
            self.var_glow.set(bool(c.get("hao_quang")))
            self.e_anh.delete(0, "end")
            self.e_anh.insert(0, (c.get("anh_mau") or [""])[0])
            self.lb_tag.configure(text="Tag: @%s" % (c.get("ten") or cid))
            self._cap_nhat_xem_truoc()

        def _nv_moi(self):
            self.e_id.delete(0, "end")
            self.e_id.insert(0, "nhan_vat_moi")
            self.e_ten.delete(0, "end")
            self.e_ten.insert(0, "Nhân vật mới")
            self._cap_nhat_xem_truoc()

        def _chon_anh(self):
            p = filedialog.askopenfilename(
                title="Chọn ảnh mẫu nhân vật",
                filetypes=[("Ảnh", "*.png *.jpg *.jpeg *.webp"),
                           ("Mọi file", "*.*")])
            if p:
                self.e_anh.delete(0, "end")
                self.e_anh.insert(0, p)
                self._cap_nhat_xem_truoc()

        def _spec_hien_tai(self):
            return {
                "id": self.e_id.get().strip(),
                "ten": self.e_ten.get().strip(),
                "khan": self.cb_khan.get(),
                "mau_khan": self.e_mau_khan.get().strip() or "#c1272d",
                "mau_ao": self.e_mau_ao.get().strip() or "#1a1a1a",
                "nen": self.e_nen.get().strip(),
                "do_cam_mac_dinh": self.e_do_cam.get().strip(),
                "ti_le_dau": float(self.sl_ti_le.get()),
                "do_day_net": float(self.sl_net.get()),
                "kieu_chan": "1 nét",
                "hao_quang": ("vàng ấm + sao lấp lánh"
                              if self.var_glow.get() else ""),
                "giong": "Xuân Vĩnh",
                "has_reference_image": bool(self.e_anh.get().strip()),
                "anh_mau": ([self.e_anh.get().strip()]
                            if self.e_anh.get().strip() else []),
            }

        def _cap_nhat_xem_truoc(self):
            try:
                from PIL import Image, ImageTk
                spec = self._spec_hien_tai()
                # Vẽ thử bằng chính renderer Postman (không cần lưu).
                CHARACTERS["_xem_truoc_"] = spec
                _p, img = render_scene_image(
                    {"characters": ["_xem_truoc_"], "setting": "",
                     "image_prompt": "", "props": {}}, 480, 270)
                del CHARACTERS["_xem_truoc_"]
                self._anh_preview = ImageTk.PhotoImage(img)
                self.lb_preview.configure(image=self._anh_preview, text="")
            except Exception as e:
                self.lb_preview.configure(text="Xem trước lỗi: %s" % e)

        def _luu(self):
            spec = self._spec_hien_tai()
            ok, loi = luu_nhan_vat(spec)
            if not ok:
                messagebox.showerror("Lưu nhân vật", loi)
                return
            self._nap_danh_sach()
            messagebox.showinfo(
                "Lưu nhân vật",
                "Đã lưu '%s' (id: %s). Tag dùng trong Postman: @%s"
                % (spec["ten"], spec["id"], spec["ten"]))

        def _xoa(self):
            cid = self.e_id.get().strip()
            ok, loi = xoa_nhan_vat_da_luu(cid)
            if not ok:
                messagebox.showerror("Xóa bản lưu", loi)
                return
            self._nap_danh_sach()
            messagebox.showinfo("Xóa bản lưu",
                                "Đã xóa bản lưu riêng của '%s'." % cid)

    return CuaSoTaoNhanVat(quan_ly, parent)


# ------------------------------------------------------------------
# 5. Tab Postman 2D trong ChipChipStudio (tkinter, import lười)
# ------------------------------------------------------------------
def tao_tab_postman(parent, quan_ly):
    """Tạo tab 'Postman 2D' — Frame tkinter, dùng chung 1 cửa sổ
    Notebook với các tab khác (không Toplevel). Gọi lười từ
    QuanLy.__init__ của ChipChipStudio v7.24 để file exe không
    bắt buộc có module này mới chạy được các tab cũ."""
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    import threading

    class CuaSoPostman2D(tk.Frame):
        def __init__(self, ql, parent=None):
            super().__init__(parent if parent is not None else ql)
            self.quan_ly = ql
            self.cfg = ql.cfg if hasattr(ql, "cfg") else {}
            self.du_lieu = None
            self.scenes = []
            self.dang_chay = False
            self._dung_ui()

        # ----- giao diện -----
        def _dung_ui(self):
            pad = {"padx": 8, "pady": 4}
            tk.Label(self, text=(
                "Postman 2D — dán JSON kịch bản rồi ấn Áp dụng JSON. "
                "Tool tự nhận các cảnh, tự chia cảnh; mỗi cảnh có ô "
                "prompt tạo video Postman + chọn nhân vật tham chiếu "
                "đã lưu. JSON đồng thời chứa SRT tạo voice — voice "
                "đồng nhất với cảnh trong video."),
                wraplength=980, justify="left").pack(fill="x", **pad)
            # --- Giọng VieNeu (mục C): 2 ô chọn, đủ 25 preset SAU
            # khi tải tài nguyên; trước đó chỉ hiện nhắc tải.
            fr_giong = tk.Frame(self)
            fr_giong.pack(fill="x", **pad)
            tk.Label(fr_giong, text="Giọng đọc:").pack(side="left")
            self.var_giong = tk.StringVar(value=ten_hien_thi_giong(
                VIENEU_VOICE_CHINH))
            self.cb_giong = ttk.Combobox(fr_giong, state="readonly",
                                         width=34,
                                         textvariable=self.var_giong)
            self.cb_giong.pack(side="left", padx=4)
            tk.Label(fr_giong, text="Giọng dự phòng:").pack(side="left")
            self.var_giong_dp = tk.StringVar(value=ten_hien_thi_giong(
                VIENEU_VOICE_DU_PHONG))
            self.cb_giong_dp = ttk.Combobox(
                fr_giong, state="readonly", width=34,
                textvariable=self.var_giong_dp)
            self.cb_giong_dp.pack(side="left", padx=4)
            # --- Model vẽ (mục D): Pillow / Skia 2D / H2 + Phong cách.
            fr_model = tk.Frame(self)
            fr_model.pack(fill="x", **pad)
            tk.Label(fr_model, text="Model vẽ:").pack(side="left")
            self.var_model_ve = tk.StringVar(
                value=MODEL_VE[model_ve_mac_dinh()])
            self.cb_model_ve = ttk.Combobox(fr_model, state="readonly",
                                            width=22,
                                            textvariable=self.var_model_ve)
            self.cb_model_ve["values"] = list(MODEL_VE.values())
            self.cb_model_ve.pack(side="left", padx=4)
            self.cb_model_ve.bind("<<ComboboxSelected>>",
                                  self._doi_model_ve)
            tk.Label(fr_model, text="Phong cách:").pack(side="left")
            self.var_phong_cach = tk.StringVar(
                value=PHONG_CACH_H2["nhan_vat_khoa"])
            self.cb_phong_cach = ttk.Combobox(
                fr_model, state="readonly", width=20,
                textvariable=self.var_phong_cach)
            self.cb_phong_cach["values"] = list(PHONG_CACH_H2.values())
            self.cb_phong_cach.pack(side="left", padx=4)
            # (v7.30) Tự căn lại SRT theo voice thật — mặc định BẬT.
            # Tắt thì tool giữ nguyên SRT ước tính cũ.
            self.var_tu_can_srt = tk.BooleanVar(value=True)
            self.chk_tu_can_srt = tk.Checkbutton(
                fr_model, text="Tự căn SRT theo voice thật",
                variable=self.var_tu_can_srt)
            self.chk_tu_can_srt.pack(side="left", padx=4)
            self.lb_model_note = tk.Label(
                self, text="", wraplength=980, justify="left",
                fg="blue")
            self.lb_model_note.pack(fill="x", **pad)
            # (v7.31) Thư mục SFX + chèn SFX theo JSON. Mốc SFX giữa
            # cue là ƯỚC TÍNH theo vị trí chữ (sai số ~0,3-0,5 giây)
            # vì VieNeu không trả mốc từng từ — ghi rõ, không nói
            # là đo chính xác.
            fr_sfx = tk.Frame(self)
            fr_sfx.pack(fill="x", **pad)
            tk.Label(fr_sfx, text="Thư mục SFX:").pack(side="left")
            self.var_thu_muc_sfx = tk.StringVar(
                value=(self.cfg.get("postman_thu_muc_sfx") or "")
                if isinstance(self.cfg, dict) else "")
            self.ent_thu_muc_sfx = tk.Entry(
                fr_sfx, textvariable=self.var_thu_muc_sfx, width=44,
                state="readonly")
            self.ent_thu_muc_sfx.pack(side="left", padx=4)
            tk.Button(fr_sfx, text="Chọn...",
                      command=self._chon_thu_muc_sfx).pack(side="left",
                                                           padx=4)
            self.lb_sfx_trang_thai = tk.Label(
                fr_sfx, text="Chưa chọn thư mục SFX.", fg="gray")
            self.lb_sfx_trang_thai.pack(side="left", padx=4)
            self.var_chen_sfx = tk.BooleanVar(value=True)
            tk.Checkbutton(fr_sfx, text="Chèn SFX theo JSON",
                           variable=self.var_chen_sfx).pack(side="left",
                                                            padx=4)
            self.lb_sfx_ghi_chu = tk.Label(self, text=(
                "SFX chèn GIỮA CUE, ngay sau cụm neo trong lời kể "
                "(vd chuông báo thức reo sau 'sáu giờ bốn mươi'), "
                "không chèn ở đầu cue hay khoảng chuyển cảnh. Mốc "
                "neo là ước tính theo vị trí chữ (sai số ~0,3-0,5 "
                "giây) — VieNeu không trả mốc từng từ."),
                wraplength=980, justify="left", fg="gray")
            self.lb_sfx_ghi_chu.pack(fill="x", **pad)
            self._cap_nhat_giong()
            self._cap_nhat_model_note()
            self._cap_nhat_trang_thai_sfx()
            tk.Label(self, text="JSON kịch bản Postman:").pack(fill="x", **pad)
            self.txt_json = scrolledtext.ScrolledText(self, height=8)
            self.txt_json.pack(fill="x", **pad)
            f = tk.Frame(self)
            f.pack(fill="x", **pad)
            tk.Button(f, text="Áp dụng JSON",
                      command=self._ap_dung_json).pack(side="left", padx=4)
            tk.Button(f, text="Nạp mẫu Cảnh 1",
                      command=self._nap_mau_canh1).pack(side="left", padx=4)
            tk.Button(f, text="Dán từ clipboard rồi áp dụng",
                      command=self._dan_clipboard).pack(side="left", padx=4)
            tk.Button(f, text="+ Thêm cảnh",
                      command=self._them_canh).pack(side="left", padx=4)
            tk.Button(f, text="Tải tài nguyên (VieNeu)",
                      command=self._tai_tai_nguyen).pack(side="left", padx=4)
            tk.Button(f, text="Tải tài nguyên H2",
                      command=self._tai_tai_nguyen_h2).pack(side="left", padx=4)
            tk.Button(f, text="Tải tài nguyên Skia",
                      command=self._tai_tai_nguyen_skia).pack(side="left", padx=4)
            tk.Button(f, text="Tạo voice (VieNeu)",
                      command=self._tao_voice).pack(side="left", padx=4)
            tk.Button(f, text="Dựng video Postman 2D",
                      command=self._dung_video).pack(side="left", padx=4)
            tk.Button(f, text="Xem sheet",
                      command=self._xem_sheet).pack(side="left", padx=4)
            tk.Button(f, text="Lưu dự án",
                      command=self._luu_du_an).pack(side="left", padx=4)
            tk.Button(f, text="Mở dự án",
                      command=self._mo_du_an).pack(side="left", padx=4)
            tk.Button(f, text="Mở thư mục kết quả",
                      command=self._mo_thu_muc).pack(side="left", padx=4)
            self.lb_trang_thai = tk.Label(
                self, text="Chưa có JSON.", fg="blue")
            self.lb_trang_thai.pack(fill="x", **pad)
            # Danh sách cảnh (trái) + chi tiết cảnh đang chọn (phải).
            khung = tk.Frame(self)
            khung.pack(fill="both", expand=True, **pad)
            self.list_canh = tk.Listbox(khung, width=28)
            self.list_canh.pack(side="left", fill="y", padx=4)
            self.list_canh.bind("<<ListboxSelect>>", self._chon_canh)
            fr = tk.Frame(khung)
            fr.pack(side="left", fill="both", expand=True)
            tk.Label(fr, text="Lời kể (narration):").pack(anchor="w")
            self.txt_loi_ke = scrolledtext.ScrolledText(fr, height=3)
            self.txt_loi_ke.pack(fill="x")
            tk.Label(fr, text="Prompt tạo video Postman (từng cảnh):"
                     ).pack(anchor="w")
            self.txt_prompt = scrolledtext.ScrolledText(fr, height=4)
            self.txt_prompt.pack(fill="x")
            tk.Label(fr, text="Nhân vật tham chiếu (đã lưu + có sẵn "
                     "theo pack — chỉ gọi tên, không mô tả lại):").pack(
                         anchor="w")
            self.cb_nhan_vat = ttk.Combobox(fr, state="readonly", width=40)
            self.cb_nhan_vat["values"] = [
                t for _, t in danh_sach_nhan_vat_chon()]
            self.cb_nhan_vat.pack(anchor="w")
            tk.Button(fr, text="Lưu cảnh đang chọn",
                      command=self._luu_canh).pack(anchor="w", pady=4)
            tk.Label(self, text="Log:").pack(fill="x", **pad)
            self.txt_log = scrolledtext.ScrolledText(
                self, height=8, state="disabled")
            self.txt_log.pack(fill="both", expand=True, **pad)
            self.thu_muc = os.path.join(
                os.path.expanduser("~"), "Desktop", "Postman2D")

        def _log(self, msg):
            try:
                self.txt_log.configure(state="normal")
                self.txt_log.insert("end", str(msg) + "\n")
                self.txt_log.see("end")
                self.txt_log.configure(state="disabled")
            except Exception:
                pass

        # ----- giọng + model vẽ (mục C/D) -----
        def _model_ve_key(self):
            for k, v in MODEL_VE.items():
                if v == self.var_model_ve.get():
                    return k
            return "pillow"

        def _phong_cach_key(self):
            for k, v in PHONG_CACH_H2.items():
                if v == self.var_phong_cach.get():
                    return k
            return "nhan_vat_khoa"

        def _cap_nhat_giong(self):
            """Cập nhật 2 ô chọn giọng (mục C): model đã tải thì
            liệt kê đủ 25 preset (bảng SDK 3.8.5 — đã đối chiếu
            khớp tts.list_preset_voices(), tránh nạp model vào
            RAM chỉ để liệt kê tên); chưa tải thì chỉ hiện nhắc
            tải, không hiện danh sách rỗng. Ngọc Huyền (nữ, Bắc,
            Natural) có trong danh sách, gán được cho nhân vật
            nữ — không ép làm giọng kể chính của Cậu Ấy."""
            ds_giong = [VIENEU_VOICE_CHINH, VIENEU_VOICE_DU_PHONG] + \
                sorted(g for g in VIENEU_VOICES
                       if g not in (VIENEU_VOICE_CHINH,
                                    VIENEU_VOICE_DU_PHONG))
            if vieneu_model_da_tai():
                ds = [ten_hien_thi_giong(g) for g in ds_giong]
                self.cb_giong["values"] = ds
                self.cb_giong_dp["values"] = ds
                if giong_tu_hien_thi(self.var_giong.get()) not in \
                        VIENEU_VOICES:
                    self.var_giong.set(ten_hien_thi_giong(
                        VIENEU_VOICE_CHINH))
                if giong_tu_hien_thi(self.var_giong_dp.get()) not in \
                        VIENEU_VOICES:
                    self.var_giong_dp.set(ten_hien_thi_giong(
                        VIENEU_VOICE_DU_PHONG))
            else:
                nhac = "ấn Tải tài nguyên trước"
                self.cb_giong["values"] = [nhac]
                self.cb_giong_dp["values"] = [nhac]
                self.var_giong.set(nhac)
                self.var_giong_dp.set(nhac)

        def _doi_model_ve(self, _e=None):
            self._cap_nhat_model_note()

        def _cap_nhat_model_note(self):
            """Ghi chú dưới ô Model vẽ: đủ/chưa đủ tài nguyên,
            và cảnh báo chọn pack thì đổi toàn bộ kiểu vẽ + dàn
            nhân vật theo pack đó (mục D)."""
            model = self._model_ve_key()
            tt = kiem_tra_tai_nguyen_ve()
            if model == "h2":
                self.cb_phong_cach.configure(state="readonly")
                if tt["h2"]["co_san"]:
                    note = ("H2 đủ tài nguyên (%s). Chọn pack thì "
                            "đổi toàn bộ kiểu vẽ + dàn nhân vật theo "
                            "pack đó; nhân vật đã khóa chỉ dùng với "
                            "'Nhân vật đã khóa'."
                            % tt["h2"]["chi_tiet"])
                else:
                    note = ("H2 CHƯA đủ tài nguyên: %s — ấn 'Tải tài "
                            "nguyên H2'. Chưa đủ thì dựng video sẽ "
                            "báo lỗi rõ, không render sai lặng lẽ."
                            % "; ".join(tt["h2"]["thieu"]))
            elif model == "skia":
                self.cb_phong_cach.configure(state="disabled")
                note = ("Skia 2D: %s — lưu ý skia vẽ puppet thân "
                        "đầy, KHÔNG có tham số khăn (màu áo lấy "
                        "theo màu khăn để phân biệt); muốn đúng kiểu "
                        "đã khóa thì dùng H2 + 'Nhân vật đã khóa'."
                        % tt["skia"]["chi_tiet"])
                if not tt["skia"]["co_san"]:
                    note += (" Thiếu: %s — ấn 'Tải tài nguyên Skia'."
                             % "; ".join(tt["skia"]["thieu"]))
            else:
                self.cb_phong_cach.configure(state="disabled")
                note = ("Pillow (xem nhanh): renderer tối giản, 1 "
                        "ảnh tĩnh + Ken Burns mỗi cảnh — chỉ để xem "
                        "nhanh, không căn hình theo từng từ trong "
                        "voice.")
            self.lb_model_note.configure(text=note)

        # ----- SFX (v7.31) -----
        def _chon_thu_muc_sfx(self):
            """Chọn thư mục chứa file SFX (lưu mặc định toàn cục
            vào config + theo dự án khi lưu)."""
            duong = filedialog.askdirectory()
            if not duong:
                return
            self.var_thu_muc_sfx.set(duong)
            try:
                if isinstance(self.cfg, dict):
                    self.cfg["postman_thu_muc_sfx"] = duong
            except Exception:
                pass
            if self.du_lieu is not None:
                self.du_lieu["thu_muc_sfx"] = duong
            self._cap_nhat_trang_thai_sfx()
            self._cap_nhat_tom_tat_sfx()
            self._log("Đã chọn thư mục SFX: %s (%d file)."
                      % (duong, dem_file_sfx(duong)))

        def _cap_nhat_trang_thai_sfx(self):
            """Nhãn trạng thái thư mục SFX: số file trong thư mục."""
            try:
                duong = self.var_thu_muc_sfx.get()
            except Exception:
                duong = ""
            if not duong:
                self.lb_sfx_trang_thai.configure(
                    text="Chưa chọn thư mục SFX.", fg="gray")
            elif not os.path.isdir(duong):
                self.lb_sfx_trang_thai.configure(
                    text="Thư mục SFX không tồn tại.", fg="red")
            else:
                self.lb_sfx_trang_thai.configure(
                    text="%d file SFX trong thư mục."
                    % dem_file_sfx(duong), fg="green")

        def _cap_nhat_tom_tat_sfx(self):
            """Tóm tắt SFX của dự án: 1 dòng mỗi cue có SFX (tên —
            sau cụm neo — chèn/chồng — âm lượng — file ✓/✗ thiếu).
            Gọi sau khi áp dụng JSON và sau khi chọn thư mục SFX."""
            if not self.du_lieu:
                return
            thu_muc = self.var_thu_muc_sfx.get()
            co_sfx = False
            for i, sc in enumerate(self.du_lieu.get("scenes") or [], 1):
                ds, _cb = chuan_hoa_sfx_canh(sc)
                sc["sfx_list"] = ds
                for e in ds:
                    co_sfx = True
                    duong = tim_file_sfx(thu_muc, e.get("file") or "")
                    neo = e.get("neo_vao_cum") or ""
                    cach = ("chèn" if e.get("cach_chen") == "chen"
                            else "chồng")
                    self._log(
                        "SFX cue %d: %s — %s — %s — %d%% — file %s %s"
                        % (i, e.get("ten"),
                           ("sau '%s'" % neo) if neo else "đầu cue",
                           cach, int(round(
                               float(e.get("am_luong") or 0) * 100)),
                           e.get("file") or "(chưa có file)",
                           "✓" if duong else "✗ thiếu"))
            if co_sfx and not thu_muc:
                self._log("SFX: chưa chọn thư mục SFX — chọn thư mục "
                          "chứa file SFX rồi chạy lại (không thì SFX "
                          "sẽ bị bỏ qua).")

        def _du_an_co_sfx(self):
            """Dự án hiện tại có SFX nào không (kể cả field cũ)."""
            if not self.du_lieu:
                return False
            for sc in self.du_lieu.get("scenes") or []:
                ds, _cb = chuan_hoa_sfx_canh(sc)
                if ds:
                    return True
            return False

        def _log_bao_cao_sfx(self, kq):
            """Ghi báo cáo SFX sau khi chạy: từng SFX đã chèn với
            mốc tuyệt đối cuối cùng + file nào thiếu."""
            if not kq:
                return
            if kq.get("sfx_bo_qua"):
                self._log("SFX: " + kq["sfx_bo_qua"])
            for b in kq.get("bao_cao_sfx") or []:
                if b.get("trang_thai") == "da_chen":
                    self._log(
                        "SFX cue %s: '%s' chèn lúc %.3fs (kết thúc "
                        "%.3fs) — %s." % (
                            b.get("cue"), b.get("ten"),
                            b.get("sfx_moc_giay"),
                            b.get("sfx_ket_thuc_giay"),
                            b.get("cach_chen")))
            if kq.get("voice_sfx_mp3"):
                self._log("File voice+SFX: %s" % kq["voice_sfx_mp3"])
                self._log("SRT voice+SFX: %s" % kq["voice_sfx_srt"])
                self._log("JSON voice+SFX: %s"
                          % kq["postman_sfx_json"])
            if kq.get("sfx_thieu"):
                self._log("SFX thiếu file (%d): %s."
                          % (len(kq["sfx_thieu"]),
                             ", ".join(sorted(set(kq["sfx_thieu"])))))

        def _tai_tai_nguyen_h2(self):
            self._log("Đang tải tài nguyên H2 (copy kit + npm install "
                      "+ Chromium, ~400 MB, chờ vài phút)...")
            t = threading.Thread(target=self._tai_tai_nguyen_h2_bg,
                                 daemon=True)
            t.start()

        def _tai_tai_nguyen_h2_bg(self):
            ok, loi = tai_tai_nguyen_h2(self._log)
            self._log(("OK: đã tải xong tài nguyên H2." if ok
                       else "LỖI tải H2: " + loi))
            if not ok:
                messagebox.showerror("Tải tài nguyên H2", loi)
            self.after(0, self._cap_nhat_model_note)

        def _tai_tai_nguyen_skia(self):
            self._log("Đang tải tài nguyên skia (copy engine + pip "
                      "install skia-python)...")
            t = threading.Thread(target=self._tai_tai_nguyen_skia_bg,
                                 daemon=True)
            t.start()

        def _tai_tai_nguyen_skia_bg(self):
            ok, loi = tai_tai_nguyen_skia(self._log)
            self._log(("OK: đã tải xong tài nguyên skia." if ok
                       else "LỖI tải skia: " + loi))
            if not ok:
                messagebox.showerror("Tải tài nguyên Skia", loi)
            self.after(0, self._cap_nhat_model_note)

        def _xem_sheet(self):
            """Xem sheet (bảng cảnh) bằng đúng model đã chọn:
            Pillow -> ảnh tĩnh cảnh 1; H2 -> node render.mjs
            --sheet; skia -> python -m engine stills."""
            if not self.du_lieu:
                messagebox.showerror("Chưa có JSON",
                                     "Dán JSON rồi ấn Áp dụng JSON "
                                     "trước.")
                return
            t = threading.Thread(target=self._xem_sheet_bg, daemon=True)
            t.start()

        def _xem_sheet_bg(self):
            model = self._model_ve_key()
            os.makedirs(self.thu_muc, exist_ok=True)
            if model == "pillow":
                try:
                    _duong, img = render_scene_image(self.scenes[0],
                                                     1280, 720)
                except Exception as e:
                    self._log("LỖI xem sheet Pillow: %s" % e)
                    return
                duong = os.path.join(self.thu_muc, "sheet-pillow.png")
                img.save(duong)
                self._log("Sheet Pillow (cảnh 1): %s" % duong)
                self._mo_file(duong)
                return
            if model == "h2":
                tt = kiem_tra_tai_nguyen_ve()["h2"]
                if not tt["co_san"]:
                    self._log("LỖI xem sheet H2: chưa đủ tài nguyên: "
                              "%s" % "; ".join(tt["thieu"]))
                    messagebox.showerror(
                        "Chưa đủ tài nguyên H2",
                        "Chưa đủ tài nguyên H2: %s — ấn 'Tải tài "
                        "nguyên H2' trước." % "; ".join(tt["thieu"]))
                    return
                ok, proj, cb = viet_du_an_h2(
                    self.du_lieu, self.thu_muc, self._phong_cach_key(),
                    [], self.du_lieu.get("srt_cues") or
                    build_srt_cues(self.scenes, 0.95), bo_qua_voice=True)
                if not ok:
                    self._log("LỖI ghi project H2: %s" % cb)
                    return
                if cb:
                    self._log("CẢNH BÁO H2: " + cb)
                kit_dir = os.path.join(duong_dan_h2(), "kit")
                try:
                    r = subprocess.run(
                        ["node", "render.mjs", "--project", proj,
                         "--sheet"], cwd=kit_dir, capture_output=True,
                        text=True, timeout=900, **_chay_ngam_kwargs())
                except Exception as e:
                    self._log("LỖI chạy render.mjs --sheet: %s" % e)
                    return
                if r.returncode != 0:
                    self._log("LỖI render sheet H2: %s"
                              % (r.stderr or r.stdout)[-500:])
                    return
                jpg = [os.path.join(proj, f) for f in os.listdir(proj)
                       if f.lower().endswith((".jpg", ".png"))]
                if not jpg:
                    self._log("render --sheet xong nhưng không thấy "
                              "file ảnh sheet trong project.")
                    return
                duong = max(jpg, key=os.path.getmtime)
                self._log("Sheet H2: %s" % duong)
                self._mo_file(duong)
                return
            # skia
            tt = kiem_tra_tai_nguyen_ve()["skia"]
            if not tt["co_san"]:
                self._log("LỖI xem sheet skia: chưa đủ tài nguyên: "
                          "%s" % "; ".join(tt["thieu"]))
                messagebox.showerror(
                    "Chưa đủ tài nguyên skia",
                    "Chưa đủ tài nguyên skia: %s — ấn 'Tải tài "
                    "nguyên Skia' trước." % "; ".join(tt["thieu"]))
                return
            ok, proj, loi = viet_du_an_skia(
                self.du_lieu, self.thu_muc, [],
                self.du_lieu.get("srt_cues") or
                build_srt_cues(self.scenes, 0.95))
            if not ok:
                self._log("LỖI ghi project skia: %s" % loi)
                return
            env = dict(os.environ)
            env["PYTHONPATH"] = (duong_dan_skia() + os.pathsep
                                 + env.get("PYTHONPATH", ""))
            # (v7.25) Đã đóng gói thì sys.executable là exe của tool,
            # KHÔNG phải Python — dùng _python_he_thong().
            python = _python_he_thong()
            if not python:
                self._log("LỖI xem sheet skia: " + THIEU_PYTHON_THAT)
                return
            try:
                r = subprocess.run(
                    [python, "-m", "engine", "stills", proj],
                    cwd=duong_dan_skia(), env=env, capture_output=True,
                    text=True, timeout=900, **_chay_ngam_kwargs())
            except Exception as e:
                self._log("LỖI chạy engine stills: %s" % e)
                return
            if r.returncode != 0:
                self._log("LỖI stills skia: %s"
                          % (r.stderr or r.stdout)[-500:])
                return
            anh = []
            for root, _ds, files in os.walk(proj):
                for f in files:
                    if f.lower().endswith((".jpg", ".png")):
                        anh.append(os.path.join(root, f))
            if not anh:
                self._log("stills skia xong nhưng không thấy ảnh.")
                return
            duong = max(anh, key=os.path.getmtime)
            self._log("Sheet skia: %s" % duong)
            self._mo_file(duong)

        def _mo_file(self, duong_dan):
            """Mở file/ảnh bằng chương trình mặc định (lệnh mở có
            chủ đích — không dùng chay_ngam_kwargs)."""
            try:
                os.startfile(duong_dan)  # Windows
            except Exception:
                subprocess.run(["xdg-open", duong_dan])

        def _luu_du_an(self):
            """Lưu dự án (JSON kịch bản + giọng + model vẽ +
            phong cách) ra file — lựa chọn lưu theo từng dự án
            (mục D)."""
            if not self.du_lieu:
                messagebox.showerror("Chưa có dự án",
                                     "Dán JSON rồi ấn Áp dụng JSON "
                                     "trước.")
                return
            self._dong_bo_lua_chon()
            duong = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json")],
                initialfile="postman-project.json")
            if not duong:
                return
            try:
                with open(duong, "w", encoding="utf-8") as f:
                    json.dump(self.du_lieu, f, ensure_ascii=False,
                              indent=1)
                self._log("Đã lưu dự án: %s" % duong)
            except Exception as e:
                messagebox.showerror("Lưu dự án", str(e))

        def _mo_du_an(self):
            duong = filedialog.askopenfilename(
                filetypes=[("JSON", "*.json")])
            if not duong:
                return
            try:
                with open(duong, "r", encoding="utf-8") as f:
                    self.txt_json.delete("1.0", "end")
                    self.txt_json.insert("1.0", f.read())
            except Exception as e:
                messagebox.showerror("Mở dự án", str(e))
                return
            self._ap_dung_json()
            self._log("Đã mở dự án: %s" % duong)

        def _dong_bo_lua_chon(self):
            """Ghi lựa chọn giọng/model/phong cách ở UI vào du_lieu
            (để lưu theo từng dự án + dựng video dùng đúng)."""
            if not self.du_lieu:
                return
            v = self.du_lieu.setdefault("voice_settings", {})
            g = giong_tu_hien_thi(self.var_giong.get())
            g_dp = giong_tu_hien_thi(self.var_giong_dp.get())
            if g in VIENEU_VOICES:
                v["voice"] = g
            if g_dp in VIENEU_VOICES:
                v["voice_du_phong"] = g_dp
            self.du_lieu["model_ve"] = self._model_ve_key()
            self.du_lieu["phong_cach"] = self._phong_cach_key()
            # (v7.30) Tự căn SRT theo voice thật — lưu theo dự án.
            self.du_lieu["tu_can_srt_theo_voice"] = bool(
                self.var_tu_can_srt.get())
            # (v7.31) Thư mục SFX + cờ chèn SFX — lưu theo dự án.
            self.du_lieu["thu_muc_sfx"] = self.var_thu_muc_sfx.get()
            self.du_lieu["chen_sfx_theo_json"] = bool(
                self.var_chen_sfx.get())

        def _nap_mau_canh1(self):
            """(v7.24-merge) Nap SCRIPT_CANH1_POSTMAN.json (5 canh 1.1-1.5,
            da tao va kiem chung khop tung chu voi KICH_BAN_KEY1_PHAN1.md).
            Khong co file thi bao ro, khong crash, khong tao file gia."""
            ung_vien = [
                os.path.expanduser("~/workspace/goals/bilingual-faceless-"
                                   "youtube-channels-secret-love/files/"
                                   "SCRIPT_CANH1_POSTMAN.json"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "..", "goals", "bilingual-faceless-"
                             "youtube-channels-secret-love", "files",
                             "SCRIPT_CANH1_POSTMAN.json"),
            ]
            duong_dan = None
            for _u in ung_vien:
                if _u and os.path.isfile(_u):
                    duong_dan = _u
                    break
            if not duong_dan:
                messagebox.showinfo(
                    "Chưa có file mẫu",
                    "Chưa có file mẫu SCRIPT_CANH1_POSTMAN.json trong "
                    "workspace/goals/bilingual-faceless-youtube-channels-"
                    "secret-love/files/.")
                self._log("Chưa có file mẫu Cảnh 1 để nạp.")
                return
            try:
                with open(duong_dan, "r", encoding="utf-8") as _f:
                    self.txt_json.delete("1.0", "end")
                    self.txt_json.insert("1.0", _f.read())
                self._ap_dung_json()
                self._log("Đã nạp mẫu Cảnh 1 từ: %s" % duong_dan)
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Lỗi nạp mẫu", str(exc))
                self._log("LỖI nạp mẫu Cảnh 1: %s" % exc)

        def _ap_dung_json(self):
            du_lieu, loi = parse_postman_json(
                self.txt_json.get("1.0", "end"))
            if not du_lieu:
                messagebox.showerror("JSON lỗi", loi)
                return
            self.du_lieu = du_lieu
            self.scenes = du_lieu["scenes"]
            self._ve_list_canh()
            # Khôi phục lựa chọn giọng/model/phong cách của dự án
            # (chỉ khi dropdown đã liệt kê được giọng).
            v = du_lieu.get("voice_settings") or {}
            if vieneu_model_da_tai():
                if v.get("voice") in VIENEU_VOICES:
                    self.var_giong.set(ten_hien_thi_giong(v["voice"]))
                if v.get("voice_du_phong") in VIENEU_VOICES:
                    self.var_giong_dp.set(ten_hien_thi_giong(
                        v["voice_du_phong"]))
            if du_lieu.get("model_ve") in MODEL_VE:
                self.var_model_ve.set(MODEL_VE[du_lieu["model_ve"]])
            if du_lieu.get("phong_cach") in PHONG_CACH_H2:
                self.var_phong_cach.set(
                    PHONG_CACH_H2[du_lieu["phong_cach"]])
            # (v7.30) Khôi phục nút tự căn SRT của dự án (mặc định BẬT).
            if "tu_can_srt_theo_voice" in du_lieu:
                self.var_tu_can_srt.set(
                    bool(du_lieu["tu_can_srt_theo_voice"]))
            # (v7.31) Khôi phục thư mục SFX + cờ chèn SFX của dự án.
            if du_lieu.get("thu_muc_sfx"):
                self.var_thu_muc_sfx.set(du_lieu["thu_muc_sfx"])
            if "chen_sfx_theo_json" in du_lieu:
                self.var_chen_sfx.set(
                    bool(du_lieu["chen_sfx_theo_json"]))
            self._cap_nhat_trang_thai_sfx()
            self._cap_nhat_model_note()
            moc = ("mốc SRT theo JSON" if du_lieu.get("srt_tu_json")
                   else "mốc SRT ước tính (JSON không có srt_cues)")
            self.lb_trang_thai.configure(
                text=("Đã nhận %d cảnh — giọng %s, tốc độ %.2fx, "
                      "tổng ước tính %.1f giây; %s."
                      % (len(self.scenes),
                         du_lieu["voice_settings"]["voice"],
                         du_lieu["voice_settings"]["speed"],
                         du_lieu["tong_thoi_luong_uoc_tinh_giay"], moc)))
            for cb in du_lieu.get("canh_bao") or []:
                self._log("CẢNH BÁO: " + cb)
            self._log("Đã áp dụng JSON: %d cảnh, %d cue SRT."
                      % (len(self.scenes), len(du_lieu["srt_cues"])))
            # (v7.31) Tóm tắt SFX từng cue (tên — cụm neo — chèn/
            # chồng — âm lượng — file ✓/✗ thiếu).
            self._cap_nhat_tom_tat_sfx()

        def _dan_clipboard(self):
            try:
                self.txt_json.delete("1.0", "end")
                self.txt_json.insert("1.0", self.clipboard_get())
            except Exception as e:
                messagebox.showerror("Clipboard", str(e))
                return
            self._ap_dung_json()

        def _ve_list_canh(self):
            self.list_canh.delete(0, "end")
            for s in self.scenes:
                self.list_canh.insert(
                    "end", "%s — %s" % (s["id"], s.get("title", "")))

        def _chon_canh(self, _e=None):
            sel = self.list_canh.curselection()
            if not sel:
                return
            s = self.scenes[int(sel[0])]
            for w, key in ((self.txt_loi_ke, "narration"),
                           (self.txt_prompt, "prompt_video_postman")):
                w.delete("1.0", "end")
                w.insert("1.0", s.get(key) or "")
            chars = s.get("characters") or ["cau_ay"]
            ten = dict(danh_sach_nhan_vat_chon()).get(chars[0], "")
            self.cb_nhan_vat.set(ten)

        def _luu_canh(self):
            sel = self.list_canh.curselection()
            if not sel:
                return
            s = self.scenes[int(sel[0])]
            s["narration"] = self.txt_loi_ke.get("1.0", "end").strip()
            s["prompt_video_postman"] = self.txt_prompt.get("1.0",
                                                            "end").strip()
            ten = self.cb_nhan_vat.get()
            for cid, t in danh_sach_nhan_vat_chon():
                if t == ten:
                    s["characters"] = [cid] + [c for c in s["characters"]
                                               if c != cid]
            # Thời lượng ở đây chỉ là ước tính tạm — thời lượng
            # thật được đo từ file voice khi dựng (mục G).
            s["duration_s"] = round(
                uoc_tinh_thoi_luong_giay(
                    s["narration"],
                    self.du_lieu["voice_settings"]["speed"]), 2)
            if self.du_lieu:
                self.du_lieu["srt_cues"] = build_srt_cues(
                    self.scenes, self.du_lieu["voice_settings"]["speed"])
                self.du_lieu["srt_tu_json"] = False
            self._log("Đã lưu cảnh %s (SRT căn lại theo lời kể mới — "
                      "ước tính tạm, dựng video sẽ đo lại bằng voice "
                      "thật)." % s["id"])

        def _them_canh(self):
            if not self.scenes and not self.du_lieu:
                self.du_lieu = {"voice_settings": {
                    "engine": "vieneu", "voice": VIENEU_VOICE_CHINH,
                    "voice_du_phong": VIENEU_VOICE_DU_PHONG,
                    "speed": 0.95, "pitch": 0}, "scenes": []}
                self.scenes = []
            sel = self.list_canh.curselection()
            sau = (self.scenes[int(sel[0])]["id"] if sel else None)
            self.scenes = them_canh(self.scenes, sau)
            if self.du_lieu:
                self.du_lieu["scenes"] = self.scenes
                self.du_lieu["srt_cues"] = build_srt_cues(
                    self.scenes, self.du_lieu["voice_settings"]["speed"])
            self._ve_list_canh()
            self._log("Đã thêm 1 cảnh (tổng %d cảnh)."
                      % len(self.scenes))

        def _tai_tai_nguyen(self):
            # (v7.25) Chống bấm chồng nhau: đang tải mà bấm lại thì
            # chỉ log và bỏ qua, không chạy thêm thread tải nữa.
            if getattr(self, "_dang_tai_tai_nguyen", False):
                self._log("Đang tải tài nguyên VieNeu rồi — "
                          "bấm lại cũng không tải thêm.")
                return
            self._dang_tai_tai_nguyen = True
            self._log("Đang tải tài nguyên VieNeu (pip install vieneu "
                      "+ tải model lần đầu)...")
            t = threading.Thread(target=self._tai_tai_nguyen_bg,
                                 daemon=True)
            t.start()

        def _tai_tai_nguyen_bg(self):
            try:
                ok, msg = tai_tai_nguyen_vieneu(self._log)
                self._log(("OK: " if ok else "LỖI: ") + msg)
                if not ok:
                    messagebox.showerror("Tải tài nguyên", msg)
                else:
                    # Model vừa tải xong -> liệt kê đủ 25 giọng.
                    self.after(0, self._cap_nhat_giong)
            finally:
                self._dang_tai_tai_nguyen = False

        def _tao_voice(self):
            if not self.du_lieu:
                messagebox.showerror("Chưa có JSON",
                                     "Dán JSON rồi ấn Áp dụng JSON trước.")
                return
            # Đọc lựa chọn giọng ở luồng UI rồi mới chạy nền.
            self._dong_bo_lua_chon()
            # (v7.31) JSON có SFX + chèn SFX BẬT mà chưa chọn thư
            # mục SFX -> báo rõ, chưa chạy (tránh chạy xong mới
            # biết thiếu SFX). Tắt cờ "Chèn SFX theo JSON" thì
            # chạy voice thường.
            if self.var_chen_sfx.get() and self._du_an_co_sfx():
                if not self.var_thu_muc_sfx.get():
                    messagebox.showerror(
                        "Chưa chọn thư mục SFX",
                        "JSON này có hiệu ứng âm (SFX) nhưng chưa "
                        "chọn thư mục chứa file SFX.\n\nChọn thư mục "
                        "SFX ở hàng 'Thư mục SFX' rồi bấm lại, hoặc "
                        "tắt 'Chèn SFX theo JSON' để tạo voice "
                        "thường (không SFX).")
                    self._log("Chưa chạy: JSON có SFX nhưng chưa chọn "
                              "thư mục SFX.")
                    return
            v = self.du_lieu["voice_settings"]
            t = threading.Thread(
                target=self._tao_voice_bg,
                args=(v["voice"], v.get("voice_du_phong")
                      or VIENEU_VOICE_DU_PHONG, v["speed"],
                      self.du_lieu.get("tu_can_srt_theo_voice", True),
                      self.var_thu_muc_sfx.get(),
                      self.var_chen_sfx.get()),
                daemon=True)
            t.start()

        def _tao_voice_bg(self, giong, giong_dp, toc_do, tu_can_srt=True,
                          thu_muc_sfx=None, chen_sfx=True):
            os.makedirs(self.thu_muc, exist_ok=True)
            for i, sc in enumerate(self.scenes, 1):
                mp3 = os.path.join(self.thu_muc, "cue_%02d.mp3" % i)
                ok, _, loi = doc_voice_vieneu(
                    sc["narration"], giong, toc_do, mp3, self._log,
                    giong_du_phong=giong_dp)
                if not ok:
                    self._log("LỖI voice cảnh %s: %s" % (sc["id"], loi))
                    return
                # Đo thời lượng thật để căn lại SRT (mục G).
                d_that = _do_dai_audio_giay(mp3)
                if d_that:
                    sc["duration_s"] = round(d_that, 2)
                self._log("Xong voice cảnh %s: %s" % (sc["id"], mp3))
            # (v7.31) SFX + tự căn lại SRT theo voice thật (nếu bật).
            if self.du_lieu and tu_can_srt:
                _ok, kq, _loi = xu_ly_sfx_sau_voice(
                    self.du_lieu, self.thu_muc,
                    [os.path.join(self.thu_muc, "cue_%02d.mp3" % i)
                     for i in range(1, len(self.scenes) + 1)],
                    self._log, thu_muc_sfx, chen_sfx, tu_can_srt)
                write_srt(self.du_lieu["srt_cues"],
                          os.path.join(self.thu_muc, "postman.srt"))
                tong = self.du_lieu.get("tong_thoi_luong_that_giay", 0)
                self._log("Đã căn lại SRT theo voice thật: tổng %.1fs "
                          "(khoảng chờ giữa cue 5ms)." % tong)
                self._log_bao_cao_sfx(kq)
            else:
                write_srt(self.du_lieu["srt_cues"],
                          os.path.join(self.thu_muc, "postman.srt"))
            self._log("Đã tạo xong voice + SRT trong: %s" % self.thu_muc)

        def _dung_video(self):
            if not self.du_lieu:
                messagebox.showerror("Chưa có JSON",
                                     "Dán JSON rồi ấn Áp dụng JSON trước.")
                return
            self._dong_bo_lua_chon()
            # (v7.31) Chặn giống nút Tạo voice: JSON có SFX + chèn
            # SFX BẬT mà chưa chọn thư mục SFX -> báo rõ, chưa chạy.
            if self.var_chen_sfx.get() and self._du_an_co_sfx():
                if not self.var_thu_muc_sfx.get():
                    messagebox.showerror(
                        "Chưa chọn thư mục SFX",
                        "JSON này có hiệu ứng âm (SFX) nhưng chưa "
                        "chọn thư mục chứa file SFX.\n\nChọn thư mục "
                        "SFX ở hàng 'Thư mục SFX' rồi bấm lại, hoặc "
                        "tắt 'Chèn SFX theo JSON' để dựng video "
                        "thường (không SFX).")
                    self._log("Chưa chạy: JSON có SFX nhưng chưa chọn "
                              "thư mục SFX.")
                    return
            t = threading.Thread(
                target=self._dung_video_bg,
                args=(self.du_lieu.get("model_ve") or "pillow",
                      self.du_lieu.get("phong_cach")
                      or "nhan_vat_khoa",
                      self.du_lieu.get("tu_can_srt_theo_voice", True),
                      self.var_thu_muc_sfx.get(),
                      self.var_chen_sfx.get()),
                daemon=True)
            t.start()

        def _dung_video_bg(self, model_ve, phong_cach, tu_can_srt=True,
                           thu_muc_sfx=None, chen_sfx=True):
            ok, ket_qua, loi = render_project(
                self.du_lieu, self.thu_muc, log_cb=self._log,
                model_ve=model_ve, phong_cach=phong_cach,
                tu_can_srt_theo_voice=tu_can_srt,
                thu_muc_sfx=thu_muc_sfx, chen_sfx=chen_sfx)
            if ok:
                self._log("HOÀN TẤT: %s" % ket_qua["final_mp4"])
                self._log_bao_cao_sfx(ket_qua)
            else:
                self._log("LỖI dựng video: " + loi)
                messagebox.showerror("Dựng video", loi)

        def _mo_thu_muc(self):
            os.makedirs(self.thu_muc, exist_ok=True)
            try:
                os.startfile(self.thu_muc)  # Windows
            except Exception:
                subprocess.run(["xdg-open", self.thu_muc])

    return CuaSoPostman2D(quan_ly, parent)


# ------------------------------------------------------------------
# Self-test (chạy: python3 postman2d.py)
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("Postman 2D module v%s" % VERSION_POSTMAN)
    print("Nhan vat:", [c for c in CHARACTERS])
    print("VieNeu check:", kiem_tra_vieneu())
    mau = {"postman": {"title": "Test", "voice_settings": {
        "voice": "Xuân Vĩnh", "speed": 0.95}},
        "scenes": [{"id": "1.1", "narration": "Sáng thứ Hai, sáu giờ "
                    "bốn mươi, bạn thức dậy.",
                    "characters": ["cau_ay", "me"],
                    "number": {"value": 312, "character_id": "me"}}]}
    dl, loi = parse_postman_json(mau)
    assert dl and not loi, loi
    assert len(dl["scenes"]) == 1 and len(dl["srt_cues"]) == 1
    assert dl["voice_settings"]["voice"] == "Xuân Vĩnh"
    print("parse OK: 1 scene, cue:", dl["srt_cues"][0])
    p, _img = render_scene_image(dl["scenes"][0], 640, 360,
                                 "/tmp/postman-test-1.1.png")
    print("render image OK:", p)
    print("SELF-TEST OK (voice/render video cần VieNeu + ffmpeg, "
          "chưa chạy ở đây).")

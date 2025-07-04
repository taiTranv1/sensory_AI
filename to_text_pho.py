import whisper

AUDIO_FILE = "data/HD_060425_trang_s1_A_M1.wav"
OUTPUT_TEXT_FILE = "HD_060425_trang_s1_A_M1_Wm.txt"

# Tải mô hình (có thể chọn tiny, base, small, medium, large)
model = whisper.load_model("medium")

# Nhận diện và chuyển thành text
result = model.transcribe(AUDIO_FILE, language="vi")

# Ghi ra file
with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Đã lưu văn bản tại: {OUTPUT_TEXT_FILE}")
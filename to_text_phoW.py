import os
import torchaudio
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# --- CẤU HÌNH ---
AUDIO_FILE = "data/HD_060425_trang_s1_A_M1.wav"
OUTPUT_TEXT_FILE = "HD_060425_trang_s1_A_M1_PWs.txt"
CHUNK_DURATION_SEC = 30

# --- BACKEND AN TOÀN ---
torchaudio.set_audio_backend("soundfil")  # Cần có ffmpeg/sox, hoặc dùng "soundfile"

# --- B1: KIỂM TRA FILE ---
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Không tìm thấy file: {AUDIO_FILE}")

# --- B2: TẢI MÔ HÌNH ---
print("📥 Đang tải mô hình PhoWhisper...")
model = WhisperForConditionalGeneration.from_pretrained("vinai/PhoWhisper-small") #small, medium, large
processor = WhisperProcessor.from_pretrained("vinai/PhoWhisper-small")

# --- B3: LOAD ÂM THANH ---
try:
    waveform, sr = torchaudio.load(AUDIO_FILE)
except Exception as e:
    raise RuntimeError(f"Lỗi khi load file âm thanh: {e}")

waveform = waveform[0]  # Chọn 1 kênh nếu stereo

# --- B4: RESAMPLE nếu không phải 16000 Hz ---
if sr != 16000:
    print(f"⚠ Đổi sample rate từ {sr} Hz → 16000 Hz")
    resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
    waveform = resampler(waveform)
    sr = 16000

# --- B5: CHIA THÀNH ĐOẠN ---
chunk_samples = CHUNK_DURATION_SEC * sr
chunks = [waveform[i:i + chunk_samples] for i in range(0, len(waveform), chunk_samples)]

# --- B6: XỬ LÝ TỪNG ĐOẠN ---
results = []
print(f"🔁 Xử lý {len(chunks)} đoạn âm thanh...")

for idx, chunk in enumerate(chunks):
    inputs = processor(chunk, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        predicted_ids = model.generate(**inputs)
    text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    results.append(text)
    print(f"✅ Đoạn {idx+1}/{len(chunks)}: {len(text)} ký tự")

# --- B7: GHI FILE TXT ---
full_text = "\n".join(results)
with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"\n📄 Hoàn tất! Đã lưu văn bản tại: {OUTPUT_TEXT_FILE}")

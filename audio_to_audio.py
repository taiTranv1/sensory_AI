import subprocess

def convert_to_wav(input_path, output_path):
    """
    Chuyển đổi file audio sang WAV với tần số lấy mẫu 16kHz bằng ffmpeg.
    """
    command = [
        "ffmpeg",
        "-i", input_path,
        "-ar", "16000",  # tần số lấy mẫu 16kHz
        "-ac", "1",      # chuyển sang mono
        output_path
    ]
    subprocess.run(command, check=True)

# Ví dụ sử dụng:
convert_to_wav("data/HD_060425_trang_s1_A_M1.m4a", "HD_060425_trang_s1_A_M1.wav")
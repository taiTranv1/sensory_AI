import re
import evaluate

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().strip()

def main(ground_truth_path, hypothesis_path):
    # Đọc nội dung
    ground_truth = read_file(ground_truth_path)
    hypothesis = read_file(hypothesis_path)

    # Chuẩn hóa
    ground_truth_norm = normalize(ground_truth)
    hypothesis_norm = normalize(hypothesis)

    # Tính WER
    wer_metric = evaluate.load("wer")
    wer = wer_metric.compute(predictions=[hypothesis_norm], references=[ground_truth_norm])

    # In kết quả
    print("📄 Ground Truth:", ground_truth)
    print("📄 Hypothesis:", hypothesis)
    print(f"\n📏 Word Error Rate (WER): {wer:.2%}")

if __name__ == "__main__":
    ground_truth_file = "text_01.txt"
    hypothesis_file = "hien_01_large.txt"
    main(ground_truth_file, hypothesis_file)

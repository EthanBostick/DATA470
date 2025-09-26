from deepmultilingualpunctuation import PunctuationModel
import torch
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------- Configuration --------
INPUT_FILE = "superCorpus.txt"
OUTPUT_FILE = "clnPrimeCorpus.txt"
CHUNK_SIZE = 500         # words per chunk
MAX_WORKERS = 8          # number of CPU threads
# --------------------------------

# Force GPU if available
os.environ["CUDA_VISIBLE_DEVICES"] = "0" if torch.cuda.is_available() else ""
device_name = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device_name}")

# Load model
model = PunctuationModel()

def restore_chunk(chunk):
    try:
        return model.restore_punctuation(chunk)
    except Exception as e:
        print(f"Error restoring chunk: {e}")
        return chunk  # fallback

def restore_punctuation_parallel(text, chunk_size=CHUNK_SIZE, max_workers=MAX_WORKERS):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    restored_chunks = [None] * len(chunks)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(restore_chunk, chunk): idx for idx, chunk in enumerate(chunks)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            restored_chunks[idx] = future.result()

    return " ".join(restored_chunks)

# -------- Main Processing --------
if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        corpus = f.read()

    print("Restoring punctuation in parallel... this may take a while for large corpora.")
    restored_corpus = restore_punctuation_parallel(corpus)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(restored_corpus)

    print(f"Punctuation restoration complete! Output written to {OUTPUT_FILE}")


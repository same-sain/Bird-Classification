import os
import threading
from pydub import AudioSegment
from tqdm import tqdm

BASE_DIR = "./datasets"
OUT_DIR = "./wav"

def convert(dir):
    src_dir = os.path.join(BASE_DIR, dir)
    dest_dir = os.path.join(OUT_DIR, dir)
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    files = [f for f in os.listdir(src_dir) if f.endswith('.mp3')]
    
    for file in tqdm(files, desc=f'Converting {dir}'):
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file.replace(".mp3", ".wav"))
        
        try:
            sound = AudioSegment.from_mp3(src_path)
            sound = sound.set_frame_rate(16000).set_channels(1)
            sound.export(dest_path, format="wav")
            os.remove(src_path)  # Remove the original MP3 file
        except Exception as e:
            print(f'Error processing {src_path}: {e}')

def process_folders(folders):
    threads = []
    for dir in folders:
        if os.path.isdir(os.path.join(BASE_DIR, dir)):
            thread = threading.Thread(target=convert, args=(dir,))
            thread.start()
            threads.append(thread)
            
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        
    folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
    process_folders(folders)

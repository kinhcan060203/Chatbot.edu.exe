import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BASE_DIR)

from yolov10.ultralytics import YOLOv10
from pathlib import Path
from pdf2image import convert_from_bytes
import time
import shutil
from download import download_file_from_google_drive
import pandas as pd

ROOT_PATH = Path('data_pileline/systhesis_data')
MODEL_PATH = 'yolov10x_best.pt'
BOOK_LIST_FILE = 'data_pileline/book_list_info.txt'
SUBJECT_LIST = ['Toán']
NUMBER_OF_BOOKS = 1
IMAGE_SIZE = 544
CONF_THRESHOLD = 0.2

model = YOLOv10(MODEL_PATH)


if ROOT_PATH.exists():
    shutil.rmtree(ROOT_PATH)
os.makedirs(ROOT_PATH, exist_ok=True)
df = pd.read_csv(BOOK_LIST_FILE, delimiter='|')


for sub in SUBJECT_LIST:
    processed_books = 0
    for index, row in df.iterrows():
        link, subject, type, level, publicer, downloaded = row[df.columns]

        if downloaded == 'Yes' or subject != sub:
            continue

        file_id = link.split('/')[-2]
        subject_dir = ROOT_PATH / subject
        book_name = f'{type}_{subject}-{level}_{"-".join(publicer.split(" "))}'



        os.makedirs(subject_dir, exist_ok=True)

        file_object = download_file_from_google_drive(file_id)
        images = convert_from_bytes(file_object.getvalue())
        print(f"Downloaded book name: {book_name}, length: {len(images)} pages")

        start_t = time.time()
        results = model.predict(source=images, imgsz=IMAGE_SIZE, conf=CONF_THRESHOLD, index=index, subject=subject)
        print("Inference: ", time.time() - start_t)
        
        df.loc[index, 'Downloaded'] = 'Yes'
        df.to_csv(BOOK_LIST_FILE, sep='|', index=False)
        
        processed_books += 1
        if processed_books >= NUMBER_OF_BOOKS:
            break



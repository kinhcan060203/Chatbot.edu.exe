import os
import time
import shutil
import pandas as pd
from pathlib import Path
from unidecode import unidecode
from pdf2image import convert_from_bytes
from yolov10.ultralytics import YOLOv10
from download import download_file_from_google_drive

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = Path('data_pileline/systhesis_data')
MODEL_PATH = 'yolov10x_best.pt'
BOOK_LIST_FILE = 'data_pileline/book_list_info.txt'
SUBJECT_LIST = ['Toán']
NUMBER_OF_BOOKS = 2
IMAGE_SIZE = 544
CONF_THRESHOLD = 0.2


def process_book(index, row, model):
    link, subject, type, level, publicer, pagenumber, downloaded = row
    subject = unidecode(subject)
    publicer = unidecode(publicer)

    if downloaded == 'Yes' or subject not in SUBJECT_LIST:
        return False

    file_id = link.split('/')[-2]
    book_name = f'{type}_{subject}-{level}_{"-".join(publicer.split())}'

    file_object = download_file_from_google_drive(file_id)
    images = convert_from_bytes(file_object.getvalue())
    print(f"Downloaded book name: {book_name}, length: {len(images)} pages")

    start_t = time.time()
    model.predict(source=images, imgsz=IMAGE_SIZE, conf=CONF_THRESHOLD, index=index, subject=subject)
    print("Inference: ", time.time() - start_t)

    df.loc[index, 'Downloaded'] = 'Yes'
    df.loc[index, 'PageNumber'] = len(images)
    return True

if __name__ == "__main__":
    
    if (ROOT_PATH / 'images').exists():
        shutil.rmtree(ROOT_PATH / 'images')
        shutil.rmtree(ROOT_PATH / 'labels')
    os.makedirs(ROOT_PATH, exist_ok=True)
    
    df = pd.read_csv(BOOK_LIST_FILE, delimiter='|')
    df = df.astype({
        'PageNumber': 'int64',
        'Downloaded': 'string'
    }).fillna({'PageNumber': 0, 'Downloaded': 'No'})
    
    model = YOLOv10(MODEL_PATH)
    processed_books = 0
    for sub in map(unidecode, SUBJECT_LIST):
        for index, row in df.iterrows():
            if process_book(index, row, model):
                processed_books += 1
                if processed_books >= NUMBER_OF_BOOKS:
                    break
        if processed_books >= NUMBER_OF_BOOKS:
            break

    df.to_csv(BOOK_LIST_FILE, sep='|', index=False)

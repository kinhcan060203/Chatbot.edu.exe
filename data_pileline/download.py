import os
import requests
import io
def download_file_from_google_drive(file_id, destination=None):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    if destination:
        return save_response_content(response, destination)
    else:
        return create_file_object(response)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: 
                f.write(chunk)
    return destination

def create_file_object(response):
    file_object = io.BytesIO()
    CHUNK_SIZE = 32768

    for chunk in response.iter_content(CHUNK_SIZE):
        if chunk:
            file_object.write(chunk)

    file_object.seek(0)  
    return file_object



if __name__=='__main__':
    
    import pandas as pd
    df = pd.read_csv('data_pileline/book_list_info.txt', delimiter='|')
    root_url = 'data_pileline/pdf_downloaded'
    
    if not os.path.exists(root_url):
        os.makedirs(root_url,exist_ok=True)
        
    for _,row in df.iterrows():
        
        Link, Subject, Type, Level, Publicer = row[df.columns]
        file_id = Link.split('/')[-2]
        
        subject_dir = os.path.join(root_url,Subject)
        destination = os.path.join(subject_dir , f'{Type}_{Subject}-{Level}_{"-".join(Publicer.split(" "))}.pdf')
        if os.path.exists(destination):
            continue
        os.makedirs(subject_dir, exist_ok=True)  
        download_file_from_google_drive(file_id, destination)
        print(f"Downloaded file to {destination}")

from utils import *
from roboflow import Roboflow

def upload_dataset():
    rf = Roboflow(api_key=AppConst.API_KEY)
    workspace = rf.workspace(AppConst.WORKSPACE)

    workspace.upload_dataset(
        dataset_path=str(AppPath.DATASET_DIR),
        project_name=AppConst.PROJECT,
        num_workers=20,
        batch_name=AppConst.BATCH_NAME,
        num_retries=5,
    )
    
    
    # project = rf.workspace().project(AppConst.PROJECT)
    # labelmap_path = AppPath.DATASET_DIR / "data.yaml"
    # image_dir= AppPath.IMAGE_DIR
    # annotation_dir = AppPath.ANNOTATION_DIR
    
    # image_glob = sorted(image_dir.glob('*.jpg'))
    # annotation_glob = sorted(annotation_dir.glob('*.txt'))

    # print("Number of images: ",len(annotation_glob))
    # print('POC_1', f'Batch name: {AppConst.BATCH_NAME}')
    
    

    # for image_path, annotation_path in zip(image_glob,annotation_glob):
    #     print(project.single_upload(
    #         image_path=str(image_path),
    #         annotation_path=str(annotation_path),
    #         annotation_labelmap=str(labelmap_path),
    #         split='train',
    #         batch_name=AppConst.BATCH_NAME,
    #         tag_names=['POC_1',f'{AppConst.BATCH_NAME}'],
    #         annotation_overwrite=True,
    #         num_retry_uploads=3,
    #     ))

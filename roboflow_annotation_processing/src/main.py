import os
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from utils import *
from processing import process_annotations
from upload import upload_dataset

def main(args):
    
    if args.stage == "process":
        process_annotations()
    elif args.stage == "download":
        print("Download!!!")
        pass
    elif args.stage == "upload":
        upload_dataset()
    else:
        raise ValueError("Invalid stage! Please select download, process, upload")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roboflow annotation processing.")
    parser.add_argument(
        "-s",
        "--stage",
        default="download",
        help="download, process, upload",
    )

    args = parser.parse_args()
    main(args)



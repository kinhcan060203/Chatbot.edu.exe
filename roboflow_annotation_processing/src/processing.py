import glob
import json
import pandas as pd
import numpy as np
import os
import sys
from utils import *
import glob

def process_annotations():
    annot_files = sorted(AppPath.ANNOTATION_DIR.glob('*.txt'))
    with open(AppPath.CONNECT_JSONL_FILE, 'w', encoding='utf-8') as connection_jsonl:
        for annot_file in annot_files:
            df, connect_polygons = annotation_extract(annot_file)
            new_df = filter_df_merge_condition(df.copy())
            if connect_polygons:
                process_connections(connect_polygons, new_df, annot_file, connection_jsonl)

            new_df.to_csv(annot_file, sep=' ', index=False, header=None)

def merge_bbox(df):
    x_min = (df['x_center'] - df['width'] / 2).min()
    y_min = (df['y_center'] - df['height'] / 2).min()
    x_max = (df['x_center'] + df['width'] / 2).max()
    y_max = (df['y_center'] + df['height'] / 2).max()
    return (x_min + x_max) / 2, (y_min + y_max) / 2, x_max - x_min, y_max - y_min

def filter_df_merge_condition(df):
    merge_annotations = df[df['class'] == AppConst.MERGE_INDEX]
    new_df = pd.DataFrame(columns=AppConst.DEFAULT_COLUMNS)
    removed_indices = []

    for _, merge_item in merge_annotations.iterrows():
        relevant_classes = df[
            (merge_item['y_center'] - merge_item['height'] / 2 < df['y_center']) &
            (df['y_center'] < merge_item['y_center'] + merge_item['height'] / 2) &
            ~df['class'].isin([AppConst.MERGE_INDEX, AppConst.CONNECT_INDEX])
        ]
        coordinates = merge_bbox(relevant_classes)
        new_df.loc[len(new_df)] = [AppConst.CLASS_MAP['Text'], *coordinates]
        removed_indices.extend(relevant_classes.index)
    
    filtered_df = df[~df.index.isin(removed_indices) & ~df['class'].isin([AppConst.MERGE_INDEX, AppConst.CONNECT_INDEX])]

    return pd.concat([filtered_df, new_df]).astype({'class': 'int64'}).reset_index(drop=True)

def annotation_extract(annot_file):
    normal_boxes, connect_polygons = [], []
    
    with open(annot_file, 'r') as file:
        for line in file:
            components = list(map(float, line.strip().split()))
            class_index = int(components[0])
            boxes = components[1:]
            if class_index != AppConst.CONNECT_INDEX and len(boxes)==4:
                normal_boxes.append([class_index, *boxes])
            else:
                connect_polygons.append(boxes)
    
    return pd.DataFrame(normal_boxes, columns=AppConst.DEFAULT_COLUMNS), connect_polygons



def process_connections(connect_polygons, new_df, annot_file, connection_jsonl):
    connect_idx_list = []
    for connect in connect_polygons:
        connect_coordinates = np.array(connect).reshape(-1, 2)
        relevant_classes = [
            new_df[
                (new_df['y_center'] - new_df['height'] / 2 < coordinates[1]) &
                (coordinates[1] < new_df['y_center'] + new_df['height'] / 2) &
                (new_df['x_center'] - new_df['width'] / 2 < coordinates[0]) &
                (coordinates[0] < new_df['x_center'] + new_df['width'] / 2) &
                ~new_df['class'].isin([AppConst.MERGE_INDEX, AppConst.CONNECT_INDEX])
            ] for coordinates in connect_coordinates
        ]

        connected_idx = [item['width'].idxmin() for item in relevant_classes if len(item) > 0]
        connect_idx_list.append(set(connected_idx))
        json.dump({
            'ID': str(os.path.basename(annot_file)[:8]),
            'CONNECTION': json.dumps(list(set(connected_idx)), cls=NpEncoder),
        }, connection_jsonl, ensure_ascii=False)
        connection_jsonl.write('\n')

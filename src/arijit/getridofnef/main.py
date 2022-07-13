#!/usr/bin/env python3

import sys
import os 
import concurrent.futures
import rawpy
import argparse
import imageio as iio
from pathlib import Path
from pathlib import PurePath


def get_list_of_files_to_convert(path:str):
    base_path = Path(path)
    jpg_files = sorted(base_path.glob("*.JPG"))
    jpeg_files = sorted(base_path.glob("*.JPEG"))
    jpeg_file_list = []
    if jpg_files != None and len(jpg_files) > 0 : 
        jpeg_file_list += jpg_files
    if jpeg_files != None and len(jpeg_files) > 0 : 
        jpeg_file_list += jpeg_files
    jpeg_file_names = [Path(j).stem for j in jpeg_file_list]
    nef_files = sorted(base_path.glob("*.NEF"))
    nef_file_names = [Path(n).stem for n in nef_files]
    return  [os.path.join(str(base_path),n+".NEF")  for n in nef_file_names if n not in jpeg_file_names]


def convert_image(img,output_dir:str):
    print(f"Converting {img}")
    rgb  = None
    with rawpy.imread(img) as raw: 
        rgb = raw.postprocess(output_bps=16,use_camera_wb=True,bright=1.7)
    base_image_name = Path(img).stem
    iio.imwrite(os.path.join(output_dir,base_image_name+".jpg"),rgb,format="JPEG")
    print(f"Done with {img}")

def image_converter(images,output_dir:str):
    with concurrent.futures.ProcessPoolExecutor(max_workers= os.cpu_count()) as pool: 
        for img in images: 
            pool.submit(convert_image,img, output_dir)
        

def main(): 
    print("This is nef->jpeg converter") 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="input_dir",
        action = "store",
        help="input directory",
        required= True
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        action="store",
        help="output directory",
        required=True
    )
    args = parser.parse_args()

    Path(args.output_dir).mkdir(exist_ok=True)
    image_converter(get_list_of_files_to_convert(args.input_dir),args.output_dir)
    return 0


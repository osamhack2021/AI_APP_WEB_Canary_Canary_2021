# TODO : image를 download 한 후, Canary_YOLOv5 에서 detect.py 돌리기
# 처리 완료 했으면 이미지 삭제하기
from tqdm import tqdm
from utils.image_path import *

import os

class detectArgs:
    input_image_path = ''
    output_image_path = ''
    weight_path = ''
    blur = False
    output_warning_path = ''

if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		# print(path.dirname(path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) )) ))
		sys.path.append(path.dirname(path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) )) ))
		from AI.yolov5.detect import *
	else:
		from ......AI.yolov5 import detect

def make_directory_save_images(user_output_path):
    path = f'{IMAGE_OUTPUT_ROOT}/{user_output_path}'
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError: 
        print("Error : Creating directory " + path)
    return path

def make_directory_save_warning(user_output_path):
    path = f'{WARNING_OUTPUT_ROOT}/{user_output_path}'
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error : Creating directory " + path)
    return path

def detect_images():
    test_needed_user_list = os.listdir(f'{IMAGE_DOWNLOAD_ROOT}')
    test_needed_user_number = len(test_needed_user_list)

    for i in tqdm(range(0, test_needed_user_number)):
        print("== User Number : %d ==" % i)
        make_directory_save_images(test_needed_user_list[i])
        make_directory_save_warning(test_needed_user_list[i])

        test_needed_photo_list = os.listdir(f'{IMAGE_DOWNLOAD_ROOT}/{test_needed_user_list[i]}')
        test_needed_photo_number = len(test_needed_photo_list)

        for j in tqdm(range(0, test_needed_photo_number)):
            print("== Photo Number : %d ==" % j)
            user_photo_path = f'{test_needed_user_list[i]}/{test_needed_photo_list[j]}'

            IMAGE_INPUT_PATH = f'{IMAGE_DOWNLOAD_ROOT}/{user_photo_path}'
            IMAGE_OUTPUT_PATH = f'{IMAGE_OUTPUT_ROOT}/{user_photo_path}'
            WARNING_OUTPUT_PATH = f'{WARNING_OUTPUT_ROOT}/{user_photo_path}'+('.txt')

            args = detectArgs()
            args.input_image_path = f'{IMAGE_INPUT_PATH}'
            args.output_image_path = f'{IMAGE_OUTPUT_PATH}'
            args.weight_path = './weight/yolov5m6.pt'
            args.output_warning_path = f'{WARNING_OUTPUT_PATH}'

            detect(args)

# detect_images()
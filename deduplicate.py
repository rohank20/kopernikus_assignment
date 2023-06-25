import os
import argparse
import re
import cv2
from datetime import datetime
from tqdm import tqdm

from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection

parser = argparse.ArgumentParser()

parser.add_argument("--dir_path", type=str, help='Path to image directory to be de-duplicated', required=True)


def parse_args():
    args = parser.parse_args()

    dir_path = args.dir_path
    if not os.path.isdir(dir_path):
        raise Exception('This directory does not exist. Please check the input parameters again.')

    return dir_path


def format_names(dir_path):
    filenames = []
    for f in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.png'):
            camera_id = re.split(r"-|_", f)[0]
            timestamp = re.split(r"-|_", f, maxsplit=1)[1].split('.')[0]
            try:
                dt = datetime.strptime(timestamp, "%Y_%m_%d__%H_%M_%S")
            except:
                dt = datetime.fromtimestamp(int(timestamp) / 1000)
            new_timestamp = dt.strftime("%Y_%m_%d__%H_%M_%S")
            new_name = f'{camera_id}-{new_timestamp}.png'
            os.rename(os.path.join(dir_path, f), os.path.join(dir_path, new_name))
            filenames.append(new_name)

    return sorted(filenames)


def main(dir_path):
    files = format_names(dir_path)
    total = 0
    for idx, file in enumerate(tqdm(files)):
        if idx + 1 < len(files):
            try:
                reshape_size = (640, 480)
                img_area = reshape_size[0] * reshape_size[1]
                img_1 = cv2.imread(os.path.join(dir_path, file))
                img_2 = cv2.imread(os.path.join(dir_path, files[idx + 1]))
                img_1 = cv2.resize(img_1, reshape_size, interpolation=cv2.INTER_AREA)
                img_2 = cv2.resize(img_2, reshape_size, interpolation=cv2.INTER_AREA)

                gaussian_blur_radius_list = [5, 7, 9]
                gray_img_1 = preprocess_image_change_detection(img_1, gaussian_blur_radius_list)
                gray_img_2 = preprocess_image_change_detection(img_2, gaussian_blur_radius_list)

                min_cnt_area = 0.0001 * img_area  # number low, high unique_score
                uniqueness_score, res_cnts, thresh = compare_frames_change_detection(gray_img_1, gray_img_2,
                                                                                     min_cnt_area)
                if uniqueness_score < 0.01 * img_area:  # threshold low, fewer deletions
                    os.remove(os.path.join(dir_path, file))
                    total += 1
            except:
                continue
        else:
            continue
    print(f'Execution complete. Removed {total} images')


if __name__ == '__main__':
    dir_path = parse_args()
    main(dir_path)

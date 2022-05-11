import numpy as np
import shutil
import os
import re
import h5py
import cv2
import sys
import skvideo.io
from sklearn.neighbors import KDTree
import csv
from sklearn.cluster import KMeans
import threading

dirsep = '\\'

def get_all_file_path(directory, file_extension):
    all_filepath = [] # Đây là mảng lưu lại tất cả các đường dẫn chứa file có đuôi file_extension tại thư mục directory
    for root, dirs, files in os.walk(directory): # Vòng lặp để quét tất cả các file trong thư mục
        for file in files:
            for ext in file_extension:
                if file.endswith(ext): # Xuất hiện bug có kí hiệu phân cách và không có, dòng if để chuẩn hóa đường dẫn
                    if root[len(root) -  1] != dirsep:
                        all_filepath.append((root + dirsep, file, root + dirsep + file))
                    else:
                        all_filepath.append((root, file, root + file))
    return all_filepath

a = cv2.imread('168.bmp')
b = cv2.imread('168.tif')

def check_surround(mat, position):
    t1 = False
    t2 = False
    for i in range(0, 2):
        for j in range(0, 2):
            try:
                if mat[position[0] + i][position[1] + j][0] == 255:
                    t1 = True
                if mat[position[0] + i][position[1] + j][0] == 0:
                    t2 = True
            except:
                pass
    return t1 and t2

def draw(mat, position, radius=0):
    for i in range(radius * -1, radius + 1):
        for j in range(radius * -1, radius + 1):
            try:
                mat[position[0] + i][position[1] + j][0] = 0
                mat[position[0] + i][position[1] + j][1] = 0
                mat[position[0] + i][position[1] + j][2] = 255
            except:
                pass
    return

def draw_boundary(mat_bit, mat_out):
    # cv2.imshow("test1", mat_bit)
    # cv2.imshow("test2", mat_out)
    # cv2.waitKey(15000)
    counting = 0
    print('done')
    for i in range(0, mat_out.shape[0]):
        for j in range(0, mat_out.shape[1]):
            if check_surround(mat_bit, (i, j)) == True:
                # print(i, j)
                draw(mat_out, (i, j))
                counting += 1
    return counting

def draw_square(bit_map, mat_out, radius=4):
    draw(mat_out, (radius, radius), radius=radius)
    return

# x = draw_boundary(a, b)
# print(x)
# cv2.imshow('test', b)
# cv2.waitKey(15000)

ds = ['Dataset', 'Dataset2']
test_location = []
for i in ds:
    tl = [x[0] for x in os.walk(i)]
    for x in tl:
        test_location.append(x)
print(test_location)
for i in ds:
    test_location.remove(i)
for path in test_location:
    lst = get_all_file_path(path, ['.tif'])
    lst_gt = get_all_file_path(path, ['.bmp'])
    frames = []
    anomal_frames = []
    bitmap_frames = []
    bitmap = []
    for path2 in lst:
        frames.append(cv2.imread(path2[2]))
    for path2 in lst_gt:
        print(path2)
        bitmap.append(cv2.imread(path2[2]))
    print("yes0")
    for i in range(0, len(frames)):
        if bitmap[i].sum() != 0:
            anomal_frames.append(frames[i].copy())
            draw_boundary(bitmap[i], frames[i])
            # cv2.imshow("test1", frames[i])
            # cv2.imshow("test2", bitmap[i])
            # cv2.waitKey(15000)
            bitmap_frames.append(bitmap[i])
        #     draw_square(bitmap[i], frames[i])
    print("yes1")
    for i in range(0, len(frames)):
        frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB)
    for i in range(0, len(anomal_frames)):
        anomal_frames[i] = cv2.cvtColor(anomal_frames[i], cv2.COLOR_BGR2RGB)
    print("yes2")
    frames = np.asarray(frames, dtype=np.uint8)
    anomal_frames = np.asarray(anomal_frames, dtype=np.uint8)
    print(path)
    try:
        os.makedirs("Output\\" + path + dirsep)
    except:
        pass
    print("yes4")
    print(anomal_frames.shape)
    skvideo.io.vwrite("Output\\" + path + dirsep + "output1.mp4", frames)
    skvideo.io.vwrite("Output\\" + path + dirsep + "output2.mp4", anomal_frames)
    skvideo.io.vwrite("Output\\" + path + dirsep + "output3.mp4", bitmap_frames)
# list = get_all_file_path('Dataset\\', ['.tif'])
# print(list)
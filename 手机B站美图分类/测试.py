# # 示例列表
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,15,12]
#
# # 设置步幅为 2
# size = 2
#
# blocks = int(len(my_list)/2)
# print(blocks)
# start = [0]
# for i in range(1,blocks):
#     start.append(i*size-1)
# if start[-1] != len(my_list):
#     start.append(len(my_list)-1)
# print(start)
# for i in start:
#     print(my_list[i])
import os.path
from PIL import Image

# 打开图像

import cv2 as cv

# img = Image.open(r"W:\Code\PythonCode\myselfTools\手机B站美图分类\tmp\0004_2024-02-06 19-13-30 - 副本.jpg")
# print(img.size[0], img.size[1])

print(os.path.split("./测试.py"))
print("./测试.py".rsplit('.',maxsplit=1))

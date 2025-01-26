import shutil
import threading
import cv2 as cv
import os

key = 'n'


def createdir(newDir):
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    else:
        if len(os.listdir(newDir)) == 0:
            return
        global key
        if key == 'y':
            return
        if key != 'y':
            print(f"文件夹:{newDir}已存在,且其内部存在内容!!\n存在文件冲突风险\n是否全部继续?[y/n]")
            key = input()
            if key == 'y':
                return

        exit(0)

def movefile(name, dest, fontFolder=""):
    shutil.move(name, f"{fontFolder}/{dest}/{name}")

def nextfilter(name, shape0, fontFolder):
    if shape0 < 1000:
        movefile(name, dirstr2[0], fontFolder)
    elif shape0 < 2000:
        movefile(name, dirstr2[1], fontFolder)
    elif shape0 < 3000:
        movefile(name, dirstr2[2], fontFolder)
    elif shape0 < 4000:
        movefile(name, dirstr2[3], fontFolder)
    else:
        movefile(name, dirstr2[4], fontFolder)


def task(start, end):
    for lists in listdir[start:end]:
        if os.path.isfile(lists):
            if 'gif' in lists:
                movefile(lists, dirstr[3])
                continue
            img = cv.imread(lists)
            if img.shape[0] > img.shape[1]:
                nextfilter(lists, img.shape[0], dirstr[0])
            elif img.shape[0] == img.shape[1]:
                nextfilter(lists, img.shape[0], dirstr[2])
            else:
                nextfilter(lists, img.shape[0], dirstr[1])


if __name__ == '__main__':
    dirstr = ["长高宽矮", "宽高长矮", "长宽相等", "gif"]
    dirstr2 = ["小于1000", "小于2000", "小于3000", "小于4000", "大于4000"]
    for s in dirstr:
        createdir(s)
        for s2 in dirstr2:
            createdir(f"{s}/{s2}")

    listdir = os.listdir()
    if '.idea' in listdir:
        listdir.remove('.idea')
    if '通用图片长宽高整理.py' in listdir:
        listdir.remove('通用图片长宽高整理.py')

    teams = 20
    mltnums = int(len(listdir) / teams)
    print(mltnums)
    arrr = range(0, 100)
    for i in range(0, mltnums):
        thrd = threading.Thread(target=task, args=(i * teams, i * teams + teams))
        thrd.start()
    task((mltnums - 1) * teams + teams, len(listdir))

    # for num in range(1, 100):
    #     open(f"测试a{num}.txt", "w+").write(f"{num}")
    #
    # listdir = os.listdir("./")
    # listdir.remove('.idea')
    # listdir.remove('通用图片长宽高整理.py')
    # for lists in listdir:
    #     if not os.path.isdir(lists):
    #         file = open(f"{lists}", 'r')
    #         str1 = file.readline()
    #         file.close()
    #         if int(str1) % 10 == 0:
    #             shutil.move(lists, f"测试2/{lists}")
    #         else:
    #             os.unlink(lists)

    # print(listdir)
    # if os.path.exists("测试ss"):
    #     # os.rmdir("测试ss") 这个只能删除空文件夹
    #     shutil.rmtree("测试ss")  # 这个删除整个文件夹
    # os.makedirs("测试ss")
    # file = open("测试ss/测试123.txt", 'w+')
    # file.write("nihaosss")
    # file.close()
    #
    # shutil.move("测试文件1.txt","测试文件夹1")

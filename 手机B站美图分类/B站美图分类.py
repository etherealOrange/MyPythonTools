from datetime import datetime
import os
import json
import shutil
import threading
import cv2 as cv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

root = './'
needSortFolder = './tmp'
configFile = './config.json'
config = {
    "长高宽矮": {
        "小于1000": 0,
        "小于2000": 0,
        "小于3000": 0,
        "小于4000": 0,
        "大于4000": 0
    },
    "宽高长矮": {
        "小于1000": 0,
        "小于2000": 0,
        "小于3000": 0,
        "小于4000": 0,
        "大于4000": 0
    },
    "长宽相等": {
        "小于1000": 0,
        "小于2000": 0,
        "小于3000": 0,
        "小于4000": 0,
        "大于4000": 0
    },
    "gif": 0
}
folderLevelOne = list(config.keys())
# 不可靠 注意修改
folderLevelTwo = ["小于1000", "小于2000", "小于3000", "小于4000", "大于4000"]
lock = threading.Lock()
# 多线程单次 处理步幅
StepG = 5

def CheckJSONError(tmpCfg, cfg=config):
    if cfg.keys() != tmpCfg.keys():
        return True
    else:
        for key, value in cfg.items():
            tpvalue = type(value)
            tptmpcfg = type(tmpCfg[key])
            if tpvalue == tptmpcfg and (tpvalue == dict or tpvalue == int) and (tptmpcfg == dict or tptmpcfg == int):
                if isinstance(value, dict) and CheckJSONError(tmpCfg[key], cfg[key]):
                    return True
            else:
                return True
    return False


def MakeConfigCorrect():
    global config
    with open(configFile, 'r+', encoding="utf-8") as f:
        try:
            tmpCfg = json.load(f)
        except json.JSONDecodeError as e:
            print("你的config.json文件格式不正确:", e)
            exit(-200)
        if CheckJSONError(tmpCfg):
            f.seek(0)
            f.truncate(0)
            json.dump(config, f, indent=4, ensure_ascii=False)
        else:
            config = tmpCfg


def CountPicFolder(lvl1, lvl2):
    path = os.path.join(root, lvl1, lvl2)
    with os.scandir(path) as entries:
        # 过滤掉文件夹，只保留文件
        files = [entry.name for entry in entries if entry.is_file()]
    return len(files)


def CountPicALL():
    for lvl1 in folderLevelOne:
        if isinstance(config[lvl1], dict):
            folderLvlTwo = config[lvl1].keys()
            for lvl2 in folderLvlTwo:
                if config[lvl1][lvl2] == 0:
                    config[lvl1][lvl2] = CountPicFolder(lvl1, lvl2)
        else:
            config[lvl1] = CountPicFolder(lvl1, "")

    pass


def ClassifySize(imgShape):
    if imgShape < 1000:
        return folderLevelTwo[0]
    elif imgShape < 2000:
        return folderLevelTwo[1]
    elif imgShape < 3000:
        return folderLevelTwo[2]
    elif imgShape < 4000:
        return folderLevelTwo[3]
    else:
        return folderLevelTwo[4]


def ClassifyImages(imgName):
    imgPath = os.path.join(needSortFolder, imgName)
    suffix = imgName.split('.')[-1]
    if 'gif' in suffix.lower():
        return [imgPath, folderLevelOne[3], ""]
    img = Image.open(imgPath)
    if img.size[1] > img.size[0]:
        return [imgPath, folderLevelOne[0], ClassifySize(img.size[1])]
    elif img.size[0] == img.size[1]:
        return [imgPath, folderLevelOne[2], ClassifySize(img.size[0])]
    else:
        return [imgPath, folderLevelOne[1], ClassifySize(img.size[0])]

# 必须同步 !!
def DistributeIndex(AftClassify):
    if AftClassify[2] == "":
        with lock:
            config[AftClassify[1]] += 1
        nextIndex = config[AftClassify[1]]
    else:
        with lock:
            config[AftClassify[1]][AftClassify[2]] += 1
        nextIndex = config[AftClassify[1]][AftClassify[2]]
    if nextIndex < 10:
        fill00000 = "0000"
    elif nextIndex < 100:
        fill00000 = "000"
    elif nextIndex < 1000:
        fill00000 = "00"
    elif nextIndex < 10000:
        fill00000 = "0"
    else:
        fill00000 = ""
    nextIndexString = fill00000 + str(nextIndex)
    AftClassify.append(nextIndexString)
    return AftClassify


def AddImageNewName(AftIndex):
    # 获取文件的修改时间（时间戳）
    modification_time = os.path.getmtime(AftIndex[0])
    # 将时间戳转换为 datetime 对象
    modification_time = datetime.fromtimestamp(modification_time)
    # 格式化输出
    formatted_time = modification_time.strftime('%Y-%m-%d %H-%M-%S')
    suffix = AftIndex[0].split('.')[-1]
    AftIndex.append(f"{AftIndex[-1]}_{formatted_time}.{suffix}")
    return AftIndex

def MoveImage(AftNewName):
    newPath = os.path.join(root,AftNewName[1],AftNewName[2],AftNewName[4])
    shutil.move(AftNewName[0], newPath)

def Task(NeedSortLs):
    for ls in NeedSortLs:
        AftClassify = ClassifyImages(ls)
        AftIndex = DistributeIndex(AftClassify)
        AftNewName = AddImageNewName(AftIndex)
        print(AftIndex)
        MoveImage(AftNewName)

def GenerateStartList(LenLs,Step=StepG):
    BlockNum = int(LenLs / Step)
    start = [0]
    for i in range(1,BlockNum):
        start.append(i * Step)
    if start[-1] != LenLs:
        start.append(LenLs)
    return start

def CreateConfigFolder():
    for folder in folderLevelOne:
        if not os.path.exists(os.path.join(root, folder)):
            os.mkdir(os.path.join(root, folder))
        if isinstance(config[folder], dict):
            for folderlvl2 in folderLevelTwo:
                if not os.path.exists(os.path.join(root, folder,folderlvl2)):
                    os.mkdir(os.path.join(root, folder,folderlvl2))

if __name__ == '__main__':
    # 检查运行环境
    if not os.path.exists(needSortFolder):
        print("没有需要分类的文件夹, 请新建文件夹 tmp,并把图片放入其中")
        input()
        exit(-100)
    CreateConfigFolder()
    if not os.path.exists(configFile):
        # 如果不存在配置文件,就新建文件
        with open(configFile, 'w', encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    else:
        # 检查现有配置的正确性
        MakeConfigCorrect()

    CountPicALL()
    NeedSortLs = os.listdir(needSortFolder)
    threads = []
    LenLs = len(NeedSortLs)
    starts = GenerateStartList(LenLs)

    for i in range(len(starts)-1):
        thread = threading.Thread(target=Task, args=([NeedSortLs[starts[i]:starts[i+1]]]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


    # 存储
    with open(configFile, 'w', encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print("数据分类完成!!!!(输入任意键结束)")
    input()
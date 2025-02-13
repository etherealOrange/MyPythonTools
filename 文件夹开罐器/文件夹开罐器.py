import os
import shutil

root = './开罐结果'
startRoot = './'


def RenameFileName(name, suffix):
    detectName = os.path.join(root, f"{name}.{suffix}")
    repeatsNum = 0
    while os.path.exists(detectName):
        addStr = f"-重复 {repeatsNum}"
        detectName = os.path.join(root, f"{name}{addStr}.{suffix}")
        repeatsNum += 1
    return detectName
def RenameDirName(name):
    detectName = os.path.join(root, f"{name}")
    repeatsNum = 0
    while os.path.exists(detectName):
        addStr = f"-重复 {repeatsNum}"
        detectName = os.path.join(root, f"{name}{addStr}")
        repeatsNum += 1
    return detectName


def DFS_Search_MoveFile(folder,lvl):
    if lvl == 0:
        return 0
    if lvl < -500:
        lvl = -1
    ls = os.listdir(folder)
    for i in ls:
        realPath = (os.path.join(folder, i))
        if os.path.isfile(realPath):
            [name, suffix] = i.rsplit('.', maxsplit=1)
            OKname = RenameFileName(name, suffix)
            shutil.move(realPath, f"{OKname}")
        if os.path.isdir(realPath):
            if DFS_Search_MoveFile(realPath,lvl-1) == 0:
                OKname = RenameDirName(i)
                shutil.move(realPath, f"{OKname}")
    return -1


if __name__ == '__main__':
    ls = os.listdir(startRoot)
    scriptName = os.path.basename(__file__)
    ls.remove(f"{scriptName}")
    if "开罐结果" in ls:
        ls.remove("开罐结果")
    else:
        os.mkdir("开罐结果")
    print("选择你要打开的层级（回车表示无限）：")
    lvl = input()
    if len(lvl) == 0 or int(lvl) < 0:
        for i in ls:
            DFS_Search_MoveFile(os.path.join(startRoot, i),-1)
    elif int(lvl) > 0:
        for i in ls:
            DFS_Search_MoveFile(os.path.join(startRoot, i),int(lvl))



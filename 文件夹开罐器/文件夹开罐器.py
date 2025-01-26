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


def DFS_Search_MoveFile(folder):
    ls = os.listdir(folder)
    for i in ls:
        realPath = (os.path.join(folder, i))
        if os.path.isfile(realPath):
            [nosuffix, suffix] = i.rsplit('.', maxsplit=1)
            name = nosuffix.rsplit('\\', maxsplit=1)[0]
            OKname = RenameFileName(name, suffix)
            shutil.move(realPath, f"{OKname}")
        if os.path.isdir(realPath):
            DFS_Search_MoveFile(realPath)

if __name__ == '__main__':
    ls = os.listdir(startRoot)
    scriptName = os.path.basename(__file__)
    ls.remove(f"{scriptName}")
    if "开罐结果" in ls:
        ls.remove("开罐结果")
    else:
        os.mkdir("开罐结果")
    for i in ls:
        DFS_Search_MoveFile(os.path.join(startRoot, i))

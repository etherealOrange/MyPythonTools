import os

Dir = ["ACG T0", "ACG T1", "ACG T2", "ACG T3", "ACG T4", "ACG T5"]
WDir = "统计.txt"


def search_tree(root, deep):
    ls = os.listdir(root)
    if len(ls) == 0:
        return
    for i in ls:
        realPath = os.path.join(root, i)
        if os.path.exists(realPath):
            with open(WDir, 'a', encoding='utf-8') as f:
                f.write('   ' * deep + i + "\n")
        if os.path.isdir(realPath):
            search_tree(realPath, deep + 1)


if __name__ == '__main__':
    if os.path.exists(WDir):
        with open(WDir, "w", encoding='utf-8') as f:
            pass
    print("输入模式: 1.ACG T0~T5    2.只有当前文件夹   3.当前文件夹和子文件夹")
    s = input()
    if s == '1':
        for foldName in Dir:
            if os.path.exists(foldName):
                ls = os.listdir(foldName)
                with open(WDir, 'a', encoding='utf-8') as f:
                    f.write(foldName + "\n")
                    for name in ls:
                        f.write("   " + name + "\n")
    elif s == '2':
        ls = os.listdir()
        with open(WDir, 'a', encoding='utf-8') as f:
            for name in ls:
                f.write(name + "\n")
    else:
        search_tree('.\\', 0)

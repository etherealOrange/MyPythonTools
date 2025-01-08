import os
import json


def IfSearchFolder(ls, Flts):
    for dirname in ls:
        AftSplit = dirname.split('.')
        if len(AftSplit) > 1:
            for FLT in Flts:
                if FLT in AftSplit[-1].lower():
                    return True
    return False


def BuildTree(root, data, flt):
    ls = os.listdir(root)
    if ls == 0 or IfSearchFolder(ls, flt):
        return
    for i in ls:
        realpath = root + '\\' + i
        if os.path.isdir(realpath):
            data.append([i, realpath])
            BuildTree(realpath, data, flt)

def SearchTree(ACG_Data,Search_Data):
    for name in Search_Data:
        next_round = False
        for i in ACG_Data:
            for j in i[2]:
                if j[0] == name[0]:
                    name.append([i[0],j[1]])
                    next_round = True
                    break
            if next_round:
                break
        if next_round:
            continue
        name.append(['不存在','---'])



if __name__ == '__main__':
    if not os.path.exists('ACG_Sum_config.json'):
        print("配置不存在！！")
        input()
        exit(-100)
    # 配置装载
    with open('ACG_Sum_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        ACG_srt = config['config']['ACG_srt']
        Search_srt = config['config']['Search_srt']
        tmp_sort_name = config['config']['ACG_sort_names']
        ACG_sort_names = []
        ACG_Data = []
        Search_Data = []
        for lvl in tmp_sort_name:
            ACG_sort_names.append([tmp_sort_name[lvl], lvl])  # 【具体地址，等级】
            ACG_Data.append([lvl, ACG_srt + '\\' + tmp_sort_name[lvl], []])
        Result_name = config['config']['Result_name']
        Filter = config['config']['Filter'].split(',')

    for root in ACG_Data:
        BuildTree(root[1],root[2],Filter)

    BuildTree(Search_srt,Search_Data,Filter)
    SearchTree(ACG_Data, Search_Data)
    with open(Result_name, 'w', encoding='utf-8') as f:
        for data in Search_Data:
            str = '名字：'+data[0]+'\n'+'当前位置：'+data[1]+'\n'+'查找结果：'+data[2][0]+'\n'+'查找位置：'+data[2][1]+'\n'
            f.write(str)



import os
import re
import numpy as np

class GrammarAnalyzer:

    # first 集 follow 集函数，文法的存储数组是 self.grammar ,得到的结果打印出来并存到数组 self.first, self.follow
    # 详见 readme

    def FirstFollow(self):
        ###############
        # first 集
        ###############
        finished = True

        # 初始化 first 集
        for grammar in self.grammar:
            print(grammar) # 打印每一条文法

            left = grammar['Left']
            if left not in self.first: # 把尚未在 first 集里出现的非终结符都添加进去
                self.first[left] = []

            # 看产生式右边的第一个符号
            # 如果是终结符，直接加入 first 集即可
            # 如果是非终结符，则需要加入该非终结符的 first 集
            right = grammar['Right'][0]
            tmp_dict = {}
            tmp_dict['name'] = right['name']
            tmp_dict['position'] = self.grammar.index(grammar)
            if right['TYPE'] == 'UNEND': 
                finished = False
                tmp_dict['type'] = 'FIRST'
                tmp_dict['index'] = 0
            self.first[left].append(tmp_dict)
        
        # 不断展开现有 first 集里面需要替换的集合
        while finished == False:
            finished = True # 每一次循环都先把 finished 标志置为 True，若出现替换后还有需要进行替换的集合时则置 False
            for unend_symbol in self.first: # 遍历 first 集里的每一个集合
                for element in self.first[unend_symbol]: # 遍历每一个集合里的每一个元素
                    if element.get('type') == 'FIRST': # 若该元素需要展开，如：FIRST(X)
                        replace_symbol = element['name'] # 拿到 X
                        position = element['position']
                        index = element['index']
                        replace_list = self.first[replace_symbol] # 拿到当前 FIRST(X) 的集合
                        
                        # 把当前集合中的 FIRST(X) 删掉
                        del_index = self.first[unend_symbol].index(element)
                        del self.first[unend_symbol][del_index]
                        
                        # 把当前 FIRST(X) 集合中的所有元素都加到当前集合中来
                        for replace_dict in replace_list: # replace_dict 为当前 FIRST(X) 中的元素
                            if replace_dict.get('type') == 'FIRST': # 若 replace_dict 仍需要展开，则原样复制过去即可
                                finished = False
                                tmp_dict = replace_dict.copy()
                                tmp_dict['position'] = position # position 保留
                                tmp_dict['index'] = index # index 保留
                                if tmp_dict not in self.first[unend_symbol]:
                                    self.first[unend_symbol].append(tmp_dict)
                            else: # 终结符
                                if replace_dict['name'] == 'epsilon': # 如果是空字符，还需要对 X 的下一个字符进行判断
                                    right_list = self.grammar[position]['Right'] # 拿到 X 所在产生式右边的列表
                                    tmp_dict = {}
                                    if index + 1 > len(right_list) - 1: # 若 X 已是最后一个符号，则保留空字符
                                        tmp_dict['name'] = 'epsilon'
                                    else: # 若 X 后面还有符号，则应加入下一个符号的 first 集
                                        right = grammar['Right'][index + 1]
                                        if right['TYPE'] == 'UNEND': # 如果下一个符号是非终结符
                                            finished = False
                                            tmp_dict['type'] = 'FIRST'
                                            tmp_dict['index'] = index + 1
                                        tmp_dict['name'] = right['name']
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.first[unend_symbol]:
                                        self.first[unend_symbol].append(tmp_dict)
                                else: # 普通终结符，原样复制过去即可
                                    tmp_dict = replace_dict.copy()
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.first[unend_symbol]:
                                        self.first[unend_symbol].append(tmp_dict)
                    else:
                        continue

        print()
        print("目前得到的 first 集：")
        for unend_symbol in self.first:
            print(unend_symbol, '——', self.first[unend_symbol])
        print()

        ###############
        # follow 集
        ###############
        # first 集里有多少个集合 follow 集里面就有多少个集合
        for unend_symbol in self.first:
            self.follow[unend_symbol] = []

        # 给起始符号加上'#'
        tmp_dict = {}
        tmp_dict['name'] = '#'
        tmp_dict['position'] = 0
        self.follow[self.grammar[0]['Left']].append(tmp_dict)

        # 初始化 follow 集
        finished = True
        for unend_symbol in self.follow: # 对于每一个非终结符 N
            for grammar in self.grammar: # 需要一条一条 grammar 去找它的出现位置
                right = grammar['Right'] # 拿到 grammar 的右边集合
                for symbol in right: # 遍历右边集合，其中 symbol 是集合里的元素
                    if symbol['name'] == unend_symbol: # 若 symbol 的名字与 N 相同，就说明找到了
                        if right.index(symbol) + 1 > len(right) - 1: # 若 symbol 已经是集合的最后一个元素了，则需要添加 follow 集
                            if unend_symbol != grammar['Left']: # 若发现是自身的话就无需添加了
                                finished = False
                                tmp_dict = {}
                                tmp_dict['type'] = 'FOLLOW'
                                tmp_dict['name'] = grammar['Left']
                                tmp_dict['position'] = self.grammar.index(grammar)
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)
                        else: # 若 symbol 后面还有其他元素，则添加其 first 集
                            tmp_dict = {}
                            if right[right.index(symbol) + 1]['TYPE'] == 'UNEND': # 若为非终结符
                                finished = False
                                tmp_dict['type'] = 'FIRST'
                                tmp_dict['index'] = right.index(symbol) + 1
                            tmp_dict['name'] = right[right.index(symbol) + 1]['name']
                            tmp_dict['position'] = self.grammar.index(grammar)
                            if tmp_dict not in self.follow[unend_symbol]:
                                self.follow[unend_symbol].append(tmp_dict)

        # 不断展开现有 follow 集里面需要替换的集合
        while finished == False:
            finished = True # 每一次循环都先把 finished 标志置为 True，若出现替换后还有需要进行替换的集合时则置 False
            for unend_symbol in self.follow: # 遍历 follow 集里的每一个集合
                for element in self.follow[unend_symbol]: # 遍历每一个集合里的每一个元素
                    if element.get('type') == 'FIRST': # 若该元素需要展开，如：FIRST(X)
                        replace_symbol = element['name'] # 拿到 X
                        position = element['position']
                        index = element['index']
                        replace_list = self.first[replace_symbol] # 拿到当前 FIRST(X) 的集合

                        # 把当前集合中的 FIRST(X) 删掉
                        del_index = self.follow[unend_symbol].index(element)
                        del self.follow[unend_symbol][del_index]

                        # 把当前 FIRST(X) 集合中的所有元素都加到当前集合中来
                        for replace_dict in replace_list: # replace_dict 为当前 FIRST(X) 中的元素
                            if replace_dict['name'] == 'epsilon': # 如果是空字符，还需要对 X 的下一个字符进行判断
                                right = self.grammar[position]['Right'] # 拿到 X 所在产生式右边的列表
                                if index >= len(right) - 1: # 若 X 已是最后一个符号，则添加 follow
                                    finished = False
                                    tmp_dict = {}
                                    tmp_dict['type'] = 'FOLLOW'
                                    tmp_dict['name'] = self.grammar[position]['Left']
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.follow[unend_symbol]:
                                        self.follow[unend_symbol].append(tmp_dict)
                                else: # 若 X 后面还有符号，则应加入下一个符号的 first 集
                                    tmp_dict = {}
                                    if right[index + 1]['TYPE'] == 'UNEND': # 非终结符
                                        finished = False
                                        tmp_dict['type'] = 'FIRST'
                                        tmp_dict['index'] = index + 1
                                    tmp_dict['name'] = right[index + 1]['name']
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.follow[unend_symbol]:
                                        self.follow[unend_symbol].append(tmp_dict)
                            else:
                                tmp_dict = replace_dict.copy()
                                tmp_dict['position'] = position
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)
                    elif element.get('type') == 'FOLLOW': # 若该元素需要展开，如：FOLLOW(X)
                        replace_symbol = element['name'] # 拿到 X
                        position = element['position']
                        replace_list = self.follow[replace_symbol] # 拿到当前 FOLLOW(X) 的集合

                        # 把当前集合中的 FOLLOW(X) 删掉
                        del_index = self.follow[unend_symbol].index(element)
                        del self.follow[unend_symbol][del_index]

                        # 把当前 FOLLOW(X) 集合中的所有元素都加到当前集合中来
                        for replace_dict in replace_list:
                            if replace_dict['name'] != unend_symbol: # 首先，要加入的元素的名字不能和当前集合的名字相同
                                # 其次，要加入的元素的名字不能和当前集合中已经存在的元素的名字相同
                                already_exist = False
                                for dict in self.follow[unend_symbol]:
                                    if dict['name'] == replace_dict['name']:
                                        already_exist = True
                                        break
                                if already_exist == False:
                                    tmp_dict = replace_dict.copy()
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.follow[unend_symbol]:
                                        if tmp_dict.get('type') == 'FOLLOW' or tmp_dict.get('type') == 'FIRST':
                                            finished = False
                                        self.follow[unend_symbol].append(tmp_dict)
                    else:
                        continue
        
        print("目前得到的 follow 集：")
        for unend_symbol in self.follow:
            print(unend_symbol, '——', self.follow[unend_symbol])
        print()

        return 0
    
    #文法分析表函数,构造表后直接打印出来,
    def AnalyzeTable(self):
        return 0

    #符号栈函数,文法的存储数组是self.grammar,构造表后直接打印出来
    #比如 self.grammar = [{'Left': 'E', 'Right': [{'name': 'T', 'TYPE': 'UNEND'}, {'name': 'G', 'TYPE': 'UNEND'}]}]
    def SymbolStack(self,symbol):
        return 0


    def __init__(self, inputfile):
        self.inputfile = inputfile
        if not os.path.exists(inputfile):
            print(f"\033[31mcinc: fatal error: no such file: {inputfile}.\033[0m")
            print("compilation terminated.")
            exit(1)
    
    def run(self):
        self.Vg = [] #非终结符
        self.Vt = [] #终结符
        self.grammar = [] #存放文法的数组
        self.first = {} #存放first集， eg:{"first":"E", "content":['a','(']}
        self.follow = {} #存放follow集 eg:{"follow":"E", "content":['a','(']}
        self.analyse = [[]] 
        '''
        self.analyse = [
            [null, 'a', 'b', 'c', ..., '#'],
            ['A',处理后产生式() , , , , , , , , , , , , ],
            ['B', , , , , , , , , , , , , ],
            .......

        ]
        '''
           
        with open(self.inputfile, "r", encoding="utf-8") as f:
            self.Vg = f.readline().replace("\n","").split(" ")
            self.Vt = f.readline().replace("\n","").split(" ")
            for line in f.readlines():
                word =line.replace("\n","").split("->")
                right =word[1].split("|")
                for i in range(len(right)):
                    right1 =[]
                    rightson = right[i].strip().split(" ")
                    for j in range(len(rightson)):
                        if rightson[j] in self.Vg:
                            right1.append({"name":rightson[j],"TYPE":"UNEND"})
                        else:
                            right1.append({"name":rightson[j],"TYPE":"END"})
                    self.grammar.append({"Left":word[0][0],"Right":right1})
        #求解first集和follow集
        self.FirstFollow()

        #求语法分析表
        self.AnalyzeTable()

        #求符号栈
        symbol = input("输入一个字符串：")
        self.SymbolStack(symbol)






if __name__ == '__main__':
    inputfile = "test.txt"
    grammar = GrammarAnalyzer(inputfile)
    grammar.run()

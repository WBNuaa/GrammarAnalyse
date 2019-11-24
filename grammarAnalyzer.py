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

            right = grammar['Right'][0] # 看产生式右边的第一个符号
            if right['TYPE'] == 'END': # 如果是终结符，直接加入 first 集即可
                tmp_dict = {}
                tmp_dict['name'] = right['name']
                tmp_dict['position'] = self.grammar.index(grammar)
                self.first[left].append(tmp_dict)
            elif right['TYPE'] == 'UNEND': # 如果是非终结符，则需要加入该非终结符的 first 集
                finished = False
                tmp_dict = {}
                tmp_dict['type'] = 'UNEND'
                tmp_dict['name'] = right['name']
                tmp_dict['position'] = self.grammar.index(grammar)
                tmp_dict['index'] = 0
                self.first[left].append(tmp_dict)
        
        while finished == False:
            finished = True
            for unend_symbol in self.first:
                for element in self.first[unend_symbol]: # 这里拿到的是一个字典                    
                    if element.get('type') == 'UNEND':
                        finished = False
                        replace_symbol = element['name']
                        position = element['position']
                        index = element['index']
                        replace_list = self.first[replace_symbol]
                        
                        # 先把现在列表里的那个字典删掉
                        del self.first[unend_symbol][self.first[unend_symbol].index(element)]
                        
                        # 然后把要替换列表的所有字典都加到现在的列表里
                        for replace_dict in replace_list:
                            if replace_dict.get('type') == 'UNEND':
                                # 如果还是非终结符
                                tmp_dict = replace_dict.copy()
                                tmp_dict['position'] = position
                                tmp_dict['index'] = index
                                self.first[unend_symbol].append(tmp_dict)
                            else:
                                # 终结符
                                if replace_dict['name'] == 'epsilon':
                                    # 如果是空字符，需要到 grammar 里面去找
                                    for grammar in self.grammar:
                                        if grammar['Left'] == unend_symbol:
                                            right_list = grammar['Right']
                                            # right = grammar['Right'][index + 1]
                                            break
                                    if index + 1 > len(right_list) - 1:
                                        # 保留空字符
                                        tmp_dict = {}
                                        tmp_dict['name'] = 'epsilon'
                                        tmp_dict['position'] = position
                                        self.first[unend_symbol].append(tmp_dict)
                                    else:
                                        # 继续求 first 集
                                        right = grammar['Right'][index + 1]
                                        if right['TYPE'] == 'END': # 如果是终结符
                                            tmp_dict = {}
                                            tmp_dict['name'] = right['name']
                                            tmp_dict['position'] = position
                                            self.first[unend_symbol].append(tmp_dict)
                                        elif right['TYPE'] == 'UNEND': # 如果是非终结符
                                            # finished = False
                                            tmp_dict = {}
                                            tmp_dict['type'] = 'UNEND'
                                            tmp_dict['name'] = right['name']
                                            tmp_dict['position'] = position
                                            tmp_dict['index'] = index + 1
                                            self.first[unend_symbol].append(tmp_dict)
                                else:
                                    tmp_dict = replace_dict.copy()
                                    tmp_dict['position'] = position
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
        for unend_symbol in self.first:
            self.follow[unend_symbol] = []

        tmp_dict = {}
        tmp_dict['name'] = '#'
        tmp_dict['position'] = 0
        self.follow[self.grammar[0]['Left']].append(tmp_dict)

        finished = True
        for unend_symbol in self.follow:
            for grammar in self.grammar:
                right = grammar['Right'] # 拿到右边的列表 right
                for symbol in right: # symbol 是列表中的单个字典
                    if symbol['name'] == unend_symbol:
                        if right.index(symbol) + 1 > len(right) - 1:
                            if unend_symbol != grammar['Left']:
                                finished = False
                                tmp_dict = {}
                                tmp_dict['type'] = 'FOLLOW'
                                tmp_dict['name'] = grammar['Left']
                                tmp_dict['position'] = self.grammar.index(grammar)
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)
                        else:
                            if right[right.index(symbol) + 1]['TYPE'] == 'END':
                                # 终结符
                                tmp_dict = {}
                                tmp_dict['name'] = right[right.index(symbol) + 1]['name']
                                tmp_dict['position'] = self.grammar.index(grammar)
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)
                            else:
                                # 非终结符
                                finished = False
                                tmp_dict = {}
                                tmp_dict['type'] = 'FIRST'
                                tmp_dict['name'] = right[right.index(symbol) + 1]['name']
                                tmp_dict['position'] = self.grammar.index(grammar)
                                tmp_dict['index'] = right.index(symbol) + 1
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)

        while finished == False:
            finished = True
            for unend_symbol in self.follow:
                for element in self.follow[unend_symbol]:
                    if element.get('type') == 'FIRST':
                        # FIRST
                        finished = False
                        replace_symbol = element['name']
                        position = element['position']
                        index = element['index']
                        replace_list = self.first[replace_symbol]

                        # 先把现在列表里的那个字典删掉
                        del self.follow[unend_symbol][self.follow[unend_symbol].index(element)]

                        for replace_dict in replace_list:
                            if replace_dict['name'] == 'epsilon':
                                right = self.grammar[position]['Right']
                                if index >= len(right) - 1:
                                    # 添加 follow
                                    tmp_dict = {}
                                    tmp_dict['type'] = 'FOLLOW'
                                    tmp_dict['name'] = self.grammar[position]['Left']
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.follow[unend_symbol]:
                                        self.follow[unend_symbol].append(tmp_dict)
                                else:
                                    # 添加 first
                                    if right[index + 1]['TYPE'] == 'END':
                                        # 终结符
                                        tmp_dict = {}
                                        tmp_dict['name'] = right[index + 1]['name']
                                        tmp_dict['position'] = position
                                        if tmp_dict not in self.follow[unend_symbol]:
                                            self.follow[unend_symbol].append(tmp_dict)
                                    else:
                                        # 非终结符
                                        tmp_dict = {}
                                        tmp_dict['type'] = 'FIRST'
                                        tmp_dict['name'] = right[index + 1]['name']
                                        tmp_dict['position'] = position
                                        tmp_dict['index'] = index + 1
                                        if tmp_dict not in self.follow[unend_symbol]:
                                            self.follow[unend_symbol].append(tmp_dict)
                            else:
                                tmp_dict = replace_dict.copy()
                                tmp_dict['position'] = position
                                if tmp_dict not in self.follow[unend_symbol]:
                                    self.follow[unend_symbol].append(tmp_dict)
                    elif element.get('type') == 'FOLLOW':
                        # FOLLOW
                        finished = False
                        replace_symbol = element['name'] # B
                        position = element['position'] # 4
                        replace_list = self.follow[replace_symbol] # FOLLOW(T)

                        # 先把现在列表里的那个字典删掉
                        del self.follow[unend_symbol][self.follow[unend_symbol].index(element)]

                        for replace_dict in replace_list:
                            if replace_dict['name'] != unend_symbol:
                                already_exist = False
                                for dict in self.follow[unend_symbol]:
                                    if dict['name'] == replace_dict['name']:
                                        already_exist = True
                                        break
                                if already_exist == False:
                                    tmp_dict = replace_dict.copy()
                                    tmp_dict['position'] = position
                                    if tmp_dict not in self.follow[unend_symbol]:
                                        self.follow[unend_symbol].append(tmp_dict)
                    else:
                        continue
        
        print("目前得到的 follow 集：")
        for unend_symbol in self.follow:
            print(unend_symbol, '——', self.follow[unend_symbol])

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

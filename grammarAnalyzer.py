import os
import re
import numpy as np

class GrammarAnalyzer:

    #first集follow集函数，文法的存储数组是self.grammar,得到的结果打印出来并存到数组self.first,self.follow
    #比如self.grammar = [{'Left': 'E', 'Right': [{'name': 'T', 'TYPE': 'UNEND'}, {'name': 'G', 'TYPE': 'UNEND'}]}]
    def FirstFollow(self):
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
        self.first = [] 
        '''存放first集， eg:{"first":"E", "content":[
            ['a','('],]}'''
        self.follow = [] #存放follow集 eg:{"follow":"E", "content":['a','(']}
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

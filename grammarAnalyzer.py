import os
import re

class GrammarAnalyzer:

    #first集follow集函数，文法的存储数组是self.grammar,得到的结果打印出来并存到数组self.first,self.follow
    #比如self.grammar = ['E->TG', 'G->+TG|-TG', 'T->FS', 'S->*FS', 'S->/FS', 'F->(E)', 'F->i']
    def FirstFollow(self):
        return 0
    
    #文法分析表函数,构造表后直接打印出来或新建一个Listresult.xlsx文件，然后将表存到文件中
    def AnalyzeTable(self):
        #file1 = open("listresult.xlsx",'w')
        #file1.write(list)
        return 0

    #符号栈函数,文法的存储数组是self.grammar,构造表后直接打印出来或新建一个Stackresult.xlsx文件，然后将表存到文件中
    #比如 self.grammar = ['E->TG', 'G->+TG|-TG', 'T->FS', 'S->*FS', 'S->/FS','F->(E)', 'F->i']
    def SymbolStack(self):
        return 0


    def __init__(self, inputfile):
        self.inputfile = inputfile
        if not os.path.exists(inputfile):
            print(f"\033[31mcinc: fatal error: no such file: {inputfile}.\033[0m")
            print("compilation terminated.")
            exit(1)
    
    def run(self):
        self.grammar = [] #存放文法的数组
        self.first = [] #存放first集， eg:{"first":"first(E)", "content":"a,("}
        self.follow = [] #存放follow集 eg:{"follow":"follow(E)", "content":"a,("}
        with open(self.inputfile, "r", encoding="utf-8") as f:
            for line in f.readlines():
                word = line.replace(" ","").replace("\n","")
                self.grammar.append(word)
        print(self.grammar)
        #求解first集和follow集
        self.FirstFollow()

        #求语法分析表
        self.AnalyzeTable()

        #求符号栈
        self.SymbolStack()






if __name__ == '__main__':
    inputfile = "test.txt"
    grammar = GrammarAnalyzer(inputfile)
    grammar.run()

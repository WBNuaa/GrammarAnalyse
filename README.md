# GrammarAnalyse 语法分析器

## 数据结构

### 原产生式
```
E -> + T
T -> a G
G -> b
```

### 处理后产生式
#print(grammer[0]['left'], '->')
#for i in grammer[0]['right']:
#print(i['name'], ' ')
```
grammer = [{
    'left':'E', 
    'right':[{
        'name':'+', 
        'TYPE':'END'
    }, {
        'name':'T', 
        'TYPE':'UNEND'
}]}, {
    'left' : 'T', 
    'right' : [{
        'name':'a', 
        'TYPE':'END'
    }, {
        'name':'G', 
        'TYPE':'UNEND'
}]}, {
    'left' : 'G', 
    'right' : [{
        'name':'b', 
        'TYPE':'END'
}]}]
```

### first 集
```
{
    'E': [
        {
            'name':'a', 
            'position':0
        }, {
            'name':'b', 
            'position':1
        }
    ],
    'T': [
        {
            'name':'c', 
            'position':2
        }, {
            'name':'d', 
            'position':3
        }
    ]
}
```

### follow 集和 first 集类似
        
### 分析表
```
analyze = [
    [null, 'a', 'b', 'c', ..., '#'],
    ['A',处理后产生式() , , , , , , , , , , , , ],
    ['B', , , , , , , , , , , , , ],
    .......
]
```

## 测试用例
```
课本 81 页第 2 题

E -> T A
A -> + E
A -> epsilon
T -> F B
B -> T
B -> epsilon
F -> P C
C -> * C
C -> epsilon
P -> ( E )
P -> a
P -> b
P -> ^

注：原来的 E' => A，T' => B，F' => C

FIRST(E) = {(, a, b, ^}
FIRST(A) = {+, epsilon}
FIRST(T) = {(, a, b, ^}
FIRST(B) = {(, a, b, ^, epsilon}
FIRST(F) = {(, a, b, ^}
FIRST(C) = {*, epsilon}
FIRST(P) = {(, a, b, ^}

FOLLOW(E) = {#, )}
FOLLOW(A) = {#, )}
FOLLOW(T) = {+, ), #}
FOLLOW(B) = {+, ), #}
FOLLOW(F) = {(, a, b, ^, +, ), #}
FOLLOW(C) = {(, a, b, ^, +, ), #}
FOLLOW(P) = {*, (, a, b, ^, +, ), #}
```
```
PPT第四章P39例子
E -> T E'
E' -> + T E' | epsilon
T -> F T'
T' -> * F T' | epsilon
F -> ( E ) | i

FIRST(E) ={(，i}	 FOLLOW(E) = {)，#}
FIRST(E')={+，ε}	 FOLLOW(E') = {)，#}
FIRST(T) ={(，i}	 FOLLOW(T) = {+，) ，#}
FIRST(T')={*，ε}	 FOLLOW(T') = {+，)，#}
FIRST(F) ={(，i}	 FOLLOW(F)  = {*，+，)，#}

	i	  +	     *	   （	  ）	#
E	E→TE'			    E→TE'		
E'		  E'→+TE'			  E'→ε	E'→ε
T	T→FT'			    T→FT'		
T'		  T'→ε	 T'→*FT'	  T'→ε	T'→ε
F	F→i			        F→(E)		
```
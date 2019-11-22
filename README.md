# GrammarAnalyse
语法分析器
        原产生式
        E -> + T
        T -> a G
        G -> b
        处理后产生式
        #print(grammer[0]['left'], '->')
        #for i in grammer[0]['right']:
        #   print(i['name'], ' ')
        grammer =
        [
            {
                'left' : 'E', 
                'right' : [
                    {
                        'name' : '+', 
                        'TYPE' : 'END'
                    }, 
                    {
                        'name' : 'T', 
                        'TYPE' : 'UNEND'
                    }
                ]
            },
            {
                'left' : 'T', 
                'right' : [
                    {
                        'name' : 'a', 
                        'TYPE' : 'END'
                    }, 
                    {
                        'name' : 'G', 
                        'TYPE' : 'UNEND'
                    }
                ]
            },
            {
                'left' : 'G', 
                'right' : [
                    {
                        'name' : 'b', 
                        'TYPE' : 'END'
                    }
                ]
            }
        ]
        first集
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
            ],
        }
        follow集类似
        分析表
        analyze = [
            [null, 'a', 'b', 'c', ..., '#'],
            ['A',处理后产生式() , , , , , , , , , , , , ],
            ['B', , , , , , , , , , , , , ],
            .......

        ]
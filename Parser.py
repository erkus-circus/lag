
from Lexer import LexerReader
import Lexer as lexer
from pprint import pprint

class Node(dict):
    def __init__(self,name,*args):
        self['node_name'] = name
        self['children'] = []
        self.add(*args)
        
    def add(self,*args):
        for i in args:
            self['children'].append(i)

class CallNode(Node):
    def __init__(self,name,args):
        super().__init__('call')
        self.add({'args':args},{'name':name})

class StrNode(Node):
    def __init__(self,content):
        super().__init__('str')
        self.add({'string':content})

class ArgNode(Node):
    def __init__(self,args):
        super().__init__('args')
        for i in args:
            self.add(i)


def getAST(lex, nodeName='program'):
    scriptRunning = True
    reader = LexerReader(lex)
    nodePath = []
    topNode = Node(nodeName)
    reader.stepUp()
    while reader.getToken():
        tok = reader.getToken()
        reader.stepUp()

        # get type of token
        for i in tok:
            tokName = i
            tokVal = tok[i]

        if tokName == 'statement':
            reader.stepUp()
            
            if tokVal == 'call':
                topNode.add(ASTCall(reader.hereOn()))
    return topNode

def ASTCall(lex):
    reader = LexerReader(lex)
    funcDat = {
        'args': [],
        'name': ''
    }

    inLoop = True
    gotFuncName = False
    gotArgs = False
    
    while inLoop:
        reader.stepUp()
        if not gotFuncName:
            if reader.getName() == 'id':
                funcDat['name'] += reader.getChar()

            elif reader.getName() == 'whiteSpace' and funcDat['name'].strip() == '':
                continue
            elif reader.getChar() == ',':
                gotFuncName = True
            
        if not gotArgs:
            if reader.getName() == 'strSep':
                funcDat['args'].append(ASTStr(reader.hereOn()))
                inLoop = 0

    return CallNode(funcDat['name'],ArgNode(funcDat['args']))

def ASTStr(lex):
    reader = LexerReader(lex)
    reader.stepUp()
    st = ''
    inLoop = 0
    escaped = 0

    while not inLoop:
        reader.stepUp()
        char = reader.getChar()
        if escaped:
            st += char
            escaped = 0
            continue
            
        else:
            if char == '\\':
                escaped = 1
                continue

            if reader.getName() == 'strSep':
                print('strSep')
                inLoop = 1
                break
            else:
                print('add:',char)
                st += char
        
    print(st)
    return StrNode(st)
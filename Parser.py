
from Lexer import LexerReader
import Lexer as lexer
from pprint import pprint
class Node():
    def __init__(self,name,children = []):
        self.name = name
        self.children = children

    def __str__(self):
        return str(self.children)

    def add(self,*args):
        for i in args:
            self.children.append(i)


class CallNode(Node):
    def __init__(self,name,args):
        super().__init__('call')
        self.add(Node('args',args),Node('name',name))

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
            break

        if tokName == 'statement' and reader.stepUp().getName() == 'colon':
            #if tokVal == 'expr': TODO
            #    topNode.add(ASTExpr())
            if tokVal == 'call':
                topNode.add(ASTCall(reader.hereOn()))
    return topNode

def ASTCall(lex):
    reader = LexerReader(lex)
    reader.stepUp()
    callNode = Node('call')
    
    while reader.getToken() and not reader.getToken() == lexer.lexer(';')[0]:
       reader.stepUp()
    return callNode

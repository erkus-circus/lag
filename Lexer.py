"""
 " Lexer for lexing into tokens
 " Lexer Version 1.1
 " Eric Diskin
 " 2019
"""


import sys
from pprint import pprint

mathOperators = '*%+/-' # operators for math

idents = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

numbers = '1234567890'

statements = 'call expr func'.split()

class Type(object):
    def __init__(self,typeList,name,stackable=True):
        self.typeList = typeList
        self.stackable = stackable
        self.name = name

    def isOfType(self,char):
        return char in self.typeList

tNum = Type(numbers,'num')
tMathOperator = Type(mathOperators,'operator',False)
tDotOperator = Type('.','dot')
tComma = Type(',','comma')
tSpace = Type(' \n','whiteSpace')
tString = Type('\'"','strSep',False)
tParenthesis = Type('()','parenethesis',False)
tCurlyBracket = Type('{}','curlybracket',False)
tColon = Type(':','colon',False)
tSemicolon = Type(';','semicolon',False)
tIdentifier = Type(idents,'id')
tExclamation = Type('!','explanation',False)
tForwardSlash = Type('/','fslash',False)
tBackSlash = Type('\\','bslash',False)

types = [
    tNum,
    tIdentifier, 
    tMathOperator,
    tDotOperator,
    tSpace,
    tString,
    tSemicolon,
    tParenthesis,
    tColon,
    tCurlyBracket,
    tComma,
    tExclamation,
    tForwardSlash,
    tBackSlash,
]

def getCharType(char):
    for t in types:
        if t.isOfType(char):
            return t
    return

def getTypeFromName(typeName):
    for t in types:
        if t.name == typeName:
            return t
    return


def lexer(line,lnum=0):
    lexed = [] # what has been lexed

    col = 0

    for char in line:
        col += 1
        
        charType = getCharType(char)

        if not charType:
            print('Invalid character: `%s` (%s,%s).' % (char,lnum,col))
            lexed = []
            break
        
        if len(lexed) > 0:
            made = 0
            for i in lexed[-1]:
                if i == charType.name and charType.stackable:
                    lexed[-1][charType.name] += char
                    made = 1
                if made and i == 'id':
                    # check if id is a statement
                    for j in statements:
                        if j == lexed[-1][i]:
                            lexed[-1] = {'statement':lexed[-1]['id']}
                            break
            if made:
                continue

        lexed.append({charType.name:char})
    return lexed

def lexText(inpt):
    lexed = []
    lnum = 0
    for line in inpt.split('\n'):
        lnum += 1
        lexed.extend(lexer(line,lnum))
    return lexed

def lexFile(file):
    return lexText(file.read())


class LexerReader():
    def __init__(self,lex):
        self.lex = lex

    index = None

    def stepBack(self,steps=1):
        self.index -= steps
        return self
    
    def stepUp(self,steps=1):
        if self.index == None:
            self.index = -1
        self.index += steps
        return self
    
    def getChar(self):
        if self.index > len(self.lex) - 1:
            return None
        for i in self.getToken():
            return self.getToken()[i]

    
    def hereOn(self):
        """
        Return from current index till end of lexed
        """
        if self.index > len(self.lex) - 1:
            return None
        return self.lex[self.index:]
    
    def getToken(self):
        if self.index > len(self.lex) - 1:
            return None
        return self.lex[self.index]

    def getName(self):
        if self.index > len(self.lex) - 1:
            return None
        for i in self.lex[self.index]:
            return i

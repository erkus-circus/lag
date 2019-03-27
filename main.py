
import Lexer as lexer
import Parser
from pprint import pprint

exampleScript = """
call: write, 'Hello World';
"""

lexed = lexer.lexText(exampleScript)

# pprint(lexed)
ast = Parser.getAST(lexed)

pprint(ast)
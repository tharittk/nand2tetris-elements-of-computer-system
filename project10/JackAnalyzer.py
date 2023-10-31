from JackTokenizer import Tokenizer
from CompilationEngine import CompilationEngine

import sys
if __name__ == '__main__':
    inputFile =sys.argv[1]

    tkn = Tokenizer(inputFile)
    tkn.run()

    cpe = CompilationEngine(tkn.result)
    cpe.run()

    with open('./ExpressionLessSquare/OutFull.xml', 'w') as f:
        for token in cpe.result:
            f.write(token + '\n')
        

# Jack Tokenizer


keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false','null','this','let','do', 'if', 'else', 'while', 'return']
#symbol = ['{', '}', '(', ')', '[', ']', '.', ',',';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


class Tokenizer():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',',';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false','null','this','let','do', 'if', 'else', 'while', 'return']
        self.tokens = []
        self.currentToken = ''
        self.charStream = ''
        self.currentCharIdx = 0
    def _read_input_file(self):
        tokens = []
        with open(self.inputFile) as f:
            # process text file
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                # Comments or empty line
                if line[0:2] == "/*" or line[0:2] == "\n" or line[0:2] == '//' or line == '': 
                    pass
                else:
                    line = line.strip('\n')
                    line = line.strip('\t')
                    # inline comment
                    line = line.split("//")[0]
                    # Each character in line
                    for char in line:                        
                        self.charStream += char

    def hasMoreTokens(self):
        nchar = len(self.charStream)
        if self.currentCharIdx <= nchar - 1:
            return True
        else:
            return False
    
    # get the next token from the input and makes it
    # the current --- most difficult
    def advance(self):
        self.currentToken = ''
        currentChar = self.charStream[self.currentCharIdx]
        # accumulate character until becomes a token
        while (currentChar not in self.SYMBOL) and (currentChar != ' '):
            self.currentToken += currentChar
            self.currentCharIdx += 1
            currentChar = self.charStream[self.currentCharIdx]

        # no appending since '' + " " is never accounted
        if self.currentToken != '':
            self.tokens.append(self.currentToken)

        if currentChar == ' ':
            self.currentCharIdx += 1
        

        if currentChar in self.SYMBOL:
            self.tokens.append(currentChar)
            self.currentCharIdx += 1


    # return the type of the current token
    def tokenType(self):

        return 'KEYWORD'
    
    # return the keyword of the current token call iff current token type is KEYWORD
    def keyWord(self):

        return 0
    
    # return the symbol of the current token call iff current token type is SYMBOL
    def symbol(self):

        return 0        

    # return the string of the current token call iff current token type is IDENTIFIER
    def identifier(self):

        return 0        
    
    # return the integer value of the current token call iff current token type is INT_CONST
    def intVal(self):

        return 0   

    # return the string value of the current token call iff current token type is STRING_CONST
    def stringVal(self):

        return 0   

if __name__ == "__main__":
    tkn = Tokenizer('./Square.Jack')
    tkn._read_input_file()
    while tkn.hasMoreTokens():
        tkn.advance()

    #for token in tkn.tokens:
    #    print(token)

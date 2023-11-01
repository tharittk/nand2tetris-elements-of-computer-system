# CompilationEngine

class CompilationEngine():
    def __init__(self, xmlFile):
        #self.tokenizedInputList = tokenizedInput[1:-1] #exclude[<token>]
        self.tokenizedInputList = self._read_tokenized_xml(xmlFile)[1:-1]
        self.currentToken = ''
        self.currentTokenIndex = -1 # not yet look at any token
        self.result = []
        

    # during testing
    def _read_tokenized_xml(self, xml_file):
        xmlLines = []
        with open(xml_file) as f:
            for line in f:
                xmlLines.append(line.strip('\n'))
        return xmlLines
    

    def _eat(self, stringIn):
        tokenAhead = self.tokenizedInputList[self.currentTokenIndex + 1]
        stringToken = tokenAhead.split(" ")[1]
        if stringIn != stringToken:
            raise ValueError
        else:
            self._advance()

    def _advance(self):
        self.currentTokenIndex += 1
        self.currentToken = self.tokenizedInputList[self.currentTokenIndex]

    def _getCurrentTokenFull(self):
        return self.tokenizedInputList[self.currentTokenIndex]

    def _getTokenContent(self):
        return  self.currentToken.split(" ")[1]
    
    def _getTokenType(self):
        return  self.currentToken.split(">")[0].split("<")[1]
    
    def printCompileGeneral(self, stringPrint):
        self.result.append(stringPrint)

    def printCompiledTokenFull(self):
        line = self._getCurrentTokenFull()
        self.result.append(line)

    # compile a complete class
    def compileClass(self):
        pass

    # compile a static variable or a field decoration
    def compileClassVarDec(self):
        pass

    # compile a complete method, function, or constructor
    def compileSubroutine(self):
        pass

    # compile a (possibly empty) parameter list
    # does not handle the enclosing parentheses tokens ( and )
    def compileParameterList(self):
        pass

    # compile a subroutine's body
    def compileSubroutineBody(self):
        pass

    # compile a var declaration
    def compileVarDec(self):
        pass

    # compile a sequents of statements
    # does not handle enclosing { }
    def compileStatements(self):
        pass

    # compile a let statement
    def compileLet(self):
        pass

    # compile an if with possibly else clause
    def compileIf(self):
        pass

    # compile a while statement
    def compileWhile(self):
    #    eat(while); code to handle / write while
    #    eat ('('); code to hand
    #    compileExpression
        self._eat('while')
        self.printCompileGeneral('<whileStatement>')
        self.printCompiledTokenFull()
        self._eat('(')
        self.printCompiledTokenFull()
        # recursion
        self._eat(')')
        self.printCompiledTokenFull()
        self._eat('{')
        self.printCompiledTokenFull()
        self._eat('}')
        self.printCompiledTokenFull()
        self.printCompileGeneral('</whileStatement>')


    # compile a do statement
    def compileDo(self):
        pass

    # compile a return statement
    def compileReturn(self):
        pass

    # compile an expression
    def compileExpression(self):
        pass

    # compile a term
    # if current token is identifier,
    # must resolve into var, array, or subroutine call
    # with single look ahead
    def compileTerm(self):
        pass

    # compile a possibly empty comma separated list
    # of expressions. Return the number of 
    # expressions in the list
    def compileExpressionList(self):
        pass

    def run(self):
        #n_token = len(self.tokenizedInputList)
        #for i in range(n_token):
        self.compileWhile()

if __name__ == "__main__":

    #test = ['<tokens>','<keyword> while <\keyword>', '<symbol> ( <\symbol>','<\tokens>']
    cpe = CompilationEngine('./OutWhile.xml')
    
    print(cpe.tokenizedInputList)

    cpe.run()
    #cpe._eat('while')
    #print(cpe.currentToken, cpe.currentTokenIndex)
    #print(cpe.getTokenContent(), cpe.getTokenType())
    for line in cpe.result:
        print(line)
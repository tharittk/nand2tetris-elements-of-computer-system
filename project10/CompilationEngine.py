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

    def _getTokenLexical(self):
        return  self.currentToken.split(" ")[1]
    
    def _getTokenLexicalType(self):
        return  self.currentToken.split(">")[0].split("<")[1]
    
    def printCompileGeneral(self, stringPrint):
        self.result.append(stringPrint)

    def printCompiledTokenFull(self):
        line = self._getCurrentTokenFull()
        self.result.append(line)

    # compile a complete class
    def compileClass(self):

        # 'class'
        self._eat('class')
        self.printCompileGeneral('<class>')
        self.printCompiledTokenFull()
        self._advance()

        # className
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        # '{'
        self._eat('{')
        self.printCompiledTokenFull()
        self._advance()

        #
        # class var Dec, subroutine Dec
        #

        # '}'
        self._eat('}')
        self.printCompiledTokenFull()
        self.printCompileGeneral('<\class>')

    # compile a static variable or a field decoration
    def compileClassVarDec(self):

        self.printCompileGeneral('<classVarDec>')
        # (static | field)
        self._advance()
        assert self._getTokenLexical() in ['static', 'field']
        self.printCompiledTokenFull()
        self._advance()

        # type
        assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        #
        # optional other ',' + varName*
        #

        # ';'
        self._eat(';')
        self.printCompiledTokenFull()
        self.printCompileGeneral('<\classVarDec>')

    # compile a complete method, function, or constructor
    def compileSubroutine(self):

        self.printCompileGeneral('<subroutineDec>')

        # (constructor | function | method)
        assert self._getTokenLexical() in ['constructor', 'function', 'method']
        self.printCompiledTokenFull()
        self._advance()

        # ('void' | type)
        assert (self._getTokenLexical() in ['void','int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier' 
        self.printCompiledTokenFull()
        self._advance()

        # subRoutineName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        # '('
        self._eat('(')
        self.printCompiledTokenFull()

        #
        # ParameterList
        #

        # '('
        self._eat(')')
        self.printCompiledTokenFull()

        #
        # SubRoutineBody
        #

        self.printCompileGeneral('<\subroutineDec>')


    # compile a (possibly empty) parameter list
    # does not handle the enclosing parentheses tokens ( and )
    def compileParameterList(self):
        self.printCompileGeneral('<parameterList>')

        # optional - all

        # type
        #assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        #self.printCompiledTokenFull()
        #self._advance()

        # varName
        #assert self._getTokenLexicalType() == 'identifier'
        #self.printCompiledTokenFull()
        #self._advance()

        self.printCompileGeneral('<\parameterList>')

    # compile a subroutine's body
    def compileSubroutineBody(self):
        self.printCompileGeneral('<subRoutineBody>')
        self._eat('{')
        self.printCompiledTokenFull()

        #
        # statements
        #

        self._eat('}')
        self.printCompiledTokenFull()
        self.printCompileGeneral('</subRoutineBody>')

    # compile a var declaration
    def compileVarDec(self):
        self.printCompileGeneral('<varDec>')
        # 'var'
        self._eat('var')
        self.printCompiledTokenFull()

        # type
        assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        # optional ------
        # while next is ','


        self.printCompileGeneral('</varDec>')

    # compile a sequences of statements
    def compileStatements(self):
        self.printCompileGeneral('<statements>')

        # while there are next statements
        while self._getTokenLexical() in ['let', 'if', 'while', 'do' ,'return']:
            if self._getTokenLexical() == 'let':
                self.compileLet()
            elif self._getTokenLexical() == 'if':
                self.compileIf()
            elif self._getTokenLexical() == 'while':
                self.compileWhile()
            elif self._getTokenLexical == 'do':
                self.compileDo()
            elif self._getTokenLexical() == 'return':
                self.compileReturn

            self._advance()

        self.printCompileGeneral('</statements>')

        
    # compile a let statement
    def compileLet(self):
        self.printCompileGeneral('<letStatement>')
        # 'let'
        self._eat('let')
        self.printCompiledTokenFull()
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        #
        # optional expression
        #
        
        # '='
        self._eat('=')
        self.printCompiledTokenFull()
        self._advance()

        #
        # compile expression
        #
        
        self.printCompileGeneral('</letStatement>')

    # compile an if with possibly else clause
    def compileIf(self):
        self.printCompileGeneral('<ifStatement>')

        # 'if'
        self._eat('if')
        self.printCompiledTokenFull()
        self._advance()

        # '('
        self._eat('(')
        self.printCompiledTokenFull()
        self._advance()

        #
        # expression
        #

        # ')'
        self._eat(')')
        self.printCompiledTokenFull()
        self._advance()

        # '{'
        self._eat('{')
        self.printCompiledTokenFull()
        self._advance()

        # statements
        self.compileStatements()

        # '}'
        self._eat('}')
        self.printCompiledTokenFull()
        self._advance()

        # optional else      
        if self._getTokenLexical() == 'else':
            self._eat('else')
            self.printCompiledTokenFull()
            self._advance()

            self._eat('{')
            self.printCompiledTokenFull()
            self._advance()

            # statements
            self.compileStatements()

            self._eat('}')
            self.printCompiledTokenFull()
            self._advance()

        self.printCompileGeneral('</ifStatement>')

    # compile a while statement
    def compileWhile(self):

        self.printCompileGeneral('<whileStatement>')

        # 'while'
        self._eat('while')
        self.printCompiledTokenFull()
        self._advance()

        # '('
        self._eat('(')
        self.printCompiledTokenFull()
        self._advance()

        #
        # expression
        #

        # ')'
        self._eat(')')
        self.printCompiledTokenFull()
        self._advance()

        # '{'
        self._eat('{')
        self.printCompiledTokenFull()
        self._advance()

        # statements
        self.compileStatements()

        # '}'
        self._eat('}')
        self.printCompiledTokenFull()
        self._advance()

        self.printCompileGeneral('</whileStatement>')


    # compile a do statement
    def compileDo(self):
        self.printCompileGeneral('<doStatement>')

        # 'do'
        self._eat('do')
        self.printCompiledTokenFull()
        self._advance()

        #
        # subroutine call
        #

        self.printCompileGeneral('</doStatement>')

    # compile a return statement
    def compileReturn(self):
        self.printCompileGeneral('<returnStatement>')
        self._eat('return')
        self.printCompiledTokenFull()
        self._advance()

        #
        # optional expression
        #
        
        self._eat(';')
        self.printCompiledTokenFull()
        self.printCompileGeneral('</returnStatement>')

    # compile an expression
    def compileExpression(self):
        
        # PLACEHOLDER
        self._advance()
        self.printCompiledTokenFull()
        #


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

    cpe = CompilationEngine('./OutWhile.xml')
    print(cpe.tokenizedInputList)
    cpe.run()
    for line in cpe.result:
        print(line)
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

    def eat_write_advance(self, stringIn):
        self._eat(stringIn)
        self.printCompiledTokenFull()
        self._advance()

    def _getCurrentTokenFull(self):
        return self.tokenizedInputList[self.currentTokenIndex]

    def _getTokenLexical(self):
        return  self.currentToken.split(" ")[1]
    
    def _getLookAheadLexical(self):
        tokenAhead = self.tokenizedInputList[self.currentTokenIndex + 1]
        stringToken = tokenAhead.split(" ")[1]
        return stringToken
    
    def _getTokenLexicalType(self):
        return  self.currentToken.split(">")[0].split("<")[1]
    
    def printCompileGeneral(self, stringPrint):
        self.result.append(stringPrint)

    def printCompiledTokenFull(self):
        line = self._getCurrentTokenFull()
        self.result.append(line)

    # compile a complete class
    def compileClass(self):

        self.printCompileGeneral('<class>')
        # 'class'
        self.eat_write_advance('class')

        # className
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        # '{'
        self.eat_write_advance('{')


        # optional class var dec
        if self._getTokenLexical() in  ['static', 'field']:
            self.compileClassVarDec()

        # optional subroutine dec
        if self._getTokenLexical() in ['constructor', 'function', 'method']:
            self.compileSubroutine()

        # '}'
        self.eat_write_advance('}')
        self.printCompileGeneral('<\class>')


    # compile a static variable or a field decoration
    def compileClassVarDec(self):

        self.printCompileGeneral('<classVarDec>')
        # (static | field)
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
        
        # optional next variable
        while self._getTokenLexical() == ',':
            # ','
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()
            self._advance()


        # ';'
        self.eat_write_advance(';')

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
        self.eat_write_advance('(')

        # parameterList
        self.compileParameterList()

        # ')'
        self.eat_write_advance(')')

        # subroutine body
        self.compileSubroutineBody()


        self.printCompileGeneral('<\subroutineDec>')


    # compile a (possibly empty) parameter list
    def compileParameterList(self):
        self.printCompileGeneral('<parameterList>')

        if (self._getTokenLexical() in ['int', 'char', 'boolean']) or (self._getTokenLexicalType() == 'identifier'):
            # type
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()
            self._advance()

            # optional next
            while self._getTokenLexical() == ',':
                # ','
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

        self.printCompileGeneral('<\parameterList>')

    # compile a subroutine's body
    def compileSubroutineBody(self):
        self.printCompileGeneral('<subRoutineBody>')
        
        self.eat_write_advance('{')

        # optional varDec
        if self._getTokenLexical() == 'var':
            self.compileVarDec()

        # statements
        self.compileStatements()

        # '}'
        self.eat_write_advance('}')

        self.printCompileGeneral('</subRoutineBody>')

    # compile a var declaration
    def compileVarDec(self):
        self.printCompileGeneral('<varDec>')

        # 'var'
        self.eat_write_advance('var')

        # type
        assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()


        # optional variable but same type
        while self._getTokenLexical() == ',':
            # ','
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()
            self._advance()

        # ';'
        self.eat_write_advance(';')
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
        self.eat_write_advance('let')

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        self._advance()

        #
        # optional expression
        #
        
        # '='
        self.eat_write_advance('=')

        #
        # compile expression
        #
        
        self.printCompileGeneral('</letStatement>')

    # compile an if with possibly else clause
    def compileIf(self):
        self.printCompileGeneral('<ifStatement>')

        # 'if'
        self.eat_write_advance('if')
        # '('
        self.eat_write_advance('(')
        #
        # expression
        #
        # ')'
        self.eat_write_advance(')')
        # '{'
        self.eat_write_advance('{')

        # statements
        self.compileStatements()

        # '}'
        self.eat_write_advance('}')

        # optional else      
        if self._getTokenLexical() == 'else':
            self.eat_write_advance('else')
            self.eat_write_advance('{')

            # statements
            self.compileStatements()

            self.eat_write_advance('}')

        self.printCompileGeneral('</ifStatement>')

    # compile a while statement
    def compileWhile(self):

        self.printCompileGeneral('<whileStatement>')

        # 'while'
        self.eat_write_advance('while')

        # '('
        self.eat_write_advance('(')

        #
        # expression
        #

        # ')'
        self.eat_write_advance(')')


        # '{'
        self.eat_write_advance('{')


        # statements
        self.compileStatements()

        # '}'
        self.eat_write_advance('}')

        self.printCompileGeneral('</whileStatement>')


    # compile a do statement
    def compileDo(self):
        self.printCompileGeneral('<doStatement>')

        # 'do'
        self.eat_write_advance('do')

        #
        # subroutine call
        #

        self.printCompileGeneral('</doStatement>')

    # compile a return statement
    def compileReturn(self):
        self.printCompileGeneral('<returnStatement>')

        self.eat_write_advance('return')

        #
        # optional expression
        #
        
        # ';'
        self.eat_write_advance(';')

        self.printCompileGeneral('</returnStatement>')

    # compile an expression
    def compileExpression(self):
        
        # PLACEHOLDER
        self._advance()
        self.printCompiledTokenFull()
        #

        # op
        if self._getTokenLexical() in ['+', '-', '*', '/', '&amp', '|', '&lt', '&gt', '=' ]:

            pass

    # compile a term
    # if current token is identifier,
    # must resolve into var, array, or subroutine call
    # with single look ahead
    def compileTerm(self):
        self.printCompileGeneral('<term>')
        
        # integer
        if self._getTokenLexicalType() == 'integerConstant':
            self.printCompiledTokenFull()
            self._advance()

        # string
        elif self._getTokenLexicalType() == 'stringConstant':
            self.printCompiledTokenFull()
            self._advance()

        # keyword constant
        elif self._getTokenLexical() in ['true', 'false', 'null', 'this']:
            self.printCompileGeneral('<keywordConstant>{kw}</keywordConstant>'.format(kw = self._getTokenLexical()))
            self._advance()

        # varName | varName[expression] | subroutineCall 
        elif self._getTokenLexicalType() == 'idenfifer':
            
            # varName[expression]
            if self._getLookAheadLexical() == '[':
                # varName
                self.printCompiledTokenFull()
                self._advance()
                # '['
                self.eat_write_advance('[')
                # expression
                self.compileExpression()
                # ']'
                self.eat_write_advance(']')

            # subrountineCall
            # subroutineName (expressionList)
            elif self._getLookAheadLexical() == '(':
                # subroutineName
                self.printCompiledTokenFull()
                self._advance()
                # '('
                self.eat_write_advance('(')
                # expressionList
                self.compileExpressionList()
                # ')'
                self.eat_write_advance(')')

            # subrountineCall
            # className | varName . subroutineName (expressionList)
            elif self._getLookAheadLexical() == '.':
                # class | varName
                self.printCompiledTokenFull()
                self._advance()
                # '.'
                self.eat_write_advance('.')
                #subroutineName
                assert self._getTokenLexicalType == 'identifier'
                self.printCompiledTokenFull()
                self._advance()
                # '('
                self.eat_write_advance('(')
                # expressionList
                self.compileExpressionList()
                # ')'
                self.eat_write_advance(')')

            # varName
            else:
                self.printCompiledTokenFull()
                self._advance()


        # ( expression )
        elif self._getTokenLexical() == '(':
            self.eat_write_advance('(')
            self.compileExpression()
            self.eat_write_advance(')')
        
        # unaryOp
        elif self._getTokenLexical() in ['-', '~'] and (self.tokenizedInputList[self.currentTokenIndex - 1]).split(" ")[1] == '=':
            
            self.printCompileGeneral('<unaryOp>{unaryOp}</unaryOp>'.format(unaryOp = self._getTokenLexical()))

            self._advance()

        self.printCompileGeneral('<\term>')
    


    # compile a possibly empty comma separated list
    # of expressions. Return the number of 
    # expressions in the list
    def compileExpressionList(self):
        pass
        self.printCompileGeneral('<statements>')

        # while there are next statements
        while self._getTokenLexical() in ['let', 'if', 'while', 'do' ,'return']:
            if self._getTokenLexical() == 'let':
                self.compileLet()


            self._advance()


            
    def run(self):
        #n_token = len(self.tokenizedInputList)
        #for i in range(n_token):
        self.compileWhile()

if __name__ == "__main__":

    cpe = CompilationEngine('./Out.xml')
    print(cpe.tokenizedInputList)
    cpe.run()
    for line in cpe.result:
        print(line)
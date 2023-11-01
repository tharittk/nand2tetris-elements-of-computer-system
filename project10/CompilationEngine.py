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
        stringToken = self._getLookAheadLexical()
        if stringIn != stringToken:
            raise ValueError
        else:
            self._advance()

    def _advance(self):
        self.currentTokenIndex += 1
        self.currentToken = self.tokenizedInputList[self.currentTokenIndex]

    def eat_write(self, stringIn):
        self._eat(stringIn)
        self.printCompiledTokenFull()

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
        self.eat_write('class')
        self._advance()

        # className
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        # '{'
        self.eat_write('{')
        self._advance()

        # optional class var dec
        if self._getTokenLexical() in  ['static', 'field']:
            self.compileClassVarDec()

        # optional subroutine dec
        if self._getTokenLexical() in ['constructor', 'function', 'method']:
            self.compileSubroutine()

        # '}'
        self.eat_write('}')
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
        self.eat_write(';')

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
        self.eat_write('(')
        self._advance()

        # parameterList
        self.compileParameterList()

        # ')'
        self.eat_write(')')
        self._advance()


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
        
        self.eat_write('{')
        self._advance()

        # optional varDec
        if self._getTokenLexical() == 'var':
            self.compileVarDec()
            self._advance()



        # statements
        self.compileStatements()

        # '}'
        self.eat_write('}')

        self.printCompileGeneral('</subRoutineBody>')

    # compile a var declaration
    def compileVarDec(self):
        self.printCompileGeneral('<varDec>')

        # 'var'
        self.eat_write('var')
        self._advance()

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
        self.eat_write(';')
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
        self.eat_write('let')
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        #
        # optional expression in case of array
        #
        if self._getLookAheadLexical() == '[':
            # '['
            self.eat_write('[')
            self._advance()
            # expression
            self.compileExpression()
            # ']'
            self.eat_write(']')

        # '='
        self.eat_write('=')
        self._advance()

        # compile expression
        self.compileExpression()

        # ';'
        self.eat_write(';')

        self.printCompileGeneral('</letStatement>')

    # compile an if with possibly else clause
    def compileIf(self):
        self.printCompileGeneral('<ifStatement>')

        # 'if'
        self.eat_write('if')
        # '('
        self.eat_write('(')
        self._advance()
        

        # expression
        self.compileExpression()

        # ')'
        self.eat_write(')')
        # '{'
        self.eat_write('{')
        self._advance()

        # statements
        self.compileStatements()

        # '}'
        self.eat_write('}')
        self._advance()

        # optional else      
        if self._getTokenLexical() == 'else':
            self.eat_write('else')
            self.eat_write('{')
            self._advance()

            # statements
            self.compileStatements()

            self.eat_write('}')
            self._advance()

        self.printCompileGeneral('</ifStatement>')

    # compile a while statement
    def compileWhile(self):

        self.printCompileGeneral('<whileStatement>')

        # 'while'
        self.eat_write('while')

        # '('
        self.eat_write('(')
        self._advance()

        
        # expression
        self.compileExpression()

        # ')'
        self.eat_write(')')


        # '{'
        self.eat_write('{')
        self._advance()


        # statements
        self.compileStatements()

        # '}'
        self.eat_write('}')

        self.printCompileGeneral('</whileStatement>')


    # compile a do statement
    def compileDo(self):
        self.printCompileGeneral('<doStatement>')

        # 'do'
        self.eat_write('do')
        self._advance()

        # subroutine call
        self.compileTerm()

        self.printCompileGeneral('</doStatement>')

    # compile a return statement
    def compileReturn(self):
        self.printCompileGeneral('<returnStatement>')

        self.eat_write('return')

        if self._getLookAheadLexical() != ';':
            self._advance()
            self.compileExpression()
        
        # ';'
        self.eat_write(';')

        self.printCompileGeneral('</returnStatement>')

    # compile an expression
    def compileExpression(self):
        self.printCompileGeneral('<expression>')
        self.compileTerm()

        self._advance()
        # (op term)
        if self._getTokenLexical() in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=' ]:
            # op
            self.printCompiledTokenFull()
            self._advance()
            # term
            self.compileTerm()

        self.printCompileGeneral('<\expression>')

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
            self.printCompileGeneral('<keyword>{kw}</keyword>'.format(kw = self._getTokenLexical()))
            self._advance()

        # varName | varName[expression] | subroutineCall 
        elif self._getTokenLexicalType() == 'idenfifer':
            
            # varName[expression]
            if self._getLookAheadLexical() == '[':
                # varName
                self.printCompiledTokenFull()
                # '['
                self.eat_write('[')
                self._advance()

                # expression
                self.compileExpression()
                # ']'
                self.eat_write(']')

            # subrountineCall
            # subroutineName (expressionList)
            elif self._getLookAheadLexical() == '(':
                # subroutineName
                self.printCompiledTokenFull()
                # '('
                self.eat_write('(')
                self._advance()

                # expressionList
                self.compileExpressionList()
                # ')'
                self.eat_write(')')

            # subrountineCall
            # className | varName . subroutineName (expressionList)
            elif self._getLookAheadLexical() == '.':
                # class | varName
                self.printCompiledTokenFull()
                # '.'
                self.eat_write('.')
                self._advance()
                #subroutineName
                assert self._getTokenLexicalType == 'identifier'
                self.printCompiledTokenFull()
                # '('
                self.eat_write('(')
                # expressionList
                self.compileExpressionList()
                # ')'
                self.eat_write(')')


            # varName
            else:
                self.printCompiledTokenFull()


        # ( expression )
        elif self._getTokenLexical() == '(':
            self.eat_write('(')
            self.compileExpression()
            self.eat_write(')')
        
        # unaryOp
        elif self._getTokenLexical() in ['-', '~'] and (self.tokenizedInputList[self.currentTokenIndex - 1]).split(" ")[1] == '=':
            self.printCompileGeneral('<unaryOp>{unaryOp}</unaryOp>'.format(unaryOp = self._getTokenLexical()))


        self.printCompileGeneral('<\term>')
    

    # compile a possibly empty comma separated list
    # of expressions. Return the number of 
    # expressions in the list
    def compileExpressionList(self):
        self.printCompileGeneral('<expressionList>')
        count = 0
        
        # empty
        if self._getLookAheadLexical() != ')':
            self._advance()
            self.compileExpression()
            self._advance()

            # optional expression
            while self._getTokenLexical() == ',':
                # ','
                self.printCompiledTokenFull()
                self._advance()

                # expression
                self.compileExpression()
                self._advance()

        self.printCompileGeneral('<\expressionList>')

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
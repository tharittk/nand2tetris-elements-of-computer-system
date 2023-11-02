# CompilationEngine

class CompilationEngine():
    def __init__(self, xmlFile):
        self.tokenizedInputList = xmlFile[1:-1] #exclude[<token>]
        #self.tokenizedInputList = self._read_tokenized_xml(xmlFile)[1:-1]
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
            print("expected: ", stringIn, "got: ", stringToken)
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
        #print("Passed:::", stringPrint)

    def printCompiledTokenFull(self):

        line = self._getCurrentTokenFull()
        self.result.append(line)
        #print("Passed:::", line)

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

        # optional class var dec
        while self._getLookAheadLexical() in  ['static', 'field']:
            self._advance()
            self.compileClassVarDec()

        # optional subroutine dec
        while self._getLookAheadLexical() in ['constructor', 'function', 'method']:
            self._advance()
            self.compileSubroutine()

        # '}'
        self.eat_write('}')
        print("CLOSING CLASS")

        self.printCompileGeneral('</class>')


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
        #self._advance()
        
        # optional next variable
        while self._getLookAheadLexical() == ',':
            # ','
            self._advance()
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()


        # ';'
        self.eat_write(';')

        self.printCompileGeneral('</classVarDec>')

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

        # '('
        self.eat_write('(')
        
        # parameterList
        self.compileParameterList()

        # ')'
        self.eat_write(')')

        # subroutine body
        self.compileSubroutineBody()

        self.printCompileGeneral('</subroutineDec>')


    # compile a (possibly empty) parameter list
    def compileParameterList(self):

        self.printCompileGeneral('<parameterList>')

        if (self._getLookAheadLexical() in ['int', 'char', 'boolean']) or (self._getTokenLexicalType() == 'identifier'):
            # type
            self._advance()
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()

            # optional next
            while self._getLookAheadLexical() == ',':
                # ','
                self._advance()
                self.printCompiledTokenFull()
                self._advance()

                # type
                assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
                self.printCompiledTokenFull()
                self._advance()

                # varName
                assert self._getTokenLexicalType() == 'identifier'
                self.printCompiledTokenFull()

        self.printCompileGeneral('</parameterList>')

    # compile a subroutine's body
    def compileSubroutineBody(self):
        self.printCompileGeneral('<subRoutineBody>')
        
        self.eat_write('{')

        # optional varDec
        while self._getLookAheadLexical() == 'var':
            self.compileVarDec()

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

        # optional variable but same type
        while self._getLookAheadLexical() == ',':
            # ','
            self._advance()
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()

        # ';'
        self.eat_write(';')
        self.printCompileGeneral('</varDec>')

    # compile a sequences of statements
    def compileStatements(self):
        self.printCompileGeneral('<statements>')

        # while there are next statements
        while self._getLookAheadLexical() in ['let', 'if', 'while', 'do' ,'return']:
            if self._getLookAheadLexical() == 'let':
                self.compileLet()
            elif self._getLookAheadLexical() == 'if':
                self.compileIf()
            elif self._getLookAheadLexical() == 'while':
                self.compileWhile()
            elif self._getLookAheadLexical() == 'do':
                self.compileDo()
            elif self._getLookAheadLexical() == 'return':
                self.compileReturn()

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

        # optional expression in case of array
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
        #print("finishing let ;")
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
        #self._advance()

        # statements
        self.compileStatements()

        # '}'
        self.eat_write('}')

        # optional else      
        if self._getLookAheadLexical() == 'else':
            self.eat_write('else')
            self.eat_write('{')
            # statements
            self.compileStatements()
            self.eat_write('}')

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

        self.eat_write(';')

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
        #print('>>> in expression')
        self.printCompileGeneral('<expression>')

        
        self.compileTerm()

        # (op term)
        if self._getLookAheadLexical() in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=' ]:
            # op
            self._advance()
            self.printCompiledTokenFull()
            # term
            #if self._getLookAheadLexical() == '(':
            #    print("THIS")
            #    self.compileTerm()

            #else:     
            self._advance()
            self.compileTerm()



        self.printCompileGeneral('</expression>')
        #print('<<< out expression')

    # compile a term
    # if current token is identifier,
    # must resolve into var, array, or subroutine call
    # with single look ahead

    def compileTerm(self):
        #print('>>> in term')
        self.printCompileGeneral('<term>')

        # integer
        if self._getTokenLexicalType() == 'integerConstant':
            self.printCompiledTokenFull()
            #self._advance()

        # string
        elif self._getTokenLexicalType() == 'stringConstant':
            self.printCompiledTokenFull()

        # keyword constant
        elif self._getTokenLexical() in ['true', 'false', 'null', 'this']:
            self.printCompileGeneral('<keyword>{kw}</keyword>'.format(kw = self._getTokenLexical()))


        # varName | varName[expression] | subroutineCall 
        elif self._getTokenLexicalType() == 'identifier':
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
                #self._advance()

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
                assert self._getTokenLexicalType() == 'identifier'
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


        
        # unaryOp
        #elif self._getTokenLexical() in ['-', '~'] and (self.tokenizedInputList[self.currentTokenIndex - 1]).split(" ")[1] == '=':
        elif self._getTokenLexical() in ['-', '~'] :

            self.printCompiledTokenFull()

            if self._getLookAheadLexical() == '(':
                #print('sub exp case')
                self.eat_write('(')
                self._advance()
                self.compileExpression()
                self.eat_write(')')
            else:
                self._advance()        
                self.compileTerm()


        # ( expression )
        #if self._getLookAheadLexical() == '(':
            #print('sub exp case')
            #self.eat_write('(')
            #self.compileExpression()
            #print("HERE in 1")
            #self.eat_write(')')

        if self._getTokenLexical() == '(':
            self.printCompiledTokenFull()
            self._advance()
            self.compileExpression()
            self.eat_write(')')


        self.printCompileGeneral('</term>')
        #print('<<< out term')


    # compile a possibly empty comma separated list
    # of expressions. Return the number of 
    # expressions in the list
    def compileExpressionList(self):
        #print('>>> in expressionList')
        self.printCompileGeneral('<expressionList>')
        count = 0
        
        # empty
        if self._getLookAheadLexical() != ')':
            self._advance()
            self.compileExpression()

            # optional expression
            while self._getLookAheadLexical() == ',':
                # ','
                self._advance()
                self.printCompiledTokenFull()

                self._advance()
                # expression
                self.compileExpression()


        self.printCompileGeneral('</expressionList>')

    def run(self):
        self.compileClass()

if __name__ == "__main__":

    cpe = CompilationEngine('./Out.xml')
    #print(cpe.tokenizedInputList)
    cpe.run()
    #for line in cpe.result:
    #s    print(line)



# CompilationEngine
from SymbolTable import *
from VMWriter import *

class CompilationEngine():
    def __init__(self, xmlFile):
        self.tokenizedInputList = xmlFile[1:-1] #exclude[<token>]
        #self.tokenizedInputList = self._read_tokenized_xml(xmlFile)[1:-1]
        self.currentToken = ''
        self.currentTokenIndex = -1 # not yet look at any token
        self.result = []
        
        # VM compilation
        self.className = ''
        self.classSymbolTable = SymbolTable()
        self.subRoutineSymbolTable = SymbolTable()
        self.VMWriter = VMWriter('./test.vm')

    # during testing
    def _read_tokenized_xml(self, xml_file):
        xmlLines = []
        with open(xml_file) as f:
            for line in f:
                xmlLines.append(line.strip('\n'))
        return xmlLines
    
    def outputting(self, outXMLFile):
        with open(outXMLFile, 'w') as f:
            for line in self.result:
                f.write(line + '\n')

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

    def _getVarTypeFromTables(self, varName):
        if varName in self.subRoutineSymbolTable.keys():
            return self.subRoutineSymbolTable.typeOf(varName)
        elif varName in self.classSymbolTable.keys():
            return self.classSymbolTable.typeOf(varName)
        else:
            return None # the name is subroutine name or class name
    
    def _getVarKindFromTables(self, varName):
        if varName in self.subRoutineSymbolTable.keys():
            return self.subRoutineSymbolTable.kindOf(varName)
        elif varName in self.classSymbolTable.keys():
            return self.classSymbolTable.kindOf(varName)
        else:
            return None # the name is subroutine name or class name
  
    def _getVarIndexFromTables(self, varName):
        if varName in self.subRoutineSymbolTable.keys():
            return self.subRoutineSymbolTable.indexOf(varName)
        elif varName in self.classSymbolTable.keys():
            return self.classSymbolTable.indexOf(varName)
        else:
            return None # the name is subroutine name or class name          



    # compile a complete class
    def compileClass(self):

        self.printCompileGeneral('<class>')
        # 'class'
        self.eat_write('class')
        self._advance()

        # className
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        self.className = self._getTokenLexical()

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

        self.printCompileGeneral('</class>')

    # (X) compile a static variable or a field decoration
    def compileClassVarDec(self):

        # Symbol table entry



        self.printCompileGeneral('<classVarDec>')
        # (static | field)
        assert self._getTokenLexical() in ['static', 'field']
        self.printCompiledTokenFull()
        varKind = self._getTokenLexical()

        self._advance()

        # type
        assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        varType = self._getTokenLexical()
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        varName = self._getTokenLexical()
        
        # add to symboltable
        self.classSymbolTable.define(varName, varType, varKind)



        # optional next variable
        while self._getLookAheadLexical() == ',':
            # ','
            self._advance()
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()

            # same kind and type but change name
            varName = self._getTokenLexical()
            self.classSymbolTable.define(varName, varType, varKind)


        # ';'
        self.eat_write(';')
        self.printCompileGeneral('</classVarDec>')

    # compile a complete method, function, or constructor
    def compileSubroutine(self):

        funcType = ''
        funcReturnType = ''
        funcName = ''

        self.printCompileGeneral('<subroutineDec>')


        # (constructor | function | method)
        assert self._getTokenLexical() in ['constructor', 'function', 'method']
        self.printCompiledTokenFull()
    
        funcType = self._getTokenLexical()

        self._advance()

    

        # reset table
        self.subRoutineSymbolTable.reset()



        # ('void' | type)
        assert (self._getTokenLexical() in ['void','int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier' 
        self.printCompiledTokenFull()
        
        funcReturnType = self._getTokenLexical()
        
        self._advance()

        # subRoutineName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        funcName = self.className + self._getTokenLexical()

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
        self.printCompileGeneral('<subroutineBody>')
        
        self.eat_write('{')

        # optional varDec
        while self._getLookAheadLexical() == 'var':
            self.compileVarDec()

        # statements
        self.compileStatements()

        # '}'
        self.eat_write('}')

        self.printCompileGeneral('</subroutineBody>')

    # (X) compile a var declaration
    def compileVarDec(self):
        self.printCompileGeneral('<varDec>')

        # Symbol table entry

        varKind = 'local'

        # 'var'
        self.eat_write('var')
        self._advance()

        # type
        assert (self._getTokenLexical() in ['int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        
        varType = self._getTokenLexical()
    
        
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        varName = self._getTokenLexical()

        # add to symboltable
        self.subRoutineSymbolTable.define(varName, varType, varKind)

        # optional variable but same type
        while self._getLookAheadLexical() == ',':
            # ','
            self._advance()
            self.printCompiledTokenFull()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()
            varName = self._getTokenLexical()
            self.subRoutineSymbolTable.define(varName, varType, varKind)

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
        
    # (X) compile a let statement
    def compileLet(self):
        varName = ''
        self.printCompileGeneral('<letStatement>')
        # 'let'
        self.eat_write('let')
        self._advance()

        # varName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()
        
        
        varName = self._getTokenLexical()
        varType = self._getVarTypeFromTables(varName)
        varIndex = self._getVarIndexFromTables(varName)
        varKind = self._getVarKindFromTables(varName)

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

        # write pop
        self.VMWriter.writePop(varKind, varIndex)

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

        self.printCompileGeneral('<expression>')
        
        self.compileTerm()

        # (op term)
        if self._getLookAheadLexical() in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=' ]:
            # op
            self._advance()
            self.printCompiledTokenFull()
            self._advance()
            self.compileTerm()

        self.printCompileGeneral('</expression>')

    # compile a term
    # if current token is identifier,
    # must resolve into var, array, or subroutine call
    # with single look ahead

    def compileTerm(self):
        previous = (self.tokenizedInputList[self.currentTokenIndex - 1]).split(" ")[1]
        if previous != 'do':
            self.printCompileGeneral('<term>')

        # integer
        if self._getTokenLexicalType() == 'integerConstant':
            self.printCompiledTokenFull()
            # push constant INT
            self.VMWriter.writePush('constant', self._getTokenLexical())
            

        # string
        elif self._getTokenLexicalType() == 'stringConstant':
            self.printCompiledTokenFull()
            #self.VMWriter.writeCall('String.new()', )

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
        elif self._getTokenLexical() in ['-', '~'] :

            self.printCompiledTokenFull()

            if self._getLookAheadLexical() == '(':
                self._advance()
                self.compileTerm()
                
            else:
                self._advance()        
                self.compileTerm()

        # ( expression )

        if self._getTokenLexical() == '(':
            self.printCompiledTokenFull()
            self._advance()
            self.compileExpression()
            self.eat_write(')')


        if previous != 'do':
            self.printCompileGeneral('</term>')

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
            count += 1

            # optional expression
            while self._getLookAheadLexical() == ',':
                # ','
                self._advance()
                self.printCompiledTokenFull()

                self._advance()
                # expression
                self.compileExpression()
                count += 1


        self.printCompileGeneral('</expressionList>')
        return count

    def run(self):
        self.compileClass()

if __name__ == "__main__":

    cpe = CompilationEngine('./Out.xml')
    #print(cpe.tokenizedInputList)
    cpe.run()
    #for line in cpe.result:
    #s    print(line)



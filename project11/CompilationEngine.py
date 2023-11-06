# CompilationEngine
from SymbolTable import *
from VMWriter import *

class CompilationEngine():
    def __init__(self, xmlFile, outputFileName):
        self.tokenizedInputList = xmlFile[1:-1] #exclude[<token>]
        #self.tokenizedInputList = self._read_tokenized_xml(xmlFile)[1:-1]
        self.currentToken = ''
        self.currentTokenIndex = -1 # not yet look at any token
        self.result = []
        
        # VM compilation
        self.className = ''
        self.classSymbolTable = SymbolTable()
        self.subRoutineSymbolTable = SymbolTable()
        self.VMWriter = VMWriter(outputFileName)

        self.currentSubroutineName = ''
        self.currentSubroutineType = ''

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
        if self._getTokenLexicalType() == 'stringConstant':
            return self.currentToken.split(">")[1].split("<")[0][1:-1]#conventional leading white space
        else:
            return  self.currentToken.split(" ")[1]
    
    def _getLookAheadLexical(self):
        tokenAhead = self.tokenizedInputList[self.currentTokenIndex + 1]
        stringToken = tokenAhead.split(" ")[1]
        return stringToken

    def _getLookAheadLexicalType(self):
        tokenAhead = self.tokenizedInputList[self.currentTokenIndex + 1]
        return  tokenAhead.split(">")[0].split("<")[1]

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
        if varName in self.subRoutineSymbolTable.table.keys():
            return self.subRoutineSymbolTable.typeOf(varName)
        elif varName in self.classSymbolTable.table.keys():
            return self.classSymbolTable.typeOf(varName)
        else:
            return None # the name is subroutine name or class name
    
    def _getVarKindFromTables(self, varName):
        if varName in self.subRoutineSymbolTable.table.keys():
            return self.subRoutineSymbolTable.kindOf(varName)
        elif varName in self.classSymbolTable.table.keys():
            return self.classSymbolTable.kindOf(varName)
        else:
            return None # the name is subroutine name or class name
  
    def _getVarIndexFromTables(self, varName):
        if varName in self.subRoutineSymbolTable.table.keys():
            return self.subRoutineSymbolTable.indexOf(varName)
        elif varName in self.classSymbolTable.table.keys():
            return self.classSymbolTable.indexOf(varName)
        else:
            return None # the name is subroutine name or class name          



    # (X) compile a complete class
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

    # (X) compile a complete method, function, or constructor
    def compileSubroutine(self):


        self.printCompileGeneral('<subroutineDec>')
        # reset table    
        self.subRoutineSymbolTable.reset()
        self.currentSubroutineName = ''
        self.currentSubroutineType = ''

        # (constructor | function | method)
        assert self._getTokenLexical() in ['constructor', 'function', 'method']
        self.printCompiledTokenFull()

        self.currentSubroutineType = self._getTokenLexical()

        self._advance()

        # ('void' | type)
        assert (self._getTokenLexical() in ['void','int', 'char', 'boolean']) or self._getTokenLexicalType() == 'identifier' 
        self.printCompiledTokenFull()
        
        #funcReturnType = self._getTokenLexical()
        
        self._advance()

        # subRoutineName
        assert self._getTokenLexicalType() == 'identifier'
        self.printCompiledTokenFull()

        self.currentSubroutineName = self.className + '.' + self._getTokenLexical()


        if self.currentSubroutineType == 'constructor':
            pass
        elif self.currentSubroutineType == 'method':
            # add self i.e. this
            self.subRoutineSymbolTable.define('this', self.className ,'argument')
        
        elif self.currentSubroutineType == 'function':
            pass

        #print('compiling', self.currentSubroutineName)

        # '('
        self.eat_write('(')
        
        # parameterList - nArgs
        self.compileParameterList()

        # ')'
        self.eat_write(')')

        # subroutine body - nVars

        self.compileSubroutineBody()

        self.printCompileGeneral('</subroutineDec>')


    # (X) compile a (possibly empty) parameter list
    def compileParameterList(self):

        self.printCompileGeneral('<parameterList>')
        #print('>', self._getLookAheadLexical() )
        if (self._getLookAheadLexical() in ['int', 'char', 'boolean']) or (self._getTokenLexicalType() == 'identifier') or (self._getLookAheadLexicalType() == 'identifier'):
            varKind = 'argument'
            # type
            self._advance()
            self.printCompiledTokenFull()
            varType = self._getTokenLexical()
            self._advance()

            # varName
            assert self._getTokenLexicalType() == 'identifier'
            self.printCompiledTokenFull()
            varName = self._getTokenLexical()

            self.subRoutineSymbolTable.define(varName, varType, varKind)
            #print(varName, self.subRoutineSymbolTable.table[varName])
            # optional next
            while self._getLookAheadLexical() == ',':
                # ','
                self._advance()
                self.printCompiledTokenFull()
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
                self.subRoutineSymbolTable.define(varName, varType, varKind)
                #print(varName, self.subRoutineSymbolTable.table[varName])

        self.printCompileGeneral('</parameterList>')

    # (X) compile a subroutine's body
    def compileSubroutineBody(self):
        self.printCompileGeneral('<subroutineBody>')
        
        self.eat_write('{')
        # optional varDec
        while self._getLookAheadLexical() == 'var':
            self.compileVarDec()
        
    

        nVars = self.subRoutineSymbolTable.varCount('local')
        nArgs = self.subRoutineSymbolTable.varCount('argument')

        #print('nVars, ', nVars, 'nArgs', nArgs)

        if self.currentSubroutineType == 'method':
            self.VMWriter.writeFunction(self.currentSubroutineName, nVars)
            self.VMWriter.writePush('argument', 0)
            self.VMWriter.writePop('pointer', 0)
        elif self.currentSubroutineType == 'constructor':
            nFields = self.classSymbolTable.varCount('field')
            self.VMWriter.writeFunction(self.currentSubroutineName, nVars)
            self.VMWriter.writePush('constant', nFields)
            self.VMWriter.writeCall('Memory.alloc', 1)
            self.VMWriter.writePop('pointer', 0)
        elif self.currentSubroutineType == 'function':
            self.VMWriter.writeFunction(self.currentSubroutineName, nVars)

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
        #print('adding var: ', varName)
        #print(varName, self.subRoutineSymbolTable.table[varName])
        #print('Next is', self._getLookAheadLexical())
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
            
            #print(varName, self.subRoutineSymbolTable.table[varName])

        # ';'
        self.eat_write(';')
        self.printCompileGeneral('</varDec>')

    # (X) compile a sequences of statements
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

        isArrAssign = False

        # optional expression in case of array
        if self._getLookAheadLexical() == '[':
            # push arr
            self.VMWriter.writePush(varKind, varIndex )
            # '['
            self.eat_write('[')
            self._advance()
            # expression
            self.compileExpression()
            # ']'
            self.eat_write(']')

            self.VMWriter.writeArithmatic('add')
            isArrAssign = True

        # '='
        self.eat_write('=')
        self._advance()

        # compile expression
        self.compileExpression()

        if isArrAssign:
            self.VMWriter.writePop('temp', 0)
            self.VMWriter.writePop('pointer', 1)
            self.VMWriter.writePush('temp', 0)
            self.VMWriter.writePop('that', 0)
        else:
            # write pop after expression
            self.VMWriter.writePop(varKind, varIndex)

        # ';'
        #print("finishing let ;")
        self.eat_write(';')

        self.printCompileGeneral('</letStatement>')

    # (X) compile an if with possibly else clause
    def compileIf(self):
        self.printCompileGeneral('<ifStatement>')
        uniqNum = self.currentTokenIndex

        # 'if'
        self.eat_write('if')
        # '('
        self.eat_write('(')
        self._advance()
        # expression
        self.compileExpression()
        # ')'
        self.eat_write(')')

        # write VM
        self.VMWriter.writeArithmatic('not')
        self.VMWriter.writeIf('ELSE.{uniq}'.format(uniq=uniqNum))

        # '{'
        self.eat_write('{')

        # statements
        self.compileStatements()

        self.VMWriter.writeGoto('CONT.{uniq}'.format(uniq=uniqNum))
 
        # '}'
        self.eat_write('}')

        # optional else

        self.VMWriter.writeLabel('ELSE.{uniq}'.format(uniq=uniqNum))# will be empty if no else, just con't

        if self._getLookAheadLexical() == 'else':
            self.eat_write('else')
            self.eat_write('{')
            # statements
            self.compileStatements()
            self.eat_write('}')
        

        # CONT label here
        self.VMWriter.writeLabel('CONT.{uniq}'.format(uniq=uniqNum))

        self.printCompileGeneral('</ifStatement>')

    # (X) compile a while statement
    def compileWhile(self):
        uniqNum = self.currentTokenIndex
        self.printCompileGeneral('<whileStatement>')
        self.VMWriter.writeLabel('INWHILE.{uniq}'.format(uniq=uniqNum))

        # 'while'
        self.eat_write('while')

        # '('
        self.eat_write('(')
        self._advance()

        # expression
        self.compileExpression()

        # ')'
        self.eat_write(')')
        self.VMWriter.writeArithmatic('not')
        self.VMWriter.writeIf('OUTWHILE.{uniq}'.format(uniq=uniqNum))

        # '{'
        self.eat_write('{')

        # statements
        self.compileStatements()
        self.VMWriter.writeGoto('INWHILE.{uniq}'.format(uniq=uniqNum))


        # '}'
        self.eat_write('}')
        self.VMWriter.writeLabel('OUTWHILE.{uniq}'.format(uniq=uniqNum))

        self.printCompileGeneral('</whileStatement>')

    # (X) compile a do statement
    def compileDo(self):
        self.printCompileGeneral('<doStatement>')

        # 'do'
        self.eat_write('do')
        self._advance()

        # subroutine call
        self.compileTerm()

        self.eat_write(';')

        # needDummy case
        self.VMWriter.writePop('temp', 0)

        self.printCompileGeneral('</doStatement>')

    # (X) compile a return statement
    def compileReturn(self):
        self.printCompileGeneral('<returnStatement>')
        self.eat_write('return')
        needDummy = True

        if self._getLookAheadLexical() != ';':
            self._advance()
            self.compileExpression()
            needDummy = False

        if needDummy:
            self.VMWriter.writePush('constant', 0)
            self.VMWriter.writeReturn()
        else:
            self.VMWriter.writeReturn()
        # ';'
        self.eat_write(';')
        self.printCompileGeneral('</returnStatement>')

    # (X) compile an expression
    def compileExpression(self):

        self.printCompileGeneral('<expression>')
        
        self.compileTerm()

        # (op term)
        if self._getLookAheadLexical() in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=' ]:
            # op
            op = self._getLookAheadLexical()
            self._advance()
            self.printCompiledTokenFull()
            self._advance()
            self.compileTerm()
            #print('in ops', op)
            if op == '+':
                self.VMWriter.writeArithmatic('add')
            elif op == '-':
                self.VMWriter.writeArithmatic('sub')
            elif op == '*':
                self.VMWriter.writeCall('Math.multiply', 2)
            elif op == '/':
                self.VMWriter.writeCall('Math.divide', 2)
            elif op == '&amp;':
                self.VMWriter.writeArithmatic('and')
            elif op == '|':
                self.VMWriter.writeArithmatic('or')
            elif op == '&lt;':
                self.VMWriter.writeArithmatic('lt')
            elif op == '&gt;':
                self.VMWriter.writeArithmatic('gt')
            elif op == '=':
                self.VMWriter.writeArithmatic('eq')

        self.printCompileGeneral('</expression>')

    # compile a term
    # if current token is identifier,
    # must resolve into var, array, or subroutine call
    # with single look ahead

    def compileTerm(self):
        previous = (self.tokenizedInputList[self.currentTokenIndex - 1]).split(" ")[1]
        if previous != 'do':
            self.printCompileGeneral('<term>')

        # (X) integer
        if self._getTokenLexicalType() == 'integerConstant':
            self.printCompiledTokenFull()
            # push constant INT
            self.VMWriter.writePush('constant', int(self._getTokenLexical()))
            

        # (X) string
        elif self._getTokenLexicalType() == 'stringConstant':
            self.printCompiledTokenFull()
            stringIn = self._getTokenLexical()
            length = len(stringIn)
            #print(stringIn)
            self.VMWriter.writePush('constant', length)
            self.VMWriter.writeCall('String.new', 1 )

            for i in range(length):
                self.VMWriter.writePush('constant', ord(stringIn[i]))
                self.VMWriter.writeCall('String.appendChar', 2)


        # (X) keyword constant
        elif self._getTokenLexical() in ['true', 'false', 'null', 'this']:
            self.printCompileGeneral('<keyword>{kw}</keyword>'.format(kw = self._getTokenLexical()))
            cnst = self._getTokenLexical()

            if cnst == 'true':
                self.VMWriter.writePush('constant', 1)
                self.VMWriter.writeArithmatic('neg')

            elif cnst == 'false':
                self.VMWriter.writePush('constant', 0)

            elif cnst == 'null':
                self.VMWriter.writePush('constant', 0)

            elif cnst == 'this':
                self.VMWriter.writePush('pointer', 0)

        # varName | varName[expression] | subroutineCall 
        elif self._getTokenLexicalType() == 'identifier':
            # varName[expression]
            if self._getLookAheadLexical() == '[':
                # varName
                self.printCompiledTokenFull()
                varName = self._getTokenLexical()
                varKind = self._getVarKindFromTables(varName)
                varIndex = self._getVarIndexFromTables(varName)
                self.VMWriter.writePush(varKind, varIndex )

                # '['
                self.eat_write('[')
                self._advance()
                # expression
                self.compileExpression()
                # ']'
                self.eat_write(']')

                # get address that = arr + i
                self.VMWriter.writeArithmatic('add')
                self.VMWriter.writePop('pointer', 1)
                # get value at that address i.e. arr[i]
                self.VMWriter.writePush('that', 0)

            # (X) subrountineCall
            # subroutineName (expressionList)
            elif self._getLookAheadLexical() == '(':
                # subroutineName
                self.printCompiledTokenFull()
                funcName = self._getTokenLexical()
                # '('
                self.eat_write('(')

                # expressionList
                nArgs = self.compileExpressionList()

                self.VMWriter.writePush('pointer', 0)
                self.VMWriter.writeCall(self.className + '.'+funcName, nArgs + 1)

                # ')'
                self.eat_write(')')

            # (X) subrountineCall
            # className | varName . subroutineName (expressionList)
            elif self._getLookAheadLexical() == '.':

                # class | varName
                self.printCompiledTokenFull()
                # need to be className
                classNameVarName = self._getTokenLexical()


                varName = self._getTokenLexical()
                varKind = self._getVarKindFromTables(varName)
                varIndex = self._getVarIndexFromTables(varName)
                
                className = self._getVarTypeFromTables(varName)
                # push obj
                #print(varName)


                
                if varKind != None:
                    self.VMWriter.writePush(varKind, varIndex )

                # '.'
                self.eat_write('.')
                self._advance()


                #subroutineName
                assert self._getTokenLexicalType() == 'identifier'
                self.printCompiledTokenFull()
                subroutineName = self._getTokenLexical()

                # '('
                self.eat_write('(')
                # expressionList
                

                # push other expression
                nArgs = self.compileExpressionList()

                # ')'
                self.eat_write(')')

                if varKind == None: # OS
                    self.VMWriter.writeCall(classNameVarName+'.'+subroutineName, nArgs)
                else:
                    self.VMWriter.writeCall(className+'.'+subroutineName, nArgs+1)

            # (X) varName
            else:
                varName = self._getTokenLexical()
                varKind = self._getVarKindFromTables(varName)
                varIndex = self._getVarIndexFromTables(varName)
                #print(varName)
                self.VMWriter.writePush(varKind, varIndex )

                self.printCompiledTokenFull()


        
        # (X) unaryOp
        elif self._getTokenLexical() in ['-', '~'] :

            self.printCompiledTokenFull()
            op = self._getTokenLexical()

            if self._getLookAheadLexical() == '(':
                self._advance()
                self.compileTerm()
                
            else:
                self._advance()        
                self.compileTerm()

            if op == '-':
                self.VMWriter.writeArithmatic('neg')
            elif op == '~':
                self.VMWriter.writeArithmatic('not')

        # (X) ( expression )

        if self._getTokenLexical() == '(':
            self.printCompiledTokenFull()
            self._advance()
            self.compileExpression()
            self.eat_write(')')


        if previous != 'do':
            self.printCompileGeneral('</term>')

    # (X) compile a possibly empty comma separated list
    # of expressions. Return the number of 
    # expressions in the list
    def compileExpressionList(self):
        self.printCompileGeneral('<expressionList>')
        count = 0

        
        # not empty
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



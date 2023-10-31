# CompilationEngine

class CompilationEngine():
    def __init__(self):
        self.inputFile = ''

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
        pass

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
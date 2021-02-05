#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from syntax import *


# I *Curt Wilson* have written all of this project myself, without any
# unauthorized assistance, and have followed the academic honor code.


def lex(s):
    # TODO: scan input string and return a list of its tokens

    tokens = []
    reg = r'^(\n|\r|\t|\ |\/\/[\s\S]*\n|\/\*[\s\S]*\/)*([a-zA-Z][a-zA-Z_0-9]*|[0-9]*\.?[0-9]+|\+|\-|\/|\*|\^|\,|\:|\=|\<|\{|\}|\(|\)|\;)'
    match = re.match(reg, s) #([a-zA-Z][a-zA-Z_0-9]*\w|[0-9]*\.?[0-9]+|\+|\-|\/|\*|\^|\,|\:|\=|\<|\{|\}|\(|\)|\;|\n|\r)
    
    # for x in match:
    #     if 
    # match1 = re.match(r'^(\/\/[a-zA-Z_0-9]*)')
    # if match1 == "/":
        
    while match != None:
        tokens.append(match.group(2))
        s = s[len(match.group(0)):]
        match = re.match(reg, s)
        # print(re.group1)
    
    print(tokens)
    return tokens

# print(lex("this, that, and the other"))
# print(lex("proc three() { 1+2 }; \r print three()"))

def parse(s):
    # TODO: parse and return an AST node or ErrorMsg object

    ####### CHECKLIST ########

    # parseP() = DONE
    # parseS() = DONE
    # parseP() = DONE
    # parseP() = DONE
    # parseP() = DONE
    # parseP() = DONE
    # parseP() = DONE

    tokens = s

    def peek(n):
        nonlocal tokens
        if n < len(tokens):
            return tokens[n]
        else:
            return ""
    def expect(tok):
        nonlocal tokens
        if peek(0) == tok:
            tokens = tokens[1:]
        else:
            print("Error, expected token '"+str(tok)+"', got: "+str(tokens))
            exit(1)

    def isx(s):
        return re.match(r"^([a-zA-Z][0-9_a-zA-Z]*)", s) != None 

    # def isv(Var): # is a variable
    #     return re.match(reg, s) # != None
    
    # def isf(function): # is a function
    #     return re.match(reg, s) # != None
    
    
    ########## Added methods to modify ##########

    def parseP():
        s0 = parseS()
        while peek(0) == ";":
            expect(";")
            s1 = parseS()
            s0 = SeqStmt(lhs = s0, rhs = s1)
        return s0

    def parseS():
        l = ""
        p = ""
        if peek(0) == "proc": 
            expect("proc")
            if not isx(peek(0)): 
                errM = peek(0)
                expect(errM)
                errM = ErrorMsg(errM)
                return errM
            f = peek(0)
            expect(f)
            f = Var(f)
            expect("(")
            l = parseL()
            expect(")")
            expect("{")
            p = parseP()
            expect("}")
            return ProcStmt(f, params = l, body = p)
        elif peek(0) == "if":
            expect("if")
            c = parseC()
            if peek(0) == "{":
                expect("{")
                p1 = parseP()
            if peek(0) == "}":
                expect("}")
            if peek(0) == "else":
                expect("else")
            if peek(0) == "{":
                expect("{")
                p2 = parseP()
            if peek(0) == "}":
                expect("}")
            return IfStmt(guard = c, thenbody = p1, elsebody = p2)
        elif peek(0) == "while":
            expect("while")
            c = parseC()
            if peek(0) == "{":
                expect("{")
                p = parseP()
            if peek(0) == "}":
                expect("}")
            return WhileStmt(guard = c, body = p)
        elif peek(0) == "print":
            expect("print")
            c = parseC()
            return PrintStmt(rhs = c)
        else:
            c = parseC()
            return c

    def parseL():  # in progress

        if peek(0) == ")": return []
        xst = [Var(peek(0))]
        expect(peek(0))

        while peek(0) == ",":
            expect(",")
            xst.append(Var(peek(0)))
            expect(peek(0))
        return xst


        # if peek(0) == ",":
        #     expect(",")
        #     return "x" + "," + parseX()
        # elif peek(0) == "x":
        #     expect("x")
        #     return "x"
        # elif peek(0) == "":
        #     expect("")
        #     return epsilon

    def parseC():
        e0 = parseE()
        if peek(0) == "<":
            expect("<")
            e1 = parseE()
            return LessThan(lhs = e0, rhs = e1)
        elif peek(0) == "=":
            expect("=")
            e2 = parseE()
            return Equal(lhs = e0, rhs = e2)
        else:
            return e0  
       
    def parseE():  # Only have parseE() and parseT() that contain (parseM() and parseN())
        t0 = parseT()
        while peek(0) == "+" or peek(0) == "-":
            if peek(0) == "+":
                expect("+")
                t1 = parseT()
                t0 = Plus(lhs = t0, rhs = t1)

            elif peek(0) == "-":
                expect("-")
                t1 = parseT()
                t0 = Minus(lhs = t0, rhs = t1)

        return t0


    def parseT():  # IP
        fst0 = parseF()
        while peek(0) == "*" or peek(0) == "/":
            if peek(0) == "*":
                expect("*")
                fst1 = parseF()
                fst0 = Mult(lhs = fst0, rhs = fst1)
            elif peek(0) == "/":
                expect("/")
                fst1 = parseF()
                fst0 = Div(lhs = fst0, rhs = fst1)
        return fst0
   
    def parseF():
        a = parseA()
        if peek(0) == "^":
            expect("^")
            f = parseF()
            return Expo(lhs = a, rhs = f)
        else:
            return a

    def parseA():   # FIXED # Look at this function

        if isx (peek(0)):
            x = peek(0)
            expect(x)
            x = Var(x)
            if peek(0) == "(":
                expect("(")
                r = parseR()
                expect(")")
                return Call(x, r)
            elif peek(0) == ":":
                expect(":")
                expect("=")
                c1 = parseC()
                return Assign(lhs = x, rhs = c1)
            else:
                return x
        elif peek(0) == "(":
            expect("(")
            c = parseC()
            expect(")")
            return c
        else:
            number = peek(0)
            expect(number)
            number = Lit(number)
            return number

    def parseR(): # IP, Refer to parseL()

        if peek(0) == ")": return []

        elif peek(0) != ")":
            cst = [parseC()]
            return cst
            while peek(0) == ",":
                expect(",")
                cst.append(parseC())
            return cst

        # c = parseC()
        # if peek(0) == ",":
        #     expect(",")
        #     q = parseQ()
        #     return c + "," + q
        # elif peek(0) == "":
        #     expect("")
        #     return epsilon
        # else:
        #     return c

    # string = parseP()
    # print(string)
    return parseP()

    ###############################################

# print(parse("proc three() { 1+2 }; \r print three()"))
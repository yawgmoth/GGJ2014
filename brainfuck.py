import sys
import os

def get_content(fname):
    if not os.path.exists(fname):
        return ""
    f = open(fname, "r")
    result = ""
    for line in f:
        result += line.strip()
    f.close()
    return result

class ConsoleIO:
    def read(self):
        return ord(raw_input()[0])
    def write(self, c):
        print chr(c),

class CallIO:
    def __init__(self, args):
        self.args = args
        self.output = []
    def read(self):
        if not self.args: return 0
        a = self.args[0]
        del self.args[0]
        return a
    def write(self, c):
        self.output.append(c)
        
        
class FunArgIO:
    def __init__(self, outer):
        self.outer = outer
        self.output = []
    def read(self):
        return self.outer.read()
    def write(self, c):
        self.output.append(c)
        
MODULE_DIR = "modules"

def call_bf(program, args, loc={}, glob={}):
    c = CallIO(args)
    def s(*args):
        if ord("(") in args:
            name = "".join(map(chr, args[:args.index(ord("("))]))
            params = args[args.index(ord("("))+1:-1]
        else:
            name = "".join(map(chr, args))
            params = []
        fname = os.path.join(MODULE_DIR, name + ".bf")
        res = -1
        if os.path.exists(fname):
            res = call_bf(get_content(fname), params, loc, glob)
            if res:
                res = res[0]
            else:
                res = 0
            
        return res
    loc["s"] = s
    interpret(program, c, loc, glob, tape=[0], rtape=[0])
    return c.output

def interpret(program, io, loc={}, glob={}, tape=[0], rtape=[0], position=0):
    curprog = 0
    while curprog < len(program):
        c = program[curprog]
        if c == '>':
            position += 1
            if len(tape) <= position:
                tape.append(0)
        elif c == '<':
            position -= 1
            if position < 0 and len(rtape) <= abs(position):
                rtape.append(0)
        elif c == '+':
            if position > 0:
                tape[position] += 1
            else:
                rtape[-position] += 1
        elif c == '-':
            if position > 0:
                tape[position] -= 1
            else:
                rtape[-position] -= 1
        elif c == '.':
            if position > 0:
                io.write(tape[position])
            else:
                io.write(rtape[-position])
        elif c == ',':
            if position > 0:
                tape[position] = io.read()
            else:
                rtape[position] = io.read()
        elif c == '[':
            if position > 0:
                curval = tape[position]
            else:
                curval = rtape[-position]
            if curval == 0:
                level = 0
                while curprog < len(program) and (program[curprog] != "]" or level != 1):
                    if program[curprog] == "[":
                        level += 1
                    elif program[curprog] == "]":
                        level -= 1
                    curprog += 1
        elif c == ']':
            if position > 0:
                curval = tape[position]
            else:
                curval = rtape[-position]
            if curval != 0:
                level = 0
                i = curprog - 1
                found = False
                while i >= 0 and not found:
                    if program[i] == '[' and level == 0:
                        found = True
                    elif program[i] == '[':
                        level -= 1
                    elif program[i] == ']':
                        level += 1
                    i -= 1
                if found:
                    curprog = i
                else:
                    raise Exception('Syntax error, bracket mismatch')
        elif c == ":":
            j = curprog + 1
            openat = curprog + 1
            level = 0
            while j < len(program) and (program[j] != ")" or level != 1):
                if program[j] == "(" and level == 0:
                    openat = j
                if program[j] == "(":
                    level += 1
                elif program[j] == ")":
                    level -= 1
                j += 1
            if j == len(program):
                raise Exception("Syntax error, malformed call to python (no closing paren)")
            if program[openat] != "(":
                raise "Syntax error, malformed call to python (no open paren)"
            name = program[curprog+1:openat]
            args = program[openat+1:j]
            fio = FunArgIO(io)
            position = interpret(args, fio, loc, glob, tape, rtape, position)
            params = fio.output
            res = 0
            if name in loc:
                res = loc[name](*params)
            elif name in glob:
                res = glob[name](*params)
            if res:
                if position > 0:
                    tape[position] = res
                else:
                    rtape[-position] = res
            curprog = j
        elif c == "#":
            print "prog at", curprog, "tape at", position, "value",
            if position > 0:
                print tape[position]
            else:
                print rtape[-position]
            print tape[:20]
        curprog += 1
    return position

def main(args):
    program = args[0]
    if args[0] == '-f':
        fname = args[1]
        f = open(fname, 'r')
        program = ""
        for line in f:
            program += line.strip()
        f.close()
    interpret(program, ConsoleIO())

if __name__ == '__main__':
    #main(sys.argv[1:])
    def g(x):
        return 2*x
    def f(x=None):
        return 7
    print "1:", map(chr, call_bf(':s(+++++ +++++ [> +++++ +++++<-]>+++++ [>+>+>+<<<-]>. >+++++. >------.) .', [1], locals(), globals()))
    print "2:", call_bf(',:g(.).', [1], locals(), globals())
    print "3:", call_bf(',[+].,++++.>>>>>>>>>>>++>+>+>+++<[>[-<+++>]<<]>.', [0, 1], locals(), globals())
    print "4:", call_bf('+++++ +++++ [>+++++++<-]>++. +++++++++++++++++++++++++++++. +++++++. . +++.', [], locals(), globals())

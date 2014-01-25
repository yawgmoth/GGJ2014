import sys

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
    
def call_bf(program, args):
    c = CallIO(args)
    interpret(program, c)
    return c.output


def interpret(program, io):
    tape = [0]
    rtape = [0]
    position = 0
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
                rtape[position] += 1
        elif c == '-':
            if position > 0:
                tape[position] -= 1
            else:
                rtape[position] -= 1
        elif c == '.':
            if position > 0:
                io.write(tape[position])
            else:
                io.write(rtape[position])
        elif c == ',':
            if position > 0:
                tape[position] = io.read()
            else:
                rtape[position] = io.read()
        elif c == ']':
            if position > 0:
                curval = tape[position]
            else:
                curval = rtape[position]
            if curval != 0:
                level = 0
                i = curprog - 1
                found = False
                while i > 0 and not found:
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
                    raise 'Syntax error, bracket mismatch'
        
        curprog += 1

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
    print call_bf(',>,+++.<--.', [1,2])
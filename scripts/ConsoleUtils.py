def absMove(y,x):
    print("\033[%s;%sH" % (str(y),str(x)))

def flint(string):
    print(string,end="")
        
def clear():
    flint("\033[2J")
    absmove(0,0)
    
def relX(x):
    if x>0:
        flint("\003[%sC" % str(x))
    else:
        flint("\033[%sD" % str(-x))

def relY(y):
    if y-2>0:
        flint("\033[%sB" % str(y))
    else:
        flint("\033[%sA" % str(-y))
        
def relMove(y,x):
    relY(y)
    relX(x)

def clearLine():
    flint("\033[K")

def reprint(string):
    clearLine()
    print(string)

def reflint(string):
    clearLine()
    flint(string)

def saveCurs():
    flint("\033[s")

def loadCurs():
    flint("\033[u")
    
    


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

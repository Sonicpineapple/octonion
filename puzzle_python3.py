import sys
sys.path.append('scripts')
import numpy as np
import random
import marshal
from CayleyDickson import *
from state import *
import ConsoleUtils as cu
from colorama import Fore, Back, Style, init
from random import randint

init()

use_quaternions, use_base_octonions = False, False
#use_quaternions = True
#use_base_octonions = True


def get_generators():
  bases = []
  for index in range(8):
    base = np.zeros(8)
    base[index] = 1
    bases.append(base)

  identity = bases[0]

  h = np.array([0, 1, 1, 1, 1, 0, 0, 0]) / 2.0
  if use_quaternions:
    h = np.array([1, 1, 1, 1, 0, 0, 0, 0]) / 2.0 # to generate Hurwitz quaternions
  if use_base_octonions:
    h = bases[4]

  return [bases[1], bases[2], h, bases[0]]


def load_states():
  state_file_name = 'data/states_240.txt'
  if use_quaternions:
    state_file_name = 'data/states_24.txt'
  if use_base_octonions:
    state_file_name = 'data/states_16.txt'

  with open(state_file_name, 'rb') as f:
    states = marshal.load(f)
    return [State(s, True) for s in states]

def illust(state):
  res = "("
  for x in state.value:
    if x>0:
      res+=Fore.GREEN+"#"+Style.RESET_ALL+" "
    elif x == 0:
      res+="# "
    else:
      res+=Fore.RED+"#"+Style.RESET_ALL+" "
  res = res.strip()+")"
  if any(el%2==1 for el in state.double):
    res+="/2"
  return res


def main():
  i, j, h, winning_state = [State(c) for c in get_generators()]
  states = load_states()
  states_set = set(states)

  movelist = [i,j,h,i*h,j*h,i.inv(),j.inv(),h.inv(),(i*h).inv(),(j*h).inv()]
  moves = ["i","j","h","i*h","j*h","i.inv()","j.inv()","h.inv()","(i*h).inv()","(j*h).inv()"]
  solution = ""

  def ida(state,d,previ=-1):
    nonlocal movelist
    nonlocal winning_state
    nonlocal solution
    nonlocal moves
    if state == winning_state:
      return True
    elif d>0:
      for i in range(10):
        if (previ<0 or i!=(previ+5)%10) and ida(state*movelist[i],d-1,i):
          solution = moves[i] + " "+solution
          return True
    return False

  def generate():
    nonlocal movelist
    nonlocal moves
    gens = []
    gens.append(State([1,0,0,0,0,0,0,0]))
    gensols = [0]
    d = 0
    while True:
      d+=1
      if d>6:
        break
      extra = []
      for x in gens:
        for m in movelist:
          temp = x*m
          if temp not in gens and temp not in extra:
            extra.append(temp)
            gensols.append(d)
      if len(extra) == 0:
        break
      for i in extra:
        gens.append(i)
    f = open("Generated.txt","a")
    for i in range(len(gens)):
      f.write(str(gens[i]) + " - " + str(gensols[i]) + "\n")
    f.close()
    print(str(len(gens))+"\n\n")
    
    

  print("Loaded " + repr(len(states)) + " states")

  current_state = states[random.randrange(len(states))]

  print("Random initial state: " + str(current_state) + " or " + illust(current_state))
  help_string = \
    """
      Enter an input expression to right-multiply to the current state.
      With the convention in https://en.wikipedia.org/wiki/Octonion#Definition
      and the abbreviations:
      i = """ + str(i) + """ or """ + illust(i) + """
      j = """ + str(j) + """ or """ + illust(j) + """
      h = """ + str(h) + """ or """ + illust(h) + """
      Use i, j, or h as generators and use ( ) and octonion multiplication *
      to construct complex expressions.
      Moves can be repeated by raising to a power, as in (expression)**n.
      The inverse of an expression is given by (expression).inv().
      The previous move can be repeated with r.
      Examples: h * (i * j)
                h**2 * (j * h).inv()
      The objective is to reach """ + str(winning_state) + """ or """+illust(winning_state) + """
      Enter q to stop.
    """

  colours = [Fore.RED,Fore.GREEN,Fore.BLUE,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW]
  winning_message = (
  colours[randint(0,len(colours))] + """
     __      __                         __       __  __            __ 
    /  \    /  |                       /  |  _  /  |/  |          /  |
    $$  \  /$$/______   __    __       $$ | / \ $$ |$$/  _______  $$ |
     $$  \/$$//      \ /  |  /  |      $$ |/$  \$$ |/  |/       \ $$ |
      $$  $$//$$$$$$  |$$ |  $$ |      $$ /$$$  $$ |$$ |$$$$$$$  |$$ |
       $$$$/ $$ |  $$ |$$ |  $$ |      $$ $$/$$ $$ |$$ |$$ |  $$ |$$/ 
        $$ | $$ \__$$ |$$ \__$$ |      $$$$/  $$$$ |$$ |$$ |  $$ | __ 
        $$ | $$    $$/ $$    $$/       $$$/    $$$ |$$ |$$ |  $$ |/  |
        $$/   $$$$$$/   $$$$$$/        $$/      $$/ $$/ $$/   $$/ $$/ 
  """ + Style.RESET_ALL)


  print(help_string)
  
  print("Current state: " + illust(current_state))

  #generate()
  
  #if ida(State([0,1,0,0,0,0,0,0]),4):
  #  print(solution)
  solved = False

  
  while True:
    cu.clearLine()
    input_string = input("Input = ")
    if input_string in ['q', 'exit']:
      break

    if input_string == "set":
      temp = current_state
      current_state = State(eval(input("Enter new state: ")))
      if current_state not in states_set:
        current_state = temp
        cu.relMove(-1,0)
        print("Invalid state")
      cu.relMove(-3,0)
      cu.reprint("Current state: " + illust(current_state))
    elif input_string in ["ida","solve"]:
      cu.clearLine()
      for d in range(0,7):
        if ida(current_state,d):
          print(solution+"\n\n")
          solved = True
          break
      if solved:
        break
      cu.relMove(-1,0)
    else:
      try:
        input_value = eval(input_string)
        r = input_value
        if input_value not in states_set:
          #print("Input value " + str(input_value) + " is not a valid state")
          raise

        cu.reprint("Input = " + input_string + " = " + str(input_value) + " or " + illust(input_value))
        current_state = current_state * input_value
        #print("(New state) = (Old state) * (Input) = " + str(current_state))
        cu.relMove(-3,0)
        cu.reprint("Current state: " + illust(current_state))
        if current_state == winning_state:
          cu.reprint(winning_message)
          break

      except Exception:
        cu.reprint("Invalid input")
        #print(help_string)
        cu.relMove(-3,0)
        cu.reprint("Current state: " + illust(current_state))

  

if __name__ == '__main__':
  main()

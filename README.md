# octonion

This repo contains a puzzle about integral octonions, and some scripts to explore octonions.

## How to run the integral octonions puzzle?
- Install Python, 2.* or 3.*
- Install numpy
- Run puzzle_python2.py or puzzle_python3.py depending on the Python version you installed
- Follow the instructions to solve it. You may want to refer to the explanations below.

## About [octonions](https://en.wikipedia.org/wiki/Octonion#Definition):
- Octonions are a number system extended from complex numbers and quaternions. 
- Each octonion can be thought of as a vector of 8 real numbers, or a sum of 8 basis vectors.
- Addition, subtraction, multiplication, and inverse can be defined similar to complex numbers, with a more complicated multiplication table.
- Octonion multiplication is not commutative (a * b != b * a) and not associative ((a * b) * c != a * (b * c)) in general.
## About [integral octonions](https://en.wikipedia.org/wiki/Octonion#Integral_octonions):
- They are octonions whose coordinates are all integers or all half-integers satisfying certain properties.
- The minimum nonzero norm of integral octonions is 1. There are 240 integral octonions with norm = 1.
- The identity octonion, (1, 0, 0, 0, 0, 0, 0, 0), is an integral octonion with norm = 1.
- If we start from three generators
  - i = (0, 1, 0, 0, 0, 0, 0, 0)
  - j = (0, 0, 1, 0, 0, 0, 0, 0)
  - h = (0, 1, 1, 1, 1, 0, 0, 0)/2
    
  and use the octonion multiplication *, we can generate all 240 integral octonions with unit norm.
## About this integral octonions puzzle:
- We start from a random unit norm integral octonion, called a "state".
- In each step
  - You input an expression of i, j, h, and the octonion multiplication *, with parenthesis (). For example, h * (i * j).
  - The input expression is evaluated. By construction, it is also a unit norm integral octonion.
  - (The new state) = (the old state) * (input)
- You win when the state is the identity octonion (1, 0, 0, 0, 0, 0, 0, 0).
- Significance of non-associativity:
  - Since the multiplication is not associative: state * (a * b) != (state * a) * b, applying (a * b) as input is different from applying a and then applying b.
  - If you only input i or j or h by themselves and do not use multiplication in the input expression, it is unlikely you will be able to solve the puzzle.
  - At least try (i * h) at some point!
  

import sys
from tokenizer import tokenize

# A pseudocode of the algorithm is as follows:
# 1.  While there are tokens to be read:
# 2.        Read a token
# 3.        If it's a number add it to queue
# 4.        If it's an operator
# 5.               While there's an operator on the top of the stack with greater precedence:
# 6.                       Pop operators from the stack onto the output queue
# 7.               Push the current operator onto the stack
# 8.        If it's a left bracket push it onto the stack
# 9.        If it's a right bracket 
# 10.            While there's not a left bracket at the top of the stack:
# 11.                     Pop operators from the stack onto the output queue.
# 12.             Pop the left bracket from the stack and discard it
# 13. While there are operators on the stack, pop them to the queue

BINARY_OPERATORS = ['^', '*', '/', '+', '-']
UNARY_OPERATORS = ['_', 'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'arcsin', 'arccos', 'arctan', 'arccsc', 'arcsec', 'arccot']
LEFT_PARENTHESIS = '('
RIGHT_PARENTHESIS = ')'
PEEK = 0

def eval(x, y, operator):
  x = float(x)
  y = float(y)
  if operator == "+":
    return x + y
  elif operator == "-" or operator == "_":
    return x - y
  elif operator == "/":
    return x / y
  elif operator == "*":
    return x * y
  elif operator == "^":
    return x ** y
  else:
    return 0

def shunt(eq):
  operatorStack = []
  outputQueue = []

  tokens = tokenize(eq)
  while tokens:
    token = tokens.pop(PEEK)
    # Determine if token is an operator
    if token in BINARY_OPERATORS:
      index = BINARY_OPERATORS.index(token)
      while len(operatorStack) > PEEK:
        operator = operatorStack[PEEK]
        # the least index then the higher precendence
        try:
          i = BINARY_OPERATORS.index(operator)
          if i < index:
            outputQueue.append(operatorStack.pop(PEEK))
          else:
            break
        except ValueError as e:
          break
      operatorStack.insert(PEEK, token)
    elif token == LEFT_PARENTHESIS:
      operatorStack.insert(PEEK, token)
    elif token == RIGHT_PARENTHESIS:
      while len(operatorStack) > PEEK:
        top = operatorStack.pop(PEEK)
        if top is not LEFT_PARENTHESIS:
          outputQueue.append(top)
        else:
          break
    else: # token is a constant or number
      outputQueue.append(token)
  # While there are operators on the stack, pop them to the queue
  while len(operatorStack) > 0:
    outputQueue.append(operatorStack.pop(PEEK))
  return outputQueue

def rpn(postfix): # evaluate reverse polish notation
  outputStack = []
  while postfix:
    token = postfix.pop(PEEK)
    if token in BINARY_OPERATORS:
      try:
        y = outputStack.pop()
        x = outputStack.pop()
        outputStack.append(eval(x, y, token))
      except IndexError as e:
        raise e
    elif token in UNARY_OPERATORS:
      pass
    else:
      outputStack.append(token)
  return outputStack[0]
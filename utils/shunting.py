import sys
from tokenizer import tokenize
from math import sin, cos, tan, degrees
import decimal

from kivy.logger import Logger

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

decimal.getcontext().prec = 6

def eval(x, y, operator):
  x = decimal.Decimal(x)
  y = decimal.Decimal(y)
  # print x, operator, y
  try:
    return {
    'sin': sin(degrees(x)),
    'cos': cos(degrees(x)),
    'tan': cos(degrees(x)),
    '+': x + y,
    '_': x - y,
    '-': x - y,
    '/': x / y,
    '*': x * y,
    '^': (x + 0) ** y
    }[operator]
  except ZeroDivisionError as e:
    print e
    return 0
  except ValueError as e:
    print e
    if operator == '+':
      return eval(y, x, operator)
    elif operator == '-' and x < 0.0 and y < 0.0:
      return eval(x * -1, y * -1, operator) * -1
    elif operator == '-' and x < 0.0:
      return eval(x * -1, y, '+') * -1
    else:
      return 0
  except Exception as e:
    print 'err type is:', e.__class__.__name__, x, operator, y
    if e.__class__.__name__ == 'InvalidOperation':
      if operator == '-' and x < 0.0:
        return eval(x * -1, y, '+') * -1
      elif operator == '-' and x < 0.0 and y < 0.0:
        return eval(x * -1, y * -1, operator) * -1
      elif operator == '+' and x < 0.0 and y < 0.0:
        return eval(x * -1, y * -1, operator) * -1
      elif operator == '+' and x < 0.0:
        return eval(y, x, operator)
      elif x == 0 and y == 0:
        return 0
      else:
        raise e       

  # except Exception as e:
  #   print 'type is:', e.__class__.__name__  
  #   print e

def toPostfix(infix):
  stack = []
  postfix = ''

  for c in infix:
    if isOperand(c):
      postfix += c
    else:
      if isLeftParenthesis(c):
        stack.append(c)
      elif isRightParenthesis(c):
        operator = stack.pop()
        while not isLeftParenthesis(operator):
          postfix += operator
          operator = stack.pop()              
      else:
        while (not isEmpty(stack)) and hasLessOrEqualPriority(c, stack[len(stack)-1]):
          postfix += stack.pop()
        stack.append(c)

  while (not isEmpty(stack)):
    postfix += stack.pop()
  return postfix


def isOperand(c):
  return c in BINARY_OPERATORS

def isLeftParenthesis(c):
  return c == LEFT_PARENTHESIS
def isRightParenthesis(c):
  return c == RIGHT_PARENTHESIS

def hasLessOrEqualPriority(c, peek):
  return BINARY_OPERATORS.index(c) <= BINARY_OPERATORS.index(peek)

def isEmpty(stack):
  return len(stack) == 0

def shunt(eq):

  # return toPostfix(eq)

  operatorStack = []
  outputQueue = []

  tokens = tokenize(eq)
  # print 'token', tokens
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
          if i <= index:
            
            while operatorStack:
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
    # print 'outputQueue', outputQueue
    # print 'operatorStack', operatorStack

  # While there are operators on the stack, pop them to the queue
  while len(operatorStack) > 0:
    outputQueue.append(operatorStack.pop(PEEK))
  return outputQueue

def rpn(postfix): # evaluate reverse polish notation
  outputStack = []
  # print postfix
  while postfix:
    token = postfix.pop(PEEK)
    if token in BINARY_OPERATORS:
      try:
        y = outputStack.pop()
        x = outputStack.pop()
        outputStack.append(eval(x, y, token))
        # print 'output', outputStack
      except IndexError as e:
        # print e, x, y, token
        pass
    elif token in UNARY_OPERATORS:
      print "unary", token
      pass
    else:
      outputStack.append(token)
    # print 'op', postfix
    # print 'output', outputStack
  return (outputStack[0])

if __name__ == '__main__':
  file = sys.argv[1]
  for line in open(file, 'r'):
    print line, '=> ',''.join(shunt(line)) 

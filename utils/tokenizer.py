import sys

MAX_TRIGO_LEN = 6
MIN_TRIGO_LEN = 3

arithop = ['^', '*', '/', '+', '-', '(', ')']
trigoop = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']

def tokenize(eq):
  output = []

  s = [c for c in str(eq).strip()]
  terms = []
  while s:
    # check for trig functions
    op = ''.join(s[0:MIN_TRIGO_LEN])
    nextop = ''.join(s[MIN_TRIGO_LEN:MAX_TRIGO_LEN])
    if op == 'arc' and nextop in trigoop:
      output.append(''.join(s[0:MAX_TRIGO_LEN]))
      del s[0:MAX_TRIGO_LEN]
      continue
    elif op in trigoop:
      output.append(op)
      del s[0:MIN_TRIGO_LEN]
      continue

    c = s.pop(0)
    if c in arithop:
      # special case where we need to determine if 
      # `-` was used as unary operator, 
      # then we change the symbol to `_`
      if c == '-' or c == '_':
        if output:
          tail = output[len(output)-1]
          if terms:
            tail = terms[len(terms)-1]
          if tail != ')' and tail in arithop:
            output.append('_')
            continue
        else:
          output.append('_')
          continue

      # if we have pending num in buffer, 
      # put it first into output queue, 
      # twas in for 3x, 40x, 5xy
      while terms:
        term = terms.pop(0)
        output.append(term)
        if terms:
          output.append('*')
      output.append(c)
    else:
      try:
        _ = int(c)
        num, s = leadnum(s)
        terms.append(str(c) + str(num))
      except Exception as e:
        terms.append(c)

  while terms:
    term = terms.pop(0)
    output.append(term)
    if terms:
      output.append('*')

  return output

def leadnum (s):
  num = []
  i = 0
  while i < len(s):
    try:
      n = int(s[i])
      i = i + 1
      num.append(str(n))
    except Exception as e:
      break
  if num:
    del s[0: i]
  return ''.join(num), s

def test(file):
  eqs = open(file, 'r')
  for eq in eqs:
    print eq.strip() , '=> ', tokenizer(eq)
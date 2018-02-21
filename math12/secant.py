from utils.shunting import shunt
from utils.shunting import rpn

roots = []
postfix = None

DECIMAL_PLACES = 6

# TODO: optimization
# we can store the computed value of f(x) in a dict
# so for the next iteration we dont need to solve it again

def secant(x1, x2, f, i): # here goes secant!
  fx1 = _round(f(x1))
  fx2 = _round(f(x2))

  x3 = _round(x2 - ((fx2 * (x2 - x1)) / (fx2 - fx1)))
  print i, ":", x3, _round(f(x3))

  while x3 not in roots:
    roots.append(x3)
    return secant(x2, x3, f, i+1)
  return x3

def calc(seeds, fx):
  return secant(float(seeds[0]), float(seeds[1]), fx, 2)

def _round(i):
  return round(i, DECIMAL_PLACES)
from utils.shunting import shunt
from utils.shunting import rpn

roots = []
postfix = None

DECIMAL_PLACES = 6

Fx = []

# TODO: optimization
# we can store the computed value of f(x) in a dict
# so for the next iteration we dont need to solve it again

def secant(x1, x2, f, i): # here goes secant!
  fx1 = f(x1)
  fx2 = f(x2)

  print "x1:", x1, "fx1:",fx1, "x2:", x2,'fx2:', fx2
  x3 = x2 - ((fx2 * (x2 - x1)) / (fx2 - fx1))
  Fx.append(f(x3))

  print i, ':', x3, f(x3)

  while not roots or _round(x3, 4) != _round(roots[-1], 4):
    roots.append(x3)
    return secant(x2, x3, f, i+1)
  return x3
  
def calc(seeds, fx):
  return secant(float(seeds[0]), float(seeds[1]), fx, 2), (roots, Fx)

def _round(i, x = DECIMAL_PLACES):
  return float('{:f}'.format(round(i, x)))
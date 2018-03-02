from utils.shunting import shunt
from utils.shunting import rpn

import decimal

roots = []
postfix = None

DECIMAL_PLACES = 4

Fx = []

decimal.getcontext().prec = 6

# TODO: optimization
# we can store the computed value of f(x) in a dict
# so for the next iteration we dont need to solve it again

def secant(x1, x2, f, i): # here goes secant!
  fx1 = f(x1)
  fx2 = f(x2)
  try:
    # print "x1:", x1, "fx1:",fx1, "x2:", x2,'fx2:', fx2
    x3 = x2 - ((fx2 * (x2 - x1)) / (fx2 - fx1))
    Fx.append(f(x3))

    # print i, ':', x3, f(x3)
    while not roots or _round(x3, 4) != _round(roots[-1], 4):
      roots.append(x3)
      return secant(_round(x2), _round(x3), f, i+1)
    return x3
  except Exception as e:
    print e

  
def calc(seeds, fx):
  return secant(seeds[0], seeds[1], fx, 2), (roots, Fx)

def _round(i, x = DECIMAL_PLACES):
  # return float('{:f}'.format(i))
  return decimal.Decimal(i)
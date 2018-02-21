import sys

import math12.secant as secant
import math12.newton as newton
import math12.bisection as bisection

from utils.bracketing import bracket
from utils.shunting import shunt
from utils.shunting import rpn

class Fx:
  postfix = None

  def __init__(self, postfix):
    self.postfix = postfix

  def eval(self, x):
    return rpn([x if term == 'x' else term for term in self.postfix])

# how?
# do: python rootfinder /path/to/dataset.csv secant
dataset = sys.argv[1]
algo = sys.argv[2]

def run(algo, seeds, fx):
  return {
    'secant': secant,
    'bisection': bisection,
    'newton': newton
  }[algo].calc(seeds, fx)

if algo is not None:
  lines = open(dataset, 'r')
  for line in lines:
    upper, lower, eq = line.split(',')

    # set initial seeds for the iteration
    seeds = bracket(upper, lower)

    fx = Fx(shunt(eq)).eval
    root = run(algo, seeds, fx)
    
    print line, ' => ', round(root, 4)

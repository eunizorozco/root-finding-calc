import sys

import math12.secant as secant
import math12.newton as newton
import math12.bisection as bisection

from utils.bracketing import bracket
from utils.shunting import shunt
from utils.shunting import rpn

import kivy
from kivy.logger import Logger

class Fx:
  postfix = None

  def __init__(self, postfix):
    self.postfix = postfix

  def eval(self, x):
    return rpn([x if term == 'x' else term for term in self.postfix])

def run(algo, seeds, fx):
  return {
    'secant': secant,
    'bisection': bisection,
    'newton': newton
  }[algo].calc(seeds, fx)


def solve(algo, eq, upper, lower):
  # set initial seeds for the iteration
  fx = Fx(shunt(eq)).eval
  seeds = bracket(int(upper), int(lower), fx)
  Logger.debug([eq, seeds])
  # print line, ' => ', round(root, 4)
  return run(algo, seeds, fx)

# how?
# do: python rootfinder /path/to/dataset.csv secant
  
if __name__ == '__main__':
  dataset = sys.argv[1]
  algo = sys.argv[2]

  if algo is not None:
    lines = open(dataset, 'r')
    for line in lines:
      upper, lower, eq = line.split(',')
      
      root, soln = solve(algo, eq, upper, lower)
      print eq.strip(), "=>", round(root, 4)

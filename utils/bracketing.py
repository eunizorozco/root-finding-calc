# brute force method, 
# try all values from a to b 
# until we found bracket which changes sign

import kivy
from kivy.logger import Logger

def bracket(a, b, fx):
  y = []
  for i in range(min(a, b), max(a, b)):
    ans = fx(i)
    if y:
      if ans > 0 and y[-1] < 0:
        return [i-1, i]
      elif ans < 0 and y[-1] > 0:
        return [i, i-1]
    y.append(ans)
  return [min(a, b), max(a, b)]
# brute force method, 
# try all values from a to b 
# until we found bracket which changes sign

def bracket(a, b, fx):
  y = []
  for i in range(a, b):
    ans = fx(i)
    if y:
      if ans > 0 and y[-1] < 0:
        return [i-1, i]
      elif ans < 0 and y[-1] > 0:
        return [i, i-1]
    y.append(ans)
  return [a, b]
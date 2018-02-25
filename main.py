# ---------- main.py  ---------- 

import kivy
# kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from utils.datatable import DataTable
from kivy.logger import Logger
from rootfinder import solve
import random

screen_manager = ScreenManager()

class CalculatorLayout(GridLayout):

  def enter(self, text):
    if self.input is None:
      self.input = text
    else:
      self.input += text
    self.display.text += text

  def clear(self):
    self.display.text = "f(x) = "
    self.input = None
    self.eq = None
    self.lower = None
    self.upper = None

  def calculate(self):
    if self.input:
      try:
        # Solve formula and display it in entry
        # which is pointed at by display
        if self.eq is None:
          self.eq = self.input
          self.display.text = 'A = '
        elif self.lower is None:
          self.lower = self.input
          self.display.text = 'B = '
        elif self.upper is None:
          self.upper = self.input

          self.solution()
          
          Logger.debug(['root => ', root])
          Logger.debug(['soln => ', soln])

        else:
          self.solution()
        # reset our input
        self.input = ''
      except Exception:
        # self.solution()
        pass



  def solution(self):
    
    Logger.info("solving ...")

    Logger.debug(['eq => ', self.eq])
    Logger.debug(['a => ', self.lower])
    Logger.debug(['b => ', self.upper])

    root, soln = solve("secant", self.eq, self.upper, self.lower)
    xs, fxs = soln
    xs.append(root)

    Logger.debug(["size: ", len(xs)])
    # Logger.debug([str(round(x, 4)) for x in xs])
    # Logger.debug([str(round(x, 6)) for x in fxs])
    
    self.display.text = str(round(root, 4))

    data = {
      'Step': [x+1 for x in range(len(xs))],
      'x': [round(x, 4) for x in xs],
      'f(x)': ['{:f}'.format(x) for x in fxs]
    }

    Logger.debug(data)
    soln_screen = screen_manager.get_screen('solution')
    soln_screen.display(data, ['Step', 'x', 'f(x)'], 'Step')
    screen_manager.current = 'solution'

class CalculatorScreen(Screen):
  pass

class SolutionScreen(Screen):
  def display(self, data, row, col):
    self.add_widget(DataTable(name = 'static', data=data, header_column = col,
                                    header_row = row))


class CalculatorApp(App):
  def build(self):
    calc = CalculatorScreen(name='calculator')
    calc.add_widget(CalculatorLayout())

    soln = SolutionScreen(name='solution')

    screen_manager.add_widget(calc)
    screen_manager.add_widget(soln)
    return screen_manager

calcApp = CalculatorApp()
calcApp.run()
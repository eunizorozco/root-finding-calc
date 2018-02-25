# ---------- main.py  ---------- 

import kivy
# kivy.require("1.9.0")
import itertools
from kivy.utils import get_color_from_hex as rgb
from kivy.app import App

from kivy.properties import DictProperty, NumericProperty, StringProperty, \
                            BooleanProperty, ObjectProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen

from utils.datatable import DataTable
from kivy.logger import Logger
from rootfinder import solve, Fx
from utils.shunting import shunt

import random

from math import sin, floor, ceil, sqrt
from kivy.garden.graph import Graph, LinePlot, SmoothLinePlot, HBar, MeshLinePlot

screen_manager = ScreenManager()

class CalculatorLayout(GridLayout):

  solutions = ObjectProperty(None)
  brange = ObjectProperty(None)

  def enter(self, text):
    if self.input is None:
      self.input = text
    else:
      self.input += text
    self.display.text += text

  def clear(self):
    self.display.text = "f(x) = "
    self.input = ''
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
        pass

  def graph(self):
    graph_screen = screen_manager.get_screen('graph')
    screen_manager.current = 'graph'

    fx = Fx(shunt(self.eq)).eval
    colors = itertools.cycle([rgb('dc7062'), rgb('fff400'), rgb('7dac9f'), rgb('66a8d4'), rgb('e5b060')])
      
    fxplot = SmoothLinePlot(color=next(colors))

    for i in range(-500, 501):
      x = i / 10.
      y = fx(x)
      fxplot.points.append((x, y))
    graph_screen.graph.add_plot(fxplot) 

    if self.solutions:
      plot = MeshLinePlot(color=rgb('fff400'))
      
      xmin = self.solutions[0]
      xmax = self.solutions[0]

      ymin = fx(xmin)
      ymax = ymin

      xmin = xmin
      xmax = xmin
      
      Logger.info("Plotting")

      plotx = MeshLinePlot(color=rgb('fff400'))
      plotx.points = [(x, fx(x)) for x in self.solutions]
      # graph_screen.graph.add_plot(plotx)

      counter = len(self.solutions)
      while counter >= 3:
        Logger.info(counter)
        for index in range(min(3, counter)):
          x = self.solutions[index]
          y = fx(x)
          x = x

          xmin = min([xmin, x])
          xmax = max([xmax, x])

          ymin = min([ymin, y])
          ymax = max([ymax, y])

          plot.points.append((x, y))
          counter = counter - 1
          if len(plot.points) >= min(3, len(self.solutions)):
            Logger.debug(plot.points)
            graph_screen.graph.add_plot(plot)
            plot = MeshLinePlot(color=next(colors))
            self.solutions.pop(0)
            counter = len(self.solutions)
            break
    

    pad = 0.5
    Logger.debug(plot.points)
    graph_screen.graph.xmin = min(xmin-pad, 0)
    graph_screen.graph.xmax = xmax+pad

    graph_screen.graph.ymin = ymin-pad
    graph_screen.graph.ymax = ymax+pad

    # Logger.debug([xmin, xmax])
    hbar = MeshLinePlot(color=[1, 1, 1, 1])
    hbar.points.append((graph_screen.graph.xmin, 0))
    hbar.points.append((graph_screen.graph.xmax, 0))
    
    vbar = MeshLinePlot(color=[1, 1, 1, 1])
    vbar.points.append((0, graph_screen.graph.ymin))
    vbar.points.append((0, graph_screen.graph.ymax))
    
    graph_screen.graph.add_plot(hbar)
    graph_screen.graph.add_plot(vbar)
    
    # Logger.debug([ymin, ymax])
    
  def solution(self):
    
    Logger.info("solving ...")

    Logger.debug(['eq => ', self.eq])
    Logger.debug(['a => ', self.lower])
    Logger.debug(['b => ', self.upper])

    self.brange = (int(self.lower), int(self.upper))
    root, soln = solve("secant", self.eq, self.upper, self.lower)
    roots, fxs = soln
    roots.append(root)

    self.solutions = roots
    self.display.text = str(round(root, 4))

    data = {
      'Step': [x+1 for x in range(len(roots))],
      'x': [round(x, 4) for x in roots],
      'f(x)': ['{:f}'.format(x) for x in fxs]
    }

    Logger.debug(data)
    # soln_screen = screen_manager.get_screen('solution')
    # soln_screen.display(data, ['Step', 'x', 'f(x)'], 'Step')
    # screen_manager.current = 'solution'

class CalculatorScreen(Screen):
  pass

class SolutionScreen(Screen):
  def display(self, data, row, col):
    self.add_widget(DataTable(name = 'static', data=data, header_column = col,
                                    header_row = row))

class GraphScreen(Screen):

  graph = ObjectProperty(None)

  def __init__(self, name):
    super(GraphScreen, self).__init__()
    self.name = name
    self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=0,
      x_ticks_major=0.1, y_ticks_major=0.1,
      y_grid_label=True, x_grid_label=True, padding=10,
      x_grid=True, y_grid=True, xmin=-0, xmax=50, ymin=-1, ymax=1)
    self.add_widget(self.graph)
    

class CalculatorApp(App):
  def build(self):
    calc = CalculatorScreen(name='calculator')
    calc.add_widget(CalculatorLayout())
    # calc.add_widget(GraphLayout())
    soln = SolutionScreen(name='solution')
    graph = GraphScreen(name='graph')
    
    screen_manager.add_widget(calc)
    screen_manager.add_widget(soln)
    screen_manager.add_widget(graph)

    return screen_manager

calcApp = CalculatorApp()
calcApp.run()
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
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.logger import Logger

from utils.datatable import DataTable

from rootfinder import solve, Fx
from utils.shunting import shunt

import random

from math import sin, floor, ceil, sqrt
from kivy.garden.graph import Graph, LinePlot, SmoothLinePlot, HBar, MeshLinePlot

screen_manager = ScreenManager(transition=NoTransition())

class CalculatorLayout(GridLayout):

  solutions = ObjectProperty(None)
  brange = ObjectProperty(None)

  data = ObjectProperty(None)

  def trigo(self, text):
    self.enter(text + '(')

  def enter(self, text):
    if self.input is None:
      self.input = text
    else:
      self.input += text
    self.display.text += text

  def clear(self):
    self.display.text = "f(x) = "
    self.input = ''
    self.eq = ''
    self.lower = ''
    self.upper = ''

  def calculate(self):
    if self.input:
      try:
        # Solve formula and display it in entry
        # which is pointed at by display
        if self.eq is None or self.eq == '':
          if self.input.find('x') < 0:
            self.display.text = 'Ans = ' + str(eval(self.input))
          else:
            self.eq = self.input
            self.display.text = 'A = '
        elif self.lower is None or self.lower == '':
          self.lower = self.input
          self.display.text = 'B = '
        elif self.upper is None or self.upper == '':
          self.upper = self.input

          self.solve()
          Logger.debug(['root => ', root])
          Logger.debug(['soln => ', soln])

        else:
          self.solve()
        # reset our input
        self.input = ''
      except Exception:
        pass

  def solve(self):
    
    Logger.info("solving ...")

    Logger.debug(['eq => ', self.eq])
    Logger.debug(['a => ', self.lower])
    Logger.debug(['b => ', self.upper])

    self.brange = (int(self.lower), int(self.upper))
    try:
      root, soln = solve("secant", self.eq, self.upper, self.lower)
      roots, fxs = soln
      roots.append(root)

      self.solutions = roots
      self.display.text = 'Ans = '+str(round(root, 4))
      screen = screen_manager.get_screen('solution').layout
      screen.refresh_datatable(soln)

    except Exception as e:
      Logger.debug(['exception => ', e])
      self.display.text = str(e)

  def graph(self):
    soln_graph = screen_manager.get_screen('solution').layout

    fx = Fx(shunt(self.eq)).eval
    colors = itertools.cycle([rgb('dc7062'), rgb('fff400'), rgb('7dac9f'), rgb('66a8d4'), rgb('e5b060')])
      
    fxplot = SmoothLinePlot(color=next(colors))

    for i in range(-500, 501):
      x = i / 10.
      y = fx(x)
      fxplot.points.append((x, y))
    soln_graph.graph.add_plot(fxplot) 

    if self.solutions:
      plot = MeshLinePlot(color=rgb('fff400'))
      
      xmin = round(self.solutions[0], 4)
      xmax = xmin

      ymin = fx(xmin)
      ymax = ymin

      xmin = xmin
      xmax = xmin
      
      Logger.info("Plotting")

      plotx = MeshLinePlot(color=next(colors))
      plotx.points = [(x, fx(x)) for x in self.solutions]

      counter = len(self.solutions)
      while counter >= 3:
        Logger.info(counter)
        for index in range(min(3, counter)):
          x = round(self.solutions[index], 4)
          y = round(fx(x), 4)
          x = x

          xmin = min([xmin, x])
          xmax = max([xmax, x])

          ymin = min([ymin, y])
          ymax = max([ymax, y])

          plot.points.append((x, y))
          counter = counter - 1
          if len(plot.points) >= min(3, len(self.solutions)):
            Logger.debug(plot.points)
            soln_graph.graph.add_plot(plot)
            plot = MeshLinePlot(color=next(colors))
            self.solutions.pop(0)
            counter = len(self.solutions)
            break

    pad = 0.1
    Logger.debug(plot.points)
    soln_graph.graph.xmin = round(xmin-pad, 1)
    soln_graph.graph.xmax = round(xmax+pad, 1)

    soln_graph.graph.ymin = round(ymin-pad, 2)
    soln_graph.graph.ymax = round( ymax+pad, 2)

    hbar = MeshLinePlot(color=[1, 1, 1, 1])
    hbar.points.append((soln_graph.graph.xmin, 0))
    hbar.points.append((soln_graph.graph.xmax, 0))
    soln_graph.graph.add_plot(hbar)

    for x, y in plotx.points:
      vbar = MeshLinePlot(color=rgb('6d98e2'))
      vbar.points.append((x, 0))
      vbar.points.append((x, y))
      soln_graph.graph.add_plot(vbar)
    

  def solution(self):
    # screen_manager.transition.direction = 'left'
    if self.solutions:
      if len(self.solutions) > 50:
        label = Label(text='Calculations took '+str(len(self.solutions))+ ' iterations and exceeded the allocation to be graphed.', size_hint_y=None)
        label.text_size = Window.width/3, None
        popup = Popup(title='Cannot graph solution', size_hint=(None, None), size=(Window.width/2, Window.height/2), content= label)
        popup.open()
      else:
        self.graph()
    screen_manager.current = 'solution'


class SolutionSreen(Screen):
  """docstring for SolutionSreen"""
  layout = ObjectProperty(None)


class SolutionLayout(GridLayout):

  table = GridLayout(cols=3, size_hint_y=None, spacing=5)
  graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=0,
      x_ticks_major=0.1, y_ticks_major=0.1,
      y_grid_label=True, x_grid_label=True, padding=10,
      x_grid=True, y_grid=True, xmin=-0, xmax=50, ymin=-1, ymax=1)

  boxlayout = BoxLayout(orientation='vertical')
  scrollview = ScrollView()

  backbutton = Button(text='BACK TO CALCULATOR', size_hint=(1, 0.1), background_color=[0, 0, 0, 1])

  def setup_widget(self):

    self.table.bind(minimum_height=self.table.setter('height'))
    self.backbutton.on_press = self.back

    self.scrollview.add_widget(self.table)
    self.boxlayout.add_widget(self.graph)
    self.boxlayout.add_widget(self.backbutton)

    self.add_widget(self.scrollview)
    self.add_widget(self.boxlayout)
    
  def refresh_datatable(self, data):
    self.table.clear_widgets()
    roots, fxs = data
    i = 0
    self.table.add_widget(Button(text="Steps", size_hint_y=None, height=100, size_hint=(0.2, None)))
    self.table.add_widget(Button(text="x", size_hint_y=None, height=100, size_hint=(0.4, None))) 
    self.table.add_widget(Button(text="f(x)", size_hint_y=None, height=100, size_hint=(0.4, None)))

    for x in roots:
      self.table.add_widget(Button(text=str(i+1), height=40, size_hint=(0.2, None)))
      self.table.add_widget(Button(text=str(round(x, 4)),background_color = [0, 0, 0, 1], height=40, size_hint=(0.4, None))) 
      self.table.add_widget(Button(text='{:f}'.format(fxs[i]), background_color = [0, 0, 0, 1], height=40, size_hint=(0.4, None)))
      i = i + 1
    
  def back(self):
    screen_manager.current = 'calculator'


class CalculatorApp(App):
  def build(self):

    calc = Screen(name='calculator')
    calc.add_widget(CalculatorLayout())

    soln = SolutionSreen(name='solution')
    soln.layout = SolutionLayout(cols=2, size = (Window.width, Window.height))
    soln.layout.setup_widget()
    soln.add_widget(soln.layout)
    
    screen_manager.add_widget(calc)
    screen_manager.add_widget(soln)

    return screen_manager

calcApp = CalculatorApp()
calcApp.run()
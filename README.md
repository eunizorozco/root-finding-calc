# Root Finding Calculator

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To get the Root Finding Calculator up and running for development you need to have the following installed in your machine:

```
1. Python 2.7.11
2. Kivy 
3. Java

```

To install Python go to their website and follow the instruction for your operating system.

https://wiki.python.org/moin/BeginnersGuide


To install Kivy in your Mac OSX, you must:

```
1. Navigate to the latest Kivy release at https://kivy.org/downloads/ and download Kivy-*-osx-python*.dmg.
2. Open the dmg
3. Copy the Kivy.app to /Applications.
4. Create a symlink by running the makesymlinks in the window that opens when you open the dmg
4. Examples and all the normal kivy tools are present in the Kivy.app/Contents/Resources/kivy directory.

```

If you're running other operating system see: https://kivy.org/docs/installation/installation.html

### Installing and Running

1. Download this project by clicking the "Clone or download" button at the upper right or use git:

```
git clone https://github.com/eunizorozco/root-finding-calc.git

```

2. Once downloaded, just type:

```
kivy main.py -d

```


## Features

Below are the implemented algorithms we have in this project.

### Secant Method

The secant method is a root-finding algorithm that uses a succession of roots of secant lines to better approximate a root of a function f.

The secant method can be thought of as a finite difference approximation of Newton's method. where derivative is replaced by secant line.

We use the root of secant line (the value of x such that y=0) as root approximation for function f.

Suppose we have starting values x0 and x1, with function values f(x0) and f(x1).
The secant line has equation:

![alt text](http://planetcalc.com/cgi-bin/mimetex.cgi?%5Cfrac%7By%20-%20f%28x_1%29%7D%7Bf%28x_1%29-f%28x_0%29%7D%3D%5Cfrac%7Bx%20-%20x_1%7D%7Bx_1-x_0%7D)


The root of secant line (where у=0) hence:

![alt text](http://planetcalc.com/cgi-bin/mimetex.cgi?x%20%3D%20x_1%20-%20%5Cfrac%7Bx_1%20-%20x_0%7D%7Bf%28x_1%29-f%28x_0%29%7Df%28x_1%29)

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```


## Deployment

Add additional notes about how to deploy this on a live system


## Authors

@eunizorozco



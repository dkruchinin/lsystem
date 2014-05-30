lsystem
=======

Simple [L-system](http://en.wikipedia.org/wiki/Lsystem) based fractal generator written just for fun.

Usage
=======


    % ./lsystem.py
    USAGE: ./lsystem.py -c <config.json> -g <WIDTH>x<HEIGHT> [-h]

* -g: controls geometry of a window where fractal will be drawn
* -c: specifies a file in JSON format with a description of fractal according to the L-system rules

L-system file syntax
-------------------

```javascript
{
	"iters": integer, // number of iterations
	"angle": double, // angle (in degrees from 0 to 360)
	"axiom": string,
	"rules": { // rules of inference
		string: string, // rule 1
		...,
		string: string // rule N
	}
}
```

Alphabet that can be used in axioms and rules is pretty simple: *FGf+-[]*. Each letter is responsible for particular
turtle (see [turtle graphics](http://en.wikipedia.org/wiki/Turtle_graphics) for more info) command, namely:

* *F* and *G*: draw forward
* *f*: move cursor forward without drawing anything
* *+*: turn right
* *-*: turn left
* *[*: push current state of the cursor into the stack
* *]*: pop state of the cursor from the stack

Some examples of valid L-system files:
--------------------------------------

* **Dragon curve**

```javascript
{
	"iters": 10,
	"angle": 90,
	"axiom": "F",
	"rules": {
		"F": "F+G+",
		"G": "-F-G"
	}
}
```

* **Fractal plant**

```javascript
{
	"iters": 4,
	"angle": 22.5,
	"axiom": "F",
	"rules": {
		"F": "FF-[-F+F+F]+[+F-F-F]"
	}
}
```

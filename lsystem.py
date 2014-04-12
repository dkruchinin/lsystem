#!/usr/bin/python

import sys, json, getopt
import Tkinter as tk
from lsys import LSystemVisualiser, LGrammar


MIN_WIDTH = 300
MIN_HEIGHT = 300


def usage():
    sys.stderr.write("USAGE: %s -c <config.json> -g <WIDTH>x<HEIGHT> [-h]\n"
                     % (sys.argv[0]))
    sys.exit(1)


def main(cfg, width, height):
    master = tk.Tk()
    master.geometry("%dx%d%+d%+d" % (width, height, 0, 0))
    canvas = tk.Canvas(master, width=width, height=height)
    canvas.pack()

    try:
        grammar = LGrammar(cfg['rules'])
        lvis = LSystemVisualiser(canvas, cfg['angle'],
                                 grammar.generate(cfg['axiom'],
                                                  cfg['iters']))
        lvis.draw()
    except ValueError as err:
        sys.stderr.write("Error: " + str(err) + "\n")
        sys.exit(1)

    master.update()    
    tk.mainloop()

if __name__ == '__main__':
    cfg, width, height = (None, None, None)

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "c:g:h")
    except getopt.GetoptError as err:
        sys.stderr.write("Error: " + str(err) + "\n")
        usage()

    for o, a in opts:
        if o == '-c':
            cfg = json.load(open(a))
        elif o == '-g':
            try:
                width, height = [int(i) for i in a.split("x")]
            except ValueError:
                usage()

            width = max(width, MIN_WIDTH)
            height = max(height, MIN_HEIGHT)
        else:
            usage()

    if not any([cfg, width, height]):
        usage()

    main(cfg, width, height)

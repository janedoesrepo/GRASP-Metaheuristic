""" Import-function for the data set of Martino and Pastor (2010)
    The data is available at https://www.assembly-line-balancing.de/sualbsp

    line 1:                     n; number of tasks
    line 2:                     p; number of direct precedence relations
    line 3:                     c; cycle time
    lines 4 to 4+n-1:           cl, t; id task, processing time
    lines 4+n to 4+n+p-1:       relations; direct precedence relations in form i,j
    lines 4+n+p to 4+2n+p-1:    tsu; setup times
"""

# load packages
from tkinter import filedialog
from tkinter import *


def getData(dateiname=None):

    if dateiname is None:
        # open file via Tkinter-Gui in read-only mode
        root = Tk()
        root.filename = filedialog.askopenfilename(initialdir="../data/",
                                                   title="Select file",
                                                   filetypes=(("txt-files", "*.txt"), ("all files", "*.*")))
        file = open(root.filename, "r")
        root.quit()
        root.destroy()
    else:
        file = open("../data/" + dateiname, "r")

    # Read and assign data
    n = int(file.readline())
    cl = list(range(n))
    p = int(file.readline())
    c = int(file.readline())

    t = list(range(n))
    for i in range(n):
        _, t[i] = file.readline().split(',')
        t[i] = int(t[i])

    rel = [[] for _ in range(n)]
    for i in range(p):
        a, b = file.readline().split(',')
        a, b = int(a), int(b)
        rel[b].append(a)

    tsu = []
    for i in range(n):
        line = file.readline().split(',')
        for string in line:
            line[line.index(string)] = int(string)
        tsu.append(line)

    file.close()  # close file

    print("*Import von %s erfolgreich!*" % dateiname)
    # print("Number of tasks n: %d" % n, type(n), "\n"
    #       "Cycle time c: %d" % c, type(c), "\n"
    #       "Candidate list cl.", type(cl), "of length %d." % len(cl), "\n"
    #       "Processing times for tasks t", type(t), "of length %d." % len(t),  "\n"
    #       "Precedence relations rel", type(rel), "of length %d." % len(rel), "\n"
    #       "Setup times matrix tsu:", type(tsu), "of dimensions %dx%d." % (len(tsu), len(tsu[0])))
    # for line in tsu:
    #     print(line)
    # print('-' * 25)

    return n, c, cl, t, rel, tsu

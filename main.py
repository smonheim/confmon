import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import csv
import math

# check if something is in conformance
def conf_check(ex,ey,ax,ay,r):
    r = 300
    mag_rad = math.sqrt(((ex - ax)**2) + ((ey - ay)**2))
    print(mag_rad)
    if mag_rad >= r/6:
        print("Aircraft is out of conformance\nActual position is: [" + 
              str(ax) + ',' + str(ay) + "]\nExpected position is within " + 
              str(int(r/6)) + " units around: [" + str(ex) + "," + str(ey) + ']')
        return False
    return True

# called at start of FuncAnimation
def init():
    lines[0].set_offsets([])
    lines[1].set_data([], [])
    return lines

# callback for every animation frame
def animate(i):
    xy1 = []
    x2 = []
    y2 = []
    for k in range(len(data)):

        # xy1.append([data[k][0], data[k][1]])
        if k <= i:
            xy1.append([data[k][0], data[k][1]])
            x2.append(data[k][2])
            y2.append(data[k][3])
        else: break

    conf_check(xy1[-1][0], xy1[-1][1], x2[-1], y2[-1], r)
    lines[0].set_offsets(xy1)
    lines[1].set_data(x2, y2)
    return lines

# global variable, radius of conformance bubble
r = 300

# read in csv data
with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# reorg and recast everything as ints
data = [[int(y) for y in x] for x in data]

# init matplotlib stuff
fig = plt.figure()
ax1 = plt.axes(xlim=(0,2000), ylim=(0,2000))
line, = ax1.plot([], [], lw=2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plotlays, plotcols = [2], ["black","red"]
lines = []

# instantiate the scatter (expected x/y) and append to the lines array
lobj = ax1.scatter([],[], s=r, alpha=0.2, c=plotcols[0])
lines.append(lobj)

# instantiate the line (actual x/y) and append to the lines array
lobj = ax1.plot([],[],lw=2,color=plotcols[1])[0]
lines.append(lobj)

# animate this thingymawhozitz
anim = ani.FuncAnimation(fig, animate, init_func=init,
                               frames=20, interval=1000, blit=True)

# show the plot
plt.show()
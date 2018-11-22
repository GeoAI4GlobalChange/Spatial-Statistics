import numpy as np
from common import Point, Boundary
from quadtree import DynamicQuadTree
from plotCircles import plotCircle
result_dir="dataset/Uber_QFAKDE_1000h_5_20.csv"
data_dir="dataset/Uber1000.csv"
result=open(result_dir,'a+')
result.write('ID,x,y,h\n')
def plot_partitions(node):
    x, y,key = node.boundary.center
    d = node.boundary.dimension
    if len(node._points)>0:
        pts=list(node._points)
        for pt in range(len(pts)):
            result.write(pts[pt].key+','+str(pts[pt].x)+','+str(pts[pt].y)+','+str(d)+'\n')
            plotCircle(pts[pt].x,pts[pt].y,d)

    xmin = x - d
    xmax = x + d
    ymin = y - d
    ymax = y + d

    plt.plot([xmin, xmax], [ymax, ymax], lw=.5, color='black')
    plt.plot([xmax, xmax], [ymin, ymax], lw=.5, color='black')
    plt.plot([xmax, xmin], [ymin, ymin], lw=.5, color='black')
    plt.plot([xmin, xmin], [ymin, ymax], lw=.5, color='black')

    for region in node._nodes:
        plot_partitions(node._nodes[region])
lines=open(data_dir)
import time
time_start=time.time()
x=[]
y=[]
points={}
for line in lines:
    attr = line.split('\n')[0].split(",")
    if attr[1]!='x':
        if attr[0] not in points:
            points[attr[0]]=[float(attr[1])]
            points[attr[0]].append(float(attr[2]))
            x.append(float(attr[1]))
            y.append(float(attr[2]))
import matplotlib.pyplot as plt
plt.plot(x,y,'bo')
x=np.array(x)
y=np.array(y)
x_max=np.max(x)
x_min=np.min(x)
y_max=np.max(y)
y_min=np.min(y)
x_center=(x_max-x_min)/2+x_min
y_center=(y_max-y_min)/2+y_min
dimension=max((x_max-x_min)/2,(y_max-y_min)/2)
n=len(x)
Npt=pow(n,1/2)
divide_deep=5# the maximum depth
granularity=20# the larger this value is, the finer granularity of each block is recognized
qt = DynamicQuadTree(centerPt=Point(x_center,y_center,'center'),dimension=dimension,max_points=Npt/20,max_depth=divide_deep)
for pt in points:
    qt.insert(Point(points[pt][0],points[pt][1],pt))
plot_partitions(qt.root)
time_end=time.time()
print('totally cost',time_end-time_start)
plt.show()
lines.close()
result.close()


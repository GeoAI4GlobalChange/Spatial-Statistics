import csv
#lines=csv.reader(open("E:/lifa/software/R/R-3.5.1/library/spatstat/test.csv"))


import time
import numpy as np
import math
import matplotlib.pyplot as plt
time_start=time.time()
def fixedKDE(input_dir):
    lines = open(input_dir)
    points={}
    x=[]
    y=[]
    dis=[]
    for line in lines:
        attr = line.split(",")
        if attr[1]!='x':
            if attr[0] not in points:
                points[attr[0]]=[float(attr[1])]
                points[attr[0]].append(float(attr[2]))
                x.append(float(attr[1]))
                y.append(float(attr[2]))

    #plt.plot(x,y,'bo')
    #plt.show()
    x=np.array(x)
    y=np.array(y)
    x_mean=np.mean(x)
    y_mean=np.mean(y)
    for i in range(len(x)):
        dis.append(math.pow(math.pow(x[i]-x_mean,2)+math.pow(y[i]-y_mean,2),0.5))
    dis_array=np.array(dis)
    q1=np.percentile(dis_array,25)
    q3=np.percentile(dis_array,75)
    dis_std=np.std(dis_array)
    n=len(x)
    #h=pow(2/(3*n),0.25)*dis_std
    delta=min(dis_std,(q3-q1)/1.34)
    h=1.06*delta*pow(len(x),-0.2)
    time_rule=time.time()
    print('rule of thumb time cost:',time_rule-time_start,'h:',h)
    delta_h=h/10
    e_h=delta_h/20
    iters=0
    max_iters=30
    while (delta_h>e_h) and max_iters>iters:
        iters+=1
        h_list=[h-delta_h,h,h+delta_h]
        L=[0,0,0]
        for i in points:
            fi=np.zeros(3)
            for j in points:
                if i!=j:
                    dij_square=pow(points[i][0]-points[j][0],2)+pow(points[i][1]-points[j][1],2)
                    for fi_idx in range(len(fi)):
                        fi[fi_idx]+=pow(math.e,-dij_square/(2*pow(h_list[fi_idx],2)))/pow(h_list[fi_idx],2)
            for fi_idx in range(len(fi)):
                fi[fi_idx]=1/(2*math.pi*(n-1))*fi[fi_idx]
                if fi[fi_idx]!=0:
                    L[fi_idx]+=math.log(fi[fi_idx])
        max_L=max(L)
        if max_L==L[1]:
            delta_h=delta_h/2
        else:
            idx=L.index(max_L)
            if idx==0:
                h=h-delta_h
            elif idx==2:
                h = h + delta_h
        #print(h)
    time_end = time.time()
    print('cross-validation based KDE time cost', time_end - time_start)
    print("the cross-validation based fixed h:" + str(h))


if __name__=="__main__":
    input_dir="../dataset/Uber1000.csv"
    fixedKDE(input_dir)








#for i in points:

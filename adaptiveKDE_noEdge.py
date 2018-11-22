lines=open("dataset/Uber1000.csv").readlines()
result=open("dataset/Uber1000_h.csv",'a+')
result.write('ID,x,y,h\n')
import time
time_start=time.time()
a, delta_a, e_a=0.5, 0.1, 0.005
points={}
x=[]
y=[]
dis=[]
for line in lines:
        attr = line.split("\n")[0].split(",")
        if attr[1] != '"x"':
            if attr[0] not in points:
                    points[attr[0]]=[float(attr[1])]
                    points[attr[0]].append(float(attr[2]))
                    x.append(float(attr[1]))
                    y.append(float(attr[2]))
import numpy as np
import math
import matplotlib.pyplot as plt
plt.plot(x,y,'bo')
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
print("thumb-h:",h)
delta_h=h/10
e_h=delta_h/20
iters=0
max_iters=12
while (delta_a>e_a or delta_h>e_h) and max_iters>iters:
    iters+=1
    g=[1,1,1]
    h_list=[h-delta_h,h,h+delta_h]
    for i in points:
        fi=[0,0,0]
        for j in points:
            dij_square=pow(points[i][0]-points[j][0],2)+pow(points[i][1]-points[j][1],2)
            for h_idx in range(len(h_list)):
                h1=h_list[h_idx]
                fi[h_idx]+=pow(math.e,-dij_square/(2*pow(h1,2)))
        for h_idx in range(len(h_list)):
            h1 = h_list[h_idx]
            fi[h_idx]=1/(2*math.pi*n*pow(h1,2))*fi[h_idx]
            if len(points[i])<10:
                points[i].append(fi[h_idx])
            else:
                points[i][2+h_idx]=fi[h_idx]
            if fi[h_idx]!=0:
                g[h_idx]+=math.log(fi[h_idx])
    #x,y,fi(h-delta_h),fi(h),fi(h+delta_h)
    a_list=[a-delta_a,a,a+delta_a]
    for h_idx in range(len(h_list)):
        g[h_idx]=pow(math.e,g[h_idx]/n)
        for i in points:
            if h_idx==0:
                a1=a_list[0]
                hi=pow(points[i][2+h_idx]/g[h_idx],-a1)*h_list[h_idx]
                if len(points[i]) < 10:
                    points[i].append(hi)
                else:
                    points[i][5]=hi
            elif h_idx==1:
                for a_idx in range(len(a_list)):
                    a1 = a_list[a_idx]
                    hi = pow(points[i][2 + h_idx] / g[h_idx], -a1) * h_list[h_idx]
                    if len(points[i]) < 10:
                        points[i].append(hi)
                    else:
                        points[i][6+a_idx] = hi
            else:
                a1 = a_list[2]
                hi = pow(points[i][2 + h_idx] / g[h_idx], -a1) * h_list[h_idx]
                if len(points[i]) < 10:
                    points[i].append(hi)
                else:
                    points[i][9] = hi
    #x,y,fi(h-delta_h),fi(h),fi(h+delta_h),hi(a-,h-),hi(a-,h),hi(a,h),hi(a+,h),hi(a+,h+)
    L=[0,0,0,0,0]
    for i in points:
        fi=np.zeros(5)
        for j in points:
            if i!=j:
                dij_square=pow(points[i][0]-points[j][0],2)+pow(points[i][1]-points[j][1],2)
                for fi_idx in range(len(fi)):
                    fi[fi_idx]+=pow(math.e,-dij_square/(2*pow(points[j][5+fi_idx],2)))/pow(points[j][5+fi_idx],2)
        for fi_idx in range(len(fi)):
            fi[fi_idx]=1/(2*math.pi*(n-1))*fi[fi_idx]
            if fi[fi_idx]!=0:
                L[fi_idx]+=math.log(fi[fi_idx])
    max_L=max(L)
    if max_L==L[2]:
        delta_a=delta_a/2
        delta_h=delta_h/2
    else:
        idx=L.index(max_L)
        if idx==0:
            a=a-delta_a
            h=h-delta_h
        elif idx==1:
            a=a-delta_a
        elif idx==3:
            a=a+delta_a
        elif idx==4:
            a = a + delta_a
            h = h + delta_h
    print(h)
time_end=time.time()
print('totally cost',time_end-time_start)
print("h:"+str(h)+",a:"+str(a))

for i in points:
    line=i+','+str(points[i][0])+','+str(points[i][1])+','+str(points[i][7])+'\n'
    result.write(line)
result.close()









#for i in points:

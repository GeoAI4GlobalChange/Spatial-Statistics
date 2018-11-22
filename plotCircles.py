import numpy as np
import matplotlib.pyplot as plt

def plotCircle(x,y,r):
    theta = np.arange(0, 2 * np.pi, 0.01)
    #plt.figure()
    plt.plot(x,y,'k-')
    x = x + r * np.cos(theta)
    y = y + r * np.sin(theta)
    plt.plot(x,y,'k')
    plt.axis('equal')
if __name__=="__main__":
    lines=open("QFAKDE_dataset/HubeiPOI_QFAKDE_1000h_6_20.csv")
    XC=[]
    YC=[]
    i=0;
    for line in lines:
        if i>0:
            attr=line.split('\n')[0].split(',')
            x=float(attr[1])
            y=float(attr[2])
            XC.append(x)
            YC.append(y)
            r=float(attr[3])
            plotCircle(x,y,r)
        i+=1
    plt.plot(XC,YC,'k.')
    plt.show()
    lines.close()
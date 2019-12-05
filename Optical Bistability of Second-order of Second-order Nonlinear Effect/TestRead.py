import numpy as np
data=open("data1.dat",'r')
n=2;i=0;j=0;
E=[]; g=[];
Result=[];
first=True;
dataOrigin=data.readlines()
print(dataOrigin)
for dataL in dataOrigin:
    if(dataL[1]=='-'):
        n=n-1;
        continue;
    if(n<1):
        break;
    dataS=dataL.split(' ')
    if (len(dataS)==1):
        g.append(float(dataS[0][0:-1]))
        i=i+1;
        if (i==2):
            first=False;
    else:
        if (first==True):
            j=j+1
            E.append(float(dataS[0]))
        Result.append(float(dataS[1]))
        Result.append(float(dataS[2][0:-1]))
E_array=np.asarray(E)
g_array=np.asarray(g)
ResultOut=np.asarray(Result)
ResultOut=ResultOut.reshape(i,j,2)
print(E)
print(g)
print(ResultOut)
        

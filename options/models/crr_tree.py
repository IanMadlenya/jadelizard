import math
from numpy import exp
import time

def CRRTree(K,T,S,sig,r,N,kind):
    
    dt=T/N;
    dxu=math.exp(sig*math.sqrt(dt));
    dxd=math.exp(-sig*math.sqrt(dt));
    pu=((math.exp(r*dt))-dxd)/(dxu-dxd);
    pd=1-pu;
    disc=math.exp(-r*dt);

    St = [0] * (N+1)
    C = [0] * (N+1)
    
    St[0]=S*dxd**N;
    
    for j in range(1, N+1): 
        St[j] = St[j-1] * dxu/dxd;
    
    for j in range(1, N+1):
        if kind == 'put':
            C[j] = max(K-St[j],0);
        elif kind == 'call':
            C[j] = max(St[j]-K,0);
    
    for i in range(N, 0, -1):
        for j in range(0, i):
            C[j] = disc*(pu*C[j+1]+pd*C[j]);
            
    return C[0]

if __name__=="__main__":
    time1 = time.time()
    [x=1
    for i in range(796): 
        op1 = CRRTree(125,x,100,.25,.005,25,"call")
        x+=.01
    time2 = time.time() - time1
    print(time2)


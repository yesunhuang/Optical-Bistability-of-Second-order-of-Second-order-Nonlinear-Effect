from qutip import *
from scipy import *
from scipy import optimize
from scipy.integrate import odeint
import numpy as np


class ProblemSolver:
    'The Problem Solver'
    g=0 #coupling rate
    Delta=np.zeros(2)#[Delta_a,Delta_b]
    N=np.zeros(4) #[N_a,N_b,Na_psi,Nb_psi] Number states
    E=0 #input amplitude
    c_ops=[]
    
    def __init__(self,Paramaters):
        "use this function to initial"
        self.SetParamaters(Paramaters)
        
       
    def SetParamaters(self,Paramaters):
        "use this function to set all the paramaters"
        (self.g,self.N,self.Delta,self.E)=Paramaters
        self.psi0=tensor(basis(self.N[0],self.N[2]),basis(self.N[1],self.N[3]))
        self.a=tensor(destroy(self.N[0]),qeye(self.N[1]))
        self.b=tensor(qeye(self.N[0]),destroy(self.N[1]))
        self.H=self.Delta[0]*self.a.dag()*self.a+self.Delta[1]*self.b.dag()*self.b\
            +self.g*(self.b*self.a.dag()*self.a.dag()+self.b.dag()*self.a*self.a)+self.E*(self.a.dag()+self.a)
        self.c_ops.clear()

        self.c_ops.append(sqrt(2)*self.a)
        self.c_ops.append(sqrt(4)*self.b)

    def DefaultCalculator(self):
        "Use the steadystate function to calculate"
        self.rho_ss=steadystate(self.H,self.c_ops)
        P_trans=expect(self.a.dag()*self.a,self.rho_ss)
        if self.E>0:
            P_in=self.E*self.E
        Output_rate=P_trans/P_in

        return (self.rho_ss,P_trans,Output_rate)

    def AdvanceCalculator(self,rtol,atol,steadytime,pace):
        "Use the mesolve function to calculate"
        tlistN=steadytime//pace
        tlist=np.linspace(0,steadytime,tlistN)
        options=Options()
        options.atol=atol
        options.rtol=rtol
        output=mesolve(self.H,self.psi0,tlist,self.c_ops,[self.a.dag()*self.a,self.b.dag()*self.b],options=options)
        P_trans=output.expect[0][-1]
        if self.E>0:
            P_in=self.E*self.E
        Output_rate=P_trans/P_in
        return(output,P_trans,Output_rate)

    def MeanFeildCalculator(self):
        "Use the mean-feild theory to calculate"
        N_a=optimize.fsolve(self.MeanFeildF,math.pow(self.E,2))
        N_b=math.pow(self.g,2)*math.pow(N_a,2)/(math.pow(self.Delta[1],2)+2)
        return (N_a,N_b)

    def MeanFeildF(self,N_a):
        F=(4*math.pow(self.g,4)/(math.pow(self.Delta[1],2)+2))*math.pow(N_a,3)\
        +((4*math.pow(self.g,2)*(2-self.Delta[0]*self.Delta[1]))/(math.pow(self.Delta[1],2)+2))*math.pow(N_a,2)\
        +(math.pow(self.Delta[0],2)+1)*N_a-math.pow(self.E,2)
        return F

    def ClusterSF(self,y,t):
        dy0=-(1j*self.Delta[0]+1)*y[0]-2j*self.g*y[7]-1j*self.E
        dy1=-(1j*self.Delta[1]+2)*y[1]-1j*self.g*y[2]
        dy2=-2j*self.E*y[0]-2j*self.g*y[1]-2*(1+1j*self.Delta[0])*y[2]\
            -4j*self.g*(y[1]*y[3]+np.conj(y[0])*y[6]+y[0]*y[7]-2*y[1]*np.conj(y[0])*y[0])
        dy3=1j*self.E*y[0]-1j*self.E*np.conj(y[0])-2*y[3]-2j*self.g*(y[1]*np.conj(y[2])+2*np.conj(y[0])*y[7]-2*y[1]*pow(np.conj(y[0]),2))\
            +2j*self.g*(np.conj(y[1])*y[2]+2*y[0]*np.conj(y[7])-2*np.conj(y[1])*pow(y[0],2))
        dy4=-2*(2+1j*self.Delta[1])*y[4]-2j*self.g*(y[1]*y[2]+2*y[0]*y[6]-2*y[1]*pow(y[0],2))
        dy5=-4*y[5]+1j*self.g*(y[1]*np.conj(y[2])+2*np.conj(y[0])*y[7]-2*y[1]*pow(np.conj(y[0]),2))\
            -1j*self.g*(np.conj(y[1])*y[2]+2*y[0]*np.conj(y[7])-2*np.conj(y[1])*pow(y[0],2))
        dy6=-1j*self.E*y[1]-(3+1j*self.Delta[0]+1j*self.Delta[1])*y[6]-2j*self.g*(2*y[1]*y[7]+np.conj(y[0])*y[4]-2*np.conj(y[0])*pow(y[1],2))\
            -1j*self.g*(3*y[0]*y[2]-2*pow(y[0],3))
        dy7=1j*self.E*y[1]+(1j*self.Delta[0]-3-1j*self.Delta[1])*y[7]-1j*self.g*(np.conj(y[0])*y[2]+2*y[0]*y[3]-2*np.conj(y[0])*pow(y[0],2))\
            +2j*self.g*(np.conj(y[1])*y[6]+y[1]*y[7]+y[0]*y[5]-2*np.conj(y[1])*y[1]*y[0])
        dydt=[dy0,dy1,dy2,dy3,dy4,dy5,dy6,dy7]
        return dydt

    def ClusterCtoR(self,y,t):
        yc=y[0:8]+1j*y[8:16]
        dydtc=self.ClusterSF(yc,t)
        dydt=np.hstack((np.real(dydtc),np.imag(dydtc)))
        return dydt

    def ClusterCalculator(self,steadytime,pace):
        tlistN=steadytime//pace
        tlist=np.linspace(0,steadytime,tlistN)
        y0=np.zeros(16)
        sol=odeint(self.ClusterCtoR,y0,tlist)
        return (sol[-1,3],sol[-1,5])






#from ProblemSolver import *
#Paramaters= (0.333, [10,10,2,1], [0.8, 1.6], 0.106)
#ps=ProblemSolver(Paramaters)
#(a,b,c)=ps.DefaultCalculator()
#(a1,b1,c1)=ps.AdvanceCalculator(1e-8,1e-6,10,0.001)




        






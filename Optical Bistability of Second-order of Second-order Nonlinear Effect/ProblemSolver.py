from qutip import *
from scipy import *
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
        Expect=[self.a.dag()*self.a,self.b.dag()*self.b,\
            self.a.dag()*self.a.dag()*self.a*self.a,self.b.dag()*self.b.dag()*self.b*self.b]
        output=mesolve(self.H,self.psi0,tlist,self.c_ops,Expect,options=options)
        P_trans=output.expect[0][-1]
        co1=output.expect[2][-1]/math.pow(P_trans,2)
        co2=output.expect[3][-1]/math.pow(output.expect[1][-1],2)
        return(output,P_trans,co1,co2)

#from ProblemSolver import *
#Paramaters= (0.333, [10,10,2,1], [0.8, 1.6], 0.106)
#ps=ProblemSolver(Paramaters)
#(a,b,c)=ps.DefaultCalculator()
#(a1,b1,c1)=ps.AdvanceCalculator(1e-8,1e-6,10,0.001)




        






from ProblemSolver import *
import matplotlib as mpl
import matplotlib.pyplot as plt


class OBF:
    'MainClass'
    def __init__(self):
        "Initial the setting"
        self.g=0.333
        self.Delta=np.asarray([0.8, 1.6])
        self.accuracy=0.0001
        self.Pace=0.001
        self.rtol=1e-6
        self.atol=1e-8
    def ChangeSetting(self,Paramaters):
        "Change setting"
        (self.g,self.Delta,self.Pace,self.accuracy)=Paramaters
    def PlotRevolution(self,E,N,Time):
        "Plot a simple revolution"
        solver=ProblemSolver((self.g,N,self.Delta,E))
        (output,P_trans,Output_rate)=solver.AdvanceCalculator(self.rtol,self.atol,Time,self.Pace)
        print(output.states)
        (state,P_trans2,Output_rate2)=solver.DefaultCalculator()
        print('DefalutCalculate:',P_trans2,' AdvanceCalculator:',P_trans)
        tlistN=Time//self.Pace
        tlist=np.linspace(0,Time,tlistN)
        n_a = output.expect[0];n_b = output.expect[1]
        fig, axes = plt.subplots(1, 1, figsize=(8,6))
        axes.plot(tlist, n_a, label="mode a");axes.plot(tlist, n_b, label="mode b")
        axes.set_xlim(0, Time);axes.legend(loc=0)
        axes.set_xlabel('Time');axes.set_ylabel('Photons Numbers')
        plt.show()
    def PlotRelation(self,E,g,Option=False):
        "The main function"
        E_list=E;g_list=g;
        self.Result_out=np.zeros([size(g_list),np.size(E_list)])
        ps=ProblemSolver((self.g,[6,3,1,1],self.Delta,0.333))

        for j in range(0,np.size(g_list)):
             Time=5
             for i in range(0,np.size(E_list)):
                Na=int(max(math.ceil(E_list[i]*E_list[i]+6*E_list[i]),4));
                Nb=int(Na//2);
                ps.SetParamaters((g_list[j],[Na,Nb,0,0],self.Delta,E_list[i]))
                (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,Time,self.Pace)
                while (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])>self.accuracy):
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    Time=Time*2
                    (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,Time,self.Pace)
                if (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])<(self.accuracy/100)) and (Time>2) :
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    Time=Time//2
                self.Result_out[j][i]=P_trans

        self.PlotResult(Option,E,g)


    def PlotResult(self,Option,E,g):
        "Plot the result"
        fig, axes = plt.subplots(1, 1, figsize=(8,6))
        axes.set_xlim(E[0]*E[0],E[-1]*E[-1]);
        if (not Option):
            axes.set_xlabel('P_in(E*E)')
            for j in range(0,np.size(g)):
                axes.plot(E*E,self.Result_out[j],label='g='+str(round(g[j],2)))
        else:
            axes.plot(g,self.Result_out[...,0],label='E^2='+str(round(E[0]*E[0],2)))
            axes.set_xlabel('g')
        axes.legend(loc=0);
        axes.set_ylabel('P_trans')
        plt.show()

    def SaveData(self,name,E,g):
        "Save to file"
        data = open(name,'a')
        for j in range(0,size(g)):
            data.write(str(g[j])+'\n')
            for i in range(0,size(E)):
                data.write(str(E[i])+' '+str(self.Result_out[j][i]))
                data.write('\n')
            data.write('------------------------------------------------\n')
        data.close()


          
            

            

            


    


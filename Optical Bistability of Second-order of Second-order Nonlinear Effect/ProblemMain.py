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
    def PlotRelation(self,E_range,E_step,Option):
        "The main function"
        E_N=int((E_range[1]-E_range[0])//E_step)
        E_list=np.linspace(E_range[0],E_range[1],E_N)
        self.Result_out=np.zeros([3,E_N])
        self.Result_out[0]=E_list*E_list
        ps=ProblemSolver((self.g,[6,3,1,1],self.Delta,0.333))
        if (Option[0]==0)or(Option[0]==3):
            for i in range(0,E_N):
                Na=int(max(math.ceil(E_list[i]*E_list[i]+6*E_list[i]),4));
                Nb=int(Na//2);
                ps.SetParamaters((self.g,[Na,Nb,0,0],self.Delta,E_list[i]))
                (state,P_trans,rate)=ps.DefaultCalculator()
                if Option[1]==0:
                    self.Result_out[1][i]=P_trans
                if Option[1]==1:
                    self.Result_out[1][i]=rate
        if (Option[0]==1)or(Option[0]==3):
            Time=5
            for i in range(0,E_N):
                Na=int(max(math.ceil(E_list[i]*E_list[i]+6*E_list[i]),4));
                Nb=int(Na//2);
                ps.SetParamaters((self.g,[Na,Nb,0,0],self.Delta,E_list[i]))
                (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,Time,self.Pace)
                while (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])>self.accuracy):
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    Time=Time*2
                    (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,Time,self.Pace)
                if (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])<(self.accuracy/100)) and (Time>2) :
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    Time=Time//2
                if Option[1]==0:
                    self.Result_out[2][i]=P_trans
                if Option[1]==1:
                    self.Result_out[2][i]=rate

        self.PlotResult(Option)

    def PlotResult(self,Option):
        "Plot the result"
        fig, axes = plt.subplots(1, 1, figsize=(8,6))
        if (Option[0]==0)or(Option[0]==3):
            axes.plot(self.Result_out[0], self.Result_out[1], label="DefaultCalculator")
        if (Option[0]==1)or(Option[0]==3):
            axes.plot(self.Result_out[0],self.Result_out[2],label="AdvanceCalculator")
        axes.set_xlim(self.Result_out[0][0],self.Result_out[0][-1]);axes.legend(loc=0);
        axes.set_xlabel('P_in')
        if Option[1]==0:
           axes.set_ylabel('P_trans')
        if Option[1]==1:
           axes.set_ylabel('Output Rate')
        plt.show()

    def SaveData(self,name):
        "Save to file"
        data = open(name,'a')
        for i in range(0,size(self.Result_out)//3):
            data.write(str(self.Result_out[0][i])+' ')
            data.write(str(self.Result_out[1][i])+' ')
            data.write(str(self.Result_out[2][i])+' ')
            data.write('\n')
        data.write('------------------------------------------------\n')
        data.close()


          
            

            

            


    


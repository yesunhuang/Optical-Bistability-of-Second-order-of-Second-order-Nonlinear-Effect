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
        self.ntraj=500
    def ChangeSetting(self,Paramaters):
        "Change setting"
        (self.Delta,self.Pace,self.accuracy)=Paramaters

    def PlotRelation(self,E,g,Option=False):
        "The main function"
        E_list=E;g_list=g;
        self.Result_out=np.zeros([size(g_list),np.size(E_list),2])
        self.Result_out_m=np.zeros([size(g_list),np.size(E_list),2])
        ps=ProblemSolver((self.g,[6,3,1,1],self.Delta,0.333))

        for j in range(0,np.size(g_list)):
             Time=10
             for i in range(0,np.size(E_list)):
                n=0;
                Na=int(max(math.ceil(E_list[i]*E_list[i]+6*E_list[i]),4));
                Nb=int(Na//2);
                ps.SetParamaters((g_list[j],[Na,Nb,0,0],self.Delta,E_list[i]))
                (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,self.ntraj,Time,self.Pace)
                while (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])>self.accuracy):
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    n=n+1;
                    self.ntraj=self.ntraj*2
                    if(n>3):
                        Time=Time*2;
                    (output,P_trans,rate)=ps.AdvanceCalculator(self.rtol,self.atol,self.ntraj,Time,self.Pace)
                if (math.fabs((output.expect[0][int(-0.1//self.Pace)]-P_trans))/(E_list[i]*E_list[i])<(self.accuracy/100)) and (Time>2) :
                    #print(Time,output.expect[0][int(-0.1//self.Pace)],P_trans)
                    Time=Time//2;self.ntraj=self.ntraj//2
                self.Result_out[j][i][0]=P_trans
                self.Result_out[j][i][1]=output.expect[1][-1]
                print(P_trans,output.expect[1][-1])
                (self.Result_out_m[j][i][0],self.Result_out_m[j][i][1])=ps.MeanFeildCalculator();
        self.PlotResult(Option,E,g)


    def PlotResult(self,Option,E,g):
        "Plot the result"
        fig, axes = plt.subplots(1, 2, figsize=(16,8))
        if (not Option):
            axes[0].set_xlim(E[0]*E[0],E[-1]*E[-1]);axes[1].set_xlim(E[0]*E[0],E[-1]*E[-1])
            axes[0].set_xlabel(r'$P_{in}(E^2)$');axes[1].set_xlabel(r'$P_{in}(E^2)$')
            for j in range(0,np.size(g)):
                cor=self.randomcolor()
                axes[0].plot(E*E,self.Result_out[j,...,0],color=cor,linestyle='-',label='Q:g='+str(round(g[j],2)))
                axes[1].plot(E*E,self.Result_out[j,...,1],color=cor,linestyle='-',label='Q:g='+str(round(g[j],2)))
                axes[0].plot(E*E,self.Result_out_m[j,...,0],color=cor,linestyle='--',label='M:g='+str(round(g[j],2)))
                axes[1].plot(E*E,self.Result_out_m[j,...,1],color=cor,linestyle='--',label='M:g='+str(round(g[j],2)))
        else:
            axes[0].set_xlim(g[0]*g[0],g[-1]*g[-1]);axes[1].set_xlim(g[0]*g[0],g[-1]*g[-1]);
            for j in range(0,np.size(E)):
                axes[0].plot(g,self.Result_out[...,j,0],color=cor,linestyle='-',label='Q:'+r"$E^2= $"+str(round(E[0]*E[0],2)))
                axes[1].plot(g,self.Result_out[...,j,1],color=cor,linestyle='-',label='Q:'+ r"$E^2= $"+str(round(E[0]*E[0],2)))
                axes[0].plot(g,self.Result_out_m[...,j,0],color=cor,linestyle='--',label='M:'+r"$E^2= $"+str(round(E[0]*E[0],2)))
                axes[1].plot(g,self.Result_out_m[...,j,1],color=cor,linestyle='--',label='M:'+ r"$E^2= $"+str(round(E[0]*E[0],2)))
            axes[0].set_xlabel('g');axes[1].set_xlabel('g')
        axes[0].legend(loc=0); axes[1].legend(loc=0);
        axes[0].set_ylabel(r'$<a^{\dagger}a>$')
        axes[1].set_ylabel(r'$<b^{\dagger}b>$')
        plt.show()

    def SaveData(self,name,E,g):
        "Save to file"
        data = open(name,'a')
        for j in range(0,size(g)):
            data.write(str(g[j])+'\n')
            for i in range(0,size(E)):
                data.write(str(E[i])+' ')
                data.write(str(self.Result_out[j][i][0])+' ')
                data.write(str(self.Result_out[j][i][1]))
                data.write('\n')
            data.write('------------------------------------------------\n')
        data.close()

    def randomcolor(self):
        "get random color"
        colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        color = ""
        for i in range(6):
            color += colorArr[np.random.randint(0,14)]
        return "#"+color

          
            

            

            


    


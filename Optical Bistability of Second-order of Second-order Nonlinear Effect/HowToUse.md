# Guide
**First, please add it to your system path or open it in visual studio**  
## Class Demonstration
* This project contains two classes, but generally we just gonna use `OBF`.
### `OBF`
**The main class of this program.**
#### Function
##### `__init__()`
>Initialize the class and config the default setting.  
>(g=0.333,Delta=[0.8,1.6],accuracy=0.0001,Pace=0.001,rtol=1e-6,atol=1e-8)  

**All the paramaters are in unit of Kappa_A(The total decay rate of mode A)**  

|Paramater|Type|Description|
|----|----|----|
|g|float|cavity constant|
|Delta|float[DeltaA,DeltaB]|Detuning of each cavity mode from the laser frequency|
|accuray|float|The accuracy used to calculate steady state through `mesolve()`|
|Pace|float|The step of `t_list` used in `mesolve`|
|rtol|float|Relative tolerance of the solver `mesolve()` |
|atol|float|Absolute tolerance of the solver `mesolve()`|
>Please refer to the further demonstration below.
##### `ChangeSetting(Paramaters)`
This is used to change the default settings.
`Paramaters=(g,Delta,Pace,accuracy)`
##### `PlotRevolution(E,N,Time)`
Print out the calculation result under certain value E and plot the revolution calculated by `mesolve()`

|Paramater|Type|Description|
|----|----|----|
|E|float|Amplitude of the electric field of the driving laser|
|N|int[Na,Nb,init_Na,init_Nb]|The max photons numbers of mode a and b, and also the initial value of photon numbers|
|Time|float|Revolution time|

##### `PlotRelation(E_range,E_step,Option)`
Plot the *P_trans* or *Output_rate* as function of *P_in*

|Paramater|Type|Description|
|----|----|----|
|E_range|float[start,end]|Range of amplitude of the electric field of the driving laser|
|E_step|float|Step of `E_list`|
|Option|int[solver,resultValue]|`solver=0(steadystate()) or 1(mesolve()) or 3(both)` `resultValue=0(P_trans) or 1(Output_rate)`|

#### `PlotResult(Option)`
Plot the result stored in calculated by `PlotRelation()`. It will be called automatically by `PlotRelation()` or you can also use it manually to check the result.

The paramater `Option` is the same as the above one.

#### `SaveData(name)`
Store the data calculated by `PlotRelation()` in a specific file.

|Paramater|Type|Description|
|----|----|----|
|name|string|Data file's name(Path also)|

### `ProblemSolver`
**A tool class of this program**  
Since we won't use it generally, we omit the description. Please refer to the code if u r interested in it.
It have two calculator, the default one(using `steadystate`) and the advanced one(using `mesolve()`)    

## Example
The example below will show u how to use this program.

### First step
``` python
from ProblemMain import *
```
``` python
obf=OBF()
```
``` python
obf.ChangeSetting((0.333,[0.8,1.6],0.001,0.0001))
#Do not use this method if you wanna use default setting
```
### Calculate the revolution of specific 'E'
``` python
obf.PlotRevolution(0.106,[8,4,2,1],10)
```
### Calculate `P_trans` as function of 'P_in' and save it
``` python
obf.PlotRelation([0.333,2],0.1,[3,0])
#Sincerely recommend using the advanced calculator 
#which is much more faster than the default one.
```
``` python
obf.SaveData('Data1.dat')
```
### Calculate `Output_rate` as function of 'P_in'
``` python
obf.PlotRelation([0.333,2],0.1,[3,1])
```



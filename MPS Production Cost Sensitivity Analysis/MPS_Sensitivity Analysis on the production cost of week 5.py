from pyomo.environ import*
import matplotlib.pyplot as plt

Model = ConcreteModel()

#Parameters

T = 12

Tp = 3

k = 5

d = [[1000 , 1000 , 1000 , 1000 , 1200 , 1200 , 1200 , 1200 , 1100 , 1100 , 1100 , 1100],
     [1000 , 1000 , 1000 , 1000 , 1200 , 1200 , 1200 , 1200 , 1100 , 1100 , 1100 , 1100],
     [2000 , 2000 , 2000 , 2000 , 2400 , 2400 , 2400 , 2400 , 2200 , 2200 , 2200 , 2200],
     [4500 , 4500 , 4500 , 4500 , 5400 , 5400 , 5400 , 5400 , 4950 , 4950 , 4950 , 4950],
     [1500 , 1500 , 1500 , 1500 , 1800 , 1800 , 1800 , 1800 , 1650 , 1650 , 1650 , 1650]]

Xstar = [49500 , 37500 , 44000]

Ostar = [54000 , 6000 , 32000]

Istar = [10500 , 0 , 0]

Capr = 6*24000

Cap = []

Cap1 = [(Capr + i)/4 for i in Ostar]

for i in Cap1:
    Cap.extend([i,i,i,i])

I0 = [150 , 200 , 200 ,  250 , 200]

Cr = [160000,160000,160000,160000,168000,168000,168000,168000,177600,177600,177600,177600]

h = [2500,2500,2500,2500,2625,2625,2625,2625,2750,2750,2750,2750]

b = 4

miu = 0.2

#Index

Model.k = RangeSet(k)

Model.t = RangeSet(T)

Model.s = RangeSet(0,T-1)

Cs = {}
for i in range(len(Cr)): Cs[i] = Cr[i]

# Parameter for Sensitivity analysis

Model.CR = Param(Model.s , initialize = Cs , mutable = True)

#Variables

Model.Y = Var(Model.k , Model.t , within = NonNegativeIntegers)

Model.O = Var(Model.k , Model.t , within = NonNegativeIntegers)

Model.I = Var(Model.k , Model.t , within = NonNegativeIntegers)

#Objective Function

Model.objective = Objective(expr = sum(Model.CR[t-1]*Model.Y[k,t] + h[t-1]*Model.I[k,t]
                                      for k in Model.k for t in Model.t) , sense = minimize)

#Constraints

Model.St = ConstraintList()

for k in Model.k:
    Model.St.add(I0[k-1] + Model.Y[k,1] - Model.I[k,1] == d[k-1][0])

for k in Model.k:
    for t in range(2,T+1):
        Model.St.add(Model.I[k,t-1] + Model.Y[k,t] - Model.I[k,t] == d[k-1][t-1])

for t in Model.t:
    Model.St.add(sum(b*Model.Y[k,t] for k in Model.k) <= Cap[t-1])

for t in Model.t:
    Model.St.add(sum(b*Model.Y[k,t] for k in Model.k) >= (1 - miu)*Cap[t-1])

for T in range(1,Tp+1):
    Model.St.add(sum(Model.Y[k,t] for k in Model.k for t in range(4*(T-1)+1 , 4*T+1)) == Xstar[T-1])
    
for T in range(1,Tp+1):
    Model.St.add(sum(Model.I[k,4*T] for k in Model.k) == Istar[T-1])

X = []

Y = []

for i in range(10):
    Model.CR[4] = Model.CR[4] + 100
    Solver = SolverFactory("cplex")
    Solver.solve(Model)
    X.append(value(Model.CR[4]))
    Y.append(value(Model.objective)/pow(10,9))
    print(value(Model.CR[4]), ':',value(Model.objective))
    print("---------------------")
'''    for k in Model.k:
        print(value(Model.Y[k,5])) '''

plt.plot(X , Y)
plt.title("Sensitivity Analysis on production cost of week 5")
plt.xlabel("Production cost in Tomans per Package")
plt.ylabel("Cost in Billions")
#Model.pprint()

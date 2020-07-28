#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#coefficients and parameters
Plant=["F1","F2"]
Warehouse=["WH1","WH2"]
Wholesaler=["WS1","WS2","WS3","WS4"]

supply={}
supply["F1"]=400
supply["F2"]=250

demand={}
demand["WS1"] = 200
demand["WS2"] = 100
demand["WS3"] = 150
demand["WS4"] = 200

#transportation cost from plant to warehouse
cost_to_warehouse={
    ("F1","WH1"):40,
    ("F1","WH2"):35,
    ("F2","WH2"):25,
    ("F2","WH1"):0,
}

#max capacity from F1 TO WH1
capacity_w1={
    ("F1","WH1"):250,
}

#capacity of unused plant
capacity_Plant={
    ("F2","WH1"):0,
}

#capacity of unused warehouse1
capacity_Warehouse1={
    ("WH1","WS3"):0,
    ("WH1","WS4"):0,   
}
#capacity of unused warehouse2
capacity_Warehouse2={
    ("WH2","WS1"):0, 
}

#transportation cost from warehouse to wholesaler
cost_to_wholesaler={
    ("WH1","WS1"):60,
    ("WH1","WS2"):35,
    ("WH1","WS3"):0,
    ("WH1","WS4"):0,
    ("WH2","WS1"):0,
    ("WH2","WS2"):55,
    ("WH2","WS3"):50,
    ("WH2","WS4"):65,
    
}

from gurobipy import * 
model = Model("Network Flow")

#decision variables
X={}
Y={}

for i in Plant: 
    for j in Warehouse:
        X[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)

for i in Warehouse: 
    for m in Wholesaler:
        Y[i,m] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)

        
model.modelSense = GRB.MINIMIZE                   
model.update()

#demand constraints
for m in Wholesaler:    
    model.addConstr(quicksum(Y[i,m] for i in Warehouse)== demand[m]) 
    
#maximum flow contraints
for i in Plant:
    for j in Warehouse:
        model.addConstr(X['F1','WH1'] <= capacity_w1['F1','WH1']) 

#Unsed plants and warehouse constraints
    #from factory2 to Warehouse
for F2 in Plant:
    for WH1 in Warehouse:
        model.addConstr(X["F2","WH1"] <= capacity_Plant["F2","WH1"])
            
    #from warehouse1 to wholesaler3       
for WS3 in Wholesaler:
    for WH1 in Warehouse:
        model.addConstr(Y["WH1","WS3"] <= capacity_Warehouse1["WH1","WS3"])  
        
    #from warehouse1 to wholesaler4      
for WS4 in Wholesaler:
    for WH1 in Warehouse:
        model.addConstr(Y["WH1","WS4"] <= capacity_Warehouse1["WH1","WS4"])  
        
     #from warehouse2 to wholesaler1           
for WH2 in Warehouse:
    for WS1 in Wholesaler:
        model.addConstr(Y["WH2","WS1"] <= capacity_Warehouse2["WH2","WS1"])  

# maximum capacity 
for i in Plant:    
    model.addConstr(quicksum(X[i,j] for j in Warehouse)<= supply[i] )  

# Equilibrium 
for j in Warehouse:
    model.addConstr(quicksum(X[i,j] for i in Plant) - quicksum(Y[j,m] for m in Wholesaler) == 0) 
    
#objective function
objective = quicksum(cost_to_warehouse[i,j]*X[i,j] for j in Warehouse for i in Plant)+ quicksum(cost_to_wholesaler[i,m]*Y[i,m] for m in Wholesaler for i in Warehouse)

model.setObjective(objective)
model.optimize()

#Printing outputs
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print ("--- Quantity (Production to Warehouse)---")
    for i in Plant: 
        for j in Warehouse:
            print ( i, j, X[i,j].x)
    
    print ("--- Quantity (Warehouse to Wholesaler)---")
    for i in Warehouse: 
        for j in Wholesaler:
            print (i, j, Y[i,j].x)


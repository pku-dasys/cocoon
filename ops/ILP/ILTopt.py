import gurobipy as gp
import numpy

class ILPopt():
    """
    An integer linear programming (ILP) solver based on GUROBI
    """

    def __init__(self, num_vars, obj, constrs=[]):
        """
        Params:
            - num_val: # of variables
            - obj: tuple ("x[0] + 2 * x[1] - 4 * x[2]", "min/max")
            - constr: list of tuples (expr, op, val)
                - e.g. [("2 * x[0] - 3 * x[1]**2 + 6 * x[2]", ">=", "32"), ...]
                - variables should only be x[0], x[1], ..., x[num_val - 1]
        """
        self.model = gp.Model()
        self.num_vars = num_vars
        self.obj = obj
        self.constrs = constrs
    
    def optimize(self):

        x = self.model.addVars(self.num_vars, vtype=gp.GRB.INTEGER)  # Integers
        self.vars = x

        # Set objective
        if self.obj[1] == "min":
            self.model.setObjective(eval(self.obj[0]), gp.GRB.MINIMIZE)
        elif self.obj[1] == "max":   
            self.model.setObjective(eval(self.obj[0]), gp.GRB.MAXIMIZE)
        else:
            raise Exception("obj[1] should be among 'max' and 'min'")

        # Set constraints
        for constr in self.constrs:
            if constr[1] == ">":
                self.model.addConstr(eval(constr[0]) > eval(constr[2]))
            elif constr[1] == ">=":
                self.model.addConstr(eval(constr[0]) >= eval(constr[2]))
            elif constr[1] == "<":
                self.model.addConstr(eval(constr[0]) < eval(constr[2]))
            elif constr[1] == "<=":
                self.model.addConstr(eval(constr[0]) <= eval(constr[2]))
            else:
                raise Exception("The constraint operator should be among '>', '>=', '<', '<='")
        
        self.model.optimize()
    
    def print_result(self):
        print("############## Summarize Results ###############")
        print(f"Optimal objective value: {self.model.objVal}")
        print("Solution values:")
        for i in range(self.num_vars):
            print(f"x[{i}]={self.vars[i].X}")

        
        
        

        






        


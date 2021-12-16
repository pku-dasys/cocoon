from ILTopt import ILPopt

if __name__ == "__main__":

    print("Problem 1: Quadratic equation minimal\n")
    """
    Find the minimal of x^2 + 2 * y^2 + 15.8 * x - 5 * y + 3.2,  x and y are integers
    """
    opt1 = ILPopt(2, obj=("x[0]**2 + 2 * x[1]**2 - 15.8 * x[0] - 5 * x[1] + 3.2", "min"))
    opt1.optimize()
    opt1.print_result()


    print("Problem 2: Knapsack problem\n")
    """
    N (N=5) kinds of items, with weights (3.8, 5.5, 3.2, 4, 6.5) and values (3.5, 7, 4.5, 4.8, 8.5).
    The volume of knapsack is 15. How can we maximize the value?
    """
    obj = ("3.5 * x[0] + 7 * x[1] + 4.5 * x[2] + 4.8 * x[3] + 8.5 * x[4]", "max")
    constrs = [
        ("x[0]", ">=", "0"),
        ("x[1]", ">=", "0"),
        ("x[2]", ">=", "0"),
        ("x[3]", ">=", "0"),
        ("x[4]", ">=", "0"),
        ("3.8 * x[0] + 5.5 * x[1] + 3.2 * x[2] + 4 * x[3] + 6.5 * x[4]", "<=", "15")
    ]
    opt2 = ILPopt(5, obj, constrs)
    opt2.optimize()
    opt2.print_result()
#!/usr/bin/env python3

from src import xmastree as xt
import cma
import math
import random
from functools import partial

def main():

    N_trees = 20
    N_tries = 3
    radius = 20.0
    sigma0 = 3

    placed_trees = xt.ChristmasTrees(trees=[xt.ChristmasTree(0,0,45)])
    placed_trees.get_solution().to_csv(f"results/{placed_trees.size}-tree-configuration.csv")
    placed_trees.save_config_to_pdf(f"results/{placed_trees.size}-tree-configuration.pdf")

    objective_for_cma = partial(xt.constrained_objective, placed_trees=placed_trees)

    for i in range(N_trees-1):
        best_x = None
        best_cost_value = 1e20
        for _ in range(N_tries):
            angle = xt.generate_weighted_angle()
            vx = math.cos(angle)
            vy = math.sin(angle)
            x0 = [radius * vx,radius * vy,random.uniform(0, 2*math.pi)]
            x, es = cma.fmin2(objective_for_cma, x0, sigma0, options={'verbose': -9})
            if (objective_for_cma(x) < best_cost_value):
                best_cost_value = objective_for_cma(x)
                best_x = x
        print(i)
        print(best_x)
        print(objective_for_cma(best_x))
        placed_trees.append_tree(xt.ChristmasTree(best_x[0],best_x[1],best_x[2]*180/math.pi))
        placed_trees.get_solution().to_csv(f"results/{placed_trees.size}-tree-configuration.csv")
        placed_trees.save_config_to_pdf(f"results/{placed_trees.size}-tree-configuration.pdf")


if __name__ == "__main__":
    main()
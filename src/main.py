import xmastree as xt

trees = xt.ChristmasTrees(4)

trees.plot()

trees.get_solution().to_csv('../data/configuration_4tree.csv')

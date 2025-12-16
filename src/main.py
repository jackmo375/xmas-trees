import xmastree as xt
from shapely import affinity
from shapely.ops import unary_union
from shapely.strtree import STRtree
from optimization import optimize
from decimal import Decimal
SCALE_FACTOR = Decimal('1e15')
import cma
import random

def translate_tree(tree, delta):
    tree.center_x = float(tree.center_x) + delta[0]
    tree.center_y = float(tree.center_y) + 0
    tree.polygon = affinity.translate(
        tree.polygon,
        xoff=float(tree.center_x * 1e15),
        yoff=float(tree.center_y * 1e15),
    )

def rotate_tree(tree, angle):
    tree.angle = (float(tree.angle) + angle) % 360.0
    tree.polygon = affinity.rotate(
        tree.polygon, 
        angle, 
        'center')

def overlap_present(placed_trees, tree_to_place):
    placed_polygons = [p.polygon for p in placed_trees]
    candidate_poly = tree_to_place.polygon
    tree_index = STRtree(placed_polygons)
    possible_indices = tree_index.query(candidate_poly)
    if any((candidate_poly.intersects(placed_polygons[i]) and not candidate_poly.touches(placed_polygons[i])) for i in possible_indices):
        return(True)
    return(False)

def get_side_length(trees, tree):
        all_polygons = [t.polygon for t in trees]
        all_polygons.append(tree.polygon)
        bounds = unary_union(all_polygons).bounds
        minx = bounds[0] / 1e15
        miny = bounds[1] / 1e15
        maxx = bounds[2] / 1e15
        maxy = bounds[3] / 1e15
        width = maxx - minx
        height = maxy - miny
        # this forces a square bounding using the largest side
        return(float(max(width, height)))

def generate_weighted_angle():
    """
    Generates a random angle with a distribution weighted by abs(sin(2*angle)).
    This helps place more trees in corners, and makes the packing less round.
    """
    while True:
        angle = random.uniform(0, 2 * math.pi)
        if random.uniform(0, 1) < abs(math.sin(2 * angle)):
            return angle

def cost_function(x):
    tree_to_place = xt.ChristmasTree(x[0], x[1], x[2]*180/math.pi)
    if (overlap_present(placed_trees.trees, tree_to_place) == True):
        return 1e9
    return(get_side_length(placed_trees.trees, tree_to_place)**2)


N = 20
radius = 20.0
placed_trees = xt.ChristmasTrees(trees=[xt.ChristmasTree(0,0,45)])
sigma0 = 3
for _ in range(N):
    best_x = None
    best_cost_value = 1e20
    for _ in range(10):
        angle = generate_weighted_angle()
        vx = math.cos(angle)
        vy = math.sin(angle)
        x0 = [radius * vx,radius * vy,random.uniform(0, 2*math.pi)]
        x, es = cma.fmin2(cost_function, x0, sigma0, options={'verbose': -9})
        if (cost_function(x) < best_cost_value):
            best_cost_value = cost_function(x)
            best_x = x
    print(N)
    print(cost_function(best_x))
    placed_trees.append_tree(xt.ChristmasTree(best_x[0],best_x[1],best_x[2]*180/math.pi))

placed_trees.plot()


trees_updated = optimize(trees)

trees_updated.plot()

trees_updated.get_solution().to_csv('../data/configuration_4tree.csv')

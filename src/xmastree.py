import math
import random
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
from decimal import Decimal, getcontext

COLLISION_BUFFER_SCALE = 1.06

pd.set_option('display.float_format', '{:.12f}'.format)
getcontext().prec = 25
SCALE_FACTOR = Decimal('1e15')

class ChristmasTrees:
    # def __init__(self, num_trees):
    #     self.size = num_trees
    #     self.trees = initialize_trees(num_trees, existing_trees=None)
    def __init__(self, trees):
        self.trees = trees
        self.size = len(trees)

    def __iter__(self):
        return iter(self.trees)

    def append_tree(self,tree):
        self.trees.append(tree)
        self.size = self.size + 1

    def get_side_length(self):
        all_polygons = [t.polygon for t in self.trees]
        bounds = unary_union(all_polygons).bounds

        minx = Decimal(bounds[0]) / SCALE_FACTOR
        miny = Decimal(bounds[1]) / SCALE_FACTOR
        maxx = Decimal(bounds[2]) / SCALE_FACTOR
        maxy = Decimal(bounds[3]) / SCALE_FACTOR

        width = maxx - minx
        height = maxy - miny
        # this forces a square bounding using the largest side
        return(max(width, height))

    def get_configuration_plot(self):
        """Plots the arrangement of trees and the bounding square."""
        _, ax = plt.subplots(figsize=(6, 6))
        colors = plt.cm.viridis([i / self.size for i in range(self.size)])

        all_polygons = [t.polygon for t in self.trees]
        bounds = unary_union(all_polygons).bounds

        for i, tree in enumerate(self.trees):
            # Rescale for plotting
            x_scaled, y_scaled = tree.polygon.exterior.xy
            x = [Decimal(val) / SCALE_FACTOR for val in x_scaled]
            y = [Decimal(val) / SCALE_FACTOR for val in y_scaled]
            ax.plot(x, y, color=colors[i])
            ax.fill(x, y, alpha=0.5, color=colors[i])

        minx = Decimal(bounds[0]) / SCALE_FACTOR
        miny = Decimal(bounds[1]) / SCALE_FACTOR
        maxx = Decimal(bounds[2]) / SCALE_FACTOR
        maxy = Decimal(bounds[3]) / SCALE_FACTOR

        width = maxx - minx
        height = maxy - miny

        side_length = self.get_side_length()

        square_x = minx if width >= height else minx - (side_length - width) / 2
        square_y = miny if height >= width else miny - (side_length - height) / 2
        bounding_square = Rectangle(
            (float(square_x), float(square_y)),
            float(side_length),
            float(side_length),
            fill=False,
            edgecolor='red',
            linewidth=2,
            linestyle='--',
        )
        ax.add_patch(bounding_square)

        padding = 0.5
        ax.set_xlim(
            float(square_x - Decimal(str(padding))),
            float(square_x + side_length + Decimal(str(padding))))
        ax.set_ylim(float(square_y - Decimal(str(padding))),
                    float(square_y + side_length + Decimal(str(padding))))
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        plt.title(f'{self.size} Trees: {side_length:.12f}')
        return(plt)

    def plot(self):
        plt = self.get_configuration_plot()
        plt.show()
        plt.close()

    def save_config_to_pdf(self, filename):
        plt = self.get_configuration_plot()
        plt.savefig(filename)
        plt.close()

    def get_solution(self):
        tree_data = []
        index = [f'{self.size:03d}_{t}' for t in range(self.size)]
        for tree in self.trees:
            tree_data.append([tree.center_x, tree.center_y, tree.angle])
        cols = ['x', 'y', 'deg']
        submission = pd.DataFrame(
            index=index, 
            columns=cols, 
            data=tree_data).rename_axis('id')
        for col in cols:
            submission[col] = submission[col].astype(float).round(decimals=6)
        for col in submission.columns:
            submission[col] = 's' + submission[col].astype('string')
        return(submission)

class ChristmasTree:
    """Represents a single, rotatable Christmas tree of a fixed size."""

    def __init__(self, center_x='0', center_y='0', angle='0'):
        """Initializes the Christmas tree with a specific position and rotation."""
        self.center_x = Decimal(center_x)
        self.center_y = Decimal(center_y)
        self.angle = Decimal(angle)

        trunk_w = Decimal('0.15')
        trunk_h = Decimal('0.2')
        base_w = Decimal('0.7')
        mid_w = Decimal('0.4')
        top_w = Decimal('0.25')
        tip_y = Decimal('0.8')
        tier_1_y = Decimal('0.5')
        tier_2_y = Decimal('0.25')
        base_y = Decimal('0.0')
        trunk_bottom_y = -trunk_h

        initial_polygon = Polygon(
            [
                # Start at Tip
                (Decimal('0.0') * SCALE_FACTOR, tip_y * SCALE_FACTOR),
                # Right side - Top Tier
                (top_w / Decimal('2') * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
                (top_w / Decimal('4') * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
                # Right side - Middle Tier
                (mid_w / Decimal('2') * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
                (mid_w / Decimal('4') * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
                # Right side - Bottom Tier
                (base_w / Decimal('2') * SCALE_FACTOR, base_y * SCALE_FACTOR),
                # Right Trunk
                (trunk_w / Decimal('2') * SCALE_FACTOR, base_y * SCALE_FACTOR),
                (trunk_w / Decimal('2') * SCALE_FACTOR, trunk_bottom_y * SCALE_FACTOR),
                # Left Trunk
                (-(trunk_w / Decimal('2')) * SCALE_FACTOR, trunk_bottom_y * SCALE_FACTOR),
                (-(trunk_w / Decimal('2')) * SCALE_FACTOR, base_y * SCALE_FACTOR),
                # Left side - Bottom Tier
                (-(base_w / Decimal('2')) * SCALE_FACTOR, base_y * SCALE_FACTOR),
                # Left side - Middle Tier
                (-(mid_w / Decimal('4')) * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
                (-(mid_w / Decimal('2')) * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
                # Left side - Top Tier
                (-(top_w / Decimal('4')) * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
                (-(top_w / Decimal('2')) * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
            ]
        )
        rotated = affinity.rotate(initial_polygon, float(self.angle), origin=(0, 0))
        self.polygon = affinity.translate(rotated,
                                          xoff=float(self.center_x * SCALE_FACTOR),
                                          yoff=float(self.center_y * SCALE_FACTOR))

def constrained_objective(x, placed_trees):
    tree_to_place = ChristmasTree(x[0], x[1], x[2]*180/math.pi)
    return(objective(placed_trees, tree_to_place) + overlap_constraint(placed_trees, tree_to_place))

def objective(placed_trees, tree_to_place):
    return(get_side_length(placed_trees.trees, tree_to_place)**2)

def overlap_constraint(placed_trees, tree_to_place):
    rescale_value = COLLISION_BUFFER_SCALE
    placed_polygons = [affinity.scale(p.polygon, rescale_value, rescale_value, origin=p.polygon.centroid) for p in placed_trees]
    candidate_poly = affinity.scale(tree_to_place.polygon, rescale_value, rescale_value, origin=tree_to_place.polygon.centroid)
    tree_index = STRtree(placed_polygons)
    possible_indices = tree_index.query(candidate_poly)
    if any((candidate_poly.intersects(placed_polygons[i]) and not candidate_poly.touches(placed_polygons[i])) for i in possible_indices):
        return(1e9)
    return(0)

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


def get_trees_from_df(submission):
    # remove the leading 's' from submissions
    data_cols = ['x', 'y', 'deg']
    submission = submission.astype(str)
    for c in data_cols:
        if not submission[c].str.startswith('s').all():
            raise ParticipantVisibleError(f'Value(s) in column {c} found without `s` prefix.')
        submission[c] = submission[c].str[1:]

    # enforce value limits
    limit = 100
    bad_x = (submission['x'].astype(float) < -limit).any() or \
            (submission['x'].astype(float) > limit).any()
    bad_y = (submission['y'].astype(float) < -limit).any() or \
            (submission['y'].astype(float) > limit).any()
    if bad_x or bad_y:
        raise ParticipantVisibleError('x and/or y values outside the bounds of -100 to 100.')
    placed_trees = []
    for _, row in submission.iterrows():
        placed_trees.append(ChristmasTree(row['x'], row['y'], row['deg']))
    return(ChristmasTrees(placed_trees))
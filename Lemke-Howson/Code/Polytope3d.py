from manim import *
import numpy as np
from itertools import combinations


payoff_data = [
    [(1, 5), (5, 2)],
    [(3, 3), (4, 8)],
    [(4, 8), (0, 4)]
]

B = np.array([[cell[1] for cell in row] for row in payoff_data], dtype=float)
m, n = B.shape
# Numerical tolerances for floating-point comparisons in geometric calculations
TOL_DET = 1e-9 # Minimum determinant magnitude
TOL_FEAS = 1e-7 # Margin to verify if a point satisfies all linear inequalities
TOL_DUP = 1e-6 # Distance threshold
TOL_TIGHT = 1e-6 # Residual threshold

# Constraints for inequality system (A*x <= b)

def build_constraints(B):
    m, n = B.shape
    constraints = []
    for i in range(m):
        a = np.zeros(m)
        a[i] = -1.0
        constraints.append((a, 0.0))
    for j in range(n):
        constraints.append((B[:, j].copy(), 1.0))
    return constraints

# Finds all valid 3D polytope vertices by solving d-combinations of hyperplanes (A*x = b)
def enumerate_vertices(constraints, dim):
    vertices = []
    tight_sets = []
    for combo in combinations(range(len(constraints)), dim):
        A = np.array([constraints[i][0] for i in combo])
        b = np.array([constraints[i][1] for i in combo])
        if abs(np.linalg.det(A)) < TOL_DET:
            continue
        x = np.linalg.solve(A, b)
        # Verify that the vertex satisfies all constraints
        feasible = all(a @ x <= bb + TOL_FEAS for a, bb in constraints)
        if not feasible:
            continue
        if any(np.allclose(v, x, atol=TOL_DUP) for v in vertices):
            continue
        vertices.append(x)
        tight = frozenset(
            i for i, (a, bb) in enumerate(constraints) if abs(a @ x - bb) < TOL_TIGHT
        )
        tight_sets.append(tight)
    return vertices, tight_sets

def build_faces(vertices, tight_sets, constraints):
    faces = []
    for ci in range(len(constraints)):
        idxs = [vi for vi, ts in enumerate(tight_sets) if ci in ts]
        if len(idxs) < 3:
            continue
        pts = np.array([vertices[vi] for vi in idxs])
        centroid = pts.mean(axis=0)
        normal = constraints[ci][0]
        normal = normal / np.linalg.norm(normal)
        seed = np.array([1.0, 0.0, 0.0]) if abs(normal[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        u = np.cross(normal, seed)
        u /= np.linalg.norm(u)
        v = np.cross(normal, u)
        angles = [np.arctan2((p - centroid) @ v, (p - centroid) @ u) for p in pts]
        order = np.argsort(angles)
        faces.append([idxs[k] for k in order])
    return faces

def vertex_index_by_tight(tight_sets, wanted):
    wanted = frozenset(wanted)
    for i, ts in enumerate(tight_sets):
        if ts == wanted:
            return i
    raise ValueError(f"no vertex with tight set {wanted}")

# Polytope Geometry
constraints = build_constraints(B)
vertex_arrs, tight_sets = enumerate_vertices(constraints, m)
faces_list = build_faces(vertex_arrs, tight_sets, constraints)

# Scale & Center Geometry
SCALE = 22.0
scaled_pts = [SCALE * np.array(v) for v in vertex_arrs]

min_b = np.min(scaled_pts, axis=0)
max_b = np.max(scaled_pts, axis=0)
bbox_center = (min_b + max_b) / 2.0

vertex_coords = [pt - bbox_center for pt in scaled_pts]

# Traversal 
traversal_labels = [
    frozenset({0, 1, 2}),  # Origin
    frozenset({1, 2, 3}),  # Step 1
    frozenset({2, 3, 4}),  # Step 2
    frozenset({0, 3, 4}),  # Equilibrium
]
traversal_indices = [vertex_index_by_tight(tight_sets, lbl) for lbl in traversal_labels]


class LemkeHowsonPolytope3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-52 * DEGREES, zoom=1.05)

        # floor grid
        min_z = min(v[2] for v in vertex_coords)
        floor = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=20,
            y_length=20,
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1.2,
                "stroke_opacity": 0.2,
            },
            axis_config={"stroke_opacity": 0},
        )
        floor.shift(OUT * (min_z - 0.02))

        # edges
        EDGE_COLOR = WHITE
        edges_group = VGroup()
        edge_map = {}

        for f_indices in faces_list:
            n_v = len(f_indices)
            for i in range(n_v):
                u, v = f_indices[i], f_indices[(i + 1) % n_v]
                key = tuple(sorted((u, v)))
                if key not in edge_map:
                    edge = Line3D(
                        start=vertex_coords[u],
                        end=vertex_coords[v],
                        thickness=0.038,
                        color=EDGE_COLOR
                    )
                    edges_group.add(edge)
                    edge_map[key] = edge

        #vertices
        vertices_group = VGroup()
        vertex_nodes = []
        for pt in vertex_coords:
            node = Sphere(center=pt, radius=0.16, resolution=(16, 16))
            node.set_color(WHITE)
            vertices_group.add(node)
            vertex_nodes.append(node)

        
        self.add(floor)
        self.play(Create(edges_group), FadeIn(vertices_group), run_time=1.2)
        self.wait(0.3)

        
        HIGHLIGHT_COLOR = "#FF2D55" 
        start_idx = traversal_indices[0]
        start_vertex_pos = np.array(vertex_coords[start_idx])
        
        # Spawn off-screen to the far left
        far_left_pos = start_vertex_pos + LEFT * 12 + UP * 2.5 + OUT * 1.5

        tracer = Sphere(
            center=far_left_pos, 
            radius=0.18, 
            resolution=(16, 16)
        )
        tracer.set_color(HIGHLIGHT_COLOR)
        self.add(tracer)

        # fly-in to origin vertex
        self.play(
            tracer.animate.move_to(start_vertex_pos),
            run_time=1.2,
            rate_func=smooth
        )
        
        # Color update
        vertex_nodes[start_idx].set_color(HIGHLIGHT_COLOR)
        self.wait(0.3)

        # red trail traversal
        for i in range(len(traversal_indices) - 1):
            u_idx = traversal_indices[i]
            v_idx = traversal_indices[i + 1]
            
            start_pos = np.array(vertex_coords[u_idx])
            target_pos = np.array(vertex_coords[v_idx])
            target_node = vertex_nodes[v_idx]

            # Red trail segment
            red_trail = Line3D(
                start=start_pos, 
                end=start_pos + 0.001 * (target_pos - start_pos), 
                thickness=0.040, 
                color=HIGHLIGHT_COLOR
            )
            self.add(red_trail)

            def update_step(m, alpha):
                curr_pos = (1 - alpha) * start_pos + alpha * target_pos
                tracer.move_to(curr_pos)
                
                if alpha > 0.005:
                    updated_segment = Line3D(
                        start=start_pos, 
                        end=curr_pos, 
                        thickness=0.040, 
                        color=HIGHLIGHT_COLOR
                    )
                    red_trail.become(updated_segment)

            self.play(
                UpdateFromAlphaFunc(tracer, update_step),
                run_time=1.2,
                rate_func=smooth
            )
            
            
            target_node.set_color(HIGHLIGHT_COLOR)
            self.wait(0.2)

        self.wait(2)
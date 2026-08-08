
from manim import*
from FixedText import*
from manim.utils.rate_functions import ease_in_out_sine
from manim.utils.rate_functions import ease_out_cubic
import math
import numpy as np
from manim.typing import Point3DLike


class CustomLine3D(Line3D):
    def __init__(
        self,
        start: Point3DLike = LEFT,
        end: Point3DLike = RIGHT,
        thickness: float = 0.02,
        color: ParsableManimColor | None = None,
        resolution: int | tuple[int, int] = 24,
        **kwargs: Any,
    ):
        super().__init__(start=start, end=end, thickness=thickness, color=color, resolution=resolution, **kwargs)
        self.cl_settings = kwargs
        self.cl_color = color

    def change_end_points(
        self, start: Point3DLike, end: Point3DLike
    ) -> None:
        self.set_start_and_end_attrs(start, end, **self.cl_settings)
        self.set_color(self.cl_color)


class Test(ThreeDScene):

    def construct(self):
        line = CustomLine3D((0, 0, 0), (1, 0, 0), color=YELLOW, thickness=0.05)
        self.add(line)
        self.play(line.animate.change_end_points((0, 1, 0), (2, 0, 0)))
        self.wait()

class PolytopeTraversal(ThreeDScene):

    def camera_pos(self):
        c = self.camera._frame_center.get_center()
        d = self.camera.get_focal_distance()
        phi = self.camera.get_phi()
        theta = self.camera.get_theta()

        return d * np.array([math.sin(phi) * math.cos(theta), math.sin(phi) * math.sin(theta), math.cos(phi)]) + c

    def project_point(self, point, distance=5):
        p = self.camera_pos()
        R = self.camera.generate_rotation_matrix()

        print(R)

        point = np.linalg.inv(R) @ (point - p)
        point = point / point[2] * distance

        return p + R @ point

    def project_mobject(self, mobject, distance=5):
        return mobject.animate.move_to(self.project_point(mobject.get_center(), distance))

    def project_line3d(self, line, distance=5):
        s = self.project_point(line.get_start(), distance)
        e = self.project_point(line.get_end(), distance)

        return line.animate.change_end_points(s, e)
        # return line.animate.set_points_by_ends(s, e)


    def construct(self):

        self.camera.should_apply_shading = False

        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.92,
        )
 
        title = FixedText(
            "Polytope Traversal",
            font_size=42,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP, buff=0.3)
 
        self.add_fixed_in_frame_mobjects(title)
 
        self.play(
            FadeIn(title, shift=DOWN * 0.12),
            run_time=0.7,
        )
 
        # payoff graph
 
        axes = Axes(
            x_range=[0, 1.01, 0.25],
            y_range=[0, 6.1, 1],
            x_length=6.4,
            y_length=4.9,
            tips=False,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_numbers": False,
            },
        )
 
        axes.move_to(DOWN * 0.65)
        axes.shift(OUT * 0.02)
 
        p_label = MathTex(
            "p",
            font_size=30,
        ).next_to(
            axes.x_axis.get_end(),
            RIGHT,
            buff=0.12,
        )
 
        zero_label = MathTex(
            "0",
            font_size=24,
        ).next_to(
            axes.c2p(0, 0),
            DOWN + LEFT,
            buff=0.08,
        )
 
        one_label = MathTex(
            "1",
            font_size=24,
        ).next_to(
            axes.c2p(1, 0),
            DOWN,
            buff=0.08,
        )
 
        a1_line = axes.plot(
            lambda p: 5 - 4 * p,
            x_range=[0, 1],
            color=WHITE,
            stroke_width=3.5,
        )
 
        a2_line = axes.plot(
            lambda p: 4 - p,
            x_range=[0, 1],
            color=WHITE,
            stroke_width=3.5,
        )
 
        a3_line = axes.plot(
            lambda p: 4 * p,
            x_range=[0, 1],
            color=WHITE,
            stroke_width=3.5,
        )
 
        a1_label = FixedText(
            "A1",
            font_size=31,
            weight=BOLD,
            color=RED,
        ).next_to(
            axes.c2p(1, 1),
            RIGHT,
            buff=0.2,
        )
 
        a2_label = FixedText(
            "A2",
            font_size=31,
            weight=BOLD,
            color=RED,
        ).next_to(
            axes.c2p(1, 3),
            RIGHT,
            buff=0.2,
        )
 
        a3_label = FixedText(
            "A3",
            font_size=31,
            weight=BOLD,
            color=RED,
        ).next_to(
            axes.c2p(1, 4),
            RIGHT,
            buff=0.2,
        )
 
        graph_labels = VGroup(
            p_label,
            zero_label,
            one_label,
            a1_label,
            a2_label,
            a3_label,
        )
 
        graph_labels.shift(OUT * 0.04)
 
        intersection_12 = Dot3D(
            point=axes.c2p(1 / 3, 11 / 3) + OUT * 0.07,
            radius=0.065,
            color=GREEN
        )
 
        intersection_13 = Dot3D(
            point=axes.c2p(5 / 8, 5 / 2) + OUT * 0.07,
            radius=0.06,
            color=GREEN
        )
 
        intersection_23 = Dot3D(
            point=axes.c2p(4 / 5, 16 / 5) + OUT * 0.07,
            radius=0.065,
            color=GREEN
        )
 
        intersections = VGroup(
            intersection_12,
            intersection_13,
            intersection_23,
        )

 
        self.play(
            Create(axes),
            run_time=0.75,
        )
 
        self.play(
            LaggedStart(
                Create(a1_line),
                Create(a2_line),
                Create(a3_line),
                lag_ratio=0.14,
            ),
            FadeIn(graph_labels),
            run_time=1.25,
        )
 
        self.play(
            LaggedStart(
                GrowFromCenter(intersection_12),
                GrowFromCenter(intersection_13),
                GrowFromCenter(intersection_23),
                lag_ratio=0.18,
            ),
            run_time=0.65,
        )

        self.wait(1)
 
        self.play(
            FadeOut(title),
            run_time=0.45,
        )
 
        # upper envelope
 
        edge_color = YELLOW
        edge_width = 8
        poly_line_width = 0.05
        depth = OUT * 0.12
 
        left_point = axes.c2p(0, 5) + depth
        middle_left_point = axes.c2p(1 / 3, 11 / 3) + depth
        middle_right_point = axes.c2p(4 / 5, 16 / 5) + depth
        right_point = axes.c2p(1, 4) + depth
 
        finite_edge_1 = CustomLine3D(
            left_point,
            middle_left_point,
            color=edge_color,
            thickness=poly_line_width
        )
 
        finite_edge_2 = CustomLine3D(
            middle_left_point,
            middle_right_point,
            color=edge_color,
            thickness=poly_line_width
        )
 
        finite_edge_3 = CustomLine3D(
            middle_right_point,
            right_point,
            color=edge_color,
            thickness=poly_line_width
        )
 
        finite_chain = VGroup(
            finite_edge_1,
            finite_edge_2,
            finite_edge_3,
        )
        finite_chain.set_z_index(2)
 
        vertex_radius = 0.13
 
        left_vertex = Dot3D(
            point=left_point,
            radius=vertex_radius,
            color=WHITE,
            shade_in_3d=False
        )
 
        middle_left_vertex = Dot3D(
            point=middle_left_point,
            radius=vertex_radius,
            color=WHITE,
            shade_in_3d=False
        )
 
        middle_right_vertex = Dot3D(
            point=middle_right_point,
            radius=vertex_radius,
            color=WHITE,
            shade_in_3d=False
        )
 
        right_vertex = Dot3D(
            point=right_point,
            radius=vertex_radius,
            color=WHITE,
            shade_in_3d=False
        )
 
        finite_vertices = VGroup(
            left_vertex,
            middle_left_vertex,
            middle_right_vertex,
            right_vertex,
        )
 
        finite_vertices.set_z_index(3)

        self.play(
            LaggedStart(
                Create(finite_edge_1),
                Create(finite_edge_2),
                Create(finite_edge_3),
                lag_ratio=0.14,
            ),
            run_time=1.25,
            rate_func=smooth,
        )
 
        self.play(
            LaggedStart(
                GrowFromCenter(left_vertex),
                GrowFromCenter(middle_left_vertex),
                GrowFromCenter(middle_right_vertex),
                GrowFromCenter(right_vertex),
                lag_ratio=0.12,
            ),
            run_time=0.7,
        )
 
        self.wait(0.6)
 
 
        visible_ray_length = 1000
 
        left_visible_ray = CustomLine3D(
            left_point,
            left_point + UP * visible_ray_length,
            color=edge_color,
            thickness=poly_line_width,
        )
 
        right_visible_ray = CustomLine3D(
            right_point,
            right_point + UP * visible_ray_length,
            color=edge_color,
            thickness=poly_line_width,
        )
 
        self.play(
            Create(left_visible_ray),
            Create(right_visible_ray),
            run_time=1.15,
            rate_func=linear,
        )
 
        self.wait(0.8)
 
        # remove graph
        
        analytic_graph = VGroup(
            axes,
            graph_labels,
            a1_line,
            a2_line,
            a3_line,
            intersections,
        )
 
        self.play(
            FadeOut(analytic_graph),
            run_time=0.7,
            rate_func=smooth,
        )
 
        self.wait(0.4)
 
       # horizon grid
 
        def infinite_rail(start, direction, total_length, n_segments,
                           growth, near_color, far_color, width, bias=1.0,
                           near_opacity=1.0, far_opacity=1.0):
            raw_lengths = [growth ** i for i in range(n_segments)]
            scale = total_length / sum(raw_lengths)
            group = VGroup()
            cursor = 0.0
            for i, raw in enumerate(raw_lengths):
                seg_len = raw * scale
                p0 = start + direction * cursor
                p1 = start + direction * (cursor + seg_len)
                t = (i / (n_segments - 1)) ** bias
                group.add(Line(
                    p0, p1,
                    color=interpolate_color(near_color, far_color, t),
                    stroke_width=width,
                    stroke_opacity=interpolate(near_opacity, far_opacity, t),
                ))
                cursor += seg_len
            return group
 
 
        grid_center = axes.c2p(0.5, 0) + IN * 0.05
        grid_near_y, grid_far_y = -4, 10000
        grid_x_min, grid_x_max, grid_x_step = -20, 20, 1
        grid_far_color = GREY_D
 
        floor_grid = VGroup()
 
        
        for x in np.arange(grid_x_min, grid_x_max + 0.001, grid_x_step):
            floor_grid.add(infinite_rail(
                grid_center + RIGHT * x + UP * grid_near_y, UP,
                grid_far_y - grid_near_y, 18, 1.6,
                GREY_B, grid_far_color, 1.2, bias=2,
                near_opacity=0.6, far_opacity=0.1,
            ))
 
        
        n_rungs = 50
        rung_growth = 1.3
        raw_rungs = [rung_growth ** i for i in range(n_rungs)]
        rung_scale = (grid_far_y - grid_near_y) / sum(raw_rungs)
        cursor = 0.0
        for i, raw in enumerate(raw_rungs):
            y = grid_near_y + cursor
            t = i / (n_rungs - 1)
            line = Line(
                grid_center + RIGHT * grid_x_min + UP * y,
                grid_center + RIGHT * grid_x_max + UP * y,
                stroke_width=1.2,
                color=interpolate_color(GREY_B, grid_far_color, t),
                stroke_opacity=interpolate(0.55, 0.08, t),
            )
            floor_grid.add(line)
            cursor += raw * rung_scale

        floor_grid.set_z_index(-1)
        self.add(floor_grid)
 
        lane_offset = 1.1
        lane_length = 300
        left_lane_dir = normalize(left_point - right_point)
        right_lane_dir = -left_lane_dir
 
        left_lane = DashedLine(
            left_point + left_lane_dir * lane_offset,
            left_point + left_lane_dir * lane_offset + UP * lane_length,
            color=GREY_B,
            stroke_width=2.5,
            dash_length=0.35,
            dashed_ratio=0.5,
        )
        right_lane = DashedLine(
            right_point + right_lane_dir * lane_offset,
            right_point + right_lane_dir * lane_offset + UP * lane_length,
            color=GREY_B,
            stroke_width=2.5,
            dash_length=0.35,
            dashed_ratio=0.5,
        )

        self.add(
            left_lane,
            right_lane,
        )
 
        print(axes.c2p(1, 0) - axes.c2p(0, 0))

        new_camera_origin = np.array([0, 0, 1]) * (axes.c2p(1, 0) - axes.c2p(0, 0))[0] / 2 + DOWN * 1.5
        print(new_camera_origin)
       
        # camera movement
        self.move_camera(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            frame_center= new_camera_origin,
            focal_distance=3,
            run_time=2.4,
            zoom=1.3,
            rate_func=ease_in_out_sine,
        )
        self.wait(0.45)

        infinite_vertex = Dot3D(point=new_camera_origin + UP * 3, radius=vertex_radius, color=WHITE)
        infinite_vertex.set_z_index(3)

        self.play(FadeIn(infinite_vertex))

        self.wait()

        print(self.camera_pos())
        print(self.camera.get_rotation_matrix())
        self.play(FadeOut(floor_grid, left_lane, right_lane))

        self.play(
            *[self.project_mobject(m) for m in finite_vertices],
            self.project_mobject(infinite_vertex),
            *[self.project_line3d(line) for line in finite_chain],
            *[self.project_line3d(line) for line in [left_visible_ray, right_visible_ray]]
        )
        self.wait()

        polygon = VGroup(*finite_vertices, infinite_vertex, *finite_chain, left_visible_ray, right_visible_ray)
        self.play(Rotate(polygon, angle=-135 * DEGREES, axis=UP))
        self.wait()


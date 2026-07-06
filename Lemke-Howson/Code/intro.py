from xml.dom.minidom import Text
from manim import*
from manim.utils.rate_functions import ease_out_sine
from scipy.spatial import Delaunay
import numpy as np

class Intro(Scene):
    def construct(self):
        # nash image
        image1 = ImageMobject("nash.jpg").scale(0.4) 
        caption = Text(
            "John Nash(1928-2015)", 
            font="Arial", 
            slant=ITALIC, 
            font_size=36, 
            color=WHITE
        )

        caption.next_to(image1, DOWN, buff=0.4)
        intro_group1 = Group(image1, caption)
        self.play(
            FadeIn(intro_group1),
            run_time=3.5
        )
        self.wait(2)
        self.play(
            FadeOut(intro_group1),
            run_time=1.0
        )
        self.wait(1)
        # movie image
        image2=ImageMobject("a beautiful mind.jpg").scale(1)
        caption2 = Text(
            "A Beautiful Mind(2001)", 
            font="Arial", 
            slant=ITALIC, 
            font_size=36, 
            color=WHITE
        )
        caption2.next_to(image2, DOWN, buff=0.4)
        intro_group2 = Group(image2, caption2)
        self.play(
            FadeIn(intro_group2),
            run_time=3.5
        )
        self.wait(2)
        self.play(
            FadeOut(intro_group2),
            run_time=1.0
        )
        self.wait(1)


        #---game theory---

        #split screen in 3
        pos_left = LEFT * 4.6
        pos_center = ORIGIN
        pos_right = RIGHT * 4.6

        # Draw clean column separators
        line1 = Line(UP * 4, DOWN * 4).shift(LEFT * 2.3).set_stroke(GRAY, opacity=0.2)
        line2 = Line(UP * 4, DOWN * 4).shift(RIGHT * 2.3).set_stroke(GRAY, opacity=0.2)
        self.play(Create(line1), Create(line2), run_time=0.4)

        
        g1_title = Text("Game Theory", font_size=20, color=BLUE_A).move_to(pos_left + UP * 3.3)  
        base_origin = pos_left + DOWN * 1.4 

        # The 3 Coordinate Axes 
        axis_center = base_origin + UP * 1.1
        axis_x1 = Arrow(axis_center, axis_center + UP * 2.6, color=GRAY_A, stroke_width=1.5, tip_length=0.15)
        axis_x2 = Arrow(axis_center, axis_center + LEFT * 1.67 + DOWN * 1.1, color=GRAY_A, stroke_width=1.5, tip_length=0.15)
        axis_x3 = Arrow(axis_center, axis_center + RIGHT * 1.70 + DOWN * 1.1, color=GRAY_A, stroke_width=1.5, tip_length=0.15)
        
        lbl_x1 = MathTex("x_1", font_size=16).next_to(axis_x1.get_end(), UP, buff=0.05)
        lbl_x2 = MathTex("x_2", font_size=16).next_to(axis_x2.get_end(), LEFT, buff=0.05)
        lbl_x3 = MathTex("x_3", font_size=16).next_to(axis_x3.get_end(), RIGHT, buff=0.05)

        base_origin = pos_left + DOWN * 1.4
        axis_center = base_origin + UP * 1.1


        # 1. Vertical axis 
        v_top = axis_center + UP * 1.9  # 23² 
        v_center = axis_center # 123 
        
        # 2. Middle Row
        v_x2 = axis_center + LEFT * 1.0 + DOWN * 0.65 # 1²3
        v_x3 = axis_center + RIGHT * 1.0 + DOWN * 0.65 # 12²
        
        # 3. Upper Row
        v_upper_left = axis_center + LEFT * 1.0 + UP * 0.65  # 13²
        v_upper_right = axis_center + RIGHT * 1.0 + UP * 0.65 # 2²3
        
        # 4. Bottom Row
        v_bot_left = axis_center + LEFT * 0.35 + DOWN * 1.1  # 1²3
        v_bot_right = axis_center + RIGHT * 0.35 + DOWN * 1.1 # 123

        # Polytope Lines
        polytope_lines = VGroup(
            Line(v_top, v_upper_left, stroke_width=1.5, color=WHITE),
            Line(v_top, v_center, stroke_width=1.5, color=WHITE),
            Line(v_top, v_upper_right, stroke_width=1.5, color=WHITE),
            Line(v_upper_right, v_x3, stroke_width=1.5, color=WHITE),
            Line(v_upper_right, v_bot_right, stroke_width=1.5, color=WHITE),
            Line(v_center, v_x3, stroke_width=1.5, color=WHITE),
            Line(v_x3, v_bot_right, stroke_width=1.5, color=WHITE),
            Line(v_x2, v_bot_left, stroke_width=1.5, color=WHITE),
            Line(v_center, v_x2, stroke_width=1.5, color=WHITE),
            Line(v_bot_left, v_upper_left, stroke_width=1.5, color=WHITE),
            Line(v_bot_left, v_bot_right, stroke_width=1.5, color=WHITE),
            Line(v_upper_left, v_x2, stroke_width=1.5, color=WHITE)
        )

        # Vertex Dots
        all_vertices = [v_top, v_center, v_x2, v_x3, v_upper_left, v_upper_right, v_bot_left, v_bot_right]
        dots = VGroup(*[Dot(point=pt, radius=0.035, color=WHITE) for pt in all_vertices])

        # Labels
        labels = VGroup(
            MathTex("23^2", font_size=14).next_to(v_top, RIGHT, buff=0.08),
            MathTex("123", font_size=14).next_to(v_center, RIGHT, buff=0.08),
            MathTex("1^23", font_size=14).next_to(v_x2, LEFT, buff=0.08),
            MathTex("12^2", font_size=14).next_to(v_x3, RIGHT, buff=0.08),
            MathTex("13^2", font_size=14).next_to(v_upper_left, LEFT, buff=0.08),
            MathTex("2^23", font_size=14).next_to(v_upper_right, RIGHT, buff=0.08),
            MathTex("1^23", font_size=14).next_to(v_bot_left, DOWN, buff=0.08),
            MathTex("123", font_size=14).next_to(v_bot_right, DOWN, buff=0.08),
        )

        sub_left = Text("Lemke-Howson Polytope", font_size=15, font="Arial", slant=ITALIC, color=BLUE_C).move_to(pos_left + DOWN * 3)
        
        col1_group = VGroup(
            g1_title, axis_x1, axis_x2, axis_x3, lbl_x1, lbl_x2, lbl_x3, 
            polytope_lines, dots, labels, sub_left
        )

        # --- spherical mesh(fibonacci-delaunay) ---
        g2_title = VGroup(
            Text("Computational", font_size=20, color=GREEN_A),
            Text("Geometry", font_size=20, color=GREEN_A),
        ).arrange(DOWN, buff=0.05, aligned_edge=ORIGIN)

        g2_title.move_to(pos_center + UP * 3.3)
        mesh_outer_ring = Circle(radius=1.3, color=WHITE, stroke_width=2).move_to(pos_center)
        
        np.random.seed(42)
        num_points = 85
        points_2d = []
        
        for i in range(num_points):
            phi = np.arccos(1 - 2 * (i / num_points))
            theta = np.sqrt(num_points * np.pi) * phi
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            if np.sqrt(x**2 + y**2) < 0.98:
                points_2d.append([x * 1.3, y * 1.3])
                
        for angle in np.linspace(0, 2*np.pi, 24, endpoint=False):
            points_2d.append([1.3 * np.cos(angle), 1.3 * np.sin(angle)])
            
        points_array = np.array(points_2d)
        tri = Delaunay(points_array)
        
        mesh_triangles = VGroup()
        for simplex in tri.simplices:
            p1 = np.array([points_array[simplex[0]][0], points_array[simplex[0]][1], 0]) + pos_center
            p2 = np.array([points_array[simplex[1]][0], points_array[simplex[1]][1], 0]) + pos_center
            p3 = np.array([points_array[simplex[2]][0], points_array[simplex[2]][1], 0]) + pos_center
            
            mesh_triangles.add(
                Polygon(p1, p2, p3, stroke_color=GREEN_D, stroke_width=1.0, fill_color=GREEN_E, fill_opacity=0.08)
            )

        sub_center = Text("Spherical Mesh", font_size=15, font="Arial", slant=ITALIC, color=GREEN_C).move_to(pos_center + DOWN * 3)
        col2_group = VGroup(g2_title, mesh_outer_ring, mesh_triangles, sub_center)

        # Combinatorics Tree
        g3_title = Text("Combinatorics", font_size=20, color=PURPLE_A).move_to(pos_right + UP * 3.3)
        
        r_box = Rectangle(width=0.6, height=0.3, color=PURPLE_B).move_to(pos_right + UP * 2.0)
        r_txt = Text("0", font_size=8).move_to(r_box.get_center())
        tree_elements = VGroup(r_box, r_txt)
        
        l2_offsets = [-0.9, 0, 0.9]
        l2_nodes = []
        for idx, x_off in enumerate(l2_offsets):
            c_box = Rectangle(width=0.5, height=0.25, color=PURPLE_C).move_to(pos_right + RIGHT * x_off + UP * 0.8)
            c_txt = Text(f"{idx+1}", font_size=9).move_to(c_box.get_center())
            edge = Line(r_box.get_bottom(), c_box.get_top(), color=PURPLE_E, stroke_width=2)
            tree_elements.add(c_box, c_txt, edge)
            l2_nodes.append(c_box)
            
        l3_offsets = [[-1.2, -0.7], [-0.3, 0.3], [0.7, 1.2]]
        leaf_counter = 4
        for i, branch in enumerate(l2_nodes):
            for x_off in l3_offsets[i]:
                l_box = Rectangle(width=0.3, height=0.2, color=PURPLE_D).move_to(pos_right + RIGHT * x_off + DOWN * 0.4)
                l_txt = Text(f"{leaf_counter}", font_size=8).move_to(l_box.get_center())
                edge = Line(branch.get_bottom(), l_box.get_top(), color=PURPLE_E, stroke_width=1.2)
                tree_elements.add(l_box, l_txt, edge)
                leaf_counter += 1

        sub_right = Text("Permutation Tree", font_size=15, font="Arial", slant=ITALIC, color=PURPLE_C).move_to(pos_right + DOWN * 3)
        col3_group = VGroup(g3_title, tree_elements, sub_right)

        # animation reveal
        self.play(
            VGroup(line1, line2).animate.set_stroke(opacity=0.4),
            FadeIn(col1_group, shift=UP * 0.15),
            FadeIn(col2_group, scale=0.95),
            FadeIn(col3_group, shift=UP * 0.15),
            run_time=2.2
        )
        self.wait(3)
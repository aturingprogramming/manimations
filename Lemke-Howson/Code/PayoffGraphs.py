from manim import *
from FixedText import *


class PayoffGraphs(Scene):
    def construct(self):

        alice_image = (
            SVGMobject("../Images-Icons/alice.svg")
            .scale(1.5)
            .shift(LEFT * 4)
        )

        bob_image = (
            SVGMobject("../Images-Icons/bob.svg")
            .scale(1.5)
            .shift(RIGHT * 4)
        )

        alice_image.scale(0.35).to_corner(
            UL,
            buff=0.6,
        )

        bob_image.scale(0.35).to_corner(
            UR,
            buff=0.6,
        )

        self.add(
            alice_image,
            bob_image,
        )

       
        title = FixedText(
            "Finding a Mixed Nash Equilibrium",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP)

        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.7)

        # matrix
        payoff_data = [
            [(3, 2), (1, 1)],
            [(0, 0), (2, 3)],
        ]

        cell_width = 2.15
        cell_height = 1.08

        grid = VGroup()
        cells = []

        for i in range(3):
            row = []
            for j in range(3):
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    color=WHITE,
                    stroke_width=2,
                )
                cell.move_to(RIGHT * j * cell_width + DOWN * i * cell_height)
                grid.add(cell)
                row.append(cell)
            cells.append(row)

        grid.move_to(LEFT * 2.55 + DOWN * 0.3)

        matrix_box = SurroundingRectangle(
            grid,
            buff=0.16,
            color=WHITE,
            stroke_width=2,
            corner_radius=0.08,
        )

        alice_caption = FixedText(
            "Alice",
            font_size=31,
            weight=BOLD,
            color=RED,
        ).rotate(PI / 2)
        alice_caption.next_to(grid, LEFT, buff=0.55)

        bob_caption = FixedText(
            "Bob",
            font_size=31,
            weight=BOLD,
            color=BLUE,
        ).next_to(grid, UP, buff=0.48)

        alice_bach = FixedText("Bach", font_size=29, weight=BOLD)
        alice_stravinsky = FixedText("Stravinsky", font_size=27, weight=BOLD)
        bob_bach = FixedText("Bach", font_size=29, weight=BOLD)
        bob_stravinsky = FixedText("Stravinsky", font_size=27, weight=BOLD)

        alice_bach.move_to(cells[1][0])
        alice_stravinsky.move_to(cells[2][0])
        bob_bach.move_to(cells[0][1])
        bob_stravinsky.move_to(cells[0][2])

        strategy_labels = VGroup(
            alice_bach,
            alice_stravinsky,
            bob_bach,
            bob_stravinsky,
        )

        payoff_entries = VGroup()
        payoff_groups = [[None, None], [None, None]]
        alice_scores = VGroup()
        bob_scores = VGroup()

        for i in range(2):
            for j in range(2):
                alice_value, bob_value = payoff_data[i][j]

                open_parenthesis = FixedText("(", font_size=34)
                alice_score = FixedText(
                    str(alice_value),
                    font_size=34,
                    color=RED,
                )
                comma = FixedText(",", font_size=34)
                bob_score = FixedText(
                    str(bob_value),
                    font_size=34,
                    color=BLUE,
                )
                close_parenthesis = FixedText(")", font_size=34)

                entry = VGroup(
                    open_parenthesis,
                    alice_score,
                    comma,
                    bob_score,
                    close_parenthesis,
                ).arrange(RIGHT, buff=0.04)
                comma.shift(DOWN * 0.18)
                entry.move_to(cells[i + 1][j + 1])

                payoff_entries.add(entry)
                payoff_groups[i][j] = entry
                alice_scores.add(alice_score)
                bob_scores.add(bob_score)

        matrix = VGroup(
            grid,
            matrix_box,
            alice_caption,
            bob_caption,
            strategy_labels,
            payoff_entries,
        )

        self.play(
            Create(grid),
            Create(matrix_box),
            FadeIn(VGroup(alice_caption, bob_caption)),
            FadeIn(strategy_labels),
            FadeIn(payoff_entries),
            run_time=1.25,
        )
        self.wait(0.5)

        # ============================================================
        # ALICE'S MIXED STRATEGY
        # ============================================================
        right_panel_x = 3.45

        strategy_name = MathTex(r"x_A=", font_size=43)
        left_bracket = MathTex(r"[", font_size=58)
        strategy_p = MathTex(r"p", font_size=39, color=RED)
        strategy_comma = MathTex(r",", font_size=39)
        strategy_1mp = MathTex(r"1-p", font_size=39, color=RED)
        right_bracket = MathTex(r"]", font_size=58)

        strategy_vector = VGroup(
            strategy_name,
            left_bracket,
            strategy_p,
            strategy_comma,
            strategy_1mp,
            right_bracket,
        ).arrange(RIGHT, buff=0.10)
        strategy_comma.shift(DOWN * 0.09)
        strategy_vector.move_to(RIGHT * right_panel_x + UP * 1.55)

        
        self.play(
            Write(strategy_name),
            FadeIn(left_bracket),
            FadeIn(right_bracket),
            run_time=0.55,
        )

        p_source = MathTex(r"p", font_size=39, color=RED).move_to(alice_bach)
        one_minus_p_source = MathTex(r"1-p", font_size=39, color=RED).move_to(alice_stravinsky)
        comma_source = strategy_comma.copy().move_to(UP * 3.5 + strategy_comma.get_x() * RIGHT)
        self.add(p_source, one_minus_p_source, comma_source)

        self.play(
            Transform(p_source, strategy_p),
            Transform(one_minus_p_source, strategy_1mp),
            comma_source.animate.move_to(strategy_comma),
            run_time=0.95,
            rate_func=smooth,
        )
        self.remove(p_source, one_minus_p_source, comma_source)
        self.add(strategy_p, strategy_comma, strategy_1mp)
        self.wait(0.25)

        # bob chooses Bach first
        bach_underline = Line(
            bob_bach.get_left() + DOWN * 0.19,
            bob_bach.get_right() + DOWN * 0.19,
            color=BLUE,
            stroke_width=5,
        )

        bob_bach_top = payoff_groups[0][0][3]      
        bob_bach_bottom = payoff_groups[1][0][3]  

        self.play(
            Create(bach_underline),
            payoff_entries.animate.set_opacity(0.28),
            run_time=0.45,
        )
        self.play(
            bob_bach_top.animate.set_opacity(1),
            bob_bach_bottom.animate.set_opacity(1),
            run_time=0.3,
        )

        
        bach_prefix = MathTex(r"u_B(B)=", font_size=36)
        bach_prefix.set_color_by_tex("B", BLUE)
        b2 = MathTex("2", font_size=36, color=BLUE)
        dot1 = MathTex(r"\cdot", font_size=36)
        bp = MathTex("p", font_size=36, color=RED)
        plus1 = MathTex("+", font_size=36)
        b0 = MathTex("0", font_size=36, color=BLUE)
        dot2 = MathTex(r"\cdot", font_size=36)
        b1mp = MathTex("(1-p)", font_size=36, color=RED)

        bach_work = VGroup(bach_prefix, b2, dot1, bp, plus1, b0, dot2, b1mp)
        bach_work.arrange(RIGHT, buff=0.09)
        bach_work.move_to(RIGHT * right_panel_x + UP * 0.15)

        self.play(Write(bach_prefix), run_time=0.35)
        self.play(
            TransformFromCopy(bob_bach_top, b2),
            FadeIn(dot1),
            TransformFromCopy(strategy_p, bp),
            run_time=0.65,
        )
        self.play(FadeIn(plus1), run_time=0.2)
        self.play(
            TransformFromCopy(bob_bach_bottom, b0),
            FadeIn(dot2),
            TransformFromCopy(strategy_1mp, b1mp),
            run_time=0.65,
        )

        bach_result = MathTex(r"u_B(B)=2p", font_size=40, color=BLUE)
        bach_result.move_to(bach_work)
        self.play(TransformMatchingShapes(bach_work, bach_result), run_time=0.75)

        # bob chooses Stravinsky next
        stravinsky_underline = Line(
            bob_stravinsky.get_left() + DOWN * 0.19,
            bob_stravinsky.get_right() + DOWN * 0.19,
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            ReplacementTransform(bach_underline, stravinsky_underline),
            bach_result.animate.shift(UP * 0.18),
            payoff_entries.animate.set_opacity(0.28),
            run_time=0.55,
        )

        bob_stravinsky_top = payoff_groups[0][1][3]     
        bob_stravinsky_bottom = payoff_groups[1][1][3]  
        self.play(
            bob_stravinsky_top.animate.set_opacity(1),
            bob_stravinsky_bottom.animate.set_opacity(1),
            run_time=0.3,
        )

        s_prefix = MathTex(r"u_B(S)=", font_size=35)
        s_prefix.set_color_by_tex("S", BLUE)
        s1 = MathTex("1", font_size=35, color=BLUE)
        sdot1 = MathTex(r"\cdot", font_size=35)
        sp = MathTex("p", font_size=35, color=RED)
        splus = MathTex("+", font_size=35)
        s3 = MathTex("3", font_size=35, color=BLUE)
        sdot2 = MathTex(r"\cdot", font_size=35)
        s1mp = MathTex("(1-p)", font_size=35, color=RED)

        stravinsky_work = VGroup(s_prefix, s1, sdot1, sp, splus, s3, sdot2, s1mp)
        stravinsky_work.arrange(RIGHT, buff=0.085)
        stravinsky_work.move_to(RIGHT * right_panel_x + DOWN * 1.15)

        self.play(Write(s_prefix), run_time=0.35)
        self.play(
            TransformFromCopy(bob_stravinsky_top, s1),
            FadeIn(sdot1),
            TransformFromCopy(strategy_p, sp),
            run_time=0.65,
        )
        self.play(FadeIn(splus), run_time=0.2)
        self.play(
            TransformFromCopy(bob_stravinsky_bottom, s3),
            FadeIn(sdot2),
            TransformFromCopy(strategy_1mp, s1mp),
            run_time=0.65,
        )

        expanded = MathTex(r"u_B(S)=p+3-3p", font_size=38)
        expanded.set_color_by_tex("S", BLUE)
        expanded.move_to(stravinsky_work)
        self.play(TransformMatchingShapes(stravinsky_work, expanded), run_time=0.7)

        stravinsky_result = MathTex(r"u_B(S)=3-2p", font_size=40, color=BLUE)
        stravinsky_result.move_to(expanded)
        self.play(TransformMatchingTex(expanded, stravinsky_result), run_time=0.7)

       
       
        final_equations = VGroup(bach_result, stravinsky_result)
        final_equations.generate_target()
        final_equations.target.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        final_equations.target.move_to(ORIGIN + UP * 0.10)

        linear_label = FixedText(
            "Linear in terms of p",
            font_size=32,
            weight=BOLD,
        ).next_to(final_equations.target, DOWN, buff=0.55)

        everything_else = VGroup(
            title,
            matrix,
            strategy_name,
            left_bracket,
            strategy_p,
            strategy_comma,
            strategy_1mp,
            right_bracket,
            stravinsky_underline,
        )

        self.play(
            FadeOut(everything_else),
            MoveToTarget(final_equations),
            run_time=0.85,
        )
        self.play(FadeIn(linear_label, shift=UP * 0.10), run_time=0.45)
        self.wait(1.2)


        # graph of Bob's expected payoff as a function of Alice's mixed strategy p

        self.play(
            FadeOut(linear_label),
            final_equations.animate
                .arrange(DOWN, aligned_edge=LEFT, buff=0.24)
                .scale(0.82)
                .to_corner(UL, buff=0.45)
                .shift(DOWN * 1.5),
            run_time=0.8,
            rate_func=smooth,
        )

        axes = Axes(
            x_range=[0, 1.01, 0.25],
            y_range=[0, 3.1, 0.5],
            x_length=7.0,
            y_length=4.6,
            tips=False,
            axis_config={"stroke_width": 2},
        ).move_to(RIGHT * 0.9 + DOWN * 0.35)

        p_axis_label = MathTex("p", font_size=34).next_to(
            axes.x_axis.get_end(), RIGHT, buff=0.12
        )
        bob_payoff_label = FixedText(
            "Bob's expected payoff",
            font_size=24,
        ).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.42)

        x_zero = MathTex("0", font_size=24).next_to(axes.c2p(0, 0), DOWN, buff=0.20)
        x_half = MathTex(r"\frac12", font_size=24).next_to(axes.c2p(0.5, 0), DOWN, buff=0.20)
        x_one = MathTex("1", font_size=24).next_to(axes.c2p(1, 0), DOWN, buff=0.20)

        self.play(
            Create(axes),
            FadeIn(VGroup(p_axis_label, bob_payoff_label, x_zero, x_half, x_one)),
            run_time=0.9,
            rate_func=smooth,
        )

        bob_bach_line = axes.plot(
            lambda p: 2 * p,
            x_range=[0, 1],
            color=BLUE,
            stroke_width=5,
        )
        bob_stravinsky_line = axes.plot(
            lambda p: 3 - 2 * p,
            x_range=[0, 1],
            color=BLUE,
            stroke_width=5,
        )

        bob_bach_line_label = FixedText(
            "Bach", font_size=25, weight=BOLD, color=WHITE
        ).next_to(axes.c2p(0.88, 1.76), UP + LEFT, buff=0.08)

        bob_stravinsky_line_label = FixedText(
            "Stravinsky", font_size=23, weight=BOLD, color=WHITE
        ).next_to(axes.c2p(0.12, 2.76), RIGHT, buff=0.3)

        # Draw one line at a time, linking each to its equation
        bach_formula_copy = bach_result.copy()
        self.add(bach_formula_copy)
        self.play(
            bach_formula_copy.animate
                .scale(0.65)
                .move_to(axes.c2p(0.55, 1.1))
                .set_opacity(0),
            Create(bob_bach_line),
            run_time=0.95,
            rate_func=smooth,
        )
        self.remove(bach_formula_copy)
        self.play(FadeIn(bob_bach_line_label), run_time=0.3)

        self.wait(0.25)

        stravinsky_formula_copy = stravinsky_result.copy()
        self.add(stravinsky_formula_copy)
        self.play(
            stravinsky_formula_copy.animate
                .scale(0.65)
                .move_to(axes.c2p(0.45, 2.1))
                .set_opacity(0),
            Create(bob_stravinsky_line),
            run_time=0.95,
            rate_func=smooth,
        )
        self.remove(stravinsky_formula_copy)
        self.play(FadeIn(bob_stravinsky_line_label), run_time=0.3)

        # Intersection for Bob's indifference: p = 3/4
        bob_intersection = Dot(
            axes.c2p(0.75, 1.5),
            radius=0.085,
            color=YELLOW,
        )
        bob_intersection_guide = DashedLine(
            axes.c2p(0.75, 0),
            axes.c2p(0.75, 1.5),
            color=YELLOW,
            stroke_width=3,
        )
        p_three_fourths = MathTex(r"\frac34", font_size=25).next_to(
            axes.c2p(0.75, 0), DOWN, buff=0.20
        )

        self.play(GrowFromCenter(bob_intersection), run_time=0.35)
        self.play(
            Create(bob_intersection_guide),
            FadeIn(p_three_fourths),
            run_time=0.65,
            rate_func=smooth,
        )
        self.wait(0.45)

        
        # p = 1/2 IS NOT STABLE
        

        half_guide = DashedLine(
            axes.c2p(0.5, 0),
            axes.c2p(0.5, 2.0),
            color=YELLOW,
            stroke_width=3,
        )

        self.play(
            ReplacementTransform(bob_intersection_guide, half_guide),
            FadeOut(p_three_fourths),
            bob_intersection.animate.move_to(axes.c2p(0.5, 1.5)),
            run_time=0.8,
            rate_func=smooth,
        )

        half_bach_point = Dot(axes.c2p(0.5, 1.0), radius=0.075, color=BLUE)
        half_stravinsky_point = Dot(axes.c2p(0.5, 2.0), radius=0.075, color=RED)

        self.play(
            FadeOut(bob_intersection),
            GrowFromCenter(half_bach_point),
            GrowFromCenter(half_stravinsky_point),
            run_time=0.45,
        )
        self.play(
            Indicate(half_stravinsky_point, color=RED, scale_factor=1.55),
            run_time=0.65,
        )

        
        graph_objects = VGroup(
            axes,
            p_axis_label,
            bob_payoff_label,
            x_zero,
            x_half,
            x_one,
            bob_bach_line,
            bob_stravinsky_line,
            bob_bach_line_label,
            bob_stravinsky_line_label,
            half_guide,
            half_bach_point,
            half_stravinsky_point,
        )

        self.play(
            graph_objects.animate.scale(0.65).to_edge(RIGHT, buff=0.22),
            final_equations.animate.scale(0.84).shift(RIGHT * 5.75 + UP * 1.25),
            FadeIn(matrix, scale=0.92),
            run_time=0.85,
            rate_func=smooth,
        )

        bob_stravinsky_underline = Line(
            bob_stravinsky.get_left() + DOWN * 0.18,
            bob_stravinsky.get_right() + DOWN * 0.18,
            color=RED,
            stroke_width=5,
        )
        alice_stravinsky_underline = Line(
            alice_stravinsky.get_left() + DOWN * 0.18,
            alice_stravinsky.get_right() + DOWN * 0.18,
            color=RED,
            stroke_width=5,
        )

        self.play(Create(bob_stravinsky_underline), run_time=0.4)
        self.play(
            payoff_entries.animate.set_opacity(0.25),
            payoff_groups[0][1][3].animate.set_opacity(1),
            payoff_groups[1][1][3].animate.set_opacity(1),
            run_time=0.4,
        )
        self.play(
            Create(alice_stravinsky_underline),
            payoff_groups[0][1][1].animate.set_opacity(1),
            payoff_groups[1][1][1].animate.set_opacity(1),
            run_time=0.45,
        )
        self.play(
            Indicate(payoff_groups[1][1][1], color=RED, scale_factor=1.4),
            run_time=0.65,
        )

        half_strategy = MathTex(
            r"x_A=\left[\frac12,\frac12\right]",
            font_size=35,
            color=RED,
        ).next_to(matrix, DOWN, buff=0.28)
        pure_strategy = MathTex(
            r"x_A=[0,1]",
            font_size=38,
            color=RED,
        ).move_to(half_strategy)

        self.play(FadeIn(half_strategy), run_time=0.35)
        self.play(
            TransformMatchingTex(half_strategy, pure_strategy),
            run_time=0.7,
            rate_func=smooth,
        )
        self.wait(0.35)

        
        self.play(
            FadeOut(matrix),
            FadeOut(bob_stravinsky_underline),
            FadeOut(alice_stravinsky_underline),
            FadeOut(pure_strategy),
            graph_objects.animate.scale(1 / 0.65).move_to(RIGHT * 0.9 + UP * 0.5),
            final_equations.animate.scale(1 / 0.84).to_corner(UL, buff=0.45).shift(DOWN * 1.5),
            run_time=0.85,
            rate_func=smooth,
        )
        payoff_entries.set_opacity(1)

        self.play(
            FadeOut(half_bach_point),
            FadeOut(half_stravinsky_point),
            run_time=0.25,
        )

        intersection_guide_again = DashedLine(
            axes.c2p(0.75, 0),
            axes.c2p(0.75, 1.5),
            color=YELLOW,
            stroke_width=3,
        )
        bob_intersection_again = Dot(
            axes.c2p(0.75, 1.5),
            radius=0.085,
            color=YELLOW,
        )

        p_three_fourths.move_to(
            axes.c2p(0.75, 0)
            + DOWN * 0.45
        )

        self.play(
            ReplacementTransform(half_guide, intersection_guide_again),
            GrowFromCenter(bob_intersection_again),
            FadeIn(p_three_fourths),
            run_time=0.75,
            rate_func=smooth,
        )
       

        indifferent_text = FixedText(
            "Bob is indifferent",
            font_size=30,
            weight=BOLD,
        ).next_to(axes, DOWN, buff=0.65)

        self.play(FadeIn(indifferent_text, shift=UP * 0.1), run_time=0.4)

        indifference_equation = MathTex(
            r"u_B(B)=u_B(S)",
            font_size=41,
            color=BLUE,
        ).move_to(indifferent_text)

        self.play(
            ReplacementTransform(indifferent_text, indifference_equation),
            run_time=0.65,
        )

        p_solution = MathTex(
            r"2p=3-2p\quad\Longrightarrow\quad p=\frac{3}{4}",
            font_size=37,
            color=YELLOW,
        ).next_to(indifference_equation, DOWN, buff=0.24)

        self.play(Write(p_solution), run_time=0.8)
        self.wait(0.65)

        #show Alice's graphs
        alice_bach_equation = MathTex(
            r"u_A(B)=1+2q",
            font_size=40,
            color=RED,
        )
        alice_stravinsky_equation = MathTex(
            r"u_A(S)=2-2q",
            font_size=40,
            color=RED,
        )
        alice_equations = VGroup(
            alice_bach_equation,
            alice_stravinsky_equation,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        alice_equations.move_to(final_equations)

        alice_bach_line = axes.plot(
            lambda q: 1 + 2 * q,
            x_range=[0, 1],
            color=RED,
            stroke_width=5,
        )
        alice_stravinsky_line = axes.plot(
            lambda q: 2 - 2 * q,
            x_range=[0, 1],
            color=RED,
            stroke_width=5,
        )

        q_axis_label = MathTex("q", font_size=34).move_to(p_axis_label)
        alice_payoff_label = FixedText(
            "Alice's expected payoff",
            font_size=24,
        ).rotate(PI / 2).move_to(bob_payoff_label)

        q_one_fourth = MathTex(r"\frac14", font_size=25).next_to(
            axes.c2p(0.25, 0), DOWN, buff=0.10
        )
        alice_intersection = Dot(
            axes.c2p(0.25, 1.5),
            radius=0.085,
            color=YELLOW,
        )
        alice_intersection_guide = DashedLine(
            axes.c2p(0.25, 0),
            axes.c2p(0.25, 1.5),
            color=YELLOW,
            stroke_width=3,
        )

        alice_bach_label = FixedText(
            "Bach", font_size=25, weight=BOLD, color=BLUE
        ).next_to(axes.c2p(0.82, 2.64), LEFT, buff=0.18)
        alice_stravinsky_label = FixedText(
            "Stravinsky", font_size=23, weight=BOLD, color=RED
        ).next_to(axes.c2p(0.12, 1.76), RIGHT, buff=0.3)

        self.play(
            FadeOut(VGroup(indifference_equation, p_solution, p_three_fourths)),
            Transform(final_equations, alice_equations),
            Transform(bob_bach_line, alice_bach_line),
            Transform(bob_stravinsky_line, alice_stravinsky_line),
            ReplacementTransform(p_axis_label, q_axis_label),
            ReplacementTransform(bob_payoff_label, alice_payoff_label),
            ReplacementTransform(bob_intersection_again, alice_intersection),
            ReplacementTransform(intersection_guide_again, alice_intersection_guide),
            ReplacementTransform(bob_bach_line_label, alice_bach_label),
            ReplacementTransform(bob_stravinsky_line_label, alice_stravinsky_label),
            FadeIn(q_one_fourth),
            run_time=1.15,
            rate_func=smooth,
        )

        q_solution = MathTex(
            r"q=\frac14",
            font_size=40,
            color=YELLOW,
        ).next_to(axes, DOWN, buff=0.52)
        self.play(FadeIn(q_solution, shift=DOWN * 1.8), run_time=0.45)
        self.wait(0.55)

        # combine them
        alice_mixed_vector = MathTex(
            r"x_A^*=\left[\frac34,\frac14\right]",
            font_size=42,
            color=RED,
        ).shift(LEFT * 3.0)

        bob_mixed_vector = MathTex(
            r"x_B^*=\left[\frac14,\frac34\right]",
            font_size=42,
            color=BLUE,
        ).shift(RIGHT * 3.0)

        mixed_ne_label = FixedText(
            "Mixed Nash Equilibrium",
            font_size=36,
            weight=BOLD,
        )

        mixed_vectors = VGroup(alice_mixed_vector, bob_mixed_vector).arrange(
            RIGHT, buff=1.25
        ).move_to(UP * 0.25)
        mixed_ne_label.next_to(mixed_vectors, UP, buff=0.85)

        graph_scene = VGroup(
            axes,
            q_axis_label,
            alice_payoff_label,
            x_zero,
            x_half,
            x_one,
            q_one_fourth,
            bob_bach_line,
            bob_stravinsky_line,
            alice_bach_label,
            alice_stravinsky_label,
            alice_intersection,
            alice_intersection_guide,
            final_equations,
            q_solution,
        )

        self.play(
            FadeOut(graph_scene),
            FadeIn(alice_mixed_vector, shift=RIGHT * 0.45),
            FadeIn(bob_mixed_vector, shift=LEFT * 0.45),
            run_time=0.85,
            rate_func=smooth,
        )
        self.play(FadeIn(mixed_ne_label, shift=UP * 0.1), run_time=0.45)
        self.wait(0.8)

       
        self.play(
            FadeOut(VGroup(mixed_vectors, mixed_ne_label)),
            run_time=0.6,
        )

        profile_axes = Axes(
            x_range=[0, 1.01, 0.25],
            y_range=[0, 1.01, 0.25],
            x_length=5.2,
            y_length=5.2,
            tips=False,
            axis_config={"stroke_width": 2},
        ).move_to(DOWN * 0.15)

        profile_square = Square(
            side_length=5.2,
            color=WHITE,
            stroke_width=2,
        ).move_to(profile_axes.c2p(0.5, 0.5))

        p_label_square = MathTex("p", font_size=34).next_to(
            profile_axes.x_axis.get_end(), RIGHT, buff=0.12
        )
        q_label_square = MathTex("q", font_size=34).next_to(
            profile_axes.y_axis.get_end(), UP, buff=0.12
        )

        self.play(
            Create(profile_axes),
            Create(profile_square),
            FadeIn(VGroup(p_label_square, q_label_square)),
            run_time=0.85,
        )

        # Pure equilibria are at the two extreme points
        pure_ne_stravinsky = Dot(
            profile_axes.c2p(0, 0), radius=0.095, color=GREEN
        )
        pure_ne_bach = Dot(
            profile_axes.c2p(1, 1), radius=0.095, color=GREEN
        )
        mixed_ne_point = Dot(
            profile_axes.c2p(0.75, 0.25), radius=0.095, color=YELLOW
        )

        pure_label = FixedText(
            "Pure NE",
            font_size=28,
            weight=BOLD,
            color=GREEN,
        ).next_to(VGroup(pure_ne_stravinsky, pure_ne_bach), LEFT, buff=0.65)

        mixed_label = FixedText(
            "Mixed NE",
            font_size=28,
            weight=BOLD,
            color=YELLOW,
        ).next_to(mixed_ne_point, UP, buff=0.25)

        self.play(
            LaggedStart(
                GrowFromCenter(pure_ne_stravinsky),
                GrowFromCenter(pure_ne_bach),
                lag_ratio=0.25,
            ),
            run_time=0.7,
        )
        self.play(FadeIn(pure_label), run_time=0.35)
        self.play(GrowFromCenter(mixed_ne_point), run_time=0.4)
        self.play(FadeIn(mixed_label), run_time=0.35)
        self.wait(0.55)

       # extreme and intersection labels 
        extreme_label = FixedText(
            "Extreme points",
            font_size=28,
            weight=BOLD,
            color=GREEN,
        ).move_to(pure_label)
        intersection_label = FixedText(
            "Intersection point",
            font_size=28,
            weight=BOLD,
            color=YELLOW,
        ).move_to(mixed_label)

        self.play(
            ReplacementTransform(pure_label, extreme_label),
            ReplacementTransform(mixed_label, intersection_label),
            run_time=0.65,
        )

        # Faint background points suggest the full infinite search space
        faint_points = VGroup()
        for px in [0.15, 0.3, 0.45, 0.6, 0.85]:
            for qx in [0.15, 0.35, 0.55, 0.75, 0.9]:
                if abs(px - 0.75) < 0.03 and abs(qx - 0.25) < 0.03:
                    continue
                faint_points.add(
                    Dot(
                        profile_axes.c2p(px, qx),
                        radius=0.035,
                        color=GRAY,
                        fill_opacity=0.35,
                    )
                )

        self.play(
            LaggedStart(
                *[FadeIn(point, scale=0.6) for point in faint_points],
                lag_ratio=0.025,
            ),
            run_time=0.75,
        )

        candidate_title = FixedText(
            "Candidate points",
            font_size=34,
            weight=BOLD,
        ).to_edge(UP, buff=0.45)

        self.play(FadeIn(candidate_title, shift=DOWN * 0.1), run_time=0.4)
        self.play(
            faint_points.animate.set_opacity(0.08),
            run_time=0.65,
        )

        # vertex enumeration

        vertex_title = FixedText(
            "Vertex Enumeration",
            font_size=38,
            weight=BOLD,
        ).move_to(candidate_title)

        self.play(
            ReplacementTransform(candidate_title, vertex_title),
            run_time=0.55,
        )

        search_ring = Circle(
            radius=0.22,
            color=YELLOW,
            stroke_width=4,
        ).move_to(pure_ne_stravinsky)

        self.play(Create(search_ring), run_time=0.35)
        self.play(
            search_ring.animate.move_to(pure_ne_bach),
            run_time=0.65,
            rate_func=smooth,
        )
        self.play(
            search_ring.animate.move_to(mixed_ne_point),
            run_time=0.65,
            rate_func=smooth,
        )

        enumeration_rule = FixedText(
            "Enumerate candidates, then check the Nash conditions",
            font_size=25,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(enumeration_rule, shift=UP * 0.1), run_time=0.45)
        self.wait(0.55)

        slow_label = FixedText(
            "Correct, but potentially very slow",
            font_size=31,
            weight=BOLD,
            color=RED,
        ).move_to(enumeration_rule)

        self.play(
            ReplacementTransform(enumeration_rule, slow_label),
            FadeOut(search_ring),
            run_time=0.6,
        )
        self.wait(0.65)

        final_question = FixedText(
            "Can we do better?",
            font_size=46,
            weight=BOLD,
        ).move_to(ORIGIN)

        self.play(
            FadeOut(
                VGroup(
                    profile_axes,
                    profile_square,
                    p_label_square,
                    q_label_square,
                    pure_ne_stravinsky,
                    pure_ne_bach,
                    mixed_ne_point,
                    extreme_label,
                    intersection_label,
                    faint_points,
                    vertex_title,
                    slow_label,
                )
            ),
            FadeIn(final_question, scale=0.9),
            run_time=0.85,
            rate_func=smooth,
        )
        self.wait(1.2)
from manim import *
from FixedText import *


class PureNashEquilibria(Scene):
    def construct(self):

       # old bimatrix

        alice_image = SVGMobject("../Images-Icons/alice.svg").scale(1.5)
        bob_image = SVGMobject("../Images-Icons/bob.svg").scale(1.5)
        alice_image.scale(0.35).to_corner(UL, buff=0.6)
        bob_image.scale(0.35).to_corner(UR, buff=0.6)

        payoff_data = [
            [(3, 2), (1, 1)],
            [(0, 0), (2, 3)]
        ]

        cell_width = 3.2
        cell_height = 1.8

        grid = VGroup()
        cells = []

        # ==================================================
        # CREATE 3x3 BIMATRIX GRID
        # ==================================================

        for i in range(3):
            row = []

            for j in range(3):
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    color=WHITE,
                    stroke_width=2
                )

                cell.move_to(
                    RIGHT * j * cell_width
                    + DOWN * i * cell_height
                )

                grid.add(cell)
                row.append(cell)

            cells.append(row)

        grid.move_to(DOWN * 0.3)

        matrix_box = SurroundingRectangle(
            grid,
            buff=0.2,
            color=WHITE,
            stroke_width=2
        )


        alice_caption1 = FixedText(
            "Alice",
            font_size=40,
            weight=BOLD,
            color=RED
        )

        bob_caption1 = FixedText(
            "Bob",
            font_size=40,
            weight=BOLD,
            color=BLUE
        )

        alice_caption1.rotate(PI / 2)
        alice_caption1.next_to(grid, LEFT, buff=0.8)

        bob_caption1.next_to(grid, UP, buff=0.8)


        alice_bach = FixedText(
            "Bach",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        alice_stravinsky = FixedText(
            "Stravinsky",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        bob_bach = FixedText(
            "Bach",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        bob_stravinsky = FixedText(
            "Stravinsky",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        alice_bach.move_to(cells[1][0].get_center())
        alice_stravinsky.move_to(cells[2][0].get_center())

        bob_bach.move_to(cells[0][1].get_center())
        bob_stravinsky.move_to(cells[0][2].get_center())

        strategy_labels = VGroup(
            alice_bach,
            alice_stravinsky,
            bob_bach,
            bob_stravinsky
        )

        player_labels = VGroup(
            alice_caption1,
            bob_caption1
        )

        payoff_entries = VGroup()
        alice_scores = VGroup()
        bob_scores = VGroup()

        for i in range(2):
            for j in range(2):
                alice_val, bob_val = payoff_data[i][j]

                open_p = FixedText(
                    "(",
                    font_size=50,
                    color=WHITE
                )

                alice_score = FixedText(
                    str(alice_val),
                    font_size=50,
                    color=RED
                )

                comma = FixedText(
                    ",",
                    font_size=50,
                    color=WHITE
                )

                bob_score = FixedText(
                    str(bob_val),
                    font_size=50,
                    color=BLUE
                )

                close_p = FixedText(
                    ")",
                    font_size=50,
                    color=WHITE
                )

                payoff = VGroup(
                    open_p,
                    alice_score,
                    comma,
                    bob_score,
                    close_p
                )

                payoff.arrange(RIGHT, buff=0.05)
                comma.shift(DOWN * 0.25)

                payoff.move_to(
                    cells[i + 1][j + 1].get_center()
                )

                payoff_entries.add(payoff)
                alice_scores.add(alice_score)
                bob_scores.add(bob_score)

        # group bimatrix

        bimatrix = VGroup(
            grid,
            matrix_box,
            player_labels,
            strategy_labels,
            payoff_entries
        )

        self.add(
            alice_image,
            bob_image,
            bimatrix
        )

        self.wait(1)


        top_left_cell = cells[1][1]
        top_right_cell = cells[1][2]
        bottom_left_cell = cells[2][1]
        bottom_right_cell = cells[2][2]

        top_left_payoff = payoff_entries[0]
        top_right_payoff = payoff_entries[1]
        bottom_left_payoff = payoff_entries[2]
        bottom_right_payoff = payoff_entries[3]

        # animation helper
        # IT COMPARES THE CORRESPONDIN PAYOFFS(BIGGER SCALE FOR BEST OPTION)

        def compare_payoffs(
            better_score,
            worse_score,
            better_scale=1.8,
            worse_scale=1.25,
            run_time=0.55,
        ):

            better_score.save_state()
            worse_score.save_state()

            self.play(
                better_score.animate
                    .scale(better_scale)
                    .set_opacity(1),

                worse_score.animate
                    .scale(worse_scale)
                    .set_opacity(0.45),

                run_time=run_time,
                rate_func=smooth
            )

            self.wait(0.4)

            self.play(
                Restore(better_score),
                Restore(worse_score),
                run_time=0.4,
                rate_func=smooth
            )

       #top left case
        top_left_cell = cells[1][1]

        top_left_highlight = SurroundingRectangle(
            top_left_cell,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        other_payoffs = VGroup(
            payoff_entries[1],
            payoff_entries[2],
            payoff_entries[3]
        )

        self.play(
            other_payoffs.animate.set_opacity(0.2),
            Create(top_left_highlight),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.5)

        self.play(
            FadeOut(top_left_highlight),
            run_time=0.8,
            rate_func=smooth
        )

        # Alice: 3 > 0
        compare_payoffs(
            better_score=alice_scores[0],
            worse_score=alice_scores[2]
        )

        self.wait(1)

        # Bob: 2 > 1
        compare_payoffs(
            better_score=bob_scores[0],
            worse_score=bob_scores[1]
        )
        self.wait(0.6)

        self.play(
            other_payoffs.animate.set_opacity(1),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.5)
 
        # bottom right case

        bottom_right_cell = cells[2][2]

        bottom_right_highlight = SurroundingRectangle(
            bottom_right_cell,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        # Dim the other three payoff entries
        other_payoffs = VGroup(
            payoff_entries[0],
            payoff_entries[1],
            payoff_entries[2]
        )

        self.play(
            other_payoffs.animate.set_opacity(0.2),
            Create(bottom_right_highlight),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.5)

        self.play(
            FadeOut(bottom_right_highlight),
            run_time=0.8,
            rate_func=smooth
        )

        compare_payoffs(
            better_score=alice_scores[3],
            worse_score=alice_scores[1]
        )

        self.wait(1)

        compare_payoffs(
            better_score=bob_scores[3],
            worse_score=bob_scores[2]
        )

        self.wait(0.6)

        self.play(
            other_payoffs.animate.set_opacity(1),
            run_time=0.8,
            rate_func=smooth
        )



        
        # off diagonal case 1
        top_right_cell = cells[1][2]

        top_right_highlight = SurroundingRectangle(
            top_right_cell,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        other_payoffs = VGroup(
            payoff_entries[0],
            payoff_entries[2],
            payoff_entries[3]
        )

        self.play(
            other_payoffs.animate.set_opacity(0.2),
            Create(top_right_highlight),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.5)

        self.play(
            FadeOut(top_right_highlight),
            run_time=0.8,
            rate_func=smooth
        )
        #different this time
        compare_payoffs(
            better_score=alice_scores[3],
            worse_score=alice_scores[1]
        )

        self.wait(1)

        compare_payoffs(
            better_score=bob_scores[0],
            worse_score=bob_scores[1]
        )
        self.wait(0.6)

        self.play(
            other_payoffs.animate.set_opacity(1),
            run_time=0.8,
            rate_func=smooth
        )

        
        #off diagonal case 2
        bottom_left_cell = cells[2][1]

        bottom_left_highlight = SurroundingRectangle(
            bottom_left_cell,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        other_payoffs = VGroup(
            payoff_entries[0],
            payoff_entries[1],
            payoff_entries[3]
        )

        self.play(
            other_payoffs.animate.set_opacity(0.2),
            Create(bottom_left_highlight),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.5)


        self.play(
            FadeOut(bottom_left_highlight),
            run_time=0.8,
            rate_func=smooth
        )

        compare_payoffs(
            better_score=alice_scores[0],
            worse_score=alice_scores[2]
        )

        self.wait(1)

        compare_payoffs(
            better_score=bob_scores[3],
            worse_score=bob_scores[2]
        )

        self.wait(0.6)

        self.play(
            other_payoffs.animate.set_opacity(1),
            run_time=0.8,
            rate_func=smooth    
        )

        self.wait(0.5)

        # ============================================================
        # STABILITY VS INSTABILITY
        # ============================================================

        top_left_cell = cells[1][1]
        top_right_cell = cells[1][2]
        bottom_left_cell = cells[2][1]
        bottom_right_cell = cells[2][2]

        # cell highlights

        # Unstable

        top_right_unstable = SurroundingRectangle(
            top_right_cell,
            color=RED,
            stroke_width=6,
            buff=-0.04
        )

        bottom_left_unstable = SurroundingRectangle(
            bottom_left_cell,
            color=RED,
            stroke_width=6,
            buff=-0.04
        )

        # stable

        top_left_stable = SurroundingRectangle(
            top_left_cell,
            color=GREEN,
            stroke_width=6,
            buff=-0.04
        )

        bottom_right_stable = SurroundingRectangle(
            bottom_right_cell,
            color=GREEN,
            stroke_width=6,
            buff=-0.04
        )


        unstable_label = FixedText(
            "Unstable",
            font_size=38,
            weight=BOLD,
            color=RED
        )

        unstable_label.next_to(grid, DOWN, buff=0.6)

        self.play(
            Create(top_right_unstable),
            Create(bottom_left_unstable),
            FadeIn(unstable_label, shift=UP * 0.15),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.5)

        stable_label = FixedText(
            "Stable",
            font_size=38,
            weight=BOLD,
            color=GREEN
        )

        stable_label.move_to(unstable_label)

        self.play(
            FadeOut(top_right_unstable),
            FadeOut(bottom_left_unstable),
            Transform(unstable_label, stable_label),
            Create(top_left_stable),
            Create(bottom_right_stable),
            run_time=1.1,
            rate_func=smooth
        )

        self.wait(1)

        # stable -> Nash eq.

        nash_label = FixedText(
            "Nash Equilibria",
            font_size=44,
            weight=BOLD,
            color=YELLOW
        )

        nash_label.move_to(stable_label)

        self.play(
            Transform(unstable_label, nash_label),
            top_left_stable.animate.set_stroke(
                color=YELLOW,
                width=7
            ),
            bottom_right_stable.animate.set_stroke(
                color=YELLOW,
                width=7
            ),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(1)

        self.play(
            FadeOut(top_left_stable),
            FadeOut(bottom_right_stable),
            FadeOut(nash_label),
            FadeOut(unstable_label),
            run_time=0.7,
            rate_func=smooth
        )

        # ball animation

        bottom_left_cell = cells[2][1]
        top_left_cell = cells[1][1]


        ball = Circle(
            radius=0.1,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        )

        ball.move_to(bottom_left_cell.get_center())

        self.play(
            FadeIn(ball, scale=0.5),
            run_time=0.6,
            rate_func=smooth
        )

        self.wait(0.5)



        alice_move_arrow = Arrow(
            start=bottom_left_cell.get_center() + UP * 0.2,
            end=top_left_cell.get_center() + DOWN * 0.2,
            color=RED,
            stroke_width=7,
            buff=0.15,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            GrowArrow(alice_move_arrow),
            run_time=0.7,
            rate_func=smooth
        )

        self.wait(0.3)

        self.play(
            ball.animate.move_to(top_left_cell.get_center()),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(0.4)

        self.play(
            FadeOut(alice_move_arrow),
            run_time=1,
            rate_func=smooth
        )

        stable_highlight = SurroundingRectangle(
            top_left_cell,
            color=GREEN,
            stroke_width=7,
            buff=-0.04
        )

        self.play(
            Create(stable_highlight),
            run_time=0.7,
            rate_func=smooth
        )

        # Small wobble
        self.play(
            Wiggle(
                ball,
                scale_value=1.15,
                rotation_angle=0.08
            ),
            run_time=0.8
        )

        self.wait(0.5)

        # 2nd equilibrium

        bottom_right_cell = cells[2][2]

        second_equilibrium_highlight = SurroundingRectangle(
            bottom_right_cell,
            color=GREEN,
            stroke_width=7,
            buff=-0.04
        )

        ball_target = ball.copy().move_to(bottom_right_cell.get_center())

        self.play(
            TransformFromCopy(ball, ball_target),
            Create(second_equilibrium_highlight),
            run_time=1.1,
            rate_func=smooth
        )

        self.play(
            Wiggle(
                ball_target,
                scale_value=1.15,
                rotation_angle=0.08
            ),
            run_time=0.8
        )

        self.wait(1)

        self.play(
            FadeOut(ball),
            FadeOut(ball_target),
            FadeOut(stable_highlight),
            FadeOut(second_equilibrium_highlight),
            run_time=0.7,
            rate_func=smooth
        )

        self.wait(0.5)

        # Nash applications

        previous_scene = VGroup(
            grid,
            matrix_box,
            payoff_entries,
            alice_caption1,
            bob_caption1,
            alice_bach,
            alice_stravinsky,
            bob_bach,
            bob_stravinsky
        )

        self.play(
            FadeOut(previous_scene),
            FadeOut(alice_image),
            FadeOut(bob_image),
            run_time=1,
            rate_func=smooth
        )

        self.wait(0.4)

        nash_center = FixedText(
            "Nash Equilibrium",
            font_size=48,
            weight=BOLD,
            color=YELLOW
        )

        nash_box = SurroundingRectangle(
            nash_center,
            color=YELLOW,
            stroke_width=4,
            buff=0.3,
            corner_radius=0.15
        )

        nash_group = VGroup(
            nash_box,
            nash_center
        )

        nash_group.move_to(ORIGIN)

        self.play(
            FadeIn(nash_group, scale=0.8),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.4)

        # application labels

        economics = FixedText(
            "Economic interactions",
            font_size=34,
            weight=BOLD,
            color=WHITE
        )

        geopolitics = FixedText(
            "Geopolitical negotiations",
            font_size=34,
            weight=BOLD,
            color=WHITE
        )

        evolution = FixedText(
            "Evolutionary outcomes",
            font_size=34,
            weight=BOLD,
            color=WHITE
        )

        economics.move_to(LEFT * 4.2 + UP * 2.1)
        geopolitics.move_to(RIGHT * 4.2 + UP * 2.1)
        evolution.move_to(DOWN * 2.4)

       # arrows to nash

        economics_arrow = Arrow(
            start=economics.get_bottom(),
            end=nash_box.get_corner(UL),
            buff=0.2,
            color=WHITE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.12
        )

        geopolitics_arrow = Arrow(
            start=geopolitics.get_bottom(),
            end=nash_box.get_corner(UR),
            buff=0.2,
            color=WHITE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.12
        )

        evolution_arrow = Arrow(
            start=evolution.get_top(),
            end=nash_box.get_bottom(),
            buff=0.2,
            color=WHITE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.12
        )


        self.play(
            FadeIn(economics, shift=RIGHT * 0.25),
            GrowArrow(economics_arrow),
            run_time=1,
            rate_func=smooth
        )

        self.wait(0.5)

        self.play(
            FadeIn(geopolitics, shift=LEFT * 0.25),
            GrowArrow(geopolitics_arrow),
            run_time=1,
            rate_func=smooth
        )

        self.wait(0.5)

        self.play(
            FadeIn(evolution, shift=UP * 0.25),
            GrowArrow(evolution_arrow),
            run_time=1,
            rate_func=smooth
        )

        self.wait(0.8)


        applications_group = VGroup(
            economics,
            geopolitics,
            evolution,
            economics_arrow,
            geopolitics_arrow,
            evolution_arrow,
            nash_group
        )

        self.play(
            FadeOut(applications_group),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.4)


       # FORMAL DEFINITION

        formal_title = FixedText(
            "Formal Definition",
            font_size=48,
            weight=BOLD,
            color=YELLOW
        )

        formal_title.to_edge(UP, buff=0.55)

        self.play(
            FadeIn(formal_title, shift=DOWN * 0.2),
            run_time=0.9,
            rate_func=smooth
        )

        self.wait(0.6)


        # Build a strategy profile


        player_1 = FixedText(
            "Player 1",
            font_size=27,
            color=WHITE
        )

        player_2 = FixedText(
            "Player 2",
            font_size=27,
            color=WHITE
        )

        player_n = FixedText(
            "Player n",
            font_size=27,
            color=WHITE
        )

        player_labels = VGroup(
            player_1,
            player_2,
            player_n
        ).arrange(RIGHT, buff=1.5)

        player_labels.move_to(UP * 1.3)

        strategy_1 = MathTex(
            r"s_1",
            font_size=52,
            color=WHITE
        ).next_to(player_1, DOWN, buff=0.3)

        strategy_2 = MathTex(
            r"s_2",
            font_size=52,
            color=WHITE
        ).next_to(player_2, DOWN, buff=0.3)

        strategy_n = MathTex(
            r"s_n",
            font_size=52,
            color=WHITE
        ).next_to(player_n, DOWN, buff=0.3)

        strategy_labels = VGroup(
            strategy_1,
            strategy_2,
            strategy_n
        )

        self.play(
            LaggedStart(
                FadeIn(player_1, shift=UP * 0.15),
                FadeIn(strategy_1, shift=UP * 0.15),
                FadeIn(player_2, shift=UP * 0.15),
                FadeIn(strategy_2, shift=UP * 0.15),
                FadeIn(player_n, shift=UP * 0.15),
                FadeIn(strategy_n, shift=UP * 0.15),
                lag_ratio=0.12
            ),
            run_time=1.8
        )

        self.wait(0.5)

        strategy_profile = MathTex(
            r"(s_1,\;s_2,\;\ldots,\;s_n)",
            font_size=58,
            color=WHITE
        )

        strategy_profile.move_to(DOWN * 0.2)

        self.play(
            TransformFromCopy(strategy_labels, strategy_profile),
            run_time=1.3,
            rate_func=smooth
        )

        self.wait(0.8)

        self.play(
            FadeOut(player_labels),
            FadeOut(strategy_labels),
            strategy_profile.animate.move_to(UP * 0.8),
            run_time=0.8,
            rate_func=smooth
        )

        # Focus on one player i


        general_profile = MathTex(
            r"(",
            r"s_i",
            r",",
            r"s_{-i}",
            r")",
            font_size=64
        )

        general_profile[1].set_color(RED)
        general_profile[3].set_color(BLUE)

        general_profile.move_to(strategy_profile)

        self.play(
            Transform(strategy_profile, general_profile),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(0.5)

        # labels && arrows
        player_i_label = FixedText(
            "Player i",
            font_size=25,
            color=RED
        ).next_to(strategy_profile[1], UP, buff=0.9)
        player_i_label.shift(LEFT * 0.3)

        others_label = FixedText(
            "Other players",
            font_size=25,
            color=BLUE
        ).next_to(strategy_profile[3], UP, buff=0.9)
        others_label.shift(RIGHT * 0.3)

        player_i_arrow = Arrow(
            start=player_i_label.get_bottom(),
            end=strategy_profile[1].get_top() + DOWN * 0.08,
            buff=0.15,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )

        others_arrow = Arrow(
            start=others_label.get_bottom(),
            end=strategy_profile[3].get_top() + DOWN * 0.08,
            buff=0.15,
            color=BLUE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            GrowArrow(player_i_arrow),
            FadeIn(player_i_label, shift=UP * 0.4),

            GrowArrow(others_arrow),
            FadeIn(others_label, shift=UP * 0.4),

            run_time=1
        )
        self.wait(1)

        # Construct player i's current payoff

        current_payoff = MathTex(
            r"u_i",
            r"(",
            r"s_i",
            r",",
            r"s_{-i}",
            r")",
            font_size=58
        )

        current_payoff[2].set_color(RED)
        current_payoff[4].set_color(BLUE)

        current_payoff.move_to(DOWN * 1.15)

        self.play(
            FadeOut(player_i_arrow),
            FadeOut(player_i_label),
            FadeOut(others_arrow),
            FadeOut(others_label),
            TransformFromCopy(strategy_profile, current_payoff),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(0.7)

        # Show deviation

        deviation_payoff = MathTex(
            r"u_i",
            r"(",
            r"s'_i",
            r",",
            r"s_{-i}",
            r")",
            font_size=58
        )

        deviation_payoff[2].set_color(RED)
        deviation_payoff[4].set_color(BLUE)

        deviation_payoff.move_to(RIGHT * 3.5 + DOWN * 1.15)

        current_payoff_target = current_payoff.copy()
        current_payoff_target.move_to(LEFT * 3.5 + DOWN * 1.15)

        self.play(
            Transform(current_payoff, current_payoff_target),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            TransformFromCopy(current_payoff, deviation_payoff),
            run_time=1.1,
            rate_func=smooth
        )

        # pulse
        self.play(
            Indicate(
                deviation_payoff[2],
                color=RED,
                scale_factor=1.25
            ),
            run_time=0.8
        )

        # Emphasis on everybody else's strategies remain unchanged
        fixed_others_left = SurroundingRectangle(
            current_payoff[4],
            color=BLUE,
            stroke_width=3,
            buff=0.08
        )

        fixed_others_right = SurroundingRectangle(
            deviation_payoff[4],
            color=BLUE,
            stroke_width=3,
            buff=0.08
        )

        self.play(
            Create(fixed_others_left),
            Create(fixed_others_right),
            run_time=0.7
        )

        self.wait(0.8)

        # Nash equilibrium inequality

        greater_equal = MathTex(
            r"\geq",
            font_size=70,
            color=YELLOW
        )

        greater_equal.move_to(DOWN * 1.15)

        self.play(
            FadeIn(greater_equal, scale=0.5),
            FadeOut(fixed_others_left),
            FadeOut(fixed_others_right),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(1)

        quantifier = MathTex(
            r"\text{for every player } i"
            r"\text{ and every alternative strategy } s'_i",
            font_size=34,
            color=WHITE
        )

        quantifier.next_to(
            VGroup(current_payoff, greater_equal, deviation_payoff),
            DOWN,
            buff=0.65
        )

        self.play(
            FadeIn(quantifier, shift=UP * 0.15),
            run_time=1
        )

        self.wait(1)

        #definition

        definition_formula = MathTex(
            r"u_i",
            r"(",
            r"s_i",
            r",",
            r"s_{-i}",
            r")",
            r"\geq",
            r"u_i",
            r"(",
            r"s'_i",
            r",",
            r"s_{-i}",
            r")",
            font_size=58
        )

        definition_formula[2].set_color(RED)
        definition_formula[4].set_color(BLUE)
        definition_formula[6].set_color(YELLOW)
        definition_formula[9].set_color(RED)
        definition_formula[11].set_color(BLUE)

        definition_formula.move_to(ORIGIN)

        definition_title = FixedText(
            "Nash Equilibrium",
            font_size=44,
            weight=BOLD,
            color=YELLOW
        )

        definition_title.next_to(
            definition_formula,
            UP,
            buff=0.65
        )

        meaning = FixedText(
            "No player can improve by changing alone",
            font_size=31,
            color=WHITE
        )

        meaning.next_to(
            definition_formula,
            DOWN,
            buff=0.65
        )

        self.play(
            FadeOut(formal_title),
            FadeOut(strategy_profile),
            FadeOut(quantifier),
            Transform(
                VGroup(
                    current_payoff,
                    greater_equal,
                    deviation_payoff
                ),
                definition_formula
            ),
            FadeIn(definition_title, shift=DOWN * 0.15),
            run_time=1.4,
            rate_func=smooth
        )

        self.play(
            FadeIn(meaning, shift=UP * 0.15),
            run_time=0.8
        )

        self.wait(2)

        formal_definition_group = VGroup(
            definition_title,
            definition_formula,
            meaning
        )

        self.play(
            FadeOut(formal_definition_group),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.4)

        self.play(
            FadeOut(definition_formula),
            run_time=0.8,
            rate_func=smooth
        )
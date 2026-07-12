from manim import *
from FixedText import *



class BimatrixGames(Scene):
    def construct(self):
        alice_image = SVGMobject("../Images-Icons/alice.svg").scale(1.5)
        bob_image = SVGMobject("../Images-Icons/bob.svg").scale(1.5)
        alice_image.shift(LEFT * 4)
        bob_image.shift(RIGHT * 4)
        # CAPTION 1 == PLAYER NAMES
        alice_caption1 = FixedText("Alice", font_size=50, weight=BOLD,color=RED)
        bob_caption1 = FixedText("Bob", font_size=50, weight=BOLD,color=BLUE)
        alice_caption1.move_to(alice_image.get_center() + UP * 2)
        bob_caption1.move_to(bob_image.get_center() + UP * 2)
        # CAPTION 2 == PLAYER FAVORED COMPOSER
        alice_caption2 = FixedText("Bach", font_size=50, weight=BOLD,color=WHITE)
        bob_caption2 = FixedText("Stravinsky", font_size=50, weight=BOLD,color=WHITE)
        alice_caption2.move_to(alice_image.get_center() + DOWN * 2)
        bob_caption2.move_to(bob_image.get_center() + DOWN * 2)
        # group em
        alice_group = VGroup(alice_image, alice_caption1,alice_caption2)
        bob_group = VGroup(bob_image, bob_caption1,bob_caption2)
        self.play(FadeIn(alice_group), FadeIn(bob_group), run_time=3.5)
        self.wait(3)

        # Move images to corners 
        self.play(
            alice_image.animate.scale(0.35).to_corner(UL, buff=0.6),
            bob_image.animate.scale(0.35).to_corner(UR, buff=0.6),
            run_time=2,
            rate_func=smooth,
        )

      
        # power outage effect
        power_line = Line(
            start=LEFT * 5.2 + UP * 2.8,
            end=RIGHT * 5.2 + UP * 2.8,
            color=YELLOW,
            stroke_width=6
        )

        spark1 = Flash(
            power_line.get_center() + LEFT * 1.5,
            color=YELLOW,
            flash_radius=0.35,
            line_length=0.18,
            num_lines=8
        )

        spark2 = Flash(
            power_line.get_center() + RIGHT * 1.2,
            color=YELLOW,
            flash_radius=0.35,
            line_length=0.18,
            num_lines=8
        )

        blackout = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.75,
            stroke_opacity=0
        )

        self.play(
            Create(power_line),
            run_time=0.6
        )

        self.play(
            spark1,
            power_line.animate.set_color(RED),
            run_time=0.35
        )

        self.play(
            spark2,
            power_line.animate.set_color(YELLOW),
            run_time=0.35
        )

        self.play(
            blackout.animate.set_fill(opacity=0.75),
            FadeIn(blackout),
            run_time=0.25
        )

        self.wait(0.25)

        self.play(
            FadeOut(blackout),
            FadeOut(power_line),
            run_time=0.5
        )
        
        
        
        # MATRIX DATA
        

        payoff_data = [
            [(3, 2), (1, 1)],
            [(0, 0), (2, 3)]
        ]

        cell_width = 3.2
        cell_height = 1.8

        grid = VGroup()
        cells = []

        #3x3 matrix cells
        for i in range(3):
            row = []

            for j in range(3):
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    color=WHITE
                )

                cell.move_to(RIGHT * j * cell_width + DOWN * i * cell_height)
                grid.add(cell)
                row.append(cell)

            cells.append(row)

        grid.move_to(DOWN * 0.3)

        matrix_box = SurroundingRectangle(
            grid,
            buff=0.2,
            color=WHITE
        )

        
        alice_caption1.generate_target()
        bob_caption1.generate_target()

        alice_caption1.target.rotate(PI / 2)
        alice_caption1.target.next_to(grid, LEFT, buff=0.8)

        bob_caption1.target.next_to(grid, UP, buff=0.8)

        
        alice_caption2.generate_target()
        bob_caption2.generate_target()

        
        alice_caption2.target.move_to(cells[1][0].get_center())
        bob_caption2.target.move_to(cells[0][2].get_center())

        alice_Stravinsky_row = FixedText(
            "Stravinsky",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        bob_Bach_col = FixedText(
            "Bach",
            font_size=50,
            weight=BOLD,
            color=WHITE
        )

        alice_Stravinsky_row.move_to(cells[2][0].get_center())
        bob_Bach_col.move_to(cells[0][1].get_center())

        
        self.play(
            MoveToTarget(alice_caption1),
            MoveToTarget(bob_caption1),
            MoveToTarget(alice_caption2),
            MoveToTarget(bob_caption2),
            FadeIn(alice_Stravinsky_row, shift=DOWN * 0.2),
            FadeIn(bob_Bach_col, shift=DOWN * 0.2),
            run_time=2,
            rate_func=smooth,
        )

        self.wait(0.5)


        self.play(
            LaggedStart(
                *[Create(cell) for cell in grid],
                lag_ratio=0.06
            ),
            Create(matrix_box),
            run_time=2,
            rate_func=smooth,
        )

        #payoff values

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
                    color=WHITE
                )

                comma = FixedText(
                    ",",
                    font_size=50,
                    color=WHITE
                )

                bob_score = FixedText(
                    str(bob_val),
                    font_size=50,
                    color=WHITE
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

        self.play(
            LaggedStart(
                *[
                    FadeIn(entry, scale=0.8)
                    for entry in payoff_entries
                ],
                lag_ratio=0.15
            ),
            run_time=2,
            rate_func=smooth,
        )

        self.wait(1)

        self.wait()

        #surrounding rectangle for each row
        alice_row_1 = VGroup(
            cells[1][1],
            cells[1][2]
        )

        alice_row_2 = VGroup(
            cells[2][1],
            cells[2][2]
        )

        alice_row_rect_1 = SurroundingRectangle(
            alice_row_1,
            color=RED,
            stroke_width=4,
            buff=0.05
        )

        alice_row_rect_2 = SurroundingRectangle(
            alice_row_2,
            color=RED,
            stroke_width=4,
            buff=0.05
        )


        self.play(
            Create(alice_row_rect_1),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            Create(alice_row_rect_2),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(2)
        self.play(
            FadeOut(alice_row_rect_1),
            FadeOut(alice_row_rect_2),
            run_time=0.5
        )

        self.wait(2)

    # surrounding rectangle for each column
        bob_col_1 = VGroup(
            cells[1][1],
            cells[2][1]
        )

        bob_col_2 = VGroup(
            cells[1][2],
            cells[2][2]
        )

        bob_col_rect_1 = SurroundingRectangle(
            bob_col_1,
            color=BLUE,
            stroke_width=4,
            buff=0.05
        )

        bob_col_rect_2 = SurroundingRectangle(
            bob_col_2,
            color=BLUE,
            stroke_width=4,
            buff=0.05
        )

        self.play(
            Create(bob_col_rect_1),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            Create(bob_col_rect_2),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(2)
        self.play(
            FadeOut(bob_col_rect_1),
            FadeOut(bob_col_rect_2),
            run_time=0.5
        )

        # change payoff colors
        self.play(
            *[
                score.animate.set_color(RED)
                for score in alice_scores
            ],
            run_time=1.5,
            rate_func=smooth,
        )

        self.wait(1)

        self.play(
            *[
                score.animate.set_color(BLUE)
                for score in bob_scores
            ],
            run_time=1.5,
            rate_func=smooth,
        )

        
        # both choose bach
        

        bach_bach_cell = cells[1][1]
        bach_bach_payoff = payoff_entries[0]

        bach_highlight = SurroundingRectangle(
            bach_bach_cell,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        self.play(
            Create(bach_highlight),
            run_time=0.8,
            rate_func=smooth
        )

        
        alice_three = bach_bach_payoff[1]
        bob_two = bach_bach_payoff[3]

        # Alice's payoff first
        self.play(
            Indicate(
                alice_three,
                color=RED,
                scale_factor=1.35
            ),
            run_time=1
        )

        # Then Bob's payoff
        self.play(
            Indicate(
                bob_two,
                color=BLUE,
                scale_factor=1.35
            ),
            run_time=1
        )

        
        self.wait(0.5)

       # highlight off diagonal cells

        different_cell_1 = cells[1][2]  # Alice Bach, Bob Stravinsky: (1, 1)
        different_cell_2 = cells[2][1]  # Alice Stravinsky, Bob Bach: (0, 0)

        different_highlight_1 = SurroundingRectangle(
            different_cell_1,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        different_highlight_2 = SurroundingRectangle(
            different_cell_2,
            color=YELLOW,
            stroke_width=6,
            buff=-0.04
        )

        # Two copies begin at the top-left cell
        moving_highlight_1 = bach_highlight.copy()
        moving_highlight_2 = bach_highlight.copy()

        self.add(moving_highlight_1, moving_highlight_2)

        self.play(
            FadeOut(bach_highlight),
            Transform(moving_highlight_1, different_highlight_1),
            Transform(moving_highlight_2, different_highlight_2),
            run_time=1.4,
            rate_func=smooth
        )

        self.wait(0.5)
        self.play(
            FadeOut(moving_highlight_1),
            FadeOut(moving_highlight_2),
            run_time=0.5
        )

        # Alice's available choices
        alice_choice_1 = SurroundingRectangle(
            cells[1][0],
            color=RED,
            stroke_width=5,
            buff=-0.04
        )

        alice_choice_2 = SurroundingRectangle(
            cells[2][0],
            color=RED,
            stroke_width=5,
            buff=-0.04
        )

        # Bob's available choices
        bob_choice_1 = SurroundingRectangle(
            cells[0][1],
            color=BLUE,
            stroke_width=5,
            buff=-0.04
        )

        bob_choice_2 = SurroundingRectangle(
            cells[0][2],
            color=BLUE,
            stroke_width=5,
            buff=-0.04
        )

        self.play(
            LaggedStart(
                Create(alice_choice_1),
                Create(alice_choice_2),
                lag_ratio=0.2
            ),
            run_time=1.2
        )

        self.play(
            LaggedStart(
                Create(bob_choice_1),
                Create(bob_choice_2),
                lag_ratio=0.2
            ),
            run_time=1.2
        )

        self.play(
        FadeOut(alice_choice_1),
        FadeOut(alice_choice_2),
        FadeOut(bob_choice_1),
        FadeOut(bob_choice_2),
        run_time=0.4
    )
        
        self.play(
            Indicate(alice_scores[0], color=RED, scale_factor=1.3),
            run_time=1.2
        )

        self.play(
            Indicate(bob_scores[3], color=BLUE, scale_factor=1.3),
            run_time=1.2
        )

        # split the bimatrix into two separate matrices

        self.wait(1)

        small_cell_width = 1.55
        small_cell_height = 1.25


        def create_payoff_grid(center):
            new_grid = VGroup()
            new_cells = []

            for i in range(2):
                row = []

                for j in range(2):
                    cell = Rectangle(
                        width=small_cell_width,
                        height=small_cell_height,
                        color=WHITE,
                        stroke_width=2
                    )

                    cell.move_to(
                        RIGHT * j * small_cell_width
                        + DOWN * i * small_cell_height
                    )

                    new_grid.add(cell)
                    row.append(cell)

                new_cells.append(row)

            new_grid.move_to(center)

            return new_grid, new_cells


        # group the original bimatrix elements
        
        original_bimatrix = VGroup(
            grid,
            matrix_box,
            payoff_entries,
            alice_caption1,
            bob_caption1,
            alice_caption2,
            bob_caption2,
            alice_Stravinsky_row,
            bob_Bach_col
        )

        
        alice_payoff_grid, alice_payoff_cells = create_payoff_grid(
            LEFT * 3.2 + DOWN * 0.25
        )

        bob_payoff_grid, bob_payoff_cells = create_payoff_grid(
            RIGHT * 3.2 + DOWN * 0.25
        )

        alice_matrix_title = FixedText(
            "Alice's payoff matrix",
            font_size=30,
            weight=BOLD,
            color=RED
        )

        bob_matrix_title = FixedText(
            "Bob's payoff matrix",
            font_size=30,
            weight=BOLD,
            color=BLUE
        )

        alice_matrix_title.next_to(
            alice_payoff_grid,
            UP,
            buff=0.45
        )

        bob_matrix_title.next_to(
            bob_payoff_grid,
            UP,
            buff=0.45
        )

        
        alice_split_values = VGroup()
        bob_split_values = VGroup()

        for index in range(4):
            row = index // 2
            column = index % 2

            alice_value = alice_scores[index].copy()
            bob_value = bob_scores[index].copy()

            alice_value.move_to(alice_scores[index].get_center())
            bob_value.move_to(bob_scores[index].get_center())

            alice_split_values.add(alice_value)
            bob_split_values.add(bob_value)

       
        self.add(alice_split_values, bob_split_values)

        

        self.play(
            FadeOut(original_bimatrix),
            run_time=0.6,
            rate_func=smooth
        )

       

        move_to_split_positions = []

        for index in range(4):
            row = index // 2
            column = index % 2

            move_to_split_positions.append(
                alice_split_values[index].animate.move_to(
                    alice_payoff_cells[row][column].get_center()
                )
            )

            move_to_split_positions.append(
                bob_split_values[index].animate.move_to(
                    bob_payoff_cells[row][column].get_center()
                )
            )

        self.play(
            LaggedStart(
                *[Create(cell) for cell in alice_payoff_grid],
                lag_ratio=0.08
            ),
            LaggedStart(
                *[Create(cell) for cell in bob_payoff_grid],
                lag_ratio=0.08
            ),
            FadeIn(alice_matrix_title, shift=DOWN * 0.15),
            FadeIn(bob_matrix_title, shift=DOWN * 0.15),
            AnimationGroup(
                *move_to_split_positions,
                lag_ratio=0.04
            ),
            run_time=2.2,
            rate_func=smooth
        )

        self.wait(2)

        # recombine the split matrices back into the original bimatrix

        return_animations = []

        for index in range(4):
            return_animations.append(
                alice_split_values[index].animate.move_to(
                    alice_scores[index].get_center()
                )
            )

            return_animations.append(
                bob_split_values[index].animate.move_to(
                    bob_scores[index].get_center()
                )
            )

        self.play(
            AnimationGroup(
                *return_animations,
                lag_ratio=0.04
            ),
            FadeOut(alice_payoff_grid),
            FadeOut(bob_payoff_grid),
            FadeOut(alice_matrix_title, shift=UP * 0.15),
            FadeOut(bob_matrix_title, shift=UP * 0.15),
            run_time=2.2,
            rate_func=smooth
        )

        
        self.play(
            FadeIn(original_bimatrix),
            FadeOut(alice_split_values),
            FadeOut(bob_split_values),
            run_time=0.6,
            rate_func=smooth
        )

       
        self.remove(
            alice_split_values,
            bob_split_values,
            alice_payoff_grid,
            bob_payoff_grid,
            alice_matrix_title,
            bob_matrix_title
        )

        self.wait(1)

        self.play(
            FadeOut(original_bimatrix),
            run_time=0.6,
            rate_func=smooth
        )


        # General strategy idea
        strategy_title=FixedText("Strategies", font_size=44, weight=BOLD, color=WHITE)
        state_box = RoundedRectangle(width=2.4, height=1.0)
        rule_box = RoundedRectangle(width=2.8, height=1.0)
        action_box = RoundedRectangle(width=2.4, height=1.0)

        state_text = FixedText("Game state", font_size=30)
        rule_text = FixedText("Rule / algorithm", font_size=30)
        action_text = FixedText("Action", font_size=30)

        state_group = VGroup(state_box, state_text)
        rule_group = VGroup(rule_box, rule_text)
        action_group = VGroup(action_box, action_text)

        

        state_text.move_to(state_box)
        rule_text.move_to(rule_box)
        action_text.move_to(action_box)

        strategy_flow = VGroup(
            state_group,
            rule_group,
            action_group
        ).arrange(RIGHT, buff=0.9)

        strategy_title.move_to(strategy_flow.get_center() + UP * 2.5)

        arrow_1 = Arrow(
            state_group.get_right(),
            rule_group.get_left(),
            buff=0.1
        )

        arrow_2 = Arrow(
            rule_group.get_right(),
            action_group.get_left(),
            buff=0.1
        )

        self.play(
            FadeIn(strategy_title),
            FadeIn(state_group),
            GrowArrow(arrow_1),
            FadeIn(rule_group),
            GrowArrow(arrow_2),
            FadeIn(action_group),
            run_time=2
        )

        self.wait(1)


        
        strategy_equals_choice = FixedText(
            "Strategy = Choice",
            font_size=44,
            weight=BOLD,
            color=YELLOW
        )

        strategy_equals_choice.move_to(strategy_flow.get_center()+DOWN * 1.5)

        self.play(
            FadeIn(strategy_equals_choice, scale=0.8),
            run_time=1.3
        )

        self.wait(1)

        self.play(
            FadeOut(strategy_title),
            FadeOut(state_group),
            FadeOut(rule_group),
            FadeOut(action_group),
            FadeOut(arrow_1),
            FadeOut(arrow_2),
            FadeOut(strategy_equals_choice),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.5)
        self.play(
            FadeIn(original_bimatrix),
            run_time=0.5,
            rate_func=smooth
        )

        alice_bach_cell = cells[1][0]
        bob_bach_cell = cells[0][1]

        self.play(
            alice_bach_cell.animate.set_fill(RED, opacity=0.35),
            bob_bach_cell.animate.set_fill(BLUE, opacity=0.35),
            run_time=1,
            rate_func=smooth,
        )

        self.wait(1)

        alice_stravinsky_cell = cells[2][0]
        bob_stravinsky_cell = cells[0][2]

        self.play(
            alice_stravinsky_cell.animate.set_fill(RED, opacity=0.35),
            bob_stravinsky_cell.animate.set_fill(BLUE, opacity=0.35),
            run_time=1,
            rate_func=smooth,
        )


        self.wait(1)
        self.play(
            alice_bach_cell.animate.set_fill(opacity=0),
            bob_bach_cell.animate.set_fill(opacity=0),
            alice_stravinsky_cell.animate.set_fill(opacity=0),
            bob_stravinsky_cell.animate.set_fill(opacity=0),
            run_time=1,
            rate_func=smooth,
        )

        self.wait(1)

        profiles = [
            (cells[1][1], "Strategy Profile: (Alice:Bach, Bob:Bach)"),
            (cells[1][2], "Strategy Profile: (Alice:Bach, Bob:Stravinsky)"),
            (cells[2][1], "Strategy Profile: (Alice:Stravinsky, Bob:Bach)"),
            (cells[2][2], "Strategy Profile: (Alice:Stravinsky, Bob:Stravinsky)")
        ]

        # Initial arrow
        arrow = Arrow(
            start=profiles[0][0].get_top() + UP * 0.8,
            end=profiles[0][0].get_top(),
            color=YELLOW,
            stroke_width=8,
            buff=0.1
        )

        label = FixedText(
            profiles[0][1],
            font_size=32,
            weight=BOLD,
            color=YELLOW
        )

        label.next_to(grid, DOWN, buff=0.4)

        self.play(
            GrowArrow(arrow),
            FadeIn(label),
            run_time=0.8
        )

        self.wait(0.7)

        for cell, text in profiles[1:]:

            new_arrow = Arrow(
                start=cell.get_top() + UP * 0.8,
                end=cell.get_top(),
                color=YELLOW,
                stroke_width=8,
                buff=0.1
            )

            new_label = FixedText(
                text,
                font_size=32,
                weight=BOLD,
                color=YELLOW
            )

            new_label.move_to(label)

            self.play(
                Transform(arrow, new_arrow),
                Transform(label, new_label),
                run_time=0.8,
                rate_func=smooth
            )

            self.wait(0.7)

        self.play(
            FadeOut(arrow),
            FadeOut(label),
            run_time=0.5
        )
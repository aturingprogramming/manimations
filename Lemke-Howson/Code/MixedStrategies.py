from manim import*
from FixedText import*
from manim.utils.rate_functions import ease_in_out_sine

class MixedStrategies(Scene):
    def make_strategy_box(
        self,
        label_text,
        center,
        width=2.25,
        height=0.72,
    ):
        rectangle = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=WHITE,
            stroke_width=2.5,
            fill_opacity=0,
        )

        label = FixedText(
            label_text,
            font_size=26,
            weight=BOLD,
            color=WHITE,
        )

        label.move_to(rectangle)

        strategy_box = VGroup(
            rectangle,
            label,
        )

        strategy_box.move_to(center)

        return strategy_box

    # ============================================================
    # Roulette
    # ============================================================

    def make_roulette(
        self,
        center,
        scale_factor=0.82,
    ):
        roulette_circle = Circle(
            radius=1.05,
            color=WHITE,
            stroke_width=3,
        )

        roulette_circle.move_to(center)

        roulette_divider = Line(
            roulette_circle.get_top(),
            roulette_circle.get_bottom(),
            color=WHITE,
            stroke_width=2,
        )

        roulette_bach = FixedText(
            "Bach",
            font_size=26,
            weight=BOLD,
            color=WHITE,
        )

        roulette_stravinsky = FixedText(
            "Stravinsky",
            font_size=22,
            weight=BOLD,
            color=WHITE,
        )

        roulette_bach.move_to(
            roulette_circle.get_center()
            + LEFT * 0.52
        )

        roulette_stravinsky.move_to(
            roulette_circle.get_center()
            + RIGHT * 0.52
        )

        roulette_stravinsky.rotate(PI / 2)

        roulette_center = Dot(
            point=roulette_circle.get_center(),
            radius=0.08,
            color=YELLOW,
        )

        roulette_pointer = Arrow(
            start=roulette_circle.get_center(),
            end=roulette_circle.get_center() + UP * 0.78,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.22,
        )

        roulette_body = VGroup(
            roulette_circle,
            roulette_divider,
            roulette_bach,
            roulette_stravinsky,
            roulette_center,
        )

        roulette = VGroup(
            roulette_body,
            roulette_pointer,
        )

        roulette.scale(
            scale_factor,
            about_point=center,
        )

        return {
            "group": roulette,
            "body": roulette_body,
            "circle": roulette_circle,
            "pointer": roulette_pointer,
            "center": roulette_circle.get_center(),
        }

    # ============================================================
    # Pointer angle
    # ============================================================

    def get_pointer_spin_angle(
        self,
        current_angle,
        result,
        full_turns=2,
    ):

        if result == "B":
            target_angle = PI / 2
        else:
            target_angle = -PI / 2

        current_modulo = current_angle % TAU

        correction = (
            target_angle - current_modulo
        ) % TAU

        return full_turns * TAU + correction

    # ============================================================
    # Ball destination positions
    # ============================================================

    def get_ball_destination(
        self,
        strategy_box,
        index,
    ):
        
        horizontal_offsets = [
            -0.18,
            0.18,
            -0.54,
            0.54,
        ]

        return (
            strategy_box.get_bottom()
            + DOWN * 0.34
            + RIGHT * horizontal_offsets[index]
        )

    # ============================================================
    # Curved ball trajectory
    # ============================================================

    def make_flight_path(
        self,
        start,
        end,
        curve_direction,
    ):
        control_point_1 = (
            start
            + UP * 0.45
            + curve_direction * RIGHT * 0.35
        )

        control_point_2 = (
            end
            + DOWN * 0.45
            - curve_direction * RIGHT * 0.2
        )

        return CubicBezier(
            start,
            control_point_1,
            control_point_2,
            end,
        )
    
    def make_probability_bar(
        self,
        center,
        player_color,
        initial_bach_probability=1.0,
        bar_width=4.45,
        bar_height=0.72,
    ):

        probability = ValueTracker(
            initial_bach_probability
        )

        bar_outline = RoundedRectangle(
            width=bar_width,
            height=bar_height,
            corner_radius=0.12,
            color=WHITE,
            stroke_width=3,
            fill_opacity=0,
        )

        bar_outline.move_to(center)
        bar_outline.set_z_index(3)

        bach_label = FixedText(
            "Bach",
            font_size=25,
            weight=BOLD,
            color=WHITE,
        )

        stravinsky_label = FixedText(
            "Stravinsky",
            font_size=25,
            weight=BOLD,
            color=WHITE,
        )

        bach_label.next_to(
            bar_outline,
            UP,
            buff=0.25,
        ).align_to(
            bar_outline,
            LEFT,
        )

        stravinsky_label.next_to(
            bar_outline,
            UP,
            buff=0.25,
        ).align_to(
            bar_outline,
            RIGHT,
        )

        def get_bach_color():
            return player_color

        def get_stravinsky_color():
            return BLACK

        bach_fill = always_redraw(
            lambda: Rectangle(
                width=max(
                    0.001,
                    bar_width * probability.get_value(),
                ),
                height=bar_height - 0.05,
                stroke_width=0,
                fill_color=get_bach_color(),
                fill_opacity=0.85,
            ).move_to(
                bar_outline.get_left()
                + RIGHT
                * (
                    bar_width
                    * probability.get_value()
                    / 2
                )
            ).set_z_index(1)
        )

        stravinsky_fill = always_redraw(
            lambda: Rectangle(
                width=max(
                    0.001,
                    bar_width
                    * (
                        1
                        - probability.get_value()
                    ),
                ),
                height=bar_height - 0.05,
                stroke_width=0,
                fill_color=get_stravinsky_color(),
                fill_opacity=0.85,
            ).move_to(
                bar_outline.get_right()
                + LEFT
                * (
                    bar_width
                    * (
                        1
                        - probability.get_value()
                    )
                    / 2
                )
            ).set_z_index(1)
        )

        divider = always_redraw(
            lambda: Line(
                start=bar_outline.get_bottom()
                + RIGHT
                * (
                    bar_width
                    * probability.get_value()
                    - bar_width / 2
                ),
                end=bar_outline.get_top()
                + RIGHT
                * (
                    bar_width
                    * probability.get_value()
                    - bar_width / 2
                ),
                color=WHITE,
                stroke_width=3,
            ).set_z_index(4)
        )

        bach_percentage = always_redraw(
            lambda: FixedText(
                f"{round(100 * probability.get_value())}%",
                font_size=28,
                weight=BOLD,
                color=WHITE,
            ).next_to(
                bar_outline,
                DOWN,
                buff=0.24,
            ).align_to(
                bar_outline,
                LEFT,
            )
        )

        stravinsky_percentage = always_redraw(
            lambda: FixedText(
                f"{round(100 * (1 - probability.get_value()))}%",
                font_size=28,
                weight=BOLD,
                color=WHITE,
            ).next_to(
                bar_outline,
                DOWN,
                buff=0.24,
            ).align_to(
                bar_outline,
                RIGHT,
            )
        )

        fills = VGroup(
            bach_fill,
            stravinsky_fill,
        )

        static_objects = VGroup(
            bach_label,
            stravinsky_label,
            bar_outline,
        )

        dynamic_objects = VGroup(
            divider,
            bach_percentage,
            stravinsky_percentage,
        )

        complete_bar = VGroup(
            fills,
            static_objects,
            dynamic_objects,
        )

        return {
            "group": complete_bar,
            "fills": fills,
            "static": static_objects,
            "dynamic": dynamic_objects,
            "outline": bar_outline,
            "tracker": probability,
        }
    

    #ROCK-PAPER-SCISSORS
    
    def make_rock(self):
            blobs = VGroup(
            Circle(radius=0.25).shift(LEFT*0.2+UP*0.1),
            Circle(radius=0.3).shift(RIGHT*0.2),
            Circle(radius=0.2).shift(DOWN*0.2)
            )
            blobs.set_fill('#595959', opacity=0.9).set_stroke(BLACK, width=2)
            return blobs


    def make_paper(self):
        rect = Rectangle(height=1.0, width=0.8, color=WHITE)
        rect.set_fill(WHITE, opacity=0.9).set_stroke(BLACK, width=2)
        return rect


    def make_scissors(self):
        blade1 = Line(ORIGIN, UP*0.6+RIGHT*0.3, color=GRAY, stroke_width=7)
        blade2 = Line(ORIGIN, UP*0.6+LEFT*0.3, color=GRAY, stroke_width=7)
        handle1 = Circle(radius=0.15, color="#BA2A14",stroke_width=5).shift(DOWN*0.18+LEFT*0.18)
        handle2 = Circle(radius=0.15, color="#BA2A14",stroke_width=5).shift(DOWN*0.18+RIGHT*0.18)
        return VGroup(blade1, blade2, handle1, handle2)
    
    def frame_move(self,move, size=(1.5, 1.3)):
        w, h = size
        frame = Rectangle(width=w, height=h, stroke_opacity=0).move_to(move)
        return VGroup(frame, move), frame
    
    

    
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

        # strategy rectangles

        strategy_y = 0.7
        deterministic_title = FixedText(
            "Deterministic Choices",
            font_size=42,
            weight=BOLD,
            color=WHITE
        )

        deterministic_title.to_edge(UP, buff=0.55)
        alice_bach = self.make_strategy_box(
            "Bach",
            center=LEFT * 4.5 + UP * strategy_y,
        )

        alice_stravinsky = self.make_strategy_box(
            "Stravinsky",
            center=LEFT * 2.05 + UP * strategy_y,
        )

        bob_bach = self.make_strategy_box(
            "Bach",
            center=RIGHT * 2.05 + UP * strategy_y,
        )

        bob_stravinsky = self.make_strategy_box(
            "Stravinsky",
            center=RIGHT * 4.5 + UP * strategy_y,
        )

        strategy_boxes = VGroup(
            alice_bach,
            alice_stravinsky,
            bob_bach,
            bob_stravinsky,
        )

       
        for strategy_box in strategy_boxes:
            strategy_box.set_y(strategy_y)

        self.play(
            FadeIn(deterministic_title),
            LaggedStart(
                *[
                    FadeIn(
                        strategy_box,
                        shift=UP * 0.12,
                    )
                    for strategy_box in strategy_boxes
                ],
                lag_ratio=0.08,
            ),
            run_time=0.9,
            rate_func=smooth,
        )

        self.wait(0.25)

        alice_choices = VGroup(alice_bach, alice_stravinsky)
        bob_choices = VGroup(bob_bach, bob_stravinsky)

        alice_target = alice_choices.get_top() + UP * 0.70
        bob_target = bob_choices.get_top() + UP * 0.70

        self.play(
            alice_image.animate.move_to(alice_target),
            bob_image.animate.move_to(bob_target),
            run_time=1.0,
            rate_func=smooth,
        )

        # deterministic choices

        alice_selector = Dot(
            radius=0.12,
            color=RED,
        )

        bob_selector = Dot(
            radius=0.12,
            color=BLUE,
        )

        alice_selector.move_to(
            alice_bach.get_bottom()
            + DOWN * 0.34
        )

        bob_selector.move_to(
            bob_stravinsky.get_bottom()
            + DOWN * 0.34
        )

        self.play(
            GrowFromCenter(alice_selector),
            GrowFromCenter(bob_selector),
            run_time=0.45,
        )

        self.wait(0.25)

        # switch

        self.play(
            alice_selector.animate.move_to(
                alice_stravinsky.get_bottom()
                + DOWN * 0.34
            ),
            bob_selector.animate.move_to(
                bob_bach.get_bottom()
                + DOWN * 0.34
            ),
            run_time=0.85,
            rate_func=smooth,
        )

        self.wait(0.25)

        # switch back

        self.play(
            alice_selector.animate.move_to(
                alice_bach.get_bottom()
                + DOWN * 0.34
            ),
            bob_selector.animate.move_to(
                bob_stravinsky.get_bottom()
                + DOWN * 0.34
            ),
            run_time=0.85,
            rate_func=smooth,
        )

        self.wait(0.35)


        self.play(
            FadeOut(alice_selector, scale=0.5),
            FadeOut(bob_selector, scale=0.5),
            FadeOut(deterministic_title),
            FadeOut(strategy_boxes),
            run_time=0.65,
            rate_func=smooth,
        )

        random_title = FixedText(
            "Why Choose Randomly?",
            font_size=42,
            weight=BOLD,
            color=WHITE,
        )
        random_title.to_edge(UP, buff=0.55)

        central_roulette = self.make_roulette(
            center=DOWN * 1.25,
            scale_factor=1.45,
        )

        self.play(
            FadeIn(random_title),
            FadeIn(
                central_roulette["body"],
                shift=UP * 0.18,
            ),
            GrowArrow(central_roulette["pointer"]),
            run_time=1.0,
            rate_func=smooth,
        )

        self.wait(0.35)

        central_spin_angle = self.get_pointer_spin_angle(
            current_angle=0,
            result="S",
            full_turns=5,
        )

        self.play(
            Rotate(
                central_roulette["pointer"],
                angle=central_spin_angle,
                about_point=central_roulette["center"],
                rate_func=rate_functions.ease_out_cubic,
            ),
            run_time=2.2,
        )

        self.wait(0.85)

        self.play(
            FadeOut(random_title),
            FadeOut(central_roulette["group"]),
            run_time=0.7,
            rate_func=smooth,
        )

        
        distribution_title = FixedText(
            "A Distribution Over Choices",
            font_size=42,
            weight=BOLD,
            color=WHITE,
        )
        distribution_title.to_edge(UP, buff=0.55)

        alice_bar = self.make_probability_bar(
            center=LEFT * 3.25 + UP * 0.55,
            player_color=RED,
            initial_bach_probability=1.0,
            bar_width=4.45,
            bar_height=0.72,
        )

        bob_bar = self.make_probability_bar(
            center=RIGHT * 3.25 + UP * 0.55,
            player_color=BLUE,
            initial_bach_probability=1.0,
            bar_width=4.45,
            bar_height=0.72,
        )

        self.play(
            FadeIn(distribution_title),
            FadeIn(alice_bar["static"], shift=UP * 0.1),
            FadeIn(bob_bar["static"], shift=UP * 0.1),
            run_time=0.9,
            rate_func=smooth,
        )

        self.add(
            alice_bar["fills"],
            bob_bar["fills"],
        )

        self.play(
            FadeIn(alice_bar["dynamic"]),
            FadeIn(bob_bar["dynamic"]),
            run_time=0.55,
            rate_func=smooth,
        )

        self.wait(0.7)

        
        self.play(
            alice_bar["tracker"].animate.set_value(0.70),
            bob_bar["tracker"].animate.set_value(0.30),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.65)

        
        self.play(
            alice_bar["tracker"].animate.set_value(0.30),
            bob_bar["tracker"].animate.set_value(0.70),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.65)

        
        self.play(
            alice_bar["tracker"].animate.set_value(0.60),
            bob_bar["tracker"].animate.set_value(0.40),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.65)

        
        self.play(
            alice_bar["tracker"].animate.set_value(0.50),
            bob_bar["tracker"].animate.set_value(0.50),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.85)

        self.play(
            alice_bar["tracker"].animate.set_value(0.30),
            bob_bar["tracker"].animate.set_value(0.70),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.85)

        self.play(
            FadeOut(distribution_title),
            FadeOut(alice_bar["group"]),
            FadeOut(bob_bar["group"]),
            run_time=0.8,
            rate_func=smooth,
        )


        # 2 roulletes


        random_outcomes_title = FixedText(
            "Random Outcomes",
            font_size=42,
            weight=BOLD,
            color=WHITE,
        )
        random_outcomes_title.to_edge(UP, buff=0.55)

        self.play(
            FadeIn(random_outcomes_title),
            LaggedStart(
                *[
                    FadeIn(box, shift=UP * 0.12)
                    for box in strategy_boxes
                ],
                lag_ratio=0.08,
            ),
            run_time=0.9,
            rate_func=smooth,
        )

        alice_roulette = self.make_roulette(
            center=LEFT * 3.25 + DOWN * 2.35,
            scale_factor=0.82,
        )

        bob_roulette = self.make_roulette(
            center=RIGHT * 3.25 + DOWN * 2.35,
            scale_factor=0.82,
        )

        self.play(
            FadeIn(alice_roulette["body"], shift=UP * 0.18),
            GrowArrow(alice_roulette["pointer"]),
            FadeIn(bob_roulette["body"], shift=UP * 0.18),
            GrowArrow(bob_roulette["pointer"]),
            run_time=1.1,
            rate_func=smooth,
        )

        self.wait(0.35)

        rounds = [
            ("B", "S"),
            ("B", "B"),
            ("S", "S"),
            ("B", "B"),
        ]

        alice_destinations = {
            "B": alice_bach,
            "S": alice_stravinsky,
        }

        bob_destinations = {
            "B": bob_bach,
            "S": bob_stravinsky,
        }

        alice_counts = {"B": 0, "S": 0}
        bob_counts = {"B": 0, "S": 0}

        alice_pointer_angle = 0
        bob_pointer_angle = 0

        alice_result_balls = VGroup()
        bob_result_balls = VGroup()

        for round_index, (
            alice_result,
            bob_result,
        ) in enumerate(rounds):

            if round_index == 0:
                alice_turns = 3
                bob_turns = 4
                spin_time = 1.35
            else:
                alice_turns = 2
                bob_turns = 2
                spin_time = 0.85

            alice_spin_angle = self.get_pointer_spin_angle(
                current_angle=alice_pointer_angle,
                result=alice_result,
                full_turns=alice_turns,
            )

            bob_spin_angle = self.get_pointer_spin_angle(
                current_angle=bob_pointer_angle,
                result=bob_result,
                full_turns=bob_turns,
            )

            self.play(
                Rotate(
                    alice_roulette["pointer"],
                    angle=alice_spin_angle,
                    about_point=alice_roulette["center"],
                    rate_func=rate_functions.ease_out_cubic,
                ),
                Rotate(
                    bob_roulette["pointer"],
                    angle=bob_spin_angle,
                    about_point=bob_roulette["center"],
                    rate_func=rate_functions.ease_out_cubic,
                ),
                run_time=spin_time,
            )

            alice_pointer_angle += alice_spin_angle
            bob_pointer_angle += bob_spin_angle

            self.wait(0.12)

            alice_ball = Dot(
                point=alice_roulette["center"],
                radius=0.105,
                color=RED,
            )

            bob_ball = Dot(
                point=bob_roulette["center"],
                radius=0.105,
                color=BLUE,
            )

            alice_destination = self.get_ball_destination(
                strategy_box=alice_destinations[alice_result],
                index=alice_counts[alice_result],
            )

            bob_destination = self.get_ball_destination(
                strategy_box=bob_destinations[bob_result],
                index=bob_counts[bob_result],
            )

            alice_path = self.make_flight_path(
                start=alice_ball.get_center(),
                end=alice_destination,
                curve_direction=-1,
            )

            bob_path = self.make_flight_path(
                start=bob_ball.get_center(),
                end=bob_destination,
                curve_direction=1,
            )

            self.play(
                GrowFromCenter(alice_ball),
                GrowFromCenter(bob_ball),
                run_time=0.22,
            )

            self.play(
                MoveAlongPath(
                    alice_ball,
                    alice_path,
                    rate_func=smooth,
                ),
                MoveAlongPath(
                    bob_ball,
                    bob_path,
                    rate_func=smooth,
                ),
                run_time=0.62,
            )

            self.play(
                alice_ball.animate.scale(1.2),
                bob_ball.animate.scale(1.2),
                run_time=0.1,
            )

            self.play(
                alice_ball.animate.scale(1 / 1.2),
                bob_ball.animate.scale(1 / 1.2),
                run_time=0.1,
            )

            alice_result_balls.add(alice_ball)
            bob_result_balls.add(bob_ball)

            alice_counts[alice_result] += 1
            bob_counts[bob_result] += 1

            self.wait(0.12)

        self.wait(1.2)

        self.play(
            *[
                FadeOut(mob)
                for mob in self.mobjects
                if mob not in (alice_image, bob_image)
            ],
            run_time=1.8,
            rate_func=ease_in_out_sine,
        )
        
        alice_rps_position = LEFT * 4 + UP * 3.35
        bob_rps_position = RIGHT * 4 + UP * 3.35

        self.play(
            alice_image.animate.move_to(alice_rps_position),
            bob_image.animate.move_to(bob_rps_position),
            run_time=1.0,
            rate_func=smooth,
        )

        self.wait(0.5)

        a_rock = self.make_rock()
        a_paper = self.make_paper()
        a_scissors = self.make_scissors()

        b_rock = self.make_rock()
        b_paper = self.make_paper()
        b_scissors = self.make_scissors()

        a_wrapped_rock, a_rock_frame = self.frame_move(a_rock)
        a_wrapped_paper, a_paper_frame = self.frame_move(a_paper)
        a_wrapped_scissors, a_scissors_frame = self.frame_move(a_scissors)

        b_wrapped_rock, b_rock_frame = self.frame_move(b_rock)
        b_wrapped_paper, b_paper_frame = self.frame_move(b_paper)
        b_wrapped_scissors, b_scissors_frame = self.frame_move(b_scissors)

        a_moves = VGroup(
            a_wrapped_rock,
            a_wrapped_paper,
            a_wrapped_scissors,
        ).arrange(
            DOWN,
            buff=1.2,
        ).shift(
            LEFT * 4 + DOWN * 0.5
        )

        b_moves = VGroup(
            b_wrapped_rock,
            b_wrapped_paper,
            b_wrapped_scissors,
        ).arrange(
            DOWN,
            buff=1.2,
        ).shift(
            RIGHT * 4 + DOWN * 0.5
        )

        self.play(
            FadeIn(a_moves),
            FadeIn(b_moves),
            run_time=0.8,
            rate_func = ease_in_out_sine
        )

        a_highlight = SurroundingRectangle(
            a_rock_frame,
            color=RED,
        )

        b_highlight = SurroundingRectangle(
            b_paper_frame,
            color=BLUE,
        )

        self.play(
            Create(a_highlight),
            Create(b_highlight),
        )


        self.play(
            a_highlight.animate.move_to(a_scissors_frame),
            b_highlight.animate.move_to(b_rock_frame),
            run_time=1.6,
        )

        self.wait(1)

        self.play(
            a_highlight.animate.move_to(a_paper_frame),
            b_highlight.animate.move_to(b_scissors_frame),
            run_time=1.6,
        )

        self.wait(1)

        self.play(
            a_highlight.animate.move_to(a_rock_frame),
            b_highlight.animate.move_to(b_rock_frame),
            run_time=1.6,
        )

        self.wait(1)

        # MATCHES WITH THE PHRASE => it’s actually quite damaging to the player, if she plays the same thing every time

        self.play(
            Wiggle(a_highlight),
            b_highlight.animate.move_to(b_paper_frame),
            run_time=1.6,
        )

        self.wait(1)

        self.play(
            FadeOut(a_highlight),
            FadeOut(b_highlight),
            run_time=0.5,
        )

        self.wait(1)

        self.play(
            FadeOut(a_moves),
            FadeOut(b_moves),
            FadeOut(alice_image),
            FadeOut(bob_image),
            run_time=0.8,
        )

        self.wait(1)

        # strategy vector

        strategy_vector_title = FixedText(
            "Strategy Vector",
            font_size=44,
            weight=BOLD,
            color=WHITE,
        )

        strategy_vector_title.to_edge(UP, buff=0.25)

        self.play(
            FadeIn(
                strategy_vector_title,
                shift=DOWN * 0.12,
            ),
            run_time=0.7,
            rate_func=ease_in_out_sine,
        )

        # display probabilities

        source_p1 = MathTex(
            r"p_1",
            font_size=44,
        )

        source_p2 = MathTex(
            r"p_2",
            font_size=44,
        )

        source_dots = MathTex(
            r"\cdots",
            font_size=44,
        )

        source_pn = MathTex(
            r"p_n",
            font_size=44,
        )

        source_probabilities = VGroup(
            source_p1,
            source_p2,
            source_dots,
            source_pn,
        ).arrange(
            RIGHT,
            buff=0.7,
        )

        
        source_probabilities.move_to(UP * 2.15)

        self.play(
            LaggedStart(
                FadeIn(source_p1, shift=UP * 0.1),
                FadeIn(source_p2, shift=UP * 0.1),
                FadeIn(source_dots, shift=UP * 0.1),
                FadeIn(source_pn, shift=UP * 0.1),
                lag_ratio=0.12,
            ),
            run_time=0.8,
            rate_func=ease_in_out_sine,
        )

        self.wait(0.3)

        # creTE THE VECTOR
        strategy_vector = Matrix(
            [
                [r"p_1"],
                [r"p_2"],
                [r"\vdots"],
                [r"p_n"],
            ],
            v_buff=0.68,
            h_buff=0.55,
            bracket_h_buff=0.15,
            bracket_v_buff=0.12,
        )

        strategy_vector.scale(0.76)
        strategy_vector.move_to(UP * 0.45)

        vector_entries = strategy_vector.get_entries()
        vector_brackets = strategy_vector.get_brackets()

        target_p1 = vector_entries[0]
        target_p2 = vector_entries[1]
        target_dots = vector_entries[2]
        target_pn = vector_entries[3]


        target_dots.set_x(target_p1.get_x())

        vector_brackets.set_z_index(0)
        source_probabilities.set_z_index(2)

        vector_symbol = MathTex(
            r"\mathbf{p}",
            font_size=50,
        )

        equals_sign = MathTex(
            "=",
            font_size=48,
        )

        equals_sign.next_to(
            strategy_vector,
            LEFT,
            buff=0.28,
        )

        vector_symbol.next_to(
            equals_sign,
            LEFT,
            buff=0.22,
        )

        vector_symbol.set_z_index(1)
        equals_sign.set_z_index(1)

        # Hide the matrix entries until the source probabilities arrive.
        vector_entries.set_opacity(0)

        
        self.play(
            FadeIn(
                vector_symbol,
                shift=RIGHT * 0.08,
            ),
            Write(equals_sign),
            FadeIn(vector_brackets),
            run_time=0.75,
            rate_func=ease_in_out_sine,
        )

        self.wait(0.2)

        
        # Move the original probabilities into the matrix
    
        visible_p1 = target_p1.copy().set_opacity(1)
        visible_p2 = target_p2.copy().set_opacity(1)
        visible_dots = target_dots.copy().set_opacity(1)
        visible_pn = target_pn.copy().set_opacity(1)

        for entry in [
            visible_p1,
            visible_p2,
            visible_dots,
            visible_pn,
        ]:
            entry.set_z_index(2)

        self.play(
            LaggedStart(
                ReplacementTransform(
                    source_p1,
                    visible_p1,
                ),
                ReplacementTransform(
                    source_p2,
                    visible_p2,
                ),

                # horizontal dots to vertical
                ReplacementTransform(
                    source_dots,
                    visible_dots,
                ),

                ReplacementTransform(
                    source_pn,
                    visible_pn,
                ),
                lag_ratio=0.16,
            ),
            run_time=1.6,
            rate_func=ease_in_out_sine,
        )

        self.remove(
            visible_p1,
            visible_p2,
            visible_dots,
            visible_pn,
        )

        vector_entries.set_opacity(1)
        vector_entries.set_z_index(2)

        self.add(vector_entries)

        self.wait(0.4)

        # probability interpret

        probability_meaning = MathTex(
            r"p_i",
            "=",
            r"\Pr(\text{choice } i)",
            font_size=34,
        )

        probability_meaning.next_to(
            strategy_vector,
            RIGHT,
            buff=0.65,
        )

        self.play(
            Write(probability_meaning),
            run_time=0.85,
            rate_func=ease_in_out_sine,
        )

        self.wait(0.55)

        # constraints
        constraints_title = FixedText(
            "Constraints",
            font_size=29,
            weight=BOLD,
            color=WHITE,
        )

        nonnegative_constraint = MathTex(
            r"p_i \geq 0",
            r"\quad \text{for every } i",
            font_size=34,
        )

        normalization_constraint = MathTex(
            r"\sum_{i=1}^{n}p_i=1",
            font_size=37,
        )

        constraint_expressions = VGroup(
            nonnegative_constraint,
            normalization_constraint,
        ).arrange(
            DOWN,
            buff=0.22,
        )

        constraints = VGroup(
            constraints_title,
            constraint_expressions,
        ).arrange(
            DOWN,
            buff=0.3,
        )

        constraints.next_to(
            strategy_vector,
            DOWN,
            buff=0.4,
        )

        self.play(
            FadeIn(
                constraints_title,
                shift=UP * 0.08,
            ),
            run_time=0.45,
            rate_func=smooth,
        )

        self.play(
            FadeIn(nonnegative_constraint),
            run_time=0.75,
            rate_func=smooth,
        )

        self.wait(0.3)

        self.play(
            FadeIn(normalization_constraint),
            run_time=0.75,
            rate_func=smooth,
        )

        self.wait(0.4)

        constraints_highlight = SurroundingRectangle(
            constraint_expressions,
            color=YELLOW,
            buff=0.17,
            corner_radius=0.1,
            stroke_width=4,
        )

        self.play(
            Create(constraints_highlight),
            run_time=0.65,
            rate_func=ease_in_out_sine,
        )

        self.wait(1.2)


        self.play(
            FadeOut(
                VGroup(
                    strategy_vector_title,
                    vector_symbol,
                    equals_sign,
                    strategy_vector,
                    probability_meaning,
                    constraints,
                    constraints_highlight,
                )
            ),
            run_time=1.2,
            rate_func=ease_in_out_sine,
        )

        self.wait(0.4)


        # ============================================================
        # MIXED STRATEGIES
        # ============================================================


        self.play(
            alice_image.animate
                .set_height(1.25)
                .to_corner(UL, buff=0.3),
            bob_image.animate
                .set_height(1.25)
                .to_corner(UR, buff=0.3),
            run_time=0.9,
            rate_func=ease_in_out_sine,
        )


        # ============================================================
        # PAYOFF MATRIX DATA
        # ============================================================

        payoff_data = [
            [(3, 2), (1, 1)],
            [(0, 0), (2, 3)],
        ]

        cell_width = 2.3
        cell_height = 1.2

        grid = VGroup()
        cells = []

        # ============================================================
        # CREATE 3x3 BIMATRIX GRID
        # ============================================================

        for i in range(3):
            row = []

            for j in range(3):
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    color=WHITE,
                    stroke_width=2,
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
            stroke_width=2,
            corner_radius=0.1,
        )

        # ============================================================
        # PLAYER LABELS
        # ============================================================

        alice_caption1 = FixedText(
            "Alice",
            font_size=35,
            weight=BOLD,
            color=RED,
        )

        bob_caption1 = FixedText(
            "Bob",
            font_size=35,
            weight=BOLD,
            color=BLUE,
        )

        alice_caption1.rotate(PI / 2)
        alice_caption1.next_to(
            grid,
            LEFT,
            buff=0.8,
        )

        bob_caption1.next_to(
            grid,
            UP,
            buff=0.8,
        )

        player_labels = VGroup(
            alice_caption1,
            bob_caption1,
        )

        # ============================================================
        # STRATEGY LABELS
        # ============================================================

        alice_bach = FixedText(
            "Bach",
            font_size=35,
            weight=BOLD,
            color=WHITE,
        )

        alice_stravinsky = FixedText(
            "Stravinsky",
            font_size=35,
            weight=BOLD,
            color=WHITE,
        )

        bob_bach = FixedText(
            "Bach",
            font_size=35,
            weight=BOLD,
            color=WHITE,
        )

        bob_stravinsky = FixedText(
            "Stravinsky",
            font_size=35,
            weight=BOLD,
            color=WHITE,
        )

        alice_bach.move_to(
            cells[1][0].get_center()
        )

        alice_stravinsky.move_to(
            cells[2][0].get_center()
        )

        bob_bach.move_to(
            cells[0][1].get_center()
        )

        bob_stravinsky.move_to(
            cells[0][2].get_center()
        )

        strategy_labels = VGroup(
            alice_bach,
            alice_stravinsky,
            bob_bach,
            bob_stravinsky,
        )

        # ============================================================
        # PAYOFF ENTRIES
        # ============================================================

        payoff_entries = VGroup()
        alice_scores = VGroup()
        bob_scores = VGroup()

        for i in range(2):
            for j in range(2):
                alice_val, bob_val = payoff_data[i][j]

                open_p = FixedText(
                    "(",
                    font_size=40,
                    color=WHITE,
                )

                alice_score = FixedText(
                    str(alice_val),
                    font_size=40,
                    color=RED,
                )

                comma = FixedText(
                    ",",
                    font_size=40,
                    color=WHITE,
                )

                bob_score = FixedText(
                    str(bob_val),
                    font_size=40,
                    color=BLUE,
                )

                close_p = FixedText(
                    ")",
                    font_size=40,
                    color=WHITE,
                )

                payoff = VGroup(
                    open_p,
                    alice_score,
                    comma,
                    bob_score,
                    close_p,
                )

                payoff.arrange(
                    RIGHT,
                    buff=0.05,
                )

                comma.shift(DOWN * 0.25)

                payoff.move_to(
                    cells[i + 1][j + 1].get_center()
                )

                payoff_entries.add(payoff)
                alice_scores.add(alice_score)
                bob_scores.add(bob_score)


        self.play(
            Create(grid),
            Create(matrix_box),
            FadeIn(player_labels),
            FadeIn(strategy_labels),
            FadeIn(payoff_entries),
            run_time=1.5,
        )

        self.wait(1)


        overlay_width = cell_width * 0.9
        overlay_height = cell_height * 0.82

        # Alice: Bach with probability 1/3
        Aoverlay_rect1 = Rectangle(
            width=overlay_width,
            height=overlay_height,
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.9,
        )

        Aoverlay_rect1.move_to(
            cells[1][0].get_center()
        )

        Aoverlay_text1 = MathTex(
            r"\frac{1}{3}",
            font_size=40,
            color=WHITE,
        ).move_to(
            Aoverlay_rect1.get_center()
        )

        # Alice: Stravinsky with probability 2/3
        Aoverlay_rect2 = Rectangle(
            width=overlay_width,
            height=overlay_height,
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.9,
        )

        Aoverlay_rect2.move_to(
            cells[2][0].get_center()
        )

        Aoverlay_text2 = MathTex(
            r"\frac{2}{3}",
            font_size=40,
            color=WHITE,
        ).move_to(
            Aoverlay_rect2.get_center()
        )

        # Bob: Bach with probability 2/3
        Boverlay_rect1 = Rectangle(
            width=overlay_width,
            height=overlay_height,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.9,
        )

        Boverlay_rect1.move_to(
            cells[0][1].get_center()
        )

        Boverlay_text1 = MathTex(
            r"\frac{2}{3}",
            font_size=40,
            color=WHITE,
        ).move_to(
            Boverlay_rect1.get_center()
        )

        # Bob: Stravinsky with probability 1/3
        Boverlay_rect2 = Rectangle(
            width=overlay_width,
            height=overlay_height,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.9,
        )

        Boverlay_rect2.move_to(
            cells[0][2].get_center()
        )

        Boverlay_text2 = MathTex(
            r"\frac{1}{3}",
            font_size=40,
            color=WHITE,
        ).move_to(
            Boverlay_rect2.get_center()
        )

        alice_probability_overlays = VGroup(
            Aoverlay_rect1,
            Aoverlay_text1,
            Aoverlay_rect2,
            Aoverlay_text2,
        )

        bob_probability_overlays = VGroup(
            Boverlay_rect1,
            Boverlay_text1,
            Boverlay_rect2,
            Boverlay_text2,
        )

        
        alice_probability_overlays.set_z_index(3)
        bob_probability_overlays.set_z_index(3)

        self.play(
            FadeOut(strategy_labels),
            run_time=0.6,
        )

        self.wait(0.5)

        self.play(
            LaggedStart(
                FadeIn(
                    VGroup(
                        Aoverlay_rect1,
                        Aoverlay_text1,
                    )
                ),
                FadeIn(
                    VGroup(
                        Boverlay_rect1,
                        Boverlay_text1,
                    )
                ),
                FadeIn(
                    VGroup(
                        Aoverlay_rect2,
                        Aoverlay_text2,
                    )
                ),
                FadeIn(
                    VGroup(
                        Boverlay_rect2,
                        Boverlay_text2,
                    )
                ),
                lag_ratio=0.3,
            ),
            run_time=2.5,
        )

        self.wait(1)

        alice_vector_name = FixedText(
            "Alice:",
            font_size=35,
            weight=BOLD,
            color=RED,
        )

        bob_vector_name = FixedText(
            "Bob:",
            font_size=35,
            weight=BOLD,
            color=BLUE,
        )

        alice_vector_values = MathTex(
            r"\mathbf{\left[\tfrac{1}{3},\tfrac{2}{3}\right]}",
            color=RED,
            font_size = 45
        )

        bob_vector_values = MathTex(
            r"\mathbf{\left[\frac{2}{3},\frac{1}{3}\right]}",
            color=BLUE,
            font_size=30
        )

        alice_vec = VGroup(
            alice_vector_name,
            alice_vector_values,
        ).arrange(RIGHT, buff=0.16)

        bob_vec = VGroup(
            bob_vector_name,
            bob_vector_values,
        ).arrange(RIGHT, buff=0.16)

        alice_vec.to_edge(LEFT).shift(UP * 2)
        bob_vec.to_edge(RIGHT).shift(UP * 2)

        
        self.play(
            TransformFromCopy(
                alice_caption1,
                alice_vector_name,
            ),
            TransformFromCopy(
                bob_caption1,
                bob_vector_name,
            ),
            FadeIn(
                alice_vector_values,
                shift=RIGHT * 0.12,
            ),
            FadeIn(
                bob_vector_values,
                shift=RIGHT * 0.12,
            ),
            run_time=1.2,
            rate_func=ease_in_out_sine,
        )

        self.wait(1)

        # calculations

        calc1 = MathTex(
            r"\tfrac{1}{3}"
            r"\times"
            r"\tfrac{2}{3}"
            r"="
            r"\tfrac{2}{9}",
            font_size=50,
        )

        calc2 = MathTex(
            r"\tfrac{1}{3}"
            r"\times"
            r"\tfrac{1}{3}"
            r"="
            r"\tfrac{1}{9}",
            font_size=50,
        )

        calc3 = MathTex(
            r"\tfrac{2}{3}"
            r"\times"
            r"\tfrac{2}{3}"
            r"="
            r"\tfrac{4}{9}",
            font_size=50,
        )

        calc4 = MathTex(
            r"\tfrac{2}{3}"
            r"\times"
            r"\tfrac{1}{3}"
            r"="
            r"\tfrac{2}{9}",
            font_size=50,
        )

        
        calc1.next_to(
            cells[1][1],
            LEFT,
        )

        calc2.next_to(
            cells[1][2],
            RIGHT,
        )

        calc3.next_to(
            cells[2][1],
            LEFT,
        )

        calc4.next_to(
            cells[2][2],
            RIGHT,
        )

        calc1.shift(LEFT * 3.4)
        calc2.shift(RIGHT * 0.9)
        calc3.shift(LEFT * 3.4)
        calc4.shift(RIGHT * 0.9)

        result1 = MathTex(
            r"\frac{2}{9}",
            font_size=40,
        ).move_to(
            cells[1][1].get_center()
        )

        result2 = MathTex(
            r"\frac{1}{9}",
            font_size=40,
        ).move_to(
            cells[1][2].get_center()
        )

        result3 = MathTex(
            r"\frac{4}{9}",
            font_size=40,
        ).move_to(
            cells[2][1].get_center()
        )

        result4 = MathTex(
            r"\frac{2}{9}",
            font_size=40,
        ).move_to(
            cells[2][2].get_center()
        )

        # 1st outcome
        self.play(
            Transform(
                payoff_entries[0],
                calc1,
            ),
            run_time=1,
        )

        self.wait(0.8)

        # 2nd outcome

        self.play(
            Transform(
                payoff_entries[1],
                calc2,
            ),
            run_time=1,
        )

        self.wait(0.5)

        # 3rd outcome

        self.play(
            Transform(
                payoff_entries[2],
                calc3,
            ),
            run_time=1,
        )

        self.wait(0.5)

        # 4th outcome
        self.play(
            Transform(
                payoff_entries[3],
                calc4,
            ),
            run_time=1,
        )

        self.wait(1)

        # copies to go back to the matrix

        computed_value_1 = payoff_entries[0].copy()
        computed_value_2 = payoff_entries[1].copy()
        computed_value_3 = payoff_entries[2].copy()
        computed_value_4 = payoff_entries[3].copy()

        # sum
        total = MathTex(
            r"\frac{2}{9}"
            r"+"
            r"\frac{1}{9}"
            r"+"
            r"\frac{4}{9}"
            r"+"
            r"\frac{2}{9}"
            r"="
            r"1",
            font_size=42,
        )

        total.to_edge(DOWN)

        self.play(
            Write(total),
            run_time=1,
        )

        highlight_box = SurroundingRectangle(
            total,
            color=YELLOW,
            buff=0.2,
            corner_radius=0.1,
            stroke_width=4,
        )

        self.play(
            Create(highlight_box),
            run_time=0.6,
        )

        self.wait(1)

        #place probabilities inside the cell
        self.play(
            FadeOut(payoff_entries[0]),
            ReplacementTransform(
                computed_value_1,
                result1,
            ),
            run_time=0.8,
        )

        self.wait(0.3)

        self.play(
            FadeOut(payoff_entries[1]),
            ReplacementTransform(
                computed_value_2,
                result2,
            ),
            run_time=0.8,
        )

        self.wait(0.3)

        self.play(
            FadeOut(payoff_entries[2]),
            ReplacementTransform(
                computed_value_3,
                result3,
            ),
            run_time=0.8,
        )

        self.wait(0.3)

        self.play(
            FadeOut(payoff_entries[3]),
            ReplacementTransform(
                computed_value_4,
                result4,
            ),
            run_time=0.8,
        )

        self.wait(0.3)

        self.play(
            FadeOut(total),
            FadeOut(highlight_box),
            run_time=0.7,
        )

        self.wait(1)


        title = FixedText(
            "Mixed Strategies",
            font_size=42,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP)

        self.play(
            Write(title),
            run_time=0.8,
        )


        mixed_strategy_scene = VGroup(
            title,
            alice_vec,
            bob_vec,
            grid,
            matrix_box,
            player_labels,
            alice_probability_overlays,
            bob_probability_overlays,
            result1,
            result2,
            result3,
            result4,
        )

        self.play(
            FadeOut(mixed_strategy_scene),
            run_time=1.2,
        )

        self.wait(0.4)




        finite_label = FixedText(
            "Finite pure strategies",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP)

        alice_name = FixedText(
            "Alice",
            font_size=30,
            weight=BOLD,
            color=RED,
        )
        bob_name = FixedText(
            "Bob",
            font_size=30,
            weight=BOLD,
            color=BLUE,
        )

        pure_alice = MathTex(r"\{B,S\}", color=RED, font_size=54)
        pure_bob = MathTex(r"\{B,S\}", color=BLUE, font_size=54)

        alice_group = VGroup(alice_name, pure_alice).arrange(DOWN, buff=0.3)
        bob_group = VGroup(bob_name, pure_bob).arrange(DOWN, buff=0.3)
        alice_group.shift(LEFT * 3)
        bob_group.shift(RIGHT * 3)

        self.play(
            FadeIn(finite_label),
            FadeIn(alice_group, shift=UP * 0.15),
            FadeIn(bob_group, shift=UP * 0.15),
            run_time=0.9,
        )
        self.wait(0.7)

        infinite_label = FixedText(
            "Infinitely many mixed strategies",
            font_size=38,
            weight=BOLD,
        ).move_to(finite_label)

        mixed_alice = MathTex(r"[p,\,1-p]", color=RED, font_size=54).move_to(pure_alice)
        mixed_bob = MathTex(r"[q,\,1-q]", color=BLUE, font_size=54).move_to(pure_bob)
        alice_domain = MathTex(r"p\in[0,1]", color=RED, font_size=36).next_to(mixed_alice, DOWN, buff=0.4)
        bob_domain = MathTex(r"q\in[0,1]", color=BLUE, font_size=36).next_to(mixed_bob, DOWN, buff=0.4)

        self.play(
            ReplacementTransform(finite_label, infinite_label),
            TransformMatchingTex(pure_alice, mixed_alice),
            TransformMatchingTex(pure_bob, mixed_bob),
            run_time=1.1,
            rate_func=smooth,
        )
        self.play(
            FadeIn(alice_domain, shift=UP * 0.1),
            FadeIn(bob_domain, shift=UP * 0.1),
            run_time=0.6,
        )
        self.wait(0.9)

        self.play(
            FadeOut(VGroup(
                infinite_label,
                alice_name,
                bob_name,
                mixed_alice,
                mixed_bob,
                alice_domain,
                bob_domain,
            )),
            run_time=0.8,
        )

        

        pure_heading = FixedText(
            "Pure strategies",
            font_size=40,
            weight=BOLD,
        ).shift(UP * 0.8)

        pure_statement = FixedText(
            "A Nash equilibrium may not exist",
            font_size=36,
            color=RED,
        ).next_to(pure_heading, DOWN, buff=0.5)

        self.play(
            FadeIn(pure_heading),
            FadeIn(pure_statement, shift=UP * 0.12),
            run_time=0.8,
        )
        self.wait(0.7)

        mixed_heading = FixedText(
            "Mixed strategies",
            font_size=40,
            weight=BOLD,
        ).move_to(pure_heading)

        mixed_statement = FixedText(
            "A Nash equilibrium always exists",
            font_size=36,
            color=GREEN,
        ).move_to(pure_statement)

        self.play(
            ReplacementTransform(pure_heading, mixed_heading),
            ReplacementTransform(pure_statement, mixed_statement),
            run_time=0.9,
            rate_func=smooth,
        )
        self.wait(0.6)

        nash_name = FixedText(
            "John Nash",
            font_size=36,
            weight=BOLD,
        )
        nash_theorem = FixedText(
            "Existence Theorem, 1950",
            font_size=29,
        )
        nash_attribution = VGroup(nash_name, nash_theorem).arrange(DOWN, buff=0.16)
        nash_attribution.next_to(mixed_statement, DOWN, buff=0.75)

        self.play(
            FadeIn(nash_attribution, shift=UP * 0.12),
            run_time=0.65,
        )
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(mixed_heading, mixed_statement, nash_attribution)),
            run_time=0.75,
        )

        

        central_question = FixedText(
            "How do we find one efficiently?",
            font_size=48,
            weight=BOLD,
        )

        self.play(Write(central_question), run_time=0.95)
        self.wait(1.1)
        self.play(FadeOut(central_question), run_time=0.65)


        search_title = FixedText(
            "Possible strategy profiles",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP)

        profile_tex = [
            r"([0,1],[1,0])",
            r"([\tfrac14,\tfrac34],[\tfrac12,\tfrac12])",
            r"([\tfrac13,\tfrac23],[\tfrac23,\tfrac13])",
            r"([\tfrac25,\tfrac35],[\tfrac15,\tfrac45])",
            r"([\tfrac12,\tfrac12],[\tfrac34,\tfrac14])",
            r"([\tfrac35,\tfrac25],[\tfrac27,\tfrac57])",
            r"([\tfrac23,\tfrac13],[\tfrac13,\tfrac23])",
            r"([\tfrac34,\tfrac14],[\tfrac25,\tfrac35])",
            r"([1,0],[0,1])",
        ]

        profiles = VGroup(*[
            MathTex(tex, font_size=30)
            for tex in profile_tex
        ])
        profiles.arrange_in_grid(rows=3, cols=3, buff=(0.65, 0.55)).shift(DOWN * 0.2)

        continuation = MathTex(r"\vdots\qquad\vdots\qquad\vdots", font_size=42)
        continuation.next_to(profiles, DOWN, buff=0.3)

        infinity_label = FixedText(
            "Infinitely many profiles",
            font_size=34,
        ).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(search_title), run_time=0.45)
        self.play(
            LaggedStart(
                *[FadeIn(profile, shift=UP * 0.1) for profile in profiles],
                lag_ratio=0.09,
            ),
            run_time=1.6,
        )
        self.play(
            FadeIn(continuation),
            FadeIn(infinity_label, shift=UP * 0.1),
            run_time=0.6,
        )
        self.wait(0.75)

        # why exhaustive search fails

        search_marker = Underline(
            profiles[0],
            color=WHITE,
            buff=0.08,
            stroke_width=3,
        )

        self.play(Create(search_marker), run_time=0.25)
        for profile in profiles[1:5]:
            self.play(
                search_marker.animate.next_to(profile, DOWN, buff=0.08),
                run_time=0.20,
                rate_func=linear,
            )

        impossible_text = FixedText(
            "An exhaustive search never finishes",
            font_size=40,
            weight=BOLD,
            color=RED,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(search_marker),
            ReplacementTransform(infinity_label, impossible_text),
            run_time=0.7,
        )
        self.wait(0.9)

        # reduce search space

        candidate_indices = [2, 4, 6]
        candidates = VGroup(*[profiles[index] for index in candidate_indices])
        non_candidates = VGroup(*[
            profiles[index]
            for index in range(len(profiles))
            if index not in candidate_indices
        ])

        reduction_text = FixedText(
            "Use a property of Nash equilibria to reduce the search",
            font_size=32,
        ).move_to(impossible_text)

        self.play(
            ReplacementTransform(impossible_text, reduction_text),
            run_time=0.7,
        )
        self.wait(0.55)

        candidate_title = FixedText(
            "Candidate profiles",
            font_size=40,
            weight=BOLD,
        ).move_to(search_title)

        target_positions = [UP * 0.9, ORIGIN, DOWN * 0.9]

        self.play(
            ReplacementTransform(search_title, candidate_title),
            FadeOut(non_candidates),
            FadeOut(continuation),
            *[
                candidate.animate.move_to(position).scale(1.08)
                for candidate, position in zip(candidates, target_positions)
            ],
            run_time=1.05,
            rate_func=smooth,
        )

        verify_text = FixedText(
            "Then verify which candidates are Nash equilibria",
            font_size=33,
        ).move_to(reduction_text)

        self.play(
            ReplacementTransform(reduction_text, verify_text),
            run_time=0.7,
        )
        self.wait(1.2)

from manim import *
from FixedText import *
from Character import *
import numpy as np
from manim.animation.composition import AnimationGroup

payoff_data = [
	[(1, 5), (5, 2)],
	[(3, 3), (4, 8)],
	[(4, 8), (0, 4)]
]

def normalize(v):
	return v / np.linalg.norm(v)

# rotates a vector 90 degrees counter clockwise around the z axis
def rotate90_cc(v):
	return np.array([v[1], -v[0], v[2]])

class Labeling(ThreeDScene):

	def construct(self):


		lemke_img = ImageMobject("../Images-Icons/Lemke.jpg").scale_to_fit_height(3) 
		lemke_name = Tex(
			"Carlton E. ", "Lemke",
			font_size=30, 
			color=WHITE
		)
		lemke_name.next_to(lemke_img, DOWN, buff=0.4)
		lemke_img = Group(lemke_img, lemke_name)

		howson_img = ImageMobject("../Images-Icons/Lemke.jpg").scale_to_fit_height(3) 
		howson_name = Tex(
			"Joseph T. ", "Howson",
			font_size=30, 
			color=WHITE
		)
		howson_name.next_to(howson_img, DOWN, buff=0.4)
		howson_img = Group(howson_img, howson_name)

		lemke_img.shift(LEFT * 2)
		howson_img.shift(RIGHT * 2)

		self.wait()
		self.play(FadeIn(lemke_img, shift=UP))
		self.play(FadeIn(howson_img, shift=UP))

		hyphen = Tex("-", font_size=40, color=WHITE)

		self.play(
			FadeOut(lemke_img[0]),
			FadeOut(howson_img[0]),
			FadeOut(lemke_name[0]),
			FadeOut(howson_name[0]),
			FadeIn(hyphen),
			lemke_name[1].animate.next_to(hyphen, LEFT).scale(4/3),
			howson_name[1].animate.next_to(hyphen, RIGHT).scale(4/3),
		)
		self.wait()


		### REMOVE ALL AND SHOW TABLE

		self.play(FadeOut(lemke_name[1], howson_name[1], hyphen), run_time=0.5)

		self.wait()
	# def construct(self):

		# create table

		cell_width = 3.2
		cell_height = 1.8

		grid = VGroup()
		cells = []

		for i in range(len(payoff_data)):
			row = []

			for j in range(len(payoff_data[0])):
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

		payoff_entries = VGroup()
		alice_scores = VGroup()
		bob_scores = VGroup()

		for i in range(len(payoff_data)):
			for j in range(len(payoff_data[0])):
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
					cells[i][j].get_center()
				)

				payoff_entries.add(payoff)
				alice_scores.add(alice_score)
				bob_scores.add(bob_score)


		# labels for choices
		alice_strategies = VGroup()
		bob_strategies = VGroup()
		for i in range(len(payoff_data)):
			alice_strategies.add(FixedText(f"A{i + 1}", color=RED).next_to(cells[i][0], LEFT, buff=0.4))
		for i in range(len(payoff_data[0])):
			bob_strategies.add(FixedText(f"B{i + 1}", color=BLUE).next_to(cells[0][i], UP, buff=0.4))

		table = VGroup(grid, matrix_box, payoff_entries, alice_strategies, bob_strategies)
		table.shift(RIGHT * 0.3 + DOWN * 0.2)

		alice = Alice().scale(0.7)
		bob = Bob().scale(0.7)

		alice.to_corner(UL, buff=0.6)
		bob.to_corner(UR, buff=0.6)
	
		self.play(FadeIn(table, alice, bob))
		self.wait()
		self.play(bob.blink())

		overlay_box = Square(fill_color=BLACK, stroke_width=0).set_opacity(0.85)
		overlay_box.stretch_to_fit_width(cell_width * 2).stretch_to_fit_height(cell_height * 3).set_x(0.5 * (cells[1][0].get_x() + cells[1][1].get_x())).match_y(cells[1][0])

		self.play(FadeIn(overlay_box))
		self.wait()

		# expected value for alice

		temp_text = [c.copy().set_z_index(2) for c in alice_scores]

		expected1 = FixedText("1p + 5(1 - p) = -4p + 5")
		expected1[0].set_fill_color(RED)
		expected1[3].set_fill_color(RED)
		expected1.next_to(alice_strategies[0], RIGHT, buff=0.7)

		self.play(Transform(temp_text[0], expected1[0]))
		self.play(FadeIn(expected1[1]))
		self.play(FadeIn(expected1[2]))
		self.play(Transform(temp_text[1], expected1[3]))
		self.play(FadeIn(expected1[4:9]))
		self.play(FadeIn(expected1[9:]))

		self.wait()

		expected2 = FixedText("3p + 4(1 - p) = -p + 4")
		expected2[0].set_fill_color(RED)
		expected2[3].set_fill_color(RED)
		expected2.next_to(alice_strategies[1], RIGHT, buff=0.7)

		self.play(
			LaggedStart(
				Transform(temp_text[2], expected2[0]),
				FadeIn(expected2[1]),
				FadeIn(expected2[2]),
				Transform(temp_text[3], expected2[3]),
				FadeIn(expected2[4:]),
				lag_ratio=0.4
			)
		)

		self.wait()

		expected3 = FixedText("4p + 0(1 - p) = 4p")
		expected3[0].set_fill_color(RED)
		expected3[3].set_fill_color(RED)
		expected3.next_to(alice_strategies[2], RIGHT, buff=0.7)

		self.play(
			LaggedStart(
				Transform(temp_text[4], expected3[0]),
				FadeIn(expected3[1]),
				FadeIn(expected3[2]),
				Transform(temp_text[5], expected3[3]),
				FadeIn(expected3[4:]),
				lag_ratio=0.4
			)
		)

		self.wait()

		# expected_values = VGroup(
		# 	expected1[10:],
		# 	expected2[10:],
		# 	expected3[10:]
		# )


		# self.play(FadeOut(table, overlay_box, expected1[:10], expected2[:10], expected3[:10], *temp_text), expected_values.animate.shift(RIGHT * 2))
		# self.wait()

		self.play(FadeOut(table, expected1, expected2, expected3, *temp_text))
		self.wait()

		ax = Axes(
			x_range=[0, 1],
			y_range=[0, 6, 1],
			tips=False,
			x_length=6,
			y_length=6,
			axis_config={"include_numbers": True}
		)

		graphs = [ax.plot(lambda x: payoff_data[i][0][0] * x + payoff_data[i][1][0] * (1 - x), x_range=[0, 1], use_smoothing=False) for i in range(3)]

		for i in range(3):
			alice_strategies[i].move_to(ax.coords_to_point(1, payoff_data[i][0][0]) + RIGHT * 0.5)

		self.play(FadeIn(ax))

		self.play(
			LaggedStart(
				Write(graphs[0]), FadeIn(alice_strategies[0]),
				Write(graphs[1]), FadeIn(alice_strategies[1]),
				Write(graphs[2]), FadeIn(alice_strategies[2]),
				lag_ratio=0.5
			)
		)

		intersections = [
			Sphere(radius=0.075, fill_opacity=1).set_color(GREEN_D).move_to(ax.coords_to_point(1/3, 3 + 2/3)),
			Sphere(radius=0.075, fill_opacity=1).set_color(GREEN_D).move_to(ax.coords_to_point(0.8, 3.2)),
			Sphere(radius=0.075, fill_opacity=1).set_color(GREEN_D).move_to(ax.coords_to_point(0.625, 2.5))
		]

		for inter in intersections:
			inter.set_z_index(4)

		self.play(FadeIn(*intersections))

		self.wait()

		self.play(Indicate(intersections[2], scale_factor=2))
		self.wait()

		end_point = ax.coords_to_point(0.625, 3.375)
		up_arrow = Arrow(start=intersections[2].get_center(), end=end_point, buff=0.1)
		self.play(LaggedStart(FadeIn(up_arrow), intersections[2].animate.move_to(end_point), lag_ratio=0.7))
		self.wait()

		self.play(FadeOut(up_arrow), intersections[2].animate.move_to(up_arrow.start))
		self.wait()

		self.play(intersections[0].animate.move_to(ax.coords_to_point(1/3, 4/3)), intersections[1].animate.move_to(ax.coords_to_point(0.8, 1.8)))
		self.wait()
		self.play(intersections[0].animate.move_to(ax.coords_to_point(1/3, 3 + 2/3)), intersections[1].animate.move_to(ax.coords_to_point(0.8, 3.2)))
		self.wait()

		top_graph = VGroup(
			Line3D(ax.coords_to_point(0, 5), intersections[0].get_center(), color=YELLOW).set_z_index(3),
			Line3D(intersections[0].get_center(), intersections[1].get_center(), color=YELLOW).set_z_index(3),
			Line3D(intersections[1].get_center(), ax.coords_to_point(1, 4), color=YELLOW).set_z_index(3)
		)

		self.play(Write(top_graph))
		self.wait()

		self.play(FadeOut(*graphs, intersections[2]))
		self.wait()

		self.play(LaggedStart(
			*[
				a.animate.move_to(
					0.5 * (line.get_start() + line.get_end()) + 0.6 * rotate90_cc(normalize(line.get_end() - line.get_start()))
				)
				for a, line in zip(alice_strategies, top_graph)
			], lag_ratio=0.3
		))
		self.wait()

		self.play(
			LaggedStart(
				*[Wiggle(line) for line in top_graph],
				lag_ratio=0.5
			)
		)

		self.wait()

		top_graph.add(
			Line3D(ax.coords_to_point(0, 5), ax.coords_to_point(0, 5) + np.array([0, 100, 0])),
			Line3D(ax.coords_to_point(1, 4), ax.coords_to_point(1, 4) + np.array([0, 100, 0]))
		)

		intersections.pop(2)

		intersections += [
			Sphere(radius=0.075).set_color(GREEN_D).move_to(ax.coords_to_point(0, 5)),
			Sphere(radius=0.075).set_color(GREEN_D).move_to(ax.coords_to_point(1, 4))
		]

		# self.play(FadeIn(intersections[-2]), FadeIn(intersections[-1]))

		# self.wait()

		phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

		visible_obj = VGroup(top_graph, ax, *intersections, *alice_strategies)

		self.play(
			phi.animate.set_value(90 * DEGREES),
			focal_distance.animate.set_value(3),
			# distance_to_origin.animate.set_value(3),
			visible_obj.animate.shift(np.array([0, 0, -3])),
			alice.animate.shift(np.array([0, 0, -3])),
			bob.animate.shift(np.array([0, 0, -3])),
		)
		self.wait()
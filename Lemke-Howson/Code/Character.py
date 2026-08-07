
from manim import *
from FixedText import *
from manim.utils.rate_functions import there_and_back, squish_rate_func


EYE_MOVEMENT = 0.1

def update_blink(obj):
	EYES_MIN_HEIGHT = 0.04
	ANIM_DURATION = 0.2
	if obj.scene.time > obj.timer:
		obj.closing_eyes = not obj.closing_eyes
		obj.timer = obj.scene.time + (0.5 if not obj.closing_eyes else 0.2)

	if obj.closing_eyes:
		t = obj.timer - obj.scene.time
		print('Current height:', (obj.eyes_height - EYES_MIN_HEIGHT) * abs(2 * t / ANIM_DURATION - 1) + EYES_MIN_HEIGHT)
		print('Start height:', obj.eyes_height)
		obj.eyes.stretch_to_fit_height((obj.eyes_height - EYES_MIN_HEIGHT) * abs(2 * t / ANIM_DURATION - 1) + EYES_MIN_HEIGHT)
	else:
		obj.eyes.stretch_to_fit_height(obj.eyes_height)

class Character(Mobject):
	# def __init__(self):
	# 	super().__init__()
	# 	alice = SVGMobject("..\\Images-Icons\\alice-final1").scale(1.3)
	# 	eyes = VGroup(alice.submobjects[3], alice.submobjects[4], alice.submobjects[7], alice.submobjects[8])
	# 	for s in eyes:
	# 		alice.submobjects.remove(s)

	# 	self.add(alice)
	# 	self.add(eyes)

	# 	self.character = alice
	# 	self.eyes = eyes

	# 	self.eyes_pos = 0

	def __init__(self, scene=None):
		super().__init__()

		self.closing_eyes = False
		self.timer = 0.5
		self.eyes_height = None

		self.scene = scene
		self.add_updater(update_blink)


	def look_left(self):
		anim = self.eyes.animate.shift(LEFT * (self.eyes_pos + EYE_MOVEMENT))
		self.eyes_pos = -EYE_MOVEMENT
		return anim

	def look_right(self):
		anim = self.eyes.animate.shift(RIGHT * (EYE_MOVEMENT - self.eyes_pos))
		self.eyes_pos = EYE_MOVEMENT
		return anim

	def look_streight(self):
		anim = self.eyes.animate.shift(RIGHT * (-self.eyes_pos))
		self.eyes_pos = 0
		return anim

	def __blink__(self):
		self.eyes.stretch_to_fit_height(0.04),
		return self

	def blink(self):
		return ApplyMethod(self.__blink__, rate_func=there_and_back, run_time=0.2)


class Alice(Character):
	def __init__(self):
		super().__init__()
		svg = SVGMobject("..\\Images-Icons\\alice-final1").scale(1.3)
		eyes = VGroup(svg.submobjects[3], svg.submobjects[4], svg.submobjects[7], svg.submobjects[8])
		for s in eyes:
			svg.submobjects.remove(s)

		self.add(svg)
		self.add(eyes)

		self.character = svg
		self.eyes = eyes

		self.eyes_pos = 0
		self.eyes_height = eyes.height


class Bob(Character):
	def __init__(self):
		super().__init__()
		svg = SVGMobject("..\\Images-Icons\\bob-final1").scale(1.3)
		eyes = VGroup(svg.submobjects[2], svg.submobjects[4])
		for s in eyes:
			svg.submobjects.remove(s)

		self.add(svg)
		self.add(eyes)

		self.character = svg
		self.eyes = eyes

		self.eyes_pos = 0
		self.eyes_height = eyes.height


class Test(Scene):
	def construct(self):
		self.camera.background_color = "#d3cdc0"

		alice = Alice()
		alice.scene = self
		self.add(alice)
		self.wait()
		self.play(alice.look_left())
		self.wait()
		self.play(alice.look_right())
		self.wait()
		self.play(alice.look_streight())
		self.wait()
		# self.play(alice.blink())
		# self.wait()
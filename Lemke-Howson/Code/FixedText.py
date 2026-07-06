
from manim import Text
from manim.mobject.text.text_mobject import TEXT2SVG_ADJUSTMENT_FACTOR
import copy
import hashlib
import re
from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any

import manimpango
import numpy as np
from manimpango import MarkupUtils, PangoUtils, TextSetting

from manim import config, logger
from manim.constants import *
from manim.mobject.geometry.arc import Dot
from manim.mobject.svg.svg_mobject import SVGMobject
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
from manim.typing import Point3D
from manim.utils.color import ManimColor, ParsableManimColor, color_gradient

class FixedText(Text):
	def __init__(
		self,
		text: str,
		fill_opacity: float = 1.0,
		stroke_width: float = 0,
		color: ParsableManimColor | None = None,
		font_size: float = DEFAULT_FONT_SIZE,
		line_spacing: float = -1,
		font: str = "",
		slant: str = NORMAL,
		weight: str = NORMAL,
		t2c: dict[str, str] | None = None,
		t2f: dict[str, str] | None = None,
		t2g: dict[str, Iterable[ParsableManimColor]] | None = None,
		t2s: dict[str, str] | None = None,
		t2w: dict[str, str] | None = None,
		gradient: Iterable[ParsableManimColor] | None = None,
		tab_width: int = 4,
		warn_missing_font: bool = True,
		# Mobject
		height: float | None = None,
		width: float | None = None,
		should_center: bool = True,
		disable_ligatures: bool = False,
		use_svg_cache: bool = False,
		**kwargs: Any,
	):
		super().__init__(
			text,
			fill_opacity,
			stroke_width,
			color,
			font_size * TEXT2SVG_ADJUSTMENT_FACTOR,
			line_spacing,
			font,
			slant,
			weight,
			t2c,
			t2f,
			t2g,
			t2s,
			t2w,
			gradient,
			tab_width,
			warn_missing_font,
			height,
			width,
			should_center,
			disable_ligatures,
			use_svg_cache,
			**kwargs
		)
		self.scale(1 / TEXT2SVG_ADJUSTMENT_FACTOR)
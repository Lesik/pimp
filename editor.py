#!/usr/bin/env python3

import numpy
import scipy.misc

class Editor:

	undo = []

	def __init__(self):
		pass

	def load_image_from_path(self, path):
		self.path = path
		self.image = scipy.misc.imread(path)

	def save_image(self):
		scipy.misc.imsave(self.path, self.image)

	def get_image(self):
		return self.image

	def get_image_size(self):
		pass

	def undo(self):
		self.undo.pop()

	def apply_scale(self, width, height):
		pass

	def apply_invert(self):
		self.undo.append(self.image)
		self.image = numpy.invert(self.image)
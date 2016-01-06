#!/usr/bin/env python3

import numpy
import scipy.misc
import random, string
from gi.repository import GdkPixbuf


class Editor:

	filetype = ""
	history = []

	def __init__(self, path, image_widget):
		self.path = path
		self.image = scipy.misc.imread(path)
		self.image_widget = image_widget
		self.image_widget.set_from_file(path)

	def save_image(self):
		scipy.misc.imsave(self.path, self.image)

	def get_image(self):
		return self.image

	def get_image_size(self):
		pass

	def do_undo(self):
		self.image = self.history[-1]
		self.history.pop()
		self.reload_image()

	def apply_scale(self, width, height):
		self.history.append(self.image)
		self.image = scipy.misc.imresize(self.image, (width, height))
		self.reload_image()

	def randomword(self, length):
		return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

	def reload_image(self):
		randomfilename = "/tmp/pimp" + self.randomword(6) + ".png"
		scipy.misc.imsave(randomfilename, self.image)
		self.image_widget.set_from_file(randomfilename)

	def apply_invert(self):
		self.history.append(self.image)
		self.image = numpy.invert(self.image)
		self.reload_image()
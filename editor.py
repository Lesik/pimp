#!/usr/bin/env python3

import numpy
import scipy.misc
from gi.repository import GdkPixbuf


class Editor:

	undo = []

	def __init__(self, image_widget):
		self.image_widget = image_widget

	def load_image_from_path(self, path):
		self.path = path
		self.image = scipy.misc.imread(path)
		self.image_widget.set_from_file(path)

	def save_image(self):
		scipy.misc.imsave(self.path, self.image)

	def get_image(self):
		return self.image

	def get_image_size(self):
		pass

	def do_undo(self):
		self.undo.pop()

	def reload_image(self):
		width, height = self.image.size
		asd = GdkPixbuf.Pixbuf.new_from_data(self.image.tostring(),
											 GdkPixbuf.COLORSPACE.RGB,
											 True,
											 8,
											 width,
											 height,
											 width * 4)
		self.image_widget.set_from_pixbuf(asd)

	def apply_scale(self, width, height):
		pass

	def apply_invert(self):
		self.undo.append(self.image)
		self.image = numpy.invert(self.image)
		self.reload_image()
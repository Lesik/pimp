#!/usr/bin/env python3

import numpy
import scipy.misc
import random, string
import os
from gi.repository import GdkPixbuf


class Editor:

	def __init__(self, path, image_widget, builder):
		self.path = path
		self.image = scipy.misc.imread(path)
		self.image_widget = image_widget
		self.image_widget.set_from_file(path)
		self.builder = builder
		self.filetype = ""
		self.history = []
		self.future = []

	def save_image(self):
		self.save_image_as(self.path)

	def save_image_as(self, path):
		if path[-4:] != '.png' and path[-4:] != '.jpg' and \
		path[-4:] != '.bmp' and path[-4:] != '.tif' and\
		path[-5:] != '.tiff':
			path += '.png'
		scipy.misc.imsave(path, self.image)

	def get_image(self):
		return self.image

	def get_image_size(self):
		pass

	def do_undo(self):		
		self.future.append(self.image)
		self.image = self.history[-1]
		self.history.pop()
		self.reload_image()

	def do_redo(self):		
		self.history.append(self.image)
		self.image = self.future[-1]
		self.future.pop()		
		self.reload_image()

	def randomword(self, length):
		return ''.join(random.choice(string.ascii_lowercase)
				for i in range(length))

	def reload_image(self):
		path = "/tmp/pimp" + self.randomword(6) + ".png"
		scipy.misc.imsave(path, self.image)
		self.image_widget.set_from_file(path)
		os.remove(path)
		
	def avail_undo(self):
		return not len(self.history) == 0

	def avail_redo(self):
		return not len(self.future) == 0

	def apply_scale(self, height, width):
		self.history.append(self.image)
		self.future = []
		self.image = scipy.misc.imresize(self.image, (height, width))
		self.reload_image()

	def apply_aspect_ratio(self):		
		height = numpy.size(self.image, 0)
		width = numpy.size(self.image, 1)
		return (height / width)

	def apply_invert(self):
		self.history.append(self.image)
		self.future = []
		self.image = numpy.invert(self.image)
		self.reload_image()

	def apply_grayscale(self):
		self.history.append(self.image)
		self.future = []
		try:
			self.image = self.image[:, :, 0]
			self.reload_image()
		except:
			return

	def apply_flip_horiz(self):
		self.history.append(self.image)
		self.future = []
		self.image = numpy.fliplr(self.image)
		self.reload_image()

	def apply_flip_verti(self):
		self.history.append(self.image)
		self.future = []
		self.image = numpy.flipud(self.image)
		self.reload_image()




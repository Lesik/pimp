#!/usr/bin/env python3

""" Backend of PIMP Imagine Manipulation Program """


__author__ = "6040239: Elizaveta Kovalevskaya, 608220: Oles Pidgornyy"
__licence__ = "GPLv2"
__copyleft__ = "Copyleft 2016"
__credits__ = "Wir haben heute schon so viel verpasst! \
Ey ich glaube wir machen uns sofort auf den Weg nachdem wir gechillt haben!"
__email__ = "klisa-2008@yandex.ru, pidgornyy@informatik.uni-frankfurt.de"


import numpy
import scipy.misc
import scipy.ndimage
import scipy.signal
import sklearn.preprocessing
import random, string
import os


class Editor:

	def __init__(self, path, image_widget, builder):
		self.path = path
		self.image = scipy.ndimage.imread(path)
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
		path[-4:] != '.bmp' and path[-4:] != '.dib' and \
		path[-4:] != '.tif' and path[-4:] != '.xpm' and \
		path[-5:] != '.tiff':
			path += '.png'
		scipy.misc.imsave(path, self.image)

	def get_image(self):
		return self.image

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
		""" Return a random word of requested length.
		:param length: length of the returned word
		:return: the returned word
		"""
		return ''.join(random.choice(string.ascii_lowercase)
				for i in range(length))

	def reload_image(self):
		""" Reloads the UI image widget (GtkImage) by saving the
			vector to a file, then loading it.
		"""
		path = "/tmp/pimp" + self.randomword(6) + ".png"
		scipy.misc.imsave(path, self.image)
		self.image_widget.set_from_file(path)
		os.remove(path)
		
	def avail_undo(self):
		return not len(self.history) == 0

	def avail_redo(self):
		return not len(self.future) == 0

	def apply_scale(self, height, width):
		self.effect_init()
		self.image = scipy.misc.imresize(self.image, (height, width))
		self.reload_image()

	def apply_aspect_ratio(self):
		'''has no funcion yet'''		
		height = numpy.size(self.image, 0)
		width = numpy.size(self.image, 1)
		return (height / width)

	def apply_invert(self):
		self.effect_init()
		self.image = numpy.invert(self.image)
		self.reload_image()

	def apply_grayscale(self):
		self.effect_init()
		try:
			self.image = self.image[:, :, 0]
			self.reload_image()
		except:
			return

	def effect_init(self):
		self.history.append(self.image)
		self.future = []

	def apply_median(self):
		self.effect_init()
		self.image = scipy.ndimage.filters.median_filter(self.image, 20)
		self.reload_image()

	def apply_gauss(self, level):
		self.effect_init()
		self.image = scipy.ndimage.filters.gaussian_filter(self.image,
			level)
		#self.image = scipy.signal.spline_filter(self.image)
		self.reload_image()

	def apply_sobel(self, axis=1):
		self.effect_init()
		self.image = scipy.ndimage.filters.sobel(self.image, axis)
		self.reload_image()

	def apply_laplace(self):
		self.effect_init()
		self.image = scipy.ndimage.filters.laplace(self.image)
		self.reload_image()

	def apply_treshold(self):
		self.effect_init()
		self.image = scipy.stats.treshold(self.image)
		self.reload_image()

	def apply_normalize(self):
		self.effect_init()
		self.image = sklearn.preprocessing.normalize(self.image)
		self.reload_image()

	def apply_histogram(self):
		self.effect_init()
		self.image = numpy.history(self.image)
		self.reload_image()

	def apply_flip_horiz(self):
		self.effect_init()
		self.image = numpy.fliplr(self.image)
		self.reload_image()

	def apply_flip_verti(self):
		self.effect_init()
		self.image = numpy.flipud(self.image)
		self.reload_image()

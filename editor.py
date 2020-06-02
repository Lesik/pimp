#!/usr/bin/env python3

""" Backend of PIMP Imagine Manipulation Program """


__licence__ = "GPLv2"


import numpy
import scipy.misc
import scipy.ndimage
import scipy.stats
import scipy.signal
import matplotlib.pyplot
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
		""" Calles the save_image_as function with it's own path.
		"""
		self.save_image_as(self.path)

	def save_image_as(self, path):
		""" Checks if there's an acceptable ending and saves the file.
		"""
		if path[-4:] != '.png' and path[-4:] != '.jpg' and \
		path[-4:] != '.bmp' and path[-4:] != '.dib' and \
		path[-4:] != '.tif' and path[-4:] != '.xpm' and \
		path[-5:] != '.tiff':
			path += '.png'
		scipy.misc.imsave(path, self.image)

	def get_image(self):
		return self.image

	def do_undo(self):
		""" Applies the undo.
		"""
		self.future.append(self.image)
		self.image = self.history[-1]
		self.history.pop()
		self.reload_image()

	def do_redo(self):
		""" Applies the redo.
		"""
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

	def effect_init(self):
		""" Appends the image for the undo function and clears the 'future'
		images
		"""
		self.history.append(self.image)
		self.future = []

	def avail_undo(self):
		""" Checks if undo is possible.
		"""
		return not len(self.history) == 0

	def avail_redo(self):
		""" Checks if redo is possible.
		"""
		return not len(self.future) == 0

	def apply_scale(self, height, width):
		""" Scales the image.
		"""
		self.effect_init()
		self.image = scipy.misc.imresize(self.image, (height, width))
		self.reload_image()

	def apply_aspect_ratio(self):
		'''has no funcion yet'''		
		height = numpy.size(self.image, 0)
		width = numpy.size(self.image, 1)
		return (height / width)

	def apply_invert(self):
		""" Inverts the image.
		"""
		self.effect_init()
		self.image = numpy.invert(self.image)
		self.reload_image()

	def apply_grayscale(self):
		""" Grayscales the image if possible.
		"""
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
		""" Blurs by median
		"""
		self.effect_init()
		self.image = scipy.ndimage.filters.median_filter(self.image, 20)
		self.reload_image()

	def apply_gauss(self, level):
		""" Blurs by gauss
		"""
		self.effect_init()
		self.image = scipy.ndimage.filters.gaussian_filter(self.image,
			level)
		#self.image = scipy.signal.spline_filter(self.image)
		self.reload_image()

	def apply_sobel(self, axis = 1):
		""" Applies the sobel operator.
		"""
		self.effect_init()
		self.image = scipy.ndimage.filters.sobel(self.image, axis)
		self.reload_image()

	def apply_laplace(self):
		""" Applies the laplace operator.
		"""
		self.effect_init()
		self.image = scipy.ndimage.filters.laplace(self.image)
		self.reload_image()

	def apply_threshold(self, threshmin, threshmax):
		""" Makes a threshold with user data.
		"""
		self.effect_init()
		self.image = scipy.stats.threshold(self.image, threshmin, threshmax)
		self.reload_image()

	def apply_normalize(self):
		""" Normalizes the image.
		"""
		self.effect_init()
		try:
			self.image = self.image[:, :, 0]
			self.image = sklearn.preprocessing.normalize(self.image)
			self.reload_image()
		except:
			return

	def apply_histogram(self):
		""" Makes a histogram in a new window.
		"""
		hist, bins = numpy.histogram(self.image)
		matplotlib.pyplot.bar((bins[:-1] + bins[1:]) / 2,
							  hist,
							  align='center',
							  width = 0.7 * (bins[1] - bins[0]))
		matplotlib.pyplot.show()

	def apply_flip_horiz(self):
		""" Flips the image horizontally.
		"""
		self.effect_init()
		self.image = numpy.fliplr(self.image)
		self.reload_image()

	def apply_flip_verti(self):
		""" Flips the image vertically.
		"""
		self.effect_init()
		self.image = numpy.flipud(self.image)
		self.reload_image()

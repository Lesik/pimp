#!/usr/bin/env python3

""" Frontend of PIMP Imagine Manipulation Program

This software has the following dependencies that need to
be installed in order for it to run properly:

* GTK (PyGObject, Keybinder)
* numpy
* scipy
* matplotlib
* sklearn

THIS PROGRAM IS DEVELOPED FOR GNU/LINUX AND BSD ONLY!
PROGRAM WILL MALFUNCTION WHEN RUN UNDER OTHER OPERATING SYSTEM!

"""


__author__ = "6040239: Elizaveta Kovalevskaya, 608220: Oles Pidgornyy"
__licence__ = "GPLv2"
__copyleft__ = "Copyleft 2016"
__credits__ = "Wir haben heute schon so viel verpasst! \
Ey ich glaube wir machen uns sofort auf den Weg nachdem wir gechillt haben!"
__email__ = "klisa-2008@yandex.ru, pidgornyy@informatik.uni-frankfurt.de"


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, GObject, Keybinder
import editor
from random import randint

UI_FILE = "pimp.ui"


class Pimp:

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.btms = [] # buttons_to_make_sensitive

		self.btn_open = self.builder.get_object('btn-open')
		self.btms.append(self.go('btn-save'))
		self.btms.append(self.go('btn-save-as'))
		self.btn_undo = self.go('btn-undo')
		self.btn_redo = self.go('btn-redo')
		self.btms.append(self.go('menuitem-save'))
		self.btms.append(self.go('menuitem-save-as'))
		self.menuitem_undo = self.go('menuitem_undo')
		self.menuitem_redo = self.go('menuitem_redo')
		self.btms.append(self.go('effect-scale'))
		self.btms.append(self.go('effect-flip-horiz'))
		self.btms.append(self.go('effect-flip-vert'))
		self.btms.append(self.go('effect-invert'))
		self.btms.append(self.go('effect-grayscale'))
		self.btms.append(self.go('effect-sobel'))
		self.btms.append(self.go('effect-laplace'))
		self.btms.append(self.go('effect-median'))
		self.btms.append(self.go('effect-gaussian'))
		self.btms.append(self.go('effect-threshold'))
		self.btms.append(self.go('effect-normalize'))
		self.btms.append(self.go('effect-histogram'))

		Keybinder.init()
		#Keybinder.bind("<Ctrl>O", self.on_open, True)
		#Keybinder.bind("<Ctrl>S", self.on_save, True)
		#Keybinder.bind("<Ctrl>Z", self.on_undo, True)
		#Keybinder.bind("<Ctrl>Y", self.on_redo, True)
		Keybinder.bind("<Ctrl>P", self.celebrate_easter, True)

		self.image_widget = self.builder.get_object('image')

		self.window = self.builder.get_object('window')
		self.builder.get_object('dialog-gaussian').set_transient_for(self.window)
		self.builder.get_object('dialog-scale').set_transient_for(self.window)
		self.window.show_all()

	def go(self, id):
		""" Gets the object from the UI file.
		"""
		return self.builder.get_object(id)

	def celebrate_easter(self, shortcut, var = True):
		""" This is not an easter egg! We swear!
		:param shortcut: the shortcut that was pressed
		:param var: some useless parameter
		"""
		pimp = self.builder.get_object('pimp')
		pimp.set_opacity(0)
		pimp.show_all()
		screen_dimens = [pimp.get_screen().get_width() - pimp.get_size()[0],
			pimp.get_screen().get_height() - pimp.get_size()[1],
			pimp]
		for i in range(500):
			GObject.timeout_add(i * 30, self.fly_around, screen_dimens)

	def fly_around(self, args):
		""" Lets the object move in different directories.
		"""
		args[2].move(randint(0, args[0]),
			randint(0, args[1]))
		args[2].show_all()

	def window_hide(self, window, event):
		""" Hide function so that the window won't be distroyed and has
		no item when it's opened the next time.
		"""
		window.hide()
		return True
	
	def dialog_hide(self, dialog):
		""" Actually we don't need no button cancel, but it's too
		funny, so we let it hide.
		"""
		dialog.hide()
		return True

	def load_image(self, path):
		""" Creating a instance of the Editor class and setting the 
		buttons sensitive, so that changes can be made.
		"""
		self.editor = editor.Editor(path, self.image_widget, self.builder)
		self.sensitivity_check()
		for widget in self.btms:
			widget.set_sensitive(True)

	def on_open(self, widget, var = True):
		""" Opens a Dialog with only picture files.
		"""
		dialog = Gtk.FileChooserDialog("Please choose a file",
			self.window,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		imagefilter = Gtk.FileFilter()
		imagefilter.set_name("Images")
		imagefilter.add_mime_type("image/png")
		imagefilter.add_mime_type("image/jpeg")
		imagefilter.add_mime_type("image/gif")
		imagefilter.add_pattern("*.png")
		imagefilter.add_pattern("*.jpg")
		imagefilter.add_pattern("*.gif")
		imagefilter.add_pattern("*.tif")
		imagefilter.add_pattern("*.tiff")
		imagefilter.add_pattern("*.xpm")
		imagefilter.add_pattern("*.bmp")
		imagefilter.add_pattern("*.dib")
		dialog.add_filter(imagefilter)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.load_image(dialog.get_filename())
		
		dialog.destroy()

	def on_save(self, widget, var = True):
		""" Replaces the original image by the current image.
		"""
		self.editor.save_image()
	
	def on_save_as(self, widget):
		""" Opens a dialog and saves the image as a new file.
		"""
		dialog = Gtk.FileChooserDialog("Please choose a directory",
			self.window,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.editor.save_image_as(dialog.get_filename())

		dialog.destroy()

	def on_undo(self, widget, var = True):
		""" Removes the last change.
		"""
		self.editor.do_undo()
		self.sensitivity_check()

	def on_redo(self, widget, var = True):
		""" Redoes the last change.
		"""
		self.editor.do_redo()
		self.sensitivity_check()

	def sensitivity_check(self):
		""" Checks if there's something to undo or redo and set's the
		buttons sensitive if necessary.
		"""
		self.btn_undo.set_sensitive(self.editor.avail_undo())
		self.btn_redo.set_sensitive(self.editor.avail_redo())
		self.menuitem_undo.set_sensitive(self.editor.avail_undo())
		self.menuitem_redo.set_sensitive(self.editor.avail_redo())

	def g(self, widget_id):
		""" Returns label of a widget with given ID
		:param widget_id: ID of widget
		:return: label of widget
		"""
		return self.builder.get_object(widget_id).get_label()

	def on_effect(self, widget):
		""" This function is run when an effect has been selected.
			Function analyzes the widget and executes the according function
		:param widget: the widget that was pressed
		"""
		chosen_effect = widget.get_label()
		if (chosen_effect == self.g('effect-scale')):
			self.spinbtnheight = self.builder.get_object('spinbtnheight')
			self.spinbtnheight.set_range(1, 1000)
			self.spinbtnwidth = self.builder.get_object('spinbtnwidth')
			self.spinbtnwidth.set_range(1, 1000)
			self.dialog_scale = self.builder.get_object('dialog-scale')
			self.dialog_scale.connect('delete-event', self.window_hide)
			self.dialog_scale.show_all()

		elif (chosen_effect == self.g('effect-flip-horiz')):
			self.editor.apply_flip_horiz()
		elif (chosen_effect == self.g('effect-flip-vert')):
			self.editor.apply_flip_verti()

		elif (chosen_effect == self.g('effect-invert')):
			self.editor.apply_invert()
		elif (chosen_effect == self.g('effect-grayscale')):
			self.editor.apply_grayscale()

		elif (chosen_effect == self.g('effect-sobel')):
			self.editor.apply_sobel()
		elif (chosen_effect == self.g('effect-laplace')):
			self.editor.apply_laplace()
		elif (chosen_effect == self.g('effect-median')):
			self.editor.apply_median()
		elif (chosen_effect == self.g('effect-gaussian')):
			self.smoothing_gaussian = \
				self.builder.get_object('smoothing-gaussian')
			self.dialog_gaussian = self.builder.get_object('dialog-gaussian')
			self.dialog_gaussian.connect('delete-event', self.window_hide)
			self.dialog_gaussian.show_all()

		elif (chosen_effect == self.g('effect-threshold')):
			self.threshold_min = self.builder.get_object('threshold_min')
			self.threshold_min.set_range(0, 1000)
			self.threshold_max = self.builder.get_object('threshold_max')
			self.threshold_max.set_range(0, 1000)
			self.dialog_threshold = self.builder.get_object('dialog_threshold')
			self.dialog_threshold.connect('delete-event', self.window_hide)
			self.dialog_threshold.show_all()

		elif (chosen_effect == self.g('effect-normalize')):
			self.editor.apply_normalize()
		elif (chosen_effect == self.g('effect-histogram')):
			self.editor.apply_histogram()

		self.sensitivity_check()

	def on_effect_scale_commit(self, user_data):
		""" Gets the user values for scale.
		"""
		height = self.spinbtnheight.get_value_as_int()
		width = self.spinbtnwidth.get_value_as_int()
		self.editor.apply_scale(height, width)
		self.sensitivity_check()
		self.dialog_scale.hide()

	def on_effect_gauss_commit(self, user_data):
		""" Gets the user values for gauss.
		"""
		level = self.smoothing_gaussian.get_value_pos()
		level = level * 0.5
		self.editor.apply_gauss(level)
		self.sensitivity_check()
		self.dialog_gaussian.hide()

	def on_effect_thresh_commit(self, user_data):
		""" Gets the user values for threshold.
		"""
		threshmin = self.threshold_min.get_value_as_int()
		threshmax = self.threshold_max.get_value_as_int()
		self.editor.apply_threshold(threshmin, threshmax)
		self.sensitivity_check()
		self.dialog_threshold.hide()

	def on_about(self, widget):
		""" Opens the infomation about PIMP.
		"""
		self.builder.get_object('dialog-about').show()

	def on_quit(self, widget):
		""" Destroys the window.
		"""
		Gtk.main_quit()
		
print("THIS PROGRAM IS DEVELOPED FOR GNU/LINUX AND BSD ONLY!")
print("PROGRAM WILL MALFUNCTION WHEN RUN UNDER OTHER OPERATING SYSTEM!")

if __name__ == "__main__":
	Pimp()
	Gtk.main()


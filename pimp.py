#!/usr/bin/env python3

""" Frontend of PIMP Imagine Manipulation Program """


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
import numpy
import scipy.misc
import editor
from random import randint
from time import sleep

UI_FILE = "pimp.ui"


class Pimp:

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.btn_open = self.builder.get_object('btn-open')
		self.btn_save = self.builder.get_object('btn-save')
		self.btn_save_as = self.builder.get_object('btn-save-as')
		self.btn_undo = self.builder.get_object('btn-undo')
		self.btn_redo = self.builder.get_object('btn-redo')
		self.menuitem_save = self.builder.get_object('menuitem-save')
		self.menuitem_save_as = self.builder.get_object('menuitem-save-as')
		self.menuitem_undo = self.builder.get_object('menuitem_undo')
		self.menuitem_redo = self.builder.get_object('menuitem_redo')
		self.effect_scale = self.builder.get_object('effect-scale')
		self.effect_flip_horiz = self.builder.get_object('effect-flip-horiz')
		self.effect_flip_vert = self.builder.get_object('effect-flip-vert')
		self.effect_invert = self.builder.get_object('effect-invert')
		self.effect_grayscale = self.builder.get_object('effect-grayscale')
		self.effect_sobel = self.builder.get_object('effect-sobel')
		self.effect_laplace = self.builder.get_object('effect-laplace')
		self.effect_median = self.builder.get_object('effect-median')
		self.effect_gaussian = self.builder.get_object('effect-gaussian')

		Keybinder.init()
		#Keybinder.bind("<Ctrl>O", self.on_open, True)
		#Keybinder.bind("<Ctrl>S", self.on_save, True)
		#Keybinder.bind("<Ctrl>Z", self.on_undo, True)
		#Keybinder.bind("<Ctrl>Y", self.on_redo, True)
		Keybinder.bind("<Ctrl>P", self.celebrate_easter, True)

		self.image_widget = self.builder.get_object('image')

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def celebrate_easter(self, shortcut, var = True):
		""" This is not an easter egg! I swear!
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
		args[2].move(randint(0, args[0]),
			randint(0, args[1]))
		args[2].show_all()

	def window_hide(self, window, event):
		window.hide()
		return True

	def load_image(self, path):
		self.editor = editor.Editor(path, self.image_widget, self.builder)
		self.sensitivity_check()
		self.menuitem_save.set_sensitive(True)
		self.menuitem_save_as.set_sensitive(True)
		self.btn_save.set_sensitive(True)
		self.btn_save_as.set_sensitive(True)
		self.effect_scale.set_sensitive(True)
		self.effect_flip_horiz.set_sensitive(True)
		self.effect_flip_vert.set_sensitive(True)
		self.effect_invert.set_sensitive(True)
		self.effect_grayscale.set_sensitive(True)
		self.effect_sobel.set_sensitive(True)
		self.effect_laplace.set_sensitive(True)
		self.effect_median.set_sensitive(True)
		self.effect_gaussian.set_sensitive(True)

	def on_open(self, widget, var = True):
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
		self.editor.save_image()
	
	def on_save_as(self, widget):
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
		self.editor.do_undo()
		self.sensitivity_check()

	def on_redo(self, widget, var = True):
		self.editor.do_redo()
		self.sensitivity_check()

	def sensitivity_check(self):
		self.btn_undo.set_sensitive(self.editor.avail_undo())
		self.btn_redo.set_sensitive(self.editor.avail_redo())
		self.menuitem_undo.set_sensitive(self.editor.avail_undo())
		self.menuitem_redo.set_sensitive(self.editor.avail_redo())

	def on_effect_scale_commit(self, button):
		height = self.spinbtnheight.get_value_as_int()
		width = self.spinbtnwidth.get_value_as_int()
		self.editor.apply_scale(height, width)
		self.sensitivity_check()
		self.dialog_scale.hide()
	
	def on_effect_scale_cancel(self, user_data):
		self.dialog_scale.hide()
		return True

	def aspect_ratio_checkbtn_toggled(self, user_data):
		# has no function yet
		ratio = self.editor.apply_aspect_ratio()
		print(self.spinbtnheight.get_adjustment())
		self.spinbtnheight.configure(ratio, 0)
		#self.spinbtnwidth.configure(adjustment, ratio, 0)	

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
			self.aspect_ratio_checkbtn = \
				self.builder.get_object('aspect_ratio_checkbtn')
			self.dialog_scale = self.builder.get_object('dialog_scale')
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
			self.dialog_gaussian = self.builder.get_object('dialog_gaussian')
			self.dialog_gaussian.connect('delete-event', self.window_hide)
			self.dialog_gaussian.show_all()
		self.sensitivity_check()

	def on_effect_gauss_commit(self, button):
		level = self.smoothing_gaussian.get_value_pos()
		level = level * (1 / 2)
		self.editor.apply_gauss(level)
		self.sensitivity_check()
		self.dialog_gaussian.hide()
	
	def on_effect_gauss_cancel(self, user_data):
		self.dialog_gaussian.hide()
		return True
	    
	def on_window_destroy(self, window):
		Gtk.main_quit()

	def on_about(self, widget):
		self.builder.get_object('dialog-about').show()

	def on_quit(self, widget):
		Gtk.main_quit()
		
print("THIS PROGRAM IS DEVELOPED FOR GNU/LINUX AND BSD ONLY!")
print("PROGRAM WILL MALFUNCTION WHEN RUN UNDER OTHER OPERATING SYSTEM!")

if __name__ == "__main__":
	Pimp()
	Gtk.main()


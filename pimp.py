#!/usr/bin/env python3

__author__ = "6040239: Elizaveta Kovalevskaya, 608220: Oles Pidgornyy"
__licence__ = "GPLv2"
__copyright__ = "Copyright 2015/2016 – EPR-Goethe-Uni"
__credits__ = "Wir haben heute schon so viel verpasst! \
Ey ich glaube wir machen uns sofort auf den Weg nachdem wir gechillt haben!"
__email__ = "klisa-2008@yandex.ru"
'''frontend of P Imagine Manipulation Programm'''


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
		self.btn_undo = self.builder.get_object('btn-undo')
		self.btn_redo = self.builder.get_object('btn-redo')
		self.menuitem_undo = self.builder.get_object('menuitem_undo')
		self.menuitem_redo = self.builder.get_object('menuitem_redo')
		
		Keybinder.init()
		#Keybinder.bind("<Ctrl>O", self.on_open, True)
		#Keybinder.bind("<Ctrl>S", self.on_save, True)
		#Keybinder.bind("<Ctrl>Z", self.on_undo, True)
		#Keybinder.bind("<Ctrl>Y", self.on_redo, True)
		Keybinder.bind("<Ctrl>P", self.on_pimp, True)

		self.image_widget = self.builder.get_object('image')

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def on_pimp(self, shortcut, var = True):
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

	def on_effect_scale(self, user_data):
		self.spinbtnheight = self.builder.get_object('spinbtnheight')
		self.spinbtnheight.set_range(1, 1000)
		self.spinbtnwidth = self.builder.get_object('spinbtnwidth')
		self.spinbtnwidth.set_range(1, 1000)
		self.aspect_ratio_checkbtn = \
			self.builder.get_object('aspect_ratio_checkbtn')
		self.dialog_scale = self.builder.get_object('dialog_scale')
		self.dialog_scale.connect('delete-event', self.window_hide)
		self.dialog_scale.show_all()

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
		'''has no function yet'''
		ratio = self.editor.apply_aspect_ratio()
		print(self.spinbtnheight.get_adjustment())
		self.spinbtnheight.configure(ratio, 0)
		#self.spinbtnwidth.configure(adjustment, ratio, 0)	

	def on_effect_invert(self, user_data):
		self.editor.apply_invert()		
		self.sensitivity_check()

	def on_effect_sobel(self, user_data):
		self.editor.apply_sobel()
		self.sensitivity_check()

	def on_effect_median(self, user_date):
		self.editor.apply_median()
		self.sensitivity_check()

	def on_effect_gauss(self, user_data):
		self.smoothing_gaussian = \
			self.builder.get_object('smoothing-gaussian')
		self.dialog_gaussian = self.builder.get_object('dialog_gaussian')
		self.dialog_gaussian.connect('delete-event', self.window_hide)
		self.dialog_gaussian.show_all()

	def on_effect_gauss_commit(self, button):
		level = self.smoothing_gaussian.get_value_pos()
		level = level * (1 / 2)
		self.editor.apply_gauss(level)
		self.sensitivity_check()
		self.dialog_gaussian.hide()
	
	def on_effect_gauss_cancel(self, user_data):
		self.dialog_gaussian.hide()
		return True
	    
	def on_effect_grayscale(self, user_data):
		self.editor.apply_grayscale()
		self.sensitivity_check()

	def on_window_destroy(self, window):
		Gtk.main_quit()

	def on_effect_flip_horiz(self, widget):
		self.editor.apply_flip_horiz()
		self.sensitivity_check()

	def on_effect_flip_verti(self, widget):
		self.editor.apply_flip_verti()
		self.sensitivity_check()

	def on_about(self, widget):
		# dummy function, will use later
		pass

	def on_quit(self, widget):
		Gtk.main_quit()
		


if __name__ == "__main__":
	Pimp()
	Gtk.main()

#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Keybinder
import numpy
import scipy.misc
import editor

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
		Keybinder.bind("<Ctrl>O", self.on_open, True)
		Keybinder.bind("<Ctrl>S", self.on_save, True)
		Keybinder.bind("<Ctrl>Z", self.on_undo, True)
		Keybinder.bind("<Ctrl><Shift>Z", self.on_redo, True)
		Keybinder.bind("<Ctrl>P", self.on_pimp, True)

		self.image_widget = self.builder.get_object('image')

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def on_pimp(self):
		pass

	def window_hide(self, window, event):
		window.hide()
		return True

	def load_image(self, path):
		self.editor = editor.Editor(path, self.image_widget, self.builder)
		self.sensitivity_check()

	def on_open(self, widget):
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
		imagefilter.add_pattern("*.xpm")
		dialog.add_filter(imagefilter)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.load_image(dialog.get_filename())
		
		dialog.destroy()

	def on_save(self, widget):
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

	def on_undo(self, widget):
		self.editor.do_undo()
		self.sensitivity_check()

	def on_redo(self, widget):
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
		ratio = self.editor.apply_aspect_ratio()
		print(self.spinbtnheight.get_adjustment())
		self.spinbtnheight.configure(ratio, 0)
		#self.spinbtnwidth.configure(adjustment, ratio, 0)	

	def on_effect_invert(self, user_data):
		self.editor.apply_invert()		
		self.sensitivity_check()

	def on_effect_gauss(self, user_data):
	        self.editor.apply_gauss()
	        self.sensitivity_check()

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

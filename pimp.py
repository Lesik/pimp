#!/usr/bin/env python3

from gi.repository import Gtk
#gi.require_version('Gtk', '3.6')
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

		self.image_widget = self.builder.get_object('image')

		self.editor = editor.Editor(self.image_widget)

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def load_image(self, filename):
		self.editor.load_image_from_path(filename)

	def save_file(self, filename):
		if filename[-4:] != '.png' and filename[-4:] != '.jpg' and \
		filename[-4:] != '.tif' and filename[-5:] != '.tiff':
			filename += '.png'
		scipy.misc.imsave(filename, self.image)

	def on_btn_open_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a file",
			self.window,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.load_image(dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("lol?")

		dialog.destroy()
	
	def on_btn_save_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a directory",
			self.window,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.save_file(dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("lol?")

		dialog.destroy()

	def on_effect_scale(self, user_data):
		self.editor.apply_invert()

	def on_effect_invert(self, user_data):
		self.editor.apply_invert()

	def on_window_destroy(self, window):
		Gtk.main_quit()


if __name__ == "__main__":
	Pimp()
	Gtk.main()

#!/usr/bin/env python3

from gi.repository import Gtk
import numpy
import scipy.misc

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

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def load_image(self, filename):
		self.current_file = filename
		self.image = scipy.misc.imread(filename)
		self.image_widget.set_from_file(filename)

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
		self.spinbtnwidth = self.builder.get_object('spinbtnwidth')
		self.spinbtnheight = self.builder.get_object('spinbtnheight')
		self.popup_scale = self.builder.get_object('popup_scale')
		self.popup_scale.show_all()

		

	def on_effect_invert(self, user_data):
		if self.current_file is not None:
			self.image = numpy.invert(self.image)
			self.save_file(self.current_file)
			self.load_image(self.current_file)

	def on_window_destroy(self, window):
		Gtk.main_quit()


if __name__ == "__main__":
	Pimp()
	Gtk.main()

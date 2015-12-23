#!/usr/bin/env python3

from gi.repository import Gtk

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

		self.image = self.builder.get_object('image')
		self.builder.get_object('window').show_all()
		self.load_image()

	def load_image(self):
		self.image.set_from_file('Lenna.png')

	def on_window_destroy(self, window):
		Gtk.main_quit()


if __name__ == "__main__":
	Pimp()
	Gtk.main()

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

		self.window = self.builder.get_object('window')
		self.window.show_all()

	def load_image(self, filename):
		self.image.set_from_file(filename)

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

	def on_window_destroy(self, window):
		Gtk.main_quit()


if __name__ == "__main__":
	Pimp()
	Gtk.main()

#!/usr/bin/env python3

from gi.repository import Gtk, Keybinder

UI_FILE = "pimp.ui"

class Pimp:

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals()

		self.btn_open = self.builder.get_object('btn-open')
		self.btn_save = self.builder.get_object('btn-save')
		self.btn_undo = self.builder.get_object('btn-undo')
		self.btn_redo = self.builder.get_object('btn-redo')

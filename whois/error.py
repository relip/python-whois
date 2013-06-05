# -*- coding: utf-8 -*-

class InvalidInputText(Exception):
	def __init__(self, text):
		self.message = "Invalid input text: %s"%(text)
		Exception.__init__(self, self.message)

class Category:

	def __init__(self, id, name, slug, icon, input, output):
		self._id = id
		self.name = name
		self.slug = slug
		self.icon = icon
		self.input = input
		self.output = output

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		if type(value) == str and value != "":
			self._name = value
		else:
			raise ValueError("Geen geldige categorie naam!")

	@property
	def slug(self):
		return self._slug

	@slug.setter
	def slug(self, value):
		if type(value) == str and value != "":
			self._slug = value
		else:
			raise ValueError("Geen geldige categorie slug!")

	@property
	def icon(self):
		return self._icon

	@slug.setter
	def icon(self, value):
		if type(value) == str and value != "":
			self._icon = value
		else:
			raise ValueError("Geen geldig categorie icon!")

	@property
	def input(self):
		return self._input

	@input.setter
	def input(self, value):
		if type(value) == bool:
			self._input = value
		else:
			raise ValueError("Categorie input is geen geldige boolean.")

	@property
	def output(self):
		return self._output

	@output.setter
	def output(self, value):
		if type(value) == bool:
			self._output = value
		else:
			raise ValueError("Categorie output is geen geldige boolean.")

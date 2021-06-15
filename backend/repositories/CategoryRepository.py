from utils import serialize
from models.Category import Category
from repositories.Database import Database
from repositories.SensorRepository import SensorRepository
from repositories.OutputRepository import OutputRepository


class CategoryRepository:

	@staticmethod
	def all():
		categories = []
		sql = "SELECT * FROM category;"

		rows = Database.get_rows(sql)

		if rows is not None:
			for row in rows:
				categories.append(CategoryRepository.map_to_object(row))

		return categories

	def all_seeded():
		categories = serialize(CategoryRepository.all())

		for category in categories:
			devices = serialize(CategoryRepository.devices(category['_id']))

			if (category['_output'] == True):
				category['_devices'] = devices['outputs']
			else:
				category['_devices'] = devices['sensors']

		return categories

	@staticmethod
	def find(id):
		sql = "SELECT * FROM category WHERE id = %s;"
		params = [id]

		row = Database.get_one_row(sql, params)

		return CategoryRepository.map_to_object(row)

	@staticmethod
	def devices(category_id):
		category = CategoryRepository.find(category_id)

		if category is None:
			return None

		if category.input:
			return {'sensors': SensorRepository.get_for_category(category)}
		else:
			return {'outputs': OutputRepository.get_for_category(category)}

	@staticmethod
	def get_one_by_slug(slug_value):
		sql = "SELECT * FROM category WHERE slug = %s LIMIT 1"
		params = [slug_value]

		row = Database.get_one_row(sql, params)

		return CategoryRepository.map_to_object(row)

	@staticmethod
	def map_to_object(row):
		if row is not None and type(row) is dict:
			id = int(row['id'])
			name = CategoryRepository.check_column(row, 'name')
			slug = CategoryRepository.check_column(row, 'slug')
			icon = CategoryRepository.check_column(row, 'icon')
			input = bool(row['input'])
			output = bool(row['output'])

			return Category(id, name, slug, icon, input, output)

		return row

	@staticmethod
	def check_column(row, column):
		if column in row.keys() and row[column] is not None:
			return row[column]

		return ""

from models.Sensor import Sensor
from repositories.Database import Database

class SensorRepository:

	@staticmethod
	def all():
		sensors = []
		sql = "SELECT * FROM sensor;"

		rows = Database.get_rows(sql)

		if rows is not None:
			for row in rows:
				sensors.append(SensorRepository.map_to_object(row))

		return sensors

	@staticmethod
	def find(id):
		sql = "SELECT * FROM sensor WHERE id = %s;"
		params = [id]

		row = Database.get_one_row(sql, params)

		return SensorRepository.map_to_object(row)

	@staticmethod
	def find_one_by_unit(unit_name):
		sql = "SELECT * FROM smartpccase.sensor WHERE unit = %s;"
		params = [unit_name]

		row = Database.get_one_row(sql, params)

		return SensorRepository.map_to_object(row)

	@staticmethod
	def get_for_category(category):
		sensors = []
		sql = "SELECT * FROM sensor WHERE category_id = %s"
		params = [category.id]

		rows = Database.get_rows(sql, params)

		if rows is not None:
			for row in rows:
				sensors.append(SensorRepository.map_to_object(row))

		return sensors

	@staticmethod
	def map_to_object(row):
		if row is not None and type(row) is dict:
			id = int(row['id'])
			name = SensorRepository.check_column(row, 'name')
			unit = SensorRepository.check_column(row, 'unit')
			input_bus = SensorRepository.check_column(row, 'input_bus')

			try:
				input_pin = int(row['input_pin'])
			except ValueError:
				input_pin = row['input_pin']
			
			category_id = int(row['category_id'])
			
			return Sensor(id, name, unit, input_bus, input_pin, category_id)
		
		return row

	@staticmethod
	def check_column(row, column):
		if column in row.keys() and row[column] is not None:
			return row[column]

		return ""
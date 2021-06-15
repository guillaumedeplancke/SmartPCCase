from models.Output import Output
from repositories.Database import Database

class OutputRepository:

	@staticmethod
	def all():
		outputs = []
		sql = "SELECT * FROM output;"

		rows = Database.get_rows(sql)

		if rows is not None:
			for row in rows:
				outputs.append(OutputRepository.map_to_object(row))

		return outputs

	@staticmethod
	def find(id):
		sql = "SELECT * FROM output WHERE id = %s;"
		params = [id]

		row = Database.get_one_row(sql, params)

		return OutputRepository.map_to_object(row)

	@staticmethod
	def get_for_category(category):
		outputs = []
		sql = "SELECT * FROM output WHERE category_id = %s;"
		params = [category.id]

		rows = Database.get_rows(sql, params)

		if rows is not None:
			for row in rows:
				outputs.append(OutputRepository.map_to_object(row))

		return outputs

	@staticmethod
	def map_to_object(row):
		if row is not None and type(row) is dict:
			id = int(row['id'])
			name = OutputRepository.check_column(row, 'name')
			description = OutputRepository.check_column(row, 'description')
			icon = OutputRepository.check_column(row, 'icon')
			output_num = OutputRepository.check_column(row, 'output_num')
			is_pwm = bool(OutputRepository.check_column(row, 'is_pwm'))
			category_id = int(row['category_id'])

			return Output(id, name, description, icon, output_num, is_pwm, category_id)
		
		return row

	@staticmethod
	def check_column(row, column):
		if column in row.keys() and row[column] is not None:
			return row[column]

		return ""

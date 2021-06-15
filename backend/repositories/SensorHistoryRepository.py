from repositories.Database import Database
import datetime


class SensorHistoryRepository:

    @staticmethod
    def create(history_item):
        sql = "INSERT INTO sensor_history (sensor_id, value, date, time) VALUES (%s, %s, %s, %s);"

        params = [history_item.sensor_id, history_item.value,
                  history_item.date, history_item.time]

        created_id = Database.execute_sql(sql, params)

        history_item.id = created_id

        return history_item

    @staticmethod
    def get(sensor_id):
        return SensorHistoryRepository.get_for_date(sensor_id, datetime.datetime.today().strftime('%Y-%m-%d'))

    @staticmethod
    def get_for_date(sensor_id, date):
        sql = "SELECT value, date, time FROM smartpccase.sensor_history WHERE sensor_id = %s AND date = %s;"

        params = [sensor_id, date]

        rows = Database.get_rows(sql, params)

        for row in rows:
            row['datetime'] = SensorHistoryRepository.date_and_time_to_datetime(
                row['date'], (datetime.datetime.min + row['time']).time())

            row['date'] = str(row['date'])
            row['time'] = str(row['time'])

            row.pop('date')
            row.pop('time')

        return rows

    @staticmethod
    def date_and_time_to_datetime(date, time):
        return datetime.datetime.combine(date, time)

from repositories.Database import Database
import datetime


class OutputHistoryRepository:

    @staticmethod
    def create(history_item):
        sql = "INSERT INTO output_history (output_id, user_id, value, date, time) VALUES (%s, %s, %s, %s, %s);"

        params = [history_item.output_id, history_item.user_id,
                  history_item.value, history_item.date, history_item.time]

        created_id = Database.execute_sql(sql, params)

        history_item.id = created_id

        return history_item

    @staticmethod
    def get(output_id):
        sql = "SELECT * FROM smartpccase.output_history WHERE output_id = %s AND date = curdate();"

        params = [output_id]

        rows = Database.get_rows(sql, params)

        for row in rows:
            row['datetime'] = OutputHistoryRepository.date_and_time_to_datetime(
                row['date'], (datetime.datetime.min + row['time']).time())

            row['date'] = str(row['date'])
            row['time'] = str(row['time'])

        return rows

    def get_latest_10(output_id):
        sql = "SELECT * FROM output_history WHERE output_id = %s ORDER BY date DESC, time DESC LIMIT 5;"

        params = [output_id]

        rows = Database.get_rows(sql, params)

        if rows is not None:
            for row in rows:
                row['datetime'] = OutputHistoryRepository.date_and_time_to_datetime(
                    row['date'], (datetime.datetime.min + row['time']).time())

                row['date'] = str(row['date'])
                row['time'] = str(row['time'])

        return rows

    @staticmethod
    def date_and_time_to_datetime(date, time):
        return datetime.datetime.combine(date, time)

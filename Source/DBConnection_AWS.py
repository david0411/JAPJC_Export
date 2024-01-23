from datetime import datetime
import mysql.connector


class DBConnection_AWS:
    def __init__(self):
        try:
            self.conn = (mysql.connector.
                         connect(user='admin', password='password',
                                 host='fsse2305-davidcheng-db.cbwrtddcgbnj.ap-southeast-1.rds.amazonaws.com',
                                 database='JAPJC'))
            self.conn.time_zone = '+08:00'
            self.c = self.conn.cursor(buffered=True)
        except Exception as e:
            print('Database connection error')
            print(e)

        self.sql_horse_list = "SELECT HORSE_ID FROM JAPJC_HORSE"
        self.sql_first_fixture = "SELECT MIN(FIXTURE) FROM JAPJC_FIXTURES"
        self.sql_last_fixture = "SELECT MAX(FIXTURE) FROM JAPJC_FIXTURES"

        self.sql_first_horse_record_date = "SELECT MIN(日期) FROM JAPJC_HORSE_RESULT WHERE ID = %s"
        self.sql_last_horse_record_date = "SELECT MAX(日期) FROM JAPJC_HORSE_RESULT WHERE ID = %s"

        self.sql_first_race_result_date = "SELECT MIN(日期) FROM JAPJC_RESULT2"
        self.sql_last_race_result_date = "SELECT MAX(日期) FROM JAPJC_RESULT2"

        self.sql_prev_rd = "SELECT FIXTURE, FEATURE FROM JAPJC_FIXTURES WHERE FIXTURE <= %s ORDER BY FIXTURE DESC"
        self.sql_next_rd = "SELECT FIXTURE, FEATURE FROM JAPJC_FIXTURES WHERE FIXTURE >= %s ORDER BY FIXTURE"

        self.sql_next_venue = "SELECT FEATURE FROM JAPJC_FIXTURES WHERE FIXTURE >= %s ORDER BY FIXTURE"
        self.sql_future_rd_date_list = "SELECT FIXTURE FROM JAPJC_FIXTURES WHERE FIXTURE >= %s"
        self.sql_next_venue2 = "SELECT FEATURE FROM JAPJC_FIXTURES WHERE FIXTURE = %s"
        self.sql_race_num = ("SELECT MAX(場次) FROM JAPJC_CARD WHERE 日期 "
                             "IN(SELECT FIXTURE FROM JAPJC_FIXTURES WHERE FIXTURE >= %s)")

        self.sql_check_fixture = "SELECT COUNT(*) FROM JAPJC_FIXTURES WHERE FIXTURE = %s"
        self.sql_pools = "SELECT 場次, 投注額時間, WIN, PLA FROM JAPJC_JCPOOL WHERE 日期 = %s"
        self.sql_odds = "SELECT 場次, 賠率時間, 馬號, 獨贏, 位置 FROM JAPJC_JCODDS WHERE 日期 = %s"

    def get_prev_rd(self):
        self.c.execute(self.sql_prev_rd, [datetime.now()])
        return self.c.fetchone()

    def get_next_rd(self):
        self.c.execute(self.sql_next_rd, [datetime.now().date()])
        return self.c.fetchone()

    def get_next_rd2(self, target_date):
        self.c.execute(self.sql_future_rd_date_list, [target_date])
        return [item[0] for item in self.c.fetchall()]

    def get_next_venue(self):
        self.c.execute(self.sql_next_venue)
        for row in self.c:
            return str(row[0])[:2]

    def get_next_venue2(self, target_date):
        self.c.execute(self.sql_next_venue2, [target_date])
        for row in self.c:
            return str(row[0])[:2]

    def get_race_num(self):
        self.c.execute(self.sql_race_num, [datetime.now().date()])
        for row in self.c:
            return int(row[0])

    def get_pools(self, target_date):
        self.c.execute(self.sql_pools, [target_date])
        return [[item[0], item[1], item[2], item[3]] for item in self.c.fetchall()]

    def get_odds(self, target_date):
        self.c.execute(self.sql_odds, [target_date])
        return [[item[0], item[1], item[2], item[3], item[4]] for item in self.c.fetchall()]

    def close_connection(self):
        self.conn.close()

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

        self.sql_next_rd = "SELECT FIXTURE, FEATURE FROM JAPJC_FIXTURES WHERE FIXTURE >= %s ORDER BY FIXTURE"
        self.sql_race_num = "SELECT MAX(場次) FROM JAPJC_CARD WHERE 日期 = %s"
        self.sql_horse_num = "SELECT MAX(馬匹編號) FROM JAPJC_CARD WHERE  日期 = %s AND 場次 = %s"
        self.sql_pools = "SELECT 場次, 投注額時間, WIN, PLA FROM JAPJC_JCPOOL WHERE 日期 = %s"
        self.sql_odds = "SELECT 場次, 賠率時間, 馬號, 獨贏, 位置 FROM JAPJC_JCODDS WHERE 日期 = %s"

    def get_next_rd(self):
        self.c.execute(self.sql_next_rd, [datetime.now().date()])
        return self.c.fetchone()

    def get_race_num(self, target_date):
        self.c.execute(self.sql_race_num, [target_date])
        return self.c.fetchone()[0]

    def get_horse_num(self, target_date, race_num):
        self.c.execute(self.sql_horse_num, [target_date, race_num])
        return self.c.fetchone()[0]

    def get_pools(self, target_date):
        self.c.execute(self.sql_pools, [target_date])
        return [[item[0], item[1], item[2], item[3]] for item in self.c.fetchall()]

    def get_odds(self, target_date):
        self.c.execute(self.sql_odds, [target_date])
        return [[item[0], item[1], item[2], item[3], item[4]] for item in self.c.fetchall()]

    def close_connection(self):
        self.conn.close()

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
        # HORSE_ID, HORSE_NAME
        self.sql_import_horse = "INSERT INTO JAPJC_HORSE VALUES(%s,%s)"
        # 日期,場次,馬匹編號,六次近績,綵衣,馬名,負磅,騎師,檔位,練馬師,評分,評分加減,排位體重,優先參賽次序,配備
        self.sql_import_card = ("INSERT INTO JAPJC_CARD "
                                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # FIXTURE, FEATURE
        self.sql_import_fixture = "INSERT INTO JAPJC_FIXTURES VALUES(%s,%s)"
        # 日期,場次,投注額時間,Win,PLA,QIN,QPL,FCT,TCE,TRI,F_F,DBL,TBL,D_T,T_T,6UP
        self.sql_import_jcpool = "INSERT INTO JAPJC_JCPOOL VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 日期,賠率時間,場次,馬號,綵衣,馬名,檔位,負磅,騎師,練馬師,獨贏,位置,EMT
        self.sql_import_jcodds = "INSERT INTO JAPJC_JCODDS VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # ID, 場次, 名次, 日期, 馬場跑道賽道, 途程, 場地狀況, 賽事班次, 檔位, 評分, 練馬師, 騎師,
        # 頭馬距離, 獨贏賠率, 實際負磅, 沿途走位, 完成時間, 排位體重, 配備, 賽事重播, LAST_UPDATE
        self.sql_import_horse_result = ("INSERT INTO JAPJC_HORSE_RESULT VALUES (%s,%s,%s,%s,%s,%s,%s,"
                                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # 日期, 時間, 途程, 賽事班次
        self.sql_import_race_details = "INSERT INTO JAPJC_RACE_DETAILS VALUES(%s,%s,%s)"
        # 日期, 場次, 場號, 賽事班次, 途程, 場地狀況, 賽事名稱, 馬場跑道, 馬場賽道, 時間1, 時間2, 時間3, 時間4, 時間5, 時間6,
        # 分段時間1, 分段時間2, 分段時間3, 分段時間4, 分段時間5, 分段時間6, 分段時間7, 分段時間8, 分段時間9, 分段時間10
        self.sql_import_race_result1 = ("INSERT INTO JAPJC_RESULT VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # 日期, 場次, 名次, 馬號, 馬名, 騎師, 練馬師, 負磅, 排位體重, 檔位, 頭馬距離, 沿途走位, 完成時間, 獨贏賠率
        self.sql_import_race_result2 = "INSERT INTO JAPJC_RESULT2 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        self.sql_delete_fixture = "DELETE FROM JAPJC_FIXTURES WHERE FIXTURE>=%s"

    def get_horse_list(self):
        self.c.execute(self.sql_horse_list)
        return [item[0] for item in self.c.fetchall()]

    def get_first_horse_record_date(self, target_horse_id):
        self.c.execute(self.sql_first_horse_record_date, target_horse_id)
        return self.c.fetchone()[0]

    def get_last_horse_record_date(self, target_horse_id):
        self.c.execute(self.sql_last_horse_record_date, target_horse_id)
        return self.c.fetchone()[0]

    def get_first_fixture(self):
        self.c.execute(self.sql_first_fixture)
        return self.c.fetchone()[0]

    def get_last_fixture(self):
        self.c.execute(self.sql_last_fixture)
        return self.c.fetchone()[0]

    def get_first_race_result_date(self):
        self.c.execute(self.sql_first_race_result_date)
        return self.c.fetchone()[0]

    def get_last_race_result_date(self):
        self.c.execute(self.sql_last_race_result_date)
        return self.c.fetchone()[0]

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

    def import_data(self, data_format, data_type, data):
        import_sql = None
        if data_type == 'horse':
            import_sql = self.sql_import_horse
        elif data_type == 'card':
            import_sql = self.sql_import_card
        elif data_type == 'fixture':
            import_sql = self.sql_import_fixture
        elif data_type == 'result1':
            import_sql = self.sql_import_race_result1
        elif data_type == 'result2':
            import_sql = self.sql_import_race_result2
        elif data_type == 'horse_result':
            import_sql = self.sql_import_horse_result
        elif data_type == 'jcpool':
            import_sql = self.sql_import_jcpool
        elif data_type == 'jcodds':
            import_sql = self.sql_import_jcodds

        if data_format == 'row':
            try:
                self.c.execute(import_sql, data)
                self.conn.commit()
            except ValueError as e:
                print(e)
                pass
        elif data_format == 'df':
            try:
                for i, row in data.iterrows():
                    self.c.execute(import_sql, tuple(row))
                    self.conn.commit()
            except ValueError as e:
                print(e)
                pass
        else:
            try:
                for i, row in data.iterrows():
                    ls = list(row)
                    if ls[1] == '場次' or '馬季' in ls[1]:
                        continue
                    ls[3] = datetime.strptime(ls[3][:6] + '20' + ls[3][6:], "%d/%m/%Y")
                    for j in range(len(ls)):
                        if ls[j] == '--':
                            ls[j] = ''
                    self.c.execute(self.sql_import_horse_result, tuple(ls))
                    self.conn.commit()
            except Exception as e:
                print(e)

    def delete_fixture(self, start_date):
        self.c.execute(self.sql_delete_fixture, [start_date])

    def close_connection(self):
        self.conn.close()

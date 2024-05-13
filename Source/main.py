import datetime as dt
from Source.DBConnection_AWS import DBConnection_AWS
import xlsxwriter

if __name__ == '__main__':
    db_connection = DBConnection_AWS()
    next_rd_date, *temp = db_connection.get_next_rd()
    no_of_race = db_connection.get_race_num(next_rd_date)
    result_pool = db_connection.get_pools(next_rd_date)
    result_odds = db_connection.get_odds(next_rd_date)
    time_list = [
        dt.datetime.combine(next_rd_date + dt.timedelta(days=-1), dt.datetime.strptime('21:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date + dt.timedelta(days=-1), dt.datetime.strptime('22:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date + dt.timedelta(days=-1), dt.datetime.strptime('23:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('00:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('01:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('02:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('03:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('04:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('05:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('06:00', '%H:%M').time()),
        dt.datetime.combine(next_rd_date, dt.datetime.strptime('07:00', '%H:%M').time())]
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('JAPJC_Export_' + str(next_rd_date.strftime('%Y%m%d')) + '_test.xlsx')
    for i in range(no_of_race):
        target_pool_win = []
        target_pool_pla = []
        target_odds_win = []
        target_odds_pla = []
        row_pool_win = 0
        col_pool_win = 0
        row_pool_pla = 0
        col_pool_pla = 12
        row_odds_win = 2
        col_odds_win = 0
        row_odds_pla = 2
        col_odds_pla = 12
        horse_num = db_connection.get_horse_num(next_rd_date, i + 1)
        worksheet = workbook.add_worksheet('R' + str(i + 1))
        # Filter data
        for item in time_list:
            worksheet.write(row_pool_win, col_pool_win,
                            min([sublist for sublist in result_pool if sublist[0] == i + 1],
                                key=lambda x: abs(x[1] - item))[2])
            col_pool_win += 1
            worksheet.write(row_pool_pla, col_pool_pla,
                            min([sublist for sublist in result_pool if sublist[0] == i + 1],
                                key=lambda x: abs(x[1] - item))[3])
            col_pool_pla += 1
            for j in range(horse_num):
                worksheet.write(row_odds_win, col_odds_win,
                                min([sublist for sublist in result_odds if
                                     (sublist[0] == i + 1) and (sublist[2] == j + 1)],
                                    key=lambda x: abs(x[1] - item))[3])
                row_odds_win += 1
                worksheet.write(row_odds_pla, col_odds_pla,
                                min([sublist for sublist in result_odds if
                                     (sublist[0] == i + 1) and (sublist[2] == j + 1)],
                                    key=lambda x: abs(x[1] - item))[4])
                row_odds_pla += 1
            row_odds_win = 2
            row_odds_pla = 2
            col_odds_win += 1
            col_odds_pla += 1
    workbook.close()

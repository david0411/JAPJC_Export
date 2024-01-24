import datetime
from Source.DBConnection_AWS import DBConnection_AWS
import xlsxwriter

if __name__ == '__main__':
    db_connection = DBConnection_AWS()
    next_rd_date, *temp = db_connection.get_next_rd()
    no_of_race = db_connection.get_race_num()
    result_pool = db_connection.get_pools(next_rd_date)
    result_odds = db_connection.get_odds(next_rd_date)
    time_list = [datetime.datetime.strptime('20:59', '%H:%M'),
                 datetime.datetime.strptime('21:59', '%H:%M'),
                 datetime.datetime.strptime('22:59', '%H:%M'),
                 datetime.datetime.strptime('23:59', '%H:%M'),
                 datetime.datetime.strptime('00:59', '%H:%M'),
                 datetime.datetime.strptime('01:59', '%H:%M'),
                 datetime.datetime.strptime('02:59', '%H:%M'),
                 datetime.datetime.strptime('03:59', '%H:%M'),
                 datetime.datetime.strptime('04:59', '%H:%M'),
                 datetime.datetime.strptime('05:59', '%H:%M'),
                 datetime.datetime.strptime('06:59', '%H:%M')
                 ]

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('JAPJC_Export_' + str(next_rd_date.strftime('%Y%m%d')) + '.xlsx')
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
        worksheet = workbook.add_worksheet('R' + str(i + 1))
        # Filter data
        for item in time_list:
            target_pool_win.append([sublist[2] for sublist in result_pool if (
                    sublist[1].time() == item.time()) and (sublist[0] == i + 1)])
            target_pool_pla.append([sublist[3] for sublist in result_pool if (
                    sublist[1].time() == item.time()) and (sublist[0] == i + 1)])
            target_odds_win.append([[sublist[2], sublist[3]] for sublist in result_odds if (
                    sublist[1].time() == item.time()) and (sublist[0] == i + 1)])
            target_odds_pla.append([[sublist[2], sublist[4]] for sublist in result_odds if (
                    sublist[1].time() == item.time()) and (sublist[0] == i + 1)])
        # Write Pool
        for val in target_pool_win:
            if len(val) != 0:
                worksheet.write(row_pool_win, col_pool_win, val[0])
                col_pool_win += 1
            else:
                col_pool_win += 1
        for val in target_pool_pla:
            if len(val) != 0:
                worksheet.write(row_pool_pla, col_pool_pla, val[0])
                col_pool_pla += 1
            else:
                col_pool_pla += 1
        for val in target_odds_win:
            if len(val) != 0:
                for val1 in val:
                    worksheet.write(row_odds_win + val1[0] - 1, col_odds_win, val1[1])
                col_odds_win += 1
            else:
                col_odds_win += 1
        for val in target_odds_pla:
            if len(val) != 0:
                for val1 in val:
                    worksheet.write(row_odds_pla + val1[0] - 1, col_odds_pla, val1[1])
                col_odds_pla += 1
            else:
                col_odds_pla += 1
    workbook.close()

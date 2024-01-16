import datetime
from DBConnection_AWS import DBConnection_AWS
import xlsxwriter

if __name__ == '__main__':
    db_connection = DBConnection_AWS()
    today = datetime.datetime.today()
    next_rd_date, *temp = db_connection.get_next_rd()
    no_of_race = db_connection.get_race_num()
    result_pool = db_connection.get_pools(next_rd_date)
    result_odds = db_connection.get_odds(next_rd_date)
    # print(result_pool)
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('JAPJC_Export_' + str(next_rd_date.strftime('%Y%m%d')) + '.xlsx')
    for i in range(no_of_race):
        worksheet = workbook.add_worksheet('R' + str(i + 1))

    # # Some data we want to write to the worksheet.
    # expenses = (
    #     ['Rent', 1000],
    #     ['Gas',   100],
    #     ['Food',  300],
    #     ['Gym',    50],
    # )
    #
    # # Start from the first cell. Rows and columns are zero indexed.
    # row = 2
    # col = 5
    #
    # # Iterate over the data and write it out row by row.
    # for item, cost in (expenses):
    #     worksheet.write(row, col,     item)
    #     worksheet.write(row, col + 1, cost)
    #     row += 1
    #
    # # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')
    #
    workbook.close()

import datetime
from DBConnection_AWS import DBConnection_AWS

if __name__ == '__main__':
    # Initialize
    action = None
    next_rd = None
    next_rd_date = None
    next_rd_venue = None
    next_rd_course = None
    # must include
    db_connection = DBConnection_AWS()
    today = datetime.datetime.today()
    next_rd = db_connection.get_next_rd()
    next_rd_date, *temp, next_rd_venue = next_rd
    next_rd_course = str(next_rd_venue).split(' ')[0]

import datetime


def datetime_handler(x):
    """ Allow serializing datetime objects to JSON """
    if isinstance(x, datetime.datetime) or isinstance(x, datetime.date):
        return x.isoformat()
    raise TypeError("Unknown type")


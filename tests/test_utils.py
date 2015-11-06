from dateutil.parser import parse as datetime_parser


def get_secs(t):
    '''
    Helper function for converting string time into seconds
    '''
    return datetime_parser(t).strftime("%s")

import logging
from django.utils import timezone

logging = logging.getLogger('skyCarManager')

def exception_log(exception, file, str_info=""):
    logging.error("---------------------- Exception at {date} {info}-----------------------".format(date=timezone.now(), info=str_info))
    logging.error("type:{error}".format(error=type(exception).__name__))
    logging.error("file:{file}".format(file=file))
    logging.error("line:{line}".format(line=exception.__traceback__.tb_lineno))
    logging.error("description:{exception}".format(exception=exception))
    logging.error("---------------------------------------------------------------------------------------")
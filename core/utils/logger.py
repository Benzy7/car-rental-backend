import logging
from django.utils import timezone

logger  = logging.getLogger('skyCarManager')

def exception_log(exception, file, str_info=""):
    logger .error("---------------------- Exception at {date} {info}-----------------------".format(date=timezone.now(), info=str_info))
    logger .error("type:{error}".format(error=type(exception).__name__))
    logger .error("file:{file}".format(file=file))
    logger .error("line:{line}".format(line=exception.__traceback__.tb_lineno))
    logger .error("description:{exception}".format(exception=exception))
    logger .error("---------------------------------------------------------------------------------------")
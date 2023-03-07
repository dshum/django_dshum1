import logging

from django.conf import settings


class RequireDebugSqlTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG_SQL

# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand

# These are the statements that matter -- we use these to get the test to run.

from mongo_db.tests import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        return


from django.core.management.base import BaseCommand
from lottery.models import Lottery
from datetime import datetime, timedelta

tfl = '%Y-%m-%d %H:%M:%S'
tfs = '%Y/%m/%d'

class Command(BaseCommand):
    help = "generate lottery SN"

    def handle(self, *args, **options):
        now = datetime.now()
        self.stdout.write(u'current time: ' + now.strftime(tfl))
        Lottery.objects.all().delete()
        for i in range(1,13):
            num = ('{:08}'.format(i))
            lottery = Lottery(sn=num)
            lottery.save()


        now2 = datetime.now()
        self.stdout.write(u'end time: ' + now2.strftime(tfl))
        val = now2 - now
        self.stdout.write(u'waste time: %s' % val)

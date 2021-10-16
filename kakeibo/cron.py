from django_cron import CronJobBase, Schedule
from .models import Category, Kakeibo

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 minitues

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'kakeibo.MyCron'    # a unique code

    def do(self):
        print("Hello Medium!") 
        print("hwssssssss")

    def do(self):
        print("hwssssssss")

class Time(CronJobBase):
    RUN_EVERY_MINS = 2

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'kakeibo.MyCron'

    def auto(request, params):

        kakeibo_data = Kakeibo.objects.all()

        print("cron")
        post_pks = request.POST.getlist('cron')
        Kakeibo.objects.filter(pk__in=post_pks).add()
        
        params = {
            'kakeibo_data':kakeibo_data,
        }

        return (request, params)


    
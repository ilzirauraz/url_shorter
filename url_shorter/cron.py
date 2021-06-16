from django_cron import CronJobBase, Schedule
from .models import ShortenedLink
from datetime import datetime, timedelta
import redis
from django.conf import settings


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, 
                                   db=0)

class CleanShortenedLinksCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'url_shorter.clean_shortened_links_cron_job'

    def do(self):
        shortened_links = ShortenedLink.objects.filter(created_at__lt=datetime.now()-timedelta(minutes=5))
        for shortened_link in shortened_links:
            if redis_instance.exists(shortened_link.subpart):
                print('delete: ', subpart)
                redis_instance.delete(subpart)

        shortened_links.delete()


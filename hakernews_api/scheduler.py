from apscheduler.schedulers.background import BackgroundScheduler

from hakernews_api.views.story_views import ReadStoryViewset


def start(*args):
    scheduler = BackgroundScheduler()
    story = ReadStoryViewset()
    scheduler.add_job(
        story.save_item_data,
        "interval",
        minutes=1,
        replace_existing=True
    )
    scheduler.start()

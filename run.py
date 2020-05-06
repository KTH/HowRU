import logging
import asyncio
from threading import Thread
import slack_util
import schedule
import log as log_module

log_module.init_logging()
log = logging.getLogger(__name__)

#schedule.every().day.at("09:00").do(slack_util.post_todays_question)
#schedule.every().day.at("15:00").do(slack_util.post_question_summary)

def main():
    try:
        #loop = asyncio.new_event_loop()
        #thread = Thread(target=slack_util.init, args=(loop,))
        #thread.start()
        slack_util.init()
        log.info("Everest Bot connected and running!")
        slack_util.post_todays_question()
    except Exception as err:
        log.error (f'Oh :poop:, I died and had to restart myself. {err}')
        raise


if __name__ == "__main__":
    main()
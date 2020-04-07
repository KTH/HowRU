import logging
import time
import slack
import schedule
import log as log_module
import util

log_module.init_logging()
log = logging.getLogger(__name__)

schedule.every().day.at("09:00").do(slack.post_todays_question())
schedule.every().day.at("15:00").do(slack.post_question_summary())

def main():
    try:
        if slack.init():
            log.info("Everest Bot connected and running!")

            while True:
                schedule.run_pending()
                log.debug('Check for new messages sent to the bot.')
                rtm_messages = []
                try:
                    rtm_messages = slack.get_rtm_messages(slack.rtm_read())
                except Exception:
                    log.warn('Timeout when reading from Slack')
                if len(rtm_messages) > 0:
                    log.debug('Got %s messages since last update',
                              len(rtm_messages))
                for message in rtm_messages:
                    log.debug('Handling message "%s"', message)
                    slack.handle_im_created(message)
                    slack.handle_im(message)
                time.sleep(slack.rtm_read_delay)
        else:
            log.error("Connection to Slack failed!")
    except Exception as err:
        log.error (f'Oh :poop:, I died and had to restart myself. {err}')
        raise


if __name__ == "__main__":
    main()
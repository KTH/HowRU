import logging
import time
import slack
import log as log_module

log_module.init_logging()
log = logging.getLogger(__name__)

# On time, write todays question to #section-sfu
# register DMs sent to the bot and save in memory
# On time, write summary to #section-sfu

def main():
    try:
        if slack.init():
            log.info("Everest Bot connected and running!")

            while True:
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
                    command, user, channel = slack.message_is_direct_mention(
                        message)
                    if command:
                        handle_command(command, channel, user)
                    url, channel = slack.message_is_utr_down(message)
                time.sleep(slack.rtm_read_delay)
        else:
            log.error("Connection to Slack failed!")
    except Exception as err:
        log.error (f'Oh :poop:, I died and had to restart myself. {err}')
        raise


if __name__ == "__main__":
    main()
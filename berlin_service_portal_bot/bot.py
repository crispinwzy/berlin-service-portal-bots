import helpers

from telegram_bot import TelegramBot
from web_driver import WebDriver
from config import Config


class Bot:
  def __init__(self, name):
    config = Config()

    # Setup web driver
    headless = config.get_boolean(
        "default",
        "headless",
        "Should I start the browser in headless mode?"
    )

    timeout = config.get_int(
        "default",
        "timeout",
        "What's the maximum time in seconds that I should wait for a response?"
    )

    incognito = config.get_boolean(
        "default",
        "incognito",
        "Should I start the browser in incognito mode?"
    )

    detach = config.get_boolean(
        "default",
        "detach",
        "Should I close the browser when the script exits?"
    )

    self.refresh_interval = config.get_int(
        "default",
        "refresh_interval",
        "How many seconds should I wait to refresh a page, when looking for appointments?"
    )

    # Setup Telegram bot
    telegram_bot_token = config.get(
        "telegram_bot",
        "token",
        "What's your Telegram bot token?"
    )

    telegram_bot_chat = config.get(
        "telegram_bot",
        "chat",
        "What's your Telegram chat ID from where I should send notification messages?"
    )

    self.name = name
    self.config = config
    self.web_driver = WebDriver(headless, timeout, incognito, detach)
    self.telegram_bot = TelegramBot(telegram_bot_token, telegram_bot_chat)

  def _notify(self, text):
    print(text)
    helpers.os_notify(self.name, text)
    self.telegram_bot.send_text(text)
    self.web_driver.save_page_source()
    self.telegram_bot.send_photo(self.web_driver.save_page_screenshot())


def loop(load):
  def __safe_load():
    try:
      load()
      return 1
    except Exception as e:
      print(e)
      return 0

  while 1:
    if __safe_load():
      break
    continue

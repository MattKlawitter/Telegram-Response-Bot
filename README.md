# Important Notice:
Development on this bot/framework has largely been abandoned (though it may still be helpful for throwing together a quick bot and there are quite a few plugins that can still be downloaded for it). Development has instead moved to a Java varient featuring an implementation of the entire Telegram API along with built in plugins. You can find this new project at the following repo: [https://github.com/Matthew-Klawitter/Telegram-Response-Bot-Java](https://github.com/Matthew-Klawitter/Telegram-Response-Bot-Java)

# Telegram-Plugin-Bot
A [telegram](https://telegram.org/) bot that supports plugins. This allows for
creating bots with all sorts of functions without having to deal with much boiler
plate code.

This fork features a few more updated features including an built in plugin management and an attempt at faster plugin based responses through multithreading. The plugin api is also slightly updated with an enforced interface. For a collection of useful and unuseful plugins that can manually be installed check out the following repo: [https://github.com/Matthew-Klawitter/Telegram-Response-Bot-KPlugins](https://github.com/Matthew-Klawitter/Telegram-Response-Bot-KPlugins)

### Setup ###
Requirements
- [Python 3](https://www.python.org/)
  - [Requests](http://docs.python-requests.org/en/master/) module
- Telegram Bot Token
  - Make sure to change the privacy settings to see all messages

Run *start.py* using Python 3. The first time it is a ran, you will be prompted to enter your bot's token, directory for the bot, sleep interval, and a list of plugins to load. This will be saved in `config.txt`.

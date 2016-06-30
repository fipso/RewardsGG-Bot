# RewardsGG-Bot
Tickets farming bot for Rewards.GG written in Python

This tool needs python 3 to run

##Usage:
 * Clone this repo
 * Install requirements:
   * `pip install pycurl`
 * Create an 'accounts.secure' file
 * Add RewardsGG accounts to this file
   * Use `|` as seperator
   * Example: `user100|pasword123`
 * Run `python RewardsGG.py`
 * Farming process will run in background
 * Enter `fix`
 * Done - That`s it

##Avaible Commands:
While farming process is running you can use the following commands

 * `tickets` shows current ticket amount of every account
 * `fix` solves problems for new accounts
 * `spent <itemURL> <amount> <account>`
   * Example: `spent https://rewards.gg/giveaway/half-life-3 200 user100`
 * `debug` switches debug mode on/off
 * `exit` and `quit` does someting

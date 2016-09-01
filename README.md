# NAOMI Game Selector

This allows you to boot your NAOMI using a nice web interface. I made this because I wanted to be able to load NAOMI games from anywhere in my house on any device (including my phone or tablet), so a network app made the most sense to me. Then I figured, why not give it a nice little UI? And here we are.

The backend is written in Django (Python) and the frontend is done in AngularJS.

# Requirements
* Ubuntu Server or Desktop 12.04 LTS or later (tested on 16.04 LTS)
* Basic Linux sysadmin skills.
* Python 2.7 (though this should be in naomienv)
* redis-server (sudo apt-get install redis-server)
* A gunicorn service daemon and a celery service daemon. TODO: Provide sample configs.

You could probably get it working on Windows too with a little more work and cygwin, mingwin, or the wonderful Bash on Ubuntu on Windows in Windows 10.

# Installation
TODO

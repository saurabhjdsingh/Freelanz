<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Credit System" />

  &#xa0;

  <!-- <a href="https://creditsystem.netlify.app">Demo</a> -->
</div>

<h1 align="center">Freelancing Platform : Freelanz (Thinkgroupy)</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/badge/language-Python-red">
  <img alt="Repository size" src="https://img.shields.io/badge/Repository_size->500KB-red">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-red">
  <a href="https://linkedin.com/in/saurabhjdsingh"><img alt="Author" src="https://img.shields.io/badge/Author-Saurabhjdsingh-blue"></a>
</p>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/saurabhjdsingh" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Freelanz is a full-stack freelancing platform that lets users signup, sign in, and bid on various projects as a freelancer, 
also helps freelancers connect to their clients via 1-1 Audio or Video calls through Websockets.

## :sparkles: Features ##

:heavy_check_mark: Signup & Signin;\
:heavy_check_mark: Create projects as clients and post them for bidding;\
:heavy_check_mark: Let freelancers bid on live projects;\
:heavy_check_mark: Clients can chat via web socket connection through 1-1 Audio or Video call;\
:heavy_check_mark: Razorpay payment gateway added for smooth transactions;\

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/start/overview/)
- [Django channels](https://channels.readthedocs.io/en/latest/)
- [Websockets](https://websockets.readthedocs.io/en/stable/howto/django.html)
- [Razorpay](https://razorpay.com)
- [Postgres](https://www.postgresql.org/docs/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com), [Python](https://www.python.org/) and [Redis](https://redis.io/) installed.

## :checkered_flag: Starting ##

```bash
+ FOR MAC (These commands can be different for non-Linux computers):


# Install Redis (background worker service, used with celery):
brew update
brew install redis

# Set up a virtual env. into parent folder

1. `python3 -m venv env`
2. `source env/bin/active`

# Clone this project (Kindly clone this repository into the parent folder)
$ git clone https://github.com/saurabhjdsingh/Freelanz

# Go to the project
$ cd Freelanz

# install dependencies
$ pip install -r requirements.txt

# runserver (In first terminal window)
$ python manage.py runserver

# Start Redis Server (In the second terminal):
$ redis-server


# The server will initialize in the <http://127.0.0.1:8000/>
```




## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.

Made with :heart: by <a href="https://linkedin.com/in/saurabhjdsingh" target="_blank">Saurabh</a>

&#xa0;

<a href="#top">Back to top</a>

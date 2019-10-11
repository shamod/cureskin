# Cure Skin

![License](http://img.shields.io/:license-mit-blue.svg)

## Overview

Cure Skin is a Python Flask app using a Tensorflow DNN model trained to classify skin conditions from a picture and give
a diagnosis with suggested information the user can use to learn more.


## Walk Through

The user first lands on the home page and signs up for a new account, where they can buy credits to use for diagnosises of 
skin conditions:

![Home Page](./screenshots/home.png) 

![Signup Page](./screenshots/sign_up.png)

A pack of 10 credits for $10 is purchased using Stripe, and 1 credit is deducted per diagnosis:

![Signup Page](./screenshots/buy_credits.png)

The user can view a list of their purchases on their user account page:

![Signup Page](./screenshots/user_account.png)

Once credits have been added to the account, the user can click on the 'Diagnosis' tab to
begin uploading images and receiving diagnosises from the AI model:

## Setup

### Vanilla

- Install the requirements and setup the development environment.

	`make install && make dev`

- Create the database.

	`python manage.py initdb`

- Run the application.

	`python manage.py runserver`

- Navigate to `localhost:5000`.

## Configuration

The goal is to keep most of the application's configuration in a single file called `config.py`. I added a `config_dev.py` and a `config_prod.py` who inherit from `config_common.py`. The trick is to symlink either of these to `config.py`. This is done in by running `make dev` or `make prod`.

I have included a working Gmail account to confirm user email addresses and reset user passwords, although in production you should't include the file if you push to GitHub because people can see it. The same goes for API keys, you should keep them secret. You can read more about secret configuration files [here](https://exploreflask.com/configuration.html).

Read [this](http://flask.pocoo.org/docs/0.10/config/) for information on the possible configuration options.

## Contributors

This project was completed by:

* [David Gildeh](https://github.com/dgildeh)
* [Shamod Lacoul](https://github.com/shamod)
* [Craig Burnett](https://github.com/haggishm)

## Thanks

This Flask app is originally a fork of [Max Halford's](https://github.com/MaxHalford) 
[flask-boilerplate](https://github.com/MaxHalford/flask-boilerplate). 

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.

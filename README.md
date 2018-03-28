# TragicReviews
WAD2 project

## Environment Requiments
Python 3.6 or later is __required__ for the web application to run. Earlier 3.x versions will not work and will result in syntax errors. The version of Python used in the labs satisfies this requirement.

## Additional Packages 
* [django-registration-redux v2.2](https://django-registration-redux.readthedocs.io/en/latest/index.html)

  Installation: `pip install django-registration-redux`

* [bcrypt v3.1.4](https://pypi.python.org/pypi/bcrypt/3.1.4)

  Installation: `pip install bcrypt`

* [django-bootstrap3 v9.1.0](https://pypi.python.org/pypi/django-bootstrap3/9.1.0)

  Installation: `pip install django-bootstrap4`

* [django-haystack 2.8.0](http://haystacksearch.org)

  Installation: `pip install django-haystack`

* [Whoosh 2.7.4](https://pypi.python.org/pypi/Whoosh/2.7.4)

  Installation: `pip install Whoosh`

* [freezegun v0.3.10](https://github.com/spulec/freezegun)

  Installation: `pip install freezegun`

* [coverage v4.5.1](https://coverage.readthedocs.io/en/coverage-4.5.1/)

  Installation: `pip install coverage`

## External APIs

* [Tweet Button](https://dev.twitter.com/web/tweet-button)

* [Facebook Share Button](https://developers.facebook.com/docs/plugins/share-button)

* [Google+ Share Button](https://developers.google.com/+/web/share/)

## Running the Populate Script
The population script can be run in two modes: “core” or “examples”. The “core” mode sets up the staff and student groups which are required by the web application. It also adds the default list of categories. This is what is used for deployment to PythonAnywhere. The “examples” mode does everything that “core” does but it _additionally_ adds 10 fake users (5 student, 5 staff) and a random number of articles (1-3) in each category, each with a random number (0-5) of ratings and comments. This is useful for a quick-start demo. __Specifying which mode to use is required.__

Example usage: `python populate_tragicreviews.py examples`

## Search Functionality
Auto-updates its index but requires an initial `./manage.py rebuild_index` to create the index.

Initiallise index: `python manage.py rebuild_index`

## Testing
### Running Unit Tests:
`python manage.py test tragicreviews.unit_test.your_test`

Example:
`python manage.py test tragicreviews.unit_test.test_models`


### Code Coverage Testing:
Running tests: `coverage run --source='.' manage.py test tragicreviews`

Viewing report: `coverage report`


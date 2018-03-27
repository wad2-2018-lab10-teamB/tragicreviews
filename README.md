# TragicReviews
WAD2 project

## Additional Packages: 
[django-registration-redux v2.2](https://django-registration-redux.readthedocs.io/en/latest/index.html)

Installation: `pip install django-registration-redux`

[bcrypt v3.1.4](https://pypi.python.org/pypi/bcrypt/3.1.4)

Installation: `pip install bcrypt`

[django-bootstrap3 v9.1.0](https://pypi.python.org/pypi/django-bootstrap3/9.1.0)

Installation: `pip install django-bootstrap4`

[freezegun v0.3.10](https://github.com/spulec/freezegun)

Installation: `pip install freezegun`

[django-haystack 2.8.0](http://haystacksearch.org)

Installation: `pip install django-haystack`

[Whoosh 2.7.4](https://pypi.python.org/pypi/Whoosh/2.7.4)

Installation: `pip install Whoosh`

[coverage v4.5.1](https://coverage.readthedocs.io/en/coverage-4.5.1/)

Installation: `pip install coverage`

## Testing
### Running Unit Tests:
`python manage.py test tragicreviews.unit_test.your_test`

example:
`python manage.py test tragicreviews.unit_test.test_models`


### Code Coverage Testing:
Running tests: `coverage run --source='.' manage.py test tragicreviews`

Viewing report: `coverage report`

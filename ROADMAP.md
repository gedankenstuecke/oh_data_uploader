# ROADMAP
What things do we want to work on next? And what did we already achieve?

## Short term plans
- get feedback on whether the project template is useful so far. Reach out to interested individuals

## Mid term plans
- style project admin backend better, e.g. given an example of how how does markdown work?
- display existing files and allow user to delete individual files from their accounts
- allow multiple upload fields with different meta data that'll be associated
- write full set of tests, so far most things have to be tested manually 😱

## Long term plans
- add a simple `celery` integration that allows people to write their own validations for uploaded files

## Already done 🎉
- make sure that `APP_BASE_URL` will be stripped of trailing `/`s
- read project descriptions etc. from `markdown` files somewhere and render accordingly
- deploy to heroku works thanks to @madprime!
- styled all forms enough to be usable.
- travis CI is set up!

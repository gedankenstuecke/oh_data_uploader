# Local Deployment and Development

This tool is designed to be deployed to *heroku* ([see README.md](https://github.com/gedankenstuecke/oh_data_uploader/blob/master/README.md)). To install it
locally to develop it further (or to deploy to non-heroku hosts) see the guidelines here:

### *Step 1: Install pipenv and needed packages*

This project now [uses the recommended `pipenv` workflow for installing dependencies](http://pipenv.readthedocs.io/en/latest/).

If you already have a `Python` installation on your end do the following to get started with all required Python packages do the following from the main `oh_data_uploader` folder: 

```
pip install pipenv
pipenv install --three
pipenv shell
```

You should now be in a shell that is specifically set up with all the required Python packages. You can exit this shell any time by just writing `exit`. If new packages have been added to this repository any time, you can upgrade all the packages for it by typing `pipenv install` again and it will use the existing `Pipfile` and `Pipfile.lock` to install the appropriate modules. 

### *Step 2: Install Heroku Command Line Interface (CLI)*

You should install the Heroku CLI to run this app locally.
Heroku has [installation instructions for MacOS, Windows, and Linux](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

If you are running MacOS the easiest way to do this is using [Homebrew](https://brew.sh/). After installing Homebrew you have two options:

Simply run:
`brew install heroku/brew/heroku`

Or

```
brew tap heroku/brew
brew install heroku
```

The second option shown above adds the Heroku repository to your Homebrew configuration allowing you to access all of the Heroku library rather than the single `heroku` application.

### *Step 3: Set-up the local `.env` file*
Once this is done you can complete minimal setup by:
* Create an `.env` file from the example: `cp .env.sample .env`
* Edit `.env` to set a random string for `SECRET_KEY` and `ADMIN_PASSWORD`
* Make sure to activate your `Python` environment with `pipenv shell`
* Migrate your database using `heroku local:run python manage.py migrate`
* Initialize config with `heroku local:run python manage.py init_proj_config`

Now you can run the webserver of your local heroku environment using `heroku local`.

This should give you a development server up and running on `http://0.0.0.0:5000`.
On `http://0.0.0.0:5000/project-admin/` you should fine the project admin interface,
you can login to it using the `ADMIN_PASSWORD` you set above.


## FAQ

**When I run `heroku local` or use the app it crashes/complains about missing packages.**

It seems that either new packages are required to run the latest version of `oh_data_uploader` or that you're not in the `pipenv shell`. To check for both things run:

```
pipenv install
pipenv shell
heroku local
```
The app should start now.

**I get an error about the project config not found!**

You probably forgot the initialization step. Inside your `pipenv shell` run `heroku local:run python manage.py init_proj_config`

**I get an error about tables/columns not found!**

You probably didn't migrate your database. Run `heroku local:run python manage.py migrate` to add the missing database tables/columns.

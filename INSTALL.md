# Local Deployment and Development

This tool is designed to be deployed to *heroku* ([see README.md](https://github.com/gedankenstuecke/oh_data_uploader/blob/master/README.md)). To install it
locally to develop it further (or to deploy to non-heroku hosts) see the guidelines here:

### *Step 1: Install Anaconda and needed packages*

[Download & Install the appropriate version of *Anaconda* on your end](https://www.anaconda.com/download/#macos),
this makes it easy to keep Python versions and modules clean. If you are already familiar with [*virtualenv*](https://virtualenv.pypa.io/en/stable/) you can use their workflow instead of *Anaconda*.

After you have installed *Anaconda*, create a fresh environment for the *Open Humans uploader* and activate it:

```
conda create -n oh_uploader python=3.6
source activate oh_uploader
```

Now you can install the packages needed to locally run the `oh_data_uploader` by navigating into the
directory of the `oh_data_uploader` and running pip:

```
cd oh_data_uploader/
```
Install `pipenv` using `pip install pipenv`

Install all packages using `pipenv install`

To activate this project's `virtualenv` use `pipenv shell`

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

This second options adds the Heroku repository to your Homebrew configuration allowing you to access all of the Heroku library rather than the single `heroku` application.

### *Step 3: Set-up the local `.env` file*
Once this is done you can complete minimal setup by:
* Create an `.env` file from the example: `cp .env.sample .env`)
* Edit `.env` to set a random string for `SECRET_KEY` and `ADMIN_PASSWORD`
* Migrate your database using `heroku local:run python manage.py migrate`
* Initialize config with `heroku local:run python manage.py init_proj_config`

Now you can run the webserver of your local heroku environment using `heroku local`.

This should give you a development server up and running on `http://0.0.0.0:5000`.
On `http://0.0.0.0:5000/project-admin/` you should fine the project admin interface,
you can log into it using the `ADMIN_PASSWORD` you set above.

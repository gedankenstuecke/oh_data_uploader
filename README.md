# Open Humans Uploader
> *it's like Jekyll for Open Humans*
or something along the lines.

Ultimately this should be an easy to deploy Django project that functions as a
file uploader for individual *Open Humans* projects. It should be easy deploy to
*heroku* and the configuration/styling of the project website should be done more
or less exclusively through a `yaml` configuration file and `markdown` files that
are rendered to HTML.

## Installation
The *Open Humans Uploader* is written in *Python* with *Django* and is designed to be ultimately deployed
to *Heroku*. To install a copy of it on MacOS you will need to install some additional modules. Here's the Step-by-Step guide.

 *Step 1: Install Anaconda*

[Download & Install the appropriate version of *Anaconda* on your end](https://www.anaconda.com/download/#macos),
this makes it easy to keep Python versions and modules clean.

After you have installed *Anaconda*, create a fresh environment for the *Open Humans uploader* and install the needed Python packages:

```
conda create -n oh_uploader python=3.6
pip install -r requirements.txt
```

*Step 2: Install heroku-CLI & PostgreSQL*

If you are running MacOS the easiest way to do this is using [Homebrew](https://brew.sh/). After installing Homebrew
you can do:

```
brew install postgres
brew install heroku/brew/heroku
```

Once this is done you can start the setup of your *Open Humans uploader* by copying the example `.env` file (`cp .env.sample .env`) and starting the local heroku environment using `heroku local`.

To fully set up your uploader you will have to modify some files, as described below: 

## Configuration

### Setting up a project on *Open Humans*
To connect this data uploader to your own *Open Humans* project you should start out by
[creating a new project on Open Humans](https://www.openhumans.org/direct-sharing/projects/manage/).
Select the *Create a new OAuth2 data request project* button and fill out the form.

For this uploader to work you have to give the correct redirect URL in the form (it's the last field).
Our uploader expects redirects to `youraddress.com/complete`. If you run this tool on your development
machine it will probably be `http://127.0.0.1:5000/complete`. If you deploy it to *heroku* it will be
`https://yourappname.herokuapp.com/complete`.

### Configure the *Open Humans Uploader*

This configuration is done by two means:
1. The `config.yaml` file contains information that will be displayed on your website later on. As such it is not sensitive and can be publicly available.
2. For sensitive information there is the `.env` file that contains your **secret** information that you need to connect to your database and *Open Humans*. This file should not be available online! An example file can be found in `.env.sample`.

#### The `config.yaml`

This file contain a number of details. First of all are the metadata that will decide on the style of the main page, how your project will be called throughout the application etc.

```
# REQUIRED: What's the name of your project?
project_title: My Open Humans Project
# REQUIRED: Will be displayed on the front page of the uploader
project_description: This template demonstrates how you can run your own Open Humans data upload project.
# REQUIRED: Where can we find your project on Open Humans
oh_activity_page: https://www.openhumans.org/activity/your-project-url/
```

The `app_base_url` tells the *Open Humans Uploader* where it will be located. It's
important to get this right. Amongst other things this will also decide on what the `REDIRECT URL` is.
For your local development you can keep `http://127.0.0.1:5000`. If you deploy to *heroku* you might
want to change this.

```
# REQUIRED: which URL will lead to your Open Humans uploader
app_base_url: http://127.0.0.1:5000
```

Files that are uploaded to *Open Humans* require metadata that describe the files
along with some tags. These two parameters set the metadata for your uploads:

```
# REQUIRED: Tell Open Humans what kind of data is being uploaded
file_description: This is an example file that doesnt have any meaning.
# REQUIRED: Tags to add to your file uploads
file_tags:
- tags
- 'are a good way to'
- 'describe the files you are uploading'
```

Optionally you can also specify your own logo for your project. It will be displayed
prominently on the front page.

```
# Give the path to the logo of your project.
logo: ' static/example_logo.png'

# Is there a larger project website where more info might be located?
more_info_link: http://www.github.com/gedankenstuecke/oh_data_uploader
```

#### The `.env` file
In addition to the public parameters you will need to set the parameters that control the API
connection to *Open Humans* and your database. For your development environment these parameters
can be set in the `.env` file (an example is provided in `.env.sample`):

```
DATABASE_URL=postgres:///myurl
SECRET_KEY=mysecretshouldnotbeongit
OH_CLIENT_ID=myclientidshouldnotbeongit
OH_CLIENT_SECRET=myclientsecretshouldnotbeongit
```

The `DATABASE_URL` tells your uploader to which database it should connect, while the `SECRET_KEY` is used
to keep your uploader itself safe. The `OH_CLIENT_ID` and `OH_CLIENT_SECRET` are used for the communication with
*Open Humans*. You can find both on your project site, by [clicking on the name of your project here](https://www.openhumans.org/direct-sharing/projects/manage/).

If you deploy your application to *heroku* you will not use the `.env` for the parameters, rather you will use the [config variables as described by Heroku](https://devcenter.heroku.com/articles/config-vars).

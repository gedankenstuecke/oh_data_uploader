# What does my project do?
This tool allows you to easily setup your own *Open Humans* project that wants
to collect data. You just need to set up some configuration files before you
can deploy it *heroku*.

The configuration files are:

- `config.yaml` in the main directory of this git repository. This contains details
on your project that aren't secret like the title, description, where the logo can be found etc.
- The `.env` contains the secret details that shouldn't be shared. E.g. your database setup,
your *Open Humans* API keys etc.
- The texts that should be displayed on this project website. In `_descriptions` you can find the
markdown files needed to customize this template. E.g. this page is written in `_descriptions/index.md`.

Use this page to inform your users about what your project is about and what it tries to do. It's the first
page they will see, so be verbose!

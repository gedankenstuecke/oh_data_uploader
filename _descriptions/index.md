# What does my project do?
This tool allows you to easily setup your own *Open Humans* project that wants
to collect data.

The configuration for this project is in:

- **Environment variables:** If you deploy to Heroku, you'll probably be
prompted to provide these, and they can be modified in the the app. Locally,
your `.env` file defines these. These are secret details that should not be
shared. (Be sure not to add this to your git repository!)
- **Project configuration:** The [Project Admin page](/project-admin) can be
used to configure other aspects of your site. Log in with the `ADMIN_PASSWORD`
you set in environment variables.

As you configure the project, replace this "front page" text to inform
users what your project is about and what it tries to do. It's the first page
they will see, so be verbose!

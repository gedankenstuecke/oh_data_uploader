# Open Humans Uploader

Ultimately this should be an easy to deploy project data uploader template that
allows users to style the template through markdown files and just uses a simple
`yaml` file to pass the basic configuration.

*it's like Jekyll for Open Humans* or something along the lines.


## Configuration

There are two places where you have to make adjustments for your own deployment:

1. The `config.yaml` contains information that will be displayed on your website later on
2. There is the `.env` file that contains your **secret** information that you need to connect to your database and Open Humans. This file should not be available online! An example file can be found in `.env.sample`.

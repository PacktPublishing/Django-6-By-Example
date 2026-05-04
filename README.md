# Django-6-By-Example

This is the code repository for Django 6 by Example, written by [Antonio Melé](https://antoniomele.es/) and published by [Packt](). It contains all the supporting project files necessary to work through the book from start to finish.


## Instructions
The code is organised into directories with the chapter number. For example, `Chapter02` contains the source code for chapter 2. 

After cloning the project, you can go to the first chapter with the following command:
```sh
cd Chapter01
```
Next, you can create and activate a virtual environment, install packages using python venv module and pip or uv.

With python venv module with pip:
```sh
python3.12 -m venv my_env
```

with uv:
```sh
uv venv my_env
```
You can get more information about uv in the first chapter of the book. Next, you can activate your environment with the following command:
```sh
source my_env/bin/activate
```
Each chapter folder has a requirements.txt file and a uv.lock file that includes all packages required to run the code of that chapter. These can be installed with the command: `pip install -r requirements.txt` or `uv sync` if you use uv.

Finally, you can install the packages and go to the project folder with the commands below:

with python venv module with pip:
```sh
pip install -r requirements.txt
cd mysite
```

with uv:
```sh
uv sync
cd mysite
```

Run the Django development server with the command:

```sh
python manage.py runserver
```

Fixtures has been created in order to ease the data creation for some chapters. To use them, you need to make sure you have applied the migrations and created a super user with the "admin" username. You can add them with the `loaddata` command with the path of the filename of the fixture. For example, to load data for the chapter 1:
```sh
python manage.py loaddata fixtures/chapter_1.json
```

Docker Compose is explained in Chapter 17. However all chapters include a Docker Compose configuration and a management script (contribution by [@marksweb](https://github.com/marksweb)).

Make sure you run these commands from the chapter directory (e.g. Chapter01) where the do.sh script is located.

Commands to build and run using Docker Compose:
```sh
./do.sh build
./do.sh start
```

List of commands:
- `build [<arg>]`: Builds Docker images. Optional arguments can specify specific images to build.
- `exec [<arg>]`: Execute a command in a container.
- `compose`: Minimal wrapper around Docker Compose, ensuring correct configuration files are loaded.
- `migrate [<arg>]`: Apply any unapplied Django migrations.
- `makemigrations [<arg>]`: Create a new Django migration, specifying additional arguments if needed.
- `check`: Validate Django settings.
- `shell`: Open a bash terminal in the specified container (web_run).
- `start [<arg>]`: Start the Django server and dependent services. Use -d to run detached.
- `stop [<arg>]`: Stop the Django server and dependent services.

## About the Book
Django 6 by Example (6th edition) will guide you through the entire process of developing professional web applications with Django. The book not only covers the most relevant aspects of the framework, but it will also teach you how to integrate other popular technologies into your Django projects.

The book will walk you through the creation of four real-world applications, solving common problems, and implementing best practices, using a step-by-step approach that is easy to follow.

After reading this book, you will have a good understanding of how Django works and how to build practical, advanced web applications.

## Requirements
This book requires Python 3.12+ and Django 6.

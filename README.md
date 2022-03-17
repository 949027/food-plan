# "Where To Go" site project

This is an interactive map of Moscow, where you can view outdoor activities with detailed descriptions and comments.

## Requirements

Python3 should be installed. Use command line utility `cmd.exe` to run Python3 scripts.

## Prerequisites

Use `pip` to install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Installation

Migrate the database
```bash
python manage.py migrate
```

Create superuser
```bash
python manage.py createsuperuser
```

## Launch the site

```bash
python manage.py runserver
```

Launch the [django admin site](http://127.0.0.1:8000/admin).

Launch the ["Where To Go" project stite](http://127.0.0.1:8000).

To load test receipts from [Povarenok site](https://www.povarenok.ru/) run script:
```bash
python manage.py parsing_recipes_website
```

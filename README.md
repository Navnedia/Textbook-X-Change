### Building and running the application

First configure a `.env` file based on the example shown in [.env.example](/.env.example)

When you're ready, start the application by running:
`docker compose up --build`

or in development you can use the watch attribute to automatically watch for and sync file
changes into they running docker container to make testing changes easier:

`docker compose up --build --watch`.


The application will be available at http://127.0.0.1:8000.

If you have any issue you can try to run the DB migrations:
`docker compose run django-web python manage.py migrate`

You will also need to run the management command to load in the schools dataset:

`docker compose run django-web python manage.py loadschools ./us-colleges-and-universities.csv`

If you need to delete all users from the db do the following in order

`docker-compose down`
`docker-compose up -d`
`docker exec -it poc-demo-team-two-django-web-1 /bin/bash`
`python manage.py shell`
`from django.contrib.auth.models import User`
`User.objects.all().delete()`
`docker logs poc-demo-team-two-db-1`

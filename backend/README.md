# Cleon Server

## Local Development

1. Open VS Code
2. Open backend project as DevContainer: `Backend Container`
3. Wait until VS Code is ready – this can take a while
4. Add a `.env` file (keys see email)
5. Check active python environment in the terminal via `which python` (may be necessary to run `source .venv/bin/activate`)
6. Init database:
    1. Run `./manage.py makemigrations`
    2. Run `./manage.py migrate`
    3. Run `./manage.py createsuperuser`: `{username: cleon, password: thp.F26zeJ}`
    4. Run `./manage.py runscript seed_database`
7. Start development server via `./manage.py runserver` and open `http://127.0.0.1:8000/api/v1/docs`
8. Run tests via `./manage.py test .` ( `./manage.py test <appname>.tests` )

pip install -r requirements.txt

# Init database migrations
alembic init -t async migrations
alembic revision --autogenerate -m "init"
alembic upgrade head

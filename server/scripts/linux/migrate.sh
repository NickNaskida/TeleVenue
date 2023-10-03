read -p 'Commit message: ' message
alembic revision --autogenerate -m "$message"
alembic upgrade head
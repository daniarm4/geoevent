from decouple import config

DATABASE_URL = config("DATABASE_URL")
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
TEST_DATABASE_URL = config("TEST_DATABASE_URL")

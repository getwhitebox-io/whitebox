from src.schemas.model import ModelType

register_payload = dict(
    email="mark@knight.com",
    password="pass",
)
login_payload = dict(username="mark@knight.com", password="pass")
client_update_payload = dict(password="pass1", email="mark@knight1.com")

user_create_payload = dict(name="User", email="user@yahoo.com", password="1234567890")
users_in_db = dict(amount=1)
user_update_payload = dict(
    name="Userius", email="user@yahoo.com", password="1234567890"
)

project_create_payload = dict(name="Project 1")
projects_in_db = dict(amount=1)
project_update_payload = dict(name="Project 2")


model_create_payload = dict(name="Model 1", type=ModelType.multi_class)
model_update_payload = dict(name="Model 2", type=ModelType.binary)

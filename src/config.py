import requests
import yaml
from pydantic import BaseModel, Field, AnyHttpUrl


class ClientConfig(BaseModel):
    login: str = Field(..., title="Login", description="User login")
    password: str = Field(..., title="Password", description="User password")
    host: AnyHttpUrl = Field(..., title="Host", description="XUI host")


def load_config(file_path: str) -> ClientConfig:
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return ClientConfig(**config_data)


def test_connect(config: ClientConfig) -> requests.Response:
    data = {"username": config.login, "password": config.password}
    ses = requests.Session()
    response = ses.post(f"{config.host}/login", data=data)
    return response

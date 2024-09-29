import requests
from src.config import ClientConfig


def authenticate(config: ClientConfig) -> requests.Session:
    data = {"username": config.login, "password": config.password}
    ses = requests.Session()
    response = ses.post(f"{config.host}/login", data=data)

    if response.status_code == 200:
        print("Successfull authenticated.")
        return ses
    else:
        print("Authentication error.")
        raise Exception(f"Error: {response.status_code} - {response.text}")

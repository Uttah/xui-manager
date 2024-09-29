from src.config import ClientConfig, load_config
from src.auth import authenticate
from src.gen_secrets import generate_keys
from src.xui_api import generate_shortid, get_all_inbounds, add_inbound, add_client, get_all_clients, get_link


def main():
    config = load_config("config.yaml")
    session = authenticate(config)

    inbounds = get_all_inbounds(config, session)
    print(inbounds)
    clients = get_all_clients(config, session)
    print(clients)

    # Add entyties into 3xui
    # response = add_client(config, session, day=30,
    #                       tg_id="uttah", user_id="2")
    # response = add_inbound(config, session)
    # print(response.status_code)
    # print(response.json())

    response = get_link(config=config, session=session, user_id="2")
    print(response)


if __name__ == "__main__":
    main()

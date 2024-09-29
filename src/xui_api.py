import json
import requests
import uuid
import secrets
from src.config import ClientConfig


def generate_shortid():
    return secrets.token_hex(4)


def get_all_inbounds(config: ClientConfig, session: requests.Session) -> dict:
    """
    Get inbounds list
    """
    response = session.get(f'{config.host}/panel/api/inbounds/list')

    # debug info
    # print(f"Status code: {response.status_code}")
    # print(f"Response text: {response.text}")

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return {}
    else:
        print("Error")
        return {}


def add_inbound(config: ClientConfig, session: requests.Session) -> requests.Response:
    """
    Port in data is always 39724 now, but it need to be changed in future
    """
    private_key, public_key = generate_keys()
    shortid = generate_shortid()

    settings = {
        "clients": [],
        "decryption": "none",
        "fallbacks": []
    }

    streamSettings = {
        "network": "tcp",
        "security": "reality",
        "externalProxy": [],
        "realitySettings": {
            "show": False,
            "xver": 0,
            "dest": "yahoo.com:443",
            "serverNames": [
                    "yahoo.com",
                    "www.yahoo.com"
            ],
            "privateKey": private_key.strip(),
            "minClient": "",
            "maxClient": "",
            "maxTimediff": 0,
            "shortIds": [
                shortid
            ],
            "settings": {
                "publicKey": public_key.strip(),
                "fingerprint": "chrome",
                "serverName": "",
                "spiderX": "/"
            }
        },
        "tcpSettings": {
            "acceptProxyProtocol": False,
            "header": {
                "type": "none"
            }
        }
    }

    sniffing = {
        "enabled": True,
        "destOverride": [
            "http",
            "tls",
            "quic",
            "fakedns"
        ]
    }

    settings_str = json.dumps(settings)
    streamSettings_str = json.dumps(streamSettings)
    sniffing_str = json.dumps(sniffing)

    header = {"Accept": "application/json"}
    data = {
        "enable": True,
        "remark": "New inbound",
        "listen": "",
        "port": 39724,
        "protocol": "vless",
        "expiryTime": 0,
        "settings": settings_str,
        "streamSettings": streamSettings_str,
        "sniffing": sniffing_str
    }
    response = session.post(
        f'{config.host}/panel/api/inbounds/add', headers=header, json=data)
    return response


def add_client(config: ClientConfig,
               session: requests.Session,
               day: int,
               tg_id: str,
               user_id: str) -> requests.Response:
    """
    id in data1 is always 26 now, but it need to be changed in future
    """

    epoch = datetime.datetime.utcfromtimestamp(0)
    x_time = int((datetime.datetime.now() - epoch).total_seconds() * 1000.0)
    x_time += 86400000 * day - 10800000

    header = {"Accept": "application/json"}
    data1 = {
        "id": 26,
        "settings": json.dumps({
            "clients": [
                {
                    "id": str(uuid.uuid1()),
                    "alterId": 90,
                    "email": str(user_id),
                    "limitIp": 3,
                    "totalGB": 0,
                    "expiryTime": x_time,
                    "enable": True,
                    "tgId": str(tg_id),
                    "subId": ""
                }
            ]
        })
    }
    response = session.post(
        f'{config.host}/panel/api/inbounds/addClient', headers=header, json=data1)
    return response


def get_all_clients(config: ClientConfig, session: requests.Session) -> list:
    """
    Get all clients from all inbounds
    :param session: requests.Session - session after authentication
    :param config: ClientConfig - configuration
    :return: list - list of all clients
    """
    clients_list_response = get_all_inbounds(config, session)

    all_clients = []

    for obj in clients_list_response['obj']:
        settings = json.loads(obj['settings'])
        all_clients.extend(settings['clients'])

    return all_clients


def get_link(user_id: str, session: requests.Session, config: ClientConfig) -> str:
    """
    Clients link using user_id.
    :param user_id: str - clients id (email)
    :param session: requests.Session - seession after authentication
    :param config: ClientConfig - configuration
    :return: str - generated link
    """
    # All inbounds
    inbounds_response = get_all_inbounds(config, session)

    client_id = None
    short_id = None
    public_key = None
    stream_settings = None

    # Find client by user_id in all inbounds
    for inbound in inbounds_response['obj']:
        clients = json.loads(inbound['settings'])['clients']

        # Find client with client_id (user_id)
        for client in clients:
            if client['email'] == user_id:
                client_id = client['id']
                stream_settings = json.loads(inbound['streamSettings'])
                short_id = stream_settings['realitySettings']['shortIds'][0]
                public_key = stream_settings['realitySettings']['settings']['publicKey']
                break

    if not client_id or not short_id or not public_key:
        raise ValueError(
            f"Клиент с user_id {user_id} не найден или отсутствуют необходимые данные")

    # Its need for generate network and security settings if they are not tcp and reality
    # tcp = stream_settings['network']
    # reality = stream_settings['security']

    tcp = "tcp"
    security = "reality"
    sni = "yahoo.com"
    host = str(config.host)
    host_with_port = host.split("//")[-1]
    host_ip = host_with_port.split(":")[0]

    link = (f"vless://{client_id}@{host_ip}:39724/"
            f"?type={tcp}&security={security}&fp=chrome"
            f"&pbk={public_key}"
            f"&sni={sni}&sid={short_id}&spx=%2F#New%20inbound-{user_id}")

    return link

# Скрипт конфигурации клиента

Этот Python-скрипт взаимодействует с сервером для управления конфигурацией клиентов и inbound для указанного хоста. Он использует различные библиотеки, включая `requests`, `pydantic` и `cryptography`, для выполнения таких задач, как аутентификация, генерация ключей и управление клиентами.

## Требования

Для запуска этого скрипта необходимо установить следующие библиотеки Python:

- `requests`
- `pydantic`
- `cryptography`
- `pyyaml`

Вы можете установить их с помощью pip:

```sh
pip install requests pydantic cryptography pyyaml
```

## Конфигурация

Создайте файл `config.yaml` в той же директории, что и скрипт, со следующим содержимым:

```yaml
login: ваш_логин
password: ваш_пароль
host: http://example.com:2053
```

Замените `ваш_логин`, `ваш_пароль` и `http://example.com:2053` на ваши реальные учетные данные и URL хоста.

## Функции

### `load_config(file_path: str) -> ClientConfig`

Загружает конфигурацию из YAML-файла.

**Параметры:**

- `file_path`: Путь к YAML-файлу конфигурации.

**Возвращает:**

- Экземпляр `ClientConfig`.

### `test_connect(config: ClientConfig) -> requests.Response`

Тестирует соединение с хостом, отправляя запрос на вход.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.

**Возвращает:**

- Объект `requests.Response`.

### `authenticate(config: ClientConfig) -> requests.Session`

Аутентифицируется и возвращает сессию, если аутентификация успешна.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.

**Возвращает:**

- Объект `requests.Session`.

### `base64_url_safe_encode(data: bytes) -> str`

Кодирует данные в формат base64 URL-safe.

**Параметры:**

- `data`: Данные в формате байт.

**Возвращает:**

- Закодированная строка.

### `generate_keys() -> tuple`

Генерирует приватные и публичные ключи для VLESS.

**Возвращает:**

- Кортеж, содержащий приватный и публичный ключи в виде строк.

### `generate_shortid() -> str`

Генерирует короткий ID.

**Возвращает:**

- Строка, представляющая короткий ID.

### `get_all_inbounds(config: ClientConfig, session: requests.Session) -> dict`

Получает список inbound с сервера.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.
- `session`: Аутентифицированная `requests.Session`.

**Возвращает:**

- Словарь с данными о inbound.

### `add_inbound(config: ClientConfig, session: requests.Session) -> requests.Response`

Добавляет новый inbound на сервер.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.
- `session`: Аутентифицированная `requests.Session`.

**Возвращает:**

- Объект `requests.Response`.

### `add_client(config: ClientConfig, session: requests.Session, day: int, tg_id: str, user_id: str) -> requests.Response`

Добавляет нового клиента на сервер.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.
- `session`: Аутентифицированная `requests.Session`.
- `day`: Количество дней до истечения срока действия.
- `tg_id`: Telegram ID клиента.
- `user_id`: ID или email клиента.

**Возвращает:**

- Объект `requests.Response`.

### `get_all_clients(config: ClientConfig, session: requests.Session) -> list`

Получает список всех клиентов из всех inbound.

**Параметры:**

- `config`: Экземпляр `ClientConfig`.
- `session`: Аутентифицированная `requests.Session`.

**Возвращает:**

- Список клиентов.

### `get_link(user_id: str, session: requests.Session, config: ClientConfig) -> str`

Генерирует ссылку для клиента по его user ID.

**Параметры:**

- `user_id`: ID или email клиента.
- `session`: Аутентифицированная `requests.Session`.
- `config`: Экземпляр `ClientConfig`.

**Возвращает:**

- Строка с сгенерированной ссылкой.

## Использование

1. **Загрузите конфигурацию и аутентифицируйтесь:**

   ```python
   config = load_config("config.yaml")
   session = authenticate(config)
   ```

2. **Получите все inbound:**

   ```python
   inbounds = get_all_inbounds(config, session)
   print(inbounds)
   ```

3. **Добавьте новый inbound:**

   ```python
   response = add_inbound(config, session)
   print(response.status_code, response.text)
   ```

4. **Добавьте нового клиента:**

   ```python
   response = add_client(config, session, day=30, tg_id="123456789", user_id="client@example.com")
   print(response.status_code, response.text)
   ```

5. **Получите всех клиентов:**

   ```python
   clients = get_all_clients(config, session)
   print(clients)
   ```

6. **Генерируйте ссылку для клиента:**

   ```python
   link = get_link(user_id="client@example.com", session=session, config=config)
   print(link)
   ```



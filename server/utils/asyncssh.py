import asyncssh


class SSHSession:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.conn = None

    async def connect(self):
        try:
            print(f"Подключение к {self.hostname}...")
            self.conn = await asyncssh.connect(
                self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                known_hosts=None
            )
            print("Соединение установлено!")
        except Exception as e:
            print(f"Ошибка подключения: {str(e)}")

    async def run_command(self, command):
        if self.conn is None:
            print("Сначала подключитесь к серверу.")
            return None
        
        result = await self.conn.run(command)
        return result

    async def close(self):
        if self.conn:
            await self.conn.close()
            print("Соединение закрыто.")
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from schemas.terminal import SSHSchema
import asyncssh
from utils.asyncssh import SSHSession
import json

router = APIRouter()

class SSHSession:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
    
    async def connect(self):
        return await asyncssh.connect(self.hostname, port=self.port, username=self.username, password=self.password, known_hosts=None)

@router.websocket("/ws/terminal")
async def get_terminal(websocket: WebSocket):
    await websocket.accept()
    print("Клиент подключился!")

    connection_params = await websocket.receive_text()
    params = json.loads(connection_params)

    ssh_session = SSHSession(
        hostname=params['hostname'],
        port=params['port'],
        username=params['username'],
        password=params['password'],
    )

    await handle_session(ssh_session, websocket)

async def handle_session(ssh_session: SSHSession, websocket: WebSocket):
    try:
        async with await ssh_session.connect() as conn:
            current_dir = '/root'  # Начальная директория, измените при необходимости

            while True:
                command = await websocket.receive_text()
                if command.lower() in ['exit', 'quit']:
                    break
                
                # Обработка команды 'cd'
                if command.startswith('cd '):
                    new_dir = command[3:].strip()
                    if new_dir == '..':
                        # Возвращаемся на уровень выше
                        current_dir = '/'.join(current_dir.split('/')[:-1]) or '/'
                    else:
                        # Пытаемся перейти в новую директорию
                        new_path = f"{current_dir}/{new_dir}".replace('//', '/')
                        result = await conn.run(f"cd {new_path} && pwd")
                        if result.returncode == 0:
                            current_dir = new_path
                        else:
                            await websocket.send_text(result.stderr.strip())
                    continue  # Пропускаем выполнение команды cd

                # Выполняем команду
                result = await conn.run(f"cd {current_dir} && {command}")
                await websocket.send_text(f"Команда: {command}\nРезультат:\n{result.stdout.strip() or result.stderr.strip()}")

    except WebSocketDisconnect:
        print("Клиент отключился.")


import React, { useEffect, useState } from 'react';
import CommandForm from './CommandForm';

const WebSocketTerminal = () => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [command, setCommand] = useState('');
  const [port, setPort] = useState(22);
  const [hostname, setHostname] = useState('185.251.90.58');
  const [username, setUsername] = useState('root');
  const [password, setPassword] = useState('ufexwepukawead');
  const [sessionId] = useState(Date.now().toString()); // Уникальный идентификатор сессии

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/v1/ws/terminal`);

    ws.onopen = () => {
      const connectionData = {
          hostname: hostname,
          port: port,
          username: username,
          password: password
      };

      ws.send(JSON.stringify(connectionData));
      console.log('Данные для подключения отправлены:', connectionData);
      console.log('Соединение с вебсокетом установлено!');
      // Можно отправить дополнительные данные, если нужно
    };

    ws.onmessage = (event) => {
      const newMessage = event.data;
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    ws.onclose = () => {
      console.log('Соединение с вебсокетом закрыто.');
    };

    setSocket(ws);

    return () => {
      ws.close();
      console.log('Вебсокет закрыт при размонтировании компонента.');
    };
  }, [sessionId]);

  const handleFormSend = (e) => {
    e.preventDefault();
    if (socket && command) {
      socket.send(command);
      setCommand(''); // Очищаем поле ввода
    }
  };

  return (
    <div className="bg-white flex justify-center p-4">
      <div>
        <CommandForm />
      </div>
      <form onSubmit={handleFormSend}>
      <div className="flex bg-black rounded-lg justify-center items-center w-">
        <div className="p-2 flex">

          <div className="m-2">
            <input
              type="text"
              className="text-gray-900 p-2 rounded-lg"
              value={port}
              onChange={(e) => setPort(e.target.value)}
              placeholder="Введите порт..."
              />
          </div>
          <div className="mt-2">
            <input
              type="text"
              className="text-gray-900 p-2 rounded-lg"
              value={hostname}
              onChange={(e) => setHostname(e.target.value)}
              placeholder="Введите адрес..."
              />
          </div>
          <div className="m-2">
            <input
              type="text"
              className="text-gray-900 p-2 rounded-lg"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Введите пользователя..."
              />
          </div>
          <div className="m-2">
            <input
              type="text"
              className="text-gray-900 p-2 rounded-lg"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Введите пароль..."
              />
          </div>
            <button 
              type="submit" 
              className="p-2 mt-2 bg-black rounded-lg"
              >
                Подключиться
            </button>
        </div>
      </div>
      <div className="bg-black rounded-lg p-4 mt-4">
        <ul>
          {messages.map((msg, index) => (
            <li className="mt-2" key={index}>{msg}</li>
          ))}
        </ul>
        <div className="mt-2">
            <input
              type="text"
              className="text-white p-2 bg-black w-full rounded-lg mt-2"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Введите команду..."
              />
          </div>
      </div>

      </form>
    </div>
  );
};

export default WebSocketTerminal;
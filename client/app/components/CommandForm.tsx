import React, { useState } from 'react';

const CommandForm = () => {
  const [commands, setCommands] = useState(['']); // Начинаем с одного пустого поля

  const handleChange = (index, value) => {
    const newCommands = [...commands];
    newCommands[index] = value; // Обновляем значение в массиве
    setCommands(newCommands);
  };

  const addCommandField = () => {
    setCommands([...commands, '']); // Добавляем новое пустое поле
  };

  return (
    <div className="max-w-sm lg:mr-4">
      <h1 className="text-2xl font-semibold text-black mb-4">Введите последовательность команд:</h1>
      {commands.map((command, index) => (
        <div className="flex items-center mb-3" key={index}>
          <input
            type="text"
            value={command}
            onChange={(e) => handleChange(index, e.target.value)}
            className="flex-1 p-2 border rounded border-gray-300"
            placeholder="Введите команду"
          />
          <button onClick={addCommandField} className="ml-2 text-green-500 hover:text-green-700">
            ➕
          </button>
        </div>
      ))}
      <button className="mt-4 bg-blue-500 text-white py-2 px-4 rounded">
        Отправить команды
      </button>
    </div>
  );
};

export default CommandForm;

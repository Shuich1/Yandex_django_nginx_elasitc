import abc
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    """
    Реализация хранилища состояния в файле json
    """
    def __init__(self, file_path: Optional[str] = None) -> None:
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """
        Сохранить состояние в файл
        Args:
            state: Словарь с состоянием
        Returns:
            None
        """

        base_state = self.retrieve_state()
        base_state.update(state)

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(
                base_state,
                file
            )

    def retrieve_state(self) -> dict:
        """
        Загрузить состояние из файла
        Returns:
            Словарь с состоянием
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError):
            return {
                'last_etl_process_time': '1970-01-01 00:00:00.000000+00',
                'previous_extracted_ids': []
            }


class State:
    """
    Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение
    на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """
        Установить состояние для определённого ключа
        Args:
            key: Ключ
            value: Значение
        Returns:
            None
        """
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """
        Получить состояние по определённому ключу
        Args:
            key: Ключ
        Returns:
            Значение
        """
        return self.storage.retrieve_state().get(key)

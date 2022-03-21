class Dispatcher:
    """Диспетчер предоставляет интерфейс для работы со списком задач (технически это словарь)."""
    def __init__(self):
        self.index = 0
        self.task_list = {}

    def add_task(self, task: dict):
        """Функция добавляет задачу в список и присваивает ей id и начальный статус"""
        self.index += 1
        task['id'] = self.index
        task['status'] = "queued"
        self.task_list[self.index] = task

    def get_task(self, task_id: int):
        """Функция возвращает из списка задачу с заданным id"""
        try:
            task = self.task_list[task_id]
        except KeyError:
            pass
        else:
            return task

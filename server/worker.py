from time import sleep


class Worker:
    def __init__(self, dispatcher):
        self.index = 1
        self.dispatcher = dispatcher

    def worker_process(self):
        while True:
            try:
                task = self.dispatcher.task_list[self.index]
            except KeyError:
                cleanup()
                # When queue is empty, worker performs clean-up operations, deleting outdated tasks
                # worker.cleanup()
                # Не реализовано из-за отутствия задачи в ТЗ и лишнего времени у автора :)
            else:
                # TO-DO: перенести все обновления очереди в диспетчер: только он может изменять список
                self.dispatcher.task_list[self.index]['status'] = 'in progress'
                func = task['task']
                result = globals()[func](task)
                self.dispatcher.task_list[self.index] = result
                self.index += 1

            sleep(5)
            print(self.dispatcher.task_list)


def reverse(data: dict):
    data['result'] = data['text'][::-1]
    data['status'] = 'done'
    sleep(2)
    return data


def switch(data: dict):
    s = data['text']
    data['result'] = ''.join([s[x:x + 2][::-1] for x in range(0, len(s), 2)])
    data['status'] = 'done'
    sleep(5)
    return data


def repeat(data: dict):
    s = data['text']
    data['result'] = ''.join([s[x] * (x + 1) for x in range(len(s))])
    data['status'] = 'done'
    sleep(7)
    return data


def cleanup():
    """Предполагаемый алгоритм: при выдаче результата функция диспетчера get_task проставляет задаче таймстемп.
    Функция cleanup проходится по очереди начиная с младших индексов и проверяет таймстемпы у задач.
    Если текущее время - таймстемп > TTL, задача удаляется.
    """
    pass

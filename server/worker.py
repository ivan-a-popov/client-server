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
                # When queue is empty, worker performs clean-up operations, deleting outdated tasks
                # worker.cleanup()
                pass
            else:
                self.dispatcher.task_list[self.index]['status'] = 'in progress'
                print(self.dispatcher.task_list)
                func = task['task']
                result = globals()[func](task)
                result['status'] = 'done'
                self.dispatcher.task_list[self.index] = result
                self.index += 1

            sleep(5)
            print(self.dispatcher.task_list)


def reverse(data: dict):
    data['result'] = data['text'][::-1]
    sleep(2)
    return data


def switch(data: dict):
    s = data['text']
    data['result'] = ''.join([s[x:x + 2][::-1] for x in range(0, len(s), 2)])
    sleep(5)
    return data


def repeat(data: dict):

    sleep(7)


def cleanup():
    pass

#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread
import json

import dispatcher
import log_setup
import worker

HOST = "localhost"
PORT = 8080
TTL = 600  # task time to live (seconds since last call)


class SimpleServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Функция для обработки get-запросов.
        Мы оставляем валидацию данных на клиенте, поэтому здесь
        дополнительные проверки не проводятся.
        Интерпретацию пустого ответа (индекс не найден) мы также оставляем на клиенте.
        """
        self._set_headers()
        parsed_data = urlparse(self.path)
        task_id = int(parse_qs(parsed_data.query)['id'][0])
        response = dispatcher.get_task(task_id)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        """Функция для обработки post-запросов.
        Мы оставляем валидацию данных на клиенте, поэтому здесь
        дополнительные проверки не проводятся.
        """
        self._set_headers()
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)
        dispatcher.add_task(data)
        self.wfile.write(json.dumps(data).encode('utf-8'))


def start(web_server):
    log_setup.logger.info("Server started at http://%s:%s" % (HOST, PORT))
    web_server.serve_forever()


if __name__ == "__main__":

    webServer = HTTPServer((HOST, PORT), SimpleServer)
    dispatcher = dispatcher.Dispatcher()
    worker = worker.Worker(dispatcher)

    server_thread = Thread(target=start, args=(webServer,), daemon=True)
    server_thread.start()

    worker_thread = Thread(target=worker.worker_process())
    worker_thread.start()

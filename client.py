#!/usr/bin/env python3
import http.client
import argparse
import signal
import json
import sys
from time import sleep

HOST = "localhost"
PORT = 8080


def ctrlc_handler(sig, frame):
    print('Waiting stopped by keyboard command')
    sys.exit(0)


def get(task_id: str):
    try:
        int(task_id)
    except ValueError:
        print("Error: ID must be integer")
        quit(1)
    conn = http.client.HTTPConnection(HOST, PORT)
    try:
        conn.request("GET", "/?id=" + task_id)
    except ConnectionRefusedError:
        print("Error: can't establish connection with server")
        quit(1)
    else:
        r = conn.getresponse()
        raw_data = r.read()
        data = (json.loads(raw_data.decode('utf-8')))
        return data


def post(cmd: str, text: str):
    conn = http.client.HTTPConnection(HOST, PORT)
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"task": cmd, "text": text})
    conn.request("POST", "/", payload, headers)
    res = conn.getresponse()
    response = json.loads(res.read())
    return response


def check(data, cmd):
    if data:
        print('status:', data['status'])
        if data['result'] and cmd == 'result':
            print('result:', data['result'])
        return
    else:
        print("Error: task not found")
        quit(1)


signal.signal(signal.SIGINT, ctrlc_handler)

parser = argparse.ArgumentParser(description='Sends commands and/or data to String Process Server')

parser.add_argument('text', metavar='string or task ID', type=str,
                    help='a string to process or task ID to check')

parser.add_argument('-w', '--wait', action='store_true', dest='wait',
                    help='tells client to wait until task is done')

command = parser.add_mutually_exclusive_group(required=True)
command.add_argument('-s', '--status', action='store_const', dest='command', const='status',
                     help='gets the status and result of the task from server')
command.add_argument('-t', '--result', action='store_const', dest='command', const='result',
                     help='gets the status and result of the task from server')
command.add_argument('-c', '--switch', action='store_const', dest='command', const='switch',
                     help='switch symbols in pairs (turns "abcd" to "badc")')
command.add_argument('-v', '--reverse', action='store_const', dest='command', const='reverse',
                     help='reverse a string (turns "abc" to "cba")')
command.add_argument('-r', '--repeat', action='store_const', dest='command', const='repeat',
                     help='repeat each symbol of a string according to its position (turns "abc" to "abbccc")')

args = parser.parse_args()

if args.command in ["status", "result"]:
    data = get(args.text)
    print('Checking task...')
    check(data, args.command)
    quit(0)

print('Sending task to server...')
task = post(args.command, args.text)
print('OK', '\n'
      'task ID:', task['id'], '\n'
      'status:', task['status']
      )

if args.wait:
    print('Waiting for result...')
    while True:
        data = get(str(task['id']))
        if data['result']:
            check(data, 'result')
            quit(0)
        else:
            check(data, 'status')

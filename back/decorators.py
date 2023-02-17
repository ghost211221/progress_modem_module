import re

def clear_ok(func):
    def wrapper(cmd, response):
        resp = response
        resp['ans'] = resp['ans'].replace('OK', '')

        return func(cmd, resp)
    return wrapper

def clear_premessage(func):
    def wrapper(cmd, response):
        resp = response
        resp['ans'] = re.sub(r'^[\+\r\n\w]+\:\s', '', resp['ans'].strip())

        return func(cmd, resp)
    return wrapper
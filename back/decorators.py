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
        resp['ans'] = re.sub(r'^\+[\w]+\:\s', '', resp['ans'])

        return func(cmd, resp)
    return wrapper
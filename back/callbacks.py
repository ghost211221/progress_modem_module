from back.context import Context

c = Context()

def cgmi(cmd, response):
    """get manufacturer id"""
    return [{'field': 'manufacturer_id', 'data': response['ans']}]

def cgmm(cmd, response):
    """get device decimal number"""
    return [{'field': 'decimal_number', 'data': response['ans']}]

def cgmr(cmd, response):
    """get firmware version"""
    return [{'field': 'firmware_version', 'data': response['ans']}]

def ati(cmd, response):
    """universal imformation"""
    return [{'field': 'firmware_version', 'data': response['ans']}]
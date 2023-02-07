from back.context import Context

c = Context()

def cgmi(cmd, response):
    """get manufacturer id"""
    return [{'field': 'manufacturer_id', 'data': response['ans'] or ''}]

def cgmm(cmd, response):
    """get device decimal number"""
    return [{'field': 'decimal_number', 'data': response['ans'] or ''}]

def cgmr(cmd, response):
    """get firmware version"""
    return [{'field': 'firmware_version', 'data': response['ans'] or ''}]

def ati(cmd, response):
    """universal imformation"""
    return [{'field': 'firmware_version', 'data': response['ans'] or ''}]
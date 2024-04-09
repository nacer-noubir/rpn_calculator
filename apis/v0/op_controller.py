import requests
from flask import request

def op_list():
    links = {"self": request.url}
    operands = ['+', '-', '*', '/']
    result = {
        "operands": operands,
        "meta": {"pageSize": str(len(operands))},
        "links": links
    }
    print(result)
    return result

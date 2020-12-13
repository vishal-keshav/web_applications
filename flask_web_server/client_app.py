import requests

function_code=\
"""
def factorial(a):
    b = 1
    for c in range(1, a+1):
        b *= c
    return b
factorial(5)
"""

if __name__ == "__main__":
    #base_address = "http://127.0.0.1:5000/"
    base_address = "http://10.0.0.19:5000/"
    #response  = requests.get(base_address + "battery")
    response  = requests.put(base_address + "executer", {"func": function_code})
    print(response.json())
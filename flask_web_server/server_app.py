from flask import Flask
from flask_restful import Api, Resource, reqparse

import ast
import copy
import subprocess

app = Flask(__name__)
api = Api(app)

ctx = {
    "lights": 0,
    "fan": 1
}

def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)
        return result

def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(
            last_ast.body[0]), "<ast>", "eval"),globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"),globals())


# This is stateless (class object created on every request)
class TestService(Resource):
    def get(self, key):
        return {"status": ctx[key]}

class BatteryStatus(Resource):
    def get(self):
        command = 'cat /sys/class/power_supply/battery/capacity'
        out = subprocess.check_output(command, shell=True).decode("utf-8").rstrip()
        return {"battery_percentage": str(out)}

class Executer(Resource):
    def get(self):
        pass

    def put(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument("func", type=str, help="Function to execute")
        args = req_parser.parse_args()
        results = {'out': exec_with_return(args.func)}
        return results

api.add_resource(TestService, "/test/<string:key>")
api.add_resource(BatteryStatus, "/battery")
api.add_resource(Executer, "/executer")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
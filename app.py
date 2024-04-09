from flask import Flask, jsonify, send_from_directory
#from flasgger import Swagger, swag_from
from apis.v0 import op_controller, stack_controller
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('rpnapi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stacks (id TEXT PRIMARY KEY, stack TEXT)''')
    conn.commit()
    conn.close()


@app.route("/specifications/<path:path>")
def send_spec(path):
    return send_from_directory('specifications', path)


SWAGGER_URL = '/swagger'
API_URL = '/specifications/api_v0.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        "app_name": "RPN"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL
                       )
@app.route("/rpn/op")
def list_operands():
    return op_controller.op_list()

@app.route('/rpm/stack', methods = ['POST'])
def create_stack():
    return stack_controller.create_stack()

@app.route("/rpm/stack", methods=['GET'])
def list_stacks():
    return stack_controller.get_stacks()

@app.route("/rpm/stack/<string:stack_id>", methods=['GET'])
def get_stack_by_stack_id(stack_id):
    return stack_controller.get_stack_by_stack_id(stack_id)

@app.route("/rpm/stack/<string:stack_id>", methods=['POST'])
def  push(stack_id):
    return stack_controller.push_value_to_stack(stack_id)

@app.route("/rpm/stack/<string:stack_id>/op/<path:op>", methods=['POST'])
def  apply_operand_to_stack(stack_id,op):
    return stack_controller.apply_operand_to_stack(stack_id,op)

@app.route("/rpm/stack/<string:stack_id>", methods=['DELETE'])
def delete_stack(stack_id):
    return stack_controller.delete_stack(stack_id)
if __name__ == "__main__":
    create_database()
    app.run(debug=True)
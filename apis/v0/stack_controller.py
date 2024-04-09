from flask import request, abort
import sqlite3
import uuid
import ast
from rpn.rpn import stack
import operator

ops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/":operator.floordiv }

def get_cursor():
    #Connect to db and return con and cusor
    conn = sqlite3.connect('rpnapi.db')
    c = conn.cursor()
    return conn, c

def create_stack():
    #get stack from payload and insert it in db
    if not request.get_json():
        abort(400)

    data = request.get_json()

    stack_id = str(uuid.uuid4())
    try:
        conn, c = get_cursor()

        c.execute('INSERT INTO stacks (id, stack) VALUES (?, ?)', (stack_id, str(data['stack']),))
        conn.commit()
    except Exception as e:
        raise("Error updating db")
    finally:
        if conn:
            conn.close()
    links = request.url

    result = {
        "stack_id": stack_id,
        "links": links
    }
    print(result)
    return result, 201

def format_stack(stack_data):
    stack = {
        "stack_id": stack_data[1],
        "stack": stack_data[0]
        }
    return stack

def get_stacks():
    try:
        conn, c = get_cursor()
        c.execute('SELECT * FROM stacks')
        result_data = c.fetchall()
    except Exception as e:
        raise("Error accessing db")
    finally:
        if conn:
            conn.close()
    
    formated_result = []
    for stack in result_data:
        formated_result.append(format_stack(stack))

    links = {"self": request.url}
    result = {
        "stacks": formated_result,
        "meta": {"pageSize": str(len(result_data))},
        "links": links
    }
    return result

def get_stack_by_stack_id(stack_id):
    try:
        conn, c = get_cursor()
        c.execute(f'SELECT * FROM stacks where id = "{stack_id}"')
        result_data = c.fetchone()
        conn.close()
    except Exception as e:
        raise("Error accessing db")
    finally:
        if conn:
            conn.close()

    if len(result_data) == 0:
        raise ValueError(f'Stack with id:{stack_id} not found')
    formated_result = format_stack(result_data)

    links = {"self": request.url}
    result = {
        "stack": formated_result,
        "links": links
    }
    return result

def push_value_to_stack(stack_id):
    
    if not request.get_json():
        abort(400)
    new_value = request.get_json()['value']
    try:
        conn, c = get_cursor()
        c.execute(f'SELECT * FROM stacks where id = "{stack_id}"')
        result_data = c.fetchone()

        result_list = ast.literal_eval(result_data[1])
        result_list.append(int(new_value))
        new_stack = str(result_list)
        c.execute(f'UPDATE stacks SET stack ="{new_stack}" WHERE id = "{stack_id}"')
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.close()

    formated_result = format_stack([new_stack, stack_id])
    links = {"self": request.url}
    result = {
        "stack": formated_result,
        "links": links
    }
    return result, 202

def apply_operand_to_stack(stack_id, op):
    try:
        conn = sqlite3.connect('rpnapi.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM stacks where id = "{stack_id}"')
        result_data = c.fetchone()

        result_list = ast.literal_eval(result_data[1])
        stack_op = stack(result_list)

        op = op.replace("'","")

        new_stack = ops[op](stack_op, 1)
        c.execute(f'UPDATE stacks SET stack ="{new_stack}" WHERE id = "{stack_id}"')
        conn.commit()
    
    except Exception as e:
        raise e
    finally:
        conn.close()

    formated_result = format_stack([new_stack, stack_id])
    links = {"self": request.url}
    result = {
        "stack": formated_result,
        "links": links
    }
    return result

def delete_stack(stack_id):
    try:
        conn, c = get_cursor()
        c.execute(f'SELECT * FROM stacks where id = "{stack_id}"')
        result_data = c.fetchone()
        
        if result_data:
            c.execute(f'DELETE from stacks where id = "{stack_id}"')
            conn.commit()
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

    if not result_data:
        raise ValueError(f'Stack with id:{stack_id} not found')

    links = {"self": request.url}
    result = {
        "links": links
    }
    return result, 204
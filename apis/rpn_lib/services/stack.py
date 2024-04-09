import sqlite3

def insert_stack(stack_id, stack_data = []):
    conn = sqlite3.connect('rpnapi.db')
    try:
        c = conn.cursor()
        c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    except Exception as e:
        print('ok')
    finally:
        conn.commit()
        conn.close()

    return 
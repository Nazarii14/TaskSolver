from constants import *
from prime import is_prime
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    port=DATABASE_PORT,
)

def update_task_running(id, is_running):
    global conn

    try:
        with conn.cursor() as cursor:
            update_is_running = sql.SQL('UPDATE tasksolver_task SET is_running = %s WHERE id = %s;')
            cursor.execute(update_is_running, (is_running, id))
            conn.commit()

            print("**************** Committed!")
    except Exception as e:
        print("Error occurred while updating database:", str(e))
        conn.rollback()


def find_nth_prime_number(n, id):
    global conn

    # running task update
    update_task_running(id, True)

    prime_count, candidate, iteration_count = 0, 2, 0
    previous_percent = -1

    while True:
        if is_prime(candidate):
            prime_count += 1
            if prime_count == n:
                write_final_result(candidate, id)
                conn.commit()
                return candidate

        iteration_count += 1
        candidate += 1
        current_percent = int((candidate / n) * 100)

        if current_percent != previous_percent and current_percent in range(0, 101):
            status = update_db(current_percent, id)
            if status == 'error':
                print("THERE WAS AN ERROR WHILE UPDATING DB...")
                break
            previous_percent = current_percent
    return None


def update_db(percentage, id):
    global conn

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL('SELECT id FROM tasksolver_task WHERE id = %s;'), (id,))
            existing_row = cursor.fetchone()

            if existing_row:
                update_query = sql.SQL('UPDATE tasksolver_task SET completion_percentage = %s WHERE id = %s;')
                cursor.execute(update_query, (percentage, id))
                conn.commit()
                print("**************** ITERATIONS")
                get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
                cursor.execute(get_data_by_id, (id,))
                row = cursor.fetchone()
                print("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
                res_row = [str(i) for i in row] if row else []
                print('\t'.join(res_row))
                return 'success'
            else:
                print(f"TASK {id} DOES NOT EXIST IN DB.")
                return 'error'
    except Exception as e:
        print("Error occurred while updating database:", str(e))

    try:
        with conn.cursor() as cursor:
            print("**************** ITERATIONS")
            get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
            cursor.execute(get_data_by_id, (id,))
            row = cursor.fetchone()
            print("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
            res_row = [str(i) for i in row] if row else []
            print('\t'.join(res_row))
    except Exception as e:
        print("Error occurred while updating database:", str(e))


def write_final_result(result, id):
    global conn

    try:
        with conn.cursor() as cursor:
            update_query = sql.SQL('UPDATE tasksolver_task SET result = %s, is_running = %s, is_finished = %s WHERE id = %s;')
            print("**************** WRITING FINAL RESULT")
            print("**************** RESULT:", result)
            print("**************** ID:", id)
            cursor.execute(update_query, (result, False, True, id))
            conn.commit()
    except Exception as e:
        print("Error occurred while updating/querying database:", str(e))
        conn.rollback()

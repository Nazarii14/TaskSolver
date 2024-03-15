import psycopg2
import logging
from constants import *
from prime import is_prime
from psycopg2 import sql
from psycopg2.pool import SimpleConnectionPool

connection_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=15,
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    port=DATABASE_PORT,
)

def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)

def update_task_running(id: int, is_running: bool) -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            update_is_running = sql.SQL('UPDATE tasksolver_task SET is_running = %s WHERE id = %s;')
            cursor.execute(update_is_running, (is_running, id))
            conn.commit()
    except Exception as e:
        logging.error("Error occurred while updating database:", str(e))
        conn.rollback()
    finally:
        release_connection(conn)


def find_nth_prime_number(n: int, id: int) -> int | None:
    conn = get_connection()
    update_task_running(id, True)

    prime_count, candidate, iteration_count = 0, 2, 0
    previous_percent = -1

    while True:
        if is_prime(candidate):
            prime_count += 1
            if prime_count == n:
                write_final_result(str(candidate), id)
                conn.commit()
                return candidate

        iteration_count += 1
        candidate += 1
        current_percent = int((candidate / n) * 100)

        if current_percent != previous_percent and current_percent in range(0, 101):
            status = update_db(current_percent, id)
            if status == 'error':
                logging.error("THERE WAS AN ERROR WHILE UPDATING DB...")
                conn.rollback()
                break
            previous_percent = current_percent

    return None


def update_db(percentage, id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL('SELECT id FROM tasksolver_task WHERE id = %s;'), (id,))
            existing_row = cursor.fetchone()

            if existing_row:
                update_query = sql.SQL('UPDATE tasksolver_task SET completion_percentage = %s WHERE id = %s;')
                cursor.execute(update_query, (percentage, id))
                conn.commit()

                get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
                cursor.execute(get_data_by_id, (id,))
                row = cursor.fetchone()
                logging.debug("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
                res_row = [str(i) for i in row] if row else []
                logging.debug('\t'.join(res_row))
                return 'success'
            else:
                logging.error(f"TASK {id} DOES NOT EXIST IN DB.")
                return 'error'
    except Exception as e:
        logging.error("Error occurred while updating database:", str(e))
        conn.rollback()
    finally:
        release_connection(conn)

    try:
        with conn.cursor() as cursor:
            get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
            cursor.execute(get_data_by_id, (id,))
            row = cursor.fetchone()
            logging.debug("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
            res_row = [str(i) for i in row] if row else []
            logging.debug('\t'.join(res_row))
    except Exception as e:
        logging.error("Error occurred while updating database:", str(e))
        conn.rollback()
    finally:
        release_connection(conn)

def write_final_result(result, id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            update_query = sql.SQL('UPDATE tasksolver_task SET result = %s, is_running = %s, is_finished = %s WHERE id = %s;')
            cursor.execute(update_query, (result, False, True, id))
            conn.commit()
            logging.debug("**************** WRITING FINAL RESULT")
            logging.debug("**************** RESULT:", result)
            logging.debug("**************** ID:", id)
    except Exception as e:
        logging.error("Error occurred while updating/querying database:", str(e))
        conn.rollback()
    finally:
        release_connection(conn)

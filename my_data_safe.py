import mysql.connector


# Connection to database
def return_my_database_cursor(prepared=False):
    try:
        return my_database.cursor(prepared=prepared)
    except(mysql.connector.OperationalError, UnboundLocalError):
        my_database = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="sql_injection"
                    )
        return my_database, my_database.cursor(prepared=prepared)


# Login not injectable
def login_checker(username, password):
    my_database, my_cursor_prepared = return_my_database_cursor(prepared=True)
    checker_query = "SELECT * FROM users WHERE username = %s AND password = %s;"
    credentials = (username, password)
    my_cursor_prepared.execute(checker_query, credentials)
    my_result = my_cursor_prepared.fetchall()
    my_cursor_prepared.close()
    if len(my_result) > 0:
        return True
    return False

# Register not injectable
def register_checker(username, password):
    my_database, my_cursor_prepared = return_my_database_cursor(prepared=True)
    checker_query = "Select * FROM users WHERE username = %s;"
    my_cursor_prepared.execute(checker_query, [username])
    my_result = my_cursor_prepared.fetchall()
    if len(my_result) > 0:
        my_cursor_prepared.close()
        return False
    register_query = "INSERT INTO users (username, password) VALUES (%s, %s);"
    credentials = (username, password)
    my_cursor_prepared.execute(register_query, credentials)
    my_cursor_prepared.close()
    my_database.commit()
    return True

# Truncate users table
def truncate_users_table():
    my_database, my_cursor = return_my_database_cursor()
    my_cursor.execute("TRUNCATE TABLE users")
    my_cursor.close()

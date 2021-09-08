import mysql.connector


# Connection to database
def return_my_database_cursor():
    try:
        return my_database.cursor()
    except(mysql.connector.OperationalError, UnboundLocalError):
        my_database = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="sql_injection"
                    )
        return my_database, my_database.cursor()


# Login injectable
def login_checker(username, password):
    my_database, my_cursor = return_my_database_cursor()
    my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';")
    my_result = my_cursor.fetchall()
    my_cursor.close()
    if len(my_result) > 0:
        return True
    return False
    
# Register injectable
def register_checker(username, password):
    my_database, my_cursor = return_my_database_cursor()
    my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "';")
    my_result = my_cursor.fetchall()
    if len(my_result) > 0:
        my_cursor.close()
        return False
    my_cursor.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');")
    my_cursor.close()
    my_database.commit()
    return True

# Truncate users table
def truncate_users_table():
    my_database, my_cursor = return_my_database_cursor()
    my_cursor.execute("TRUNCATE TABLE users")
    my_cursor.close()

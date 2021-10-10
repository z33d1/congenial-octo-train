from flask import Flask, request, render_template
import requests
import jwt

CLIENT_ID = 1
CLIENT_SECRET = 'SECRET_KEY_APP_1'
app = Flask(__name__)


@app.route('/')
def hello_world():
    code = request.args['code']

    print("Getting token...")
    data = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code}
    r = requests.post('http://localhost:8089/auth/token', json=data)
    if r.status_code != 200:
        print(r.status_code)
        print('Cant get token')
        return "<h1>Server error<h1>"

    token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']
    print("access token:", token)
    print("refresh token:", refresh_token)

    print("Getting user orders...")
    user_id = jwt.decode(token, CLIENT_SECRET)['sub']
    print("user_id =",user_id)

    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get('http://localhost:8080/user/{}/order'.format(user_id),
                     headers=headers)

    if r.status_code != 200:
        print('Cant get orders')
        print(r.text)
        return "<h1>Server error<h1>"

    orders = r.json()
    print(orders)


    print("Refresh token...")
    data = {'refresh_token': refresh_token}
    r = requests.post('http://localhost:8089/auth/refresh', json=data)
    print(r.status_code)
    new_access_token = r.json()['access_token']

    print("Getting user orders...")
    user_id = jwt.decode(token, CLIENT_SECRET)['sub']
    print("user_id =",user_id)

    headers = {'Authorization': 'Bearer ' + new_access_token}
    r = requests.get('http://localhost:8080/user/{}/order'.format(user_id),
                     headers=headers)

    if r.status_code != 200:
        print('Cant get orders')
        print(r.text)
        return "<h1>Server error<h1>"

    return "<h1>Your orders: {0}<h1>".format(r.json())



if __name__ == '__main__':
    app.run('localhost', port=9090, debug=True)
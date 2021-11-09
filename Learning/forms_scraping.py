import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

# # POST info to form and return result
# params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
# r = requests.post("http://pythonscraping.com/pages/processing.php",data=params)
# print(r.text)

# params = {'email_addr': 'ryan.e.mitchell@gmail.com'}
# r = requests.post("http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi",data=params)
# print(r.text)

# # POST files
# files = {'uploadFile': open('files/python.png', 'rb')}
# r = requests.post('http://pythonscraping.com/pages/processing2.php', files=files)
# print(r.text)

# # Track login cookies
# params = {'username': 'Ryan', 'password': 'password'}
# r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php', params)
# print('Cookie is set to:')
# print(r.cookies.get_dict())
# print('Going to profile page...')
# r = requests.get('http://pythonscraping.com/pages/cookies/profile.php', cookies=r.cookies)
# print(r.text)

# # requests.Session() to track changing cookies
# session = requests.Session()

# params = {'username': 'username', 'password': 'password'}
# s = session.post('http://pythonscraping.com/pages/cookies/welcome.php',params)

# print('Cookie is set to:')
# print(s.cookies.get_dict())
# print('Going to profile page...')

# s = session.get('http://pythonscraping.com/pages/cookies/profile.php')

# print(s.text)

auth = HTTPBasicAuth('ryan', 'password')
r = requests.post(url='http://pythonscraping.com/pages/auth/login.php', auth=auth)
print(r.text)
import random
from termcolor import colored, cprint
import requests_oauthlib

emails = []
client_key = '6f715814678fcb6db736db4a3dd05386064ffb8be'
client_secret = '2f36af1ef33e0a2bbe5dd5d492269ea7'
lcps = requests_oauthlib.OAuth1Session(client_key=client_key, client_secret=client_secret, signature_method='PLAINTEXT',
                                       signature_type='AUTH_HEADER')


def print_emails(group_id, color):
    data = lcps.get(f'https://api.schoology.com/v1/groups/{group_id}/enrollments',
                    params={"type": "member", "limit": 200, "name_title": ""}).json()
    class_list = data['enrollment']

    try:
        while True:
            data = lcps.get(data['links']['next']).json()
            class_list += data['enrollment']
    except KeyError:
        pass

    def check_num(num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    class_list = [i for i in class_list if i['name_title'] == '' and (check_num(i['school_uid']) and int(i['school_uid']) > 700000)]

    for i in range(30):
        user_id = class_list[random.randint(0, len(class_list) - 1)]["uid"]
        email = lcps.get(f'https://api.schoology.com/v1/users/{user_id}').json()['primary_email']
        while emails.__contains__(email):
            user_id = class_list[random.randint(0, len(class_list) - 1)]["uid"]
            email = lcps.get(f'https://api.schoology.com/v1/users/{user_id}').json()['primary_email']
        cprint(email, color)


# sophomores
print_emails(6242742588, "red")
# juniors
print_emails(5143511856, "green")
# seniors
print_emails(2889950317, "blue")
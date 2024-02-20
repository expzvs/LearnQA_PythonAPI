#import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
#from datetime import datetime
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

    # def setup_method(self):
    #     base_part = "lernqua"
    #     domain = "example.com"
    #     random_part = datetime.now().strftime("%m%d%Y%H%M%S");
    #     self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        # data = {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': self.email
        # }

        res = MyRequests.post("/user/", data=data)

#        assert res.status_code == 200, f"Wrong status code {res.status_code}"
        Assertions.assert_code_status(res, 200)
        #print(res.content)
        Assertions.assert_json_has_key(res, "id")


    def test_create_user_with_existing_email(self):

        email='vinkotov@example.com'
        data = self.prepare_registration_data(email)
#         data = {
#             'password': '123',
#             'username': 'learnqa',
#             'firstName': 'learnqa',
#             'lastName': 'learnqa',
# #            'email': self.email
#              'email': email
#         }

        res = MyRequests.post("/user/", data=data)

        # print(data)
        # print(res.status_code)
        # print(res.content)

#        assert res.status_code == 400, f"Unexpected status code {res.status_code}"
        Assertions.assert_code_status(res, 400)
        assert res.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{res.content}'"


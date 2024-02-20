#import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        res = MyRequests.get("/user/2")
        # print(res.content)
        Assertions.assert_json_has_key(res, "username")
        Assertions.assert_json_has_not_key(res, "email")
        Assertions.assert_json_has_not_key(res, "firstName")
        Assertions.assert_json_has_not_key(res, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        res1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_header(res1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(res1, "user_id")

        res2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        exptd_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(res2, exptd_fields)
#        Assertions.assert_json_has_keys(res2, ["username", "email", "firstName", "lastName"])
        # Assertions.assert_json_has_key(res2, "username")
        # Assertions.assert_json_has_key(res2, "email")
        # Assertions.assert_json_has_key(res2, "firstName")
        # Assertions.assert_json_has_key(res2, "lastName")

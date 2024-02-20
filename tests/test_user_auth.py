import pytest
#import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Autrization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):

        data = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        # res1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        res1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(res1, "auth_sid")
        self.token = self.get_header(res1, "x-csrf-token")

        self.user_id_in_auth_method  = self.get_json_value(res1, "user_id")

#        assert "auth_sid" in res1.cookies, "There is not auth cookie in the response "
#        assert "x-csrf-token" in res1.headers, "There is no CSRF token headers in the response"


        assert "user_id" in res1.json(), "There is no user_id in the response"

#        self.auth_sid = res1.cookies.get("auth_sid")
#        self.token = res1.headers.get("x-csrf-token")
        self.user_id_in_auth_method = res1.json()["user_id"]

    @allure.description("This test successfullly autorize user by email and apssword")
    def test_auth_user(self):

        res2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid":self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            res2,
            "user_id",
            self.user_id_in_auth_method,
            "User id from auth method is not equal to user id from check method"
        )
        # assert "user_id" in res2.json(), "There is no user id in the second response"
        # user_id_in_check_method = res2.json()["user_id"]
        #
        # assert self.user_id_in_auth_method == user_id_in_check_method, "User id from auth method is not equal to user id in check method"

    @allure.description("This test checks authorization status w/o sending cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            res2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            res2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            res2,
            "user_id",
            0,
            f"User is auth with condition {condition}"

        )
        # assert "user_id" in res2.json(), "There is no id in the second response"
        #
        # user_id_from_check_method = res2.json()["user_id"]
        #
        # assert user_id_from_check_method == 0, f"User is auth with condition {condition}"


import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # REGISTER
        register_data = self.prepare_registration_data()

        res1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(res1, 200)
        Assertions.assert_json_has_key(res1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(res1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        res2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(res2, "auth_sid")
        token = self.get_header(res2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        res3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(res3, 200)

        # GET
        res4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            res4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

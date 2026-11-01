"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="test/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ADD YOUR TEST CASES HERE ...

    def test_read_account(self):
        """It should read an account and return its full representation"""
        account = self._create_accounts(1)[0]
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), account.serialize())

    def test_read_missing_account(self):
        """It should return a JSON 404 for a missing account"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Not Found")

    def test_list_accounts(self):
        """It should list every persisted account"""
        accounts = self._create_accounts(3)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({a["id"] for a in response.get_json()}, {a.id for a in accounts})

    def test_list_empty(self):
        """It should return an empty list when no accounts exist"""
        self.assertEqual(self.client.get(BASE_URL).get_json(), [])

    def test_update_account(self):
        """It should persist a full update without changing the id"""
        account = self._create_accounts(1)[0]
        data = account.serialize()
        data["name"] = "Updated Customer"
        data["id"] = 999999
        response = self.client.put(f"{BASE_URL}/{account.id}", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], account.id)
        actual = self.client.get(f"{BASE_URL}/{account.id}").get_json()
        self.assertEqual(actual["name"], "Updated Customer")

    def test_update_missing(self):
        """It should not create an account through PUT"""
        response = self.client.put(f"{BASE_URL}/0", json=AccountFactory().serialize())
        self.assertEqual(response.status_code, 404)

    def test_update_invalid(self):
        """It should reject invalid updates without corrupting stored data"""
        account = self._create_accounts(1)[0]
        response = self.client.put(f"{BASE_URL}/{account.id}", json={"name": "Oops"})
        self.assertEqual(response.status_code, 400)
        db.session.expire_all()
        self.assertEqual(Account.find(account.id).name, account.name)

    def test_update_wrong_content_type(self):
        """It should require JSON for updates"""
        account = self._create_accounts(1)[0]
        response = self.client.put(f"{BASE_URL}/{account.id}", data="text")
        self.assertEqual(response.status_code, 415)

    def test_delete_account(self):
        """It should delete an account and return an empty 204"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.client.get(f"{BASE_URL}/{account.id}").status_code, 404)

    def test_delete_missing(self):
        """It should make repeated deletions idempotent"""
        self.assertEqual(self.client.delete(f"{BASE_URL}/0").status_code, 204)

    def test_create_location(self):
        """It should return a Location that resolves to the new resource"""
        response = self.client.post(BASE_URL, json=AccountFactory().serialize())
        location = response.headers["Location"]
        self.assertEqual(location, f'/accounts/{response.get_json()["id"]}')
        self.assertEqual(self.client.get(location).status_code, 200)
        self.assertEqual(self.client.get("/", base_url="https://example.test").get_json()["paths"], BASE_URL)

    def test_nul_text_rejected_without_mutating(self):
        """It should reject PostgreSQL-invalid NULs for POST and preserve valid data on PUT."""
        response = self.client.post(BASE_URL, json=AccountFactory().serialize())
        self.assertEqual(response.status_code, 201)
        original = response.get_json()
        resource = f'{BASE_URL}/{original["id"]}'
        for field in ["name", "email", "address", "phone_number"]:
            data = dict(original)
            data[field] = "bad\x00value"
            with self.subTest(field=field):
                self.assertEqual(self.client.post(BASE_URL, json=data).status_code, 400)
                self.assertEqual(self.client.put(resource, json=data).status_code, 400)
                self.assertEqual(self.client.get(resource).get_json(), original)
                self.assertEqual(len(Account.all()), 1)

    def test_invalid_input(self):
        """It should reject malformed dates, empty/oversized fields and non-object JSON"""
        original = AccountFactory().serialize()
        invalid = [None, [], "text", 3]
        for field, value in [
            ("date_joined", "not-a-date"),
            ("date_joined", 12),
            ("name", ""),
            ("name", "x" * 65),
            ("email", None),
            ("address", 5),
            ("phone_number", 7),
        ]:
            data = dict(original)
            data[field] = value
            invalid.append(data)
        for data in invalid:
            response = self.client.post(
                BASE_URL, data=__import__("json").dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, 400, repr(data))
        self.assertEqual(Account.all(), [])

    def test_optional_fields(self):
        """It should allow omitted phone and date fields"""
        response = self.client.post(
            BASE_URL, json={"name": "Ada", "email": "a@b.test", "address": "Jakarta"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.get_json()["phone_number"])

    def test_method_not_allowed(self):
        """It should return JSON for an unsupported method"""
        response = self.client.patch(BASE_URL)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.get_json()["status"], 405)

    def test_server_error_handler(self):
        """It should format internal errors as JSON with status 500"""
        from service.common.error_handlers import internal_server_error

        response, code = internal_server_error(Exception("test error"))
        self.assertEqual(code, 500)
        self.assertEqual(response.get_json()["message"], "test error")

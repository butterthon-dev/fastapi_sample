import json
from crud.crud_user import CRUDUser
from fastapi import status
from tests.base import BaseTestCase


class TestUserAPI(BaseTestCase):
    """ ユーザーAPIのテストクラス
    """
    TEST_URL = '/api/v1/users/'

    def test_gets(self):
        """ 一覧取得のテスト
        """
        # テストユーザー登録
        test_data = [
            {
                'email': 'test1@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': False
            },
            {
                'email': 'test2@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': True
            },
            {
                'email': 'test3@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': False
            },
        ]
        for data in test_data:
            CRUDUser(self.db_session).create(data)
            self.db_session.commit()

        response = self.client.get(self.TEST_URL)

        # ステータスコードの検証
        assert response.status_code == status.HTTP_200_OK

        # 取得した件数の検証
        response_data = json.loads(response._content)
        assert len(response_data) == len(test_data)

        # レスポンスの内容を検証
        expected_data = [{
            'email': item['email'],
            'last_name': item['last_name'],
            'first_name': item['first_name'],
            'is_admin': item['is_admin'],
        } for i, item in enumerate(test_data, 1)]
        assert response_data == expected_data

    def test_gets_confirm_rollback(self):
        """ 一覧取得のテスト
        """
        # テストユーザー登録
        test_data = [
            {
                'email': 'test1@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': False
            },
            {
                'email': 'test2@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': True
            },
            {
                'email': 'test3@example.com',
                'password': 'password',
                'last_name': 'last_name',
                'first_name': 'first_name',
                'is_admin': False
            },
        ]
        for data in test_data:
            CRUDUser(self.db_session).create(data)
            self.db_session.commit()

        response = self.client.get(self.TEST_URL)

        # ステータスコードの検証
        assert response.status_code == status.HTTP_200_OK

        # 取得した件数の検証
        response_data = json.loads(response._content)
        assert len(response_data) == len(test_data)

        # レスポンスの内容を検証
        expected_data = [{
            'email': item['email'],
            'last_name': item['last_name'],
            'first_name': item['first_name'],
            'is_admin': item['is_admin'],
        } for i, item in enumerate(test_data, 1)]
        assert response_data == expected_data

from.test_setup import TestSetUp
import pdb

class TestViews(TestSetUp):
    
    def test_user_register_data(self):
        res = self.client.post(self.create_url, self.user1_data, format='json')
        self.assertEqual(res.status_code, 201)
    
    def test_user_login(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        res = self.client.post(self.login_url, self.login_user1, format='json')
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, 302)

    def test_contact_add(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        self.client.post(self.create_url, self.user2_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.post(self.contact_url, self.add_contact_user2, **header)
        self.assertEqual(res.status_code, 201)

    def test_modify_user(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.put(self.modify_user_url, self.user1_modified_data, **header)
        self.assertEqual(res.status_code, 200)
    
    def test_modify_user_password(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.put(self.modify_user_password_url, self.user1_modified_password_data, **header)
        self.assertEqual(res.status_code, 200)

    def test_get_contacts(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.get(self.contact_list_url,{},**header)
        self.assertEqual(res.status_code, 200)

    def test_contact_delete(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        self.client.post(self.create_url, self.user2_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        self.client.post(self.contact_url, self.add_contact_user2, **header)
        res = self.client.post(self.contact_delete, self.add_contact_user2, **header)
        self.assertEqual(res.status_code, 200)
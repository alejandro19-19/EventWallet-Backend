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
        res = self.client.post(self.contact_url, self.add_contact_user2, format='json',**header)
        self.assertEqual(res.status_code, 201)

    def test_modify_user(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.put(self.modify_user_url, self.user1_modified_data,format='json', **header)
        self.assertEqual(res.status_code, 200)
    
    def test_modify_user_password(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.put(self.modify_user_password_url, self.user1_modified_password_data, format='json', **header)
        self.assertEqual(res.status_code, 200)

    def test_get_contacts(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.get(self.contact_list_url,{},format='json',**header)
        self.assertEqual(res.status_code, 200)

    def test_contact_delete(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        self.client.post(self.create_url, self.user2_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        self.client.post(self.contact_url, self.add_contact_user2, format='json', **header)
        res = self.client.post(self.contact_delete, self.add_contact_user2,format='json', **header)
        self.assertEqual(res.status_code, 200)

    def test_create_event(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        self.assertEqual(res.status_code, 201)
    
    def test_modify_event(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        respuesta = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = respuesta.data["data"]["id"]
        data = self.event_modified_data
        data["evento_id"] = id
        res = self.client.put(self.modify_event_url,data,**header)
        self.assertEqual(res.status_code, 200)

    def test_create_invitation(self):
        self.client.post(self.create_url, self.user1_data, format='json') 
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.invitation_data
        data["evento_id"] = id
        data["email"] = mail
        res = self.client.post(self.create_invitation_url,data,format='json',**header)
        self.assertEqual(res.status_code, 201)

    def test_list_invitations(self):
        self.client.post(self.create_url, self.user1_data, format='json') 
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.invitation_data
        data["evento_id"] = id
        data["email"] = mail
        self.client.post(self.create_invitation_url,data,format='json',**header)
        log2 = self.client.post(self.login_url, self.login_user2, format='json')
        Token2 = log2.data['token']
        header2 = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token2)}
        res = self.client.get(self.invitation_list_url,{},format='json',**header2)
        self.assertEqual(res.status_code, 200)

    def test_respond_to_invitation(self):
        self.client.post(self.create_url, self.user1_data, format='json') 
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.invitation_data
        data["evento_id"] = id
        data["email"] = mail
        res3 = self.client.post(self.create_invitation_url,data, format='json',**header)
        inv_id = res3.data["data"]["id"]
        inv_data = self.respond_invitation_data
        inv_data["invitacion_id"] = inv_id
        log2 = self.client.post(self.login_url, self.login_user2, format='json')
        Token2 = log2.data['token']
        header2 = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token2)}
        res = self.client.post(self.r_to_invitation_url, inv_data, format='json', **header2)
        self.assertEqual(res.status_code, 200)

    def test_get_events(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.get(self.event_list_url,{},format='json',**header)
        self.assertEqual(res.status_code, 200)
    
    def test_create_activity(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        data = self.create_activity_data
        res = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res.data["data"]["id"]
        data["evento"] = id
        res2 = self.client.post(self.create_activity_url, data,format='json',**header)
        self.assertEqual(res2.status_code, 201)
    
    def test_create_invitation_activity(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.create_activity_data
        data["evento"] = id
        res3 = self.client.post(self.create_activity_url, data,format='json',**header)
        id2 = res3.data["data"]["id"]
        data2 = self.create_invitation_activity_data
        data2["actividad"] = id2
        data2["participante"] = mail
        res4 = self.client.post(self.create_invitation_activity_url, data2, format='json',**header)
        self.assertEqual(res4.status_code, 403)

    def test_delete_activity(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.create_activity_data
        data["evento"] = id
        res3 = self.client.post(self.create_activity_url, data,format='json',**header)
        id2 = res3.data["data"]["id"]
        data2 = self.delete_activity_data
        data2["actividad_id"] = id2
        res = self.client.post(self.activity_delete_url, data2 ,format='json',**header)
        self.assertEqual(res.status_code, 200)

    def test_modify_activity(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.create_activity_data
        data["evento"] = id
        res3 = self.client.post(self.create_activity_url, data,format='json',**header)
        id2 = res3.data["data"]["id"]
        data2 = self.modify_activity_data
        data2["actividad_id"] = id2
        res = self.client.put(self.modify_activity_url, data2,format='json',**header)
        self.assertEqual(res.status_code, 200)

    def test_get_activities(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res = self.client.get(self.get_activities_url,{},format='json',**header)
        self.assertEqual(res.status_code, 404)

    def test_get_activities(self):
        self.client.post(self.create_url, self.user1_data, format='json')
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}   
        res = self.client.get(self.get_event_balances_url,{},format='json',**header)
        self.assertEqual(res.status_code, 404)
        
    def test_delete_contact_event(self):
        self.client.post(self.create_url, self.user1_data, format='json') 
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.invitation_data
        data["evento_id"] = id
        data["email"] = mail
        res3 = self.client.post(self.create_invitation_url,data, format='json',**header)
        inv_id = res3.data["data"]["id"]
        inv_data = self.respond_invitation_data2
        inv_data["invitacion_id"] = inv_id
        log2 = self.client.post(self.login_url, self.login_user2, format='json')
        Token2 = log2.data['token']
        header2 = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token2)}
        res3 = self.client.post(self.r_to_invitation_url, inv_data, format='json', **header2)
        data = self.delete_contact_event_data
        data["evento"] = id
        data["contacto"] = res1.data["id"]
        res = self.client.post(self.delete_contact_event_url, data, format='json', **header)
        self.assertEqual(res.status_code, 200)  

    def test_assign_value_activity(self):
        self.client.post(self.create_url, self.user1_data, format='json') 
        log = self.client.post(self.login_url, self.login_user1, format='json')
        Token = log.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token)}
        res1 = self.client.post(self.create_url, self.user2_data, format='json')
        mail = res1.data["email"]
        res2 = self.client.post(self.create_event_url,self.event_data,format='json',**header)
        id = res2.data["data"]["id"]
        data = self.invitation_data
        data["evento_id"] = id
        data["email"] = mail
        res3 = self.client.post(self.create_invitation_url,data, format='json',**header)
        inv_id = res3.data["data"]["id"]
        inv_data = self.respond_invitation_data2
        inv_data["invitacion_id"] = inv_id
        log2 = self.client.post(self.login_url, self.login_user2, format='json')
        Token2 = log2.data['token']
        header2 = {'HTTP_AUTHORIZATION': 'Token {}'.format(Token2)}
        res3 = self.client.post(self.r_to_invitation_url, inv_data, format='json', **header2)
        id = res2.data["data"]["id"]
        data = self.create_activity_data
        data["evento"] = id
        res4 = self.client.post(self.create_activity_url, data,format='json',**header)
        id2 = res4.data["data"]["id"]
        data2 = self.create_invitation_activity_data
        data2["actividad"] = id2
        data2["participante"] = mail
        res4 = self.client.post(self.create_invitation_activity_url, data2, format='json',**header)
        data3 = self.assign_value_activity_data
        data3["actividad"] = id2
        data3["participantes"][0]["id"] = res4.data["data"]["participante"]["id"]
        res5 = self.client.put(self.assign_value_activity_url, data3, format='json',**header)
        self.assertEqual(res5.status_code, 200)
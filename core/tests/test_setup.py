from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = reverse('login_user')
        self.create_url = reverse('create_user')
        self.modify_user_url = reverse('modify_user')
        self.modify_user_password_url = reverse('modify_user_password')
        self.contact_url = reverse('create_contact')
        self.contact_list_url = reverse('get_contacts')
        self.contact_delete = reverse('delete_contact')
        self.create_event_url = reverse('create_event')
        self.modify_event_url = reverse('modify_event')
        self.create_invitation_url = reverse('create_invitation')
        self.invitation_list_url = reverse('get_invitations')

        self.user1_data ={
            "nombre": "prueba1",
            "apellidos": "prueba1",
            "apodo":"test1",
            "password": "1234",
            "email": "test@test.com",
            "foto": "test/path"         
        }

        self.user2_data ={
            "nombre": "prueba2",
            "apellidos": "prueba2",
            "apodo":"test2",
            "password": "1234",
            "email": "test2@test.com",
            "foto": "test/path"         
        }

        self.login_user1 = {
            "username":"test@test.com",
            "password":"1234"
        }

        self.user1_modified_data = {
            "nombre": "prueba1mod",
            "apellidos": "prueba1mod",
            "apodo": "test1mod",
            "foto": "test/path"
        }

        self.user1_modified_password_data = {
            "old_password": "1234",
            "new_password": "123456",
        }


        self.add_contact_user2 ={
            "email":"test2@test.com"
        }

        self.event_data ={
            "nombre": "test",
            "descripcion":"test",
            "tipo":"C",
            "foto":"test"
            }
        
        self.event_modified_data={
            "evento_id": None,
            "nombre": "samplename",
            "descripcion":"sampledescription",
            "tipo":"O",
            "foto":"samplepathfoto"
            }
        self.invitation_data={
            "evento_id": None,
            "email": None
        }
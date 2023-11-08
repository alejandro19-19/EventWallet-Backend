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
        self.r_to_invitation_url = reverse('respond_to_invitation')
        self.event_list_url = reverse('get_events')
        self.create_activity_url = reverse('create_activity')
        self.create_invitation_activity_url = reverse('create_invitation_activity')
        self.activity_delete = reverse('delete_activity')
        
        self.user1_data ={
            "nombre": "prueba1",
            "apellidos": "prueba1",
            "apodo":"test1",
            "password": "1234",
            "email": "test@test.com"        
        }

        self.user2_data ={
            "nombre": "prueba2",
            "apellidos": "prueba2",
            "apodo":"test2",
            "password": "1234",
            "email": "test2@test.com"        
        }

        self.login_user1 = {
            "username":"test@test.com",
            "password":"1234"
        }

        self.login_user2 = {
            "username":"test2@test.com",
            "password":"1234"
        }

        self.user1_modified_data = {
            "nombre": "prueba1mod",
            "apellidos": "prueba1mod",
            "apodo": "test1mod"
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
        }
        
        self.event_modified_data={
            "evento_id": None,
            "nombre": "samplename",
            "descripcion":"sampledescription",
            "tipo":"O"
        }
        
        self.invitation_data={
            "evento_id": None,
            "email": None
        }

        self.respond_invitation_data = {
            "invitacion_id":None,
            "respuesta": False
        }

        self.create_activity_data={
            "evento": None,
            "nombre": "samplename",
            "descripcion":"sampledescription",
            "valor": 12345
        }

        self.create_invitation_activity_data={
            "actividad": None,
            "participante" : None
        }

        self.delete_activity_data = {
            "actividad_id": None
        }
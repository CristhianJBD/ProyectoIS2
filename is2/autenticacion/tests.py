from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test import Client
# Create your tests here.


class test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
        """
         200 códigos de estado de la respuesta
        :return:
        """
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertNotAlmostEquals(response.status_code, 301)

    def test_loggedin(self):
        """
        301 Movido permanentemente se utiliza para el permanente cambio de dirección URL
        :return:
        """
        u = User()
        u.username = 'admin'
        u.set_password('adminadmin')
        u.is_active = True
        u.save()
        self.client.post('/login/', {'username': 'admin', 'password': 'adminadmin'})
        response = self.client.get('/loggedin/')
        self.assertEquals(response.status_code, 301)

    def test_invalid(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'adminadmin'})
        self.assertEquals(response.status_code, 200)

    def test_ver_loginPage(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'autenticacion/login_view.html')

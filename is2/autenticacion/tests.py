from django.test import TestCase, RequestFactory
from django.test import Client
# Create your tests here.


class test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
        """
         el test muestra que al dirigir a la pagina login, este envia un response, con codigo
         200, que significa que la pagina cargo correctamente
        """
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertNotAlmostEquals(response.status_code, 301)


    def test_ver_loginPage(self):
        """
         el test muestra que al dirigir a la pagina login, este envia un response, con el template
        """
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'autenticacion/login_view.html')


    def test_logout(self):
         """
        indica que que la redireccion es temporal por lo tanto envia un codigo 302
        """
         resp = self.client.get('/logout/')
         self.assertEqual(resp.status_code, 302)


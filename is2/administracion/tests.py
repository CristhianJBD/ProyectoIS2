from django.contrib.auth.models import User, Permission, Group
from django.db.models.expressions import Date
from django.db.models.fields import DateTimeField
from django.test import TestCase
from django.utils import timezone

from administracion.models import Proyecto


class RoleTest(TestCase):
    def setUp(self):
        u = User.objects.create_user('admin','admin@gmail.com','admin')
        u.user_permissions.add(Permission.objects.get(codename='add_group'))
        u.user_permissions.add(Permission.objects.get(codename='change_group'))
        u.user_permissions.add(Permission.objects.get(codename='delete_group'))


    def create_role(self, name):
        g = Group.objects.create(name=name)
        g.save()
        return g


    def test_create_role(self):
        c = self.client
        self.assertTrue(c.login(username='admin', password='admin'))
        response = c.get('/roles/add/');
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a roles/add')
        #intentamos crear un rol developer que pueda crear, editar y borrar proyectos
        response = c.post('/roles/add/', {'name':'scrum', 'perms_proyecto':[u'add_proyecto', u'change_proyecto', u'delete_proyecto']}, follow=True)
        #deberia redirigir
        self.assertRedirects(response, '/roles/1/')


    def test_delete_role(self):
        c = self.client
        self.assertTrue(c.login(username='admin', password='admin'))
        response = c.post('/roles/add/', {'name':'developer', 'perms_proyecto':[u'add_proyecto', u'change_proyecto', u'delete_proyecto']}, follow=True)
        #deberia redirigir
        self.assertRedirects(response, '/roles/2/')
        #eliminamos el rol
        response = c.post('/roles/2/delete/', {'Confirmar':True}, follow=True)
        self.assertRedirects(response, '/roles/')
        #ahora ya no deberia existir el registro
        response = c.get('/roles/2/')
        self.assertEquals(response.status_code, 404)





class UserTest(TestCase):
    def setUp(self):
        u = User.objects.create_user('temp','temp@email.com', 'temp')
        p = Permission.objects.get(codename='add_user')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='change_user')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='delete_user')
        u.user_permissions.add(p)
        u = User.objects.create_user('fulano','temp@email.com', 'temp')

    def create_role(self, name):
        g = Group.objects.create(name=name)
        g.save()
        return g

    def test_create_user(self):
        c = self.client
        self.assertTrue(c.login(username='temp', password='temp'))
        response = c.get('/users/add/')
        self.assertEquals(response.status_code, 200)
        #intentamos crear un rol developer que pueda crear, editar y borrar proyectos, y crear y borrar US
        response = c.post('/users/add/', {'first_name': 'John', 'last_name': 'Doe', 'username':'john', 'email': 'john@doe.com', 'password1': 'adminadmin', 'password2': 'adminadmin'}, follow=True)
        u = User.objects.get(username='john')
        #comprobamos que exista el usuario
        self.assertIsNotNone(u)
        #deberia redirigir
        self.assertRedirects(response, '/{}'.format(u.id))


    def test_edit_user(self):
        c = self.client
        self.assertTrue(c.login(username='temp', password='temp'))
        u = User.objects.get(username='fulano')
        self.assertIsNotNone(u)
        response = c.get('/users/{}/edit/'.format(u.id))
        self.assertEquals(response.status_code, 200)
        #modificamos el nombre
        response = c.post('/users/{}/edit/'.format(u.id), {'username':'melgano', 'email': 'asd@asd.com'}, follow=True)
        #deberia redirigir
        self.assertRedirects(response, '/{}'.format(u.id))
        #comprobamos el cambio en la bd
        self.assertIsNotNone(User.objects.get(username='melgano'))

    def test_delete_user(self):
        c = self.client
        self.assertTrue(c.login(username='temp', password='temp'))
        #vemos que el usuario existe
        u = User.objects.get(username='fulano')
        self.assertIsNotNone(u)
        #eliminamos el user
        response = c.post('/users/{}/delete/'.format(u.id), {'Confirmar':True}, follow=True)
        self.assertRedirects(response, '/users/')
        #ahora ya no deberia estar activo el usuario
        response = c.get('/users/{}/'.format(u.id))
        self.assertEquals(response.status_code, 404)
        u = User.objects.get(pk=u.id)
        self.assertIsNotNone(u)
        self.assertFalse(u.is_active)





class ProjectTest(TestCase):

    def setUp(self):
        u = User.objects.create_superuser('temp','temp@email.com', 'temp')
        p = Permission.objects.get(codename='add_proyecto')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='change_proyecto')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='delete_proyecto')
        u.user_permissions.add(p)
        u = User.objects.create_user('fulano','temp@email.com', 'temp')

    def test_permission_to_create_proyecto(self):
        c = self.client
        self.assertTrue(c.login(username='temp', password='temp'))
        response = c.get('/proyecto/agregar/')
        self.assertEquals(response.status_code, 200)

    def test_not_permission_to_create_proyecto(self):
        c = self.client
        self.assertTrue(c.login(username='fulano', password='temp'))
        response = c.get('/proyecto/agregar/')
        self.assertEquals(response.status_code, 403)




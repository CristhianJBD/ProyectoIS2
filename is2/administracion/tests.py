from django.contrib.auth.models import User, Permission, Group
from django.db.models.expressions import Date
from django.db.models.fields import DateTimeField
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from administracion.models import Proyecto, Flujo, UserStory, Actividad, Sprint


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
        self.assertRedirects(response, '/roles/')


    def test_delete_role(self):
        c = self.client
        self.assertTrue(c.login(username='admin', password='admin'))
        response = c.post('/roles/add/', {'name':'developer', 'perms_proyecto':[u'add_proyecto', u'change_proyecto', u'delete_proyecto']}, follow=True)
        #deberia redirigir
        self.assertRedirects(response, '/roles/')
        #eliminamos el rol
        response = c.post('/roles/2/delete/', {'Confirmar':True}, follow=True)
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
        response = c.get('/proyectos/agregar/')
        self.assertEquals(response.status_code, 200)

    def test_not_permission_to_create_proyecto(self):
        c = self.client
        self.assertTrue(c.login(username='fulano', password='temp'))
        response = c.get('/proyectos/agregar/')
        self.assertEquals(response.status_code, 403)


class FlujoTest(TestCase):

    def setUp(self):
        u = User.objects.create_superuser('test', 'temp@email.com', 'test')
        p = Permission.objects.get(codename='crear_flujo')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='editar_flujo')
        u.user_permissions.add(p)
        p = Permission.objects.get(codename='eliminar_flujo')
        u.user_permissions.add(p)
        u1 = User.objects.create_user('fulano','temp@email.com', 'temp')
        pro= Proyecto.objects.create(nombre='Proyecto', estado='PE', fecha_inicio=timezone.now(), fecha_fin=timezone.now() + datetime.timedelta(days=30))
        f = Flujo.objects.create(nombre='Flujo1', proyecto=pro)
        Group.objects.create(name='rol')


    def test_permission_to_create_flujo(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #deberia existir
        self.assertIsNotNone(p)
        response = c.get(reverse('flujo_add', args=(str(p.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a agregar flujo')

    def test_not_permission_to_create_flujo(self):
        c = self.client
        login = c.login(username='fulano', password='temp')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #deberia existir
        self.assertIsNotNone(p)
        response = c.get(reverse('flujo_add', args=(str(p.id))))
        self.assertEquals(response.status_code, 403)


    def test_permission_to_change_flujo(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        f = Flujo.objects.first()
        #deberia existir
        self.assertIsNotNone(f)
        response = c.get(reverse('flujo_update', args=(str(f.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a editar flujo')

    def test_not_permission_to_change_flujo(self):
        c = self.client
        login = c.login(username='fulano', password='temp')
        self.assertTrue(login)
        f = Flujo.objects.first()
        #deberia existir
        self.assertIsNotNone(f)
        response = c.get(reverse('flujo_update', args=(str(f.id))))
        self.assertEquals(response.status_code, 403)




class UserStoryTest(TestCase):
    def setUp(self):
        u = User.objects.create_superuser('test', 'test@test.com', 'test') #Superusuario con todos los permisos
        u2 = User.objects.create_user('none', 'none@none.com', 'none') #Usuario sin permisos
        pro= Proyecto.objects.create(nombre='Proyecto', estado='PE', fecha_inicio=timezone.now(), fecha_fin=timezone.now() + datetime.timedelta(days=30))

    def test_add_userstory_with_permission(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #deberia existir
        self.assertIsNotNone(p)
        response = c.get(reverse('userstory_add', args=(str(p.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a Agreagar detail')
        response = c.post(reverse('userstory_add', args=(str(p.id))),
            {'nombre_corto': 'Test US', 'nombre_largo': 'Test User story', 'descripcion': 'This is a User Story for testing purposes.','prioridad':1,
             'valor_negocio': 10, 'valor_tecnico': 10, 'tiempo_estimado': 10}, follow=True)
        #deberia redirigir
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        self.assertRedirects(response, '/userstory/{}/'.format(us.id))
        response = c.get(reverse('userstory_detail', args=(str(us.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a userstory detail')


    def test_update_userstory_with_permission(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #creamos un user story
        response = c.post(reverse('userstory_add', args=(str(p.id))),
        {'nombre_corto': 'Test US', 'nombre_largo': 'Test User story', 'descripcion': 'This is a User Story for testing purposes.', 'prioridad':1,
        'valor_negocio': 10, 'valor_tecnico': 10, 'tiempo_estimado': 10}, follow=True)
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        self.assertEquals(us.nombre_corto, 'Test US')
        response = c.get(reverse('userstory_detail', args=(str(us.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a userstory detail')
        #nos vamos a la página de edición de user story
        response = c.get(reverse('userstory_update', args=(str(us.id))))
        #debería retornar 200
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a editar user Story')
        response = c.post(reverse('userstory_update', args=(str(us.id))),
         {'nombre_corto': 'Test US2', 'nombre_largo': 'Test User story2', 'descripcion': 'This is a User Story2 for testing purposes.','prioridad':1,
        'valor_negocio': 10, 'valor_tecnico': 10, 'tiempo_estimado': 10}, follow=True)
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        #vemos que el nombre ya no es el anterior
        self.assertNotEquals(us.nombre_corto, 'Test US')
        self.assertEquals(us.nombre_corto, 'Test US2')


    def test_registraractividad_userstory_with_permission(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #creamos un user story
        response = c.post(reverse('userstory_add', args=(str(p.id))),
            {'nombre_corto':'First Value US', 'nombre_largo': 'Test User story', 'descripcion':'This is a User Story for testing purposes.', 'prioridad': 1,
             'valor_negocio': 10, 'valor_tecnico': 10, 'tiempo_estimado': 10}, follow=True)
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a agregar user Story')
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        self.assertEquals(us.nombre_corto, 'First Value US')
        s = Sprint.objects.create(nombre="Sprint 1", fecha_inicio=timezone.now(), fecha_fin=timezone.now() + datetime.timedelta(days=30), proyecto=p)
        f = Flujo.objects.create(nombre="Desarrollo", proyecto=p)
        a1 = Actividad.objects.create(nombre="Analisis", flujo=f)
        a2 = Actividad.objects.create(nombre="Diseno", flujo=f)
        us.actividad = a2
        us.estado = 1 #Estado en curso
        us.sprint = s
        us.desarrollador = p.equipo.first()
        us.save()
        response = c.get(reverse('userstory_detail', args=(str(us.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a userstory detail')
        #nos vamos a la página de registrar actividad de user story
        response = c.get(reverse('userstory_registraractividad', args=(str(us.id))))
        #debería retornar 200
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a registrar actividad user story')

        post_data = {
            'horas_a_registrar': 4,
            'actividad': 1,
            'estado_actividad':1,
            'form-INITIAL_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-MIN_NUM_FORMS': 0,
            'form-TOTAL_FORMS': 1,
        }
        response = c.post(reverse('userstory_registraractividad', args=(str(us.id))), post_data, follow=True)
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a registrar actividad user story' )


    def test_list_userstories_with_permission(self):
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        p = Proyecto.objects.first()
        #listamos user stories del proyecto
        response = c.get(reverse('product_backlog', args=(str(p.id))))
        self.assertEquals(response.status_code, 200, 'No se pudo redirigir correctamente a registrar actividad user story')


class SprintTest(TestCase):

    def setUp(self):
        u = User.objects.create_superuser('temp','temp@email.com', 'temp')
        pro = Proyecto.objects.create(nombre='Proyecto', estado='PE', fecha_inicio=timezone.now(), fecha_fin=timezone.now() + datetime.timedelta(days=30))
        User.objects.create_user('tempdos', 'tempdos@email.com', 'tempdos')
        UserStory.objects.create(nombre_corto= 'Test_Version',nombre_largo= 'Test_Version', descripcion= 'Test Description',
                       valor_negocio= 10, valor_tecnico = 10, tiempo_estimado = 10, proyecto = pro)
        f = Flujo.objects.create(nombre ='flujo_test', proyecto= pro)
        Actividad.objects.create(nombre ='actividad_test', flujo=f)
        Sprint.objects.create(nombre='sprint_test',fecha_inicio=timezone.now(),fecha_fin=timezone.now(), proyecto=pro)

    def test_to_create_sprint(self):
        c = self.client
        self.assertTrue(c.login(username='temp', password='temp'))
        p = Proyecto.objects.first()
        self.assertIsNotNone(p)
        us = UserStory.objects.first()
        self.assertIsNotNone(us)
        d = User.objects.first()
        self.assertIsNotNone(d)
        f = User.objects.first()
        self.assertIsNotNone(f)
        response = c.get(reverse('sprint_add', args=(str(p.id))))
        self.assertEquals(response.status_code, 200)
        post_data = {
        'nombre': 'Sprint_test',
        'fecha_inicio': timezone.now(),
        'proyecto':p,
        'fecha_fin':timezone.now(),
        'actividad': 1,
        'tiempo_registrado': 4,
        'estado_actividad': 1,
        'form-INITIAL_FORMS': 0,
        'form-MAX_NUM_FORMS': 1000,
        'form-MIN_NUM_FORMS': 0,
        'form-TOTAL_FORMS': 1,
        'form-0-userStory': us.id,
        'form-0-desarrollador':d.id,
        'form-0-flujo':f.id,
    }
        response = c.post(reverse('sprint_add', args=(str(p.id))), post_data, follow=True)
        self.assertEquals(response.status_code,200)
        s=Sprint.objects.first()
        self.assertIsNotNone(s)


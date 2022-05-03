from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from .models import jsonData, toggled_classes, classes, Location


class PracticeTests(TestCase):

    def test_practice(self):
        self.assertIs(True, True)

# tests for signing in were based on the following tutorial https://mkdev.me/en/posts/how-to-cover-django-application-with-unit-tests
class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@tst.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='test')
        self.assertTrue((user is not None) and user.is_authenticated)

class AddClassTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.client.login(username='test', password='test')
        data = jsonData(label="classes")
        data.save()

    def tearDown(self):
        self.user.delete()

    def test_add_real_class(self):
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_fake_class(self):
        title = 'Not a Class'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, 'You do not have any classes added')

class RemoveClassTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.client.login(username='test', password='test')
        data = jsonData(label="classes")
        data.save()
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title':title})

    def tearDown(self):
        self.user.delete()

    def test_remove_class(self):
        title = 'CS 3240'
        self.client.post(reverse('remove'), {'choice':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, 'You do not have any classes added')

class ToggleClassTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.client.login(username='test', password='test')
        data = jsonData(label="classes")
        data.save()

    def tearDown(self):
        self.user.delete()

    def test_add_real_class(self):
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 3102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_toggle_real_class(self):
        choice = ['CS 3240', 'CS 3102']
        self.client.post(reverse('toggle'),{'choice':choice})
        qs = toggled_classes.objects.all()
        self.assertQuerysetEqual(list(qs),['<toggled_classes: CS 3240>', '<toggled_classes: CS 3102>'])



class UntoggleClassTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.client.login(username='test', password='test')
        data = jsonData(label="classes")
        data.save()

    def tearDown(self):
        self.user.delete()

    def test_add_real_class1(self):
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class2(self):
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class3(self):
        title = 'CS 3102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class4(self):
        title = 'CS 9999'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class5(self):
        title = 'CS 4414'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('classes_view')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_toggleuntoggle_real_class(self):
        choice = ['CS 3240', 'CS 3102', 'CS 4414']
        self.client.post(reverse('toggle'),{'choice':choice})
        qs = toggled_classes.objects.all()
        self.assertQuerysetEqual(list(qs),['<toggled_classes: CS 3240>', '<toggled_classes: CS 3102>', '<toggled_classes: CS 4414>'])

        choice2 = ['CS 3240']
        response1 = self.client.post(reverse('toggle'), {'choice': choice2})
        self.assertContains(response1, 'One or more of these classes has already been toggled.')

        choice3 = ['CS 4414', 'CS 3102']
        response2 = self.client.post(reverse('toggle'), {'choice': choice3})
        self.assertContains(response2, 'One or more of these classes has already been toggled.')

        choice4 = []
        response3 = self.client.post(reverse('toggle'), {'choice': choice4})
        self.assertContains(response3, 'You did not select a class.')

        choice5 = ['CS 3102', 'CS 4414']
        self.client.post(reverse('untoggle'),{'choice':choice5})
        qs1 = toggled_classes.objects.all()
        self.assertQuerysetEqual(list(qs1),['<toggled_classes: CS 3240>'])

        choice6 = []
        response4 = self.client.post(reverse('untoggle'), {'choice': choice6})
        self.assertContains(response4, 'You did not select a class.')


class MatchingTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='test1', password='test1', email='t1@st.com')
        self.user.save()
        data = jsonData(label="classes")
        data.save()

    def tearDown(self):
        self.user.delete()

    def test_match_with_similar_person(self):
        self.client.login(username='test', password='test')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test', 'year': '3', 'match_students': ""})

        self.client.login(username='test1', password='test1')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test1', 'year': '3', 'match_students': ""})

        url = reverse('matching')
        response = self.client.get(url)
        self.assertContains(response, 'test')

    def test_match_with_most_similar_person(self):
        self.user = get_user_model().objects.create_user(username='test2', password='test2', email='t2@st.com')
        self.user.save()
        self.client.login(username='test', password='test')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test', 'year': '3', 'match_students': ""})

        self.client.login(username='test1', password='test1')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        choice = ['CS 4102']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test1', 'year': '3', 'match_students': ""})

        self.client.login(username='test2', password='test2')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        choice = ['CS 4102']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test1', 'year': '3', 'match_students': ""})

        url = reverse('matching')
        response = self.client.get(url)
        self.assertContains(response, 'test1')


class LocationsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', email='t@st.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='test1', password='test1', email='t1@st.com')
        self.user.save()

    
    def tearDown(self):
        self.user.delete()

    def test_add_studdy_session(self):
        self.client.login(username='test', password='test')
        usera = self.user

        self.client.login(username='test1', password='test1')
        userb = self.user

        l = Location(location='38.038903204641144,-78.51953506456474',
                     address='104 Midmont Lane, Charlottesville, Virginia 22903, United States', date='2022-10-10',
                     time='22:10:00')
        l.save()
        l.users.add(usera)
        l.users.add(userb)

        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, 'test')

    def test_remove_studdy_session(self):
        self.client.login(username='test', password='test')
        usera = self.user

        self.client.login(username='test1', password='test1')
        userb = self.user

        l = Location(location='38.038903204641144,-78.51953506456474',
                     address='104 Midmont Lane, Charlottesville, Virginia 22903, United States', date='2022-10-10',
                     time='22:10:00')
        l.save()
        l.users.add(usera)
        l.users.add(userb)

        url = reverse('remove', args=[l.id])
        self.client.get(url)
        url = reverse('index')
        response = self.client.get(url)

        self.assertContains(response, 'You do not have any sessions scheduled')
    
    def test_delete_studdy_session(self):
        self.client.login(username='test', password='test')
        usera = self.user

        self.client.login(username='test1', password='test1')
        userb = self.user

        l = Location(location='38.038903204641144,-78.51953506456474',
                     address='104 Midmont Lane, Charlottesville, Virginia 22903, United States', date='2022-10-10',
                     time='22:10:00')
        l.save()
        l.users.add(usera)
        l.users.add(userb)

        url = reverse('delete', args=[l.pk])
        self.client.get(url)

        self.client.login(username='test', password='test')
        url = reverse('index')
        response = self.client.get(url)

        self.assertContains(response, 'You do not have any sessions scheduled')

    def test_edit_studdy_session(self):
        data = jsonData(label="classes")
        data.save()
        self.client.login(username='test', password='test')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test', 'year': '3', 'match_students': ""})

        self.client.login(username='test1', password='test1')
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title': title})
        choice = ['CS 3240']
        self.client.post(reverse('toggle'), {'choice': choice})
        self.client.post(reverse('info_submit'),
                         {'major': 'Computer Science', 'seriousness': "9", 'name': 'test1', 'year': '3', 'match_students': ""})

        url = reverse('matching')
        response = self.client.get(url)

        self.client.login(username='test', password='test')
        usera = self.user

        self.client.login(username='test1', password='test1')
        userb = self.user

        l = Location(location='38.038903204641144,-78.51953506456474',
                     address='104 Midmont Lane, Charlottesville, Virginia 22903, United States', date='2022-10-10',
                     time='22:10:00')
        l.save()
        l.users.add(usera)
        l.users.add(userb)

        url = reverse('update', args=[l.pk])
        response = self.client.get(url)
        self.assertContains(response, 'test')
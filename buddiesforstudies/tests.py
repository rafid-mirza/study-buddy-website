from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from .models import jsonData, toggled_classes, classes, Room


class PracticeTests(TestCase):

    def test_practice(self):
        self.assertIs(True, True)

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
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'Not a Class'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
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
        url = reverse('index')
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
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 3102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
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

    def test_add_real_class(self):
        title = 'CS 3240'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 4102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 3102'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 9999'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, title)

    def test_add_real_class(self):
        title = 'CS 4414'
        self.client.post(reverse('submit'), {'title':title})
        url = reverse('index')
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

class HomePageTest(TestCase):
    def test_all_rooms_are_rendered_in_homepage(self):
        Room.objects.create(
            name='room 1',
            slug='room-1',
            description='This is the 1st room'
        )
        Room.objects.create(
            name='room 2',
            slug='room-2',
            description='This is the 2nd room'
        )

        response = self.client.get('/buddiesforstudies/rooms/')

        self.assertContains(response, 'room 1')
        self.assertContains(response, 'room 2')


class RoomDetailTest(TestCase):

    def test_room_details_are_present_in_room_page(self):
        room_1 = Room.objects.create(
            name='room X',
            slug='room-x',
            description='This is the X-room'
        )

        response = self.client.get('/buddiesforstudies/rooms/{}/'.format(room_1.slug))

        self.assertContains(response, room_1.name)
        self.assertContains(response, room_1.description)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import Restaurant
from booking.models import Booking
from datetime import date, timedelta
from django.contrib.messages import get_messages


class TestCreateBookingView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="123 Street",
            city="Town",
            phone_number="123456789",
            online_capacity=4,
        )

        self.booking_date = date.today() + timedelta(days=1)

    def test_create_booking_get_page(self):
        """
        GET request should return the booking form page with correct context.
        """
        response = self.client.get(reverse(
            'create_booking', args=[self.restaurant.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/create_booking.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)

    def test_create_booking_post_success(self):
        """
        Valid POST should create booking and redirect with success message.
        """
        data = {
            'booking_date': self.booking_date,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 2,
            'special_requests': 'Birthday'
        }
        response = self.client.post(
            reverse('create_booking', args=[self.restaurant.slug]),
            data
        )
        self.assertRedirects(response, reverse('my_bookings'))
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.number_of_people, 2)
        self.assertEqual(booking.restaurant, self.restaurant)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "created successfully" in str(m) for m in messages)
        )

    def test_create_booking_over_capacity(self):
        """Booking more people than restaurant capacity should fail."""
        # Restaurant capacity = 4
        Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=3
        )
        data = {
            'booking_date': self.booking_date,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 2,
            'special_requests': ''
        }
        response = self.client.post(
            reverse('create_booking', args=[self.restaurant.slug]),
            data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "capacity limits",
            response.context['form'].errors['number_of_people'][0]
        )

    def test_create_booking_double_booking(self):
        """User cannot book same restaurant/date/time twice."""
        Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2
        )
        data = {
            'booking_date': self.booking_date,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 1
        }
        response = self.client.post(
            reverse('create_booking', args=[self.restaurant.slug]),
            data
        )
        self.assertFormError(
            response,
            'form',
            'time_slot',
            "You already have a booking for this restaurant "
            "at the selected date and time."
        )

    def test_create_booking_invalid_date(self):
        """Booking with today and past date should fail."""
        data = {
            'booking_date': date.today(),
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 2
        }
        response = self.client.post(
            reverse('create_booking', args=[self.restaurant.slug]),
            data
        )
        self.assertFalse(response.context['form'].is_valid())

    def test_create_booking_not_logged_in(self):
        """Anonymous users should be redirected to login page."""
        self.client.logout()
        response = self.client.get(
            reverse('create_booking', args=[self.restaurant.slug])
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/booking/{self.restaurant.slug}/book/"
        )

    def test_user_can_book_again_after_cancellation(self):
        """ User should be able to rebook after cancellation. """
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2,
            status=1
        )
        self.booking.status = 2
        self.booking.save()

        response = self.client.post(
            reverse('create_booking', args=[self.restaurant.slug]),
            {
                'booking_date': self.booking_date,
                'time_slot': '12:00 PM - 1:30 PM',
                "number_of_people": 2,
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        new_booking = Booking.objects.filter(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2,
            status=1
        ).exists()

        self.assertTrue(new_booking,
                        "User should be able to rebook after cancellation.")


class TestMyBookings(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="123 Street",
            city="Town",
            phone_number="123456789",
            online_capacity=4,
        )

        self.future_date = date.today() + timedelta(days=1)
        self.past_date = date.today() - timedelta(days=1)

        # active booking in the future
        self.future_booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.future_date,
            time_slot="12:00 PM - 1:30 PM",
            number_of_people=2,
            status=1  # Active
        )

        # Active booking in the past
        self.past_booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.past_date,
            time_slot="12:00 PM - 1:30 PM",
            number_of_people=3,
            status=1  # Active initially
        )

    def test_my_bookings_page_loads(self):
        """ Dashboard should load correctly with all bookings. """
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booking/my_bookings.html")
        self.assertIn("bookings", response.context)

    def test_past_bookings_marked_completed(self):
        """
        Past booking should be automatically marked as comleted / status=3.
        """
        self.client.get(reverse('my_bookings'))
        self.past_booking.refresh_from_db()
        self.assertEqual(self.past_booking.status, 3)

    def test_future_bookings_remains_active(self):
        """ Future bookings should remain active/ status=1."""
        self.client.get(reverse('my_bookings'))
        self.future_booking.refresh_from_db()
        self.assertEqual(self.future_booking.status, 1)

    def test_user_only_sees_own_bookings(self):
        """ User should only see their own bookings on dashboard. """
        other_user = User.objects.create_user(
            username="other",
            password="password"
        )
        Booking.objects.create(
            user=other_user,
            restaurant=self.restaurant,
            booking_date=self.future_date,
            time_slot="12:00 PM - 1:30 PM",
            number_of_people=1,
            status=1
        )

        response = self.client.get(reverse('my_bookings'))
        bookings = response.context["bookings"]

        self.assertTrue(all(b.user == self.user for b in bookings))


class TestEditBooking(TestCase):

    def setUp(self):
        # Create user and login
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        # create restaurant
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="123 Street",
            city="Town",
            phone_number="123456789",
            online_capacity=4
        )

        # create a booking
        self.booking_date = date.today() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2,
            status=1
        )

        # store edit_booking URL for reuse
        self.url = reverse('edit_booking', args=[self.booking.pk])

    def test_edit_booking_get_redirects(self):
        """
        GET request should redirect to my_bookings
        (since form in inline).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_bookings'))

    def test_edit_booking_post_success(self):
        """ POST with valid number_of_people should update booking. """
        response = self.client.post(
            self.url,
            {'number_of_people': 4},
            follow=True
        )
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.number_of_people, 4)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "updated successfully" in str(m) for m in messages
            )
        )

    def test_edit_booking_over_capacity(self):
        """ POST exceeding restaurant capacity should show error. """
        other_user = User.objects.create_user(
            username="other",
            password="password"
        )
        Booking.objects.create(
            user=other_user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2,
            status=1
        )

        response = self.client.post(self.url,
                                    {'number_of_people': 3},
                                    follow=True
                                    )
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.number_of_people, 2)

        messages = list(response.context['messages'])
        self.assertTrue(any(
            "Cannot update booking due to capacity" in str(m) for m in messages
            )
        )


class TestCancelBooking(TestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        # create restaurant
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="123 Street",
            city="Town",
            phone_number="123456789",
            online_capacity=4
        )

        # create a booking
        self.booking_date = date.today() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot='12:00 PM - 1:30 PM',
            number_of_people=2,
            status=1
        )

        # store edit_booking URL for reuse
        self.url = reverse('cancel_booking', args=[self.booking.pk])

    def test_cancel_booking_success(self):
        """
        Cancelling own booking sets status to 'Cancelled'
        and shows a success message.
        """
        response = self.client.post(self.url, follow=True)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 2)
        self.assertRedirects(response, reverse('my_bookings'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("cancelled" in str(m) for m in messages))

    def test_cancel_booking_other_user(self):
        """
        User cannot cancel another user’s booking;
        booking remains unchanged and 404 returned.
        """
        other_booking = Booking.objects.create(
            user=self.other_user,
            restaurant=self.restaurant,
            booking_date=self.booking_date,
            time_slot="12:00 PM - 1:30 PM",
            number_of_people=1,
            status=1
        )
        url = reverse('cancel_booking', args=[other_booking.pk])
        response = self.client.post(url, follow=True)

        other_booking.refresh_from_db()
        self.assertEqual(other_booking.status, 1)
        self.assertEqual(response.status_code, 404)

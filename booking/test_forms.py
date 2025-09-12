from django.test import TestCase
from datetime import date, timedelta
from .forms import BookingForm, EditBookingForm


class TestBookingForm(TestCase):
    def test_form_is_valid(self):
        tomorrow = date.today() + timedelta(days=1)
        booking_form = BookingForm({
            'booking_date': tomorrow,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 3,
            'special_requests': 'Birthday party'
            })
        self.assertTrue(booking_form.is_valid(), msg='Form is not valid')

    def test_form_is_valid_with_empty_special_requests(self):
        tomorrow = date.today() + timedelta(days=1)
        booking_form = BookingForm({
            'booking_date': tomorrow,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 6,
            'special_requests': ''
        })
        self.assertTrue(booking_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid_with_past_booking_date(self):
        booking_form = BookingForm({
            'booking_date': date.today(),
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 2,
            'special_requests': ''
            })
        self.assertFalse(booking_form.is_valid(), msg='Form is valid')

    def test_form_is_invalid_on_first_dissalowed_day(self):
        day_after = date.today() + timedelta(days=181)
        booking_form = BookingForm({
            'booking_date': day_after,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 4,
            'special_requests': ''
            })
        self.assertFalse(booking_form.is_valid(), msg='Form is valid')

    def test_form_is_valid_on_last_allowed_day(self):
        last_day = date.today() + timedelta(days=180)
        booking_form = BookingForm({
            'booking_date': last_day,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 5,
            'special_requests': ''
            })
        self.assertTrue(booking_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid_with_less_than_one_people(self):
        last_day = date.today() + timedelta(days=180)
        booking_form = BookingForm({
            'booking_date': last_day,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 0,
            'special_requests': ''
            })
        self.assertFalse(booking_form.is_valid(), msg='Form is valid')

    def test_form_is_invalid_with_more_than_six_people(self):
        last_day = date.today() + timedelta(days=180)
        booking_form = BookingForm({
            'booking_date': last_day,
            'time_slot': '12:00 PM - 1:30 PM',
            'number_of_people': 7,
            'special_requests': ''
            })
        self.assertFalse(booking_form.is_valid(), msg='Form is valid')

    def test_form_is_invalid_with_missing_fields(self):
        booking_form = BookingForm({'number_of_people': 5})
        self.assertFalse(booking_form.is_valid(), msg='Form is valid')
        self.assertIn('booking_date', booking_form.errors)
        self.assertIn('time_slot', booking_form.errors)


class TestEditBookingForm(TestCase):
    def test_form_is_invalid_with_less_than_one_people(self):
        edit_form = EditBookingForm({
            'number_of_people': 0,
            })
        self.assertFalse(edit_form.is_valid(), msg='Form is valid')
  
    def test_form_is_invalid_with_more_than_six_people(self):
        edit_form = EditBookingForm({
            'number_of_people': 7,
            })
        self.assertFalse(edit_form.is_valid(), msg='Form is valid')

    def test_form_is_valid_with_range(self):
        edit_form = EditBookingForm({
            'number_of_people': 5,
            })
        self.assertTrue(edit_form.is_valid(), msg='Form is not valid')

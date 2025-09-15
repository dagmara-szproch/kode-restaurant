from django.urls import reverse
from django.test import TestCase
from .models import Restaurant, RestaurantCarouselImage


class TestRestaurantViews(TestCase):
    """ Tests for restaurant views: home + detail."""

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="Restaurant address",
            city="Restaurant city",
            phone_number="123456789",
            email="test@example.com",
            description="Test place"
        )

        # Carousel image
        self.image1 = RestaurantCarouselImage.objects.create(
            restaurant=self.restaurant,
            image="carousel/test1.webp",
            caption="First slide",
            order=0
        )

        self.image2 = RestaurantCarouselImage.objects.create(
            restaurant=self.restaurant,
            image="carousel/test2.webp",
            caption="Second slide",
            order=1
        )

    def test_home_view_renders_correct_template(self):
        """ Home view should render the first restaurant detail page. """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')
        self.assertContains(response, "Test Bistro")
        self.assertContains(response, "Test place")
        self.assertContains(response, "Restaurant address")
        self.assertContains(response, "Restaurant city")

    def test_home_view_context_includes_restaurant_and_carousel(self):
        """ Home view context should include restaurant and carousel images """
        response = self.client.get(reverse('home'))
        self.assertIn('restaurant', response.context)
        self.assertIn('carousel_images', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertListEqual(list(response.context['carousel_images']),
                              [self.image1, self.image2])
        
    def test_restaurant_detail_view_with_valid_slug(self):
        """ Restaurant detail page loads correctly for a valid slug. """
        response = self.client.get(reverse('restaurant_detail', args=['test-bistro']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')
        self.assertContains(response, "Test Bistro")
        self.assertContains(response, "Restaurant address")
        self.assertContains(response, "Restaurant city")
        self.assertContains(response, "Test place")

    def test_restaurant_detail_view_context_include_carousel(self):
        """ Restaurant detail context should include carousel images. """
        response = self.client.get(reverse('restaurant_detail', args=['test-bistro']))
        self.assertIn('restaurant', response.context)
        self.assertIn('carousel_images', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertListEqual(
            list(response.context['carousel_images']), [self.image1, self.image2])

    def test_restaurant_detail_view_Invalid_slug(self):
        """ Restaurant detail page should return 404 for invalid slug. """
        response = self.client.get(reverse('restaurant_detail', args=['non-slug']))
        self.assertEqual(response.status_code, 404)


class TestRestaurantModels(TestCase):
    """ Tests for Restaurant and CarouselImage models. """
    
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            address="123 High Street",
            city="London",
            phone_number="0123456789",
            email="test@example.com",
            description="Nice test place"
        )

        self.carousel1 = RestaurantCarouselImage.objects.create(
            restaurant=self.restaurant,
            image="carousel/test1.webp",
            caption="Front view",
            order=0
        )

        self.carousel2 = RestaurantCarouselImage.objects.create(
            restaurant=self.restaurant,
            image="carousel/test2.webp",
            caption="Back view",
            order=1
        )

    def test_restaurant_defaults(self):
        """Check default capacities for online and walk-in seats."""
        self.assertEqual(self.restaurant.online_capacity, 50)
        self.assertEqual(self.restaurant.table_capacity, 80)
        self.assertEqual(self.restaurant.table_capacity - self.restaurant.online_capacity, 30)

    def test_restaurant_str(self):
        """Check __str__ returns the restaurant name."""
        self.assertEqual(str(self.restaurant), "Test Bistro")

    def test_carousel_str(self):
        """Check __str__ returns a descriptive string for carousel images."""
        self.assertEqual(str(self.carousel1), "Test Bistro - Image0")
        self.assertEqual(str(self.carousel2), "Test Bistro - Image1")

from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, MenuItem, Cart, Order, OrderItem, Rating

# ---------------------------------------------------------------------------
# Shared settings overrides
# ---------------------------------------------------------------------------

NO_THROTTLE = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_category(title='Sandwiches', slug='sandwiches'):
    return Category.objects.create(title=title, slug=slug)


def make_menu_item(category, title='Reuben', price='13.99',
                   is_vegetarian=False, is_vegan=False):
    return MenuItem.objects.create(
        title=title,
        description='A classic deli sandwich',
        price=Decimal(price),
        inventory=50,
        category=category,
        is_vegetarian=is_vegetarian,
        is_vegan=is_vegan,
    )


def seed_cart(user, item, quantity=1):
    return Cart.objects.create(
        user=user,
        menuitem=item,
        quantity=quantity,
        unit_price=item.price,
        price=item.price * quantity,
    )


def place_order(client, orders_url):
    """POST to create an order; returns the response."""
    return client.post(orders_url, {'total': '0.00'})


# ---------------------------------------------------------------------------
# Base test case — creates all role users and groups
# ---------------------------------------------------------------------------

class BaseTestCase(APITestCase):
    """
    Creates the following users once per test class:
        admin_user    — is_staff=True  (not in any group)
        manager_user  — in 'Manager' group
        crew_user     — in 'DeliveryCrew' group
        customer_user — plain authenticated user

    Throttling and pagination are disabled via NO_THROTTLE so tests get
    plain list responses without rate-limit or page interference.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._throttle_override = override_settings(REST_FRAMEWORK=NO_THROTTLE)
        cls._throttle_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._throttle_override.disable()
        super().tearDownClass()

    def setUp(self):
        cache.clear()

    @classmethod
    def setUpTestData(cls):
        cls.manager_group, _ = Group.objects.get_or_create(name='Manager')
        cls.crew_group, _ = Group.objects.get_or_create(name='DeliveryCrew')

        cls.admin_user = User.objects.create_user(
            username='admin_joe', password='testpass123', is_staff=True
        )
        cls.manager_user = User.objects.create_user(
            username='manager_joe', password='testpass123'
        )
        cls.manager_user.groups.add(cls.manager_group)

        cls.crew_user = User.objects.create_user(
            username='crew_joe', password='testpass123'
        )
        cls.crew_user.groups.add(cls.crew_group)

        cls.customer_user = User.objects.create_user(
            username='customer_joe', password='testpass123'
        )

    def force_login(self, user):
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.force_authenticate(user=None)


# ---------------------------------------------------------------------------
# BaseTestCase sanity — verify fixtures are wired correctly
# ---------------------------------------------------------------------------

class BaseTestCaseSanityTests(BaseTestCase):

    def test_admin_is_staff(self):
        self.assertTrue(self.admin_user.is_staff)

    def test_admin_not_in_any_group(self):
        self.assertFalse(self.admin_user.groups.exists())

    def test_manager_in_manager_group(self):
        self.assertTrue(self.manager_user.groups.filter(name='Manager').exists())

    def test_manager_not_staff(self):
        self.assertFalse(self.manager_user.is_staff)

    def test_crew_in_delivery_crew_group(self):
        self.assertTrue(self.crew_user.groups.filter(name='DeliveryCrew').exists())

    def test_customer_in_no_groups(self):
        self.assertFalse(self.customer_user.groups.exists())

    def test_customer_not_staff(self):
        self.assertFalse(self.customer_user.is_staff)


# ---------------------------------------------------------------------------
# Menu Item — permission tests
# ---------------------------------------------------------------------------

class MenuItemPermissionTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.item = make_menu_item(cls.category)

    def _list_url(self):
        return reverse('menu-items-list')

    def _detail_url(self, pk=None):
        return reverse('menu-items-detail', args=[pk or self.item.pk])

    def _post_payload(self):
        return {
            'title': 'New Sandwich',
            'description': 'Fresh',
            'price': '11.00',
            'inventory': 20,
            'category_id': self.category.pk,
        }

    # --- READ ---

    def test_anonymous_can_list_menu_items(self):
        self.logout()
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_can_list_menu_items(self):
        self.force_login(self.customer_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delivery_crew_can_read_menu_items(self):
        self.force_login(self.crew_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_retrieve_menu_item(self):
        self.logout()
        response = self.client.get(self._detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_menu_item_returns_404(self):
        self.logout()
        response = self.client.get(self._detail_url(pk=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- CREATE ---

    def test_anonymous_cannot_create_menu_item(self):
        self.logout()
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_create_menu_item(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_cannot_create_menu_item(self):
        self.force_login(self.crew_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_cannot_update_menu_item(self):
        self.force_login(self.crew_user)
        response = self.client.patch(self._detail_url(), {'price': '5.00'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_create_menu_item(self):
        self.force_login(self.manager_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_menu_item(self):
        self.force_login(self.admin_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_menu_item_missing_required_fields_rejected(self):
        self.force_login(self.manager_user)
        response = self.client.post(self._list_url(), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu_item_negative_price_rejected(self):
        self.force_login(self.manager_user)
        payload = {**self._post_payload(), 'price': '-1.00'}
        response = self.client.post(self._list_url(), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- UPDATE ---

    def test_customer_cannot_update_menu_item(self):
        self.force_login(self.customer_user)
        response = self.client.patch(self._detail_url(), {'price': '5.00'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_update_menu_item(self):
        self.force_login(self.manager_user)
        response = self.client.patch(self._detail_url(), {'price': '15.99'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.price, Decimal('15.99'))

    def test_admin_can_update_menu_item(self):
        self.force_login(self.admin_user)
        response = self.client.patch(self._detail_url(), {'price': '16.99'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- DELETE ---

    def test_customer_cannot_delete_menu_item(self):
        self.force_login(self.customer_user)
        response = self.client.delete(self._detail_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_delete_menu_item(self):
        self.force_login(self.manager_user)
        item = make_menu_item(self.category, title='To Delete by Manager')
        response = self.client.delete(self._detail_url(pk=item.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_delete_menu_item(self):
        self.force_login(self.admin_user)
        item = make_menu_item(self.category, title='To Delete by Admin')
        response = self.client.delete(self._detail_url(pk=item.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Menu Item — filter / search / ordering tests
# ---------------------------------------------------------------------------

class MenuItemFilterTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sandwiches = make_category('Sandwiches', 'sandwiches')
        cls.soups = make_category('Soups', 'soups')

        cls.reuben = make_menu_item(cls.sandwiches, 'Reuben', '13.99')
        cls.veg_reuben = make_menu_item(
            cls.sandwiches, 'Vegetarian Reuben', '12.99', is_vegetarian=True
        )
        cls.vegan_reuben = make_menu_item(
            cls.sandwiches, 'Vegan Reuben', '13.49',
            is_vegetarian=True, is_vegan=True
        )
        cls.lentil = make_menu_item(
            cls.soups, 'Lentil Spinach Soup', '6.49',
            is_vegetarian=True, is_vegan=True
        )

    def test_filter_by_category(self):
        response = self.client.get(reverse('menu-items-list'), {'category': self.soups.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertIn('Lentil Spinach Soup', titles)
        self.assertNotIn('Reuben', titles)

    def test_filter_vegetarian(self):
        response = self.client.get(reverse('menu-items-list'), {'is_vegetarian': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertTrue(item['is_vegetarian'])

    def test_filter_vegan(self):
        response = self.client.get(reverse('menu-items-list'), {'is_vegan': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertTrue(item['is_vegan'])

    def test_filter_combined_vegetarian_and_category(self):
        response = self.client.get(reverse('menu-items-list'), {
            'is_vegetarian': 'true',
            'category': self.sandwiches.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertIn('Vegetarian Reuben', titles)
        self.assertIn('Vegan Reuben', titles)
        self.assertNotIn('Reuben', titles)
        self.assertNotIn('Lentil Spinach Soup', titles)

    def test_empty_category_filter_returns_message(self):
        empty_cat = make_category('Empty Cat', 'empty-cat')
        response = self.client.get(reverse('menu-items-list'), {'category': empty_cat.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'No items found in this category'})

    def test_search_by_title(self):
        response = self.client.get(reverse('menu-items-list'), {'search': 'Lentil'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertIn('Lentil Spinach Soup', titles)

    def test_search_by_description(self):
        # All items share the description 'A classic deli sandwich' from make_menu_item
        response = self.client.get(reverse('menu-items-list'), {'search': 'classic deli'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_ordering_by_price_ascending(self):
        response = self.client.get(reverse('menu-items-list'), {'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [Decimal(i['price']) for i in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_ordering_by_price_descending(self):
        response = self.client.get(reverse('menu-items-list'), {'ordering': '-price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [Decimal(i['price']) for i in response.data]
        self.assertEqual(prices, sorted(prices, reverse=True))


# ---------------------------------------------------------------------------
# Cart tests
# ---------------------------------------------------------------------------

class CartTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.item = make_menu_item(cls.category, 'Reuben', '13.99')
        cls.item2 = make_menu_item(cls.category, 'Turkey Club', '12.99')

    def setUp(self):
        super().setUp()
        Cart.objects.all().delete()

    def _list_url(self):
        return reverse('cart-items-list')

    def _detail_url(self, pk):
        return reverse('cart-items-detail', args=[pk])

    def test_anonymous_cannot_access_cart(self):
        self.logout()
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_can_list_cart_items(self):
        self.force_login(self.customer_user)
        seed_cart(self.customer_user, self.item, quantity=2)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['menuitem'], self.item.pk)

    def test_customer_can_add_to_cart(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._list_url(), {
            'menuitem': self.item.pk,
            'quantity': 2,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['price']), Decimal('27.98'))

    def test_adding_same_item_increments_quantity(self):
        self.force_login(self.customer_user)
        self.client.post(self._list_url(), {'menuitem': self.item.pk, 'quantity': 1})
        self.client.post(self._list_url(), {'menuitem': self.item.pk, 'quantity': 2})
        cart = Cart.objects.get(user=self.customer_user, menuitem=self.item)
        self.assertEqual(cart.quantity, 3)

    def test_cart_is_user_scoped(self):
        self.force_login(self.customer_user)
        self.client.post(self._list_url(), {'menuitem': self.item.pk, 'quantity': 1})

        other = User.objects.create_user(username='other_joe', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._list_url())
        self.assertEqual(len(response.data), 0)

    def test_delete_specific_item_removes_only_that_item(self):
        """DELETE /cart-items/<pk>/ must remove only that item, not the whole cart."""
        self.force_login(self.customer_user)
        entry1 = seed_cart(self.customer_user, self.item, quantity=1)
        entry2 = seed_cart(self.customer_user, self.item2, quantity=1)

        response = self.client.delete(self._detail_url(entry1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(pk=entry1.pk).exists())
        self.assertTrue(Cart.objects.filter(pk=entry2.pk).exists())

    def test_clear_cart_removes_all_items(self):
        self.force_login(self.customer_user)
        seed_cart(self.customer_user, self.item, quantity=1)
        seed_cart(self.customer_user, self.item2, quantity=1)
        response = self.client.delete(reverse('cart-items-clear-cart'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.customer_user).count(), 0)

    def test_add_nonexistent_menu_item_rejected(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._list_url(), {
            'menuitem': 99999,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_item_with_zero_quantity_rejected(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._list_url(), {
            'menuitem': self.item.pk,
            'quantity': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Order tests
# ---------------------------------------------------------------------------

class OrderTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.item = make_menu_item(cls.category, 'Turkey Club', '12.99')

    def setUp(self):
        super().setUp()
        Cart.objects.all().delete()
        Order.objects.all().delete()

    def _orders_url(self):
        return reverse('orders-list')

    def _order_url(self, pk):
        return reverse('orders-detail', args=[pk])

    def _place_order(self, user):
        seed_cart(user, self.item, quantity=1)
        self.force_login(user)
        return self.client.post(self._orders_url(), {'total': '0.00'})

    # --- Authentication gate ---

    def test_anonymous_cannot_list_orders(self):
        self.logout()
        response = self.client.get(self._orders_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_cannot_create_order(self):
        self.logout()
        response = self.client.post(self._orders_url(), {'total': '0.00'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Create ---

    def test_customer_cannot_create_order_with_empty_cart(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._orders_url(), {'total': '0.00'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_can_create_order_from_cart(self):
        seed_cart(self.customer_user, self.item, quantity=2)
        self.force_login(self.customer_user)
        response = self.client.post(self._orders_url(), {'total': '0.00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.filter(user=self.customer_user).count(), 0)
        order = Order.objects.get(user=self.customer_user)
        self.assertEqual(order.total, Decimal('25.98'))

    def test_order_creation_produces_correct_order_items(self):
        seed_cart(self.customer_user, self.item, quantity=3)
        self.force_login(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})
        order = Order.objects.get(user=self.customer_user)
        self.assertEqual(order.order_items.count(), 1)
        oi = order.order_items.first()
        self.assertEqual(oi.menuitem, self.item)
        self.assertEqual(oi.quantity, 3)
        self.assertEqual(oi.unit_price, self.item.price)
        self.assertEqual(oi.price, self.item.price * 3)

    # --- Queryset scoping ---

    def test_customer_only_sees_own_orders(self):
        self._place_order(self.customer_user)
        other = User.objects.create_user(username='other_customer', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._orders_url())
        self.assertEqual(len(response.data), 0)

    def test_customer_cannot_retrieve_another_users_order(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        other = User.objects.create_user(username='nosy_customer', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._order_url(order.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_sees_all_orders(self):
        self._place_order(self.customer_user)
        self.force_login(self.manager_user)
        response = self.client.get(self._orders_url())
        self.assertGreaterEqual(len(response.data), 1)

    def test_delivery_crew_sees_only_assigned_orders(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        response = self.client.get(self._orders_url())
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], order.pk)

    # --- Date filter ---

    def test_manager_can_filter_orders_by_today(self):
        self._place_order(self.customer_user)
        self.force_login(self.manager_user)
        response = self.client.get(self._orders_url(), {'date': 'today'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # --- Update ---

    def test_customer_cannot_update_order(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        self.force_login(self.customer_user)
        response = self.client.patch(self._order_url(order.pk), {'status': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_can_update_order_status(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        response = self.client.patch(self._order_url(order.pk), {'status': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertTrue(order.status)

    def test_crew_update_with_invalid_status_rejected(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        response = self.client.patch(self._order_url(order.pk), {'status': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_assign_delivery_crew(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        self.assertIsNone(order.delivery_crew)

        self.force_login(self.manager_user)
        response = self.client.patch(
            self._order_url(order.pk),
            {'delivery_crew': self.crew_user.pk},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.delivery_crew, self.crew_user)

    # --- Delete ---

    def test_customer_cannot_delete_order(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        self.force_login(self.customer_user)
        response = self.client.delete(self._order_url(order.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_cannot_delete_order(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        response = self.client.delete(self._order_url(order.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_delete_order(self):
        self._place_order(self.customer_user)
        order = Order.objects.get(user=self.customer_user)
        self.force_login(self.manager_user)
        response = self.client.delete(self._order_url(order.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Rating tests
# ---------------------------------------------------------------------------

class RatingTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.item = make_menu_item(cls.category, 'Classic Caesar', '9.99')

    def setUp(self):
        super().setUp()
        Rating.objects.all().delete()

    def _ratings_url(self):
        return reverse('rating-list')

    def test_anonymous_cannot_rate(self):
        self.logout()
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': 5,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_can_rate_menu_item(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': 4,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cannot_rate_same_item_twice(self):
        self.force_login(self.customer_user)
        self.client.post(self._ratings_url(), {'menuitem': self.item.pk, 'rating': 4})
        response = self.client.post(self._ratings_url(), {'menuitem': self.item.pk, 'rating': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_out_of_range_rejected(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': 6,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_below_zero_rejected(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': -1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_of_zero_accepted(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rating_of_five_accepted(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem': self.item.pk,
            'rating': 5,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_empty_ratings_returns_empty_list(self):
        self.force_login(self.customer_user)
        response = self.client.get(self._ratings_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_customer_only_sees_own_ratings(self):
        self.force_login(self.customer_user)
        self.client.post(self._ratings_url(), {'menuitem': self.item.pk, 'rating': 5})
        other = User.objects.create_user(username='rater2', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._ratings_url())
        self.assertEqual(len(response.data), 0)


# ---------------------------------------------------------------------------
# Group management — permission tests
# ---------------------------------------------------------------------------

class GroupManagementTests(BaseTestCase):

    def _members_url(self, group_name='Manager'):
        return f'/api/groups/{group_name}/users/'

    def _member_url(self, user_id, group_name='Manager'):
        return f'/api/groups/{group_name}/users/{user_id}/'

    # --- Authentication / role gate ---

    def test_anonymous_cannot_list_group_members(self):
        self.logout()
        response = self.client.get(self._members_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_list_group_members(self):
        self.force_login(self.customer_user)
        response = self.client.get(self._members_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_cannot_list_group_members(self):
        self.force_login(self.crew_user)
        response = self.client.get(self._members_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_list_group_members(self):
        self.force_login(self.manager_user)
        response = self.client.get(self._members_url('Manager'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [u['username'] for u in response.data]
        self.assertIn(self.manager_user.username, usernames)

    def test_admin_can_manage_groups(self):
        """is_staff admin should be able to manage groups (IsManagerOrAdmin)."""
        self.force_login(self.admin_user)
        response = self.client.get(self._members_url('Manager'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_list_delivery_crew_members(self):
        self.force_login(self.manager_user)
        response = self.client.get(self._members_url('DeliveryCrew'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [u['username'] for u in response.data]
        self.assertIn(self.crew_user.username, usernames)

    # --- Add user ---

    def test_manager_can_add_user_to_delivery_crew(self):
        self.force_login(self.manager_user)
        new_user = User.objects.create_user(username='new_crew', password='testpass123')
        response = self.client.post(
            self._members_url('DeliveryCrew'),
            {'user_id': new_user.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(new_user.groups.filter(name='DeliveryCrew').exists())

    def test_manager_can_add_user_to_manager_group(self):
        self.force_login(self.manager_user)
        new_user = User.objects.create_user(username='new_manager', password='testpass123')
        response = self.client.post(
            self._members_url('Manager'),
            {'user_id': new_user.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cannot_add_user_to_group(self):
        self.force_login(self.customer_user)
        response = self.client.post(
            self._members_url('Manager'),
            {'user_id': self.customer_user.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_nonexistent_user_returns_404(self):
        self.force_login(self.manager_user)
        response = self.client.post(
            self._members_url('Manager'),
            {'user_id': 99999},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- Remove user ---

    def test_manager_can_remove_user_from_group(self):
        self.force_login(self.manager_user)
        target = User.objects.create_user(username='temp_crew', password='testpass123')
        self.crew_group.user_set.add(target)
        response = self.client.delete(self._member_url(target.pk, 'DeliveryCrew'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(target.groups.filter(name='DeliveryCrew').exists())

    # --- Error cases ---

    def test_nonexistent_group_returns_404(self):
        self.force_login(self.manager_user)
        response = self.client.get(self._members_url('NonExistentGroup'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Order item — permission and scoping tests
# ---------------------------------------------------------------------------

class OrderItemPermissionTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.menu_item = make_menu_item(cls.category, 'Club Sandwich', '11.99')

    def setUp(self):
        super().setUp()
        Order.objects.all().delete()

    def _make_order(self, user, assign_crew=False):
        order = Order.objects.create(user=user, total='11.99', status=False)
        if assign_crew:
            order.delivery_crew = self.crew_user
            order.save()
        OrderItem.objects.create(
            order=order,
            menuitem=self.menu_item,
            quantity=1,
            unit_price=self.menu_item.price,
            price=self.menu_item.price,
        )
        return order

    def _list_url(self):
        return reverse('orderitem-list')

    def _detail_url(self, pk):
        return reverse('orderitem-detail', args=[pk])

    # --- Anonymous ---

    def test_anonymous_cannot_read_order_items(self):
        self.logout()
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Queryset scoping ---

    def test_customer_can_read_own_order_items(self):
        self._make_order(self.customer_user)
        self.force_login(self.customer_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_cannot_read_other_users_order_items(self):
        other = User.objects.create_user(username='other_cust', password='testpass123')
        self._make_order(other)
        self.force_login(self.customer_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_delivery_crew_sees_only_assigned_order_items(self):
        assigned_order = self._make_order(self.customer_user, assign_crew=True)
        unassigned_order = self._make_order(self.customer_user)

        self.force_login(self.crew_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_ids = {oi['order'] for oi in response.data}
        self.assertIn(assigned_order.pk, order_ids)
        self.assertNotIn(unassigned_order.pk, order_ids)

    def test_manager_can_read_all_order_items(self):
        other = User.objects.create_user(username='cust_a', password='testpass123')
        self._make_order(self.customer_user)
        self._make_order(other)
        self.force_login(self.manager_user)
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    # --- Write permissions ---

    def test_customer_cannot_create_order_item_directly(self):
        self.force_login(self.customer_user)
        order = self._make_order(self.customer_user)
        response = self.client.post(self._list_url(), {
            'order': order.pk,
            'menuitem': self.menu_item.pk,
            'quantity': 1,
            'unit_price': '11.99',
            'price': '11.99',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delivery_crew_cannot_create_order_item(self):
        self.force_login(self.crew_user)
        order = self._make_order(self.customer_user)
        response = self.client.post(self._list_url(), {
            'order': order.pk,
            'menuitem': self.menu_item.pk,
            'quantity': 1,
            'unit_price': '11.99',
            'price': '11.99',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_update_order_item(self):
        self.force_login(self.manager_user)
        order = self._make_order(self.customer_user)
        item = order.order_items.first()
        response = self.client.patch(self._detail_url(item.pk), {'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_delete_order_item(self):
        self.force_login(self.manager_user)
        order = self._make_order(self.customer_user)
        item = order.order_items.first()
        response = self.client.delete(self._detail_url(item.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_write_order_items(self):
        self.force_login(self.admin_user)
        order = self._make_order(self.customer_user)
        item = order.order_items.first()
        response = self.client.patch(self._detail_url(item.pk), {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Pagination tests
# ---------------------------------------------------------------------------

from rest_framework.pagination import PageNumberPagination
from JoesDeliDRF.views import MenuItemViewSet


class _SmallPagination(PageNumberPagination):
    """3-item pages used only by PaginationTests."""
    page_size = 3


class PaginationTests(BaseTestCase):
    """
    DRF sets GenericAPIView.pagination_class at class import time, so
    override_settings cannot change it at runtime. We instead temporarily
    swap pagination_class directly on MenuItemViewSet in setUp/tearDown.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pag_category = Category.objects.create(title='Pagination Cat', slug='pagination-cat')
        for i in range(8):
            MenuItem.objects.create(
                title=f'Item {i:02d}',
                description='A classic deli sandwich',
                price=Decimal(f'{10 + i}.99'),
                inventory=10,
                category=cls.pag_category,
            )

    def setUp(self):
        super().setUp()
        self._orig_pagination = MenuItemViewSet.pagination_class
        MenuItemViewSet.pagination_class = _SmallPagination

    def tearDown(self):
        MenuItemViewSet.pagination_class = self._orig_pagination
        super().tearDown()

    def test_paginated_response_has_expected_structure(self):
        response = self.client.get(reverse('menu-items-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_page_size_is_respected(self):
        response = self.client.get(reverse('menu-items-list'))
        self.assertEqual(len(response.data['results']), 3)

    def test_next_page_link_present_on_first_page(self):
        response = self.client.get(reverse('menu-items-list'))
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_page_2_returns_different_items(self):
        page1 = self.client.get(reverse('menu-items-list'), {'page': 1})
        page2 = self.client.get(reverse('menu-items-list'), {'page': 2})
        self.assertEqual(page2.status_code, status.HTTP_200_OK)
        titles_p1 = {i['title'] for i in page1.data['results']}
        titles_p2 = {i['title'] for i in page2.data['results']}
        self.assertTrue(titles_p1.isdisjoint(titles_p2))

    def test_count_reflects_total_items(self):
        response = self.client.get(reverse('menu-items-list'))
        # 8 from setUpTestData + 39 from seed migration (0007) = 47 minimum
        self.assertGreaterEqual(response.data['count'], 8)


# ---------------------------------------------------------------------------
# JWT authentication tests
# ---------------------------------------------------------------------------

class JWTAuthTests(BaseTestCase):
    """Tests the djoser JWT endpoints: /auth/jwt/create/ and /auth/jwt/refresh/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.jwt_user = User.objects.create_user(
            username='jwt_user', password='jwtpass123'
        )

    def test_valid_credentials_return_access_and_refresh_tokens(self):
        response = self.client.post('/auth/jwt/create/', {
            'username': 'jwt_user',
            'password': 'jwtpass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials_rejected(self):
        response = self.client.post('/auth/jwt/create/', {
            'username': 'jwt_user',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_password_rejected(self):
        response = self.client.post('/auth/jwt/create/', {'username': 'jwt_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_token_authenticates_protected_endpoint(self):
        token_response = self.client.post('/auth/jwt/create/', {
            'username': 'jwt_user',
            'password': 'jwtpass123',
        })
        access = token_response.data['access']
        # Use token directly on the client (no force_authenticate)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get(reverse('orders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()  # clear

    def test_refresh_token_returns_new_access_token(self):
        token_response = self.client.post('/auth/jwt/create/', {
            'username': 'jwt_user',
            'password': 'jwtpass123',
        })
        refresh = token_response.data['refresh']
        refresh_response = self.client.post('/auth/jwt/refresh/', {'refresh': refresh})
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_invalid_refresh_token_rejected(self):
        response = self.client.post('/auth/jwt/refresh/', {'refresh': 'not.a.token'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

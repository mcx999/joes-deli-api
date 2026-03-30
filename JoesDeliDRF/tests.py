from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, MenuItem, Cart, Order, OrderItem, Rating


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_category(title='Sandwiches', slug='sandwiches'):
    return Category.objects.create(title=title, slug=slug)


def make_menu_item(category, title='Reuben', price='13.99',
                   is_vegetarian=False, is_vegan=False):
    return MenuItem.objects.create(
        title=title,
        description='Test item',
        price=Decimal(price),
        inventory=50,
        category=category,
        is_vegetarian=is_vegetarian,
        is_vegan=is_vegan,
    )


# ---------------------------------------------------------------------------
# Base test case — creates all role users and groups
# ---------------------------------------------------------------------------

class BaseTestCase(APITestCase):
    """
    Creates the following users once per test class:
        admin_user    — is_staff=True
        manager_user  — in 'Manager' group
        crew_user     — in 'Delivery crew' group
        customer_user — plain authenticated user
    Anonymous access is tested via self.client (unauthenticated).
    """

    @classmethod
    def setUpTestData(cls):
        cls.manager_group = Group.objects.create(name='Manager')
        cls.crew_group = Group.objects.create(name='Delivery crew')

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

    def test_anonymous_can_retrieve_menu_item(self):
        self.logout()
        response = self.client.get(self._detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_manager_can_create_menu_item(self):
        self.force_login(self.manager_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_menu_item(self):
        self.force_login(self.admin_user)
        response = self.client.post(self._list_url(), self._post_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
# Menu Item — filter / search tests
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

    def test_search_by_title(self):
        response = self.client.get(reverse('menu-items-list'), {'search': 'Lentil'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertIn('Lentil Spinach Soup', titles)

    def test_ordering_by_price_ascending(self):
        response = self.client.get(reverse('menu-items-list'), {'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [Decimal(i['price']) for i in response.data]
        self.assertEqual(prices, sorted(prices))


# ---------------------------------------------------------------------------
# Cart tests
# ---------------------------------------------------------------------------

class CartTests(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = make_category()
        cls.item = make_menu_item(cls.category, 'Reuben', '13.99')

    def setUp(self):
        Cart.objects.all().delete()

    def _list_url(self):
        return reverse('cart-items-list')

    def test_anonymous_cannot_access_cart(self):
        self.logout()
        response = self.client.get(self._list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_clear_cart(self):
        self.force_login(self.customer_user)
        self.client.post(self._list_url(), {'menuitem': self.item.pk, 'quantity': 1})
        response = self.client.delete(reverse('cart-items-clear-cart'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.customer_user).count(), 0)


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
        Cart.objects.all().delete()
        Order.objects.all().delete()

    def _seed_cart(self, user, quantity=1):
        Cart.objects.create(
            user=user,
            menuitem=self.item,
            quantity=quantity,
            unit_price=self.item.price,
            price=self.item.price * quantity,
        )

    def _orders_url(self):
        return reverse('orders-list')

    def test_customer_cannot_create_order_with_empty_cart(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._orders_url(), {'total': '0.00'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_can_create_order_from_cart(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user, quantity=2)
        response = self.client.post(self._orders_url(), {'total': '0.00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.filter(user=self.customer_user).count(), 0)
        order = Order.objects.get(user=self.customer_user)
        self.assertEqual(order.total, Decimal('25.98'))

    def test_customer_only_sees_own_orders(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})

        other = User.objects.create_user(username='other_customer', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._orders_url())
        self.assertEqual(len(response.data), 0)

    def test_manager_sees_all_orders(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})

        self.force_login(self.manager_user)
        response = self.client.get(self._orders_url())
        self.assertGreaterEqual(len(response.data), 1)

    def test_delivery_crew_sees_only_assigned_orders(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        response = self.client.get(self._orders_url())
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], order.pk)

    def test_delivery_crew_can_update_order_status(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})
        order = Order.objects.get(user=self.customer_user)
        order.delivery_crew = self.crew_user
        order.save()

        self.force_login(self.crew_user)
        url = reverse('orders-detail', args=[order.pk])
        response = self.client.patch(url, {'status': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertTrue(order.status)

    def test_customer_cannot_delete_order(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})
        order = Order.objects.get(user=self.customer_user)

        url = reverse('orders-detail', args=[order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_delete_order(self):
        self.force_login(self.customer_user)
        self._seed_cart(self.customer_user)
        self.client.post(self._orders_url(), {'total': '0.00'})
        order = Order.objects.get(user=self.customer_user)

        self.force_login(self.manager_user)
        url = reverse('orders-detail', args=[order.pk])
        response = self.client.delete(url)
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
        Rating.objects.all().delete()

    def _ratings_url(self):
        return reverse('rating-list')

    def test_anonymous_cannot_rate(self):
        self.logout()
        response = self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 5,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_can_rate_menu_item(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 4,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cannot_rate_same_item_twice(self):
        self.force_login(self.customer_user)
        self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 4,
        })
        response = self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 3,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_out_of_range_rejected(self):
        self.force_login(self.customer_user)
        response = self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 6,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_only_sees_own_ratings(self):
        self.force_login(self.customer_user)
        self.client.post(self._ratings_url(), {
            'menuitem_id': self.item.pk,
            'rating': 5,
        })
        other = User.objects.create_user(username='rater2', password='testpass123')
        self.force_login(other)
        response = self.client.get(self._ratings_url())
        self.assertEqual(len(response.data), 0)

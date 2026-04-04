from django.db import migrations


# ---------------------------------------------------------------------------
# Forward: apply the refined menu changes
# ---------------------------------------------------------------------------

def update_menu(apps, schema_editor):
    Category = apps.get_model('JoesDeliDRF', 'Category')
    MenuItem = apps.get_model('JoesDeliDRF', 'MenuItem')

    # 1. Remove Salads category (cascades to its items)
    Category.objects.filter(slug='salads').delete()

    # 2. Update individual items
    item_updates = [
        # (category_slug, current_title, fields_to_update)
        (
            'soups', 'French Onion',
            {
                'description': 'Caramelized onion broth, gruyère crouton, traditional beef broth',
                'is_vegetarian': False,
                'is_vegan': False,
            },
        ),
        (
            'soups', 'Minestrone',
            {
                'title': 'Minestrone (Vegetarian)',
                'description': 'Cannellini beans, pasta, zucchini, tomato, vegetarian parmesan broth (microbial rennet)',
            },
        ),
        (
            'sandwiches', 'Veggie Wrap',
            {
                'description': 'Hummus, roasted veggies, spinach, feta in a whole wheat wrap\nVegan cheese available +$1.49',
            },
        ),
        (
            'beverages', 'Fountain Soda',
            {
                'description': 'Coke, Diet Coke, Sprite, Dr Pepper',
            },
        ),
    ]
    for category_slug, title, fields in item_updates:
        category = Category.objects.get(slug=category_slug)
        MenuItem.objects.filter(title=title, category=category).update(**fields)

    # 3. Add new items
    new_items = [
        (
            'soups',
            [
                {
                    'title': 'Matzo Ball Soup (Traditional)',
                    'description': 'Chicken broth, matzo balls, carrot, celery, dill',
                    'price': '6.49',
                    'is_vegetarian': False,
                    'is_vegan': False,
                },
                {
                    'title': 'Matzo Ball Soup (Vegetarian)',
                    'description': 'Vegetable broth, matzo balls (egg-based), carrot, celery, dill',
                    'price': '6.49',
                    'is_vegetarian': True,
                    'is_vegan': False,
                },
            ],
        ),
        (
            'sandwiches',
            [
                {
                    'title': 'Pastrami on Rye',
                    'description': 'Hand-sliced pastrami, spicy brown mustard, rye',
                    'price': '13.99',
                    'is_vegetarian': False,
                    'is_vegan': False,
                },
                {
                    'title': 'BLT',
                    'description': 'Thick-cut bacon, lettuce, tomato, mayo on toasted sourdough',
                    'price': '10.49',
                    'is_vegetarian': False,
                    'is_vegan': False,
                },
                {
                    'title': 'Chicken Salad Sandwich',
                    'description': 'House chicken salad, lettuce, tomato on a kaiser roll',
                    'price': '11.49',
                    'is_vegetarian': False,
                    'is_vegan': False,
                },
                {
                    'title': 'Tuna Melt',
                    'description': 'Albacore tuna salad, cheddar, grilled on sourdough',
                    'price': '11.99',
                    'is_vegetarian': False,
                    'is_vegan': False,
                },
            ],
        ),
        (
            'beverages',
            [
                {
                    'title': 'Hot Coffee',
                    'description': 'Fresh-brewed medium roast',
                    'price': '2.49',
                    'is_vegetarian': True,
                    'is_vegan': True,
                },
                {
                    'title': 'Bottled Water',
                    'description': '16.9 oz',
                    'price': '1.99',
                    'is_vegetarian': True,
                    'is_vegan': True,
                },
            ],
        ),
        (
            'sides',
            [
                {
                    'title': 'Potato Salad',
                    'description': 'Red potatoes, celery, dill, creamy dressing',
                    'price': '3.49',
                    'is_vegetarian': True,
                    'is_vegan': False,
                },
                {
                    'title': 'Soft Pretzel',
                    'description': 'Warm salted pretzel, mustard on the side',
                    'price': '3.99',
                    'is_vegetarian': True,
                    'is_vegan': True,
                },
            ],
        ),
        (
            'desserts',
            [
                {
                    'title': 'Chocolate Chip Cookie',
                    'description': 'Soft-baked, semi-sweet chocolate',
                    'price': '2.49',
                    'is_vegetarian': True,
                    'is_vegan': False,
                },
                {
                    'title': 'Cannoli',
                    'description': 'Crisp shell, sweet ricotta filling, chocolate chips',
                    'price': '3.99',
                    'is_vegetarian': True,
                    'is_vegan': False,
                },
            ],
        ),
    ]
    for category_slug, items in new_items:
        category = Category.objects.get(slug=category_slug)
        for item in items:
            MenuItem.objects.get_or_create(
                title=item['title'],
                category=category,
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                    'inventory': 50,
                    'is_vegetarian': item['is_vegetarian'],
                    'is_vegan': item['is_vegan'],
                },
            )


# ---------------------------------------------------------------------------
# Reverse: undo changes from update_menu
# ---------------------------------------------------------------------------

SALADS_ITEMS = [
    {
        'title': 'Classic Caesar',
        'description': 'Romaine, parmesan, croutons, Caesar dressing',
        'price': '9.99',
        'is_vegetarian': True,
        'is_vegan': False,
    },
    {
        'title': 'Greek Salad',
        'description': 'Cucumber, tomato, olives, feta, red onion, oregano vinaigrette',
        'price': '10.49',
        'is_vegetarian': True,
        'is_vegan': False,
    },
    {
        'title': 'Chopped Italian',
        'description': 'Salami, provolone, pepperoncini, romaine, Italian dressing',
        'price': '11.49',
        'is_vegetarian': False,
        'is_vegan': False,
    },
    {
        'title': 'Tuna Niçoise',
        'description': 'Albacore tuna, green beans, hard-boiled egg, olives, Dijon vinaigrette',
        'price': '12.99',
        'is_vegetarian': False,
        'is_vegan': False,
    },
]


def reverse_update_menu(apps, schema_editor):
    Category = apps.get_model('JoesDeliDRF', 'Category')
    MenuItem = apps.get_model('JoesDeliDRF', 'MenuItem')

    # 1. Restore Salads category and items
    salads, _ = Category.objects.get_or_create(
        slug='salads', defaults={'title': 'Salads'}
    )
    for item in SALADS_ITEMS:
        MenuItem.objects.get_or_create(
            title=item['title'],
            category=salads,
            defaults={
                'description': item['description'],
                'price': item['price'],
                'inventory': 50,
                'is_vegetarian': item['is_vegetarian'],
                'is_vegan': item['is_vegan'],
            },
        )

    # 2. Revert updated items
    soups = Category.objects.get(slug='soups')
    sandwiches = Category.objects.get(slug='sandwiches')
    beverages = Category.objects.get(slug='beverages')

    MenuItem.objects.filter(title='French Onion', category=soups).update(
        description='Caramelized onion broth, gruyère crouton',
        is_vegetarian=True,
        is_vegan=False,
    )
    MenuItem.objects.filter(title='Minestrone (Vegetarian)', category=soups).update(
        title='Minestrone',
        description='Cannellini beans, pasta, zucchini, tomato, parmesan broth',
    )
    MenuItem.objects.filter(title='Veggie Wrap', category=sandwiches).update(
        description='Hummus, roasted veggies, spinach, feta in a whole wheat wrap',
    )
    MenuItem.objects.filter(title='Fountain Soda', category=beverages).update(
        description='Coke, Diet Coke, Sprite, or Dr Pepper',
    )

    # 3. Remove added items
    added_titles = [
        'Matzo Ball Soup (Traditional)',
        'Matzo Ball Soup (Vegetarian)',
        'Pastrami on Rye',
        'BLT',
        'Chicken Salad Sandwich',
        'Tuna Melt',
        'Hot Coffee',
        'Bottled Water',
        'Potato Salad',
        'Soft Pretzel',
        'Chocolate Chip Cookie',
        'Cannoli',
    ]
    MenuItem.objects.filter(title__in=added_titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('JoesDeliDRF', '0009_rename_delivery_crew_group'),
    ]

    operations = [
        migrations.RunPython(update_menu, reverse_code=reverse_update_menu),
    ]

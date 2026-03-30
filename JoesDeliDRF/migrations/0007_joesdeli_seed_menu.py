from django.db import migrations


MENU_DATA = {
    'Salads': {
        'slug': 'salads',
        'items': [
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
        ],
    },
    'Soups': {
        'slug': 'soups',
        'items': [
            {
                'title': 'New England Clam Chowder',
                'description': 'Creamy chowder with clams, potatoes, and bacon',
                'price': '6.49',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'French Onion',
                'description': 'Caramelized onion broth, gruyère crouton',
                'price': '6.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Chicken Noodle',
                'description': 'House-made broth, egg noodles, carrots, celery',
                'price': '5.99',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'Tomato Bisque',
                'description': 'Roasted tomato, fresh basil, cream',
                'price': '5.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Lentil Spinach Soup',
                'description': 'Red lentils, wilted spinach, cumin, lemon',
                'price': '6.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Potato Leek Soup',
                'description': 'Creamy potato and leek, chives, olive oil',
                'price': '5.99',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Broccoli Cheddar',
                'description': 'Roasted broccoli, sharp cheddar, cream',
                'price': '6.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Vegetable Soup',
                'description': 'Seasonal vegetables, tomato broth, herbs',
                'price': '5.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Minestrone',
                'description': 'Cannellini beans, pasta, zucchini, tomato, parmesan broth',
                'price': '5.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
        ],
    },
    'Sandwiches': {
        'slug': 'sandwiches',
        'items': [
            {
                'title': 'Reuben',
                'description': 'Corned beef, Swiss, sauerkraut, Thousand Island on rye',
                'price': '13.99',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'Turkey Club',
                'description': 'Roasted turkey, bacon, lettuce, tomato, mayo on sourdough',
                'price': '12.99',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'Italian Hoagie',
                'description': 'Capicola, salami, provolone, roasted peppers on a hoagie roll',
                'price': '13.49',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'Roast Beef & Cheddar',
                'description': 'Slow-roasted beef, sharp cheddar, horseradish aioli on a kaiser roll',
                'price': '14.49',
                'is_vegetarian': False,
                'is_vegan': False,
            },
            {
                'title': 'Veggie Wrap',
                'description': 'Hummus, roasted veggies, spinach, feta in a whole wheat wrap',
                'price': '10.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Classic Grilled Cheese',
                'description': 'American cheese on sourdough. Specify bread in notes: sourdough, rye, whole wheat, or ciabatta',
                'price': '8.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Three Cheese Melt',
                'description': 'Cheddar, Swiss, provolone on ciabatta. Specify bread in notes: sourdough, rye, whole wheat, or ciabatta',
                'price': '9.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Swiss & Tomato Grilled Cheese',
                'description': 'Swiss, beefsteak tomato, fresh basil on rye. Specify bread in notes: sourdough, rye, whole wheat, or ciabatta',
                'price': '9.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Deluxe Grilled Cheese',
                'description': 'Cheddar, provolone, caramelized onion, roasted red pepper on whole wheat. Specify bread in notes: sourdough, rye, whole wheat, or ciabatta',
                'price': '10.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Avocado & Hummus Sandwich',
                'description': 'Avocado, hummus, cucumber, sprouts, shredded carrot on whole wheat',
                'price': '10.99',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Roasted Veggie Ciabatta',
                'description': 'Zucchini, eggplant, roasted red pepper, arugula, olive tapenade on ciabatta',
                'price': '11.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Vegetarian Reuben',
                'description': 'Tempeh or tofu, Swiss, sauerkraut, Thousand Island on rye. Specify protein in notes: tempeh or tofu',
                'price': '12.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Vegan Reuben',
                'description': 'Tempeh or tofu, vegan Swiss, sauerkraut, vegan Thousand Island on rye. Specify protein in notes: tempeh or tofu',
                'price': '13.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
        ],
    },
    'Beverages': {
        'slug': 'beverages',
        'items': [
            {
                'title': 'Fresh Lemonade',
                'description': 'House-squeezed, sweetened or unsweetened',
                'price': '3.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Iced Tea',
                'description': 'Black or green, sweetened or unsweetened',
                'price': '2.99',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Cold Brew Coffee',
                'description': '12-hour cold brew, served over ice',
                'price': '4.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Fountain Soda',
                'description': 'Coke, Diet Coke, Sprite, or Dr Pepper',
                'price': '2.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
        ],
    },
    'Sides': {
        'slug': 'sides',
        'items': [
            {
                'title': 'Deli Pickle',
                'description': 'House-brined whole dill pickle',
                'price': '1.49',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Kettle Chips',
                'description': 'Sea salt, BBQ, or jalapeño cheddar',
                'price': '2.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Pasta Salad',
                'description': 'Rotini, olives, cherry tomatoes, Italian dressing',
                'price': '3.99',
                'is_vegetarian': True,
                'is_vegan': True,
            },
            {
                'title': 'Coleslaw',
                'description': 'Creamy house-made slaw',
                'price': '2.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Mac & Cheese',
                'description': 'Creamy elbow macaroni, sharp cheddar',
                'price': '4.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
        ],
    },
    'Desserts': {
        'slug': 'desserts',
        'items': [
            {
                'title': 'New York Cheesecake',
                'description': 'Classic dense cheesecake with graham cracker crust',
                'price': '5.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Black & White Cookie',
                'description': 'Soft sponge cookie, half vanilla / half chocolate fondant',
                'price': '2.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Brownie',
                'description': 'Fudge brownie, walnuts optional',
                'price': '3.49',
                'is_vegetarian': True,
                'is_vegan': False,
            },
            {
                'title': 'Rice Pudding',
                'description': 'Creamy vanilla rice pudding, cinnamon',
                'price': '3.99',
                'is_vegetarian': True,
                'is_vegan': False,
            },
        ],
    },
}


def seed_menu(apps, schema_editor):
    Category = apps.get_model('JoesDeliDRF', 'Category')
    MenuItem = apps.get_model('JoesDeliDRF', 'MenuItem')

    for category_title, data in MENU_DATA.items():
        category, _ = Category.objects.get_or_create(
            title=category_title,
            defaults={'slug': data['slug']},
        )
        for item in data['items']:
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


def unseed_menu(apps, schema_editor):
    Category = apps.get_model('JoesDeliDRF', 'Category')
    Category.objects.filter(slug__in=[
        'salads', 'soups', 'sandwiches', 'beverages', 'sides', 'desserts'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('JoesDeliDRF', '0006_menuitem_dietary_flags'),
    ]

    operations = [
        migrations.RunPython(seed_menu, reverse_code=unseed_menu),
    ]

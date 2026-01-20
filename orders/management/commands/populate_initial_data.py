from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import MenuCategory, MenuItem, Table
from orders.models import OrderStatus, PaymentMethod, Restaurant, CustomerReview, Staff, InventoryItem, Shift
from datetime import date, time

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')

        # Create order statuses
        statuses = ['pending', 'processing', 'completed', 'cancelled']
        for status in statuses:
            OrderStatus.objects.get_or_create(name=status)
            self.stdout.write(f'Created order status: {status}')

        # Create payment methods
        payment_methods = ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Wallet']
        for method in payment_methods:
            PaymentMethod.objects.get_or_create(name=method)
            self.stdout.write(f'Created payment method: {method}')

        # Create menu categories
        categories = ['Appetizers', 'Main Course', 'Desserts', 'Beverages']
        for cat_name in categories:
            MenuCategory.objects.get_or_create(name=cat_name)
            self.stdout.write(f'Created category: {cat_name}')

        # Get categories
        appetizers = MenuCategory.objects.get(name='Appetizers')
        main_course = MenuCategory.objects.get(name='Main Course')
        desserts = MenuCategory.objects.get(name='Desserts')
        beverages = MenuCategory.objects.get(name='Beverages')

        # Create menu items
        menu_items = [
            ('Spring Rolls', appetizers, 120.00, True),
            ('Chicken Wings', appetizers, 180.00, False),
            ('Caesar Salad', appetizers, 150.00, False),
            ('Grilled Chicken', main_course, 250.00, True),
            ('Paneer Butter Masala', main_course, 220.00, False),
            ('Fish Curry', main_course, 280.00, False),
            ('Chocolate Brownie', desserts, 100.00, True),
            ('Ice Cream', desserts, 80.00, False),
            ('Coffee', beverages, 50.00, False),
            ('Juice', beverages, 60.00, True),
        ]

        for name, category, price, featured in menu_items:
            MenuItem.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'price': price,
                    'is_featured': featured
                }
            )
            self.stdout.write(f'Created menu item: {name}')

        # Create tables
        for i in range(1, 11):  # Tables 1-10
            capacity = 4 if i <= 5 else 6  # Smaller tables for 1-5, larger for 6-10
            Table.objects.get_or_create(
                table_number=i,
                defaults={
                    'capacity': capacity,
                    'is_available': True
                }
            )
            self.stdout.write(f'Created table: {i} (capacity: {capacity})')

        # Create restaurant
        Restaurant.objects.get_or_create(
            name='Sample Restaurant',
            defaults={
                'address': '123 Main Street, City, State',
                'phone': '1234567890',
                'has_delivery': True,
                'opening_days': 'Mon-Sun'
            }
        )
        self.stdout.write('Created restaurant')

        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created superuser: admin/admin123')

        # Create staff members
        admin_user = User.objects.get(username='admin')
        staff_members = [
            ('chef1', 'Chef', 'John', 'Smith', 'john@restaurant.com', '+1234567890'),
            ('waiter1', 'Waiter', 'Sarah', 'Johnson', 'sarah@restaurant.com', '+1234567891'),
            ('manager1', 'Manager', 'Mike', 'Davis', 'mike@restaurant.com', '+1234567892'),
        ]

        for username, role, first_name, last_name, email, phone in staff_members:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='staff123',
                    first_name=first_name,
                    last_name=last_name
                )
                Staff.objects.create(
                    user=user,
                    employee_id=f'EMP{User.objects.count():03d}',
                    role=role.lower(),
                    phone=phone,
                    hire_date=date.today(),
                    salary=30000 if role == 'Chef' else 25000 if role == 'Manager' else 20000
                )
                self.stdout.write(f'Created staff member: {first_name} {last_name} ({role})')

        # Create inventory items
        inventory_data = [
            ('Chicken Breast', 'ingredients', 25.0, 'kg', 10.0, 'Local Supplier'),
            ('Rice', 'ingredients', 100.0, 'kg', 20.0, 'Bulk Supplier'),
            ('Tomatoes', 'ingredients', 15.0, 'kg', 5.0, 'Farm Fresh'),
            ('Cheese', 'ingredients', 8.0, 'kg', 3.0, 'Dairy Corp'),
            ('Coffee Beans', 'beverages', 12.0, 'kg', 4.0, 'Premium Beans Co'),
            ('Cleaning Supplies', 'supplies', 50.0, 'pieces', 10.0, 'Clean Corp'),
            ('Plates', 'supplies', 200.0, 'pieces', 20.0, 'Dishware Inc'),
            ('Oven', 'equipment', 2.0, 'pieces', 0.0, 'Kitchen Equip Co'),
        ]

        for name, category, qty, unit, threshold, supplier in inventory_data:
            InventoryItem.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'quantity': qty,
                    'unit': unit,
                    'minimum_threshold': threshold,
                    'supplier': supplier
                }
            )
            self.stdout.write(f'Created inventory item: {name}')

        # Create sample shifts for staff
        try:
            chef_staff = Staff.objects.get(user__username='chef1')
            Shift.objects.get_or_create(
                staff=chef_staff,
                date=date.today(),
                defaults={
                    'start_time': time(9, 0),
                    'end_time': time(17, 0),
                    'role': 'chef'
                }
            )
            self.stdout.write('Created sample shift for chef')
        except Staff.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS('Initial data populated successfully!'))

from django.test import TestCase
from .models import Order, BaseEntity

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            accountId=1,
            amount=100.00,
            status='Pending',
            description='Test order',
            content='Order content',
            notes='Some notes',
            method='Credit Card'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.accountId, 1)
        self.assertEqual(self.order.amount, 100.00)
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.description, 'Test order')
        self.assertEqual(self.order.content, 'Order content')
        self.assertEqual(self.order.notes, 'Some notes')
        self.assertEqual(self.order.method, 'Credit Card')

class BaseEntityModelTest(TestCase):
    def setUp(self):
        self.base_entity = BaseEntity.objects.create(
            createBy='admin',
            createAt='2023-01-01T00:00:00Z',
            updateBy='admin',
            updateAt='2023-01-01T00:00:00Z',
            deleteBy=None,
            deleteAt=None
        )

    def test_base_entity_creation(self):
        self.assertEqual(self.base_entity.createBy, 'admin')
        self.assertEqual(self.base_entity.createAt, '2023-01-01T00:00:00Z')
        self.assertEqual(self.base_entity.updateBy, 'admin')
        self.assertEqual(self.base_entity.updateAt, '2023-01-01T00:00:00Z')
        self.assertIsNone(self.base_entity.deleteBy)
        self.assertIsNone(self.base_entity.deleteAt)
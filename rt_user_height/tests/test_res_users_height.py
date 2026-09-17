from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestResUsersHeight(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'Height Test User',
            'login': 'height_test_user',
            'email': 'height_test_user@example.com',
        })

    def test_conversion_180_cm(self):
        self.user.height = 180
        self.assertEqual(self.user.height_ft, 5)
        self.assertAlmostEqual(self.user.height_in, 10.9, places=1)
        self.assertEqual(self.user.height_display, '5 ft 10.9 in')

    def test_conversion_exact_feet(self):
        self.user.height = 182.88
        self.assertEqual(self.user.height_ft, 6)
        self.assertAlmostEqual(self.user.height_in, 0.0, places=1)
        self.assertEqual(self.user.height_display, '6 ft')

    def test_conversion_below_one_foot(self):
        self.user.height = 25.4
        self.assertEqual(self.user.height_ft, 0)
        self.assertAlmostEqual(self.user.height_in, 10.0, places=1)
        self.assertEqual(self.user.height_display, '10 in')

    def test_conversion_inches_only(self):
        self.user.height = 50.8
        self.assertEqual(self.user.height_ft, 1)
        self.assertAlmostEqual(self.user.height_in, 8.0, places=1)
        self.assertEqual(self.user.height_display, '1 ft 8 in')

    def test_no_height(self):
        self.user.height = 0
        self.assertFalse(self.user.height_display)
        self.assertEqual(self.user.height_ft, 0)
        self.assertEqual(self.user.height_in, 0.0)

    def test_negative_height_rejected(self):
        with self.assertRaises(ValidationError):
            self.user.height = -5

    def test_unrealistic_height_rejected(self):
        with self.assertRaises(ValidationError):
            self.user.height = 400

    def test_conversion_70_kg(self):
        self.user.weight = 70
        self.assertAlmostEqual(self.user.weight_lbs, 154.3, places=1)
        self.assertEqual(self.user.weight_display, '154.3 lbs')

    def test_conversion_100_kg(self):
        self.user.weight = 100
        self.assertAlmostEqual(self.user.weight_lbs, 220.5, places=1)
        self.assertEqual(self.user.weight_display, '220.5 lbs')

    def test_conversion_whole_pounds(self):
        self.user.weight = 45.3592
        self.assertAlmostEqual(self.user.weight_lbs, 100.0, places=1)
        self.assertEqual(self.user.weight_display, '100 lbs')

    def test_no_weight(self):
        self.user.weight = 0
        self.assertFalse(self.user.weight_display)
        self.assertEqual(self.user.weight_lbs, 0.0)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValidationError):
            self.user.weight = -10

    def test_unrealistic_weight_rejected(self):
        with self.assertRaises(ValidationError):
            self.user.weight = 600

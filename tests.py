import time
from unittest import TestCase, main
from unittest.mock import Mock, patch
from lemonade_stand import LemonadeStand, NotEnoughLemonsException

class TestLemonadeStandCreation(TestCase):
    def test_plain_creation(self):
        """ Creating a plain lemonade stand works """
        stand = LemonadeStand(10, 1.23)
        self.assertEqual(stand.supply, 10)
        self.assertAlmostEqual(stand.price, 1.23, delta=0.001)
        self.assertListEqual(stand.sales, [])

    def test_wrong_input_type(self):
        with self.assertRaises(ValueError):
            stand = LemonadeStand('foo', 'bar')

    def test_nonsense_input(self):
        with self.assertRaises(ValueError):
            stand = LemonadeStand(-10, 1.23)
        with self.assertRaises(ValueError):
            stand = LemonadeStand(10, -1.23)

class TestLemonadeStandSale(TestCase):
    def setUp(self):
        self.stand = LemonadeStand(10, 1.23)
    
    def test_price_calculation(self):
        total_price = self.stand.get_total(50)
        self.assertAlmostEqual(total_price, 50 * self.stand.price, delta=0.001)

    def test_correct_sale(self):
        self.stand.supply = 10 # Force there to be enough supply
        amount = 5
        expected_income = self.stand.get_total(amount)
        sales_count_old = len(self.stand.sales)

        with patch('lemonade_stand.time.time') as mock_time:
            mock_time.return_value = 1234
            sale = self.stand.sell(amount)

        self.assertEqual(sale['amount'], amount)
        self.assertAlmostEqual(sale['income'], expected_income, delta=0.001)
        self.assertEqual(sale['time'], 1234)

        self.assertEqual(len(self.stand.sales), sales_count_old+1)
        self.assertDictEqual(sale, self.stand.sales[-1])

    def test_not_enough(self):
        self.stand.supply = 0
        with self.assertRaises(NotEnoughLemonsException):
            self.stand.sell(1)

class TestLemonadeStandAggregates(TestCase):
    def setUp(self):
        self.mock_time = Mock()
        self.mock_time.return_value = 1000

        self.stand = LemonadeStand(20, 2.50)
        with patch('lemonade_stand.time.time', self.mock_time):
            self.stand.sell(2)
            self.stand.sell(3)
            self.stand.sell(5)
            
    def test_totals(self):
        self.assertEqual(self.stand.total_lemonades_sold(), 10)
        self.assertAlmostEqual(self.stand.total_income(), 10 * self.stand.price)

    def test_time_intervals(self):
        self.mock_time.return_value = 3000
        with patch('lemonade_stand.time.time', self.mock_time):
            self.stand.sell(4)

        time_start, time_end = self.stand.sale_window()
        self.assertEqual(time_start, 1000)
        self.assertEqual(time_end, 3000)

    def test_time_interval_without_sales_error(self):
        self.stand.sales = []
        with self.assertRaises(ValueError):
            self.stand.sale_window()

if __name__ == '__main__': main()

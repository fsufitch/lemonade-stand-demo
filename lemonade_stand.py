import time

class NotEnoughLemonsException(Exception): pass

class LemonadeStand(object):
    def __init__(self, num_lemons, price):
        self.supply = int(num_lemons)
        self.price = float(price)
        if self.supply < 0:
            raise ValueError("Supply cannot be negative")
        if self.price <= 0:
            raise ValueError("Price must be positive")
        self.sales = []

    def get_total(self, num_lemonades):
        """ Get the total cost of buying a number of lemonades """
        return self.price * num_lemonades

    def sell(self, num_lemonades):
        """ Sell a lemonade, but only if supply is available """
        if num_lemonades > self.supply:
            raise NotEnoughLemonsException("Not enough supply for that many lemonades")

        income = self.get_total(num_lemonades)
        timestamp = time.time()

        sale = {
            'time': timestamp,
            'amount': num_lemonades,
            'income': income,
        }

        self.sales.append(sale)
        self.supply -= num_lemonades

        return sale

    def total_lemonades_sold(self):
        return sum([s['amount'] for s in self.sales])

    def total_income(self):
        return sum([s['income'] for s in self.sales])

    def sale_window(self):
        if not self.sales:
            raise ValueError("No sales yet, cannot calculate sales window")
        sale_window_start = self.sales[0]['time']
        sale_window_end = self.sales[-1]['time']
        return sale_window_start, sale_window_end

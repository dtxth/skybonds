from functools import lru_cache

BOND_NOMINAL = 1000
MONTHLY_PROFIT = 30


class Traider:
    amount_days = None 
    max_day_lots = None 
    wallet = None

    bonds = []
    income = None

    def __init__(self, amount_days, max_day_lots, wallet):
        self.amount_days = amount_days
        self.max_day_lots = max_day_lots
        self.wallet = wallet

    def add_bond(self, bond):
        self.bonds.append(bond)


class Bond:
    day = None
    name = None
    price = None
    amount = None


    full_price = None # full lot price
    full_income = None # full lot income

    def profitability(self, amount_days):
        return amount_days - self.day + MONTHLY_PROFIT  

    def income(self):
        return round((BOND_NOMINAL - self.price / 100 * 1000), 1)  

    def __init__(self, day , name, price, amount, amount_days):
        self.day = day
        self.name = name
        self.price = price
        self.amount = amount

        self.full_price = round((self.price / 100 * 1000 * self.amount), 1)
        self.full_income = (self.income() + self.profitability(amount_days)) * amount


traider = Traider(2, 2, 8000)
bonds = []
bonds.append(Bond(1, 'alfa-05', 100.2, 2, traider.amount_days))
bonds.append(Bond(2, 'alfa-05', 101.5, 5, traider.amount_days))
bonds.append(Bond(2, 'gazprom-17', 100.0, 2, traider.amount_days))
bonds.append(Bond(2, 'my', 98.0, 2, traider.amount_days))



@lru_cache(maxsize=None)  # cache all calls
def best_value(nitems, weight_limit):
    if nitems == 0:  # no items
        return 0  # zero value
    elif bonds[nitems - 1].full_price > weight_limit:
        # new item is heavier than the current weight limit
        return best_value(nitems - 1, weight_limit)  # don't include new item
    else:
        return max(  # max of with and without the new item
            best_value(nitems - 1, weight_limit),  # without
            best_value(nitems - 1, weight_limit - bonds[nitems - 1].full_price)
            + bonds[nitems - 1].full_income)  # with the new item


def choose_bonds_to_buy(traider, bonds):
    weight_limit = traider.wallet
    for i in reversed(range(len(bonds))):
        if best_value(i + 1, weight_limit) > best_value(i, weight_limit):
            # better with the i-th item
            traider.add_bond(bonds[i])  # include it in the result
            weight_limit -= bonds[i].full_price
    traider.income = sum([ x.full_income for x in traider.bonds])


choose_bonds_to_buy(traider, bonds)

print("choosed bonds ")
print([ (x.name, x.price, x.amount) for x in traider.bonds])
print("income: ", traider.income)
print(best_value.cache_info())

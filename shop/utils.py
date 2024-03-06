class CalculateMoney:
    def sum_price_count(self, price: [float, int], quantity: [float, int], discount: int = None, nds: int = None):
        result = round(quantity * price, 2)
        if discount:
            result = round(result * (1-(discount/100)), 2)
        if nds:
            result = round(result * (1 - (nds / 100)), 2)
        return result

    def sum_price(self, prices: list, discount: int = None, nds: int = None):
        result = sum(prices)
        if discount:
            result = round(result * (1-(discount/100)), 2)
        if nds:
            result = round(result * (1 - (discount / 100)), 2)
        return result

def sum_price_count(price: [float, int], quantity: [float, int], discount: int = None, nds: int = None):
    return CalculateMoney().sum_price_count(price, quantity, discount, nds)
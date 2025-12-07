from functools import wraps
from itertools import groupby


def group_by_quantity(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        inventory = await func(*args, **kwargs)

        consumable = []
        permanent = []
        for item in inventory:
            if item["quantity"]:
                consumable.append(item)
            else:
                permanent.append(item)

        consumable = [
            {"quantity": quantity, "products": list(products)}
            for quantity, products in groupby(consumable, key=lambda q: q["quantity"])
        ]

        return {"consumable": consumable, "permanent": permanent}

    return wrapper

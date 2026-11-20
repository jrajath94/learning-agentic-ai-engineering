"""Original service behavior."""


def invoice_total(amounts: list[int]) -> int:
    if any(type(amount) is not int or amount < 0 for amount in amounts):
        raise ValueError("each amount must be a nonnegative integer")

    subtotal = sum(amounts)
    tax = round(subtotal * 0.0825)
    return subtotal + tax

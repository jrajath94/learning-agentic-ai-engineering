"""Compute invoice totals in integer cents."""


def invoice_total(amounts: list[int], discount_cents: int = 0) -> int:
    if any(type(amount) is not int or amount < 0 for amount in amounts):
        raise ValueError("each amount must be a nonnegative integer")
    if type(discount_cents) is not int or discount_cents < 0:
        raise ValueError("discount must be a nonnegative integer")

    subtotal = sum(amounts)
    taxable = max(0, subtotal - discount_cents)
    tax = (taxable * 825 + 5_000) // 10_000
    return taxable + tax

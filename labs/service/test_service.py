import os
import unittest

if os.environ.get("LAB_BASELINE") == "1":
    from baseline import invoice_total
else:
    from service import invoice_total


class InvoiceTests(unittest.TestCase):
    def test_existing_call(self):
        self.assertEqual(invoice_total([100, 200]), 325)

    def test_empty_invoice(self):
        self.assertEqual(invoice_total([]), 0)

    def test_half_cent_rounds_up(self):
        self.assertEqual(invoice_total([200]), 217)

    def test_discount_reduces_taxable_amount(self):
        self.assertEqual(invoice_total([200, 100], discount_cents=100), 217)

    def test_discount_does_not_create_credit(self):
        self.assertEqual(invoice_total([100], discount_cents=101), 0)

    def test_large_invoice_uses_exact_arithmetic(self):
        self.assertEqual(invoice_total([10**20 + 200]), 108_250_000_000_000_000_217)

    def test_invalid_amounts(self):
        for amount in (-1, True, 1.5):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                invoice_total([amount])

    def test_invalid_discounts(self):
        for discount in (-1, True, 1.5):
            with self.subTest(discount=discount), self.assertRaises(ValueError):
                invoice_total([100], discount_cents=discount)

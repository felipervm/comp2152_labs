# ============================================================
#  WEEK 09 LAB — Q3: UNIT TESTING
#  COMP2152 — Felipe Mattos
# ============================================================

import unittest


# --- Functions to test (provided) ---

def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit: c * 9/5 + 32"""
    return c * 9 / 5 + 32


def is_valid_ip(address):
    """Return True if address is a valid IPv4 string (4 octets, 0-255)."""
    try:
        parts = address.split(".")
        if len(parts) != 4:
            return False
        for p in parts:
            if int(p) < 0 or int(p) > 255:
                return False
        return True
    except (ValueError, AttributeError):
        return False


def fizzbuzz(n):
    """Return 'FizzBuzz', 'Fizz', 'Buzz', or str(n)."""
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


class TestCelsius(unittest.TestCase):

    def test_freezing(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32.0)

    def test_boiling(self):
        self.assertEqual(celsius_to_fahrenheit(100), 212.0)

    def test_negative(self):
        self.assertEqual(celsius_to_fahrenheit(-40), -40.0)


class TestValidIP(unittest.TestCase):

    def test_valid(self):
        self.assertTrue(is_valid_ip("192.168.1.1"))

    def test_invalid_octet(self):
        self.assertFalse(is_valid_ip("256.1.1.1"))

    def test_too_few_parts(self):
        self.assertFalse(is_valid_ip("1.2.3"))

    def test_empty(self):
        self.assertFalse(is_valid_ip(""))


class TestFizzBuzz(unittest.TestCase):

    def test_fizz(self):
        self.assertEqual(fizzbuzz(3), "Fizz")

    def test_buzz(self):
        self.assertEqual(fizzbuzz(5), "Buzz")

    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(15), "FizzBuzz")

    def test_number(self):
        self.assertEqual(fizzbuzz(7), "7")


if __name__ == "__main__":
    unittest.main()
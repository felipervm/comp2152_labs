# ============================================================
#  WEEK 11 LAB — Q2: PASSWORD STRENGTH CHECKER
#  COMP2152 — Felipe da Rocha Vieira Mattos
# ============================================================
#
#  For the term project, you'll be looking for weak passwords
#  on 0x10.cloud. This class helps you understand what makes
#  a password weak or strong.
#
# ============================================================

class PasswordChecker:

    def __init__(self):
        self.common_passwords = [
            "admin", "password", "123456", "root",
            "guest", "letmein", "welcome"
        ]
        self.history = []

    def check_common(self, password):
        return password.lower() in self.common_passwords

    def check_strength(self, password):
        has_length = len(password) >= 8
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)

        return {
            "length": has_length,
            "digit": has_digit,
            "special": has_special
        }

    def evaluate(self, password):
        if self.check_common(password):
            result = "WEAK (common password)"
        else:
            strength = self.check_strength(password)
            score = sum(strength.values())

            if score <= 1:
                result = "WEAK"
            elif score == 2:
                result = "MEDIUM"
            else:
                result = "STRONG"

        self.history.append((password, result))
        return result


if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: PASSWORD STRENGTH CHECKER")
    print("=" * 60)

    checker = PasswordChecker()

    test_passwords = ["admin", "hello", "hello123", "MyP@ss99", "p@ssw0rd!", "root"]

    print("\n--- Checking Passwords ---")
    for pw in test_passwords:
        result = checker.evaluate(pw)
        if result:
            print(f"  {pw:<15} → {result}")

    print("\n--- Check History ---")
    if hasattr(checker, 'history') and checker.history:
        for pw, result in checker.history:
            print(f"  {pw:<15} : {result}")
    else:
        print("  (no history)")

    print("\n" + "=" * 60)
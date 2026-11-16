"""Simple car rental system used to demonstrate static code analysis."""

import hashlib
import os
import re
import secrets
import sqlite3
import tempfile
from datetime import datetime

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car to the rental fleet."""
    if not plate:
        raise ValueError("Plate number is required")

    if features is None:
        features = []

    fleet[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": features,
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Register a customer in the database."""
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )


def find_customer(name):
    """Return customers whose name matches the supplied value."""
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Rent a car and return the calculated rental cost."""
    if not find_customer(customer):
        raise ValueError("Customer not registered")

    days = (
        datetime.strptime(end, "%Y-%m-%d")
        - datetime.strptime(start, "%Y-%m-%d")
    ).days
    cost = days * fleet[plate]["rate"]

    bookings.append(
        {
            "code": booking_code(),
            "plate": plate,
            "customer": customer,
            "days": days,
            "cost": cost,
        }
    )
    return cost


def return_car(plate, km_driven):
    """Return a rented car and calculate any extra kilometre charge."""
    if plate not in fleet:
        return None

    fleet[plate]["available"] = True

    if km_driven > 300:
        return (km_driven - 300) * 5

    return None


def booking_code():
    """Generate a secure random booking code."""
    return f"BK-{secrets.randbelow(90000) + 10000}"


def licence_hash(licence):
    """Return a SHA-256 hash of a driving licence."""
    return hashlib.sha256(licence.encode()).hexdigest()


def apply_promo(rule, amount):
    """Apply a validated multiplication-based promotional rule."""
    match = re.fullmatch(
        r"\s*amount\s*=\s*amount\s*\*\s*(\d+(?:\.\d+)?)\s*",
        rule,
    )

    if not match:
        raise ValueError("Unsupported promo rule")

    multiplier = float(match.group(1))
    return amount * multiplier


def is_valid_plate(plate):
    """Check whether a vehicle registration number is valid."""
    pattern = r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
    return bool(re.fullmatch(pattern, plate))


def write_receipt(booking):
    """Write booking information to a securely created receipt file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8",
    ) as receipt_file:
        receipt_file.write(
            f"Booking {booking['code']}: {booking['plate']} "
            f"for {booking['days']} days = Rs.{booking['cost']}\n"
        )
        path = receipt_file.name

    os.chmod(path, 0o600)
    return path


def admin_login(user, password):
    """Validate administrator credentials using an environment variable."""
    expected_password = os.environ.get("CAR_RENTAL_ADMIN_PASSWORD")

    if expected_password is None:
        return False

    return user == "admin" and secrets.compare_digest(
        password,
        expected_password,
    )


def available_cars():
    """Return the registration numbers of currently available cars."""
    return [
        plate
        for plate, car in fleet.items()
        if car["available"]
    ]


def main():
    """Demonstrate the main car rental operations."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", -500)

    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")

    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print(
        "Rent Swift again:",
        rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"),
    )
    print(
        "Rent Innova:",
        rent_car("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"),
    )

    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Return unknown car:", return_car("XX00XX0000", 50))
    print("Promo price:", apply_promo("amount = amount * 0.9", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))

    admin_password = os.environ.get("CAR_RENTAL_ADMIN_PASSWORD", "")
    print("Admin:", admin_login("admin", admin_password))

    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


main()

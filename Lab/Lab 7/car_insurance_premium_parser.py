
from datetime import datetime


def normalize_registration(plate):
    # Return an empty string for invalid input
    if not isinstance(plate, str):
        return ""

    plate = plate.strip().upper()

    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')

    if not plate.isalnum():
        return ""

    return plate


def total_claim_amount(text):
    # Check that the input is a non-empty string
    if not isinstance(text, str) or not text.strip():
        return None

    total = 0

    for amount in text.split(';'):
        amount = amount.strip()

        # Claim amounts should be non-negative integers
        if not amount or not amount.isdecimal():
            return None

        try:
            total += int(amount)
        except ValueError:
            return None

    return total


def driver_age(dob, current_year=2026):
    # Check input before splitting or converting
    if not isinstance(dob, str) or not isinstance(current_year, int):
        return None

    try:
        date = datetime.strptime(dob.strip(), "%d/%m/%Y")

        if date.year > current_year:
            return None

        return current_year - date.year

    except ValueError:
        return None


def main():
    print("SRN: PES2UG24CS903")

    print("\n==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    registration = normalize_registration(value)
    print("Normalized registration:", registration or "Invalid registration")

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    total = total_claim_amount(value)
    print("Total claimed:", total if total is not None else "Invalid claim amounts")

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    age = driver_age(value)
    print("Driver age in 2026:", age if age is not None else "Invalid date of birth")


if __name__ == "__main__":
    main()

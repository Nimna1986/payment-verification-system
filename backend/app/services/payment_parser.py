import re

from sqlalchemy import text


def parse_payment_text(text: str) -> dict:
    """
    Extract structured payment information from OCR text.
    """

    result = {
        "reference_number": None,
        "from_account": None,
        "beneficiary_account": None,
        "beneficiary_name": None,
        "amount": None,
        "status": None,
        "payment_option": None,
    }

    # Payment status
    status_match = re.search(
        r"\b(Successful|Failed|Pending)\b",
        text,
        re.IGNORECASE
    )

    if status_match:
        result["status"] = status_match.group(1).lower()

    # Reference Number
    reference_match = re.search(
        r"Reference Number\s*\n\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if reference_match:
        result["reference_number"] = reference_match.group(1)

    # From Account
    from_account_match = re.search(
        r"From Account\s*\n\s*LKR\s+([0-9-]+)",
        text,
        re.IGNORECASE
    )

    if from_account_match:
        result["from_account"] = from_account_match.group(1)

    # Beneficiary Account Number
    beneficiary_account_match = re.search(
        r"Beneficiary Account Number\s*\n\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if beneficiary_account_match:
        result["beneficiary_account"] = beneficiary_account_match.group(1)

    # Beneficiary Name
    beneficiary_name_match = re.search(
        r"Beneficiary Name\s*\n\s*([A-Z][A-Z\s]+)",
        text,
        re.IGNORECASE
    )

    if beneficiary_name_match:
        result["beneficiary_name"] = (
            beneficiary_name_match.group(1).strip()
        )

    # Transfer Amount
    amount_match = re.search(
        r"Transfer Amount\s*\n\s*LKR\s*([\d,]+(?:\.\d{2})?)",
        text,
        re.IGNORECASE
    )

    if amount_match:
        amount_string = amount_match.group(1).replace(",", "")
        result["amount"] = float(amount_string)

    # Payment Option
    payment_option_match = re.search(
        r"Payment Option\s*\n\s*(.+)",
        text,
        re.IGNORECASE
    )

    if payment_option_match:
        result["payment_option"] = (
            payment_option_match.group(1).strip()
        )

    return result
from fastapi import HTTPException

def calculate_fees(amount: float) -> tuple[float, float, float]:
    """
    Calculates the transaction fees.
    Enforces the minimum transaction amount.
    Returns a tuple of (total_fee, sender_fee, recipient_fee).
    """
    if amount < 5.00:
        raise HTTPException(status_code=400, detail="Transaction amount must be at least $5.00")

    total_fee = max(1.50, (0.03 * amount) + 0.74)
    sender_fee = total_fee / 2
    recipient_fee = total_fee / 2
    return round(total_fee, 2), round(sender_fee, 2), round(recipient_fee, 2)

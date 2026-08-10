def total_after_discount(subtotal: float, discount_percent: float) -> float:
    """Return the subtotal after applying a percentage discount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount must be between 0 and 100")
    return subtotal - discount_percent

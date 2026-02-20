from app.models.schemas import TransactionInput


BLOCKED_17_5_KEYWORDS = {'motor car', 'food', 'club', 'health insurance'}


def is_valid_gstin(gstin: str | None) -> bool:
    if not gstin:
        return False
    return len(gstin) == 15 and gstin[:2].isdigit()


def compute_gst(transactions: list[TransactionInput]) -> dict:
    output_gst = 0.0
    itc_claimed = 0.0
    itc_blocked = 0.0
    mismatch_2a = 0

    for txn in transactions:
        amount = abs(txn.amount)
        gst_value = amount * 0.18 if amount >= 5000 else 0.0
        if txn.amount > 0:
            output_gst += gst_value
        else:
            itc_claimed += gst_value
            desc = txn.description.lower()
            if any(k in desc for k in BLOCKED_17_5_KEYWORDS):
                itc_blocked += gst_value
            if not is_valid_gstin(txn.counterparty_gstin):
                mismatch_2a += 1

    return {
        'output_gst': round(output_gst, 2),
        'itc_claimed': round(itc_claimed, 2),
        'itc_blocked_u_s_17_5': round(itc_blocked, 2),
        'invoice_gstr2a_mismatches': mismatch_2a,
    }

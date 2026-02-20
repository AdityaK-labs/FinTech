from app.models.schemas import TransactionInput


SECTION_RATES = {
    '194C': 0.01,
    '194J': 0.10,
    '194H': 0.05,
    'GST_51': 0.02,
}


def detect_section(description: str) -> str | None:
    d = description.lower()
    if 'contract' in d or 'labour' in d:
        return '194C'
    if 'consult' in d or 'professional' in d:
        return '194J'
    if 'commission' in d or 'broker' in d:
        return '194H'
    if 'government vendor' in d:
        return 'GST_51'
    return None


def compute_tds(transactions: list[TransactionInput]) -> dict:
    obligations = []
    total = 0.0
    for txn in transactions:
        if abs(txn.amount) < 30000:
            continue
        section = detect_section(txn.description)
        if not section:
            continue
        value = abs(txn.amount) * SECTION_RATES[section]
        total += value
        obligations.append(
            {
                'description': txn.description,
                'section': section,
                'tds_amount': round(value, 2),
            }
        )
    return {
        'total_tds': round(total, 2),
        'obligations': obligations,
        'returns_ready': ['26Q', 'GSTR-7'],
    }

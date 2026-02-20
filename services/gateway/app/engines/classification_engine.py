from app.models.schemas import TransactionInput


PERSONAL_HINTS = {'swiggy', 'zomato', 'netflix', 'personal', 'family'}
CAPITAL_HINTS = {'machinery', 'equipment', 'asset', 'vehicle'}
LOAN_HINTS = {'loan', 'emi', 'nbfc', 'finance'}


def classify_transaction(txn: TransactionInput) -> dict:
    desc = txn.description.lower()
    tag = {
        'revenue': txn.amount > 0,
        'expense': txn.amount < 0,
        'personal': any(h in desc for h in PERSONAL_HINTS),
        'capital': any(h in desc for h in CAPITAL_HINTS),
        'loan': any(h in desc for h in LOAN_HINTS),
        'gst_applicable': abs(txn.amount) >= 5000,
        'tds_applicable': abs(txn.amount) >= 30000,
    }
    return tag

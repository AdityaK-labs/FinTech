def generate_risk_score(payload: dict) -> dict:
    mismatch = abs(payload['turnover_gst'] - payload['turnover_itr'])
    turnover_penalty = min(25, mismatch / max(payload['turnover_itr'], 1) * 100)

    presumptive_penalty = 0
    if payload['presumptive_income_rate'] < 6:
        presumptive_penalty = 12

    advance_tax_gap = max(0, payload['expected_advance_tax'] - payload['advance_tax_paid'])
    advance_tax_penalty = min(20, advance_tax_gap / max(payload['expected_advance_tax'], 1) * 100)

    unsecured_penalty = 10 if payload['unsecured_loans'] > 1_000_000 else 0
    tds_penalty = min(15, payload['missed_tds_count'] * 3)

    score = min(100, turnover_penalty + presumptive_penalty + advance_tax_penalty + unsecured_penalty + tds_penalty)

    reasons = []
    if turnover_penalty:
        reasons.append('Turnover mismatch between GST and ITR filings')
    if presumptive_penalty:
        reasons.append('Section 44AD presumptive rate appears below expected benchmark')
    if advance_tax_penalty:
        reasons.append('Advance tax gap detected')
    if unsecured_penalty:
        reasons.append('Material unsecured loans require verification')
    if tds_penalty:
        reasons.append('Recurring TDS deduction failures observed')

    return {'risk_score': round(score, 2), 'reasons': reasons}

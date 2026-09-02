SECRET_FIELDS = {'password','password_hash','api_key','access_token','refresh_token','private_key','secret'}
SENSITIVE_FIELDS = {'passport','passport_number','national_id','bank_account','card_number','cvv'}

class DataAccessError(Exception):
    pass

def classify_field(name: str) -> str:
    key = name.lower()
    if key in SECRET_FIELDS:
        return 'SECRET'
    if key in SENSITIVE_FIELDS:
        return 'SENSITIVE'
    if any(token in key for token in ('email','phone','address')):
        return 'PERSONAL'
    return 'PUBLIC'

def filter_for_agent(data, allowed_scopes: set[str]):
    if not isinstance(data, dict):
        return data
    result = {}
    for key, value in data.items():
        cls = classify_field(key)
        if cls == 'SECRET':
            continue
        if cls == 'SENSITIVE' and 'sensitive_personal_data' not in allowed_scopes:
            continue
        if cls == 'PERSONAL' and 'personal_data' not in allowed_scopes and 'application_data' not in allowed_scopes and 'public_contact_information' not in allowed_scopes:
            continue
        result[key] = value
    return result

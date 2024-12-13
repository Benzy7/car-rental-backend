import random, base64, string, time, hashlib
from django.db import transaction
from core.models.pin_code import PinCode
from .logger import exception_log

@transaction.atomic
def generate_reset_pass_code(user) :
    try :
        pin_code = str(random.randint(100000, 999999))
        PinCode.objects.create(user=user, code=pin_code, code_type=PinCode.RESET_PASSWORD)
        
        return pin_code
    except Exception as e:
        exception_log(e,__file__)
        transaction.set_rollback(True)
        raise e

# def generate_unique_code(identifier):
#     timestamp = str(int(time.time() * 1000))
#     random_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
#     entropy_source = f"{identifier}-{timestamp}-{random_salt}"
    
#     hash_object = hashlib.sha256(entropy_source.encode())
    
#     unique_base64 = base64.urlsafe_b64encode(hash_object.digest()).decode()
    
#     referral_code = ''.join(
#         char for char in unique_base64[:8].upper() 
#         if char.isalnum()
#     )
#     return referral_code

def generate_referral_code(identifier, code_type='partner'):
    if code_type == 'partner':
        first_chars = ''.join(word[0].upper() for word in identifier.split()[:3])
    else:
        first_chars = (identifier.first_name[:2].upper() + identifier.last_name[:2].upper())
    
    timestamp = str(int(time.time() * 1000))
    random_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
   
    if code_type == 'partner':
        entropy_source = f"{identifier}-{timestamp}-{random_salt}"
    else:
        entropy_source = f"{identifier.id}-{identifier.first_name}-{identifier.last_name}-{timestamp}-{random_salt}"
   
    hash_object = hashlib.sha256(entropy_source.encode())
    unique_base64 = base64.urlsafe_b64encode(hash_object.digest()).decode()
    unique_chars = ''.join(
        char for char in unique_base64[:3].upper()
        if char.isalnum()
    )
   
    referral_code = first_chars + unique_chars
    return referral_code.upper()[:8]

def generate_coupon_code(coupon_type, partner_name=None):
    type_prefixes = {
        'discount': 'DS',
        'fixed_discount': 'FD',
        'free_upgrade': 'UP',
        'free_day': 'FD',
        'weekend_special': 'WK',
        'early_bird': 'EB'
    }
    prefix = type_prefixes.get(coupon_type, 'CP')
    
    timestamp = str(int(time.time() * 1000))
    random_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    entropy_source = f"{coupon_type}-{partner_name or ''}-{timestamp}-{random_salt}"
    hash_object = hashlib.sha256(entropy_source.encode())
    unique_base64 = base64.urlsafe_b64encode(hash_object.digest()).decode()
    
    unique_chars = ''.join(
        char for char in unique_base64[:2].upper()
        if char.isalnum()
    )
    coupon_code = (prefix + unique_chars)[:6].upper()
    return coupon_code

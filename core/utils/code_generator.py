import random
import base64
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

def generate_user_referral_code(user):
    unique_string = f"{user.id}-{int(user.created_at.timestamp())}"
    return base64.urlsafe_b64encode(unique_string.encode()).decode()[:8].upper()

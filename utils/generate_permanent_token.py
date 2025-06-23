import secrets
from apps.api.models import PermanentToken


def generate_permanent_token(user):
    """
    为用户生成一个长期 Token，并删除旧的 Token（确保唯一性）。
    """
    # 删除用户已有的 Token
    PermanentToken.objects.filter(user=user).delete()
    # 生成新的 Token
    token_key = secrets.token_urlsafe(32)  # 生成 32 字节的随机字符串
    token = PermanentToken.objects.create(user=user, key=token_key)
    return token.key

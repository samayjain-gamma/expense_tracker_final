from app.core.security import create_access_token, decode_access_token


def create_validate_access_token():
    data = {"user_email": "password1"}
    token = create_access_token(data)

    decoded_token = decode_access_token(token=token)
    assert decoded_token["user_email"] == "password1"

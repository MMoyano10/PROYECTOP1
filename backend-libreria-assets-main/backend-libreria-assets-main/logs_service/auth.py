from fastapi import Header, HTTPException, status

def get_current_admin_id(x_user_id: int = Header(..., alias="X-User-Id")) -> int:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere header X-User-Id"
        )
    return x_user_id

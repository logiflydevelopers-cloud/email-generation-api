import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, status
import traceback
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)

# ----------------------------------
# TEMP: Internet connectivity test
# ----------------------------------
try:
    r = requests.get("https://www.googleapis.com", timeout=5)
    print("🌐 GOOGLE CONNECTIVITY:", r.status_code)
except Exception as e:
    print("❌ NO INTERNET FROM BACKEND:", e)

async def verify_firebase_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Firebase token",
        )

    token = auth_header.split(" ")[1]

    try:
        print("TOKEN LENGTH:", len(token))
        decoded = auth.verify_id_token(
        token,
        clock_skew_seconds=60,
        check_revoked=False
        )
        print("✅ TOKEN VERIFIED")
        print("AUD:", decoded.get("aud"))
        print("ISS:", decoded.get("iss"))
        request.state.user = decoded

    except Exception as e:
        print("❌ FIREBASE VERIFY ERROR ↓↓↓")
        print(str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token",
        )

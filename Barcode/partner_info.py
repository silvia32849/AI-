import db
import requests

# ==========================================
# 제휴사 조회
# ==========================================
def get_partner_info(barcode):

    prefix = barcode[:3]

    target_url = (
        f"{db.SUPABASE_URL}/rest/v1/partners?prefix=eq.{prefix}"
    )

    headers = {
        "apikey": db.SUPABASE_KEY,
        "Authorization": f"Bearer {db.SUPABASE_KEY}"
    }

    try:

        response = requests.get(
            target_url,
            headers=headers
        )

        data = response.json()

    except Exception as e:

        print(f"❌ 시스템 오류: {e}")
        return None

    if not isinstance(data, list):

        print("❌ API 응답 오류")
        print(data)
        return None

    if len(data) == 0:

        print("❌ 등록되지 않은 바코드")
        return None

    return data[0]


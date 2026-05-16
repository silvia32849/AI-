def get_pay_balance(pay_type_name):

    # 간편결제는 항상 결제 가능 처리
    if pay_type_name in [
        "🟩 네이버페이",
        "🟡 카카오페이",
        "🔵 페이코"
    ]:
        return 999999

    balances = {

        "🎁 카카오 선물하기": 3000,
    }

    return balances.get(pay_type_name, 0)
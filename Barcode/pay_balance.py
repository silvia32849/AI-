def get_pay_balance(pay_type_name):

    balances = {

        "카카오톡 선물하기": 3000,

        "🟩 네이버페이": 999999,
        "🟡 카카오페이": 999999,
        "🔵 페이코": 999999,
    }

    return balances.get(pay_type_name, 0)
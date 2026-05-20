def get_pay_balance(pay_type_name):
    
    balances = {
    "카카오톡 선물하기": 3000,
}

    return balances.get(pay_type_name, 0)
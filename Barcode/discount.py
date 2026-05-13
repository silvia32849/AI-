# ==========================================
# 통신사 할인
# ==========================================
def process_telecom_discount(barcode):

    telecom = None
    telecom_discount = 0

    if barcode.startswith("123"):

        telecom = "KT"
        telecom_discount = 10

    elif barcode.startswith("124"):

        telecom = "SKT"
        telecom_discount = 10

    return telecom, telecom_discount


import barcode
from barcode.writer import ImageWriter

code_data = "001777777"

code128 = barcode.get(
    'code128',
    code_data,
    writer=ImageWriter()
)

filename = code128.save("my_barcode")

print("생성 완료:", filename)
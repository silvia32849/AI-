import cv2
import zxingcpp


def scan_code():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:

        success, frame = cap.read()

        if not success:
            continue

        # 바코드/QR 인식
        results = zxingcpp.read_barcodes(frame)

        for result in results:

            data = result.text
            code_type = str(result.format)

            print("인식 성공!")
            print("종류:", code_type)
            print("데이터:", data)

            cap.release()
            cv2.destroyAllWindows()

            return {
                "type": code_type,
                "data": data
            }

        cv2.imshow("Scanner", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return None
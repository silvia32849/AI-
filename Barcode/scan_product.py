import cv2


def scan_barcode():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    detector = cv2.QRCodeDetector()

    while True:

        success, frame = cap.read()

        # 카메라 프레임 읽기 실패
        if not success or frame is None:
            print("프레임 읽기 실패")
            continue

        try:

            data, bbox, _ = detector.detectAndDecode(frame)

            if data:
                print("QR 인식 성공!")
                print("데이터:", data)

                cap.release()
                cv2.destroyAllWindows()

                return data

        except Exception as e:
            print("QR 인식 오류:", e)

        cv2.imshow("QR Scanner", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return None
import { useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Html5Qrcode } from 'html5-qrcode';

const fakeBarcodes = [
  { type: "카카오페이", code: "1234-5678-9012", amount: 10000 },
  { type: "네이버페이", code: "9876-5432-1098", amount: 15000 },
  { type: "쿠폰", code: "5555-6666-7777", amount: 5000 },
];

function BarcodeCameraScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item } = location.state || {};
  const [message, setMessage] = useState('바코드를 카메라에 비춰주세요');
  const html5QrCodeRef = useRef(null);
  const isStarted = useRef(false);

  useEffect(() => {
    if (isStarted.current) return;
    isStarted.current = true;

    const html5QrCode = new Html5Qrcode("reader");
    html5QrCodeRef.current = html5QrCode;

    html5QrCode.start(
      { facingMode: "user" },
      { fps: 10, qrbox: { width: 250, height: 250 } },
      function(decodedText) {
        isStarted.current = false;
        html5QrCode.stop().catch(function() {});
        const fake = fakeBarcodes[Math.floor(Math.random() * fakeBarcodes.length)];
        navigate('/barcode', { state: { item, barcodeData: fake } });
      },
      function() {}
    ).catch(function() {
      setMessage('카메라를 찾을 수 없어요. 카메라 권한을 허용해주세요.');
    });

    return function() {
      if (html5QrCodeRef.current && isStarted.current) {
        html5QrCodeRef.current.stop().catch(function() {});
      }
    };
  }, []);

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🎟️ 바코드 인식</h2>
      <div id="reader" style={styles.reader} />
      <p style={styles.message}>{message}</p>
      <button
        style={styles.cancelBtn}
        onClick={() => navigate('/payment', { state: { item } })}
      >
        취소
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    height: '100vh', backgroundColor: '#fff8f0', gap: '20px'
  },
  title: { fontSize: '36px' },
  reader: { width: '300px', height: '300px' },
  message: { fontSize: '20px', color: '#888' },
  cancelBtn: {
    padding: '12px 30px', fontSize: '18px',
    borderRadius: '10px', border: 'none',
    backgroundColor: '#aaa', color: 'white', cursor: 'pointer'
  },
};

export default BarcodeCameraScreen;
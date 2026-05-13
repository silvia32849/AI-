import { useNavigate, useLocation } from 'react-router-dom';

function BarcodeScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item, barcodeData } = location.state || {};

  const price = item?.price || 0;
  const remain = barcodeData?.amount || 0;
  const isEnough = remain >= price;
  const finalPrice = isEnough ? 0 : price - remain;

  const handleUse = () => {
    if (!isEnough) {
      alert(`잔여금액 ${remain.toLocaleString()}원을 결제합니다.\n나머지 ${(price - remain).toLocaleString()}원은 다른 수단으로 결제해주세요.`);
      navigate('/payment', {
        state: {
          item,
          remainingPrice: price - remain,
        }
      });
      return;
    }
    navigate('/complete', { state: { item, payType: barcodeData?.type, finalPrice: 0 } });
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🎟️ 바코드 결제</h2>

      <div style={styles.barcodeBox}>
        <p style={styles.barcodeNum}>{barcodeData?.code || '----'}</p>
      </div>

      <div style={styles.infoBox}>
        <p>명칭: {barcodeData?.type}</p>
        <p>잔여 금액: {remain.toLocaleString()}원</p>
        <p>받을 금액: {price.toLocaleString()}원</p>
        <p style={{
          ...styles.finalPrice,
          color: isEnough ? '#6f4e37' : '#ff4444'
        }}>
          결제 금액: {finalPrice.toLocaleString()}원
        </p>
        {!isEnough && (
          <p style={styles.warningText}>
            ⚠️ 잔여금액이 부족합니다
          </p>
        )}
      </div>

      <div style={styles.btnWrapper}>
        <button
          style={{ ...styles.btn, backgroundColor: '#aaa' }}
          onClick={() => navigate('/barcode-camera', { state: { item } })}
        >
          🔍 재조회
        </button>
        <button
          style={{
            ...styles.btn,
            backgroundColor: isEnough ? '#6f4e37' : '#ff4444'
          }}
          onClick={handleUse}
        >
          {isEnough ? '✅ 사용' : '💳 잔여금액 결제 후 이동'}
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    height: '100vh', backgroundColor: '#fff8f0', gap: '30px'
  },
  title: { fontSize: '36px' },
  barcodeBox: { textAlign: 'center' },
  barcodeNum: { fontSize: '24px', letterSpacing: '4px', color: '#333' },
  infoBox: {
    backgroundColor: 'white', padding: '30px',
    borderRadius: '15px', fontSize: '20px',
    lineHeight: '2', textAlign: 'center', minWidth: '300px'
  },
  finalPrice: { fontWeight: 'bold', fontSize: '24px' },
  warningText: { color: '#ff4444', fontSize: '18px' },
  btnWrapper: { display: 'flex', gap: '30px' },
  btn: {
    padding: '15px 40px', fontSize: '20px',
    borderRadius: '10px', border: 'none',
    color: 'white', cursor: 'pointer'
  },
};

export default BarcodeScreen;
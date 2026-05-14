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
      <h2 style={styles.title}>바코드 결제</h2>

      <div style={styles.barcodeBox}>
        <p style={styles.barcodeNum}>{barcodeData?.code || '----'}</p>
      </div>

      <div style={styles.infoBox}>
        <div style={styles.infoRow}>
          <span>명칭</span>
          <span style={styles.infoValue}>{barcodeData?.type}</span>
        </div>
        <div style={styles.infoRow}>
          <span>잔여 금액</span>
          <span style={styles.infoValue}>{remain.toLocaleString()}원</span>
        </div>
        <div style={styles.infoRow}>
          <span>받을 금액</span>
          <span style={styles.infoValue}>{price.toLocaleString()}원</span>
        </div>
        <div style={{...styles.infoRow, marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #f0f0f0'}}>
          <span style={styles.finalLabel}>결제 금액</span>
          <span style={{
            ...styles.finalPrice,
            color: isEnough ? '#00754a' : '#d32f2f'
          }}>{finalPrice.toLocaleString()}원</span>
        </div>
        {!isEnough && (
          <p style={styles.warningText}>
            잔여금액이 부족합니다
          </p>
        )}
      </div>

      <div style={styles.btnWrapper}>
        <button
          style={styles.retryBtn}
          onClick={() => navigate('/barcode-camera', { state: { item } })}
        >
          재조회
        </button>
        <button
          style={{
            ...styles.useBtn,
            backgroundColor: isEnough ? '#00754a' : '#d32f2f'
          }}
          onClick={handleUse}
        >
          {isEnough ? '사용' : '다른 결제수단'}
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    height: '100vh', backgroundColor: '#ffffff', gap: '32px'
  },
  title: { fontSize: '32px', color: '#00754a', fontWeight: 'bold' },
  barcodeBox: { 
    textAlign: 'center', 
    padding: '20px',
    backgroundColor: '#fafafa',
    borderRadius: '8px'
  },
  barcodeNum: { fontSize: '22px', letterSpacing: '3px', color: '#000000', fontWeight: '500' },
  infoBox: {
    backgroundColor: '#fafafa', padding: '32px',
    borderRadius: '12px', minWidth: '400px'
  },
  infoRow: {
    display: 'flex', justifyContent: 'space-between',
    fontSize: '18px', marginBottom: '12px',
    color: '#000000'
  },
  infoValue: { fontWeight: '500' },
  finalLabel: { fontSize: '20px', fontWeight: 'bold' },
  finalPrice: { fontSize: '24px', fontWeight: 'bold' },
  warningText: { 
    color: '#d32f2f', fontSize: '16px', 
    textAlign: 'center', marginTop: '12px' 
  },
  btnWrapper: { display: 'flex', gap: '20px' },
  retryBtn: {
    padding: '14px 36px', fontSize: '18px',
    borderRadius: '25px', border: '2px solid #00754a',
    backgroundColor: '#ffffff', color: '#00754a',
    cursor: 'pointer', fontWeight: 'bold'
  },
  useBtn: {
    padding: '14px 36px', fontSize: '18px',
    borderRadius: '25px', border: 'none',
    color: '#ffffff', cursor: 'pointer', fontWeight: 'bold'
  },
};

export default BarcodeScreen;
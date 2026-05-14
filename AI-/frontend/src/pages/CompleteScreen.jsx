import { useNavigate, useLocation } from 'react-router-dom';

function CompleteScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item, payType, barcodeData } = location.state || {};

  console.log(location.state);

  return (
    <div style={styles.container}>
      <div style={styles.checkmark}>✓</div>
      <h2 style={styles.title}>주문 완료</h2>
      <div style={styles.infoBox}>
        <div style={styles.infoRow}>
          <span>메뉴</span>
          <span style={styles.infoValue}>{item?.name}</span>
        </div>
        <div style={styles.infoRow}>
          <span>결제 방법</span>
          <span style={styles.infoValue}>{payType}</span>
        </div>
        <div style={{...styles.infoRow, marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #f0f0f0'}}>
          <div style={styles.infoRow}>
          <span>원가</span>
          <span style={styles.infoValue}>
            {barcodeData?.original_price?.toLocaleString()}원
          </span>
        </div>

        <div style={styles.infoRow}>
          <span>통신사 할인</span>
          <span style={styles.infoValue}>
            -{barcodeData?.telecom_discount?.toLocaleString()}원
          </span>
        </div>

        <div style={styles.infoRow}>
          <span>{barcodeData?.telecom} 할인</span>
          <span style={styles.infoValue}>
            -{barcodeData?.telecom_discount?.toLocaleString()}원
          </span>
        </div>
          <span style={styles.totalLabel}>결제 금액</span>
          <span style={styles.totalPrice}>{(barcodeData?.final_price ?? item?.price)?.toLocaleString()}원</span>
        </div>
      </div>
      <div style={styles.btnWrapper}>
        <button style={styles.receiptBtn}>
          영수증 출력
        </button>
        <button style={styles.skipBtn} onClick={() => navigate('/')}>
          미출력
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
  checkmark: { 
    fontSize: '80px', 
    color: '#00754a',
    width: '120px',
    height: '120px',
    border: '4px solid #00754a',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold'
  },
  title: { fontSize: '36px', color: '#000000', fontWeight: 'bold' },
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
  totalLabel: { fontSize: '20px', fontWeight: 'bold' },
  totalPrice: { fontSize: '24px', color: '#00754a', fontWeight: 'bold' },
  btnWrapper: { display: 'flex', gap: '20px' },
  receiptBtn: {
    padding: '14px 36px', fontSize: '18px',
    borderRadius: '25px', border: 'none',
    backgroundColor: '#00754a', color: '#ffffff',
    cursor: 'pointer', fontWeight: 'bold'
  },
  skipBtn: {
    padding: '14px 36px', fontSize: '18px',
    borderRadius: '25px', border: '2px solid #d4e9e2',
    backgroundColor: '#ffffff', color: '#000000',
    cursor: 'pointer', fontWeight: 'bold'
  },
};

export default CompleteScreen;

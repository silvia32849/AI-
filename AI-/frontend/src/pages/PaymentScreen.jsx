import { useNavigate, useLocation } from 'react-router-dom';

function PaymentScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item, orderType, remainingPrice } = location.state || {};

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>결제 수단 선택</h2>

      <div style={styles.orderInfo}>
        <p>{orderType} | {item?.name}</p>
      </div>

      <div style={styles.btnWrapper}>
        <button
          style={styles.btn}
          onClick={() => navigate('/complete', { state: { item, payType: '카드' } })}
        >
          💳 카드 결제
        </button>
        <button
          style={styles.btn}
          onClick={() => navigate('/barcode-camera', { state: { item } })}
        >
          🎟️ 바코드 결제
        </button>
      </div>

      <div style={styles.totalBar}>
        결제 금액: <strong>{(remainingPrice ?? item?.price)?.toLocaleString()}원</strong>
        {remainingPrice && (
          <p style={styles.warningText}>
            ⚠️ 바코드 차감 후 남은 금액입니다
          </p>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    height: '100vh', backgroundColor: '#fff8f0', gap: '40px'
  },
  title: { fontSize: '36px', marginBottom: '10px' },
  orderInfo: { fontSize: '20px', color: '#888' },
  btnWrapper: { display: 'flex', gap: '40px' },
  btn: {
    width: '200px', height: '200px', fontSize: '24px',
    borderRadius: '20px', border: 'none',
    backgroundColor: '#6f4e37', color: 'white', cursor: 'pointer'
  },
  totalBar: {
    fontSize: '24px', textAlign: 'center'
  },
  warningText: {
    color: '#ff4444', fontSize: '18px', marginTop: '8px'
  },
};

export default PaymentScreen;
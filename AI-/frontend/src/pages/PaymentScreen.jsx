import { useNavigate, useLocation } from 'react-router-dom';

function PaymentScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const {
  item,
  orderType,
  remainingPrice,
  discountedPrice
} = location.state || {};

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
          <div style={styles.btnIcon}>💳</div>
          <div style={styles.btnText}>카드 결제</div>
        </button>
        <button
          style={styles.btn}
          onClick={() => {
  console.log("payment discountedPrice:", discountedPrice);

  navigate('/barcode-camera', {
    state: {
      item,
      discountedPrice
    }
  });
}}
        >
          <div style={styles.btnIcon}>🎟️</div>
          <div style={styles.btnText}>바코드 결제</div>
        </button>
      </div>

      <div style={styles.totalBar}>
        <span style={styles.totalLabel}>결제 금액</span>
        <span style={styles.totalPrice}>{(discountedPrice ?? remainingPrice ?? item?.price)}</span>
        {remainingPrice && (
          <p style={styles.warningText}>
            바코드 차감 후 남은 금액입니다
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
    height: '100vh', backgroundColor: '#ffffff', gap: '40px'
  },
  title: { fontSize: '32px', color: '#000000', fontWeight: 'bold' },
  orderInfo: { fontSize: '18px', color: '#666' },
  btnWrapper: { display: 'flex', gap: '40px' },
  btn: {
    width: '200px', height: '200px',
    borderRadius: '12px', border: '2px solid #00754a',
    backgroundColor: '#ffffff', cursor: 'pointer',
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    transition: 'all 0.2s'
  },
  btnIcon: { fontSize: '60px', marginBottom: '16px' },
  btnText: { fontSize: '20px', color: '#00754a', fontWeight: 'bold' },
  totalBar: {
    textAlign: 'center', padding: '20px',
    backgroundColor: '#d4e9e2', borderRadius: '12px',
    minWidth: '300px'
  },
  totalLabel: { fontSize: '18px', color: '#000000', marginRight: '12px' },
  totalPrice: { fontSize: '28px', color: '#00754a', fontWeight: 'bold' },
  warningText: {
    color: '#00754a', fontSize: '16px', marginTop: '8px'
  },
};

export default PaymentScreen;
import { useNavigate, useLocation } from 'react-router-dom';

function CompleteScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item, payType, finalPrice } = location.state || {};

  return (
    <div style={styles.container}>
      <div style={styles.checkmark}>✅</div>
      <h2 style={styles.title}>주문 완료!</h2>
      <div style={styles.infoBox}>
        <p>메뉴: {item?.name}</p>
        <p>결제 방법: {payType}</p>
        <p>결제 금액: {(finalPrice ?? item?.price)?.toLocaleString()}원</p>
      </div>
      <div style={styles.btnWrapper}>
        <button style={styles.btn}>🧾 영수증 출력</button>
        <button style={{ ...styles.btn, backgroundColor: '#aaa' }} onClick={() => navigate('/')}>
          미출력
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', backgroundColor: '#fff8f0', gap: '30px' },
  checkmark: { fontSize: '80px' },
  title: { fontSize: '40px' },
  infoBox: { fontSize: '22px', lineHeight: '2', textAlign: 'center' },
  btnWrapper: { display: 'flex', gap: '30px' },
  btn: { padding: '15px 40px', fontSize: '20px', borderRadius: '10px', border: 'none', backgroundColor: '#6f4e37', color: 'white', cursor: 'pointer' },
};

export default CompleteScreen;
import { useNavigate } from 'react-router-dom';

function HomeScreen() {
  const navigate = useNavigate();

  const handleSelect = (type) => {
    navigate('/menu', { state: { orderType: type } });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>☕ EASY CAFE</h1>
      <p style={styles.subtitle}>주문 방식을 선택해주세요</p>
      <div style={styles.btnWrapper}>
        <button style={styles.btn} onClick={() => handleSelect('매장')}>
          🍽️ 매장
        </button>
        <button style={styles.btn} onClick={() => handleSelect('포장')}>
          🛍️ 포장
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    height: '100vh', backgroundColor: '#fff8f0',
  },
  title: { fontSize: '48px', marginBottom: '10px' },
  subtitle: { fontSize: '24px', color: '#888', marginBottom: '60px' },
  btnWrapper: { display: 'flex', gap: '40px' },
  btn: {
    width: '200px', height: '200px', fontSize: '28px',
    borderRadius: '20px', border: 'none',
    backgroundColor: '#6f4e37', color: 'white',
    cursor: 'pointer',
  },
};

export default HomeScreen;
import { useNavigate } from 'react-router-dom';

function HomeScreen() {
  const navigate = useNavigate();

  const handleSelect = (type) => {
    navigate('/menu', { state: { orderType: type } });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>EASY CAFE</h1>
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
    height: '100vh', backgroundColor: '#ffffff',
  },
  title: { 
    fontSize: '56px', 
    marginBottom: '10px', 
    color: '#00754a',
    fontWeight: 'bold',
    letterSpacing: '2px'
  },
  subtitle: { 
    fontSize: '24px', 
    color: '#000000', 
    marginBottom: '80px',
    fontWeight: '300'
  },
  btnWrapper: { display: 'flex', gap: '40px' },
  btn: {
    width: '220px', height: '220px', fontSize: '28px',
    borderRadius: '50%', border: 'none',
    backgroundColor: '#00754a', color: '#ffffff',
    cursor: 'pointer', fontWeight: 'bold',
    boxShadow: '0 4px 12px rgba(0,117,74,0.3)',
    transition: 'all 0.2s'
  },
};

export default HomeScreen;
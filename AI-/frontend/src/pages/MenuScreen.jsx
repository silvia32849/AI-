import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import menuData from '../data/menuData';

function MenuScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const orderType = location.state?.orderType || '매장';
  const categories = Object.keys(menuData);
  const [selectedCategory, setSelectedCategory] = useState('추천메뉴');
  const [selectedItem, setSelectedItem] = useState(null);
  const [showFAQ, setShowFAQ] = useState(false);

  useEffect(() => {
    if (showFAQ) return;

    const timer = setTimeout(() => {
      setShowFAQ(true);
    }, 10000);

    return () => clearTimeout(timer);
  }, [showFAQ]);

  const handleUserAction = () => {
    if (!showFAQ) {
      setShowFAQ(false);
    }
  };

  const handlePayment = () => {
    if (!selectedItem) return alert('메뉴를 선택해주세요!');
    navigate('/payment', { state: { item: selectedItem, orderType } });
  };

  return (
    <div style={styles.container} onClick={handleUserAction}>

      {/* 상단 헤더 */}
      <div style={styles.header}>
        <button
          style={styles.homeBtn}
          onClick={(e) => {
            e.stopPropagation();
            navigate('/');
          }}
        >
          🏠 Home
        </button>
        <h2 style={styles.title}>☕ EASY CAFE</h2>
        <button
          style={styles.faqBtn}
          onClick={(e) => {
            e.stopPropagation();
            setShowFAQ(true);
          }}
        >
          ❓ FAQ
        </button>
      </div>

      {/* 카테고리 탭 */}
      <div style={styles.tabs}>
        {categories.map((cat) => (
          <button
            key={cat}
            style={{
              ...styles.tab,
              backgroundColor: selectedCategory === cat ? '#6f4e37' : '#eee',
              color: selectedCategory === cat ? 'white' : 'black',
            }}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* 메뉴 그리드 */}
      <div style={styles.grid}>
        {menuData[selectedCategory].map((item) => (
          <div
            key={item.id}
            style={{
              ...styles.card,
              border: selectedItem?.id === item.id ? '3px solid #6f4e37' : '3px solid transparent',
            }}
            onClick={() => setSelectedItem(item)}
          >
            <div style={styles.emoji}>{item.emoji}</div>
            <div style={styles.itemName}>{item.name}</div>
            <div style={styles.itemPrice}>{item.price.toLocaleString()}원</div>
          </div>
        ))}
      </div>

      {/* 하단 선택 바 */}
      <div style={styles.bottomBar}>
        <span style={styles.selectedText}>
          {selectedItem
            ? `${selectedItem.emoji} ${selectedItem.name} - ${selectedItem.price.toLocaleString()}원`
            : '메뉴를 선택해주세요'}
        </span>
        <button style={styles.payBtn} onClick={handlePayment}>
          결제하기 →
        </button>
      </div>

      {/* FAQ 팝업 */}
      {showFAQ && (
        <div style={styles.faqOverlay}>
          <div style={styles.faqModal} onClick={(e) => e.stopPropagation()}>
            <button
              style={styles.faqCloseBtn}
              onClick={() => setShowFAQ(false)}
            >
              ✕
            </button>
            {/* 여기에 <FAQScreen /> 컴포넌트 붙이면 됩니다 */}
            <h3 style={{ fontSize: '28px' }}>❓ 자주 묻는 질문</h3>
            <p style={{ color: '#888', marginTop: '10px' }}>FAQ 컴포넌트 들어올 자리</p>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column',
    height: '100vh', backgroundColor: '#fff8f0',
    position: 'relative'
  },
  header: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', padding: '20px 30px'
  },
  title: {
    fontSize: '28px',
    position: 'absolute',
    left: '50%',
    transform: 'translateX(-50%)',
  },
  homeBtn: {
    padding: '10px 20px', fontSize: '18px',
    borderRadius: '10px', border: 'none',
    backgroundColor: '#6f4e37', color: 'white', cursor: 'pointer'
  },
  faqBtn: {
    padding: '10px 20px', fontSize: '18px',
    borderRadius: '10px', border: 'none',
    backgroundColor: '#6f4e37', color: 'white', cursor: 'pointer'
  },
  tabs: { display: 'flex', gap: '10px', padding: '0 30px', marginBottom: '20px' },
  tab: {
    padding: '12px 24px', fontSize: '18px',
    borderRadius: '10px', border: 'none', cursor: 'pointer'
  },
  grid: {
    display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px', padding: '0 30px', flex: 1,
    overflowY: 'auto'
  },
  card: {
    backgroundColor: 'white', borderRadius: '15px',
    padding: '20px', textAlign: 'center', cursor: 'pointer'
  },
  emoji: { fontSize: '48px', marginBottom: '10px' },
  itemName: { fontSize: '20px', fontWeight: 'bold', marginBottom: '8px' },
  itemPrice: { fontSize: '18px', color: '#6f4e37' },
  bottomBar: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', padding: '20px 30px',
    backgroundColor: 'white', borderTop: '1px solid #eee'
  },
  selectedText: { fontSize: '20px' },
  payBtn: {
    padding: '15px 30px', fontSize: '20px',
    backgroundColor: '#6f4e37', color: 'white',
    border: 'none', borderRadius: '10px', cursor: 'pointer'
  },
  faqOverlay: {
    position: 'fixed', top: 0, left: 0,
    width: '100%', height: '100%',
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    zIndex: 1000
  },
  faqModal: {
    backgroundColor: 'white', borderRadius: '20px',
    padding: '40px', width: '600px', minHeight: '400px',
    position: 'relative', textAlign: 'center'
  },
  faqCloseBtn: {
    position: 'absolute', top: '15px', right: '20px',
    fontSize: '24px', border: 'none',
    backgroundColor: 'transparent', cursor: 'pointer'
  },
};

export default MenuScreen;
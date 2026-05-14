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
    if (!showFAQ) setShowFAQ(false);
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
          onClick={(e) => { e.stopPropagation(); navigate('/'); }}
        >
          Home
        </button>
        <h2 style={styles.title}>EASY CAFE</h2>
        <button
          style={styles.faqBtn}
          onClick={(e) => { e.stopPropagation(); setShowFAQ(true); }}
        >
          FAQ
        </button>
      </div>

      {/* 카테고리 탭 */}
      <div style={styles.tabs}>
        {categories.map((cat) => (
          <button
            key={cat}
            style={{
              ...styles.tab,
              backgroundColor: selectedCategory === cat ? '#00754a' : '#d4e9e2',
              color: selectedCategory === cat ? '#ffffff' : '#000000',
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
              border: selectedItem?.id === item.id ? '3px solid #00754a' : '3px solid #f5f5f5',
              boxShadow: selectedItem?.id === item.id ? '0 4px 15px rgba(0,117,74,0.2)' : '0 2px 8px rgba(0,0,0,0.06)',
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
          결제하기
        </button>
      </div>

      {/* FAQ 팝업 */}
      {showFAQ && (
        <div style={styles.faqOverlay}>
          <div style={styles.faqModal} onClick={(e) => e.stopPropagation()}>
            <button style={styles.faqCloseBtn} onClick={() => setShowFAQ(false)}>
              ✕
            </button>
            <h3 style={{ fontSize: '28px', color: '#00754a' }}>자주 묻는 질문</h3>
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
    height: '100vh', backgroundColor: '#ffffff',
    position: 'relative'
  },
  header: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', padding: '20px 40px',
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #f0f0f0'
  },
  title: {
    fontSize: '28px', color: '#00754a',
    position: 'absolute', left: '50%',
    transform: 'translateX(-50%)',
    fontWeight: 'bold',
    letterSpacing: '1px'
  },
  homeBtn: {
    padding: '12px 24px', fontSize: '16px',
    borderRadius: '25px', border: '2px solid #00754a',
    backgroundColor: '#ffffff', color: '#00754a', 
    cursor: 'pointer', fontWeight: 'bold',
    transition: 'all 0.2s'
  },
  faqBtn: {
    padding: '12px 24px', fontSize: '16px',
    borderRadius: '25px', border: '2px solid #00754a',
    backgroundColor: '#ffffff', color: '#00754a',
    cursor: 'pointer', fontWeight: 'bold',
    transition: 'all 0.2s'
  },
  tabs: {
    display: 'flex', gap: '12px',
    padding: '20px 40px', backgroundColor: '#ffffff',
  },
  tab: {
    padding: '14px 28px', fontSize: '17px',
    borderRadius: '25px', border: 'none', cursor: 'pointer',
    fontWeight: 'bold', transition: 'all 0.2s'
  },
  grid: {
    display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '24px', padding: '24px 40px', flex: 1,
    overflowY: 'auto', backgroundColor: '#fafafa'
  },
  card: {
    backgroundColor: '#ffffff', borderRadius: '12px',
    padding: '24px', textAlign: 'center', cursor: 'pointer',
    transition: 'all 0.2s'
  },
  emoji: { fontSize: '52px', marginBottom: '12px' },
  itemName: { 
    fontSize: '19px', fontWeight: 'bold', 
    marginBottom: '8px', color: '#000000' 
  },
  itemPrice: { 
    fontSize: '17px', color: '#00754a', fontWeight: 'bold' 
  },
  bottomBar: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', padding: '24px 40px',
    backgroundColor: '#ffffff', borderTop: '1px solid #f0f0f0'
  },
  selectedText: { fontSize: '19px', color: '#000000', fontWeight: '500' },
  payBtn: {
    padding: '16px 36px', fontSize: '18px',
    backgroundColor: '#00754a', color: '#ffffff',
    border: 'none', borderRadius: '25px', cursor: 'pointer',
    fontWeight: 'bold', transition: 'all 0.2s',
    boxShadow: '0 2px 8px rgba(0,117,74,0.3)'
  },
  faqOverlay: {
    position: 'fixed', top: 0, left: 0,
    width: '100%', height: '100%',
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    zIndex: 1000
  },
  faqModal: {
    backgroundColor: '#ffffff', borderRadius: '16px',
    padding: '40px', width: '600px', minHeight: '400px',
    position: 'relative', textAlign: 'center'
  },
  faqCloseBtn: {
    position: 'absolute', top: '20px', right: '24px',
    fontSize: '28px', border: 'none',
    backgroundColor: 'transparent', cursor: 'pointer',
    color: '#000000'
  },
};

export default MenuScreen;
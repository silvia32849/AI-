import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import menuData from '../data/menuData';

const IDLE_MS = 30000; // 입력이 없을 때 도움 팝업을 띄우기까지의 시간(30초)

function MenuScreen() {
const navigate = useNavigate();
const location = useLocation();
const orderType = location.state?.orderType || '매장';
const categories = Object.keys(menuData);
const [selectedCategory, setSelectedCategory] = useState('추천메뉴');
const [selectedItem, setSelectedItem] = useState(null);
const [showFAQ, setShowFAQ] = useState(false);


// 스마트 헬퍼: 30초 동안 입력이 없으면 FAQ 팝업을 자동으로 띄운다
useEffect(() => {
  if (showFAQ) return; // FAQ가 열려 있으면 타이머·리스너를 걸지 않음

  let timer;
  const startTimer = () => {
    clearTimeout(timer); // 입력이 있을 때마다 타이머를 처음부터 다시 시작
    timer = setTimeout(() => setShowFAQ(true), IDLE_MS);
  };

  // capture(true): 버튼의 stopPropagation()에 막히지 않고 모든 입력을 감지
  const events = ['click', 'touchstart', 'keydown', 'scroll'];
  events.forEach((e) => window.addEventListener(e, startTimer, true));
  startTimer(); // 화면 진입 시 첫 타이머 시작

  return () => {
    // 화면을 벗어나거나 팝업이 열리면 타이머와 리스너를 함께 정리
    clearTimeout(timer);
    events.forEach((e) => window.removeEventListener(e, startTimer, true));
  };
}, [showFAQ]);


const handlePayment = () => {
if (!selectedItem) return alert('메뉴를 선택해주세요!');
navigate('/payment', { state: { item: selectedItem, orderType } });
};

return (
<div style={styles.container}>
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
<img src={item.image} alt={item.name} style={styles.itemImage} />
<div style={styles.itemName}>{item.name}</div>
<div style={styles.itemPrice}>{item.price.toLocaleString()}원</div>
</div>
))}
</div>

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

{/* 선배님의 기존 FAQ 모달 코드 구역 */}
      {showFAQ && (
        <div style={styles.faqOverlay}>
          {/* 모달 창 크기를 서영님 FAQ 너비(480px)에 맞춰 540px 정도로 살짝 키워줍니다 */}
          <div style={{...styles.faqModal, width: '540px', padding: '30px 20px 20px 20px'}} onClick={(e) => e.stopPropagation()}>
            <button style={styles.faqCloseBtn} onClick={() => setShowFAQ(false)}>
              ✕
            </button>
            <h3 style={{ fontSize: '26px', color: '#00754a', marginBottom: '15px', marginTop: '10px' }}>자주 묻는 질문</h3>
            
            {/* 💡 [여기 수정] 선배님이 비워둔 자리에 서영님 FAQ 주소를 iframe으로 삽입! */}
            <iframe 
              src="http://127.0.0.1:8000/" 
              title="FAQ 센터"
              style={{
                width: '100%',
                height: '550px', // 모달창 안에서 스크롤하며 볼 수 있도록 높이 지정
                border: 'none',
                borderRadius: '12px'
              }}
            />
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
overflowY: 'auto', backgroundColor: '#fafafa',
alignContent: 'start'
},
card: {
backgroundColor: '#ffffff', borderRadius: '12px',
padding: '16px', textAlign: 'center', cursor: 'pointer',
transition: 'all 0.2s',
display: 'flex',
flexDirection: 'column',
alignItems: 'center',
height: 'auto',
boxSizing: 'border-box'
},
itemImage: {
width: '100%',
height: 'auto',
maxHeight: '220px',
objectFit: 'contain',
borderRadius: '8px',
marginBottom: '12px',
backgroundColor: '#ffffff'
},
itemName: {
fontSize: '18px', fontWeight: 'bold',
marginBottom: '8px', color: '#000000',
wordBreak: 'keep-all'
},
itemPrice: {
fontSize: '16px', color: '#00754a', fontWeight: 'bold'
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
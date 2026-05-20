import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function BarcodeScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { item, barcodeData } = location.state || {};

  const price = item?.price || 0;

  const finalPrice = barcodeData?.final_price || 0;

  const isSimplePay = barcodeData?.is_simple_pay;

  const isEnough = finalPrice === 0;

  console.log(barcodeData);
console.log("finalPrice:", finalPrice);
console.log("isEnough:", isEnough);
console.log("isSimplePay:", isSimplePay);

useEffect(() => {

  if (isSimplePay && finalPrice === 0) {

    navigate('/complete', {
      state: {
        item,
        payType: barcodeData?.partner_name,
        barcodeData
      }
    });

  }

}, [isSimplePay, finalPrice, navigate, item, barcodeData]);

const handleUse = () => {

  // 잔액 부족 → 추가 결제
  if (!isEnough) {

    navigate('/payment', {
      state: {
        item,
        discountedPrice: finalPrice,
      }
    });

    return;
  }

  // 잔액 충분 → 바로 완료
  navigate('/complete', {
    state: {
      item,
      payType: barcodeData?.partner_name,
      barcodeData
    }
  });
};

  return (
    <div style={styles.container}>
      <div style={styles.checkmark}>✓</div>

      <h2 style={styles.title}>바코드 결제</h2>

      <div style={styles.barcodeBox}>
 
      <div style={styles.infoBox}>

  <div style={styles.infoRow}>
    <span>명칭</span>
    <span style={styles.infoValue}>
      {barcodeData?.partner_name}
    </span>
  </div>

  <div style={styles.infoRow}>
    <span>원가</span>

    <span style={styles.infoValue}>
      {barcodeData?.original_price?.toLocaleString()}원
    </span>
  </div>

  {barcodeData?.is_simple_pay && (
  <div style={styles.infoRow}>
    <span>사용 금액</span>

    <span style={styles.infoValue}>
      -{(barcodeData?.original_price - finalPrice).toLocaleString()}원
    </span>
  </div>
)}

      {barcodeData?.telecom_discount > 0 && (
      <div style={styles.infoRow}>
        <span>통신사 할인</span>

        <span style={styles.infoValue}>
          -{barcodeData.telecom_discount.toLocaleString()}원
        </span>
      </div>
    )}
        <div style={{...styles.infoRow, marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #f0f0f0'}}>
          <span style={styles.finalLabel}>결제 금액</span>
          <span style={{
            ...styles.finalPrice,
            color: isEnough ? '#00754a' : '#d32f2f'
          }}>{finalPrice.toLocaleString()}원</span>
        </div>
        {!isEnough && (
          <p style={styles.warningText}>
            결제를 진행해주세요.
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
            {isEnough ? '사용' : '결제수단 선택'}
          </button>
        </div>
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
  btnWrapper: {
  display: 'flex',
  gap: '20px',
  justifyContent: 'center',
  width: '100%'
},
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
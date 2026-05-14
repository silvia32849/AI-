import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomeScreen from './pages/HomeScreen';
import MenuScreen from './pages/MenuScreen';
import PaymentScreen from './pages/PaymentScreen';
import BarcodeCameraScreen from './pages/BarcodeCameraScreen';
import BarcodeScreen from './pages/BarcodeScreen';
import CompleteScreen from './pages/CompleteScreen';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeScreen />} />
        <Route path="/menu" element={<MenuScreen />} />
        <Route path="/payment" element={<PaymentScreen />} />
        <Route path="/barcode-camera" element={<BarcodeCameraScreen />} />
        <Route path="/barcode" element={<BarcodeScreen />} />
        <Route path="/complete" element={<CompleteScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from './screens/Home/Home';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Subscribe from './screens/Subscribe/Subscribe';
import  Unsubscribe  from './screens/Unsubscribe/Unsubscribe';
import TransactionHistory from './screens/TransactionHistory/TransactionHistory';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './App.css';
import Funds from './screens/Funds/Funds';

function App() {
  const [drawerOpen, setDrawerOpen] = React.useState(false);

  const toggleDrawer = (open: boolean) => () => {
    setDrawerOpen(open);
  };

  return (
    <div className="App">
      <Router>
        <Header onMenuClick={toggleDrawer(true)} />
        <Sidebar open={drawerOpen} onClose={toggleDrawer(false)} />
        <main className="main-content">
        <ToastContainer />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/clients" element={<Home />} />
            <Route path="/subscribe" element={<Subscribe />} />
            <Route path="/unsubscribe" element={<Unsubscribe />} />
            <Route path="/transaction-history" element={<TransactionHistory />} />
            <Route path="/funds" element={<Funds />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App

import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Store.css';

const Store = () => {
  return (
    <div className="store-page">
      <Header />
      
      <main className="store-main">
        <div className="store-content">
          <h1 className="store-title">The Store Page</h1>
          <div className="store-placeholder">
            <p>Store functionality coming soon...</p>
            <p>Here you'll be able to browse and purchase our premium doorbells.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Store;

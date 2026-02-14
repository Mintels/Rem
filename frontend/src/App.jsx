import styles from './App.module.css';
import Hero from './components/hero';
import Footer from './components/footer';
import Sidebar from './components/sidebar';
import { useState } from 'react';

function App() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  return (
    <div className={styles.appContainer}>

      <span className={styles.sidebar}>  
        <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen}/>
      </span>
      <div className={`${styles.mainContent} ${!isSidebarOpen ? styles.sidebarClosed : ''}`}>
        <Hero />
        <Footer />
      </div>


    </div>
  )
}



export default App

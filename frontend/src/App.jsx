import styles from './App.module.css';
import Hero from './components/hero';
import Chat from './components/Chat';
import Footer from './components/footer';
import Sidebar from './components/sidebar';
import { useState } from 'react';

function App() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth > 768);
    const [initialMessage, setInitialMessage] = useState(null);
  
    return (
        <div className={styles.appContainer}>
            <span className={styles.sidebar}>
                <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen}/>
            </span>
            <div className={`${styles.mainContent} ${!isSidebarOpen ? styles.sidebarClosed : ''}`}>
                {!initialMessage ? <Hero setInitialMessage={setInitialMessage}/> : <Chat initialMessage={initialMessage}/>}
                <Footer isSidebarOpen={isSidebarOpen} />
            </div>
        </div>
    )
}

export default App;
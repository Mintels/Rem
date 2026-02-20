import styles from './css/hero.module.css';
import { useState } from 'react';

function Hero({setInitialMessage}) {

    const [message, setMessage] = useState("");
    
    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (!message.trim()) return;
        
        setInitialMessage(message);
    }
    return (
        <div className={styles.heroContainer}>

            <h1 className={styles.title}>Rem</h1>

            <div className={styles.inputContainer}>
                <form className={styles.form} onSubmit={handleSubmit}>

                    <input className={styles.input}
                    onChange ={(e) => setMessage(e.target.value)}
                    type="text" 
                    name="message" 
                    placeholder="Ask me anything..." 
                    value={message}
                    required />

                </form>
            </div>
        </div>
    )
}

export default Hero; 
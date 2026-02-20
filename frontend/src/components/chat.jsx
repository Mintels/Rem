import styles from './css/chat.module.css';
import { useState, useEffect } from 'react';
import { useRef } from 'react';

export default function Chat({initialMessage}) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        {id: Date.now(), text: initialMessage, sender: "user"},
    ]);

    const initialized = useRef(true);

    useEffect(() => {
        if(!initialized.current) return;
        initialized.current = false;

        setTimeout(() => {
            const remMessage = {
                id: Date.now(),
                text: "Placeholder",
                sender: "rem"
            };
            setMessages(prev => [...prev, remMessage]);
        }, 700);
    });

    const handleSubmit = (e) => {

        e.preventDefault();
        
        if (!message.trim()) return;

        const userText = message;

        const newMessage = {
            id: Date.now(),
            text: userText,
            sender: "user"
        };

        setMessages([...messages, newMessage]);
        setMessage("");

        setTimeout(() => {
            const remMessage = {
                id: Date.now() + 1,
                text:  "Placeholder",
                sender: "rem"
            };
            setMessages(prev => [...prev, remMessage]);
        }, 500);
    }

    return (
        <div className={styles.chatContainer}>
            <div className={styles.messages}>
                {messages.map(msg => (
                    <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
                        {msg.text}
                    </div>
                ))}
            </div> 
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
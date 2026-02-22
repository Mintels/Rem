import styles from './css/chat.module.css';
import { useState, useEffect, useRef } from 'react';

export default function Chat({initialMessage}) {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState([
        {id: Date.now(), text: initialMessage, sender: "user"},
    ]);

    const initialized = useRef(false);
    const bottomRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        if(initialized.current) return;
        initialized.current = true;
        setIsLoading(true);

        fetch("https://mintels.pythonanywhere.com/chats/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: initialMessage })
        })
        .then(res => res.json())
        .then(data => {
            setTimeout(() => {
                const remMessage = {
                    id: Date.now(),
                    text: data.reply,
                    sender: "rem"
                };
                setMessages(prev => [...prev, remMessage]);
                setIsLoading(false);
                setTimeout(() => inputRef.current?.focus(), 50);
            }, 700);
        });
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!message.trim()) return;

        setIsLoading(true);

        const userText = message;

        const newMessage = {
            id: Date.now(),
            text: userText,
            sender: "user"
        };

        setMessages(prev => [...prev, newMessage]);
        setMessage("");

        fetch("https://mintels.pythonanywhere.com/chats/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        })
        .then(res => res.json())
        .then(data => {
            setTimeout(() => {
                const remMessage = {
                    id: Date.now(),
                    text: data.reply,
                    sender: "rem"
                };
                setMessages(prev => [...prev, remMessage]);
                setIsLoading(false);
                setTimeout(() => inputRef.current?.focus(), 50);
            }, 700);
        });
    }

    return (
        <div className={styles.chatContainer}>
            <div className={styles.messages}>
                {messages.map(msg => (
                    <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
                        {msg.text}
                    </div>
                ))}
                <div ref={bottomRef} />
            </div> 
            <div className={styles.inputContainer}>
                <form className={styles.form} onSubmit={handleSubmit}>
                    <input
                        ref={inputRef}
                        className={styles.input}
                        onChange={(e) => setMessage(e.target.value)}
                        type="text"
                        name="message"
                        placeholder="Ask me anything..."
                        value={message}
                        disabled={isLoading}
                        autoComplete="off"
                        required />
                </form>
            </div>
        </div>
    )
}
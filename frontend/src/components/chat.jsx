import styles from './css/chat.module.css';
import { useState, useEffect, useRef } from 'react';

export default function Chat({initialMessage}) {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [timedOut, setTimedOut] = useState(false);
    const [messages, setMessages] = useState(() => {
        const noticeText = "Reminder: This is a proof of concept application. Refer to source code for more details.";
        const now = Date.now();

        return [
            { id: now + 1, text: noticeText, sender: "rem" },
            { id: now, text: initialMessage, sender: "user" },
        ];
    });

    const initialized = useRef(false);
    const bottomRef = useRef(null);
    const inputRef = useRef(null);
    const errorTimerRef = useRef(null);

    const cleanResponse = (text) => {
        return text
            .replace(/\s([ms])(?=\s|$)/g, "$1")
            .replace(/\s('s|'t|'ve|'ll|'m|'d|'re)\b/g, "$1")
            .replace(/\s+/g, " ")
            .trim();
    };

    const getResponse = (userMessage) => {
        fetch("https://mintels.pythonanywhere.com/chats/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(res => res.json())
        .then(data => {
            clearTimeout(errorTimerRef.current);
            setTimeout(() => {
                const remMessage = {
                    id: Date.now(),
                    text: cleanResponse(data.reply),
                    sender: "rem"
                };
                setMessages(prev => [...prev, remMessage]);
                setIsLoading(false);
                setTimeout(() => inputRef.current?.focus(), 50);
            }, 700);
        });
    }

    useEffect(() => {
        if(initialized.current) return;
        initialized.current = true;
        setIsLoading(true);
        setTimedOut(false);
        errorTimerRef.current = setTimeout(() => { setTimedOut(true); setIsLoading(false); }, 12000);

        getResponse(initialMessage);
    }, []);


    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (isLoading) return;
        if (!message.trim()) return;

        setIsLoading(true);
        setTimedOut(false);
        errorTimerRef.current = setTimeout(() => { setTimedOut(true); setIsLoading(false); }, 12000);

        const userText = message;

        const newMessage = {
            id: Date.now(),
            text: userText,
            sender: "user"
        };

        setMessages(prev => [...prev, newMessage]);
        setMessage("");

        getResponse(userText);
    }

    return (
        <div className={styles.chatContainer}>
            <div className={styles.navSpacer} />
            <div className={styles.messages}>
                {messages.map(msg => (
                    <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
                        {msg.text}
                    </div>
                ))}
                {isLoading && !timedOut && (
                    <div className={styles.typingIndicator}>
                        <span /><span /><span />
                    </div>
                )}
                {timedOut && <div className={styles.errorBubble}>Error: Could Not Connect to Server</div>}
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
import styles from './css/sidebar.module.css';
import chatBubbleIcon from '../assets/chat-bubble.svg';
import contactIcon from '../assets/contact.svg';
import plusIcon from '../assets/plus.svg';
import sidebarIcon from '../assets/sidebar.svg';
import { useState } from 'react';

function Sidebar({isOpen, setIsOpen}) {

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    }

    return (
        <div className={`${styles.sidebarContainer} ${!isOpen ? styles.closed : ''}`}>
            <span className={`${styles.titleContainer} ${!isOpen ? styles.closed : ''}`}>
                <h2 className={styles.sidebarTitle}>
                    {isOpen && "Rem AI"}
                </h2>
                <img className={`${styles.titleIcon} ${!isOpen ? styles.closed: ''}`} src={sidebarIcon}   onClick={toggleSidebar} alt="Sidebar Icon" />
            </span>

            <ul className={styles.sidebarList}>
                <li className={styles.sidebarItem}> 
                    <img className={styles.imageIcon} src={plusIcon} alt="Plus Icon" />
                    {isOpen && "New Chat"}
                </li>
    
                <li className={styles.sidebarItem}> 
                    <img className={styles.imageIcon} src={chatBubbleIcon} alt="Chat Icon" />
                    {isOpen && "Chats"}
                </li>
                <li className={styles.sidebarItem}>
                    <img className={styles.imageIcon} src={contactIcon} alt="Contact Icon" />
                    {isOpen && "Contact"}
                </li>
            </ul>

            {isOpen && <h4 className={styles.subTitle}> Recents </h4>}

        </div>
    )
}

export default Sidebar;

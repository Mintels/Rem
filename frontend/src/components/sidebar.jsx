import styles from './css/sidebar.module.css';
import discordIcon from '../assets/discord.png';
import contactIcon from '../assets/contact.svg';
import plusIcon from '../assets/plus.png';
import sidebarIcon from '../assets/sidebar.png';
import codeIcon from '../assets/code.png';
import { useState } from 'react';

function Sidebar({isOpen, setIsOpen}) {

    const [isNavbarOpen, setNavbarOpen] = useState(false);
    
    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    }

    const toggleNavbar = () => {
        setNavbarOpen(!isNavbarOpen);
    }

    const reloadPage = () => {
        window.location.reload();
    }

    const discordLink = 
    "https://discord.com/oauth2/authorize?client_id=1199193712459251742&scope=bot&permissions=277062162688";

    return (
        <>
        <div className={`${styles.sidebarContainer} ${!isOpen ? styles.closed : ''}`}>
            <span className={`${styles.titleContainer} ${!isOpen ? styles.closed : ''}`}>
                <h2 className={styles.sidebarTitle} onClick={reloadPage}>
                    {isOpen && "Rem AI"}
                </h2>
                <img className={`${styles.titleIcon} ${!isOpen ? styles.closed: ''}`} src={sidebarIcon}   onClick={toggleSidebar} alt="Sidebar Icon" />
            </span>

            <ul className={styles.sidebarList}>
                <li className={styles.sidebarItem} onClick={reloadPage}>
                        <img className={styles.imageIcon} src={plusIcon} alt="Plus Icon" />
                        {isOpen && "New Chat"}
                </li>
    
                <a className={styles.sidebarLink} href={discordLink} target="_blank">
                    <li className={styles.sidebarItem}>
                        <img className={styles.imageIcon} src={discordIcon} alt="Discord Icon" />
                        {isOpen && "Discord"}
                    </li>
                </a>

                <a className={styles.sidebarLink} href="https://github.com/Mintels/Rem" target="_blank">
                    <li className={styles.sidebarItem}>
                        <img className={styles.imageIcon} src={codeIcon} alt="Code Icon" />
                        {isOpen && "My Code"}
                    </li>
                </a>
            </ul>
        </div>

        <div className={styles.navBar}> 
            <span className={`${styles.titleContainer}`}>
                <h2 className={styles.sidebarTitle} onClick={reloadPage}>
                    Rem AI
                </h2>
                <img className={`${styles.titleIcon} ${isNavbarOpen ? styles.open : ''}`} src={sidebarIcon} onClick={toggleNavbar} alt="Navbar Icon" />
        </span>
        </div>

        {isNavbarOpen && (
            <ul className={styles.navbarList}>
                <li className={styles.navbarItem} onClick={reloadPage}>
                    <img className={styles.imageIcon} src={plusIcon} alt="Plus Icon" />
                    New Chat
                </li>
                <a className={styles.sidebarLink} href={discordLink} target="_blank">
                    <li className={styles.navbarItem}>
                        <img className={styles.imageIcon} src={discordIcon} alt="Discord Icon" />
                        Discord
                    </li>
                </a>
                <a className={styles.sidebarLink} href="https://github.com/Mintels/Rem" target="_blank">
                    <li className={styles.navbarItem}>
                        <img className={styles.imageIcon} src={codeIcon} alt="Code Icon" />
                        My Code
                    </li>
                </a>
            </ul>
        )}
        </>
    )
}

export default Sidebar;

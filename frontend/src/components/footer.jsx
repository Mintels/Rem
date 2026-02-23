import styles from './css/footer.module.css';
import githubIcon from '../assets/github.png';
import linkedinIcon from '../assets/linkedin.png';

function Footer({ isSidebarOpen }) {
    const isMobile = window.innerWidth <= 768;

    return (
        <div className={`${styles.footerContainer} ${!isMobile && !isSidebarOpen ? styles.sidebarClosed : ''}`}>
            <a href="https://github.com/Mintels" target="_blank"><img className={styles.footerIcon} src={githubIcon} alt="GitHub Icon"/></a>
            <a href="https://www.linkedin.com/in/evancnicholas/" target="_blank"><img className={styles.footerIcon} src={linkedinIcon} alt="LinkedIn Icon"/></a>
        </div>
    )
}

export default Footer;
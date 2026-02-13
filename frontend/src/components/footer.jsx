import styles from './css/footer.module.css';

function Footer() {
    return (
        <div className={styles.footerContainer}>
            <p className={styles.footerText}> Made by <a href="https://github.com/Mintels">Evan Nicholas</a> </p>
        </div>
    )
}

export default Footer;

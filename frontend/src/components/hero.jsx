import styles from './css/hero.module.css';

function Hero() {
    return (
        <div className={styles.heroContainer}>

            <h1 className={styles.title}>Rem</h1>

            <div className={styles.inputContainer}>
                <form className={styles.form}>
                    <input className={styles.input} type="text" name="message" placeholder="Ask me anything..." required />
                </form>
            </div>
        </div>
    )
}

export default Hero; 
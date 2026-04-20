import styles from './css/onload.module.css';
import { useEffect, useState } from 'react';

function animateText(setDisplayText, setIsFadingOut, setShowAnimation) {
    const fullWord = 'Remnant';
    let currentIndex = 0;
    let phase = 'building'; // 'building' | 'collapsingFast' | 'collapsingSlow' | 'fadeOut'
    const timeoutIds = [];

    const runAnimation = () => {
        // Text from R to Remnant
        if (phase === 'building') {
            if (currentIndex < fullWord.length) {
                const displayText = fullWord.substring(0, currentIndex + 1);
                setDisplayText(`{${displayText}}`);
                currentIndex++;
                timeoutIds.push(setTimeout(runAnimation, 50));
            } else {
                // Move to phase 2 after reaching Remnant
                phase = 'collapsingFast';
                currentIndex = fullWord.length;
                timeoutIds.push(setTimeout(runAnimation, 200));
            }
        }
        // Collapse from Remnant to Rem
        else if (phase === 'collapsingFast') {
            if (currentIndex > 3) { // Stop at 'Rem' (3 letters)
                currentIndex--;
                const displayText = fullWord.substring(0, currentIndex);
                setDisplayText(`{${displayText}}`);
                timeoutIds.push(setTimeout(runAnimation, 50));
            } else {
                // Move to phase 3
                phase = 'collapsingSlow';
                timeoutIds.push(setTimeout(runAnimation, 300));
            }
        }
        // Collapse from Rem to R
        else if (phase === 'collapsingSlow') {
            if (currentIndex > 1) { // Stop at 'R' (1 letter)
                currentIndex--;
                const displayText = fullWord.substring(0, currentIndex);
                setDisplayText(`{${displayText}}`);
                timeoutIds.push(setTimeout(runAnimation, 150));
            } else {
                // Move to phase 4
                phase = 'fadeOut';
                timeoutIds.push(setTimeout(runAnimation, 500));
            }
        }
        // Fade out the remaining 'R'
        else if (phase === 'fadeOut') {
            setIsFadingOut(true);
            timeoutIds.push(setTimeout(() => {
                setShowAnimation(false);
            }, 600));
        }
    };

    runAnimation();
    return () => timeoutIds.forEach(id => clearTimeout(id));
}

export default function OnLoad() {
    const [showAnimation, setShowAnimation] = useState(true);
    const [displayText, setDisplayText] = useState('{R}');
    const [isFadingOut, setIsFadingOut] = useState(false);

    useEffect(() => { 
        return animateText(setDisplayText, setIsFadingOut, setShowAnimation);
    }, []);

    if (!showAnimation) return null;
    
    return (
        <div className={`${styles.onLoadContainer} ${isFadingOut ? styles.fadeOut : ''}`}>
            <h1 className={styles.title}>{displayText}</h1>
        </div>
    )
}
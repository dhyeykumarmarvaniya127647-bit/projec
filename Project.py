import time
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('typing_debug.log'), logging.StreamHandler()])

TEXTS = [
    "The quick brown fox jumps over the lazy dog near the riverbank.",
    "Python is a powerful programming language used for web development and data science.",
    "Practice makes perfect when learning to type faster and more accurately.",
    "Coding requires patience, dedication, and continuous learning every single day.",
    "The sun sets slowly over the horizon painting the sky in brilliant colors."
]

def calc_wpm(t, txt):
    logging.debug(f"WPM calc: {t:.2f}s, {len(txt)} chars")
    wpm = round(len(txt.split()) / (t / 60), 2) if t > 0 else 0
    logging.debug(f"WPM: {wpm}")
    return wpm

def calc_accuracy(orig, typed):
    logging.debug(f"Accuracy: orig={len(orig)}, typed={len(typed)}")
    if not orig: return 100.0
    correct = sum(1 for o, t in zip(orig, typed) if o == t)
    acc = round((correct / max(len(orig), len(typed))) * 100, 2)
    if acc < 100:
        errors = [f"pos{i}:'{o}'!='{t}'" for i, (o, t) in enumerate(zip(orig, typed)) if o != t][:5]
        logging.debug(f"Errors: {errors}")
    logging.debug(f"Accuracy: {acc}%")
    return acc

def main():
    logging.info(f"Session start: {datetime.now()}")
    print("="*60 + "\nTYPING SPEED TESTER".center(60) + "\n" + "="*60)
    print("\nDebug enabled - logs saved to 'typing_debug.log'\n")
    
    test_num = 0
    while True:
        test_num += 1
        logging.info(f"Test #{test_num}")
        
        text = random.choice(TEXTS)
        logging.debug(f"Text: '{text[:30]}...' ({len(text)} chars)")
        
        print("-"*60 + f"\n{text}\n" + "-"*60)
        input("Press ENTER to start...")
        print("\nType NOW!\n")
        
        start = time.time()
        try:
            typed = input()
            elapsed = time.time() - start
            logging.debug(f"Input: '{typed[:50]}...' ({len(typed)} chars, {elapsed:.2f}s)")
        except Exception as e:
            logging.error(f"Input error: {e}")
            print("❌ Input error!")
            continue
        
        try:
            wpm, acc = calc_wpm(elapsed, typed), calc_accuracy(text, typed)
        except Exception as e:
            logging.error(f"Calc error: {e}")
            print("❌ Calculation error!")
            continue
        
        print(f"\n{'='*60}\nRESULTS".center(60) + f"\n{'='*60}")
        print(f"\nTime: {elapsed:.2f}s | Speed: {wpm} WPM | Accuracy: {acc}%")
        
        msg = {100: "🎉 Perfect!", 90: "👍 Great!", 75: "👌 Good!"}.get(
            next((k for k in [100, 90, 75] if acc >= k), 0), "💪 Keep practicing!")
        print(f"\n{msg}\n" + "="*60)
        logging.info(f"Results: {wpm} WPM, {acc}%")
        
        if input("\nTry again? (yes/no): ").lower() not in ['yes', 'y']:
            logging.info(f"Session end: {test_num} tests, {datetime.now()}")
            print(f"\nThanks! Check 'typing_debug.log' for details. 🚀\n")
            break
        print()

if __name__ == "__main__":
    main()
import random
import streamlit as st
import time

# Function to generate a random secret number
def generate_secret_number():
    return str(random.randint(100, 999))

# Function to evaluate the guess
def evaluate_guess(secret, guess):
    feedback = ["❌"] * 3  # Default feedback
    secret_counts = {}  

    # Count occurrences of digits in secret number
    for digit in secret:
        secret_counts[digit] = secret_counts.get(digit, 0) + 1

    # First pass: Check correct position (👌)
    for i in range(3):
        if guess[i] == secret[i]:
            feedback[i] = "👌"
            secret_counts[guess[i]] -= 1  

    # Second pass: Check correct digit but wrong place (👍)
    for i in range(3):
        if feedback[i] == "❌" and guess[i] in secret_counts and secret_counts[guess[i]] > 0:
            feedback[i] = "👍"
            secret_counts[guess[i]] -= 1  

    return " ".join(feedback)

# Mobile-Friendly UI Optimization
st.set_page_config(page_title="Guess the Number", layout="centered")

# Game Title
st.markdown("<h1 style='text-align: center;'>🔢 Deductive Logic Game 🎮</h1>", unsafe_allow_html=True)

# Game Instructions (Always Visible)
with st.expander("📜 How to Play?", expanded=True):
    st.write("""
    - Enter a **3-digit number**  
    - Get hints after each guess:  
      - **👌 Correct digit, correct place**  
      - **👍 Correct digit, wrong place**  
      - **❌ No correct digits**  
    - You have **10 attempts** to guess the secret number.  
    - 🎉 Win by guessing correctly or ❌ lose if attempts run out!
    """)

# Store game state
if "secret_number" not in st.session_state:
    st.session_state.secret_number = generate_secret_number()
    st.session_state.attempts = 10
    st.session_state.history = []
    st.session_state.submitted = False  # Ensure single submission

# User Input Section
st.markdown("<h3 style='text-align: center;'>🔢 Enter a 3-digit number:</h3>", unsafe_allow_html=True)
guess = st.text_input("", max_chars=3, help="Enter a 3-digit number (e.g., 123)")

# Submit Button with Prevention for Double Submission
if st.button("Submit Guess", use_container_width=True):
    if not st.session_state.submitted:
        st.session_state.submitted = True  # Lock further submissions

        if len(guess) == 3 and guess.isdigit():
            feedback = evaluate_guess(st.session_state.secret_number, guess)
            st.session_state.history.append(f"🔢 {guess} → {feedback}")
            st.session_state.attempts -= 1

            if guess == st.session_state.secret_number:
                st.success(f"🎉 You guessed it! The secret number was {st.session_state.secret_number} 🎉")
                st.balloons()
                time.sleep(2)
                st.session_state.clear()
                st.rerun()

            elif st.session_state.attempts == 0:
                st.error(f"❌ Game Over! The secret number was {st.session_state.secret_number}. Try again!")
                time.sleep(2)
                st.session_state.clear()
                st.rerun()
        else:
            st.warning("⚠️ Please enter a valid 3-digit number!")

        st.session_state.submitted = False  # Unlock submission for next input

# Display Previous Attempts in a Scrollable Box
st.markdown("<h3 style='text-align: center;'>📜 Previous Attempts</h3>", unsafe_allow_html=True)
st.markdown("<div style='max-height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px;'>", unsafe_allow_html=True)
for attempt in st.session_state.history:
    st.write(attempt)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar - Game Information
st.sidebar.subheader("ℹ️ Game Info")
st.sidebar.write(f"🎯 **Attempts Left:** {st.session_state.attempts}")
st.sidebar.write("✅ **Correct Place:** `👌`")
st.sidebar.write("🔄 **Wrong Place:** `👍`")
st.sidebar.write("❌ **Not Present:** `❌`")

# Footer - Developed By
st.markdown(
    """
    ---
    🔥 **Developed by Shoaib Munir** 🚀  
    *Built with ❤️ using Streamlit*
    """,
    unsafe_allow_html=True
)

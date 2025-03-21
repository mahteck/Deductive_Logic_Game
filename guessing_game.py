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

# Streamlit UI
st.title("🔢 Deductive Logic Game - Guess the Secret Number 🎮")

# Store secret number & attempts in session state
if "secret_number" not in st.session_state:
    st.session_state.secret_number = generate_secret_number()
    st.session_state.attempts = 10
    st.session_state.history = []
    st.session_state["user_guess"] = ""  # Reset input box

# User input (RESET TEXT BOX)
guess = st.text_input("Enter a 3-digit number:", value=st.session_state["user_guess"], max_chars=3)

if st.button("Submit Guess"):
    if len(guess) == 3 and guess.isdigit():
        feedback = evaluate_guess(st.session_state.secret_number, guess)
        st.session_state.history.append(f"🔢 {guess} → {feedback}")
        st.session_state.attempts -= 1

        if guess == st.session_state.secret_number:
            st.success(f"🎉 You guessed it! The secret number was {st.session_state.secret_number} 🎉")
            st.balloons()
            time.sleep(2)
            st.session_state.clear()  # Reset game
            st.rerun()  # Refresh page

        elif st.session_state.attempts == 0:
            st.error(f"❌ Game Over! The secret number was {st.session_state.secret_number}. Try again!")
            time.sleep(2)
            st.session_state.clear()  # Reset game
            st.rerun()  # Refresh page
    else:
        st.warning("⚠️ Please enter a valid 3-digit number!")

# Display previous attempts
st.subheader("Previous Attempts")
for attempt in st.session_state.history:
    st.write(attempt)

# Display remaining attempts
st.sidebar.subheader("Game Info")
st.sidebar.write(f"🎯 Attempts Left: {st.session_state.attempts}")
st.sidebar.write("✅ Correct Place → `👌`")
st.sidebar.write("🔄 Wrong Place → `👍`")
st.sidebar.write("❌ Not Present → `❌`")

# 🏆 Developed by Section at the Bottom
st.markdown(
    """
    ---
    🔥 **Developed by Shoaib** 🚀  
    *Built with ❤️ using Streamlit and python*
    """,
    unsafe_allow_html=True
)
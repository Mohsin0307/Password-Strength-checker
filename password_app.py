import streamlit as st
import re
import random
import string
import time

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Empty password check
    if not password:
        return "Not Rated", 0, ["Please enter a password to check"]
    
    # Blacklist Check
    if is_blacklisted(password):
        feedback.append("❌ This is a commonly used password and easily guessable!")
        strength = "Very Weak"
        return strength, 0, feedback
    
    # Length Check - weighted more for longer passwords
    if len(password) >= 12:
        score += 1.5
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long (12+ recommended).")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Check for repetitive patterns
    if re.search(r"(.)\1{2,}", password):  # Same character repeated 3+ times
        feedback.append("❌ Avoid repeating the same character multiple times (e.g., 'aaa', '111').")
        score -= 0.5
    
    # Check for sequential patterns
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)", password.lower()):
        feedback.append("❌ Avoid sequential patterns like 'abc', '123'.")
        score -= 0.5
    
    # Prevent negative scores
    score = max(0, score)
    
    # Strength Rating
    if score >= 4:
        strength = "Strong"
        if not feedback:  # If no negative feedback
            feedback.append("✅ Strong Password! Excellent job!")
    elif score >= 3:
        strength = "Moderate"
        feedback.append("⚠️ Moderate Password - Consider improving with the suggestions above.")
    elif score >= 2:
        strength = "Fair"
        feedback.append("⚠️ Fair Password - Please improve using the suggestions above.")
    else:
        strength = "Weak"
        feedback.append("❌ Weak Password - Significantly improve it using the suggestions above.")
    
    return strength, round(score, 1), feedback

def is_blacklisted(password):
    common_passwords = [
        "password", "123456", "qwerty", "admin", "welcome",
        "password123", "abc123", "letmein", "monkey", "1234567890",
        "trustno1", "dragon", "baseball", "football", "superman",
        "iloveyou", "starwars", "master", "login", "princess"
    ]
    
    return password.lower() in common_passwords

def generate_strong_password(length=12):
    # Ensure length is at least 8
    if length < 8:
        length = 8
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*"
    
    # Ensure at least one of each character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest with random characters from all sets
    remaining_length = length - 4
    all_chars = lowercase + uppercase + digits + special_chars
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)
    
    # Convert list to string
    return ''.join(password)

def get_strength_color(strength):
    if strength == "Strong":
        return "green"
    elif strength == "Moderate":
        return "orange"
    elif strength == "Fair":
        return "yellow"
    elif strength == "Weak":
        return "red"
    elif strength == "Very Weak":
        return "darkred"
    else:
        return "gray"

def main():
    st.set_page_config(
        page_title="Password Strength Meter",
        page_icon="🔒",
        layout="centered"
    )
    
    st.title("🔒 Password Strength Meter")
    st.write("Check the strength of your password or generate a strong one!")
    
    tab1, tab2 = st.tabs(["Check Password", "Generate Password"])
    
    # Password Checker Tab
    with tab1:
        st.subheader("Check Your Password Strength")
        
        # Password input with toggle visibility
        col1, col2 = st.columns([3, 1])
        with col1:
            password_visible = st.checkbox("Show password", value=False)
        
        if password_visible:
            password = st.text_input("Enter your password:", key="visible_password")
        else:
            password = st.text_input("Enter your password:", type="password", key="hidden_password")
        
        if st.button("Check Strength", key="check_button"):
            with st.spinner("Analyzing password..."):
                time.sleep(0.5)  # Small delay for effect
                strength, score, feedback = check_password_strength(password)
            
            # Display strength with appropriate color
            color = get_strength_color(strength)
            st.markdown(f"### Password Strength: <span style='color:{color}'>{strength}</span> (Score: {score}/4)", unsafe_allow_html=True)
            
            # Progress bar for visualization
            st.progress(min(score/4, 1.0))
            
            # Feedback
            st.subheader("Feedback:")
            for item in feedback:
                st.write(item)
    
    # Password Generator Tab
    with tab2:
        st.subheader("Generate a Strong Password")
        
        # Password length slider
        length = st.slider("Password Length", min_value=8, max_value=32, value=16, step=1)
        
        if st.button("Generate Password", key="generate_button"):
            with st.spinner("Generating strong password..."):
                time.sleep(0.5)  # Small delay for effect
                generated_password = generate_strong_password(length)
            
            # Display the generated password
            st.success("Generated Password:")
            
            # Display in a box with copy button
            st.code(generated_password)
            
            # Check and display the strength of the generated password
            strength, score, _ = check_password_strength(generated_password)
            color = get_strength_color(strength)
            st.markdown(f"### Password Strength: <span style='color:{color}'>{strength}</span> (Score: {score}/4)", unsafe_allow_html=True)
            st.progress(min(score/4, 1.0))
    
    # Information section
    st.markdown("---")
    st.subheader("What makes a strong password?")
    
    with st.expander("Password Strength Criteria"):
        st.markdown("""
        A strong password should:
        - Be at least **8 characters long** (12+ recommended)
        - Contain **uppercase & lowercase letters**
        - Include at least **one digit** (0-9)
        - Have **one special character** (!@#$%^&*)
        - Avoid common patterns like '123', 'abc', etc.
        - Not be a commonly used password
        """)

if __name__ == "__main__":
    main()
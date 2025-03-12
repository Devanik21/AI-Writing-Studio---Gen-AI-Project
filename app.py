import streamlit as st
import google.generativeai as genai

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Writing Studio",
    page_icon="✍️",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #f5f5dc;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div {
            background-color: #fff7e6;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
        }
        .stButton>button {
            background: linear-gradient(to right, #ff7f50, #ff4500);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for API Key
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")

# Page Header
st.title("✍️ AI Writing Studio")
st.write("Generate high-quality written content effortlessly! Create poems, essays, letters, articles, posters, reports, and more.")

# Input fields
categories = [
    "Poem", "Essay", "Letter", "Article", "Poster", "Report", "Story", "Diary Entry", "Speech", "Notice",
    "Advertisement", "Dialogue Writing", "Autobiography", "Summary Writing", "Book Review", "Movie Review",
    "News Report", "Paragraph Writing", "Debate", "Script Writing"
]

lengths = ["Short", "Medium", "Long", "Very Short", "Very Long", "Concise", "Elaborate", "Brief", "Extended", "Detailed"]

languages = ["English", "Hindi", "Spanish", "French", "German", "Mandarin", "Portuguese", "Italian", "Russian", "Arabic"]

tones = ["Professional", "Casual", "Inspirational", "Motivational", "Humorous", "Empathetic", "Bold", "Encouraging", "Analytical"]

styles = ["None", "Hashtags", "Emojis", "Both Hashtags & Emojis", "Custom Formatting", "Bullet Points", "Lists", "Story Format"]

levels = ["Easy", "Medium", "Hard", "Advanced", "Nightmare"]

topics = [
    "My Best Friend", "A Day at the Park", "Importance of Kindness", "My Favorite Animal", "A Trip to the Moon",
    "If I Had a Superpower", "A Letter to Santa", "Why Books Are Important", "The Magic Pencil", "A Rainy Day",
    "Saving the Environment", "The Funniest Day of My Life", "My Dream Job", "An Adventure in the Jungle",
    "How to Stay Healthy", "The Future of Technology", "A Story About Friendship", "A Mystery to Solve",
    "A Letter to My Future Self", "What If Animals Could Talk?"
]

# Create select boxes
category = st.selectbox("📖 Choose Writing Type:", categories)
length = st.selectbox("📏 Select Length:", lengths)
language = st.selectbox("🌍 Select Language:", languages)
tone = st.selectbox("💭 Select Tone:", tones)
style = st.selectbox("🎨 Include Extras:", styles)
level = st.selectbox("📜 Level of Writing:", levels)
topic = st.selectbox("🌟 Pick a Topic:", topics)

# Generate button
if st.button("📝 Generate Content"):
    if not api_key:
        st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Create a prompt for AI
            prompt = (f"Generate a {category.lower()} at a {level.lower()} level with a {tone.lower()} tone, "
                      f"in {language} on the topic '{topic}'. The post should be {length.lower()} and engaging. "
                      f"Include {style.lower()} if applicable.")

            # Generate response
            with st.spinner("🔄 Creating your content..."):
                response = model.generate_content(prompt)

            # Display result
            st.success("✅ Generated Content:")
            st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")

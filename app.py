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

lengths = ["Short", "Medium", "Long", "Very Short", "Very Long", "Concise", "Elaborate", "Brief", "Extended", "Detailed", "Twitter-Style", "Engaging", "In-Depth", "Compact", "Summarized", "Expanded", "Micro", "Mini", "Maxi", "Verbose", "Comprehensive", "To-the-Point", "Rich", "Layered"]

languages = [
    "English", "Hindi", "Bengali", "Spanish", "French", "German", "Mandarin", "Portuguese", "Italian", "Russian", "Arabic", "Korean", "Japanese", 
    "Dutch", "Swedish", "Turkish", "Hebrew", "Tamil", "Urdu", "Indonesian", "Greek", "Polish", "Thai", "Vietnamese", "Filipino", "Malay", "Czech", 
    "Hungarian", "Romanian", "Finnish", "Norwegian", "Danish", "Slovak", "Ukrainian", "Persian", "Hebrew", "Swahili", "Hausa", "Zulu", "Xhosa", 
    "Igbo", "Yoruba", "Burmese", "Khmer", "Lao", "Sinhala", "Pashto", "Kurdish", "Basque", "Catalan", "Galician", "Maltese", "Luxembourgish", 
    "Icelandic", "Welsh", "Scottish Gaelic", "Irish", "Maori", "Hawaiian", "Samoan", "Tongan", "Tahitian", "Chamorro", "Fijian", "Mongolian", 
    "Tibetan", "Quechua", "Aymara", "Guarani", "Haitian Creole", "Twi", "Amharic", "Tigrinya", "Oromo", "Shona", "Sesotho", "Tswana", "Sindhi", 
    "Nepali", "Kashmiri", "Assamese", "Marathi", "Gujarati", "Punjabi", "Kannada", "Malayalam", "Telugu", "Santali", "Meitei", "Bodo", "Dogri", 
    "Konkani", "Maithili", "Bhili", "Gondi", "Tulu", "Bishnupriya", "Manipuri", "Sylheti", "Afrikaans", "Albanian", "Amharic", "Armenian", 
    "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Burmese", "Cebuano", "Chichewa", "Corsican", "Croatian", "Esperanto", "Estonian", 
    "Frisian", "Gaelic", "Georgian", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hmong", "Igbo", "Javanese", "Kannada", "Kazakh", 
    "Khmer", "Kinyarwanda", "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", 
    "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar", "Nepali", "Odia", "Pashto", "Persian", "Punjabi", "Samoan", "Scots Gaelic", 
    "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Sundanese", "Swahili", "Tajik", "Tamil", "Tatar", 
    "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu",
    "Abkhazian", "Acehnese", "Acholi", "Adyghe", "Afar", "Afrihili", "Ainu", "Akan", "Akkadian", "Aleut", "Algonquin", "Alsatian", "Altai", 
    "Ancient Egyptian", "Ancient Greek", "Anglo-Saxon", "Angika", "Apache", "Aragonese", "Aramaic", "Arapaho", "Arawak", "Assamese", "Asturian", 
    "Avaric", "Avestan", "Awadhi", "Balinese", "Baluchi", "Bambara", "Bashkir", "Bassa", "Batak", "Bemba", "Bhojpuri", "Bikol", "Bini", 
    "Bislama", "Blackfoot", "Braj", "Brahui", "Breton", "Buginese", "Buhid", "Cakchiquel", "Californian", "Cantonese", "Carib", "Cayuga", 
    "Cebuano", "Chagatai", "Chamorro", "Chechen", "Cherokee", "Cheyenne", "Chibcha", "Chiga", "Chin", "Chipewyan", "Choctaw", "Church Slavic", 
    "Chuvash", "Comorian", "Coptic", "Cornish", "Corsican", "Cree", "Creek", "Crimean Tatar", "Croatian", "Dakota", "Dargwa", "Delaware", 
    "Dinka", "Divehi", "Dogri", "Douala", "Duala", "Dzongkha", "Efik", "Ekajuk", "Elamite", "Erzya", "Ewe", "Ewondo", "Fang", "Fanti", 
    "Faroese", "Fijian", "Filipino", "Finnish", "Fon", "Frafra", "Frisian", "Friulian", "Fulah", "Ga", "Gagauz", "Galician", "Ganda", 
    "Gayo", "Gbaya", "Geez", "Gilbertese", "Gondi", "Gorontalo", "Gothic", "Grebo", "Guarani", "Gujarati", "Gwich'in"
]

tones = [
    "Professional", "Casual", "Inspirational", "Motivational", "Humorous", "Empathetic", "Bold", "Encouraging", "Analytical", "Optimistic", 
    "Confident", "Direct", "Persuasive", "Engaging", "Friendly", "Warm", "Serious", "Critical", "Thoughtful", "Visionary", "Pragmatic", 
    "Respectful", "Conversational", "Exciting", "Academic", "Authoritative", "Balanced", "Candid", "Caring", "Cautious", "Challenging", 
    "Cheerful", "Clear", "Collaborative", "Commanding", "Compassionate", "Conciliatory", "Concerned", "Congratulatory", "Constructive", 
    "Contemplative", "Convincing", "Cooperative", "Creative", "Credible", "Curious", "Decisive", "Delightful", "Diplomatic", "Disarming", 
    "Dramatic", "Earnest", "Educational", "Eloquent", "Emotional", "Empowering", "Energetic", "Enlightening", "Enthusiastic", "Ethical", 
    "Evocative", "Excited", "Expert", "Explanatory", "Expressive", "Factual", "Fair", "Fascinating", "Fierce", "Firm", "Forward-Thinking", 
    "Genuine", "Gracious", "Grateful", "Guiding", "Helpful", "Honest", "Hopeful", "Humble", "Impartial", "Impassioned", "Inclusive", 
    "Informative", "Inquisitive", "Insightful", "Instructive", "Intellectual", "Intense", "Intimate", "Introspective", "Intuitive", 
    "Inviting", "Judicial", "Kind", "Knowledgeable", "Lighthearted", "Logical", "Loving", "Lyrical", "Matter-of-Fact", "Meditative", 
    "Methodical", "Mindful", "Modest", "Nurturing", "Objective", "Open-Minded", "Opinionated", "Passionate", "Patient", "Patriotic", 
    "Peaceful", "Personable", "Philosophical", "Pioneering", "Playful", "Poetic", "Polite", "Practical", "Proactive", "Problem-Solving", 
    "Progressive", "Provocative", "Questioning", "Quirky", "Rational", "Reassuring", "Reflective", "Reinforcing", "Relaxed", "Reliable", 
    "Resolute", "Resonant", "Resourceful", "Reverent", "Revolutionary", "Rigorous", "Robust", "Sarcastic", "Satirical", "Scholarly", 
    "Scientific", "Sensible", "Sensitive", "Sentimental", "Sincere", "Skeptical", "Smart", "Sobering", "Solemn", "Sophisticated", "Soulful", 
    "Spirited", "Spiritual", "Stimulating", "Strategic", "Straightforward", "Strong", "Supportive", "Surprised", "Sympathetic", "Tactical", 
    "Tactful", "Technical", "Tenacious", "Tender", "Thorough", "Thoughtful", "Thought-Provoking", "Tolerant", "Tough", "Transparent", 
    "Trendy", "Trustworthy", "Understanding", "Unexpected", "Unfiltered", "Upbeat", "Uplifting", "Urgent", "Vibrant", "Vigilant", 
    "Virtuous", "Visionary", "Vivid", "Vulnerable", "Welcoming", "Whimsical", "Wise", "Witty", "Wonder-Filled", "Worried", "Yearning", 
    "Zealous", "Adventurous", "Appreciative", "Articulate", "Astute", "Attentive", "Authentic", "Awe-Struck", "Breathtaking", "Calm", 
    "Captivating", "Celebratory", "Charismatic", "Civic-Minded", "Clever", "Committed", "Comforting", "Compelling", "Conscientious", 
    "Conservative", "Considerate", "Consistent", "Controversial", "Cool", "Courageous", "Cynical", "Daring", "Data-Driven", "Dazzling", 
    "Deliberate", "Devoted", "Dignified", "Diligent", "Dynamic", "Easy-Going", "Eclectic", "Economical", "Effervescent", "Efficient", 
    "Elegant", "Elevated", "Emotional", "Enchanting", "Encouraging", "Endearing", "Energetic", "Enigmatic", "Entertaining", "Entrepreneurial", 
    "Environmental", "Equitable", "Experimental", "Expository", "Extraordinary", "Fair-Minded", "Faithful", "Fearless", "Feminist", 
    "Fervent", "Festive", "Fiery", "Flamboyant", "Folksy", "Formal", "Fortifying", "Fresh", "Futuristic", "Gentle", "Gifted", "Gritty", 
    "Grounded", "Growth-Oriented", "Harmonious", "Hearty", "Heroic", "High-Energy", "Historical", "Holistic", "Idealistic", "Idiosyncratic", 
    "Illuminating", "Immersive", "Impactful", "Impeccable", "Impulsive", "Incisive", "Indignant", "Industrious", "Inimitable", "Innovative", 
    "Inquisitive", "Insistent", "Inspiring", "Instructional", "Intelligent", "Intentional", "Intimate", "Intriguing", "Judicial"
]


tones = [
    "Professional", "Casual", "Inspirational", "Motivational", "Humorous", "Empathetic", "Bold", "Encouraging", "Analytical", "Optimistic", 
    "Confident", "Direct", "Persuasive", "Engaging", "Friendly", "Warm", "Serious", "Critical", "Thoughtful", "Visionary", "Pragmatic", 
    "Respectful", "Conversational", "Exciting", "Academic", "Authoritative", "Balanced", "Candid", "Caring", "Cautious", "Challenging", 
    "Cheerful", "Clear", "Collaborative", "Commanding", "Compassionate", "Conciliatory", "Concerned", "Congratulatory", "Constructive", 
    "Contemplative", "Convincing", "Cooperative", "Creative", "Credible", "Curious", "Decisive", "Delightful", "Diplomatic", "Disarming", 
    "Dramatic", "Earnest", "Educational", "Eloquent", "Emotional", "Empowering", "Energetic", "Enlightening", "Enthusiastic", "Ethical", 
    "Evocative", "Excited", "Expert", "Explanatory", "Expressive", "Factual", "Fair", "Fascinating", "Fierce", "Firm", "Forward-Thinking", 
    "Genuine", "Gracious", "Grateful", "Guiding", "Helpful", "Honest", "Hopeful", "Humble", "Impartial", "Impassioned", "Inclusive", 
    "Informative", "Inquisitive", "Insightful", "Instructive", "Intellectual", "Intense", "Intimate", "Introspective", "Intuitive", 
    "Inviting", "Judicial", "Kind", "Knowledgeable", "Lighthearted", "Logical", "Loving", "Lyrical", "Matter-of-Fact", "Meditative", 
    "Methodical", "Mindful", "Modest", "Nurturing", "Objective", "Open-Minded", "Opinionated", "Passionate", "Patient", "Patriotic", 
    "Peaceful", "Personable", "Philosophical", "Pioneering", "Playful", "Poetic", "Polite", "Practical", "Proactive", "Problem-Solving", 
    "Progressive", "Provocative", "Questioning", "Quirky", "Rational", "Reassuring", "Reflective", "Reinforcing", "Relaxed", "Reliable", 
    "Resolute", "Resonant", "Resourceful", "Reverent", "Revolutionary", "Rigorous", "Robust", "Sarcastic", "Satirical", "Scholarly", 
    "Scientific", "Sensible", "Sensitive", "Sentimental", "Sincere", "Skeptical", "Smart", "Sobering", "Solemn", "Sophisticated", "Soulful", 
    "Spirited", "Spiritual", "Stimulating", "Strategic", "Straightforward", "Strong", "Supportive", "Surprised", "Sympathetic", "Tactical", 
    "Tactful", "Technical", "Tenacious", "Tender", "Thorough", "Thoughtful", "Thought-Provoking", "Tolerant", "Tough", "Transparent", 
    "Trendy", "Trustworthy", "Understanding", "Unexpected", "Unfiltered", "Upbeat", "Uplifting", "Urgent", "Vibrant", "Vigilant", 
    "Virtuous", "Visionary", "Vivid", "Vulnerable", "Welcoming", "Whimsical", "Wise", "Witty", "Wonder-Filled", "Worried", "Yearning", 
    "Zealous", "Adventurous", "Appreciative", "Articulate", "Astute", "Attentive", "Authentic", "Awe-Struck", "Breathtaking", "Calm", 
    "Captivating", "Celebratory", "Charismatic", "Civic-Minded", "Clever", "Committed", "Comforting", "Compelling", "Conscientious", 
    "Conservative", "Considerate", "Consistent", "Controversial", "Cool", "Courageous", "Cynical", "Daring", "Data-Driven", "Dazzling", 
    "Deliberate", "Devoted", "Dignified", "Diligent", "Dynamic", "Easy-Going", "Eclectic", "Economical", "Effervescent", "Efficient", 
    "Elegant", "Elevated", "Emotional", "Enchanting", "Encouraging", "Endearing", "Energetic", "Enigmatic", "Entertaining", "Entrepreneurial", 
    "Environmental", "Equitable", "Experimental", "Expository", "Extraordinary", "Fair-Minded", "Faithful", "Fearless", "Feminist", 
    "Fervent", "Festive", "Fiery", "Flamboyant", "Folksy", "Formal", "Fortifying", "Fresh", "Futuristic", "Gentle", "Gifted", "Gritty", 
    "Grounded", "Growth-Oriented", "Harmonious", "Hearty", "Heroic", "High-Energy", "Historical", "Holistic", "Idealistic", "Idiosyncratic", 
    "Illuminating", "Immersive", "Impactful", "Impeccable", "Impulsive", "Incisive", "Indignant", "Industrious", "Inimitable", "Innovative", 
    "Inquisitive", "Insistent", "Inspiring", "Instructional", "Intelligent", "Intentional", "Intimate", "Intriguing", "Judicial"
]
styles = ["None", "Hashtags", "Emojis", "Both Hashtags & Emojis", "Custom Formatting", "Bullet Points", "Lists", "Story Format", "Quotes", "Engagement Hooks", "Q&A Style", "Conversational", "Narrative", "Infographic-Oriented", "Tweet-Like", "Mini-Thread", "News Headline", "Interactive", "Slang-Friendly", "Puns & Wordplay", "Clickbait-Free", "Educational-Focused", "Professional Journal", "SEO-Friendly", "Visual Elements", "Data-Driven Insights", "Minimalist Style", "Call-to-Action Focused", "Humor-Infused", "Metaphor-Based", "Dialogue-Driven", "Question-Led", "Trend-Jacking"]

levels = [
    "Easy", "Medium", "Hard", "Advanced", "Nightmare", "Beginner", "Basic", "Intermediate", "Skilled", "Proficient", 
    "Fluent", "Creative", "Technical", "Master", "Legendary", "Expert", "Formal", "Casual", "Poetic", "Narrative", 
    "Academic", "Persuasive", "Descriptive", "Expository", "Satirical", "Argumentative", "Jargon-Heavy", "Metaphorical", 
    "Lyrical", "Abstract", "Concise", "Verbose", "Imaginative", "Sophisticated"
]


topics = [
    # Personal & Biographical
    "My Best Friend", "A Day at the Park", "Importance of Kindness", "My Favorite Animal", "A Trip to the Moon",
    "If I Had a Superpower", "A Letter to Santa", "Why Books Are Important", "The Magic Pencil", "A Rainy Day",
    "Saving the Environment", "The Funniest Day of My Life", "My Dream Job", "An Adventure in the Jungle",
    "How to Stay Healthy", "The Future of Technology", "A Story About Friendship", "A Mystery to Solve",
    "A Letter to My Future Self", "What If Animals Could Talk?"
    "My Best Friend",
    "My Childhood Memories",
    "A Day in My Life",
    "My Dream Job",
    "My Hometown",
    "My Family Traditions",
    "Personal Growth Journey",
    "Life Lessons I've Learned",
    "My Cultural Heritage",
    "My Educational Experience",
    
    # Academic Essays
    "Climate Change Impact Analysis",
    "Historical Event Analysis",
    "Literary Criticism Essay",
    "Scientific Research Summary",
    "Comparative Cultural Study",
    "Economic Theory Application",
    "Philosophical Concept Exploration",
    "Political System Analysis",
    "Environmental Policy Review",
    "Educational Theory Discussion",
    
    # Business Content
    "Executive Summary",
    "Business Proposal",
    "Marketing Strategy",
    "Brand Voice Guide",
    "Competitor Analysis",
    "Product Description",
    "Service Overview",
    "Company History",
    "Mission Statement",
    "Vision Statement",
    "SWOT Analysis",
    "Market Research Report",
    "Business Plan",
    "Annual Report",
    "Investor Pitch",
    "Customer Testimonial",
    "Case Study",
    "White Paper",
    "Industry Trend Analysis",
    "Sales Script",
    
    # Marketing & Advertising
    "Email Newsletter",
    "Social Media Post",
    "Ad Copy",
    "Landing Page Content",
    "Product Launch Announcement",
    "Press Release",
    "Promotional Campaign",
    "Contest Announcement",
    "Event Invitation",
    "Webinar Description",
    "Brand Story",
    "Slogan Generation",
    "Value Proposition",
    "Feature Highlight",
    "Benefit Explanation",
    "Call to Action",
    "Customer Pain Points",
    "Solution Presentation",
    "User Guide",
    "FAQ Section",
    
    # Creative Writing
    "Short Story",
    "Poem",
    "Dialogue Scene",
    "Character Sketch",
    "Setting Description",
    "Plot Outline",
    "Creative Prompt",
    "Flash Fiction",
    "Novel Chapter",
    "Fairy Tale",
    "Science Fiction Scenario",
    "Fantasy World Building",
    "Mystery Plot",
    "Romance Scene",
    "Thriller Excerpt",
    "Horror Story",
    "Adventure Narrative",
    "Historical Fiction",
    "Memoir Excerpt",
    "Personal Essay",
    
    # Technical Writing
    "Technical Specification",
    "API Documentation",
    "Code Explanation",
    "Software Manual",
    "Hardware Guide",
    "Troubleshooting Instructions",
    "Release Notes",
    "Technical Comparison",
    "System Requirements",
    "Implementation Guide",
    "Configuration Steps",
    "Data Analysis Report",
    "Technical Process Description",
    "Algorithm Explanation",
    "Technical Concept Definition",
    
    # Health & Wellness
    "Nutritional Guide",
    "Fitness Routine",
    "Mental Health Tips",
    "Wellness Practice",
    "Medical Condition Explanation",
    "Health Research Summary",
    "Diet Plan",
    "Exercise Instruction",
    "Stress Management Technique",
    "Sleep Improvement Guide",
    "Meditation Script",
    "Yoga Sequence",
    "Healthy Lifestyle Tips",
    "Symptom Checker",
    "Recovery Story",
    
    # Travel & Lifestyle
    "Travel Destination Guide",
    "Packing List",
    "Itinerary Planning",
    "Cultural Customs Guide",
    "Restaurant Review",
    "Hotel Description",
    "Tourist Attraction Overview",
    "Local Cuisine Exploration",
    "Travel Tips",
    "Adventure Activity Guide",
    "City Comparison",
    "Budget Travel Advice",
    "Luxury Experience Description",
    "Off-the-Beaten-Path Suggestions",
    "Travel Story",
    
    # Education & Learning
    "Lesson Plan",
    "Educational Resource",
    "Learning Objective",
    "Study Guide",
    "Quiz Questions",
    "Educational Activity",
    "Concept Explanation",
    "Teaching Strategy",
    "Learning Outcome Assessment",
    "Educational Research Summary",
    "Student Assignment",
    "Curriculum Overview",
    "Learning Theory Application",
    "Educational Technology Review",
    "Classroom Management Tips",
    
    # Web Content
    "Website Homepage",
    "About Us Page",
    "Services Page",
    "Contact Page",
    "Blog Post",
    "Article",
    "News Update",
    "Product Page",
    "Category Description",
    "Privacy Policy",
    "Terms of Service",
    "Cookie Policy",
    "User Agreement",
    "Portfolio Description",
    "Team Member Bio",
    
    # Professional Documents
    "Resume/CV",
    "Cover Letter",
    "Recommendation Letter",
    "Reference Letter",
    "Performance Review",
    "Job Description",
    "Professional Bio",
    "LinkedIn Profile",
    "Professional Statement",
    "Career Objective",
    "Skills Summary",
    "Work Experience Description",
    "Accomplishment Highlight",
    "Professional Development Plan",
    "Career Transition Narrative",
    
    # Social Media Content
    "Twitter/X Post",
    "Facebook Update",
    "Instagram Caption",
    "LinkedIn Article",
    "YouTube Video Description",
    "TikTok Script",
    "Pinterest Description",
    "Reddit Post",
    "Social Media Profile Bio",
    "Hashtag Strategy",
    "Social Media Calendar",
    "Engagement Post",
    "Poll Question",
    "Social Media Contest",
    "Social Media Trend Analysis",
    
    # Entertainment
    "Movie Review",
    "Book Review",
    "Music Review",
    "Game Review",
    "TV Show Recap",
    "Celebrity Profile",
    "Entertainment News",
    "Event Coverage",
    "Interview Questions",
    "Entertainment List Article",
    "Entertainment Recommendation",
    "Cultural Critique",
    "Performance Analysis",
    "Media Comparison",
    "Entertainment Industry Trend",
    
    # Legal Content
    "Legal Agreement",
    "Contract Clause",
    "Legal Notice",
    "Compliance Document",
    "Legal Procedure Explanation",
    "Legal Case Summary",
    "Law Interpretation",
    "Legal Rights Explanation",
    "Legal Requirement Outline",
    "Legal Disclaimer",
    "Legal FAQ",
    "Legal Advice Article",
    "Regulatory Update",
    "Legal Document Template",
    "Legal Term Definition",
    
    # Science & Technology
    "Scientific Discovery Explanation",
    "Technology Trend Analysis",
    "Tech Product Review",
    "Scientific Process Description",
    "Research Methodology",
    "Innovation Overview",
    "Technology Comparison",
    "Scientific Study Summary",
    "Future Technology Prediction",
    "Scientific Concept Explanation",
    "Tech Troubleshooting Guide",
    "Science News Update",
    "Technology Impact Analysis",
    "Scientific History Article",
    "Tech Industry Profile",
    
    # Finance & Economics
    "Financial Report",
    "Investment Analysis",
    "Economic Trend Forecast",
    "Budget Planning Guide",
    "Financial Advice Article",
    "Tax Explanation",
    "Financial Product Description",
    "Economic Policy Analysis",
    "Market Trend Report",
    "Financial Literacy Guide",
    "Retirement Planning",
    "Wealth Management Strategy",
    "Economic Theory Application",
    "Financial Risk Assessment",
    "Economic Impact Analysis",
    
    # Email Content
    "Cold Outreach Email",
    "Follow-up Email",
    "Thank You Email",
    "Introduction Email",
    "Networking Email",
    "Apology Email",
    "Request Email",
    "Invitation Email",
    "Confirmation Email",
    "Reminder Email",
    "Update Email",
    "Announcement Email",
    "Farewell Email",
    "Recommendation Request Email",
    "Feedback Request Email",
    
    # Persuasive Writing
    "Persuasive Essay",
    "Opinion Piece",
    "Argumentative Essay",
    "Debate Speech",
    "Position Statement",
    "Advocacy Article",
    "Campaign Message",
    "Call to Action Statement",
    "Persuasive Presentation",
    "Convincing Argument",
    "Value Proposition",
    "Benefit Statement",
    "Problem-Solution Outline",
    "Persuasive Letter",
    "Motivational Message",
    
    # Special Occasions
    "Wedding Toast",
    "Eulogy",
    "Graduation Speech",
    "Anniversary Message",
    "Birthday Wish",
    "Congratulatory Note",
    "Holiday Greeting",
    "Invitation Text",
    "Welcome Speech",
    "Farewell Message",
    "Award Acceptance Speech",
    "Recognition Speech",
    "Celebratory Announcement",
    "Memorial Tribute",
    "Baby Shower Message",
    
    # SEO Content
    "SEO-Optimized Blog Post",
    "Keyword Research Analysis",
    "Meta Description",
    "Title Tag",
    "Header Tag Optimization",
    "SEO Content Brief",
    "Content Cluster Plan",
    "Pillar Page Content",
    "Long-Tail Keyword Article",
    "Local SEO Content",
    "Voice Search Optimization",
    "Featured Snippet Content",
    "SEO Strategy Document",
    "Competitor SEO Analysis",
    "Link-Building Content",
    
    # Current Events & News
    "News Article",
    "Current Event Analysis",
    "News Summary",
    "Event Coverage",
    "Commentary Article",
    "Trend Report",
    "Political Analysis",
    "Cultural Commentary",
    "Breaking News Update",
    "Investigative Report",
    "Interview Transcript",
    "Public Statement",
    "Media Response",
    "Crisis Communication",
    "Public Announcement",
    
    # Storytelling Formats
    "Hero's Journey Narrative",
    "Case Study Story",
    "Personal Transformation Story",
    "Customer Success Story",
    "Origin Story",
    "Challenge-Solution-Result Narrative",
    "Before-After Story",
    "Day-in-the-Life Narrative",
    "Behind-the-Scenes Story",
    "Failure-to-Success Story",
    "Inspirational Journey",
    "Cautionary Tale",
    "Myth or Legend Adaptation",
    "Historical Narrative",
    "Future Scenario",
    
    # Instructional & How-To
    "Step-by-Step Tutorial",
    "How-To Guide",
    "DIY Instructions",
    "Process Explanation",
    "Quick Start Guide",
    "Beginner's Guide",
    "Advanced Technique Guide",
    "Troubleshooting Walkthrough",
    "Recipe",
    "Craft Instructions",
    "Life Hack Explanation",
    "Best Practice Guide",
    "Tips and Tricks Article",
    "Maintenance Guide",
    "Setup Instructions",
    
    # Community & Social
    "Community Guidelines",
    "Group Introduction",
    "Volunteer Opportunity Description",
    "Community Event Announcement",
    "Membership Benefits",
    "Social Cause Explanation",
    "Nonprofit Mission Statement",
    "Donation Appeal",
    "Community Success Story",
    "Collaborative Project Description",
    "Community Challenge",
    "Social Impact Report",
    "Community Survey",
    "Social Movement Explanation",
    "Community Resource Guide"
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

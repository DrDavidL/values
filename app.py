import streamlit as st
from google import genai

st.set_page_config(page_title="Value Cards App", page_icon="🔮", layout="wide")
st.title("Value Cards App")
st.write("Select your core values from each category below. Toggle the items you resonate with, and your final list will update below.")

col1, col3 = st.columns(2, gap="medium")
with col1:

    # Final, expanded categorized core values
    categories = {
        "I. Authenticity & Integrity": [
            "Authenticity", "Honesty", "Integrity", "Sincerity", "Vulnerability", "Truth", 
            "Uniqueness", "Intuition", "Self-respect"
        ],
        "II. Personal Growth & Achievement": [
            "Achievement", "Ambition", "Growth", "Learning", "Determination", "Perseverance",
            "Discipline / Self-discipline", "Initiative", "Curiosity", "Innovation", 
            "Creativity", "Resourcefulness", "Accountability", "Legacy", "Risk-taking", 
            "Personal Fulfillment", "Understanding", "Wisdom", "Adaptability", "Commitment", 
            "Competence", "Excellence", "Knowledge", "Pride", "Success", "Diligence"
        ],
        "III. Independence & Freedom": [
            "Autonomy", "Freedom", "Independence", "Self-reliance"
        ],
        "IV. Interpersonal Relationships & Connection": [
            "Connection", "Compassion", "Empathy", "Kindness", "Caring", "Friendship", 
            "Belonging", "Community", "Loyalty", "Family", "Teamwork", "Collaboration", 
            "Cooperation", "Love", "Trust"
        ],
        "V. Leadership & Influence": [
            "Authority", "Leadership", "Influence", "Confidence", "Power", "Recognition", "Vision"
        ],
        "VI. Well-being, Balance & Happiness": [
            "Balance", "Harmony", "Health", "Well-being", "Joy", "Contentment", "Peace", 
            "Serenity", "Fun", "Optimism", "Patience", "Gratitude", "Hope", "Humor", 
            "Leisure", "Wholeheartedness", "Simplicity"
        ],
        "VII. Ethical & Moral Values": [
            "Fairness", "Justice", "Ethics", "Responsibility", "Respect", "Honor", "Humility", 
            "Forgiveness", "Non-violence", "Tradition", "Dignity"
        ],
        "VIII. Stability & Security": [
            "Financial Stability", "Job Security", "Safety", "Security", "Order", "Stability", 
            "Dependability", "Reliability", "Thrift", "Home", "Wealth"
        ],
        "IX. Generosity & Contribution": [
            "Generosity", "Contribution", "Service", "Giving", "Making a Difference", 
            "Stewardship", "Altruism", "Future Generations"
        ],
        "X. Aesthetics & Appreciation": [
            "Beauty", "Appreciation", "Grace"
        ],
        "XI. Exploration & Experience": [
            "Adventure", "Boldness", "Bravery", "Travel", "Challenge", "Courage"
        ],
        "XII. Miscellaneous & Broader Values": [
            "Citizenship", "Efficiency", "Enthusiasm", "Equality", "Faith", "Inclusion", 
            "Career", "Nature", "Environment", "Openness", "Parenting", "Patriotism", 
            "Self-expression", "Sportsmanship", "Time", "Usefulness", "Diversity", "Spirituality"
        ]
    }

    # Create a session state list to collect selected values
    if "final_selection" not in st.session_state:
        st.session_state.final_selection = []

    st.write("## Select Your Values")
    for category, values in categories.items():
        with st.expander(category):
            selected = st.multiselect(
                f"Select values from {category}",
                options=values,
                key=category
            )
            # Append selections to the session state
            st.session_state.final_selection.extend(selected)
            
with col3:

    st.write("## Your Final Values List")
    if st.session_state.final_selection:
        # Remove duplicates and sort alphabetically for clarity
        unique_values = sorted(set(st.session_state.final_selection))
        for value in unique_values:
            st.write(f"- {value}")
    else:
        st.info("No values selected yet.")

    st.markdown("---")
    st.markdown(
        "**Sources:** This app’s values list is based on curated items from "
        "[James Clear](https://jamesclear.com/core-values), "
        "[Brené Brown](https://brenebrown.com/resources/dare-to-lead-list-of-values/), "
        "[Nir Eyal](https://www.nirandfar.com/common-values/), and "
        "[Colin Breck](https://blog.colinbreck.com/understanding-our-core-values-an-exercise-for-individuals-and-teams/)."
    )

    # Proceed only if there are selected values
    if st.session_state.final_selection:
        st.write("## Step 2: Choose Two Core Values to Form Buckets")
        # Let user choose exactly two core values from their final list.
        selected_cores = st.multiselect("Select two core values from your final list to form your two main buckets:",
                                        options=unique_values, key="core_values", max_selections=2)
        
        if len(selected_cores) == 2:
            st.write("### Organize Your Values into Buckets")
            st.write("Assign each of your final values into one of the two buckets below.")
            
            # For each bucket, allow the user to choose items from the unique_values list.
            bucket1 = st.multiselect(f"Select values for bucket **{selected_cores[0]}**:", 
                                    options=unique_values, key="bucket1")
            bucket2 = st.multiselect(f"Select values for bucket **{selected_cores[1]}**:", 
                                    options=unique_values, key="bucket2")
            
            # Display the buckets for clarity
            st.write("#### Bucket Organization")
            st.write(f"**{selected_cores[0]} Bucket:** {bucket1}")
            st.write(f"**{selected_cores[1]} Bucket:** {bucket2}")
            
            # Finalize and make LLM calls using the provided code when the button is clicked.
            if st.button("Finalize Statements"):
                try:
                    # Import the client library for LLM call
                    from google import genai
                    
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                    
                    # Build the statements with the chosen core value and interweaved bucket values.
                    statement1 = f"I value {selected_cores[0]} - " + ", ".join(bucket1)
                    statement2 = f"I value {selected_cores[1]} - " + ", ".join(bucket2)
                    
                    # LLM call for the first statement
                    response1 = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=statement1,
                    )
                    # LLM call for the second statement
                    response2 = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=statement2,
                    )
                    
                    st.write("### Final Statements from LLM")
                    st.write(response1.text)
                    st.write(response2.text)
                except Exception as e:
                    st.error(f"An error occurred during the LLM call: {e}")
        else:
            st.info("Please select exactly two core values to create your buckets.")

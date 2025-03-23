import streamlit as st
from google import genai

st.set_page_config(page_title="Value Cards App", page_icon="🔮", layout="wide")
st.title("Value Cards App")
st.write("Select your core values from each category below. Toggle the items you resonate with, and your tier 2 list will update on the right side.")
with st.expander("About this App"):
    st.write(
        "This app helps you identify and organize your core values. "
        "Select your values from the list, then choose two core values to form buckets. "
        "Finally, organize your values into the two buckets to generate your final statements."
        "The draft statements at the end are generated using the [Gemini Language Model](https://aistudio.google.com/)."
        "This app was authored by David Liebovitz, MD, and is open-source on [GitHub](https://github.com/DrDavidL/values)."
    )
    st.markdown("---")
    st.markdown(
        "**Sources:** This app’s values list is based on curated items from "
        "[James Clear](https://jamesclear.com/core-values), "
        "[Brené Brown](https://brenebrown.com/resources/dare-to-lead-list-of-values/), "
        "[Nir Eyal](https://www.nirandfar.com/common-values/), and "
        "[Colin Breck](https://blog.colinbreck.com/understanding-our-core-values-an-exercise-for-individuals-and-teams/)."
    )

# Define categories and associated values
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

# Compute the final selection from toggles
final_selection = []

col1, col3 = st.columns(2, gap="medium")
with col1:
    st.write("## Select Your Values")
    # Loop over each category and each value within the category.
    for category, values in categories.items():
        with st.expander(category):
            for value in values:
                # Use a toggle for each value.
                if st.toggle(label=value, key=f"{category}_{value}"):
                    final_selection.append(value)

    # Store the final selection in session state if needed later.
    st.session_state.final_selection = final_selection

with col3:
    st.write("## Your Tier 2 Values List")
    if final_selection:
        unique_values = sorted(set(final_selection))
        for value in unique_values:
            st.write(f"- {value}")
    else:
        st.info("No values selected yet.")



    if final_selection:
        st.write("## Step 2: Choose Two Values to Form Tier 1 Buckets")
        unique_values = sorted(set(final_selection))
        selected_cores = st.multiselect(
            "Select two core values from your tier 2 list to form your two tier 1 buckets:",
            options=unique_values, key="core_values", max_selections=2
        )
        
        if len(selected_cores) == 2:
            st.write("### Organize Your Tier 2 Values into  Your Tier 1 Buckets")
            st.write("Assign each of your final values into one of the two buckets below.")
            
            bucket1 = st.multiselect(
                f"Select values for bucket **{selected_cores[0]}**:", 
                options=unique_values, key="bucket1"
            )
            bucket2 = st.multiselect(
                f"Select values for bucket **{selected_cores[1]}**:", 
                options=unique_values, key="bucket2"
            )
            
            # st.write("#### Bucket Organization")
            # st.write(f"**{selected_cores[0]} Bucket:** {bucket1}")
            # st.write(f"**{selected_cores[1]} Bucket:** {bucket2}")
            
            if st.button("Draft Values Statements"):
                try:
                    from google import genai
                    
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                    
                    statement1 = f"I value {selected_cores[0]} - " + ", ".join(bucket1)
                    statement2 = f"I value {selected_cores[1]} - " + ", ".join(bucket2)
                    
                    response1 = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=f"""Rephrase each of the following statements to convey a draft essence of the user\'s core values. Return only numbered rephrased versions, not other comments or information.:
                        Statement 1: {statement1},
                        Statement 2: {statement2}""",
                    )
                    st.write(f'1. {statement1}')
                    st.write(f'2. {statement2}')
                    st.write("### Draft Statements")
                    st.write(response1.text)
                except Exception as e:
                    st.error(f"An error occurred during the LLM call: {e}")
        else:
            st.info("Please select exactly two core values to create your buckets.")

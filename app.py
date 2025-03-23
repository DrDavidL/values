import streamlit as st

st.title("Value Cards App")
st.write("Select your core values from each category below. Toggle the items you resonate with, and your final list will update below.")

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
        # Because each category call is separate, we will store them in session state
        # and compile them after the loop
        st.session_state.final_selection.extend(selected)

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


import os
import streamlit as st
from google import genai
from datetime import datetime

# --------------------------------------------------
# CLINMIND AI v1.0
# Clinical Thinking Partner
# --------------------------------------------------

st.set_page_config(
    page_title="ClinMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: #F5F7FB;
}
.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #14233F;
    letter-spacing: -1px;
}
.subtitle {
    color: #68758B;
    font-size: 15px;
}
.section-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E4E9F1;
    margin-bottom: 12px;
}
.warning-text {
    color: #A65C19;
    font-size: 13px;
}
div.stButton > button {
    border-radius: 9px;
    font-weight: 650;
    min-height: 44px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "")


# --------------------------------------------------
# AI REASONING ENGINE
# --------------------------------------------------

SYSTEM_INSTRUCTIONS = """
You are ClinMind AI, a clinician-facing clinical reasoning
and educational discussion assistant.

YOUR PURPOSE:
Help clinicians critically examine clinical cases.
Do not simply agree with the clinician's initial hypothesis.

IMPORTANT LIMITATIONS:
- You are not a doctor.
- You do not make definitive diagnoses.
- You do not prescribe medicines or treatment.
- Do not replace clinical examination or professional judgment.
- Never invent patient findings, laboratory results, or references.
- Distinguish established facts from assumptions.
- Explicitly state uncertainty.
- Do not calculate clinical risk scores unless all required
  validated inputs are provided and the method is appropriate.
- If critical information is missing, explain what is missing.
- Highlight potentially urgent warning signs when relevant.
- Do not falsely reassure when important information is absent.
- Do not assume a common diagnosis is correct simply because
  it is the clinician's initial hypothesis.
- Do not invent citations. Only identify evidence sources
  when you can do so reliably.

Use the following structure:

1. CASE UNDERSTANDING
Summarize the supplied case without adding facts.

2. INITIAL HYPOTHESIS REVIEW
Examine the clinician's proposed explanation.
Identify supporting and contradictory findings.

3. ALTERNATIVE EXPLANATIONS
Discuss relevant differential possibilities.
For each, explain why it may or may not fit.
Avoid presenting a ranked definitive diagnosis.

4. WHAT MAY BE MISSING?
Identify important history, examination findings,
and investigations that may be relevant.
Explain why each matters.

5. CLINICAL CHALLENGE
Ask the clinician three useful questions that could
change their current thinking.

6. SAFETY REVIEW
Identify potential warning signs and circumstances
that may require urgent in-person assessment.
Do not claim that their absence has been established
unless the case explicitly provides that information.

7. EVIDENCE TO REVIEW
Suggest relevant clinical guidelines, authoritative
medical resources, or research topics.
Clearly distinguish suggested reading from verified sources.

8. LEARNING POINT
Give one concise educational takeaway.

Always maintain a respectful, collaborative tone.
Do not shame or criticize the clinician.
"""


def generate_clinical_analysis(api_key, model, case):
    client = genai.Client(api_key=api_key)

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

Analyze the following FICTIONAL educational case.

PATIENT AGE:
{case['age']}

SEX (IF PROVIDED):
{case['sex']}

CLINICAL SPECIALTY:
{case['specialty']}

PRESENTING COMPLAINT:
{case['complaint']}

DURATION:
{case['duration']}

RELEVANT HISTORY:
{case['history']}

CLINICAL FINDINGS:
{case['findings']}

CLINICIAN'S INITIAL HYPOTHESIS:
{case['hypothesis']}

SPECIFIC QUESTION FROM THE CLINICIAN:
{case['question']}

Provide a careful, structured clinical reasoning discussion.
Do not add information that was not supplied.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise ValueError("The AI returned an empty response.")

    return response.text


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🧠 ClinMind AI")

    st.caption("Clinical Thinking Partner")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("""
    - 🧠 Clinical Challenge
    - 📚 Evidence Explorer (Coming soon)
    - 📓 Learning Journal (Coming soon)
    - 📊 Experience Intelligence (Coming soon)
    """)

    st.divider()

    st.markdown("### System information")
    st.caption("Version: 1.0.0")
    st.caption("AI engine: Google Gemini")
    st.caption("Mode: Educational prototype")

    st.divider()

    st.markdown("""
    **Development roadmap**

    1. Clinical reasoning
    2. Evidence retrieval
    3. Case learning
    4. Experience analytics
    """)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">ClinMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Think beyond the first diagnosis. '
    'Challenge assumptions. Explore clinical uncertainty.</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "Educational prototype: Use fictional cases only. "
    "Do not enter patient names, contact information, "
    "medical record numbers, or identifiable patient details. "
    "This application is not validated for clinical decisions."
)

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AI Engine", "Gemini")

with col2:
    st.metric("Core Module", "Clinical Challenge")

with col3:
    st.metric("Version", "1.0")

st.divider()

# --------------------------------------------------
# CASE INPUT
# --------------------------------------------------

st.markdown("## 🧠 Clinical Case Workspace")

st.markdown(
    "Enter a fictional clinical scenario for structured "
    "reasoning and educational discussion."
)

with st.form("clinical_case_form"):

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Patient age",
            min_value=0,
            max_value=120,
            value=48
        )

        sex = st.selectbox(
            "Sex",
            ["Not specified", "Female", "Male", "Other"]
        )

        specialty = st.selectbox(
            "Clinical specialty",
            [
                "General Medicine",
                "General Practice",
                "Dentistry",
                "Cardiology",
                "Gastroenterology",
                "Orthopaedics",
                "Dermatology",
                "ENT",
                "Neurology",
                "Other"
            ]
        )

    with col2:
        duration = st.text_input(
            "Duration of symptoms",
            placeholder="Example: 3 weeks"
        )

        complaint = st.text_input(
            "Presenting complaint",
            placeholder="Example: Recurrent abdominal discomfort"
        )

    history = st.text_area(
        "Relevant medical and clinical history",
        placeholder=(
            "Describe relevant history, risk factors, "
            "previous episodes and associated symptoms."
        ),
        height=120
    )

    findings = st.text_area(
        "Clinical findings",
        placeholder=(
            "Enter the available examination findings "
            "and any relevant investigation results."
        ),
        height=120
    )

    hypothesis = st.text_area(
        "What is your initial clinical hypothesis?",
        placeholder="Describe your current clinical thinking.",
        height=90
    )

    question = st.text_area(
        "What would you like ClinMind to challenge?",
        placeholder=(
            "Example: What important alternatives "
            "or missing information should I consider?"
        ),
        height=90
    )

    confirm_synthetic = st.checkbox(
        "I confirm this is a fictional educational case "
        "and contains no real patient information."
    )

    submitted = st.form_submit_button(
        "🧠 Analyse Clinical Case",
        use_container_width=True
    )

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if submitted:

    if not confirm_synthetic:
        st.error("Please confirm that this is a fictional case.")

    elif not complaint.strip():
        st.error("Please enter a presenting complaint.")

    elif not history.strip() and not findings.strip():
        st.error("Please provide some clinical context.")

    else:

        api_key = get_api_key()

        if not api_key:
            st.error(
                "Gemini API key not found. "
                "Add GEMINI_API_KEY to Streamlit Secrets."
            )

        else:

            model = os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            )

            case = {
                "age": age,
                "sex": sex,
                "specialty": specialty,
                "duration": duration or "Not specified",
                "complaint": complaint,
                "history": history or "Not provided",
                "findings": findings or "Not provided",
                "hypothesis": hypothesis or "Not specified",
                "question": question or "General clinical challenge"
            }

            with st.spinner(
                "ClinMind is examining the case..."
            ):

                try:
                    analysis = generate_clinical_analysis(
                        api_key,
                        model,
                        case
                    )

                    st.session_state["analysis"] = analysis
                    st.session_state["case"] = case
                    st.session_state["analysis_time"] = (
                        datetime.now().strftime("%d %b %Y, %I:%M %p")
                    )

                except Exception as error:
                    st.error(
                        "Unable to generate the analysis. "
                        "Check your API key, model availability, "
                        "API quota and application logs."
                    )
                    st.caption(str(error))


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "analysis" in st.session_state:

    st.divider()

    st.markdown("## 📋 Clinical Challenge Report")

    st.caption(
        "Generated: " + st.session_state["analysis_time"]
    )

    st.markdown(st.session_state["analysis"])

    st.divider()

    st.markdown("### Doctor's feedback")

    feedback = st.radio(
        "How useful was this clinical discussion?",
        [
            "Very useful",
            "Somewhat useful",
            "Not useful",
            "Potentially misleading"
        ],
        horizontal=True,
        key="feedback"
    )

    learning = st.text_area(
        "What did you learn from this case?",
        placeholder="Record an educational takeaway..."
    )

    st.caption(
        "Feedback remains in this session and is not "
        "automatically sent to a training system."
    )

    report = f"""
CLINMIND AI - CLINICAL CHALLENGE REPORT
Generated: {st.session_state['analysis_time']}

FICTIONAL CASE
{st.session_state['case']}

AI ANALYSIS
{st.session_state['analysis']}

DOCTOR FEEDBACK
{feedback}

LEARNING NOTE
{learning}
"""

    st.download_button(
        "⬇️ Download Clinical Learning Report",
        data=report,
        file_name="clinmind_learning_report.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("Start a new case", use_container_width=True):
        st.session_state.pop("analysis", None)
        st.session_state.pop("case", None)
        st.session_state.pop("analysis_time", None)
        st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center>ClinMind AI · Clinical Thinking Partner · "
    "Educational Prototype v1.0</center>",
    unsafe_allow_html=True
)

"""Grade 9 AI Math Differentiator: Streamlit + Google Gemini."""

import os

import streamlit as st
from google import genai

st.set_page_config(page_title="AI Math Differentiator", page_icon="📐", layout="centered")

MODEL = "gemini-3.5-flash-lite"
LEVEL_GUIDANCE = {
    "Foundation": (
        "Create an easy version with small integers and factorable roots. "
        "Include two scaffold questions that guide a beginner. "
        "Keep the wording simple and supportive."
    ),
    "Standard": (
        "Create a grade-9-level version needing independent calculation. "
        "Keep appropriate challenge and avoid giving away the method."
    ),
    "Advanced": (
        "Create a more challenging extension involving a realistic situation, "
        "more than one reasoning step, or checking a restriction on an answer. "
        "Keep it mathematically solvable by a grade-9 student."
    ),
}


def get_api_key():
    """Read the key from Streamlit Cloud Secrets (or an environment variable)."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None
    except Exception as e:
        
        print(f"Gemini API error: {type(e).__name__}: {e}", flush=True)



def ask_ai(prompt):
    """Call Gemini on the server, never in a browser/client JavaScript."""
    key = get_api_key()
    if not key:
        st.error("AI key is missing. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
        return None
    try:
        with st.spinner("AI is thinking…"):
            response = genai.Client(api_key=key).models.generate_content(
                model=MODEL,
                contents=prompt,
            )
        if not response.text:
            st.error("AI returned an empty response. Try again.")
            return None
        return response.text
    except Exception:
        st.error("AI request failed. Check your Gemini API key, model access, and rate limits.")
        return None


st.title("📐 AI Math Differentiator")
st.write("**Grade 9 · Algebra · Differentiated learning**")
st.caption("One mathematical concept, three learning pathways. Built with Streamlit and Gemini.")

core_task = st.text_area(
    "Core mathematical task",
    value="Solve the quadratic equation x² − 5x + 6 = 0.",
    height=90,
    help="Keep one central mathematical concept. AI will adapt its difficulty.",
)
level = st.radio(
    "Choose a learning level",
    ["Foundation", "Standard", "Advanced"],
    horizontal=True,
)

st.info({
    "Foundation": "Guided entry: easier numbers and scaffold questions.",
    "Standard": "Curriculum-level problem with independent reasoning.",
    "Advanced": "Real-world or multi-step extension.",
}[level])

context = (core_task.strip(), level)
if st.session_state.get("context") != context:
    st.session_state["context"] = context
    for item in ("problem", "hint", "solution", "feedback"):
        st.session_state[item] = ""

if st.button("✨ Generate adapted problem", type="primary", use_container_width=True):
    if not core_task.strip():
        st.warning("Please enter a core mathematical task.")
    else:
        prompt = f"""
You are a careful Grade 9 mathematics teacher designing differentiated instruction.
The ONE core task is: {core_task}
Selected difficulty: {level}.
Differentiation requirements: {LEVEL_GUIDANCE[level]}

Write exactly ONE student-facing task that practices the same core mathematical idea.
Use mathematically consistent numbers and prefer integer answers when possible.
Do not include the final answer or full solution yet.
Use concise, clear English (B1 or easier).
Format your response with these headings:
### Adapted problem
### Student instructions
### What you should learn
For Foundation, include two guiding questions under Student instructions.
"""
        result = ask_ai(prompt)
        if result:
            st.session_state["problem"] = result
            st.session_state["hint"] = ""
            st.session_state["solution"] = ""
            st.session_state["feedback"] = ""

if st.session_state.get("problem"):
    st.divider()
    st.markdown(st.session_state["problem"])

    left, right = st.columns(2)
    with left:
        if st.button("💡 Get a hint", use_container_width=True):
            result = ask_ai(
                f"Act as a Grade 9 tutor. The level is {level}. "
                f"Give one specific, helpful hint without stating the final answer "
                f"or giving the entire solution. Student task:\n{st.session_state['problem']}"
            )
            if result:
                st.session_state["hint"] = result
    with right:
        if st.button("📖 Show step-by-step solution", use_container_width=True):
            result = ask_ai(
                f"You are a careful Grade 9 math teacher. Solve this problem accurately "
                f"with a short, level-appropriate step-by-step explanation. "
                f"Show a final check, and state any real-world restrictions. "
                f"Level: {level}. Problem:\n{st.session_state['problem']}"
            )
            if result:
                st.session_state["solution"] = result

    if st.session_state.get("hint"):
        st.markdown("#### Your hint")
        st.markdown(st.session_state["hint"])
    if st.session_state.get("solution"):
        st.markdown("#### Worked solution")
        st.markdown(st.session_state["solution"])

    student_answer = st.text_area(
        "Try it yourself: your answer or working",
        placeholder="Example: x = 2 or x = 3 because ...",
        height=100,
    )
    if st.button("✅ Check my answer", use_container_width=True):
        if not student_answer.strip():
            st.warning("Enter your answer or working first.")
        else:
            result = ask_ai(
                f"You are a supportive Grade 9 math teacher. Check the student's work "
                f"for correctness; compute independently instead of trusting the student's claims. "
                f"State Correct, Partly correct, or Not yet correct and explain why. "
                f"Give one level-appropriate next step. Use clear and kind English. "
                f"Level: {level}. Problem:\n{st.session_state['problem']}\n"
                f"Student response:\n{student_answer}"
            )
            if result:
                st.session_state["feedback"] = result
    if st.session_state.get("feedback"):
        st.markdown("#### AI feedback")
        st.markdown(st.session_state["feedback"])

st.divider()
st.caption("AI can make mathematical mistakes. A teacher should verify generated tasks and solutions.")

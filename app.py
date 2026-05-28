import os
import streamlit as st
from openai import OpenAI

SYSTEM_PROMPT = """You are a Python data analysis expert helping marketing analysts write data scripts.

When the user describes a marketing data task, respond in EXACTLY four sections with these labels:

## 1. Python Code
Provide complete, runnable Python code for the task.

## 2. Section-by-Section Explanation
Describe what each part of the code does in plain English, step by step. No technical jargon.

## 3. Assumption Warnings
List any lines or blocks that assume something specific about the user's data — such as column names, file formats, data types, or structure. If none, say "None."

## 4. Interview Summary
Write a short paragraph (3–5 sentences) the analyst could read aloud to explain what the script does. Do not mention AI, ChatGPT, or any AI tool. Write it as if the analyst wrote the script themselves.

Always include all four sections, in order, using exactly those headers.
"""

def call_openai(messages: list[dict]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content

def render_response(text: str):
    sections = {
        "## 1. Python Code": None,
        "## 2. Section-by-Section Explanation": None,
        "## 3. Assumption Warnings": None,
        "## 4. Interview Summary": None,
    }
    headers = list(sections.keys())
    positions = {}
    for h in headers:
        idx = text.find(h)
        if idx != -1:
            positions[h] = idx

    sorted_headers = sorted(positions.items(), key=lambda x: x[1])

    for i, (header, start) in enumerate(sorted_headers):
        end = sorted_headers[i + 1][1] if i + 1 < len(sorted_headers) else len(text)
        content = text[start + len(header):end].strip()
        sections[header] = content

    labels = {
        "## 1. Python Code": ("Python Code", "code"),
        "## 2. Section-by-Section Explanation": ("Section-by-Section Explanation", "text"),
        "## 3. Assumption Warnings": ("Assumption Warnings", "text"),
        "## 4. Interview Summary": ("Interview Summary", "text"),
    }

    for header in headers:
        label, kind = labels[header]
        content = sections.get(header)
        if content is None:
            continue
        with st.expander(label, expanded=True):
            if kind == "code":
                # Strip markdown fences if present
                code = content
                if code.startswith("```"):
                    lines = code.split("\n")
                    code = "\n".join(lines[1:])
                if code.endswith("```"):
                    code = code[: code.rfind("```")].rstrip()
                st.code(code, language="python")
            else:
                st.markdown(content)


st.set_page_config(page_title="MarketScript", page_icon="📊", layout="centered")
st.title("📊 MarketScript")
st.caption("Describe a marketing data task and get ready-to-run Python code with plain-English explanations.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "history" not in st.session_state:
    st.session_state.history = []  # list of (prompt, response) for display
if "generated" not in st.session_state:
    st.session_state.generated = False

# Render past exchanges
for i, (prompt, response) in enumerate(st.session_state.history):
    label = "Initial request" if i == 0 else f"Refinement {i}"
    st.markdown(f"---\n**{label}:** {prompt}")
    render_response(response)

# Input area
if not st.session_state.generated:
    placeholder = "e.g. Read a CSV of customer orders, group by product category, and calculate total revenue and average order value per category."
    label = "Describe your marketing data task"
else:
    placeholder = 'e.g. "group by region instead of age" or "add a bar chart of the results"'
    label = "Refine the script"

with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area(label, placeholder=placeholder, height=100)
    submitted = st.form_submit_button("Generate" if not st.session_state.generated else "Refine")

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Generating script…"):
        response_text = call_openai(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.history.append((user_input.strip(), response_text))
    st.session_state.generated = True
    st.rerun()

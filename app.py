import streamlit as st

import os
import docx
from io import BytesIO

from resume_utils import extract_text_from_pdf
from generator import generate_cover_letter, generate_resume_bullets, generate_full_resume
from pdf_utils import create_resume_pdf

openai_api_key = st.secrets["api_keys"]["openai"]

# Streamlit page configuration
st.set_page_config(
    page_title="Smart Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {background-color: #f5f7fa;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
    .stTextInput, .stTextArea {border-radius: 8px;}
    .stFileUploader {border: 2px dashed #d3d3d3; padding: 10px;}
    .stSuccess {background-color: #e6f3e6; border-radius: 8px;}
    .stWarning {background-color: #fff3e0; border-radius: 8px;}
    .stError {background-color: #ffe6e6; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing generated outputs
if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.cover_letter = None
    st.session_state.resume_bullets = None
    st.session_state.full_resume_content = None
    st.session_state.pdf_file = None
    st.session_state.template = None
    st.session_state.cover_letter_widget = ""  # Separate key for widget value
    st.session_state.full_resume_widget = ""  # Separate key for widget value

# Sidebar for inputs
with st.sidebar:
    st.header("📋 Input Details")
    job_title = st.text_input(
        "🔍 Job Title",
        placeholder="e.g., Software Engineer",
        help="Enter the job title you're applying for."
    )
    job_description = st.text_area(
        "📝 Job Description",
        placeholder="Paste the job description here...",
        height=200,
        max_chars=5000,
        help="Provide the job description to tailor your documents."
    )
    resume_file = st.file_uploader(
        "📤 Upload Resume (PDF)",
        type=["pdf"],
        help="Upload your existing resume in PDF format (max 5MB).",
        accept_multiple_files=False
    )
    # Template selection
    template = st.selectbox(
        "🎨 Select Template",
        ["Professional", "Modern", "Creative"],
        help="Choose a style for your resume and cover letter."
    )
    generate_full = st.checkbox("🧾 Generate Full Resume (Enhanced)", value=True)
    generate_button = st.button("🚀 Generate Documents", use_container_width=True)
    if st.session_state.generated:
        if st.button("🗑️ Clear Session", use_container_width=True):
            st.session_state.generated = False
            st.session_state.cover_letter = None
            st.session_state.resume_bullets = None
            st.session_state.full_resume_content = None
            st.session_state.pdf_file = None
            st.session_state.template = None
            st.session_state.cover_letter_widget = ""
            st.session_state.full_resume_widget = ""
            st.experimental_rerun()

# Main content area with tabs
st.title("📄 Smart Resume & Cover Letter Generator")
st.markdown("Create tailored cover letters and resumes effortlessly using AI-powered generation!")

if generate_button:
    # Input validation
    if not job_title or not job_description or not resume_file:
        st.warning("⚠️ Please provide job title, job description, and upload a resume.")
    elif resume_file.size > 5 * 1024 * 1024:  # 5MB limit
        st.warning("⚠️ Resume file size exceeds 5MB. Please upload a smaller file.")
    else:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Extract resume text
            status_text.text("📄 Reading your resume...")
            progress_bar.progress(20)
            resume_text = extract_text_from_pdf(resume_file)

            # Step 2: Generate cover letter
            status_text.text("✍️ Generating cover letter...")
            progress_bar.progress(40)
            st.session_state.cover_letter = generate_cover_letter(job_title, job_description, resume_text, openai_api_key, template=template)
            st.session_state.cover_letter_widget = st.session_state.cover_letter

            # Step 3: Generate resume bullets
            status_text.text("🧠 Writing tailored resume bullet points...")
            progress_bar.progress(60)
            bullets = generate_resume_bullets(job_title, job_description, resume_text, openai_api_key, template=template)
            st.session_state.resume_bullets = "\n".join([f"- {bullet}" for bullet in bullets])

            # Step 4: Generate full resume (if selected)
            if generate_full:
                status_text.text("📄 Creating polished full resume...")
                progress_bar.progress(80)
                st.session_state.full_resume_content = generate_full_resume(resume_text, job_title, job_description, openai_api_key, template=template)
                st.session_state.full_resume_widget = st.session_state.full_resume_content
                st.session_state.pdf_file = create_resume_pdf(st.session_state.full_resume_content, template=template)
            else:
                st.session_state.full_resume_content = None
                st.session_state.full_resume_widget = ""
                st.session_state.pdf_file = None

            # Step 5: Mark generation as complete
            st.session_state.generated = True
            st.session_state.template = template
            status_text.text("✅ Generation complete!")
            progress_bar.progress(100)

        except Exception as e:
            status_text.error(f"❌ Error: {str(e)}")
            st.markdown("Please check your inputs or try again. If the issue persists, ensure your API key is valid.")
            st.button("🔄 Retry", use_container_width=True)

# Display outputs if generated
if st.session_state.generated:
    # Tabs for different outputs
    tabs = st.tabs(["Cover Letter", "Resume Bullets", "Full Resume" if st.session_state.full_resume_content else None])

    # Cover Letter Tab
    with tabs[0]:
        st.subheader(" Tailored Cover Letter")
        # Use separate session state key for widget to avoid conflict
        cover_letter_value = st.text_area(
            "Cover Letter",
            value=st.session_state.cover_letter_widget,
            height=400,
            key="cover_letter"
        )
        # Sync user edits back to session state
        if cover_letter_value != st.session_state.cover_letter_widget:
            st.session_state.cover_letter_widget = cover_letter_value
            st.session_state.cover_letter = cover_letter_value  # Update generated content if desired
        # Download as TXT
        st.download_button(
            label="⬇️ Download as TXT",
            data=st.session_state.cover_letter,
            file_name=f"cover_letter_{st.session_state.template.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )
        # Download as DOCX
        doc = docx.Document()
        doc.add_paragraph(st.session_state.cover_letter)
        docx_buffer = BytesIO()
        doc.save(docx_buffer)
        docx_buffer.seek(0)
        st.download_button(
            label="⬇️ Download as DOCX",
            data=docx_buffer,
            file_name=f"cover_letter_{st.session_state.template.lower()}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    # Resume Bullets Tab
    with tabs[1]:
        st.subheader("📌 Recommended Resume Bullet Points")
        st.markdown(st.session_state.resume_bullets)
        st.download_button(
            label="⬇️ Download Bullets as TXT",
            data=st.session_state.resume_bullets,
            file_name=f"resume_bullets_{st.session_state.template.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Full Resume Tab (if generated)
    if st.session_state.full_resume_content:
        with tabs[2]:
            st.subheader("🧾 Enhanced Resume")
            # Use separate session state key for widget to avoid conflict
            full_resume_value = st.text_area(
                "Generated Resume",
                value=st.session_state.full_resume_widget,
                height=500,
                key="full_resume"
            )
            # Sync user edits back to session state
            if full_resume_value != st.session_state.full_resume_widget:
                st.session_state.full_resume_widget = full_resume_value
                st.session_state.full_resume_content = full_resume_value  # Update generated content if desired
                st.session_state.pdf_file = create_resume_pdf(st.session_state.full_resume_content, template=st.session_state.template)
            st.download_button(
                label="⬇️ Download Enhanced Resume (PDF)",
                data=st.session_state.pdf_file,
                file_name=f"enhanced_resume_{st.session_state.template.lower()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("Powered by **xAI** | Built with **Streamlit** | © 2025")

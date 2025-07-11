
from openai import OpenAI

def call_gpt(prompt, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700
    )
    return response.choices[0].message.content.strip()


def generate_cover_letter(job_title, job_description, resume_text, api_key, template="Professional"):
    prompt = f"""
You are a professional career assistant. Generate a {template.lower()}-style personalized cover letter tailored to the following job and resume details:

Job Title: {job_title}
Job Description: {job_description}

Resume:
{resume_text}

The cover letter should:
- Be professional and concise
- Highlight relevant skills from the resume
- Be addressed generically (no company name required)
- Be suitable for copy-pasting into a job portal
"""
    return call_gpt(prompt, api_key)


def generate_resume_bullets(job_title, job_description, resume_text, api_key, template="Professional"):
    prompt = f"""
You are an expert resume editor. Based on the resume and the following job, suggest 5 {template.lower()}-style bullet points to include in the resume that best match the role.

Job Title: {job_title}
Job Description: {job_description}

Resume:
{resume_text}

Return only 5 strong bullet points in plain text format.
"""
    response = call_gpt(prompt, api_key)
    bullets = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]
    return bullets

def generate_full_resume(resume_text, job_title, job_description, api_key, template="Professional"):
    prompt = f"""
You're a professional resume creator. Generate a full resume in {template.lower()} style using the following resume content and tailored to this job:

Job Title: {job_title}
Job Description: {job_description}

Resume Content:
{resume_text}

Ensure the format includes:
- A professional summary
- Skills
- Experience
- Education

Return as clean plain text.
"""
    return call_gpt(prompt, api_key)

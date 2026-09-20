from google import genai
from ai.prompts import work_report_prompt, daily_summary_prompt, weekly_summary_prompt

client = genai.Client()

def generate_work_report(raw_text):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""{work_report_prompt} Raw note = {raw_text}""")
        return {'success':True,
                'report': response.text,
                'error':None}
    except Exception as e:
        return {'success':False,
                'report': None,
                'error':str(e)}

def generate_daily_summary(raw_text):
    try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"""{daily_summary_prompt} Raw note = {raw_text}""")
            return {'success':True,
                    'summary': response.text,
                    'error':None}
    except Exception as e:
        return {'success':False,
                'summary': None,
                'error':str(e)}

def generate_weekly_summary(raw_text):
    try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"""{weekly_summary_prompt} Raw note = {raw_text}""")
            return {'success':True,
                    'summary': response.text,
                    'error':None}
    except Exception as e:
        return {'success':False,
                'summary': None,
                'error':str(e)}


from configparser import ConfigParser

import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict
from groq import Groq
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

from ai_analysis.analyzer import TestAnalyzer
from ai_analysis.groqsetuptest import ChatGroq

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def _initialize_model(self):
    """Initialize the LLM based on configuration."""
    model_config = {
        "ollama": {
            "class": OllamaLLM,
            "params": {"model": self.config.get('AI', 'OLLAMA_MODEL', fallback="llama3")}
        },
        "openai": {
            "class": ChatOpenAI,
            "params": {
                "model": self.config.get('AI', 'OPENAI_MODEL', fallback="gpt-4-turbo"),
                "temperature": 0.3,
                "api_key": os.getenv("OPENAI_API_KEY")
            }
        },
        "gemini": {
            "class": ChatGoogleGenerativeAI,
            "params": {
                "model": self.config.get('AI', 'GEMINI_MODEL', fallback="gemini-pro"),
                "temperature": 0.5,
                "google_api_key": os.getenv("GOOGLE_API_KEY")
            }
        },
        "groq": {
            "class": ChatGroq,
            "params": {
                "model": self.config.get('AI', 'GROQ_MODEL', fallback="llama3-70b-8192"),
                "temperature": 0.5,
                "api_key": os.getenv("GROQ_API_KEY")
            }
        }
    }





def load_test_logs() -> List[Dict]:
    """Load and validate test logs with error handling"""
    try:
        with open('reports/logs/test_logs.json') as f:
            return [json.loads(line) for line in f]
    except Exception as e:
        st.error(f"Error loading logs: {str(e)}")
        return []

def parse_ai_response(response: str) -> Dict:
    """Safely parse AI response with multiple fallback strategies"""
    try:
        json_str = re.search(r'```(?:json)?\n({.*?})\n```', response, re.DOTALL).group(1)
        return json.loads(json_str)
    except (AttributeError, json.JSONDecodeError):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response"}


# In your analyze_test_failure function
def analyze_test_failure(test_name: str, error_details: str) -> Dict:
    """Get AI analysis for specific test failure"""
    try:
        # Initialize Groq client with API key from secrets
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
            #api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
        )

        if not client.api_key:
            raise ValueError("Groq API key not found in secrets or environment variables")

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"""Analyze this test failure:
                - Test Name: {test_name}
                - Error: {error_details}

                Respond in JSON format:
                {{
                    "root_cause": string,
                    "recommendations": [string],
                    "confidence_score": 0-100
                }}"""
            }],
            model="llama3-70b-8192",
            temperature=0.3,
            max_tokens=1024
        )

        return parse_ai_response(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def main():
    st.set_page_config(
        page_title="Test Analytics Dashboard",
        layout="wide",
        page_icon="📊"
    )
    st.title("🔍 AI-Powered Test Analysis Portal")

    # Load data
    logs = load_test_logs()
    if not logs:
        st.warning("No test logs found. Run tests first!")
        return

    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Ensure testname is used instead of test_id
    if 'testname' in df.columns:
        df.rename(columns={"test_id": "testname"}, inplace=True)

    # Date Selection Section
    st.sidebar.header("🕰 Date & Time Filter")

    # Default to last 7 days
    default_end = datetime.today()
    default_start = default_end - timedelta(days=7)

    start_date = st.sidebar.date_input("Start Date", value=default_start.date())
    end_date = st.sidebar.date_input("End Date", value=datetime.today().date())

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    # Filter dataframe
    time_mask = (df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)
    filtered_df = df[time_mask].copy()
    filtered_df['date'] = filtered_df['timestamp'].dt.date

    # Show date range info
    st.sidebar.markdown(f"""
    **Selected Range:**  
    {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}  
    ({len(filtered_df)} test executions)
    """)

    # Section 1: Test Case History Table
    st.header("📋 Test Case History")

    if filtered_df.empty:
        st.warning("No test executions found in selected date range")
        return

    history_df = filtered_df.groupby(['testname', 'status']).agg({
        'timestamp': ['min', 'max', 'count'],
        'error': 'last'
    }).reset_index()

    st.dataframe(
        history_df,
        use_container_width=True,
        height=400
    )

    # Section 2: Detailed Failure Analysis
    st.header("🛑 Failure Analysis")

    failed_tests = filtered_df[filtered_df['status'] == 'FAIL']['testname'].unique()

    if len(failed_tests) == 0:
        st.success("🎉 No failed tests in selected period!")
        return

    selected_test = st.selectbox("Select Failed Test Case", failed_tests)

    if selected_test:
        test_data = filtered_df[filtered_df['testname'] == selected_test].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Test Details")
            st.markdown(f"""
            - **Test Name**: {test_data.get('testname', 'N/A')}
            - **Last Run**: {test_data['timestamp'].strftime('%Y-%m-%d %H:%M')}
            - **Status**: {test_data['status']}
            - **Error**: `{test_data.get('error', 'No error details')}`
            """)

        with col2:
            st.subheader("AI Analysis")

            if st.button("Run Analysis", key="analyze_btn"):
                with st.spinner("Analyzing with Groq AI..."):
                    analysis = analyze_test_failure(
                        test_data['testname'],
                        test_data.get('error', '')
                    )

                    if 'error' in analysis:
                        st.error(f"Analysis Error: {analysis['error']}")
                    else:
                        st.markdown("### Root Cause")
                        st.info(analysis.get('root_cause', 'No analysis available'))

                        st.markdown("### Recommendations")
                        for rec in analysis.get('recommendations', []):
                            st.success(f"- {rec}")

                        st.metric("Confidence Score", f"{analysis.get('confidence_score', 0)}%")

    # Section 3: Historical Trends
    st.header("📈 Historical Trends")

    try:
        trend_data = filtered_df.groupby(['date', 'status']).size().unstack().fillna(0)
        st.line_chart(trend_data)
    except Exception as e:
        st.error(f"Couldn't generate trends: {str(e)}")

if __name__ == "__main__":
    main()

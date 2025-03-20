# ai_analysis/analyzer.py
import json
import logging
import re
from typing import Dict, List, Optional

from groq import Groq
from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_core.tracers import ConsoleCallbackHandler
from langchain_ollama import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from configparser import ConfigParser
import os
from dotenv import load_dotenv
import os

from ai_analysis.groqsetuptest import ChatGroq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()  # Load variables from .env


class TestAnalyzer:
    """AI-powered test log analysis engine with multi-model support."""

    def __init__(self, model_type: str = "groq"):
        """
        Initialize the AI analyzer with specified model type.

        Args:
            model_type (str): One of "ollama", "openai", "gemini" or "groq"
        """
        self.config = ConfigParser()
        self.config.read('config/config.ini')
        self.model_type = model_type.lower()
        self.llm = self._initialize_model()
        self.prompt_templates = self._load_prompt_templates()

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

        if self.model_type not in model_config:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        return model_config[self.model_type]["class"](**model_config[self.model_type]["params"])

    def _load_prompt_templates(self) -> Dict[str, PromptTemplate]:
        """Load prompt templates from directory."""
        return {
            "root_cause": PromptTemplate(
                input_variables=["logs"],
                template="""Analyze these test failures and identify root causes:
                {logs}

                Format response as JSON with:
                - "root_causes": list of potential issues
                - "confidence_score": 0-100
                - "related_components": list of affected modules"""
            ),
            "flakiness": PromptTemplate(
                input_variables=["historical_data"],
                template="""Calculate test flakiness score based on:
                {historical_data}

                Output JSON with:
                - "flakiness_score": 0-100
                - "failure_patterns": list of patterns
                - "stability_tips": list of recommendations"""
            )
        }

    def analyze_logs(self, log_path: str, analysis_type: str = "root_cause") -> Dict:
        """
        Analyze test logs using AI models.

        Args:
            log_path: Path to JSON log file
            analysis_type: Type of analysis ("root_cause" or "flakiness")

        Returns:
            Analysis results as dictionary
        """
        try:
            with open(log_path) as f:
                logs = [json.loads(line) for line in f]

            if analysis_type == "root_cause":
                return self._analyze_root_cause(logs)
            elif analysis_type == "flakiness":
                return self._analyze_flakiness(logs)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            print(e.args)
            return {"error": str(e)}

    def _analyze_root_cause(self, logs: List[Dict]) -> Dict:
        """Perform root cause analysis on test failures."""
        chain = self.prompt_templates["root_cause"] | self.llm
        # Create a callback handler to output verbose logs to the console.
        callback_handler = ConsoleCallbackHandler()
        # Pass the verbose flag and callbacks via the config
        response = chain.invoke({"logs": logs}, config={"callbacks": [callback_handler], "verbose": True})
        return self._parse_json_response(response)

    def _analyze_flakiness(self, logs: List[Dict]) -> Dict:
        """Calculate test flakiness score and patterns."""
        historical_data = self._aggregate_historical_data(logs)
        chain = self.prompt_templates["flakiness"] | self.llm
        response = chain.invoke({"historical_data": historical_data})
        return self._parse_json_response(response)

    import re

    def _parse_json_response(self, response: str) -> Dict:
        """Parse LLM JSON response with error handling."""
        try:
            # Use regex to find JSON block between ``` markers
            json_match = re.search(r'```(?:json)?\n({.*?})\n```', response, re.DOTALL)

            if not json_match:
                # Fallback: Try to find JSON without backticks
                json_match = re.search(r'({.*})', response, re.DOTALL)
                if not json_match:
                    return {}

            json_str = json_match.group(1)

            # Clean common formatting issues
            json_str = json_str.strip()
            json_str = re.sub(r',\s*}', '}', json_str)  # Fix trailing commas
            json_str = re.sub(r',\s*]', ']', json_str)  # Fix trailing commas in arrays
            json_str = json_str.replace(" metadata]", ' "metadata"]')  # Fix improperly formatted list
            return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing JSON: {str(e)}")
            return {"raw_response": response}

    def _aggregate_historical_data(self, logs: List[Dict]) -> Dict:
        """Aggregate log data for historical analysis."""
        return {
            "total_runs": len(logs),
            "failure_count": sum(1 for log in logs if log["status"] == "FAIL"),
            "common_errors": self._count_errors(logs)
        }

    def _count_errors(self, logs: List[Dict]) -> Dict[str, int]:
        """Count error frequencies in logs."""
        errors = {}
        for log in logs:
            if error := log.get("error"):
                errors[error] = errors.get(error, 0) + 1
        return errors


# Example usage
if __name__ == "__main__":
    os.system("ollama pull llama3.1:latest")  # Ensure the model is pulled before execution
    analyzer = TestAnalyzer(model_type="groq")

    # Analyze test failures
    result = analyzer.analyze_logs(
        log_path="reports/logs/test_logs.json",
        analysis_type="root_cause"
    )

    print("Root Cause Analysis Results:")
    print(json.dumps(result, indent=2))

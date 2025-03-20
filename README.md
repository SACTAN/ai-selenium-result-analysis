# AI-Driven Selenium Test Analysis Solution (Python Version)

An end-to-end solution for intelligent test automation analysis using **Selenium**, **LLMs** (Groq/OpenAI/Gemini), and **Streamlit** visualization.

---

## 🔹 Key Features

- **AI-Powered Root Cause Analysis**  
  - Automatic failure diagnosis using LLMs (**Groq Llama3 / OpenAI GPT-4 / Gemini**)
- **Historical Trend Visualization**  
  - Interactive charts showing test stability over time
- **Multi-LLM Support**  
  - Switch between **Groq, OpenAI, and Gemini** providers
- **CI/CD Integration**  
  - Ready for **GitHub Actions / Jenkins** with AI reporting
- **Self-Healing Recommendations**  
  - AI-generated fixes for flaky tests
- **Structured Logging**  
  - JSON logs with test case metadata and screenshots

---

## 📌 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-selenium-analytics.git
cd ai-selenium-analytics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### API Keys (Create `.streamlit/secrets.toml`):

```toml
[secrets]
GROQ_API_KEY = "your_groq_key"
OPENAI_API_KEY = "your_openai_key"  # Optional
GOOGLE_API_KEY = "your_gemini_key"  # Optional
```

### Configurations (`config.ini`):

```ini
[AI]
provider = groq  # groq / openai / gemini
model = llama3-70b-8192

[Paths]
screenshots = reports/screenshots
logs = reports/logs
```

---

## 🚀 Usage

```bash
# Run tests with JSON logging
pytest tests/ --log-file=reports/logs/test_logs.json -v

# Launch analytics dashboard
streamlit run dashboard/app.py
```

---

## 📊 Features Demo

### **AI Analysis Portal**
### **Dashboard Preview**

#### **Test History Table**
✅ Filter by **date range (last 7 days)**  
✅ Sort by **status / failure rate**  
✅ Direct **error message inspection**  

#### **Root Cause Analysis**
✅ LLM-generated **failure diagnosis**  
✅ Confidence scoring **(0-100%)**  
✅ Actionable **repair recommendations**  

#### **Trend Visualization**
✅ **Daily pass/fail trends**

![image](https://github.com/user-attachments/assets/50766347-a26d-4ab4-895a-d2a31cc2cf7e)

![image](https://github.com/user-attachments/assets/0566fe72-8a97-49aa-8353-27d6877fdd25)

![image](https://github.com/user-attachments/assets/cd66b577-78e0-4e97-bc8c-a7d2b4e2d481)

---

## 📁 Project Structure

```
Directory structure:
└── ai-selenium-result-analysis/
    ├── README.md
    ├── Makefile
    ├── pytest.ini
    ├── requirements.txt
    ├── setup.py
    ├── ai_analysis/
    │   ├── __init__.py
    │   ├── analyzer.py
    │   ├── groqsetuptest.py
    │   ├── loganalysis.py
    │   ├── __pycache__/
    │   └── prompts/
    │       ├── recommendations.j2
    │       └── root_cause.j2
    ├── config/
    │   ├── config.ini
    │   ├── config.json
    │   └── logging_config.ini
    ├── dashboard/
    │   ├── __init__.py
    │   ├── app.py
    │   └── assets/
    ├── docs/
    │   ├── architecture.md
    │   └── setup.md
    ├── infrastructure/
    │   ├── docker-compose.yml
    │   └── selenium-grid/
    │       └── hub-config.yml
    ├── reports/
    │   ├── __init__.py
    │   ├── test-report.html
    │   ├── ai_reports/
    │   ├── assets/
    │   ├── logs/
    │   │   └── test_logs.json
    │   └── screenshots/
    ├── requirements/
    │   ├── ai.txt
    │   ├── base.txt
    │   └── dev.txt
    ├── tests_suite/
    │   ├── __init__.py
    │   ├── browser_factory.py
    │   ├── conftest.py
    │   ├── logger.py
    │   ├── report_generator.py
    │   ├── screenshot_utils.py
    │   ├── test_demo.py
    │   ├── test_login.py
    │   ├── __pycache__/
    │   ├── auth/
    │   │   └── __pycache__/
    │   ├── dashboard/
    │   │   ├── __init__.py
    │   │   ├── test_navigation.py
    │   │   ├── test_widgets.py
    │   │   └── __pycache__/
    │   ├── page_objects/
    │   │   ├── __init__.py
    │   │   ├── dashboard_page.py
    │   │   ├── login_page.py
    │   │   └── __pycache__/
    │   ├── reports/
    │   │   ├── __init__.py
    │   │   ├── test-report.html
    │   │   └── assets/
    │   └── utilities/
    │       ├── __init__.py
    │       ├── check_config.py
    │       └── __pycache__/
    └── .github/
        └── workflows/
            └── ai-analysis.yml

```

---

## 🔎 AI Analysis Process

### **1️⃣ Structured Logging**

JSON logs capture:
```json
{
  "test_case": "test_login_valid",
  "status": "FAIL",
  "error": "ElementNotVisibleException",
  "timestamp": "2024-03-20T12:34:56Z"
}
```

### **2️⃣ LLM Integration**
- Uses **LangChain** for multi-provider support
- Custom **prompt engineering** for test analysis
- Response validation with **Pydantic**

### **3️⃣ Dashboard Features**
✅ Real-time **analysis triggers**  
✅ **Historical comparison** of test runs  
✅ **Exportable reports (CSV)**  

---

## ❓ Troubleshooting

### **Common Issues:**

#### ❌ `ModuleNotFoundError: No module named 'ai_analysis'`
```bash
export PYTHONPATH="$PWD"  # Add project root to path
```

#### ❌ `GROQ_API_KEY not found`
```bash
# Verify secrets.toml exists in .streamlit/
echo $GROQ_API_KEY  # Check environment variables
```

#### ❌ `JSONDecodeError in analysis`
🔹 Ensure that test logs are correctly formatted.

---

## 📩 Contact
📧 **Email**: sachinbhute23nov@gmail.com  
📜 **Documentation**: NA

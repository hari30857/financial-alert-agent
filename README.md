# 🏦 Financial Alert Agent  
### A News-to-Action AI Agent powered by Gemini 2.5 + FastAPI + Streamlit  

---

## 📘 Overview
**Financial Alert Agent** is an AI-powered financial news analysis system that reads financial articles and automatically identifies:  
- Market sentiment (Bullish / Bearish / Neutral)  
- Primary financial risk (Regulatory, Credit, Liquidity, etc.)  
- Risk rationale and severity score (1–5)  
- Key entities like banks, people, or organizations involved  

It leverages **Google Gemini 2.5 Flash**, **FastAPI**, and **Streamlit** to deliver real-time financial risk insights.

---

## 🚀 Tech Stack
| Component | Technology Used |
|------------|------------------|
| LLM | Gemini 2.5 Flash (Google Generative AI) |
| Backend | FastAPI |
| Frontend | Streamlit |
| NLP | spaCy (for Named Entity Recognition) |
| Language | Python 3.10+ |
| Deployment | Local (Uvicorn) / Streamlit Cloud |

---

## 🧠 Core Features
✅ Extracts organizations, people, and locations using **spaCy**  
✅ Analyzes sentiment and market implications using **Gemini**  
✅ Detects **risk types** (Regulatory, Liquidity, Credit, etc.)  
✅ Generates **risk score (1–5)** with clear reasoning  
✅ Clean, interactive **Streamlit UI** for visualization  

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/hari30857/financial-alert-agent.git
cd financial-alert-agent
2️⃣ Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
Activate it:

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

3️⃣ Install Required Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Add Gemini API Key
Create a file named .env in the project root and add your API key:

ini
Copy code
GEMINI_API_KEY=your_google_api_key_here
💡 You can generate your key at: https://aistudio.google.com/apikey

🧠 Running the Project
▶️ Start the Backend (FastAPI)
bash
Copy code
uvicorn main:app --reload
This starts the API server at:
👉 http://127.0.0.1:8000

To verify it’s running:

json
Copy code
{"message": "✅ Financial Alert Agent backend is running with Gemini 2.5!"}
▶️ Start the Frontend (Streamlit)
Open a new terminal in the same folder and run:

bash
Copy code
streamlit run app.py
This opens the app in your browser:
👉 http://localhost:8501

📰 Example Input
“The Reserve Bank of India fined ICICI Bank ₹5 crore for non-compliance with liquidity coverage ratio norms.”

🧾 Example Output
Field	Result
Summary	RBI fined ICICI Bank ₹5 crore for failing to comply with LCR norms.
Sentiment	Bearish
Primary Risk Type	Regulatory
Risk Rationale	Penalty imposed for regulatory non-adherence.
Risk Score	2 / 5 (Low Risk)
Entities	RBI, ICICI Bank

🧩 Folder Structure
bash
Copy code
financial-alert-agent/
│
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI backend
├── requirements.txt       # Dependencies
├── .env                   # Gemini API key (not uploaded)
├── sample_news.json       # Example test data
├── test_gemini_generate.py
├── test_gemini_connection.py
└── README.md
💡 How It Works
User inputs a financial news article/headline.

FastAPI backend sends it to Gemini 2.5 Flash.

Gemini analyzes sentiment, risk, and rationale.

spaCy extracts organizations, people, and locations.

Streamlit visualizes everything beautifully for analysts.

🌐 Deployment
This app runs locally using:

bash
Copy code
uvicorn main:app --reload
streamlit run app.py
Optional: You can deploy the Streamlit app using Streamlit Cloud for online demos.

👨‍💻 Developer
👤 Boddhapu Hareendra
B.Tech – Computer Science (AI & ML)
KL University

🏁 Hackathon Info
This project was created for AgenThink Hackathon 2025.
It follows the official FastAPI + Streamlit architecture, uses Gemini 2.5 Flash,
and complies with all submission guidelines outlined in the AgenThink Official Rules.

🏷️ License
This project is for educational and hackathon demonstration purposes only.

⭐ If you found this useful, please give the repository a star on GitHub!

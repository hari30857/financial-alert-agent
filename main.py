from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import spacy
import os
import json
import re


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Financial News Risk Analyzer")


try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class AnalysisRequest(BaseModel):
    article_text: str


class AnalysisResponse(BaseModel):
    summary: str
    sentiment: str
    risk_type: str
    risk_rationale: str
    risk_score: int
    key_points: list[str]
    entities: dict[str, list[str]]


def extract_json_from_text(text: str) -> dict:
    """Safely extracts JSON-like content from Gemini responses."""
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            return json.loads(text)
    except Exception:
        raise ValueError("Gemini did not return valid JSON")


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_article(request: AnalysisRequest):
    article_text = request.article_text.strip()

    if not article_text:
        raise HTTPException(
            status_code=400, detail="Article text cannot be empty.")

   
    doc = nlp(article_text)
    entities = {"organizations": [], "persons": [], "locations": []}

    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "PERSON":
            entities["persons"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)

    
    for k in entities:
        entities[k] = list(set(entities[k]))

    
    prompt = f"""
    You are a financial analyst AI. Analyze this financial news article and return a JSON with these fields:
    {{
      "summary": "short 1–2 sentence summary of the key financial event",
      "sentiment": "Bearish / Bullish / Neutral",
      "risk_type": "Credit / Market / Liquidity / Operational / Regulatory / Reputational / None",
      "risk_rationale": "brief reason for the risk type chosen",
      "risk_score": 1-5,
      "key_points": ["point1", "point2", "point3"]
    }}

    Article:
    {article_text}
    """

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError("Empty response from Gemini API.")

        cleaned = extract_json_from_text(response.text)

        
        risk_score = cleaned.get("risk_score", 0)
        try:
            risk_score = int(float(risk_score))
        except:
            risk_score = 0

        
        return AnalysisResponse(
            summary=cleaned.get("summary", "N/A"),
            sentiment=cleaned.get("sentiment", "N/A"),
            risk_type=cleaned.get("risk_type", "N/A"),
            risk_rationale=cleaned.get("risk_rationale", "N/A"),
            risk_score=risk_score,
            key_points=cleaned.get("key_points", []),
            entities=entities
        )

    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        print("❌ Error in /analyze:", e)
        raise HTTPException(
            status_code=500, detail="Gemini response parsing failed.")


@app.get("/")
def root():
    return {"message": "✅ Financial Alert Agent backend is running with Gemini 2.5 Flash!"}

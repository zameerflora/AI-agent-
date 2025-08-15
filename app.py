import os
import json
import re
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import streamlit as st
import pandas as pd
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Visa Requirement Checker",
    page_icon="🛂",
    layout="wide"
)

# JSON-focused prompt template
PROMPT_TEMPLATE = """You are a visa requirement assistant. Based on the passport index data provided, return a structured JSON response about visa requirements.

Context from passport index data:
{context}

Question: {question}

Data interpretation:
- 3, VF, or visa-free: No visa required
- 2, VOA, or visa on arrival: Visa can be obtained on arrival  
- 1, VR, or visa required: Visa must be obtained in advance
- 0 or -1: No travel allowed or no data available

Return ONLY a valid JSON object in the following format:
{{
  "passport_country": "country holding the passport",
  "destination_country": "country being visited",
  "visa_requirement": "visa-free|visa-on-arrival|visa-required|no-data",
  "raw_code": "the numeric/text code from data",
  "description": "brief explanation",
  "confidence": "high|medium|low"
}}

JSON Response:"""

@st.cache_resource
def load_embeddings():
    """Load embeddings model with caching"""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def load_database():
    """Load ChromaDB with caching"""
    embeddings = load_embeddings()
    try:
        db = Chroma(persist_directory="Chroma_Free", embedding_function=embeddings)
        return db, "✅ Using ChromaDB with free embeddings"
    except:
        try:
            db = Chroma(persist_directory="Chroma", embedding_function=embeddings)
            return db, "⚠️ Using original ChromaDB"
        except Exception as e:
            return None, f"❌ Error loading ChromaDB: {e}"

@st.cache_data
def load_country_list():
    """Load available countries from CSV for dropdown"""
    try:
        df = pd.read_csv("passport-index-matrix.csv")
        passport_countries = df.iloc[:, 0].tolist()  # First column
        destination_countries = df.columns[1:].tolist()  # Remaining columns
        return passport_countries, destination_countries
    except:
        return [], []

def extract_json_from_response(response_text):
    """Extract JSON from LLM response"""
    try:
        return json.loads(response_text.strip())
    except:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
    
    return {
        "passport_country": "unknown",
        "destination_country": "unknown", 
        "visa_requirement": "error",
        "raw_code": "N/A",
        "description": response_text[:200] + "..." if len(response_text) > 200 else response_text,
        "confidence": "low"
    }

def parse_query_for_countries(query_text):
    """Extract countries from user query"""
    query_lower = query_text.lower()
    
    country_patterns = {
        r'(us|usa|united states|america|american)': 'United States',
        r'(uk|britain|england|british|united kingdom)': 'United Kingdom',
        r'(germany|german)': 'Germany',
        r'(japan|japanese)': 'Japan',
        r'(canada|canadian)': 'Canada',
        r'(india|indian)': 'India',
        r'(china|chinese)': 'China',
        r'(france|french)': 'France',
        r'(australia|australian)': 'Australia',
        r'(brazil|brazilian)': 'Brazil',
    }
    
    found_countries = []
    for pattern, country in country_patterns.items():
        if re.search(pattern, query_lower):
            found_countries.append(country)
    
    return found_countries

def check_visa_requirement(query_text, model_name="llama3.2"):
    """Check visa requirements and return JSON response"""
    db, db_status = load_database()
    
    if db is None:
        return {
            "error": "Database not available",
            "passport_country": "unknown",
            "destination_country": "unknown",
            "visa_requirement": "error"
        }
    
    # Search for relevant visa information
    results = db.similarity_search_with_score(query_text, k=5)
    
    if len(results) == 0:
        return {
            "passport_country": "unknown",
            "destination_country": "unknown",
            "visa_requirement": "no-data",
            "description": "No matching data found in database"
        }
    
    # Format context from search results
    context_text = "\n\n".join([doc.page_content for doc, score in results])
    
    # Create prompt
    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    formatted_prompt = prompt.format(context=context_text, question=query_text)
    
    try:
        llm = Ollama(model=model_name, temperature=0, num_predict=300)
        response = llm.invoke(formatted_prompt)
        
        # Extract JSON
        json_response = extract_json_from_response(response)
        
        # Enhance with query analysis
        if json_response.get("passport_country") == "unknown":
            countries = parse_query_for_countries(query_text)
            if len(countries) >= 2:
                json_response["passport_country"] = countries[0]
                json_response["destination_country"] = countries[1]
        
        return json_response
        
    except Exception as e:
        return {
            "error": f"Ollama error: {str(e)}",
            "passport_country": "unknown",
            "destination_country": "unknown",
            "visa_requirement": "error"
        }

def display_visa_result(result):
    """Display visa result with styling"""
    if "error" in result:
        st.error(f"❌ Error: {result['error']}")
        return
    
    passport = result.get("passport_country", "Unknown")
    destination = result.get("destination_country", "Unknown")
    requirement = result.get("visa_requirement", "unknown")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("🛂 Passport Country", passport)
    
    with col2:
        st.metric("🌍 Destination", destination)
    
    with col3:
        # Style based on visa requirement
        if requirement == "visa-free":
            st.success("✅ VISA-FREE")
        elif requirement == "visa-on-arrival":
            st.warning("🟡 VISA ON ARRIVAL")
        elif requirement == "visa-required":
            st.error("❌ VISA REQUIRED")
        else:
            st.info(f"❓ {requirement.upper()}")
    
    # Additional details
    if "description" in result:
        st.info(f"📝 Details: {result['description']}")
    
    if "raw_code" in result:
        st.caption(f"📊 Raw Code: {result['raw_code']}")
    
    if "confidence" in result:
        confidence = result["confidence"]
        emoji = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else "🔴"
        st.caption(f"{emoji} Confidence: {confidence}")

# Streamlit App
def main():
    # Header
    st.title("🛂 AI-Powered Visa Requirement Checker")
    st.markdown("""
    💡 **Check visa requirements instantly!**  
    Enter your travel details below, and our AI will provide visa requirements including:
    - Visa-free travel ✅   
    - Visa on arrival 🟡   
    - Visa required ❌   
    - Processing requirements 📋
    """)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        model_name = st.selectbox(
            "🤖 Ollama Model",
            ["llama3.2", "llama3.2:1b", "phi3:mini", "gemma2:2b"],
            index=0
        )
        
        st.info("💡 Faster models: llama3.2:1b, phi3:mini")
        
        # Database status
        db, db_status = load_database()
        st.caption(db_status)
    
    # Main interface options
    tab1, tab2 = st.tabs(["🔍 Natural Language Query", "📋 Dropdown Selection"])
    
    with tab1:
        st.subheader("Ask in Natural Language")
        
        # Text input for natural language queries
        query = st.text_input(
            "💬 Enter your visa question",
            placeholder="Do US citizens need visa for Germany?",
            help="Examples: 'Can UK passport holders visit Japan?' or 'India to Canada visa requirements'"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            check_button = st.button("🚀 Check Visa Requirements", type="primary")
        
        if check_button and query:
            with st.spinner("⏳ AI is checking visa requirements... Please wait."):
                result = check_visa_requirement(query, model_name)
                
                st.subheader("✅ Visa Requirement Result")
                display_visa_result(result)
                
                # Download options
                col1, col2 = st.columns([1, 1])
                with col1:
                    # JSON download
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name=f"visa_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Text summary download
                    summary = f"""Visa Requirement Summary
                    
Passport Country: {result.get('passport_country', 'Unknown')}
Destination: {result.get('destination_country', 'Unknown')}
Visa Status: {result.get('visa_requirement', 'Unknown')}
Description: {result.get('description', 'No description')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    st.download_button(
                        label="📄 Download Summary",
                        data=summary,
                        file_name=f"visa_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                # Show raw JSON
                with st.expander("📋 View Raw JSON"):
                    st.json(result)
    
    with tab2:
        st.subheader("Select Countries from Dropdown")
        
        # Load country lists
        passport_countries, destination_countries = load_country_list()
        
        if passport_countries and destination_countries:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                passport_country = st.selectbox(
                    "🛂 Passport Country",
                    [""] + passport_countries,
                    help="Select your passport/citizenship country"
                )
            
            with col2:
                destination_country = st.selectbox(
                    "🌍 Destination Country", 
                    [""] + destination_countries,
                    help="Select country you want to visit"
                )
            
            if passport_country and destination_country:
                query_formatted = f"Do {passport_country} citizens need visa for {destination_country}?"
                
                if st.button("🔍 Check Requirements", type="primary"):
                    with st.spinner("⏳ Checking visa requirements..."):
                        result = check_visa_requirement(query_formatted, model_name)
                        
                        st.subheader("✅ Visa Requirement Result")
                        display_visa_result(result)
                        
                        # Download option
                        json_str = json.dumps(result, indent=2)
                        st.download_button(
                            label="📥 Download Result",
                            data=json_str,
                            file_name=f"visa_{passport_country}_to_{destination_country}.json",
                            mime="application/json"
                        )
        else:
            st.warning("⚠️ Could not load country data. Make sure 'passport-index-matrix.csv' exists.")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit, LangChain, and Ollama")

if __name__ == "__main__":
    main()
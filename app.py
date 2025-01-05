import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import PyPDF2 as pdf
import os
from dotenv import load_dotenv

# Set page config first
st.set_page_config(
    page_title="GreenTech Finance Analyzer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_response(pdf_content):
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )

    prompt = PromptTemplate.from_template(
        """
        You are a Green Finance expert tasked with analyzing and evaluating multiple project reports for green finance investments. 
        The goal is to evaluate, prioritize, and allocate resources to projects that have the highest Environmental, Social, and Governance (ESG) impact while predicting future risks using the content from the uploaded project report.

        The Content of the report:
        {pdf_content}

        The output structure should be like: 
        (Strictly don’t deviate from the given output structure)

        1. Project Information: (Use Proper tables to display data)
        - Project Name
        - Location
        - Expected Carbon Savings
        - Budget Allocation
        - ROI (Return on Investment)

        2. ESG Scores: (Use tables to display data)
        - Environmental Score (E): Extract information related to the environmental impact of the project, including carbon savings, renewable energy generation, resource conservation, etc.
                                    Carbon Savings,Renewable Energy Generation,Resource Conservation,Biodiversity Impact
        - Social Score (S): Extract details about the social impact, such as job creation, community benefits, stakeholder engagement, etc.
                              Job Creation,Community Development,Stakeholder Engagement,Access to Services  
        - Governance Score (G): Extract information about the governance structure, policies, ethical standards, and compliance with regulations.
                                  Regulatory Compliance,Ethical Standards,Corporate Governance

        3. Overall ESG Score: (Use tables to display data)
        - Calculate the Overall ESG Score for each project by averaging the Environmental, Social, and Governance scores.
        - Overall ESG Score = (Environmental Score + Social Score + Governance Score) / 3
        - Provide this score as a metric for overall sustainability evaluation.

        4. Risk Assessment: 
        For each project, identify the following risks:
        - Environmental Risks: Potential environmental risks such as climate-related impacts (e.g., droughts, storms).
        - Financial Risks: Assess financial risks like cost overruns, ROI predictions, and budget constraints.
        - Operational Risks: Operational challenges, such as construction delays, resource shortages, or regulatory hurdles.

        5. Optimization Recommendations: 
        Based on the extracted ESG scores, overall ESG score, and risk assessments, provide recommendations for allocating resources. Consider the following factors:
        - Maximizing ESG impact: Prioritize projects with high ESG impact (Environmental, Social, Governance).
        - Minimizing risks: Avoid projects with high financial or operational risks.
        - Budget Constraints: If a budget is provided, ensure that resource allocation stays within the total available budget.

        6. Conclusion:
        - Provide an overall summary and recommendations on the best investment strategy to maximize ESG impact.
        Score projects based on their sustainability impact Optimize resource allocation across
multiple projects to maximize ESG outcomes while staying within budget constraints.
2. Predict future risks associated with green investments
        3. Evaluate, prioritize, and optimizes green finance
        investments, helping banks and financial institutions allocate capital to the most impactful and
        sustainable projects.

        7. Final Suggestion
        As an expert give a suggestion whether this project has a good ESG Score and can other organizations provide fund for this project.


        """
    )

    chain = prompt | llm
    res = chain.invoke(input={"pdf_content": pdf_content})
    return res.content

def extract_text(file):
    try:
        reader = pdf.PdfReader(file)
        pages = len(reader.pages)
        text = ""
        for page_num in range(pages):
            page = reader.pages[page_num]
            text += str(page.extract_text())
        return text

    except Exception as e:
        st.error(f"Error occurred while extracting text: {str(e)}")


# Custom styling for better text visibility
st.markdown("""
    <style>
    /* Base text colors for dark mode */
    body {
        color: white !important;
        background-color: #0E1117;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #262730;
    }
    
    /* Card styling */
    .custom-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    /* Text colors */
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-weight: 600;
    }
    
    p, li {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #4CAF50;
        border-radius: 5px;
        padding: 20px;
        color: white;
    }
    
    /* Metrics */
    .metric-label {
        color: white !important;
    }
    
    .metric-value {
        color: #4CAF50 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

load_dotenv()

def main():
    # Header with proper visibility
    st.markdown("<h1 style='color: #4CAF50; text-align: center;'>🌱 GreenTech Finance Optimizer</h1>", unsafe_allow_html=True)
    
    # Sidebar with improved visibility
    with st.sidebar:
        st.markdown("<h2 style='color: #4CAF50;'>Analysis Dashboard</h2>", unsafe_allow_html=True)
        
        # Key Metrics
        st.markdown("<h3 style='color: white;'>Key Metrics</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Projects Analyzed", value="0", delta="New")
        with col2:
            st.metric(label="Avg ESG Score", value="N/A")
        
        # Analysis Features
        st.markdown("<h3 style='color: white;'>Analysis Features</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div style='color: white;'>
            • 📊 ESG Score Calculation<br>
            • 🔍 Risk Assessment<br>
            • 💡 Investment Recommendations<br>
            • 📈 Sustainability Metrics
            </div>
        """, unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class='custom-card'>
                <h2 style='color: #4CAF50;'>Upload Project Report</h2>
                <p style='color: white;'>Submit your ESG project report (PDF format) for comprehensive analysis</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Drag and drop file here",
            type=["pdf"],
            help="Limit 200MB per file • PDF"
        )

    with col2:
        st.markdown("""
            <div class='custom-card'>
                <h3 style='color: #4CAF50;'>Process Overview</h3>
                <ol style='color: white;'>
                    <li>Upload PDF report</li>
                    <li>AI analysis begins</li>
                    <li>Review detailed results</li>
                    <li>Export recommendations</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        with st.spinner("Processing report..."):
            pdf_content = extract_text(uploaded_file)

        if pdf_content:
            st.markdown("<div style='color: #4CAF50;'>✅ Report processed successfully!</div>", unsafe_allow_html=True)

            if st.button("🔍 Analyze Report"):
                with st.spinner("Performing AI analysis..."):
                    response = get_response(pdf_content)
                
                # Results in tabs with improved visibility
                tabs = st.tabs(["📊 Project Overview", "🎯 ESG Analysis", "⚠️ Risk Assessment", "💡 Recommendations"])
                
                with tabs[0]:
                    st.markdown("<h3 style='color: #4CAF50;'>Project Information</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: white;'>{response}</div>", unsafe_allow_html=True)

                with tabs[1]:
                    st.markdown("<h3 style='color: #4CAF50;'>ESG Analysis</h3>", unsafe_allow_html=True)

                with tabs[2]:
                    st.markdown("<h3 style='color: #4CAF50;'>Risk Assessment</h3>", unsafe_allow_html=True)

                with tabs[3]:
                    st.markdown("<h3 style='color: #4CAF50;'>Recommendations</h3>", unsafe_allow_html=True)

    else:
        st.info("👆 Upload a PDF report to begin analysis")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p style='color: #888;'>GreenTech Finance Optimizer | Powered by AI 🤖</p>
            <p style='color: #888;'>Making sustainable investments smarter</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# 📌 LLM-Based Ticket Reply Evaluation

## 📝 Overview
This project evaluates AI-generated responses to customer support tickets using **OpenAI's LLM API**. Each response is assessed based on:
1. **Content**: Relevance, correctness, and completeness.
2. **Format**: Clarity, structure, and grammar.

The evaluation process generates a **scored dataset** that can be used for AI response quality analysis.

---

## 📂 Project Structure
```
├── ticket_eval.py          # Main script for evaluation
├── tests.py                # Unit tests for key functions
├── tickets.csv             # Input dataset (customer tickets and AI replies)
├── tickets_evaluated.csv   # Output dataset with evaluations
├── requirements.txt        # Required dependencies
├── .env                    # API key configuration (excluded from Git)
└── README.md               # Documentation
```

---

## ⚙️ How It Works
1. **Reads** `tickets.csv`, which contains:
   - `ticket`: The customer's support message.
   - `reply`: The AI-generated response.
2. **Uses OpenAI's LLM** to evaluate each reply based on:
   - **Content Score (1-5)**: Measures relevance, correctness, and completeness.
   - **Format Score (1-5)**: Assesses clarity, structure, and grammar.
3. **Outputs** `tickets_evaluated.csv` with:
   - `content_score`
   - `content_explanation`
   - `format_score`
   - `format_explanation`

---

## 🚀 Setup & Usage

### 1️⃣ Install Dependencies
Ensure you have **Python 3.8+** and install dependencies:
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

### 3️⃣ Run the Evaluation Script
```bash
python ticket_eval.py
```

### 4️⃣ Output Example
The script generates `tickets_evaluated.csv` with scores:
```csv
ticket,reply,content_score,content_explanation,format_score,format_explanation
"Hi, I'd like to check my order status.","Your package arrives tomorrow.",4,"Relevant but lacks confirmation of order number.",5,"Clear and grammatically correct."
"The product I received is defective.","Send a photo for refund processing.",3,"Acknowledges issue but lacks refund details.",5,"Well-structured and concise."
```

---

## 🎡 Prompt Engineering
To ensure **accurate and structured LLM responses**, the script provides a **well-crafted prompt**:
```python
prompt = f"""
Analyze an AI-generated customer support reply based on two dimensions:

**Content (1-5 Score)**
- **Relevance**: Does it address the customer's issue?
- **Correctness**: Is the information accurate?
- **Completeness**: Does it provide all necessary details?

**Format (1-5 Score)**
- **Clarity**: Is it easy to understand?
- **Structure**: Is the information logically organized?
- **Grammar & Spelling**: Are there any mistakes?

Return a **JSON response**:
{{
  "content_score": X, 
  "content_explanation": "Brief explanation.",
  "format_score": Y,
  "format_explanation": "Brief explanation."
}}
"""
```
The **structured JSON response** ensures seamless parsing and CSV generation.

---

## 🛠️ Error Handling & Robustness
- **API Errors**: Handles quota limits, invalid responses, and missing keys.
- **Missing Data**: Skips incomplete rows and logs errors.
- **Rate Limiting**: Prevents excessive API calls with controlled execution.

---

## 🧪 Unit Testing
Unit tests ensure **code reliability** using `pytest`. The **tests cover**:
✔️ **Reading CSV input**  
✔️ **Calling OpenAI API**  
✔️ **Parsing JSON output**  
✔️ **Saving results correctly**  

### Run Tests:
```bash
pytest tests.py -v
```

Example **test case**:
```python
def test_csv_reading():
    df = read_csv("tickets.csv")
    assert isinstance(df, pd.DataFrame)
    assert "ticket" in df.columns and "reply" in df.columns
```

---

## 🌊 Evaluation Criteria & Best Practices

✔️ **Code Quality**: Follows **PEP-8**, modular functions, and clear structure.  
✔️ **Prompt Engineering**: **Detailed but concise prompts** for reliable AI responses.  
✔️ **Correctness of Output**: Ensures structured JSON parsing and valid score assignment.  
✔️ **Documentation & Tests**: Comprehensive README and **unit test coverage**.  

---

## 📌 Next Steps & Improvements
- **Automated Testing**: Expand test cases for edge scenarios.
- **Batch Processing**: Optimize API calls for large datasets.
- **UI Dashboard**: Implement a frontend for interactive evaluation.

---

## 🏆 Conclusion
This project **automates AI response evaluation**, ensuring high-quality customer interactions. It applies **prompt engineering, structured data processing, and automated testing** to deliver **scalable and maintainable results**.

✅ **Ready for deployment & further enhancements!** 🚀

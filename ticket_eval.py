import os
import openai
import pandas as pd
import json
import time
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OpenAI API Key not found. Please check your .env file.")

# Configure OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def clean_json_response(response_text):
    """
    Cleans OpenAI response to ensure valid JSON format.
    - Removes triple backticks (` ``` `)
    - Removes "json" label if present
    """
    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove "```json"
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove trailing triple backticks

    return response_text.strip()


def evaluate_reply(ticket, reply, retries=3):
    """
    Sends the ticket and AI reply to OpenAI LLM for evaluation.
    Implements retry logic for API errors.
    """

    if not ticket or not reply or pd.isna(ticket) or pd.isna(reply):
        print(f"⚠️ Skipping empty ticket/reply: {ticket[:50]}...")
        return None, "Missing data", None, "Missing data"

    prompt = f"""
    Analyze the AI-generated response to a customer support ticket and evaluate it based on two dimensions:

    **Customer Ticket:**
    "{ticket}"

    **AI Response:**
    "{reply}"

    **Evaluation Criteria:**

    **Content Evaluation (content_score)**: Score from 1 to 5 considering:
       - **Relevance**: Does it directly answer the customer’s question?
       - **Accuracy**: Is the information correct?
       - **Completeness**: Does it cover all necessary aspects?

    **Format Evaluation (format_score)**: Score from 1 to 5 considering:
       - **Clarity**: Is it easy to understand?
       - **Structure**: Is the information well-organized?
       - **Grammar and spelling**: Are there any mistakes?

    **Mandatory output format (JSON):**
    {{
      "content_score": X,  
      "content_explanation": "Brief explanation for content score.",
      "format_score": Y,  
      "format_explanation": "Brief explanation for format score."
    }}
    """

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in evaluating customer support responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200  # Prevent response truncation
            )

            # Print raw API response for debugging
            raw_response = response.choices[0].message.content.strip()
            print(f"\n🔹 OpenAI Raw Response:\n{raw_response}\n")

            # Clean response to ensure valid JSON format
            cleaned_response = clean_json_response(raw_response)

            # Parse response into JSON
            result = json.loads(cleaned_response)

            return result["content_score"], result["content_explanation"], result["format_score"], result[
                "format_explanation"]

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Error processing ticket: {ticket[:50]}... - {str(e)}")
            return None, "Evaluation error", None, "Evaluation error"

        except openai.OpenAIError as e:
            if "rate_limit" in str(e) or "insufficient_quota" in str(e):
                wait_time = (2 ** attempt)  # Exponential backoff (2s, 4s, 8s)
                print(f"⚠️ Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"⚠️ API Error processing ticket: {ticket[:50]}... - {str(e)}")
                return None, "API error", None, "API error"

        except Exception as e:
            print(f"⚠️ Unexpected Error processing ticket: {ticket[:50]}... - {str(e)}")
            return None, "Unexpected error", None, "Unexpected error"

    print(f"❌ Failed after {retries} attempts: {ticket[:50]}...")
    return None, "Max retries exceeded", None, "Max retries exceeded"


# 📌 Read input CSV file
input_file = "tickets.csv"
output_file = "tickets_evaluated.csv"

df = pd.read_csv(input_file)

# Add new columns for evaluations
df["content_score"] = None
df["content_explanation"] = None
df["format_score"] = None
df["format_explanation"] = None

# 📌 Process each ticket and evaluate the response
for index, row in df.iterrows():
    content_score, content_explanation, format_score, format_explanation = evaluate_reply(row["ticket"], row["reply"])

    df.at[index, "content_score"] = content_score
    df.at[index, "content_explanation"] = content_explanation
    df.at[index, "format_score"] = format_score
    df.at[index, "format_explanation"] = format_explanation

    time.sleep(1)  # Prevent exceeding API rate limits

# 📌 Save evaluated results
df.to_csv(output_file, index=False)

print(f"✅ Evaluation completed. File saved at {output_file}")

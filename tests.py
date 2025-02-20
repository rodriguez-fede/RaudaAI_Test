import os
import json
import pandas as pd
import pytest
from unittest.mock import patch
from ticket_eval import evaluate_reply, clean_json_response

# ✅ Sample test data
MOCK_TICKETS = [
    ("Hi, I'd like to check the shipping status of my order #1234.",
     "Sure, you can check your shipping status on our website. Your package is scheduled for delivery tomorrow."),

    ("The product I received is defective. I'd like a refund, please.",
     "We're sorry to hear that. Could you please provide a photo of the defect so we can proceed with the return process?"),

    ("Hello, my account was charged twice. Could you help me fix that?",
     "We've identified the issue and have requested a refund for the second charge. You should see the funds returned within 5-7 business days."),
]

MOCK_RESPONSE = json.dumps({
    "content_score": 4,
    "content_explanation": "The response is relevant and provides the correct information, but lacks an order confirmation.",
    "format_score": 5,
    "format_explanation": "The response is clear, well-structured, and free of grammatical and spelling errors."
})


# ✅ Test if the CSV loads correctly
def test_csv_loading():
    """Check if the input CSV loads correctly"""
    df = pd.DataFrame(MOCK_TICKETS, columns=["ticket", "reply"])
    assert len(df) == 3
    assert list(df.columns) == ["ticket", "reply"]


# ✅ Test cleaning OpenAI response JSON
def test_clean_json_response():
    """Ensure JSON cleaning works correctly"""
    raw_json = "```json\n" + MOCK_RESPONSE + "\n```"
    cleaned_json = clean_json_response(raw_json)
    assert cleaned_json == MOCK_RESPONSE


# ✅ Mock API calls to OpenAI
@patch("ticket_eval.client.chat.completions.create")
def test_evaluate_reply(mock_openai):
    """Mock OpenAI response and test evaluate_reply()"""

    # Mock OpenAI API response
    mock_openai.return_value.choices = [
        type("obj", (object,), {"message": type("msg", (object,), {"content": MOCK_RESPONSE})})]

    # Test function with a sample ticket
    content_score, content_explanation, format_score, format_explanation = evaluate_reply(
        MOCK_TICKETS[0][0], MOCK_TICKETS[0][1])

    assert content_score == 4
    assert format_score == 5
    assert "relevant" in content_explanation
    assert "clear" in format_explanation


# ✅ Test CSV writing
def test_csv_saving(tmp_path):
    """Test that results are correctly saved to CSV"""

    # Create dummy dataframe
    output_file = tmp_path / "test_output.csv"
    df = pd.DataFrame([
        ["Test Ticket", "Test Reply", 4, "Good content", 5, "Good format"]
    ], columns=["ticket", "reply", "content_score", "content_explanation", "format_score", "format_explanation"])

    df.to_csv(output_file, index=False)

    # Load the saved CSV and verify data
    loaded_df = pd.read_csv(output_file)
    assert loaded_df.shape == (1, 6)
    assert loaded_df["content_score"][0] == 4
    assert loaded_df["format_score"][0] == 5

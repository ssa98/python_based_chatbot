import os
import openai
from transformers import pipeline

#openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...your-key...")

# Load Hugging Face pipeline as fallback (distilbert for QA)
hf_qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def generate_answer(question, context_chunks):
    prompt = f"Context: {' '.join(context_chunks)}\n\nQuestion: {question}\nAnswer:"
    # Try OpenAI first
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided PDF context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback to Hugging Face QA
        try:
            context = ' '.join(context_chunks)
            result = hf_qa(question=question, context=context)
            return result['answer']
        except Exception as hf_e:
            print(f"Hugging Face QA error: {hf_e}")
            return f"Error: {e} | HF Error: {hf_e}"

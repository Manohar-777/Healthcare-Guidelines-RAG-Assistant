"""
LLM provider module - improved version with better validation
Supports Groq (default) and can be extended for local models
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, Any
import re

# Load environment variables
load_dotenv()

def get_llm():
    """
    Returns an LLM instance using the provider defined in .env.
    Default provider = Groq Llama 3.1 8B Instant.
    
    Returns:
        ChatGroq instance configured for answer generation
    """
    provider = os.getenv("LLM_PROVIDER", "groq")

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY missing in .env file. "
                "Get your key from https://console.groq.com/"
            )

        return ChatGroq(
            api_key=api_key,
            model="llama-3.1-8b-instant",
            temperature=0.1,  
            max_tokens=300    
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")


def generate_answer(question: str, passages: List[Dict[str, Any]]) -> str:
    """
    Generate answer using LLM based on retrieved passages.
    
    Args:
        question: User's question
        passages: List of retrieved passages with 'text', 'path', 'section'
        
    Returns:
        Generated answer string
    """
    if not passages:
        return "I don't have enough information in the provided guidelines to answer this question."
    
    # Get LLM instance
    llm = get_llm()
    
    # Prepare context from passages - use top 3 with full text
    context_parts = []
    for i, passage in enumerate(passages[:3], 1):
        context_parts.append(
            f"[Source {i}: {passage['section']}]\n"
            f"{passage['text']}"  # Full text
        )
    
    context = "\n\n".join(context_parts)
    
    # Clearer system prompt
    system_prompt = """You are a healthcare guidelines assistant. Answer questions using ONLY the exact information in the provided sources.

    CRITICAL RULES:
    1. Use ALL relevant facts from the sources
    2. If sources have specific examples or lists, include them
    3. Do NOT add examples that aren't in the sources
    4. Do NOT expand with general knowledge
    5. Be complete with what IS there, but don't invent what ISN'T there
    6. Keep answers factual and direct (2-4 sentences)
    7. If sources don't answer the question, say: "The provided guidelines do not contain specific information about [topic]."

    Format: Give the facts from the sources - nothing more, nothing less."""

    # Clearer user prompt
    user_prompt = f"""Guidelines:
                {context}

                Question: {question}

                Provide a complete answer using ALL relevant information from the guidelines above. Be thorough but concise."""

    # Generate response
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        answer = response.content.strip()
        
        # Remove citation patterns the LLM might add
        import re
        answer = re.sub(r'\(Source \d+[^\)]*\)', '', answer)
        answer = re.sub(r'\[Guideline \d+[^\]]*\]', '', answer)
        answer = re.sub(r'\(Guideline \d+[^\)]*\)', '', answer)
        
        # Clean up extra whitespace
        answer = re.sub(r'\s+', ' ', answer).strip()
        
        # Remove common preambles
        preambles = [
            "Based on the provided guideline excerpts, ",
            "Based on the provided guidelines, ",
            "According to the guidelines, ",
            "The guidelines state that ",
            "Based on the sources, "
        ]
        
        for preamble in preambles:
            if answer.startswith(preamble):
                answer = answer[len(preamble):]
                if answer:
                    answer = answer[0].upper() + answer[1:]
                break
        
        return answer
    
    except Exception as e:
        print(f"LLM generation error: {e}")
        return passages[0]["text"].split(".")[0].strip() + "."
    


def improved_coverage(answer: str, passages: List[Dict[str, Any]]) -> float:
    """
    Improved coverage metric that accounts for semantic content.
    
    Measures:
    1. Token overlap (basic)
    2. Phrase overlap (2-3 word phrases)
    3. Length penalty (very short answers get lower scores)
    """
    # Combine all source texts
    source_texts = [p["text"] for p in passages[:5]]
    source_text = " ".join(source_texts).lower()
    
    answer_lower = answer.lower()
    
    # 1. Token overlap
    ans_tokens = set(re.findall(r"\b[a-z]{3,}\b", answer_lower))  # 3+ char words
    src_tokens = set(re.findall(r"\b[a-z]{3,}\b", source_text))
    
    if not ans_tokens:
        return 0.0
    
    token_overlap = len(ans_tokens & src_tokens) / len(ans_tokens)
    
    # 2. Phrase overlap (bigrams)
    ans_words = re.findall(r"\b[a-z]+\b", answer_lower)
    src_words = re.findall(r"\b[a-z]+\b", source_text)
    
    if len(ans_words) >= 2:
        ans_bigrams = set(zip(ans_words, ans_words[1:]))
        src_bigrams = set(zip(src_words, src_words[1:]))
        phrase_overlap = len(ans_bigrams & src_bigrams) / len(ans_bigrams) if ans_bigrams else 0
    else:
        phrase_overlap = 0
    
    # 3. Length bonus (penalize very short answers)
    word_count = len(ans_words)
    if word_count < 5:
        length_penalty = 0.5
    elif word_count < 10:
        length_penalty = 0.8
    else:
        length_penalty = 1.0
    
    # Combine metrics
    # Weight: 60% token overlap, 30% phrase overlap, 10% length
    score = (0.6 * token_overlap + 0.3 * phrase_overlap) * length_penalty
    
    # Boost if answer contains key guideline terms
    guideline_terms = ["should", "must", "recommended", "required", "guidance", 
                       "protocol", "procedure", "according to", "per", "guideline"]
    term_boost = sum(1 for term in guideline_terms if term in answer_lower) * 0.02
    
    final_score = min(1.0, score + term_boost)
    
    return final_score


def generate_answer_with_validation(
    question: str, 
    passages: List[Dict[str, Any]],
    min_confidence: float = 0.25
) -> Dict[str, Any]:
    """
    Generate answer with improved validation and confidence scoring.
    
    Args:
        question: User's question
        passages: Retrieved passages
        min_confidence: Minimum confidence threshold
        
    Returns:
        Dict with answer, confidence, and validation status
    """
    # CHECK 1: If top passage has very low score, question is likely off-topic
    if passages and passages[0].get("score", 0) < 0.5:
        # Very low retrieval score = question not about healthcare guidelines
        return {
            "answer": "This question does not appear to be related to the healthcare guidelines in our database. Please ask about topics like hand hygiene, PPE, environmental cleaning, isolation protocols, vaccination programs, respiratory etiquette, or evidence hierarchy.",
            "confidence": 0.0,
            "status": "needs_review"
        }
    
    # Generate answer
    answer = generate_answer(question, passages)
    
    # CHECK 2: If LLM says it doesn't have information
    no_info_phrases = [
        "do not contain information",
        "don't contain information", 
        "no information",
        "not mentioned",
        "does not address",
        "doesn't address"
    ]
    
    if any(phrase in answer.lower() for phrase in no_info_phrases):
        return {
            "answer": answer,
            "confidence": 0.0,
            "status": "needs_review"
        }
    
    # Calculate improved confidence
    conf = improved_coverage(answer, passages)
    
    # CHECK 3: Boost confidence based on answer quality and retrieval score
    word_count = len(answer.split())
    top_score = passages[0].get("score", 0) if passages else 0
    
    # Quality boost
    if word_count >= 15 and conf >= 0.15:
        conf = min(1.0, conf + 0.20)
    
    # Retrieval score boost - if we retrieved highly relevant sources
    if top_score >= 0.8:
        conf = min(1.0, conf + 0.10)
    
    # CHECK 4: Penalize if retrieval scores are mediocre
    if top_score < 0.7:
        conf = max(0.0, conf - 0.15)
    
    # Determine status
    status = "validated" if conf >= min_confidence else "needs_review"
    
    return {
        "answer": answer,
        "confidence": round(conf, 3),
        "status": status
    }


# Test function
if __name__ == "__main__":
    print("Testing improved LLM provider...")
    
    try:
        llm = get_llm()
        print("✅ LLM initialized successfully")
        print(f"   Model: llama-3.1-8b-instant")
        print(f"   Provider: Groq")
        
        # Test with more realistic passage
        test_passages = [{
            "path": "who_hand_hygiene_2019.md",
            "section": "Recommendations",
            "text": "WHO guidance for hand hygiene. Key recommendations include: perform hand hygiene before patient contact, before aseptic procedures, after body fluid exposure risk, after touching patient, and after touching patient surroundings. Use alcohol-based handrub when hands not visibly soiled. Training and monitoring required.",
            "score": 0.85
        }, {
            "path": "cdc_hand_hygiene_2020.md",
            "section": "Implementation",
            "text": "CDC recommends implementing hand hygiene at five key moments: before patient contact, before clean/aseptic procedures, after body fluid exposure, after patient contact, after contact with patient environment. Monitor compliance quarterly.",
            "score": 0.82
        }]
        
        test_question = "When should hand hygiene be performed?"
        
        print("\nTest question:", test_question)
        print("\nGenerating answer...")
        
        result = generate_answer_with_validation(test_question, test_passages)
        
        print(f"\n✅ Answer generated:")
        print(f"   {result['answer']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Status: {result['status']}")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
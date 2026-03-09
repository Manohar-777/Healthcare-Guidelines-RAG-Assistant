"""
Create custom query set based on actual document content
Total: ~65 queries covering all topics with various difficulty levels
"""

import csv
from pathlib import Path

OUTPUT_DIR = Path("evaluation")
QUERIES_FILE = OUTPUT_DIR / "queries_custom.csv"

def create_queries():
    """Create comprehensive query set."""
    
    queries = []
    
    # ========================================================================
    # ENVIRONMENTAL CLEANING (12 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "What cleaning agents are recommended for routine environmental cleaning in healthcare settings?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "How often should high-touch surfaces be disinfected according to WHO guidelines?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "Why is respecting manufacturer contact times important during environmental cleaning?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "How should the cleaning frequency be adjusted for high-touch surfaces?",
            "expected": "environmental",
            "category": "complex",
            "topic": "environmental_cleaning"
        },
        {
            "question": "What is the rule regarding manufacturer contact times for disinfectants?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "Under what circumstances should deviations from cleaning protocols be documented?",
            "expected": "environmental",
            "category": "edge_case",
            "topic": "environmental_cleaning"
        },
        {
            "question": "Give examples of surfaces that require increased cleaning frequency in a patient room.",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "Does the WHO specify which types of disinfectants are 'approved' for routine cleaning?",
            "expected": "environmental",
            "category": "comparative",
            "topic": "environmental_cleaning"
        },
        {
            "question": "What are the principles of WHO environmental cleaning guidelines?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "How should staff be trained on environmental cleaning protocols?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "What monitoring is required for environmental cleaning adherence?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
        {
            "question": "What counts as high-touch surfaces for cleaning?",
            "expected": "environmental",
            "category": "simple",
            "topic": "environmental_cleaning"
        },
    ])
    
    # ========================================================================
    # HAND HYGIENE (9 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "In what specific clinical scenarios is hand hygiene mandatory according to WHO?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "Does WHO recommend hand hygiene before or after touching patient surroundings?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "How often should adherence to hand hygiene protocols be reviewed?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "Which guideline specifically mentions hand hygiene before aseptic procedures?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "What are the principles of CDC hand hygiene guidelines?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "When should hand hygiene be performed?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "How should staff be trained on hand hygiene protocols?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "What monitoring is required for hand hygiene adherence?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
        {
            "question": "What are the key principles of hand hygiene?",
            "expected": "hand",
            "category": "simple",
            "topic": "hand_hygiene"
        },
    ])
    
    # ========================================================================
    # PPE (10 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "When should a healthcare worker use a combination of gloves, gowns, and eye protection?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "What is the correct protocol for donning and doffing PPE safely?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "How does a clinician determine which PPE is necessary for a specific patient interaction?",
            "expected": "ppe",
            "category": "complex",
            "topic": "ppe"
        },
        {
            "question": "Does PPE selection require risk assessment?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "How should staff be trained on PPE protocols?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "What monitoring is needed for PPE adherence?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "What deviations from PPE protocols should be documented?",
            "expected": "ppe",
            "category": "edge_case",
            "topic": "ppe"
        },
        {
            "question": "What principles guide PPE use in WHO guidelines?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
        {
            "question": "Which situations require full PPE compared to minimal protection?",
            "expected": "ppe",
            "category": "complex",
            "topic": "ppe"
        },
        {
            "question": "How should PPE be selected for exposure risk?",
            "expected": "ppe",
            "category": "simple",
            "topic": "ppe"
        },
    ])
    
    # ========================================================================
    # RESPIRATORY ETIQUETTE & SEASONS (11 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "What are the primary recommendations for cough and sneeze etiquette in clinical settings?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "What triage and testing capacity changes are recommended during peak respiratory seasons?",
            "expected": "respiratory",
            "category": "complex",
            "topic": "respiratory"
        },
        {
            "question": "Is staff training a requirement for implementing respiratory etiquette policies?",
            "expected": "respiratory",
            "category": "edge_case",
            "topic": "respiratory"
        },
        {
            "question": "Who is responsible for issuing public health advisories during respiratory seasons?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "According to the 2024 CDC update, what is the current stance on masking in respiratory seasons?",
            "expected": "respiratory",
            "category": "comparative",
            "topic": "respiratory"
        },
        {
            "question": "When should mask use be encouraged?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "How should coughs and sneezes be covered?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "What distance measures are recommended for respiratory etiquette?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "What practices are included in respiratory etiquette during respiratory virus seasons?",
            "expected": "respiratory",
            "category": "simple",
            "topic": "respiratory"
        },
        {
            "question": "How do respiratory season guidelines differ from routine IPC procedures?",
            "expected": "respiratory",
            "category": "comparative",
            "topic": "respiratory"
        },
        {
            "question": "How should hospitals adjust staffing or operations during respiratory surges?",
            "expected": "respiratory",
            "category": "complex",
            "topic": "respiratory"
        },
    ])
    
    # ========================================================================
    # VACCINATION PROGRAMS (7 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "What is the requirement for recording vaccine doses in a CDC-compliant program?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
        {
            "question": "What are the essential steps to ensure cold chain integrity during vaccine storage?",
            "expected": "vaccination",
            "category": "complex",
            "topic": "vaccination"
        },
        {
            "question": "What is CDC guidance for vaccination programs?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
        {
            "question": "Which groups should be prioritized in vaccination programs?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
        {
            "question": "How is cold chain integrity ensured in vaccination?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
        {
            "question": "Why must high-risk groups be prioritized in vaccination programs?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
        {
            "question": "What steps are required for accurate dose recording?",
            "expected": "vaccination",
            "category": "simple",
            "topic": "vaccination"
        },
    ])
    
    # ========================================================================
    # ISOLATION & RETURN TO WORK (5 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "What strategies are recommended by the CDC for determining when staff can return to work?",
            "expected": "isolation",
            "category": "simple",
            "topic": "isolation"
        },
        {
            "question": "Can a staff member with respiratory symptoms continue working if they use a mask?",
            "expected": "isolation",
            "category": "edge_case",
            "topic": "isolation"
        },
        {
            "question": "When can symptomatic healthcare staff return to work?",
            "expected": "isolation",
            "category": "simple",
            "topic": "isolation"
        },
        {
            "question": "What is the difference between time-based and test-based return-to-work strategies?",
            "expected": "isolation",
            "category": "comparative",
            "topic": "isolation"
        },
        {
            "question": "What criteria must be met before symptomatic staff can resume duties?",
            "expected": "isolation",
            "category": "simple",
            "topic": "isolation"
        },
    ])
    
    # ========================================================================
    # EVIDENCE HIERARCHY & GRADING (11 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "Which types of studies are considered to provide the highest certainty in the evidence hierarchy?",
            "expected": "evidence",
            "category": "simple",
            "topic": "evidence"
        },
        {
            "question": "When is a clinical recommendation classified as 'strong' versus 'conditional'?",
            "expected": "grading",
            "category": "simple",
            "topic": "grading"
        },
        {
            "question": "If the balance of benefits and harms is uncertain, what type of recommendation is issued?",
            "expected": "grading",
            "category": "complex",
            "topic": "grading"
        },
        {
            "question": "What is the difference between an Evidence Hierarchy and a Grading system in NIH guidelines?",
            "expected": "evidence",
            "category": "comparative",
            "topic": "evidence"
        },
        {
            "question": "Why does expert opinion have lower certainty?",
            "expected": "evidence",
            "category": "simple",
            "topic": "evidence"
        },
        {
            "question": "What are the principles of NIH evidence hierarchy guidelines?",
            "expected": "evidence",
            "category": "simple",
            "topic": "evidence"
        },
        {
            "question": "How does expert opinion rank in the NIH evidence hierarchy?",
            "expected": "evidence",
            "category": "simple",
            "topic": "evidence"
        },
        {
            "question": "When should strong recommendations be issued according to NIH grading guidelines?",
            "expected": "grading",
            "category": "simple",
            "topic": "grading"
        },
        {
            "question": "What characterizes a conditional recommendation in clinical guidance?",
            "expected": "grading",
            "category": "simple",
            "topic": "grading"
        },
        {
            "question": "How should clinicians assess the balance of benefits and harms when grading recommendations?",
            "expected": "grading",
            "category": "complex",
            "topic": "grading"
        },
        {
            "question": "What is the hierarchy of clinical evidence?",
            "expected": "evidence",
            "category": "simple",
            "topic": "evidence"
        },
    ])
    
    # ========================================================================
    # SHARED DECISION MAKING (5 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "How should clinicians incorporate patient values into the decision-making process?",
            "expected": "shared",
            "category": "simple",
            "topic": "shared_decision"
        },
        {
            "question": "What steps ensure transparency when presenting risks and benefits to patients?",
            "expected": "shared",
            "category": "complex",
            "topic": "shared_decision"
        },
        {
            "question": "What defines the 'collaboration' aspect of shared decision-making according to the NIH?",
            "expected": "shared",
            "category": "simple",
            "topic": "shared_decision"
        },
        {
            "question": "How should clinicians present benefits and risks transparently?",
            "expected": "shared",
            "category": "simple",
            "topic": "shared_decision"
        },
        {
            "question": "Which core principles define shared decision-making guidelines?",
            "expected": "shared",
            "category": "simple",
            "topic": "shared_decision"
        },
    ])
    
    # ========================================================================
    # CROSS-CUTTING / GENERAL (5 queries)
    # ========================================================================
    queries.extend([
        {
            "question": "What are the four common implementation steps across all WHO and CDC guidelines?",
            "expected": "hand",  # Should retrieve any guideline
            "category": "comparative",
            "topic": "general"
        },
        {
            "question": "Compare the WHO and CDC approach to risk assessment in PPE and Hygiene.",
            "expected": "ppe",
            "category": "comparative",
            "topic": "comparison"
        },
        {
            "question": "How should clinicians evaluate the certainty of evidence before making recommendations?",
            "expected": "evidence",
            "category": "complex",
            "topic": "evidence"
        },
        {
            "question": "What role does vaccination promotion play during respiratory seasons?",
            "expected": "respiratory",
            "category": "complex",
            "topic": "respiratory_vaccination"
        },
        {
            "question": "How can clinicians document shared decision-making discussions?",
            "expected": "shared",
            "category": "simple",
            "topic": "shared_decision"
        },
    ])
    
    return queries

def save_queries(queries):
    """Save queries to CSV."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    with open(QUERIES_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['question', 'expected', 'category', 'topic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for query in queries:
            writer.writerow(query)
    
    print(f"✅ Saved {len(queries)} queries to {QUERIES_FILE}")

def print_summary(queries):
    """Print summary."""
    from collections import Counter
    
    print(f"\n{'='*60}")
    print("CUSTOM QUERY SET SUMMARY")
    print(f"{'='*60}\n")
    
    print(f"Total queries: {len(queries)}\n")
    
    categories = Counter(q['category'] for q in queries)
    print("By Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:20s} : {count:2d} queries")
    
    print()
    
    topics = Counter(q['expected'] for q in queries)
    print("By Expected Topic:")
    for topic, count in sorted(topics.items(), key=lambda x: -x[1]):
        print(f"  {topic:20s} : {count:2d} queries")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    print("Creating custom query set...")
    queries = create_queries()
    print_summary(queries)
    save_queries(queries)
    
    print("\nSample queries:")
    print("-" * 60)
    for i, q in enumerate(queries[:5], 1):
        print(f"{i}. [{q['category']}] {q['question']}")
        print(f"   Expected: {q['expected']}\n")
"""
Detailed corpus analysis to understand available topics
for test query generation
"""

from pathlib import Path
import re
from collections import Counter, defaultdict

CORPUS = Path("corpus/guidelines")

def analyze_corpus():
    """Analyze corpus to identify topics and structure."""
    
    docs = list(CORPUS.glob("*.md"))
    print(f"{'='*60}")
    print(f"CORPUS ANALYSIS")
    print(f"{'='*60}\n")
    
    print(f"Total documents: {len(docs)}\n")
    
    # Extract topics from filenames
    topics = []
    organizations = []
    years = []
    
    topic_docs = defaultdict(list)
    org_docs = defaultdict(list)
    
    for doc in docs:
        name = doc.stem
        parts = name.split("_")
        
        if len(parts) >= 2:
            org = parts[0].upper()  # WHO, CDC, NIH
            topic = parts[1]  # hand_hygiene, ppe, vaccination
            
            organizations.append(org)
            topics.append(topic)
            
            topic_docs[topic].append(doc.name)
            org_docs[org].append(doc.name)
            
            # Extract year if present
            year_match = re.search(r'(19|20)\d{2}', name)
            if year_match:
                years.append(year_match.group())
    
    # Topic distribution
    print("TOPIC DISTRIBUTION:")
    print("-" * 60)
    topic_counts = Counter(topics)
    for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {topic:30s} : {count:2d} documents")
        # Show sample document
        sample_docs = topic_docs[topic][:2]
        for sample in sample_docs:
            print(f"      └─ {sample}")
    
    print(f"\n{'='*60}\n")
    
    # Organization distribution
    print("ORGANIZATION DISTRIBUTION:")
    print("-" * 60)
    org_counts = Counter(organizations)
    for org, count in sorted(org_counts.items(), key=lambda x: -x[1]):
        print(f"  {org:10s} : {count:2d} documents")
    
    print(f"\n{'='*60}\n")
    
    # Year distribution
    print("YEAR DISTRIBUTION:")
    print("-" * 60)
    year_counts = Counter(years)
    for year, count in sorted(year_counts.items()):
        print(f"  {year} : {count:2d} documents")
    
    print(f"\n{'='*60}\n")
    
    # Sample document structure
    print("SAMPLE DOCUMENT STRUCTURE:")
    print("-" * 60)
    sample_doc = sorted(docs)[0]
    print(f"Document: {sample_doc.name}\n")
    
    text = sample_doc.read_text(encoding='utf-8')
    lines = text.split('\n')
    
    print("Sections found:")
    for line in lines:
        if line.startswith('#'):
            level = len(line.split()[0])
            section_name = line.lstrip('#').strip()
            print(f"  {'  ' * (level-1)}└─ {section_name}")
    
    print(f"\n{'='*60}\n")
    
    # Content preview
    print("SAMPLE CONTENT PREVIEW:")
    print("-" * 60)
    preview_docs = sorted(docs)[:3]
    for doc in preview_docs:
        text = doc.read_text(encoding='utf-8')
        # Get first 200 chars
        preview = ' '.join(text[:200].split())
        print(f"\n{doc.name}:")
        print(f"  {preview}...")
    
    print(f"\n{'='*60}\n")
    
    return {
        'topics': list(topic_counts.keys()),
        'organizations': list(org_counts.keys()),
        'total_docs': len(docs),
        'topic_docs': dict(topic_docs)
    }

if __name__ == "__main__":
    result = analyze_corpus()
    
    print("\nQUERY GENERATION RECOMMENDATIONS:")
    print("-" * 60)
    print(f"✅ Cover {len(result['topics'])} topics")
    print(f"✅ Include all {len(result['organizations'])} organizations")
    print(f"✅ Mix simple and complex queries")
    print(f"✅ Add edge cases and ambiguous questions")
    print(f"✅ Target: 30-60 total queries")
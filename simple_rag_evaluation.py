#!/usr/bin/env python3
"""
Simplified RAG Evaluation Test for Kodit MCP Server

This script provides a basic evaluation of the Kodit RAG system by:
1. Loading questions from grip_qa repository
2. Querying Kodit MCP server for responses
3. Performing basic similarity and relevance evaluation
4. Generating a simple evaluation report

Note: This is a simplified version that avoids complex dependencies
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

# Basic imports that should be available
try:
    import subprocess
    from difflib import SequenceMatcher
except ImportError as e:
    print(f"Missing basic Python modules: {e}")
    sys.exit(1)


@dataclass
class TestCase:
    """A single test case for RAG evaluation"""
    question: str
    expected_answer: str
    category: str
    difficulty: str


@dataclass 
class RAGResponse:
    """Response from the RAG system"""
    question: str
    answer: str
    contexts: List[str]
    retrieval_time: float
    success: bool


class SimpleKoditClient:
    """Simple client for interacting with Kodit via command line"""
    
    def __init__(self):
        self.kodit_available = self._check_kodit_available()
    
    def _check_kodit_available(self) -> bool:
        """Check if kodit command is available"""
        try:
            result = subprocess.run(['kodit', 'version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False
    
    async def search(self, question: str) -> Dict[str, Any]:
        """Search using Kodit via command line"""
        if not self.kodit_available:
            return {"error": "Kodit not available"}
        
        try:
            # Extract simple keywords from question
            keywords = self._extract_keywords(question)
            
            # Use kodit search command - try different search types
            result = None
            
            # Try keyword search first
            if keywords:
                cmd = ['kodit', 'search', 'keyword'] + keywords + ['--top-k', '3']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result and result.returncode == 0 and result.stdout.strip():
                return {"success": True, "output": result.stdout}
            else:
                return {"error": f"Search failed: {result.stderr if result else 'No result'}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extract simple keywords from question"""
        # Simple keyword extraction
        words = question.lower().split()
        keywords = []
        
        # Filter out common words and keep relevant terms
        stop_words = {'what', 'how', 'when', 'where', 'why', 'does', 'do', 'is', 'are', 
                     'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'can', 'i', 'you', 'we', 'they'}
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3 and clean_word not in stop_words:
                keywords.append(clean_word)
        
        return keywords[:5]  # Return top 5 keywords


class GripQALoader:
    """Loads test cases from grip_qa repository"""
    
    def __init__(self, grip_qa_path: str):
        self.grip_qa_path = Path(grip_qa_path)
        if not self.grip_qa_path.exists():
            raise FileNotFoundError(f"grip_qa repository not found at {grip_qa_path}")
    
    def load_test_cases(self) -> List[TestCase]:
        """Load test cases from grip_qa Q&A files"""
        test_cases = []
        
        # Find all question files
        question_files = sorted(self.grip_qa_path.glob("*.q.md"))
        
        for q_file in question_files:
            # Get corresponding answer file
            base_name = q_file.stem.replace('.q', '')
            a_file = self.grip_qa_path / f"{base_name}.a.md"
            
            if a_file.exists():
                try:
                    # Read question
                    with open(q_file, 'r', encoding='utf-8') as f:
                        question = f.read().strip()
                    
                    # Read answer
                    with open(a_file, 'r', encoding='utf-8') as f:
                        answer = f.read().strip()
                    
                    # Classify question
                    category, difficulty = self._classify_question(question)
                    
                    test_cases.append(TestCase(
                        question=question,
                        expected_answer=answer,
                        category=category,
                        difficulty=difficulty
                    ))
                    
                except Exception as e:
                    print(f"Warning: Could not read {q_file.name}: {e}")
                    continue
        
        print(f"✅ Loaded {len(test_cases)} test cases from grip_qa")
        return test_cases
    
    def _classify_question(self, question: str) -> tuple[str, str]:
        """Classify question into category and difficulty"""
        question_lower = question.lower()
        
        # Determine category
        if any(word in question_lower for word in ['command', 'run', 'start', 'use']):
            category = "usage"
        elif any(word in question_lower for word in ['function', 'method', 'class']):
            category = "function"
        elif any(word in question_lower for word in ['license', 'permission', 'distribute']):
            category = "legal"
        else:
            category = "general"
        
        # Determine difficulty based on question length
        word_count = len(question.split())
        if word_count < 10:
            difficulty = "easy"
        elif word_count < 20:
            difficulty = "medium"
        else:
            difficulty = "hard"
            
        return category, difficulty


class SimpleEvaluator:
    """Simple evaluation metrics without external dependencies"""
    
    def __init__(self):
        pass
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """Calculate basic similarity score between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def keyword_overlap(self, text1: str, text2: str) -> float:
        """Calculate keyword overlap between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def answer_quality_score(self, question: str, answer: str) -> float:
        """Simple answer quality assessment"""
        if not answer or answer == "Error: Unable to retrieve answer":
            return 0.0
        
        # Basic quality indicators
        score = 0.0
        
        # Length check (not too short, not too long)
        if 20 <= len(answer) <= 1000:
            score += 0.3
        
        # Contains question keywords
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        if question_words.intersection(answer_words):
            score += 0.3
        
        # Coherent sentences (contains periods)
        if '.' in answer:
            score += 0.2
        
        # Not just code (has some explanatory text)
        if any(word in answer.lower() for word in ['the', 'is', 'are', 'can', 'will', 'allows', 'provides']):
            score += 0.2
        
        return min(score, 1.0)


async def run_simple_evaluation():
    """Run the simplified RAG evaluation"""
    
    print("🚀 Starting Simple RAG Evaluation for Kodit MCP Server")
    print("=" * 60)
    
    # Configuration
    GRIP_QA_PATH = "/home/a.subramanian/github/grip_qa"
    OUTPUT_DIR = "simple_rag_results"
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    # Initialize components
    try:
        loader = GripQALoader(GRIP_QA_PATH)
        client = SimpleKoditClient()
        evaluator = SimpleEvaluator()
        
        if not client.kodit_available:
            print("❌ Kodit command not available. Please ensure kodit is installed and in PATH.")
            return
        
        # Load test cases
        print("\n📝 Loading test cases...")
        test_cases = loader.load_test_cases()
        
        if not test_cases:
            print("❌ No test cases loaded. Check grip_qa repository.")
            return
        
        # Run evaluation
        print(f"\n🔍 Evaluating {len(test_cases)} test cases...")
        
        responses = []
        total_time = 0
        successful_retrievals = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"  [{i}/{len(test_cases)}] {test_case.question[:50]}...")
            
            start_time = time.time()
            
            # Query Kodit
            search_result = await client.search(test_case.question)
            
            end_time = time.time()
            retrieval_time = end_time - start_time
            total_time += retrieval_time
            
            # Extract answer from result
            if "success" in search_result:
                answer = search_result.get("output", "No answer generated")
                success = True
                successful_retrievals += 1
                contexts = [answer]  # Use the full output as context
            else:
                answer = f"Error: {search_result.get('error', 'Unknown error')}"
                success = False
                contexts = []
            
            responses.append(RAGResponse(
                question=test_case.question,
                answer=answer,
                contexts=contexts,
                retrieval_time=retrieval_time,
                success=success
            ))
        
        # Calculate metrics
        print("\n📊 Calculating evaluation metrics...")
        
        total_similarity = 0
        total_keyword_overlap = 0
        total_quality = 0
        valid_responses = 0
        
        detailed_results = []
        
        for test_case, response in zip(test_cases, responses):
            if response.success:
                similarity = evaluator.similarity_score(test_case.expected_answer, response.answer)
                keyword_overlap = evaluator.keyword_overlap(test_case.expected_answer, response.answer)
                quality = evaluator.answer_quality_score(test_case.question, response.answer)
                
                total_similarity += similarity
                total_keyword_overlap += keyword_overlap
                total_quality += quality
                valid_responses += 1
            else:
                similarity = 0.0
                keyword_overlap = 0.0
                quality = 0.0
            
            detailed_results.append({
                "question": test_case.question,
                "category": test_case.category,
                "difficulty": test_case.difficulty,
                "expected_answer": test_case.expected_answer[:200] + "..." if len(test_case.expected_answer) > 200 else test_case.expected_answer,
                "generated_answer": response.answer[:200] + "..." if len(response.answer) > 200 else response.answer,
                "success": response.success,
                "similarity_score": similarity,
                "keyword_overlap": keyword_overlap,
                "quality_score": quality,
                "retrieval_time": response.retrieval_time
            })
        
        # Calculate overall metrics
        avg_similarity = total_similarity / valid_responses if valid_responses > 0 else 0
        avg_keyword_overlap = total_keyword_overlap / valid_responses if valid_responses > 0 else 0
        avg_quality = total_quality / valid_responses if valid_responses > 0 else 0
        success_rate = successful_retrievals / len(test_cases)
        avg_retrieval_time = total_time / len(test_cases)
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            "evaluation_metadata": {
                "timestamp": timestamp,
                "total_test_cases": len(test_cases),
                "evaluation_type": "simple_rag_evaluation"
            },
            "performance_metrics": {
                "success_rate": success_rate,
                "avg_retrieval_time": avg_retrieval_time,
                "successful_retrievals": successful_retrievals,
                "total_test_cases": len(test_cases)
            },
            "quality_metrics": {
                "avg_similarity_score": avg_similarity,
                "avg_keyword_overlap": avg_keyword_overlap,
                "avg_quality_score": avg_quality
            },
            "detailed_results": detailed_results
        }
        
        # Save JSON report
        json_file = output_path / f"simple_rag_evaluation_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save text summary
        summary_file = output_path / f"simple_rag_summary_{timestamp}.txt"
        with open(summary_file, 'w') as f:
            f.write("Simple RAG Evaluation Summary\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Evaluation Date: {timestamp}\n")
            f.write(f"Total Test Cases: {len(test_cases)}\n")
            f.write(f"Successful Retrievals: {successful_retrievals}\n")
            f.write(f"Success Rate: {success_rate:.2%}\n")
            f.write(f"Average Retrieval Time: {avg_retrieval_time:.4f}s\n\n")
            
            f.write("Quality Metrics:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Average Similarity Score: {avg_similarity:.4f}\n")
            f.write(f"Average Keyword Overlap: {avg_keyword_overlap:.4f}\n")
            f.write(f"Average Quality Score: {avg_quality:.4f}\n\n")
            
            # Category breakdown
            categories = {}
            for result in detailed_results:
                cat = result["category"]
                if cat not in categories:
                    categories[cat] = {"count": 0, "successful": 0}
                categories[cat]["count"] += 1
                if result["success"]:
                    categories[cat]["successful"] += 1
            
            f.write("Category Breakdown:\n")
            f.write("-" * 20 + "\n")
            for category, stats in categories.items():
                success_rate = stats["successful"] / stats["count"] if stats["count"] > 0 else 0
                f.write(f"{category.upper()}: {stats['successful']}/{stats['count']} ({success_rate:.1%})\n")
        
        # Print results
        print("\n" + "=" * 60)
        print("🎉 SIMPLE RAG EVALUATION COMPLETE")
        print("=" * 60)
        print(f"📊 Overall Results:")
        print(f"   Total Test Cases: {len(test_cases)}")
        print(f"   Successful Retrievals: {successful_retrievals}")
        print(f"   Success Rate: {success_rate:.2%}")
        print(f"   Average Retrieval Time: {avg_retrieval_time:.4f}s")
        
        print(f"\n🎯 Quality Metrics:")
        print(f"   Similarity Score: {avg_similarity:.4f}")
        print(f"   Keyword Overlap: {avg_keyword_overlap:.4f}")
        print(f"   Quality Score: {avg_quality:.4f}")
        
        print(f"\n📁 Results saved to:")
        print(f"   📄 {json_file}")
        print(f"   📋 {summary_file}")
        
        return report
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Run the evaluation
    asyncio.run(run_simple_evaluation()) 
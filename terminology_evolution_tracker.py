"""
Terminology Evolution Tracker - 術語演變追蹤器
Track how terms and their meanings change over time in a domain.
追蹤術語及其含義在特定領域中隨時間的變化。

Author: DigiMarketingAI
GitHub: https://github.com/digimarketingai
"""

import os
import re
import json
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from mistralai import Mistral
except ImportError:
    raise ImportError("Please install mistralai: pip install mistralai")


class TermStatus(Enum):
    """Term lifecycle status 術語生命週期狀態"""
    EMERGING = "emerging"           # 新興術語
    ESTABLISHED = "established"     # 已確立術語
    EVOLVING = "evolving"          # 演變中術語
    DEPRECATED = "deprecated"       # 已棄用術語
    ARCHAIC = "archaic"            # 古舊術語
    REVIVED = "revived"            # 復興術語


class SemanticShiftType(Enum):
    """Types of semantic shift 語義轉變類型"""
    NARROWING = "narrowing"         # 語義縮小
    BROADENING = "broadening"       # 語義擴大
    AMELIORATION = "amelioration"   # 語義升格
    PEJORATION = "pejoration"       # 語義降格
    METAPHOR = "metaphor"           # 隱喻轉變
    METONYMY = "metonymy"           # 轉喻轉變
    SPECIALIZATION = "specialization"  # 專業化
    GENERALIZATION = "generalization"  # 泛化


@dataclass
class TermSnapshot:
    """A snapshot of a term at a specific time period 特定時期的術語快照"""
    term: str
    period: str                     # e.g., "1990s", "2000-2010", "2020"
    year_start: int
    year_end: int
    definition: str
    definition_zh: str
    usage_context: str
    frequency: str                  # "high", "medium", "low", "rare"
    domain: str
    status: str
    example_sentence: str
    notes: str


@dataclass
class SemanticShift:
    """Record of a semantic shift 語義轉變記錄"""
    term: str
    shift_type: str
    period_from: str
    period_to: str
    meaning_before: str
    meaning_after: str
    explanation: str
    explanation_zh: str
    evidence: str


@dataclass
class TermEvolutionRecord:
    """Complete evolution record for a term 術語的完整演變記錄"""
    term: str
    domain: str
    origin_period: str
    origin_language: str
    etymology: str
    etymology_zh: str
    snapshots: List[Dict]
    semantic_shifts: List[Dict]
    related_terms: List[str]
    current_status: str
    future_prediction: str
    future_prediction_zh: str


class TerminologyEvolutionTracker:
    """
    Track terminology evolution over time.
    追蹤術語隨時間的演變。
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "mistral-medium-latest"):
        """
        Initialize the tracker.
        初始化追蹤器。
        
        Args:
            api_key: Mistral API key. Mistral API 金鑰。
            model: Mistral model to use. 使用的 Mistral 模型。
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set MISTRAL_API_KEY environment variable or pass api_key parameter.\n"
                "需要 API 金鑰。請設置 MISTRAL_API_KEY 環境變數或傳入 api_key 參數。"
            )
        
        self.model = model
        self.client = Mistral(api_key=self.api_key)
        self.evolution_database: Dict[str, TermEvolutionRecord] = {}
    
    def analyze_term_evolution(
        self,
        term: str,
        domain: str = "general",
        time_periods: Optional[List[str]] = None,
        languages: List[str] = ["English", "Traditional Chinese"]
    ) -> Optional[TermEvolutionRecord]:
        """
        Analyze the evolution of a term over time.
        分析術語隨時間的演變。
        
        Args:
            term: The term to analyze. 要分析的術語。
            domain: The domain/field of the term. 術語的領域。
            time_periods: Specific periods to analyze. 要分析的特定時期。
            languages: Languages for definitions. 定義的語言。
        
        Returns:
            TermEvolutionRecord with complete evolution data.
            包含完整演變數據的術語演變記錄。
        """
        
        if not time_periods:
            time_periods = ["Pre-1900", "1900-1950", "1950-1980", "1980-2000", "2000-2010", "2010-2020", "2020-Present"]
        
        prompt = f"""You are a historical linguist and terminology expert. Analyze the evolution of the following term through history.

TERM TO ANALYZE: "{term}"
DOMAIN/FIELD: {domain}
TIME PERIODS TO COVER: {', '.join(time_periods)}

Provide a comprehensive analysis in the following JSON format:

{{
    "term": "{term}",
    "domain": "{domain}",
    "origin_period": "earliest known period of use",
    "origin_language": "language of origin",
    "etymology": "detailed etymology in English",
    "etymology_zh": "詞源說明（繁體中文）",
    "snapshots": [
        {{
            "term": "term form used in this period",
            "period": "time period label",
            "year_start": 1900,
            "year_end": 1950,
            "definition": "definition during this period in English",
            "definition_zh": "此時期的定義（繁體中文）",
            "usage_context": "how it was used",
            "frequency": "high/medium/low/rare",
            "domain": "primary domain of use",
            "status": "emerging/established/evolving/deprecated/archaic/revived",
            "example_sentence": "example from this period",
            "notes": "additional notes"
        }}
    ],
    "semantic_shifts": [
        {{
            "term": "{term}",
            "shift_type": "narrowing/broadening/amelioration/pejoration/metaphor/metonymy/specialization/generalization",
            "period_from": "starting period",
            "period_to": "ending period",
            "meaning_before": "meaning before the shift",
            "meaning_after": "meaning after the shift",
            "explanation": "explanation of the shift in English",
            "explanation_zh": "語義轉變說明（繁體中文）",
            "evidence": "evidence or examples of this shift"
        }}
    ],
    "related_terms": ["list", "of", "related", "terms", "that", "emerged"],
    "current_status": "current status and usage",
    "future_prediction": "prediction for future evolution in English",
    "future_prediction_zh": "未來演變預測（繁體中文）"
}}

IMPORTANT GUIDELINES:
1. Provide snapshots for EACH time period where the term was in use
2. Identify ALL semantic shifts that occurred
3. Be historically accurate - if the term didn't exist in a period, note it
4. Include both English and Traditional Chinese (繁體中文) definitions
5. Note any spelling/form changes over time
6. Identify if the term was borrowed from another language
7. Track domain shifts (e.g., from technical to general use)

Respond ONLY with valid JSON. No additional text."""

        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = chat_response.choices[0].message.content
            
            # Parse JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                
                record = TermEvolutionRecord(
                    term=data.get("term", term),
                    domain=data.get("domain", domain),
                    origin_period=data.get("origin_period", "Unknown"),
                    origin_language=data.get("origin_language", "Unknown"),
                    etymology=data.get("etymology", ""),
                    etymology_zh=data.get("etymology_zh", ""),
                    snapshots=data.get("snapshots", []),
                    semantic_shifts=data.get("semantic_shifts", []),
                    related_terms=data.get("related_terms", []),
                    current_status=data.get("current_status", ""),
                    future_prediction=data.get("future_prediction", ""),
                    future_prediction_zh=data.get("future_prediction_zh", "")
                )
                
                # Store in database
                self.evolution_database[term] = record
                
                return record
            else:
                print(f"⚠️ Could not parse response for term: {term}")
                return None
                
        except Exception as e:
            print(f"❌ Error analyzing term '{term}': {str(e)}")
            return None
    
    def analyze_multiple_terms(
        self,
        terms: List[str],
        domain: str = "general"
    ) -> List[TermEvolutionRecord]:
        """
        Analyze evolution of multiple terms.
        分析多個術語的演變。
        """
        results = []
        for term in terms:
            print(f"Analyzing: {term}...")
            result = self.analyze_term_evolution(term, domain)
            if result:
                results.append(result)
        return results
    
    def compare_terms_evolution(
        self,
        terms: List[str],
        domain: str = "general"
    ) -> Dict:
        """
        Compare the evolution of multiple terms.
        比較多個術語的演變。
        """
        prompt = f"""You are a historical linguist. Compare the evolution of these terms in the {domain} domain:

TERMS: {', '.join(terms)}

Analyze and provide a comparison in this JSON format:

{{
    "terms_compared": {json.dumps(terms)},
    "domain": "{domain}",
    "comparison_summary": "overall comparison summary in English",
    "comparison_summary_zh": "整體比較摘要（繁體中文）",
    "emergence_timeline": [
        {{"term": "term1", "emerged": "period", "year_approx": 1900}},
        {{"term": "term2", "emerged": "period", "year_approx": 1950}}
    ],
    "evolution_patterns": [
        {{
            "pattern_name": "name of pattern",
            "pattern_name_zh": "模式名稱",
            "description": "description in English",
            "description_zh": "描述（繁體中文）",
            "terms_showing_pattern": ["term1", "term2"]
        }}
    ],
    "replacement_relationships": [
        {{
            "old_term": "deprecated term",
            "new_term": "replacement term",
            "transition_period": "when the shift happened",
            "reason": "why the replacement occurred"
        }}
    ],
    "semantic_divergence": [
        {{
            "terms": ["term1", "term2"],
            "originally": "original shared meaning",
            "diverged_to": {{"term1": "current meaning", "term2": "current meaning"}},
            "divergence_period": "when they diverged"
        }}
    ],
    "current_usage_ranking": [
        {{"term": "most used", "frequency": "high", "trend": "increasing/stable/decreasing"}},
        {{"term": "less used", "frequency": "medium", "trend": "increasing/stable/decreasing"}}
    ],
    "predictions": {{
        "likely_to_grow": ["terms expected to increase in use"],
        "likely_to_decline": ["terms expected to decrease"],
        "reasoning": "explanation in English",
        "reasoning_zh": "推理說明（繁體中文）"
    }}
}}

Respond ONLY with valid JSON."""

        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = chat_response.choices[0].message.content
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            
            if json_match:
                return json.loads(json_match.group())
            return None
            
        except Exception as e:
            print(f"❌ Error comparing terms: {str(e)}")
            return None
    
    def detect_neologisms(
        self,
        text: str,
        domain: str = "general",
        reference_period: str = "2020"
    ) -> List[Dict]:
        """
        Detect potential neologisms (new terms) in text.
        檢測文本中的潛在新詞。
        """
        prompt = f"""You are a neologism detection expert. Analyze this text for new or recently coined terms.

TEXT TO ANALYZE:
\"\"\"
{text}
\"\"\"

DOMAIN: {domain}
REFERENCE PERIOD: Terms new since {reference_period}

Identify neologisms and provide analysis in this JSON format:

{{
    "neologisms_found": [
        {{
            "term": "the new term",
            "translation_zh": "繁體中文翻譯",
            "first_appeared": "approximate year or period",
            "formation_type": "compound/blend/acronym/borrowing/semantic_shift/derivation",
            "formation_type_zh": "構詞類型",
            "source_elements": ["element1", "element2"],
            "definition": "definition in English",
            "definition_zh": "定義（繁體中文）",
            "domain": "primary domain",
            "adoption_level": "niche/growing/mainstream",
            "predicted_longevity": "ephemeral/established/permanent",
            "example_usage": "example sentence",
            "notes": "additional notes"
        }}
    ],
    "emerging_trends": [
        {{
            "trend": "description of terminology trend",
            "trend_zh": "術語趨勢描述",
            "examples": ["term1", "term2"]
        }}
    ],
    "total_neologisms": 0,
    "analysis_summary": "summary in English",
    "analysis_summary_zh": "分析摘要（繁體中文）"
}}

Respond ONLY with valid JSON."""

        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = chat_response.choices[0].message.content
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            
            if json_match:
                return json.loads(json_match.group())
            return None
            
        except Exception as e:
            print(f"❌ Error detecting neologisms: {str(e)}")
            return None
    
    def generate_timeline_data(self, record: TermEvolutionRecord) -> Dict:
        """
        Generate data structure for timeline visualization.
        生成時間線可視化的數據結構。
        """
        timeline_data = {
            "term": record.term,
            "domain": record.domain,
            "events": [],
            "periods": [],
            "shifts": []
        }
        
        # Add origin event
        timeline_data["events"].append({
            "type": "origin",
            "year": self._extract_year(record.origin_period),
            "period": record.origin_period,
            "label": f"Origin: {record.origin_language}",
            "description": record.etymology
        })
        
        # Add snapshots as periods
        for snapshot in record.snapshots:
            timeline_data["periods"].append({
                "period": snapshot.get("period", ""),
                "year_start": snapshot.get("year_start", 0),
                "year_end": snapshot.get("year_end", 0),
                "definition": snapshot.get("definition", ""),
                "status": snapshot.get("status", ""),
                "frequency": snapshot.get("frequency", "")
            })
        
        # Add semantic shifts
        for shift in record.semantic_shifts:
            timeline_data["shifts"].append({
                "type": shift.get("shift_type", ""),
                "period_from": shift.get("period_from", ""),
                "period_to": shift.get("period_to", ""),
                "meaning_before": shift.get("meaning_before", ""),
                "meaning_after": shift.get("meaning_after", ""),
                "explanation": shift.get("explanation", "")
            })
        
        return timeline_data
    
    def _extract_year(self, period_str: str) -> int:
        """Extract approximate year from period string."""
        # Try to find a year
        match = re.search(r'\d{4}', str(period_str))
        if match:
            return int(match.group())
        
        # Handle decade/century references
        period_lower = str(period_str).lower()
        if "pre-1900" in period_lower or "19th century" in period_lower:
            return 1850
        elif "1900" in period_lower:
            return 1925
        elif "1950" in period_lower:
            return 1965
        elif "1980" in period_lower:
            return 1990
        elif "2000" in period_lower:
            return 2005
        elif "2010" in period_lower:
            return 2015
        elif "2020" in period_lower or "present" in period_lower:
            return 2022
        
        return 2000  # Default
    
    def to_dict(self, record: TermEvolutionRecord) -> Dict:
        """Convert record to dictionary."""
        return asdict(record)
    
    def to_json(self, record: TermEvolutionRecord, indent: int = 2) -> str:
        """Convert record to JSON string."""
        return json.dumps(self.to_dict(record), ensure_ascii=False, indent=indent)


# Convenience function
def track_term_evolution(
    term: str,
    domain: str = "general",
    api_key: Optional[str] = None
) -> Optional[TermEvolutionRecord]:
    """
    Quick function to track term evolution.
    快速追蹤術語演變的函數。
    """
    tracker = TerminologyEvolutionTracker(api_key=api_key)
    return tracker.analyze_term_evolution(term, domain)


if __name__ == "__main__":
    print("Terminology Evolution Tracker - 術語演變追蹤器")
    print("=" * 50)
    print("Import this module to use the tracker.")
    print("導入此模組以使用追蹤器。")

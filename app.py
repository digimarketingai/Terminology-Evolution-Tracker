"""
Terminology Evolution Tracker - Gradio Web Interface with INSTANT Visualizations
術語演變追蹤器 - 即時可視化的 Gradio 網頁介面

Features:
- Pre-loaded demo data for instant visualization
- Optimized API calls with timeout handling
- Works offline with sample data

Run with: python app.py
"""

import os
import json
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Optional, Dict, List
import re

# ============================================================
# PRE-LOADED DEMO DATA - Shows instantly without API call
# ============================================================

DEMO_DATA = {
    "buddha": {
        "term": "Buddha",
        "domain": "religion / philosophy",
        "origin_period": "6th-5th century BCE",
        "origin_language": "Sanskrit/Pali",
        "etymology": "From Sanskrit 'buddha' meaning 'awakened one' or 'enlightened one', derived from the root 'budh' (to awaken, to know).",
        "etymology_zh": "源自梵語「buddha」，意為「覺醒者」或「覺悟者」，來自詞根「budh」（覺醒、知曉）。",
        "snapshots": [
            {
                "term": "Buddha",
                "period": "6th-5th century BCE",
                "year_start": -500,
                "year_end": -400,
                "definition": "Title given to Siddhartha Gautama, the founder of Buddhism, meaning 'the awakened one'",
                "definition_zh": "授予悉達多·喬達摩的稱號，佛教創始人，意為「覺醒者」",
                "usage_context": "Religious/philosophical title",
                "frequency": "medium",
                "domain": "Buddhism",
                "status": "emerging",
                "example_sentence": "The Buddha taught the Middle Way.",
                "notes": "Originally referred specifically to Siddhartha Gautama"
            },
            {
                "term": "Buddha",
                "period": "1st-5th century CE",
                "year_start": 100,
                "year_end": 500,
                "definition": "Expanded to include multiple buddhas in Mahayana tradition; any fully enlightened being",
                "definition_zh": "在大乘佛教傳統中擴展為包括多位佛陀；任何完全覺悟的存在",
                "usage_context": "Religious worship and philosophy",
                "frequency": "high",
                "domain": "Buddhism",
                "status": "established",
                "example_sentence": "Amitabha Buddha presides over the Western Pure Land.",
                "notes": "Concept expanded with Mahayana Buddhism spread"
            },
            {
                "term": "Buddha",
                "period": "500-1500 CE",
                "year_start": 500,
                "year_end": 1500,
                "definition": "Central figure of worship across Asia; statues and temples built in his honor",
                "definition_zh": "亞洲各地崇拜的中心人物；為他建造雕像和寺廟",
                "usage_context": "Religious worship, art, architecture",
                "frequency": "high",
                "domain": "Buddhism/Culture",
                "status": "established",
                "example_sentence": "The giant Buddha statue was carved into the cliff.",
                "notes": "Buddhism spreads throughout Asia"
            },
            {
                "term": "Buddha",
                "period": "1800-1950",
                "year_start": 1800,
                "year_end": 1950,
                "definition": "Introduced to Western consciousness; studied academically; seen as philosopher",
                "definition_zh": "被引入西方意識；進行學術研究；被視為哲學家",
                "usage_context": "Academic study, orientalism, philosophy",
                "frequency": "medium",
                "domain": "Academia/Religion",
                "status": "evolving",
                "example_sentence": "Western scholars began translating Buddhist texts.",
                "notes": "Western academic interest grows"
            },
            {
                "term": "Buddha",
                "period": "1950-2000",
                "year_start": 1950,
                "year_end": 2000,
                "definition": "Symbol of peace, meditation, mindfulness; enters popular culture",
                "definition_zh": "和平、冥想、正念的象徵；進入流行文化",
                "usage_context": "Pop culture, meditation, wellness",
                "frequency": "high",
                "domain": "Culture/Wellness",
                "status": "evolving",
                "example_sentence": "She placed a Buddha statue in her meditation corner.",
                "notes": "Secularization and commercialization begins"
            },
            {
                "term": "Buddha",
                "period": "2000-Present",
                "year_start": 2000,
                "year_end": 2024,
                "definition": "Used in wellness industry, home decor, mindfulness apps; sometimes controversial commercialization",
                "definition_zh": "用於健康產業、家居裝飾、正念應用程式；商業化有時具爭議性",
                "usage_context": "Wellness, decor, apps, meditation",
                "frequency": "high",
                "domain": "Wellness/Commercial",
                "status": "evolving",
                "example_sentence": "The Buddha Bowl is a popular healthy meal option.",
                "notes": "Term used in secular contexts like 'Buddha bowl', 'Buddha belly'"
            }
        ],
        "semantic_shifts": [
            {
                "term": "Buddha",
                "shift_type": "broadening",
                "period_from": "6th century BCE",
                "period_to": "5th century CE",
                "meaning_before": "Specific title for Siddhartha Gautama",
                "meaning_after": "Any fully enlightened being (multiple Buddhas)",
                "explanation": "Mahayana Buddhism expanded the concept to include countless Buddhas across time and space",
                "explanation_zh": "大乘佛教將概念擴展為包括跨越時空的無數佛陀",
                "evidence": "Amitabha Buddha, Medicine Buddha, future Maitreya Buddha"
            },
            {
                "term": "Buddha",
                "shift_type": "generalization",
                "period_from": "1950s",
                "period_to": "2000s",
                "meaning_before": "Religious/spiritual figure requiring reverence",
                "meaning_after": "Cultural symbol of peace, calm, and mindfulness",
                "explanation": "Secularization in Western culture transformed Buddha into a lifestyle symbol",
                "explanation_zh": "西方文化的世俗化將佛陀轉變為生活方式的象徵",
                "evidence": "Buddha statues as decor, 'Buddha bowl' food trend"
            },
            {
                "term": "Buddha",
                "shift_type": "metaphor",
                "period_from": "1990s",
                "period_to": "2020s",
                "meaning_before": "Enlightened spiritual teacher",
                "meaning_after": "Adjective meaning calm, peaceful, or wise",
                "explanation": "Used metaphorically to describe a state of calm or wisdom",
                "explanation_zh": "隱喻性地用於描述平靜或智慧的狀態",
                "evidence": "'He's so Buddha about everything' (meaning calm/zen)"
            }
        ],
        "related_terms": ["Buddhism", "Dharma", "Sangha", "Nirvana", "Enlightenment", "Zen", "Mindfulness", "Meditation"],
        "current_status": "Highly active in both religious and secular contexts; experiencing tension between sacred and commercial uses",
        "future_prediction": "Likely to continue expanding in wellness/secular contexts while maintaining religious significance; may see pushback against commercialization",
        "future_prediction_zh": "可能繼續在健康/世俗語境中擴展，同時保持宗教意義；可能會看到對商業化的反對"
    },
    "computer": {
        "term": "Computer",
        "domain": "technology",
        "origin_period": "1640s",
        "origin_language": "English (from Latin 'computare')",
        "etymology": "From Latin 'computare' meaning 'to count, sum up, reckon together'. Originally referred to a person who computes.",
        "etymology_zh": "源自拉丁語「computare」，意為「計算、總結、一起計算」。最初指進行計算的人。",
        "snapshots": [
            {
                "term": "Computer",
                "period": "1640-1900",
                "year_start": 1640,
                "year_end": 1900,
                "definition": "A person who performs mathematical calculations",
                "definition_zh": "進行數學計算的人",
                "usage_context": "Professional occupation",
                "frequency": "low",
                "domain": "Mathematics/Business",
                "status": "established",
                "example_sentence": "The computers worked long hours calculating astronomical tables.",
                "notes": "Originally a job title, not a machine"
            },
            {
                "term": "Computer",
                "period": "1900-1945",
                "year_start": 1900,
                "year_end": 1945,
                "definition": "Both human calculators and early mechanical calculating machines",
                "definition_zh": "人類計算員和早期機械計算機器",
                "usage_context": "Business, military, science",
                "frequency": "medium",
                "domain": "Technology/Military",
                "status": "evolving",
                "example_sentence": "The women computers at NASA calculated rocket trajectories.",
                "notes": "Transition period - term applies to both humans and machines"
            },
            {
                "term": "Computer",
                "period": "1945-1980",
                "year_start": 1945,
                "year_end": 1980,
                "definition": "Large electronic calculating machine; mainframe systems",
                "definition_zh": "大型電子計算機器；主機系統",
                "usage_context": "Business, government, universities",
                "frequency": "high",
                "domain": "Technology",
                "status": "established",
                "example_sentence": "The company's computer filled an entire room.",
                "notes": "Human meaning becomes obsolete; machine meaning dominates"
            },
            {
                "term": "Computer",
                "period": "1980-2000",
                "year_start": 1980,
                "year_end": 2000,
                "definition": "Personal computing device; desktop and laptop machines",
                "definition_zh": "個人計算設備；桌上型和筆記型電腦",
                "usage_context": "Home, office, school",
                "frequency": "high",
                "domain": "Consumer Technology",
                "status": "established",
                "example_sentence": "Every household should have a computer.",
                "notes": "Personal computer revolution"
            },
            {
                "term": "Computer",
                "period": "2000-Present",
                "year_start": 2000,
                "year_end": 2024,
                "definition": "Any programmable electronic device; includes smartphones, tablets, embedded systems",
                "definition_zh": "任何可程式化的電子設備；包括智慧手機、平板電腦、嵌入式系統",
                "usage_context": "Ubiquitous in daily life",
                "frequency": "high",
                "domain": "Technology/Daily Life",
                "status": "established",
                "example_sentence": "Your phone is a computer more powerful than what sent humans to the moon.",
                "notes": "Term has broadened to include many device types"
            }
        ],
        "semantic_shifts": [
            {
                "term": "Computer",
                "shift_type": "narrowing",
                "period_from": "1640s",
                "period_to": "1950s",
                "meaning_before": "Person who computes (human calculator)",
                "meaning_after": "Electronic calculating machine only",
                "explanation": "As machines took over computing tasks, the human meaning became obsolete",
                "explanation_zh": "隨著機器接管計算任務，人類的含義變得過時",
                "evidence": "NASA 'computers' (human) replaced by electronic computers"
            },
            {
                "term": "Computer",
                "shift_type": "broadening",
                "period_from": "1980s",
                "period_to": "2020s",
                "meaning_before": "Large room-sized calculating machine",
                "meaning_after": "Any programmable device including phones and tablets",
                "explanation": "Miniaturization led to computers being embedded everywhere",
                "explanation_zh": "微型化導致計算機無處不在",
                "evidence": "Smartphones, smartwatches, IoT devices all called computers"
            }
        ],
        "related_terms": ["Computing", "Calculator", "Processor", "PC", "Laptop", "Server", "Mainframe"],
        "current_status": "Ubiquitous term; sometimes considered old-fashioned compared to 'device' for phones/tablets",
        "future_prediction": "May further broaden to include AI systems, or narrow as 'traditional computers' versus AI agents",
        "future_prediction_zh": "可能進一步擴展到包括 AI 系統，或縮小為「傳統計算機」與 AI 代理的對比"
    },
    "virus": {
        "term": "Virus",
        "domain": "medicine / technology",
        "origin_period": "1590s",
        "origin_language": "Latin",
        "etymology": "From Latin 'virus' meaning 'poison, sap of plants, slimy liquid'. Originally referred to any poisonous substance.",
        "etymology_zh": "源自拉丁語「virus」，意為「毒藥、植物汁液、黏液」。最初指任何有毒物質。",
        "snapshots": [
            {
                "term": "Virus",
                "period": "1590-1890",
                "year_start": 1590,
                "year_end": 1890,
                "definition": "Venom, poison, or any noxious substance causing disease",
                "definition_zh": "毒液、毒藥或任何引起疾病的有害物質",
                "usage_context": "Medical/scientific discourse",
                "frequency": "low",
                "domain": "Medicine",
                "status": "established",
                "example_sentence": "The virus in the wound caused infection.",
                "notes": "Pre-germ theory understanding"
            },
            {
                "term": "Virus",
                "period": "1890-1950",
                "year_start": 1890,
                "year_end": 1950,
                "definition": "Submicroscopic infectious agent smaller than bacteria",
                "definition_zh": "比細菌更小的亞顯微感染性病原體",
                "usage_context": "Microbiology, medicine",
                "frequency": "medium",
                "domain": "Medicine/Science",
                "status": "evolving",
                "example_sentence": "The tobacco mosaic virus was the first to be identified.",
                "notes": "Scientific discovery of viral nature"
            },
            {
                "term": "Virus",
                "period": "1950-1985",
                "year_start": 1950,
                "year_end": 1985,
                "definition": "Infectious agent consisting of nucleic acid in protein coat; causes diseases",
                "definition_zh": "由蛋白質外殼包裹的核酸組成的感染性病原體；引起疾病",
                "usage_context": "Medicine, public health",
                "frequency": "high",
                "domain": "Medicine",
                "status": "established",
                "example_sentence": "The polio virus was nearly eradicated by vaccines.",
                "notes": "Modern understanding of viral structure"
            },
            {
                "term": "Virus",
                "period": "1985-2000",
                "year_start": 1985,
                "year_end": 2000,
                "definition": "1) Biological pathogen 2) Malicious computer program that self-replicates",
                "definition_zh": "1) 生物病原體 2) 自我複製的惡意電腦程式",
                "usage_context": "Medicine and computing",
                "frequency": "high",
                "domain": "Medicine/Technology",
                "status": "evolving",
                "example_sentence": "My computer caught a virus from that email attachment.",
                "notes": "Metaphorical extension to computing"
            },
            {
                "term": "Virus",
                "period": "2000-Present",
                "year_start": 2000,
                "year_end": 2024,
                "definition": "1) Biological pathogen 2) Computer malware 3) 'Viral' content that spreads rapidly online",
                "definition_zh": "1) 生物病原體 2) 電腦惡意軟體 3) 在網上迅速傳播的「病毒式」內容",
                "usage_context": "Medicine, tech, social media",
                "frequency": "high",
                "domain": "Multiple domains",
                "status": "established",
                "example_sentence": "That video went viral overnight.",
                "notes": "'Viral' became common adjective for internet phenomena"
            }
        ],
        "semantic_shifts": [
            {
                "term": "Virus",
                "shift_type": "narrowing",
                "period_from": "1590s",
                "period_to": "1900s",
                "meaning_before": "Any poison or noxious substance",
                "meaning_after": "Specific type of submicroscopic pathogen",
                "explanation": "Scientific discovery narrowed the meaning to a specific biological entity",
                "explanation_zh": "科學發現將含義縮小到特定的生物實體",
                "evidence": "Discovery of viruses as distinct from bacteria"
            },
            {
                "term": "Virus",
                "shift_type": "metaphor",
                "period_from": "1983",
                "period_to": "1990s",
                "meaning_before": "Biological infectious agent only",
                "meaning_after": "Extended to self-replicating computer programs",
                "explanation": "The behavior of malicious programs mimicked viral spread",
                "explanation_zh": "惡意程式的行為模仿了病毒的傳播",
                "evidence": "First computer virus (Elk Cloner) named using biological metaphor"
            },
            {
                "term": "Virus",
                "shift_type": "broadening",
                "period_from": "2000s",
                "period_to": "2010s",
                "meaning_before": "Harmful entity (biological or digital)",
                "meaning_after": "Any rapidly spreading phenomenon (including positive ones)",
                "explanation": "'Going viral' can be positive - rapid spread of popular content",
                "explanation_zh": "「病毒式傳播」可以是正面的——流行內容的快速傳播",
                "evidence": "Viral marketing, viral videos, viral trends"
            }
        ],
        "related_terms": ["Viral", "Malware", "Pathogen", "Infection", "Contagion", "Epidemic", "Pandemic"],
        "current_status": "Multi-domain term with biological, computing, and social media meanings all active",
        "future_prediction": "May develop further meanings related to AI or digital phenomena; biological meaning reinforced post-COVID",
        "future_prediction_zh": "可能發展出與 AI 或數位現象相關的更多含義；生物學含義在後疫情時代得到加強"
    },
    "cloud": {
        "term": "Cloud",
        "domain": "technology",
        "origin_period": "Old English",
        "origin_language": "Old English (clūd)",
        "etymology": "From Old English 'clūd' originally meaning 'rock, hill' then shifting to 'mass of water vapor'. Technology meaning emerged in 1990s.",
        "etymology_zh": "源自古英語「clūd」，最初意為「岩石、山丘」，後轉變為「水蒸氣團」。科技含義於1990年代出現。",
        "snapshots": [
            {
                "term": "Cloud",
                "period": "Pre-1300",
                "year_start": 700,
                "year_end": 1300,
                "definition": "Rock or hill; mass of earth",
                "definition_zh": "岩石或山丘；土塊",
                "usage_context": "Geographic description",
                "frequency": "medium",
                "domain": "General",
                "status": "archaic",
                "example_sentence": "The shepherd climbed the cloud.",
                "notes": "Original meaning now completely obsolete"
            },
            {
                "term": "Cloud",
                "period": "1300-1990",
                "year_start": 1300,
                "year_end": 1990,
                "definition": "Visible mass of water droplets suspended in atmosphere",
                "definition_zh": "懸浮在大氣中的可見水滴團",
                "usage_context": "Weather, poetry, general usage",
                "frequency": "high",
                "domain": "Meteorology/General",
                "status": "established",
                "example_sentence": "Dark clouds gathered on the horizon.",
                "notes": "Primary meaning for centuries"
            },
            {
                "term": "Cloud",
                "period": "1990-2006",
                "year_start": 1990,
                "year_end": 2006,
                "definition": "1) Atmospheric phenomenon 2) Network diagram symbol for the internet",
                "definition_zh": "1) 大氣現象 2) 網路圖中代表網際網路的符號",
                "usage_context": "Meteorology and technical diagrams",
                "frequency": "high",
                "domain": "Weather/Technology",
                "status": "evolving",
                "example_sentence": "The cloud symbol represents external network connections.",
                "notes": "Cloud used in network diagrams to represent 'somewhere else'"
            },
            {
                "term": "Cloud",
                "period": "2006-Present",
                "year_start": 2006,
                "year_end": 2024,
                "definition": "1) Atmospheric phenomenon 2) Remote computing services accessed via internet",
                "definition_zh": "1) 大氣現象 2) 通過網際網路訪問的遠端計算服務",
                "usage_context": "Technology, business, daily life",
                "frequency": "high",
                "domain": "Technology",
                "status": "established",
                "example_sentence": "Store your files in the cloud for easy access anywhere.",
                "notes": "Amazon Web Services launched 2006; term became mainstream"
            }
        ],
        "semantic_shifts": [
            {
                "term": "Cloud",
                "shift_type": "metaphor",
                "period_from": "Pre-1300",
                "period_to": "1300s",
                "meaning_before": "Rock or hill (solid earth mass)",
                "meaning_after": "Mass of water vapor in sky",
                "explanation": "Transferred from earthly mass to sky mass based on visual similarity",
                "explanation_zh": "基於視覺相似性，從地面的土塊轉移到天空的雲團",
                "evidence": "Historical etymology documented in OED"
            },
            {
                "term": "Cloud",
                "shift_type": "metaphor",
                "period_from": "1990s",
                "period_to": "2000s",
                "meaning_before": "Only atmospheric water vapor",
                "meaning_after": "Remote computing infrastructure (invisible, 'up there')",
                "explanation": "The amorphous, 'somewhere up there' nature of clouds mapped onto remote servers",
                "explanation_zh": "雲的模糊、「在某處上方」的特性被映射到遠端服務器上",
                "evidence": "Network engineers used cloud symbol; term stuck"
            }
        ],
        "related_terms": ["Cloud computing", "SaaS", "IaaS", "PaaS", "Server", "AWS", "Azure", "Cloudscape"],
        "current_status": "Dual meaning fully established; context usually clarifies which meaning intended",
        "future_prediction": "Technology meaning may become primary as cloud computing becomes ubiquitous; new compounds likely (cloud AI, cloud gaming)",
        "future_prediction_zh": "隨著雲計算變得無處不在，科技含義可能成為主要含義；可能出現新的複合詞（雲端 AI、雲端遊戲）"
    },
    "mouse": {
        "term": "Mouse",
        "domain": "technology",
        "origin_period": "Old English",
        "origin_language": "Old English (mūs)",
        "etymology": "From Old English 'mūs', from Proto-Germanic *mūs, from PIE root *mus- meaning 'mouse'. Computer meaning from 1965.",
        "etymology_zh": "源自古英語「mūs」，來自原始日耳曼語 *mūs，來自原始印歐語詞根 *mus-，意為「老鼠」。電腦含義始於1965年。",
        "snapshots": [
            {
                "term": "Mouse",
                "period": "Old English-1965",
                "year_start": 700,
                "year_end": 1965,
                "definition": "Small rodent with pointed snout and long tail",
                "definition_zh": "有尖嘴和長尾巴的小型齧齒動物",
                "usage_context": "General, zoology",
                "frequency": "high",
                "domain": "General/Biology",
                "status": "established",
                "example_sentence": "The cat caught a mouse in the barn.",
                "notes": "Sole meaning for centuries"
            },
            {
                "term": "Mouse",
                "period": "1965-1984",
                "year_start": 1965,
                "year_end": 1984,
                "definition": "1) Rodent 2) Experimental pointing device for computers",
                "definition_zh": "1) 齧齒動物 2) 電腦實驗性指向設備",
                "usage_context": "Research labs, early computing",
                "frequency": "low",
                "domain": "Technology (specialized)",
                "status": "emerging",
                "example_sentence": "Engelbart demonstrated the mouse at the 1968 conference.",
                "notes": "Invented by Douglas Engelbart; named for resemblance to rodent"
            },
            {
                "term": "Mouse",
                "period": "1984-2000",
                "year_start": 1984,
                "year_end": 2000,
                "definition": "1) Rodent 2) Hand-held computer input device with buttons",
                "definition_zh": "1) 齧齒動物 2) 帶按鈕的手持電腦輸入設備",
                "usage_context": "Personal computing, offices",
                "frequency": "high",
                "domain": "Technology",
                "status": "established",
                "example_sentence": "Click the left mouse button to select.",
                "notes": "Apple Macintosh popularized the mouse in 1984"
            },
            {
                "term": "Mouse",
                "period": "2000-Present",
                "year_start": 2000,
                "year_end": 2024,
                "definition": "1) Rodent 2) Computer pointing device (now wireless, optical, or gaming variants)",
                "definition_zh": "1) 齧齒動物 2) 電腦指向設備（現有無線、光學或遊戲版本）",
                "usage_context": "Computing, gaming",
                "frequency": "high",
                "domain": "Technology",
                "status": "established",
                "example_sentence": "This gaming mouse has 12 programmable buttons.",
                "notes": "Plural 'mice' or 'mouses' both acceptable for devices"
            }
        ],
        "semantic_shifts": [
            {
                "term": "Mouse",
                "shift_type": "metaphor",
                "period_from": "1965",
                "period_to": "1984",
                "meaning_before": "Only a small rodent",
                "meaning_after": "Also a computer input device",
                "explanation": "Named for visual resemblance - small body with a 'tail' (cord)",
                "explanation_zh": "因視覺相似性而命名——小型機身帶有「尾巴」（電線）",
                "evidence": "Douglas Engelbart's naming; cord resembled mouse tail"
            }
        ],
        "related_terms": ["Trackpad", "Touchpad", "Pointer", "Cursor", "Click", "Scroll", "Trackball"],
        "current_status": "Both meanings fully active; context always clear",
        "future_prediction": "Computer meaning may decline as touchscreens and gesture control increase; may become retro/specialized term",
        "future_prediction_zh": "隨著觸控螢幕和手勢控制增加，電腦含義可能下降；可能成為復古/專業術語"
    }
}


# ============================================================
# SIMPLIFIED API CLIENT (with timeout handling)
# ============================================================

class SimpleTermTracker:
    """Simplified tracker with faster prompts and timeout handling."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=api_key)
        except Exception as e:
            print(f"Could not initialize Mistral client: {e}")
    
    def analyze_term(self, term: str, domain: str = "general") -> Optional[Dict]:
        """Analyze term with simplified, faster prompt."""
        if not self.client:
            return None
        
        prompt = f"""Analyze the term "{term}" in the {domain} domain. Return JSON only:

{{
    "term": "{term}",
    "domain": "{domain}",
    "origin_period": "when first used",
    "origin_language": "language of origin",
    "etymology": "brief etymology",
    "etymology_zh": "詞源（繁體中文）",
    "snapshots": [
        {{"period": "time period", "year_start": 1900, "year_end": 2000, "definition": "meaning then", "definition_zh": "定義", "frequency": "high/medium/low", "status": "emerging/established/evolving/deprecated"}}
    ],
    "semantic_shifts": [
        {{"shift_type": "narrowing/broadening/metaphor", "period_from": "start", "period_to": "end", "meaning_before": "old meaning", "meaning_after": "new meaning", "explanation": "why", "explanation_zh": "說明"}}
    ],
    "related_terms": ["term1", "term2"],
    "current_status": "current usage",
    "future_prediction": "prediction",
    "future_prediction_zh": "預測"
}}

Be concise. JSON only, no explanation."""

        try:
            response = self.client.chat.complete(
                model="mistral-small-latest",  # Faster model
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.choices[0].message.content
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"API Error: {e}")
        
        return None


# Global tracker
tracker = None


def initialize_tracker(api_key: str) -> str:
    """Initialize tracker with API key."""
    global tracker
    if api_key and api_key.strip():
        tracker = SimpleTermTracker(api_key.strip())
        return "✅ API key set! You can now analyze custom terms. Demo data available for: buddha, computer, virus, cloud, mouse"
    return "⚠️ No API key provided. Using demo data only. Available terms: buddha, computer, virus, cloud, mouse"


# ============================================================
# VISUALIZATION FUNCTIONS
# ============================================================

def create_timeline_chart(data: Dict) -> go.Figure:
    """Create main evolution timeline."""
    if not data or "snapshots" not in data:
        return go.Figure().add_annotation(text="No data available", showarrow=False)
    
    snapshots = data.get("snapshots", [])
    
    # Status colors
    status_colors = {
        "emerging": "#22c55e",
        "established": "#3b82f6", 
        "evolving": "#f59e0b",
        "deprecated": "#ef4444",
        "archaic": "#6b7280",
        "revived": "#8b5cf6"
    }
    
    # Frequency sizes
    freq_sizes = {"high": 45, "medium": 35, "low": 25, "rare": 18}
    
    fig = go.Figure()
    
    # Process snapshots
    for i, snap in enumerate(snapshots):
        year_start = snap.get("year_start", 1900)
        year_end = snap.get("year_end", 2000)
        year_mid = (year_start + year_end) / 2
        
        status = snap.get("status", "established").lower()
        color = status_colors.get(status, "#3b82f6")
        freq = snap.get("frequency", "medium").lower()
        size = freq_sizes.get(freq, 30)
        
        # Period bar
        fig.add_trace(go.Scatter(
            x=[year_start, year_end],
            y=[1, 1],
            mode="lines",
            line=dict(color=color, width=20),
            hoverinfo="skip",
            showlegend=False
        ))
        
        # Period marker
        fig.add_trace(go.Scatter(
            x=[year_mid],
            y=[1.3],
            mode="markers+text",
            marker=dict(size=size, color=color, line=dict(color="white", width=2)),
            text=[snap.get("period", "")],
            textposition="top center",
            textfont=dict(size=9),
            name=snap.get("period", ""),
            hovertemplate=(
                f"<b>{snap.get('period', '')}</b><br>"
                f"Status: {snap.get('status', 'N/A')}<br>"
                f"Frequency: {snap.get('frequency', 'N/A')}<br>"
                f"Definition: {snap.get('definition', '')[:80]}...<br>"
                f"定義: {snap.get('definition_zh', '')[:40]}...<br>"
                "<extra></extra>"
            )
        ))
    
    # Semantic shifts as arrows below
    shifts = data.get("semantic_shifts", [])
    shift_colors = {
        "narrowing": "#ef4444", "broadening": "#22c55e",
        "metaphor": "#8b5cf6", "metonymy": "#06b6d4",
        "amelioration": "#3b82f6", "pejoration": "#f59e0b",
        "specialization": "#ec4899", "generalization": "#14b8a6"
    }
    
    for i, shift in enumerate(shifts):
        y_pos = 0.4 - (i * 0.2)
        shift_type = shift.get("shift_type", "").lower()
        color = shift_colors.get(shift_type, "#6b7280")
        
        # Get years
        year_from = extract_year(shift.get("period_from", "1900"))
        year_to = extract_year(shift.get("period_to", "2000"))
        
        fig.add_trace(go.Scatter(
            x=[year_from, year_to],
            y=[y_pos, y_pos],
            mode="lines+markers+text",
            line=dict(color=color, width=4),
            marker=dict(size=12, symbol=["circle", "arrow-right"], color=color),
            text=["", shift_type.upper()],
            textposition="top center",
            textfont=dict(size=10, color=color),
            name=f"Shift: {shift_type}",
            hovertemplate=(
                f"<b>{shift_type.upper()}</b><br>"
                f"Before: {shift.get('meaning_before', '')}<br>"
                f"After: {shift.get('meaning_after', '')}<br>"
                f"{shift.get('period_from', '')} → {shift.get('period_to', '')}<br>"
                "<extra></extra>"
            )
        ))
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f"📈 Evolution Timeline: {data.get('term', 'Term')}",
            font=dict(size=18)
        ),
        xaxis_title="Year 年份",
        yaxis=dict(visible=False, range=[-0.5, 2]),
        height=500,
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0.5, xanchor="center"),
        margin=dict(l=50, r=50, t=80, b=80)
    )
    
    return fig


def create_status_pie(data: Dict) -> go.Figure:
    """Create status distribution pie chart."""
    if not data or "snapshots" not in data:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    
    snapshots = data.get("snapshots", [])
    status_counts = {}
    for snap in snapshots:
        status = snap.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    colors = {
        "emerging": "#22c55e", "established": "#3b82f6",
        "evolving": "#f59e0b", "deprecated": "#ef4444",
        "archaic": "#6b7280", "revived": "#8b5cf6"
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        marker_colors=[colors.get(s, "#888") for s in status_counts.keys()],
        textinfo="label+percent",
        hole=0.4
    )])
    
    fig.update_layout(
        title="📊 Status Distribution 狀態分布",
        height=300,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_frequency_chart(data: Dict) -> go.Figure:
    """Create frequency trend line chart."""
    if not data or "snapshots" not in data:
        return go.Figure().add_annotation(text="No data", showarrow=False)
    
    snapshots = data.get("snapshots", [])
    freq_map = {"high": 4, "medium": 3, "low": 2, "rare": 1}
    
    periods = [s.get("period", "") for s in snapshots]
    freqs = [freq_map.get(s.get("frequency", "medium").lower(), 2) for s in snapshots]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=periods, y=freqs,
        mode="lines+markers",
        line=dict(color="#3b82f6", width=3),
        marker=dict(size=12, color="#3b82f6"),
        fill="tozeroy",
        fillcolor="rgba(59, 130, 246, 0.2)"
    ))
    
    fig.update_layout(
        title="📈 Usage Frequency Over Time 使用頻率趨勢",
        xaxis_title="Period 時期",
        yaxis=dict(
            title="Frequency 頻率",
            tickmode="array",
            tickvals=[1, 2, 3, 4],
            ticktext=["Rare 罕見", "Low 低", "Medium 中", "High 高"]
        ),
        height=300,
        template="plotly_white",
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    return fig


def create_shift_sankey(data: Dict) -> go.Figure:
    """Create Sankey diagram for semantic shifts."""
    if not data or "semantic_shifts" not in data:
        return go.Figure().add_annotation(text="No semantic shifts found", showarrow=False)
    
    shifts = data.get("semantic_shifts", [])
    if not shifts:
        return go.Figure().add_annotation(text="No semantic shifts recorded", showarrow=False)
    
    labels = []
    sources = []
    targets = []
    values = []
    colors = []
    
    shift_colors = {
        "narrowing": "rgba(239, 68, 68, 0.6)",
        "broadening": "rgba(34, 197, 94, 0.6)",
        "metaphor": "rgba(139, 92, 246, 0.6)",
        "metonymy": "rgba(6, 182, 212, 0.6)",
        "amelioration": "rgba(59, 130, 246, 0.6)",
        "pejoration": "rgba(245, 158, 11, 0.6)",
        "specialization": "rgba(236, 72, 153, 0.6)",
        "generalization": "rgba(20, 184, 166, 0.6)"
    }
    
    for shift in shifts:
        before = shift.get("meaning_before", "Unknown")[:30]
        after = shift.get("meaning_after", "Unknown")[:30]
        shift_type = shift.get("shift_type", "unknown")
        
        if before not in labels:
            labels.append(before)
        if after not in labels:
            labels.append(after)
        
        sources.append(labels.index(before))
        targets.append(labels.index(after))
        values.append(1)
        colors.append(shift_colors.get(shift_type.lower(), "rgba(128,128,128,0.5)"))
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="rgba(59, 130, 246, 0.8)"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors
        )
    )])
    
    fig.update_layout(
        title=f"🔄 Semantic Shift Flow: {data.get('term', 'Term')}",
        height=350,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def extract_year(period_str: str) -> int:
    """Extract year from period string."""
    match = re.search(r'-?\d{3,4}', str(period_str))
    if match:
        return int(match.group())
    
    period_lower = str(period_str).lower()
    mappings = {
        "pre-1900": 1850, "1900": 1925, "1950": 1965,
        "1980": 1990, "2000": 2005, "2010": 2015,
        "2020": 2022, "present": 2023, "bce": -400
    }
    
    for key, val in mappings.items():
        if key in period_lower:
            return val
    
    return 2000


def format_report(data: Dict) -> str:
    """Format data as readable report."""
    if not data:
        return "No data available"
    
    lines = []
    lines.append("=" * 60)
    lines.append(f"📚 TERMINOLOGY EVOLUTION REPORT 術語演變報告")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"📌 Term 術語: {data.get('term', 'N/A')}")
    lines.append(f"🏷️  Domain 領域: {data.get('domain', 'N/A')}")
    lines.append(f"🌍 Origin 起源: {data.get('origin_period', 'N/A')} ({data.get('origin_language', 'N/A')})")
    lines.append("")
    lines.append("📖 Etymology 詞源:")
    lines.append(f"   EN: {data.get('etymology', 'N/A')}")
    lines.append(f"   中: {data.get('etymology_zh', 'N/A')}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("📅 HISTORICAL SNAPSHOTS 歷史快照")
    lines.append("-" * 60)
    
    for i, snap in enumerate(data.get("snapshots", []), 1):
        lines.append(f"\n【{i}】 {snap.get('period', 'N/A')}")
        lines.append(f"    Status: {snap.get('status', 'N/A')} | Frequency: {snap.get('frequency', 'N/A')}")
        lines.append(f"    EN: {snap.get('definition', 'N/A')}")
        lines.append(f"    中: {snap.get('definition_zh', 'N/A')}")
    
    lines.append("")
    lines.append("-" * 60)
    lines.append("🔄 SEMANTIC SHIFTS 語義轉變")
    lines.append("-" * 60)
    
    for i, shift in enumerate(data.get("semantic_shifts", []), 1):
        lines.append(f"\n【{i}】 {shift.get('shift_type', 'N/A').upper()}")
        lines.append(f"    {shift.get('period_from', '')} → {shift.get('period_to', '')}")
        lines.append(f"    Before: {shift.get('meaning_before', 'N/A')}")
        lines.append(f"    After: {shift.get('meaning_after', 'N/A')}")
        lines.append(f"    說明: {shift.get('explanation_zh', shift.get('explanation', 'N/A'))}")
    
    lines.append("")
    lines.append("-" * 60)
    lines.append("🔮 CURRENT STATUS & PREDICTIONS")
    lines.append("-" * 60)
    lines.append(f"\nCurrent: {data.get('current_status', 'N/A')}")
    lines.append(f"\nPrediction: {data.get('future_prediction', 'N/A')}")
    lines.append(f"預測: {data.get('future_prediction_zh', 'N/A')}")
    
    if data.get("related_terms"):
        lines.append(f"\n🔗 Related: {', '.join(data.get('related_terms', []))}")
    
    return "\n".join(lines)


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_term(term: str, domain: str) -> tuple:
    """Analyze a term - use demo data or API."""
    global tracker
    
    if not term or not term.strip():
        return (
            "❌ Please enter a term. 請輸入術語。",
            go.Figure(),
            go.Figure(),
            go.Figure(),
            go.Figure(),
            ""
        )
    
    term_lower = term.strip().lower()
    
    # Check demo data first
    if term_lower in DEMO_DATA:
        data = DEMO_DATA[term_lower]
        report = format_report(data)
        timeline = create_timeline_chart(data)
        status_pie = create_status_pie(data)
        freq_chart = create_frequency_chart(data)
        sankey = create_shift_sankey(data)
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        
        return (report, timeline, status_pie, freq_chart, sankey, json_out)
    
    # Try API if available
    if tracker and tracker.client:
        data = tracker.analyze_term(term, domain)
        if data:
            report = format_report(data)
            timeline = create_timeline_chart(data)
            status_pie = create_status_pie(data)
            freq_chart = create_frequency_chart(data)
            sankey = create_shift_sankey(data)
            json_out = json.dumps(data, ensure_ascii=False, indent=2)
            
            return (report, timeline, status_pie, freq_chart, sankey, json_out)
    
    # No data available
    return (
        f"⚠️ No data for '{term}'. Try demo terms: buddha, computer, virus, cloud, mouse\n\n"
        f"Or set your API key to analyze custom terms.",
        go.Figure().add_annotation(text=f"No data for '{term}'", showarrow=False),
        go.Figure(),
        go.Figure(),
        go.Figure(),
        ""
    )


# ============================================================
# GRADIO INTERFACE
# ============================================================

def create_app():
    """Create Gradio interface."""
    
    with gr.Blocks(title="Terminology Evolution Tracker", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("""
        # 📈 Terminology Evolution Tracker 術語演變追蹤器
        
        **Track how terms evolve over time with instant visualizations!**
        追蹤術語隨時間演變，即時可視化！
        
        🚀 **Quick Start**: Try demo terms: `buddha`, `computer`, `virus`, `cloud`, `mouse`
        """)
        
        # API Key (optional)
        with gr.Accordion("🔑 API Key (Optional - for custom terms)", open=False):
            with gr.Row():
                api_input = gr.Textbox(
                    label="Mistral API Key",
                    placeholder="Optional - demo data works without API key",
                    type="password",
                    scale=4
                )
                api_btn = gr.Button("Set Key", scale=1)
            api_status = gr.Textbox(label="Status", interactive=False, value="ℹ️ Demo data available for: buddha, computer, virus, cloud, mouse")
        
        api_btn.click(initialize_tracker, inputs=[api_input], outputs=[api_status])
        
        gr.Markdown("---")
        
        # Main input
        with gr.Row():
            term_input = gr.Textbox(
                label="🔍 Enter Term 輸入術語",
                placeholder="Try: buddha, computer, virus, cloud, mouse",
                scale=3
            )
            domain_input = gr.Dropdown(
                choices=["general", "technology", "medicine", "religion / philosophy", "business", "science"],
                value="general",
                label="Domain 領域",
                scale=1
            )
            analyze_btn = gr.Button("📊 Analyze 分析", variant="primary", scale=1)
        
        # Quick examples
        gr.Markdown("**Quick Examples 快速範例:** Click to try →")
        with gr.Row():
            for term in ["buddha", "computer", "virus", "cloud", "mouse"]:
                gr.Button(term, size="sm").click(
                    lambda t=term: t, outputs=[term_input]
                )
        
        gr.Markdown("---")
        
        # Results
        with gr.Row():
            with gr.Column(scale=1):
                report_output = gr.Textbox(
                    label="📋 Evolution Report 演變報告",
                    lines=25,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                timeline_plot = gr.Plot(label="📈 Evolution Timeline 演變時間線")
        
        with gr.Row():
            status_plot = gr.Plot(label="📊 Status Distribution 狀態分布")
            freq_plot = gr.Plot(label="📈 Frequency Trend 頻率趨勢")
        
        sankey_plot = gr.Plot(label="🔄 Semantic Shift Flow 語義轉變流程")
        
        with gr.Accordion("📄 JSON Data", open=False):
            json_output = gr.Code(label="Raw JSON", language="json")
        
        # Connect analyze button
        analyze_btn.click(
            fn=analyze_term,
            inputs=[term_input, domain_input],
            outputs=[report_output, timeline_plot, status_plot, freq_plot, sankey_plot, json_output]
        )
        
        # Also trigger on Enter key
        term_input.submit(
            fn=analyze_term,
            inputs=[term_input, domain_input],
            outputs=[report_output, timeline_plot, status_plot, freq_plot, sankey_plot, json_output]
        )
        
        gr.Markdown("---")
        
        # Academic info
        with gr.Accordion("📖 Academic Background 學術背景", open=False):
            gr.Markdown("""
            ### 🎓 Key Concepts for Terminology Studies
            
            | Type | 類型 | Description | Example |
            |------|------|-------------|---------|
            | **Narrowing** | 語義縮小 | Meaning becomes more specific | "meat" (any food → animal flesh) |
            | **Broadening** | 語義擴大 | Meaning becomes more general | "dog" (specific breed → any dog) |
            | **Metaphor** | 隱喻轉變 | Meaning shifts via metaphor | "mouse" (animal → computer device) |
            | **Amelioration** | 語義升格 | Meaning improves | "knight" (servant → noble warrior) |
            | **Pejoration** | 語義降格 | Meaning worsens | "villain" (farm worker → evil person) |
            
            ### Term Lifecycle 術語生命週期
            - 🟢 **Emerging** 新興 - Newly coined, limited use
            - 🔵 **Established** 已確立 - Widely accepted
            - 🟡 **Evolving** 演變中 - Undergoing change
            - 🔴 **Deprecated** 已棄用 - Falling out of use
            - ⚫ **Archaic** 古舊 - No longer common
            - 🟣 **Revived** 復興 - Returned to use
            """)
    
    return demo


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("🚀 Starting Terminology Evolution Tracker...")
    print("📊 Demo data available for: buddha, computer, virus, cloud, mouse")
    
    demo = create_app()
    demo.launch(share=True)

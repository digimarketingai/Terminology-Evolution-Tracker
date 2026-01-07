# 📈 Terminology Evolution Tracker 術語演變追蹤器

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

### 📖 Description

An AI-powered tool for tracking how terminology evolves over time. Designed for postgraduate terminology studies, this tool provides:

- **Historical Analysis**: Track terms through different time periods
- **Semantic Shift Detection**: Identify meaning changes (narrowing, broadening, metaphor, etc.)
- **Neologism Detection**: Find and analyze new terms in text
- **Interactive Visualizations**: Timeline charts, status distributions, frequency trends
- **Bilingual Support**: English and Traditional Chinese

### 🎓 Academic Value

This tool teaches key concepts in **diachronic terminology** and **neology**:

| Concept | Description |
|---------|-------------|
| Diachronic Terminology | Study of term evolution over time |
| Neology | Study of new word formation |
| Semantic Shift | Changes in word meaning |
| Terminology Planning | Strategic term management |

### 🚀 Quick Start

#### Google Colab (Recommended for Students)

```python
# Install dependencies
!pip install mistralai gradio plotly -q

# Clone repository
!git clone https://github.com/digimarketingai/Terminology-Evolution-Tracker.git
%cd Terminology-Evolution-Tracker

# Set API key
import os
os.environ["MISTRAL_API_KEY"] = "your-api-key-here"

# Launch interface
!python app.py

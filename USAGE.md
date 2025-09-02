# ProfileStrap - Universal Company Analysis Tool

ProfileStrap is now a flexible tool that can analyze **any company's website** to generate comprehensive business profiles for meeting preparation.

## Features

- 🔍 **Auto-discovers important pages** (about, services, contact, work, team, etc.)
- 🤖 **AI-powered analysis** using OpenAI GPT models
- 📊 **Link analysis** and categorization
- 📝 **Manual fallback** when AI is unavailable
- 🎯 **Meeting-focused insights** for business preparation

## Quick Start

### 1. Basic Usage
```bash
# Analyze any company website
python generate_summary.py https://stripe.com

# With custom output file
python generate_summary.py https://openai.com --output openai_profile.txt

# Limit number of pages scraped
python generate_summary.py https://anthropic.com --pages 5

# Skip AI and use manual summary
python generate_summary.py https://example.com --no-ai
```

### 2. Link Analysis Only
```bash
# Just analyze links without generating summary
python main.py https://company.com
```

### 3. Programmatic Usage
```python
from main import analyze_company

# Analyze a company
summary = analyze_company(
    url="https://company.com",
    output_file="company_profile.txt",
    max_pages=8,
    use_ai=True
)
print(summary)
```

## Command Line Options

### generate_summary.py
- `url` - Company website URL (required)
- `--output, -o` - Output filename (auto-generated if not provided)
- `--pages, -p` - Maximum pages to scrape (default: 8)
- `--no-ai` - Skip AI summary generation

### main.py
- `url` - Website URL to analyze (required)
- `--output, -o` - Output filename
- `--pages, -p` - Maximum pages to scrape
- `--no-ai` - Skip AI summary generation

## What It Analyzes

The tool automatically discovers and analyzes:

- **About/Company pages** - Mission, vision, history
- **Services/Solutions** - What the company offers
- **Contact information** - How to reach them
- **Work/Portfolio** - Past projects and clients
- **Team/Leadership** - Key people and structure
- **Approach/Methodology** - How they work
- **Blog/News** - Recent updates and insights

## Output

Each analysis generates:
1. **AI-powered summary** with key business insights
2. **Text file** with the complete profile
3. **Console output** showing progress and results

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key (optional, for AI summaries):
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Examples

### Analyze Stripe
```bash
python generate_summary.py https://stripe.com
# Output: stripe_company_profile.txt
```

### Analyze OpenAI
```bash
python generate_summary.py https://openai.com --pages 6
# Output: openai_company_profile.txt
```

### Quick Link Analysis
```bash
python main.py https://company.com
# Shows link categorization without full analysis
```

## Use Cases

- **Pre-meeting research** - Get comprehensive company insights
- **Competitive analysis** - Understand competitor positioning
- **Due diligence** - Research potential partners/clients
- **Market research** - Analyze industry players
- **Sales preparation** - Understand prospect's business

## Tips

- Use `--pages` to limit scraping for faster results
- Use `--no-ai` if you don't have OpenAI API access
- The tool works best with well-structured company websites
- Results are saved automatically with descriptive filenames

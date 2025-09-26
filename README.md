# Multi-Agent LLM Stock Trading Simulator

This is a system where AI agents, each backed by a large language model (like GPT or Gemini), simulate real-world stock trading. Agents react to external influences: economic news, policy shifts, company reports, and global events, mirroring how real investors make decisions.

### Key Points
- Simulates real-world market environments with LLM-based trading agents.
- Agents reflect different trader personalities and strategies.
- Supports events like macroeconomic changes, policy updates, company announcements, and random shocks.
- Avoids LLM test leakage—no access to future/known market data during simulation.
- Lets users analyze how different events change trading behaviors and profits.

***

## Architecture

- **Investment Agent Module:** Agents initialized with cash, liabilities, personality (Conservative, Aggressive, etc.)
- **Transaction Module:** Handles buy/sell decisions and order settlement like real exchanges.
- **BBS Module:** Agents post and read trading tips, simulating social influence.
- **Event Module:** Injects events (daily/quarterly/special) to test agent reactions.

***

## Quick Start

1. **Setup Environment**
   ```bash
   python -m venv .venv
    Win: .venv\\Scripts\\activate
    Linux: source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   git clone https://github.com/dhh1995/PromptCoder
   cd PromptCoder
   pip install -e .
   cd ..

   git clone https://github.com/pranav-85/trading_agent
   cd trading_agent
   pip install -r requirements.txt
   ```

3. **Set API Keys**
   - For GPT:  
     ```bash
     export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
     ```
   - For Gemini:  
     ```bash
     export GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
     ```

4. **Run Simulation**
   ```bash
   python main.py --model MODEL_NAME
   ```
   - Example:  
     ```bash
     python main.py --model gpt-3.5-turbo
     ```
   - Default is `gemini-pro` if not specified.
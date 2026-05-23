# Closira AI Agent Workflow

An AI-powered customer support workflow built for Bloom Aesthetics Clinic (a simulated SMB). This agent handles inbound queries, qualifies leads, detects escalation triggers (like medical questions or complaints), and generates a structured summary at the end of the conversation.

##  Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/amolrathod7875/CLOSIRA_PROJECT.git](https://github.com/amolrathod7875/CLOSIRA_PROJECT.git)
   cd CLOSIRA_PROJECT

##  Trade-offs & Deviations

* **API Choice:** The assignment prompt suggested OpenAI or Anthropic Claude. However, due to API access constraints at the time of development, this project utilizes the **Cerebras API (llama3.1-8b)**. The code structure remains identical to standard OpenAI ChatCompletions, proving the core logic works perfectly, but inference is handled by Cerebras for speed. It is effectively a drop-in replacement.
* **Escalation Logic:** Currently, escalation relies on the LLM generating a specific string (`[ESCALATION TRIGGERED]`) based on prompt instructions. In a production environment, it would be safer to implement this using structured Tool Calling / Function Calling.
# 🧠 Agentic AI Travel Planner — India

An intelligent **multi-agent travel planning system** built using a ReAct-based Agentic AI architecture.
The system autonomously plans trips by coordinating multiple specialized agents such as route, transport, hotel, budget, and places agents.

---

## 🚀 Features

* 🧠 **Agentic AI Architecture** (ReAct: THINK → ACT → OBSERVE → REPLAN)
* 🤖 **Multi-Agent System**

  * Route Agent (distance calculation)
  * Transport Agent (cost & mode selection)
  * Hotel Agent (budget-based selection)
  * Budget Agent (dynamic allocation & reallocation)
  * Places Agent (tourist recommendations using Geoapify API)
* 📍 **Nearest Tourist Places Fetching**
* 💰 **Budget Optimization & Validation**
* 🔁 **Iterative Planning with Reasoning Logs**
* 🌐 **Streamlit UI for interactive experience**

---

 Project Structure

```
agentic-ai-travel-planner/
│
├── agents/
│   ├── budget_agent.py
│   ├── hotel_agent.py
│   ├── places_agent.py
│   ├── route_agent.py
│   ├── transport_agent.py
│
├── data/
│   ├── hotels.py
│   ├── transport.py
│
├── app.py
├── orchestrator.py
├── validator.py
├── requirements.txt
└── README.md
```

---


1. User enters:

   * Source city
   * Destination
   * Budget
   * Number of days

2. The **Orchestrator (GPT-based reasoning engine)**:

   * Decides which agent to call
   * Uses ReAct loop (THINK → ACT → OBSERVE → REPLAN)

3. Each agent performs a specific task:

   * Route → distance calculation
   * Transport → cost & time
   * Hotel → accommodation selection
   * Budget → allocation & reallocation
   * Places → nearby tourist attractions

4. Final plan is generated and validated within budget.

---

## 🌍 API Used

* **Foursquare Places API**

  * Fetches nearest tourist attractions


---

## 🔑 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/agentic-ai-travel-planner.git
cd agentic-ai-travel-planner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file:

```
GEOAPIFY_KEY=your_geoapify_api_key
OPENAI_API_KEY=your_openai_key
```

---

### 4. Run the application

```bash
streamlit run app.py
```

---

## 📊 Example Output

* Transport: Train / Flight / Bus
* Hotel: Budget-based recommendation
* Places: Nearby tourist attractions
* Budget Breakdown
* Final Validation (Within Budget / Over Budget)

---

## 🧪 Evaluation Metrics

* ✅ Budget Accuracy (within constraints)
* 🔁 Iteration Efficiency (number of planning cycles)
* 📍 Place Relevance (API + fallback quality)
* ⚙️ System Robustness (fallback handling)

---

## ⚠️ Limitations

* API dependency for place data
* No long-term memory (no learning across sessions)
* Simplified pricing model for transport

---

## 🔮 Future Improvements

* 📅 Day-wise itinerary generation
* 🧠 Memory-based learning system
* 📍 Map visualization (interactive)
* 💬 Voice-based travel assistant

---

## 👩‍💻 Author

**Deekshitha Sai Katta**
AI/ML Student | Agentic AI Project

---

## ⭐ Acknowledgement

This project is inspired by modern **Agentic AI systems and ReAct frameworks**, combining reasoning and tool usage for real-world problem solving.

---

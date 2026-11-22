# Voyagent: Agentic AI Travel Planning Assistant

Voyagent is an AI travel agent built with LangChain. It chooses flights and
hotels, finds attractions, checks the weather and estimates the budget, then
writes a day-wise itinerary with the reasons behind its choices.

## Features
- Tool-calling agent (LangChain + Groq) that decides which tools to use
- Tools: flight search, hotel recommendation, places discovery,
  live weather (Open-Meteo), budget estimation
- Day-wise itinerary, weather per day, budget breakdown and reasoning
- Streamlit interface with a downloadable itinerary

## Project structure
    data/        flights.json, hotels.json, places.json
    tools/       the five tools and their LangChain wrappers
    agent/       system prompt and agent
    app.py       Streamlit app
    tests/       tool tests
    utils.py     JSON loading helpers

## Setup
1. Python 3.10+ is required.
2. Create and activate a virtual environment:

       python -m venv venv
       venv\Scripts\activate

3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file in the project root:

       GROQ_API_KEY=your_key
       GROQ_MODEL=openai/gpt-oss-120b

## Run
- App: `streamlit run app.py`
- CLI: `python -m agent.travel_agent`
- Tests: `python -m pytest tests`

## How it works
The agent reads the request, calls the flight, hotel, places and weather tools,
then calls the budget tool and writes the final itinerary. All arithmetic is
done in Python, not by the LLM.

## Limitations
- Flight dates in the sample dataset are indicative; prices are used as given.
- If no return flight exists, the return fare is estimated as the outbound fare.
- Weather forecasts cover about 16 days ahead.
- Attractions come from the sample dataset, so some cities have few places.
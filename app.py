"""Streamlit interface for the AI Travel Planning Assistant."""
from datetime import date, timedelta

import streamlit as st

from agent.travel_agent import plan_trip
from utils import load_json

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="centered")


@st.cache_data
def get_options():
    """Read cities and per-city place types from the datasets."""
    flights = load_json("flights.json")
    places = load_json("places.json")
    cities = sorted({f["from"] for f in flights} | {f["to"] for f in flights})
    types_by_city = {}
    for place in places:
        types_by_city.setdefault(place["city"], set()).add(place["type"])
    return cities, {city: sorted(types) for city, types in types_by_city.items()}


def build_query(source, destination, start, nights, budget, interests):
    """Turn form inputs into a clear request for the agent."""
    text = (f"Plan a {nights + 1}-day, {nights}-night trip from {source} to "
            f"{destination} starting on {start}. Budget {budget} rupees.")
    if interests:
        text += f" I like {', '.join(interests)}."
    return text


st.title("✈️ AI Travel Planning Assistant")
st.caption("Tell me where you want to go and I'll plan flights, hotel, weather and a day-wise itinerary.")

cities, types_by_city = get_options()
if not cities:
    st.error("Could not load flight data. Check that the files exist in the data folder.")
    st.stop()

col1, col2 = st.columns(2)
source = col1.selectbox("From", cities, index=0)
destination = col2.selectbox("To", cities, index=min(1, len(cities) - 1))

col3, col4 = st.columns(2)
start = col3.date_input("Start date", value=date.today() + timedelta(days=3),
                        min_value=date.today(), max_value=date.today() + timedelta(days=13),
                        help="Live weather works up to about 16 days ahead.")
nights = col4.slider("Nights", 1, 6, 2)

budget = st.number_input("Budget (₹)", min_value=3000, value=25000, step=1000)
available_types = types_by_city.get(destination, [])
interests = st.multiselect("Interests", available_types,
                           help="Only attractions available in the destination are shown.")

if st.button("Plan my trip", type="primary"):
    if source == destination:
        st.warning("Source and destination must be different.")
    else:
        query = build_query(source, destination, start, nights, budget, interests)
        with st.spinner("Searching flights, hotels, places and weather..."):
            try:
                answer = plan_trip(query)
            except Exception as error:  # LLM/network errors should not crash the app
                st.error(f"Something went wrong: {error}")
                st.info("If this is a rate-limit error, wait a minute and try again.")
                st.stop()
        st.session_state["answer"] = answer
        st.session_state["title"] = f"{source}-to-{destination}"

if "answer" in st.session_state:
    st.divider()
    st.markdown(st.session_state["answer"])
    st.download_button("Download itinerary", st.session_state["answer"],
                       file_name=f"{st.session_state['title']}_itinerary.md",
                       mime="text/markdown")
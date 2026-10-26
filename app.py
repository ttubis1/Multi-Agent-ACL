import logging
from datetime import date

import streamlit as st

from prompts import USER_PROMPT_FOR_MAIN_AGENT, WEDDING_PLANNER_AGENT_PROMPT


def format_choices(choices: list[str], additional_choice: str = "") -> str:
    selected = [choice for choice in choices if choice]
    if additional_choice.strip():
        selected.append(additional_choice.strip())
    return ", ".join(selected) if selected else "No specific preference provided."


def start_new_plan() -> None:
    for key in (
        "date_preference",
        "preferred_period",
        "range_start",
        "range_end",
        "exact_date",
        "flexibility_notes",
        "budget_range",
        "preferred_areas",
        "other_area",
        "style",
        "must_haves",
        "other_must_haves",
        "dietary_needs",
        "other_dietary_needs",
        "entertainment",
        "entertainment_details",
        "beverage_policy",
        "beverage_details",
        "wedding_requirements_text",
        "wedding_plan",
    ):
        st.session_state.pop(key, None)


st.set_page_config(page_title="NYC wedding planner", page_icon=":material/favorite:")
st.title("NYC wedding planner")
st.write(
    "Share your preferences and we'll create a venue-focused wedding plan "
    "for New York City."
)

date_preference = st.selectbox(
    "How flexible are your dates?",
    ["Flexible dates", "Month or season", "Date range", "Exact date"],
    key="date_preference",
)

range_start: date | None = None
range_end: date | None = None

with st.form("wedding_requirements"):
    st.subheader("Date and budget")
    if date_preference == "Month or season":
        preferred_period = st.text_input(
            "Preferred month or season",
            placeholder="For example, October or spring 2027",
            key="preferred_period",
        )
        date_details = preferred_period.strip() or "Not specified"
    elif date_preference == "Date range":
        range_start = st.date_input(
            "Earliest preferred date",
            value=None,
            key="range_start",
        )
        range_end = st.date_input(
            "Latest preferred date",
            value=None,
            key="range_end",
        )
        date_details = (
            f"{range_start or 'No start date'} to {range_end or 'no end date'}"
        )
    elif date_preference == "Exact date":
        exact_date = st.date_input(
            "Preferred wedding date",
            value=None,
            key="exact_date",
        )
        date_details = str(exact_date) if exact_date else "Not specified"
    else:
        flexibility_notes = st.text_input(
            "Timing notes (optional)",
            placeholder="For example, avoid holiday weekends",
            key="flexibility_notes",
        )
        date_details = flexibility_notes.strip() or "Open to dates"

    budget_range = st.text_input(
        "Rough budget range (USD)",
        placeholder="For example, $50,000–$80,000",
        help="Include venue, catering, taxes, and fees.",
        key="budget_range",
    )

    st.subheader("Location and style")
    preferred_areas = st.multiselect(
        "Preferred NYC neighborhoods or areas",
        [
            "Manhattan",
            "Brooklyn",
            "Queens",
            "The Bronx",
            "Staten Island",
            "Near Central Park",
            "Waterfront",
        ],
        key="preferred_areas",
    )
    other_area = st.text_input(
        "Other preferred areas (optional)",
        placeholder="Add neighborhoods or nearby areas",
        key="other_area",
    )
    style = st.text_area(
        "Style or vibe",
        placeholder="For example, an elegant ballroom, modern loft, classic hotel, "
        "or a venue with indoor and outdoor spaces",
        key="style",
    )

    st.subheader("Venue requirements")
    must_haves = st.multiselect(
        "On-site must-haves",
        [
            "Dance floor",
            "Stage for live music",
            "Audio/visual equipment",
            "Bridal suite",
            "Wheelchair accessibility",
            "Loading dock",
            "Parking or valet",
        ],
        key="must_haves",
    )
    other_must_haves = st.text_input(
        "Other venue requirements (optional)",
        placeholder="Add any other must-haves",
        key="other_must_haves",
    )
    dietary_needs = st.multiselect(
        "Dietary considerations beyond standard options",
        [
            "Vegetarian",
            "Vegan",
            "Gluten-free",
            "Dairy-free",
            "Kosher",
            "Halal",
            "Allergy-aware service",
        ],
        key="dietary_needs",
    )
    other_dietary_needs = st.text_input(
        "Other dietary needs (optional)",
        placeholder="Describe any other restrictions",
        key="other_dietary_needs",
    )

    st.subheader("Entertainment and beverages")
    entertainment = st.selectbox(
        "Entertainment preference",
        ["DJ", "Live band", "Either; recommend the best fit", "Other"],
        key="entertainment",
    )
    entertainment_details = st.text_input(
        "Entertainment or equipment needs (optional)",
        placeholder="For example, microphones, speakers, or a lighting setup",
        key="entertainment_details",
    )
    beverage_policy = st.selectbox(
        "Beverage policy",
        [
            "Strictly dry venue",
            "Beer and wine only under the venue's license",
            "Open to other licensed beverage options",
            "Consider BYO, subject to venue restrictions",
            "No preference; recommend suitable options",
        ],
        key="beverage_policy",
    )
    beverage_details = st.text_input(
        "Beverage or BYO restrictions (optional)",
        placeholder="Add any licensing or service details",
        key="beverage_details",
    )

    submitted = st.form_submit_button(
        "Plan my wedding",
        type="primary",
        width="stretch",
    )

if submitted:
    if (
        date_preference == "Date range"
        and range_start is not None
        and range_end is not None
        and range_start > range_end
    ):
        st.error("The earliest preferred date must be on or before the latest date.")
    else:
        requirements = "\n".join(
            [
                f"Date preference: {date_preference} ({date_details})",
                "Budget (venue, catering, taxes, and fees): "
                f"{budget_range.strip() or 'Not specified'}",
                "Preferred NYC areas: "
                f"{format_choices(preferred_areas, other_area)}",
                f"Style or vibe: {style.strip() or 'Not specified'}",
                "On-site must-haves: "
                f"{format_choices(must_haves, other_must_haves)}",
                "Dietary considerations: "
                f"{format_choices(dietary_needs, other_dietary_needs)}",
                "Entertainment preference: "
                f"{entertainment}"
                f"{': ' + entertainment_details.strip() if entertainment_details.strip() else ''}",
                "Beverage policy: "
                f"{beverage_policy}"
                f"{': ' + beverage_details.strip() if beverage_details.strip() else ''}",
            ]
        )

        from agents import delegate_to_sub_agent1, delegate_to_sub_agent2
        from langchain.agents import create_agent
        from langchain.messages import HumanMessage
        from models import openai_model
        from tavily import UsageLimitExceededError

        updated_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(
            requirements=requirements
        )
        logging.info("Creating the wedding planner agent")
        wedding_planner = create_agent(
            model=openai_model,
            tools=[delegate_to_sub_agent1, delegate_to_sub_agent2],
            name="main-agent",
            system_prompt=updated_system_prompt,
        )

        logging.info("Generating a wedding plan")
        with st.spinner("Putting together your NYC wedding plan..."):
            try:
                response = wedding_planner.invoke(
                    {"messages": [HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]}
                )
            except UsageLimitExceededError as error:
                logging.exception("Tavily search usage limit was exceeded")
                st.error(
                    "The web-search service has reached its usage limit, so the "
                    "planner couldn't complete the research. Check your Tavily "
                    "account's usage and billing limits, then try again. "
                    f"Details: {error}"
                )
                st.stop()

        st.session_state["wedding_requirements_text"] = requirements
        st.session_state["wedding_plan"] = response["messages"][-1].content

if st.session_state.get("wedding_plan"):
    st.button(
        "New plan",
        on_click=start_new_plan,
        icon=":material/add:",
    )

    with st.expander("Review your requirements"):
        st.text(st.session_state["wedding_requirements_text"])

    st.subheader("Your wedding plan")
    st.write(st.session_state["wedding_plan"])

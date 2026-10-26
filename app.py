import logging
from datetime import date

import streamlit as st

from prompts import USER_PROMPT_FOR_MAIN_AGENT, WEDDING_PLANNER_AGENT_PROMPT


def format_choices(choices: list[str], additional_choice: str = "") -> str:
    selected = [choice for choice in choices if choice]
    if additional_choice.strip():
        selected.append(additional_choice.strip())
    return ", ".join(selected) if selected else "Not specified"


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
        "wedding_summary",
        "wedding_plan",
    ):
        st.session_state.pop(key, None)


def current_date_summary() -> str:
    preference = st.session_state.get("date_preference", "Flexible dates")
    if preference == "Date range":
        start = st.session_state.get("range_start")
        end = st.session_state.get("range_end")
        if start or end:
            return f"{start or 'Any date'} – {end or 'Any date'}"
        return "Date range not set"
    if preference == "Exact date":
        return str(st.session_state.get("exact_date") or "Exact date not set")
    if preference == "Month or season":
        return st.session_state.get("preferred_period") or "Month or season"
    return "Flexible dates"


st.set_page_config(
    page_title="NYC wedding planner",
    page_icon=":material/favorite:",
    layout="wide",
)
st.title("NYC wedding planner")
st.caption(
    "A thoughtful starting point for your New York celebration. "
    "Shape your brief and let your planner take it from there."
)

if st.session_state.get("wedding_plan"):
    st.button(
        "New plan",
        on_click=start_new_plan,
        icon=":material/add:",
    )

date_summary = current_date_summary()
budget_summary = st.session_state.get("budget_range", "").strip() or "Not set"
areas = st.session_state.get("preferred_areas", [])
area_summary = ", ".join(areas) if areas else "New York City"

with st.container(horizontal=True):
    st.metric(
        "Planning status",
        "Plan ready" if st.session_state.get("wedding_plan") else "Ready to plan",
        border=True,
        height="stretch",
    )
    st.metric(
        "Date",
        date_summary,
        border=True,
        height="stretch",
    )
    st.metric(
        "Budget range",
        budget_summary,
        border=True,
        height="stretch",
    )
    st.metric(
        "Location",
        area_summary,
        border=True,
        height="stretch",
    )

st.subheader("Wedding brief")
form_column, planning_column = st.columns([1.9, 1], gap="large")

with form_column:
    with st.container(border=True):
        st.caption("BASICS")
        date_preference = st.selectbox(
            "Date flexibility",
            ["Flexible dates", "Month or season", "Date range", "Exact date"],
            key="date_preference",
        )

        range_start: date | None = None
        range_end: date | None = None

        with st.form("wedding_requirements", border=False):
            if date_preference == "Month or season":
                preferred_period = st.text_input(
                    "Preferred month or season",
                    placeholder="For example, October or spring 2027",
                    key="preferred_period",
                )
                date_details = preferred_period.strip() or "Not specified"
            elif date_preference == "Date range":
                date_columns = st.columns(2)
                range_start = date_columns[0].date_input(
                    "Earliest preferred date",
                    value=None,
                    key="range_start",
                )
                range_end = date_columns[1].date_input(
                    "Latest preferred date",
                    value=None,
                    key="range_end",
                )
                date_details = (
                    f"{range_start or 'No start date'} to "
                    f"{range_end or 'no end date'}"
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

            st.caption("BUDGET AND LOCATION")
            budget_range = st.text_input(
                "Rough budget range (USD)",
                placeholder="For example, $50,000–$80,000",
                help="Include venue, catering, taxes, and fees.",
                key="budget_range",
            )
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
                placeholder=(
                    "For example, an elegant ballroom, modern loft, classic hotel, "
                    "or a venue with indoor and outdoor spaces"
                ),
                key="style",
            )

            st.caption("PRIORITIES AND GUARDRAILS")
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

            st.caption("ENTERTAINMENT AND BEVERAGES")
            preference_columns = st.columns(2)
            entertainment = preference_columns[0].selectbox(
                "Entertainment preference",
                ["DJ", "Live band", "Either; recommend the best fit", "Other"],
                key="entertainment",
            )
            beverage_policy = preference_columns[1].selectbox(
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
            entertainment_details = st.text_input(
                "Entertainment or equipment needs (optional)",
                placeholder="For example, microphones, speakers, or lighting",
                key="entertainment_details",
            )
            beverage_details = st.text_input(
                "Beverage or BYO restrictions (optional)",
                placeholder="Add any licensing or service details",
                key="beverage_details",
            )

            submitted = st.form_submit_button(
                "Plan my wedding",
                type="primary",
                icon=":material/auto_awesome:",
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
        st.session_state["wedding_requirements_text"] = requirements
        st.session_state["wedding_summary"] = {
            "date": date_details,
            "budget": budget_range.strip() or "Not specified",
            "areas": format_choices(preferred_areas, other_area),
            "style": style.strip() or "Not specified",
            "priorities": format_choices(must_haves, other_must_haves),
        }

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

        st.session_state["wedding_plan"] = response["messages"][-1].content
        st.rerun()

with planning_column:
    with st.container(border=True):
        st.subheader("Planning lens")
        summary = st.session_state.get("wedding_summary", {})
        if summary:
            st.markdown(f"**Location**  \n{summary['areas']}")
            st.markdown(f"**Date**  \n{summary['date']}")
            st.markdown(f"**Budget**  \n{summary['budget']}")
            st.markdown(f"**Style direction**  \n{summary['style']}")
            st.markdown(f"**Planning priorities**  \n{summary['priorities']}")
        else:
            st.caption(
                "Your submitted location, timing, budget, style, and priorities "
                "will appear here."
            )

    with st.container(border=True):
        st.subheader("Agent flow")
        st.markdown("**Main wedding planner**")
        st.caption("Builds a tailored plan from your wedding brief.")
        st.markdown("**Research sub-agents**")
        st.caption("Search for venue and vendor information.")
        st.markdown("**Tavily search**")
        st.caption("Retrieves current web results for the research.")
        st.markdown("**GPT-5 nano**")
        st.caption("Coordinates recommendations and the final response.")

if st.session_state.get("wedding_plan"):
    st.subheader("Your wedding plan")
    with st.container(border=True):
        st.markdown(st.session_state["wedding_plan"])
    with st.expander("Review your requirements"):
        st.text(st.session_state["wedding_requirements_text"])

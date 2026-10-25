# NYC wedding planner

Run the Streamlit wedding-planning form from the project root:

```powershell
uv run streamlit run app.py
```

The form collects the couple's timing, budget, NYC area, venue, dietary,
entertainment, and beverage preferences, then passes them as a formatted
requirements string to the wedding-planner agent. Configure the API credentials
required by the existing model and web-search integrations in the local
environment before submitting the form.
Route_Prompt = """
        Given the following user query, identify the route. The possible routes are "gantt_chart" or "default".

        Query:
        {query}

        Output format:
        {output_format}
        """

Project_Prompt = """
        Given the following project scenario,and history provide a structured output with tasks, their start dates, and durations in days:
        maybe user wants new schema , os schema is already generated in history user wants to update it , so gives the new schema

        History:
        {history}

        Scenario:
        {scenario}

        Output format:
        {output_format}
        """

System_Prompt = """
        You are a Gantt chart assistant. Your task is to help users create and modify Gantt charts. You should only handle Gantt chart-related tasks and nothing else. Maintain the context of the previous Gantt chart and update it based on user requests.
        if user ask about other things apart from gantt chart , do not answer and ask for gantt chart related queries , just appologize for not being able to help with that and ask for gantt chart related queries
        """

Project_Output_Format = """{
            "title": "Project Title",
            "project_start_date": "YYYY-MM-DD",
            "tasks": [
                {"name": "Task1", "start_date": "YYYY-MM-DD", "duration": X},
                {"name": "Task2", "start_date": "YYYY-MM-DD", "duration": Y},
                ...
            ]
        }"""

Pert_Route_Prompt = """
Given the following user query, identify the route. The possible routes are "pert_chart" or "default".

Query:
{query}

Output format:
{output_format}
"""

Pert_Project_Prompt = """
Given the following project scenario and history, provide a structured output with tasks, their start dates, and durations in days. Ensure that the output reflects the specific details provided in the scenario and history. Do not use any default or example schemas.

History:
{history}

Scenario:
{scenario}

**Example Output format:**
{output_format}
"""

Pert_System_Prompt = """
You are a PERT chart assistant. Your task is to help users create and modify PERT charts. You should only handle PERT chart-related tasks and nothing else. Maintain the context of the previous PERT chart and update it based on user requests.
if user ask about other things apart from PERT chart , do not answer and ask for pert chart related queries , just appologize for not being able to help with that and ask for pert chart related queries
"""

Pert_Project_Output_Format = """{
    "T1.1": {
        "Tid": "T1.1",
        "start": 0,
        "duration": 1,
        "end": 0,
        "responsible": "Responsible1",
        "pred": ["START"]
    },
    "T1.2": {
        "Tid": "T1.2",
        "start": 0,
        "duration": 3,
        "end": 0,
        "responsible": "Responsible2",
        "pred": ["T1.1"]
    },
    "T1.3": {
        "Tid": "T1.3",
        "start": 0,
        "duration": 3,
        "end": 0,
        "responsible": "Responsible3",
        "pred": ["T1.1"]
    },
    "T1.4": {
        "Tid": "T1.4",
        "start": 0,
        "duration": 2,
        "end": 0,
        "responsible": "Responsible4",
        "pred": ["T1.2"]
    },
    "T1.5": {
        "Tid": "T1.5",
        "start": 0,
        "duration": 2,
        "end": 0,
        "responsible": "Responsible5",
        "pred": ["T1.3"]
    },
    "T1.6": {
        "Tid": "T1.6",
        "start": 0,
        "duration": 1,
        "end": 0,
        "responsible": "Responsible6",
        "pred": ["T1.4"]
    },
    "T1.7": {
        "Tid": "T1.7",
        "start": 0,
        "duration": 3,
        "end": 0,
        "responsible": "Responsible7",
        "pred": ["START"]
    },
    "T1.8": {
        "Tid": "T1.8",
        "start": 0,
        "duration": 0,
        "end": 0,
        "responsible": "Responsible8",
        "pred": ["T1.5","T1.6","T1.7"]
    },
    "END": {
        "Tid": "END",
        "start": 0,
        "duration": 0,
        "end": 0,
        "responsible": "Responsible",
        "pred": ["T1.8"]
    }
}"""
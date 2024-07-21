import os
import base64
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime
import openai
import instructor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
from io import BytesIO
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage
from src.models.models import Project, RouteIdentification, Task
from src.Chatbot.promptTemplates import Route_Prompt, Project_Prompt, System_Prompt , Project_Output_Format

load_dotenv()



class Bot:
    def __init__(self):
        self.instructor_client = openai.OpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.environ["TOGETHER_API_KEY"],
        )
        self.instructor_client = instructor.from_openai(self.instructor_client, mode=instructor.Mode.JSON)
        
        self.together_llm = TogetherLLM(
            model="meta-llama/Llama-3-8b-chat-hf", 
            api_key=os.environ["TOGETHER_API_KEY"]
        )
        
        self.route_prompt = Route_Prompt

        self.route_output_format = """{
            "route": "gantt_chart" or "default"
        }"""
        self.project_prompt = Project_Prompt
        self.project_output_format = Project_Output_Format
   
        self.system_prompt = System_Prompt

        self.history = [ChatMessage(role="system", content=self.system_prompt)]

    def add_message(self, role: str, content: str) -> None:
        self.history.append(ChatMessage(role=role, content=content))

    def identify_route(self, query: str) -> RouteIdentification:
        response = self.instructor_client.chat.completions.create(
            model="togethercomputer/CodeLlama-34b-Instruct",
            response_model=RouteIdentification,
            messages=[
                {"role": "user", "content": self.route_prompt.format(query=query, output_format=self.route_output_format)},
            ],
        )
        return response

    def process_project_scenario(self, scenario: str) -> Project:
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in self.history]
        response = self.instructor_client.chat.completions.create(
            model="togethercomputer/CodeLlama-34b-Instruct",
            response_model=Project,
            messages=[
                {"role": "user", "content": self.project_prompt.format(history= str(history_dicts) ,  scenario=scenario, output_format=self.project_output_format)},
            ],
        )
        return response

    def create_gantt_chart(self, project: Project) -> str:
        start_date = datetime.strptime(project.project_start_date, "%Y-%m-%d")
        tasks = {task.name: (datetime.strptime(task.start_date, "%Y-%m-%d"), task.duration) for task in project.tasks}

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (task, (start, duration)) in enumerate(tasks.items()):
            ax.broken_barh([(mdates.date2num(start), duration)], (i - 0.4, 0.8), facecolors='tab:blue')

        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels(list(tasks.keys()))

        ax.xaxis_date()
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

        fig.autofmt_xdate()

        ax.set_xlabel('Date')
        ax.set_ylabel('Task')
        ax.set_title(project.title)

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64

    def handle_query(self, query: str) -> Union[str, None]:
        route = self.identify_route(query)
        if route.route == "gantt_chart":
            project = self.process_project_scenario(query)
            img_base64 = self.create_gantt_chart(project)
            img_html = f'<img src="data:image/png;base64,{img_base64}" alt="Gantt Chart">'
            self.history.append(ChatMessage(role="user", content=query))
            self.history.append(ChatMessage(role="assistant", content=f"Image generated successfully. schema is {project}"))
            return f"Gantt chart created successfully. {img_html}"
        else:
            self.history.append(ChatMessage(role="user", content=query))

            response = self.together_llm.stream_chat(self.history)
            complete_anwer = ""
            for r in response:
                complete_anwer += r.delta

            self.history.append(ChatMessage(role="assistant", content=complete_anwer))
            return complete_anwer
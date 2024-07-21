import os
import base64
from pydantic import BaseModel
from typing import List, Union, Dict, Any
from datetime import datetime
import openai
import instructor
from dotenv import load_dotenv
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage
from src.utills.utills import PertChart
from src.models.models import PertProject, RouteIdentification
from src.Chatbot.promptTemplates import Pert_Route_Prompt, Pert_Project_Prompt, Pert_System_Prompt, Pert_Project_Output_Format

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
        
        self.route_prompt = Pert_Route_Prompt

        self.route_output_format = """{
            "route": "pert_chart" or "default"
        }"""
        self.project_prompt = Pert_Project_Prompt
        self.project_output_format = Pert_Project_Output_Format
   
        self.system_prompt = Pert_System_Prompt

        self.pc = PertChart()

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

    def process_project_scenario(self, scenario: str) -> PertProject:
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in self.history]
        response = self.instructor_client.chat.completions.create(
            model="togethercomputer/CodeLlama-34b-Instruct",
            response_model=PertProject,
            messages=[
                {"role": "user", "content": self.project_prompt.format(history=str(history_dicts), scenario=scenario, output_format=self.project_output_format)},
            ],
        )
        return response

    def create_pert_chart(self, project: PertProject) -> str:
        task_list = project.Pert_Dict
        task_list = self.pc.calculate_values(task_list)
        self.pc.create_pert_chart(task_list)
        
        with open("Pert_image.png", "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return img_base64

    def handle_query(self, query: str) -> Union[str, None]:
        route = self.identify_route(query)
        if route.route == "pert_chart":
            project = self.process_project_scenario(query)
            print(project)
            img_base64 = self.create_pert_chart(project)
            img_html = f'<img src="data:image/png;base64,{img_base64}" alt="PERT Chart">'
            self.history.append(ChatMessage(role="user", content=query))
            self.history.append(ChatMessage(role="assistant", content=f"Image generated successfully. schema is {project}"))
            return f"PERT chart created successfully. {img_html}"
        else:
            self.history.append(ChatMessage(role="user", content=query))
            # Convert ChatMessage objects to dictionaries
            response = self.together_llm.stream_chat(self.history)
            complete_anwer = ""
            for r in response:
                complete_anwer += r.delta

            self.history.append(ChatMessage(role="assistant", content=complete_anwer))
            return complete_anwer
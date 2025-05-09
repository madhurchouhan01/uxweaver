from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel
from typing import List

class ManagerOutput(BaseModel):
    page_title: str
    description : str
    pain_point : str
    technical_rationale : str
    user_rationale : str

class ManagerOutputList(BaseModel):
    core_pages : List[ManagerOutput]


@CrewBase
class ManagerCrew:
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/manager_agents.yaml"
    tasks_config = "config/manager_tasks.yaml"

    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manager_agent"], 
        )

    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config["manager_task"],  
            output_json=ManagerOutputList,
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,

        )

class Component(BaseModel):
    name: str
    description: str


class DesignStrategy(BaseModel):
    component: str
    strategy: str
    rationale: str


class InformationFlow(BaseModel):
    description: str
    sequence: List[str]


class UserStory(BaseModel):
    text: str  
    alignment: str

class TeamLeadOutput(BaseModel):
    components: List[Component]
    design_strategies: List[DesignStrategy]
    information_flow: InformationFlow
    user_story: UserStory

@CrewBase
class TeamLeaderCrew:
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/team_leader_agents.yaml"
    tasks_config = "config/team_leader_tasks.yaml"

    @agent
    def team_leader_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["team_leader_agent"], 
        )

    @task
    def team_leader_task(self) -> Task:
        return Task(
            config=self.tasks_config["team_leader_task"],  
            output_pydantic=TeamLeadOutput,
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            
        )
@CrewBase
class IADeveloperCrew:
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/ia_developer_agents.yaml"
    tasks_config = "config/ia_developer_tasks.yaml"

    @agent
    def ia_developer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ia_developer_agent"], 
        )

    @task
    def ia_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config["ia_developer_task"],  
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class UFDeveloperCrew:
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/uf_developer_agents.yaml"
    tasks_config = "config/uf_developer_tasks.yaml"

    @agent
    def uf_developer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["uf_developer_agent"], 
        )

    @task
    def uf_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config["uf_developer_task"],  
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

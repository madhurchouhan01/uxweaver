from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from uxweaver_flow.crews.uxweaver_crew.instructions_crew import ManagerCrew, TeamLeaderCrew, DeveloperCrew

req = '''

Sounds good, Sarah! Do we have a rough idea of the main features the app needs? Yep, here's what I have so far: User login/authentication Inventory dashboard (view/edit stock levels) Add/remove items Activity logs Admin panel for managing user roles Got it. Are we storing data in our existing SQL database, or setting up something new? Let’s use the existing SQL database for now. We can reassess if performance becomes an issue. Any constraints on the UI? Or should I come up with a fresh design? We want to keep it consistent with our internal tools — minimalistic and responsive. I’ll share our style guide in a bit. Sarah, do we have a deadline in mind? We’re aiming for an MVP in 6 weeks. I’ll draft a timeline and break down the milestones by tomorrow. Great. I’ll start drafting the API endpoints based on the features you listed. I’ll share initial wireframes by end of this week. Perfect. I’ll create a shared doc to track progress and decisions. Thanks, everyone! convert this in user requirements

'''
class RequirementState(BaseModel):
    requirements : str = req
    instructions : str = ""
    strategies   : str = ""
    mermaids     : str = ""

class MainFlow(Flow[RequirementState]):

    @start()
    def get_inputs(self):
        print("input completed ✨")

    @listen(get_inputs)
    def management(self):
        print("Creating Instructions from Raw Requirements...")
        result = (
            ManagerCrew()
            .crew()
            .kickoff(inputs={"requirements": self.state.requirements})
        )

        self.state.instructions = result.raw
        print("Instructions generated 🚀\n", result.raw)

    @listen(management)
    def team_leader(self):
        print("Creating Strategies for Mermaid...")
        result = (
            TeamLeaderCrew()
            .crew()
            .kickoff(inputs={"instructions": self.state.instructions})
        )

        self.state.strategies = result.raw
        print("Strategy generated 🚀\n", result.raw)

    @listen(team_leader)
    def developer(self):
        print("Creating Mermaid Code for Info Architecture and User Flow...")
        result = (
            DeveloperCrew()
            .crew()
            .kickoff(inputs={"strategies": self.state.strategies})
        )

        self.state.mermaids = result.raw
        print("Mermaid generated 🚀\n", result.raw)
    def end(self):
        print("Well done ☑️✅💫✨⭐")

def kickoff():
    poem_flow = MainFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = MainFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

# streamlit_app.py

import streamlit as st
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

from crews.uxweaver_crew.instructions_crew import (
    ManagerCrew,
    TeamLeaderCrew,
    DeveloperCrew,
)

# ------------------------
# Pydantic State Container
# ------------------------

class RequirementState(BaseModel):
    requirements: str = ""
    instructions: str = ""
    strategies: str = ""
    mermaids: str = ""


# ------------------------
# Flow Definition
# ------------------------

class MainFlow(Flow[RequirementState]):
    @start()
    def get_inputs(self):
        st.success("Requirements input received ✅")
        print("Requirements input received : ", self.state.requirements)
        print("Nothing recievedd ")
    @listen(get_inputs)
    def management(self):
        st.info("🧠 Generating Instructions...")
        result = (
            ManagerCrew()
            .crew()
            .kickoff(inputs={"requirements": self.state.requirements})
        )
        self.state.instructions = result.raw
        st.success("Instructions created!")

    @listen(management)
    def team_leader(self):
        st.info("📋 Generating Strategy...")
        result = (
            TeamLeaderCrew()
            .crew()
            .kickoff(inputs={"instructions": self.state.instructions})
        )
        self.state.strategies = result.raw
        st.success("Strategy generated!")

    @listen(team_leader)
    def developer(self):
        st.info("🎨 Generating Mermaid Diagram...")
        result = (
            DeveloperCrew()
            .crew()
            .kickoff(inputs={"strategies": self.state.strategies})
        )
        self.state.mermaids = result.raw
        st.success("Mermaid code ready!")

    def end(self):
        st.balloons()
        st.success("🎉 Flow completed successfully!")


# ------------------------
# Streamlit UI
# ------------------------

st.set_page_config(page_title="UXWeaver – Requirement Flow", layout="wide")
st.title("📐 UXWeaver – Convert Requirements to Diagrams")

default_req = '''Sounds good, Sarah! Do we have a rough idea of the main features...'''

requirements_input = st.text_area("✍️ Paste Raw Requirements", value=default_req, height=300)
print(RequirementState)
if st.button("Run UXWeaver Flow 🚀"):
    print("something isnt right here ..... ")
    state = RequirementState(requirements=requirements_input)
    print(f"It is requirements in the state {state.requirements}")
    flow = MainFlow()
    flow.kickoff()

    # Show Outputs
    st.subheader("📄 Instructions")
    st.code(state.instructions, language="markdown")

    st.subheader("📊 Strategy")
    st.code(state.strategies, language="markdown")

    st.subheader("🧬 Mermaid Diagram Code")
    st.code(state.mermaids, language="mermaid")

    # Optional Mermaid Renderer using streamlit-mermaid
    try:
        from streamlit_mermaid import mermaid
        st.subheader("🔍 Mermaid Diagram Preview")
        mermaid(state.mermaids)
    except ImportError:
        st.warning("Install `streamlit-mermaid` to render diagram preview.")

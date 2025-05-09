import streamlit as st
from streamlit_mermaid import st_mermaid
from PyPDF2 import PdfReader
import json
from PIL import Image
import io
import sys
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

from crews.uxweaver_crew.instructions_crew import (
    ManagerCrew,
    TeamLeaderCrew,
    IADeveloperCrew,
    UFDeveloperCrew,
)
from tools.extract_conversation_from_slack import find_chats_from_json
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="UXWeaver – Requirement Flow")
st.title("📐 UXWeaver – Convert Requirements to Diagrams")

# ------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               MultiModal Inputs
# ------------------------------------------------------------------------------------------------------------------------------------------------
combined_input = ""

st.markdown("## 📥 Input Requirements")
input_text = st.text_area("✍️ **Text Input**", height=200)
# -- Append Text
if input_text.strip():
    combined_input += "\n" + input_text.strip()

input_pdf = st.file_uploader("## 📄 **Upload PDF**", type=["pdf"])
# -- Extract from PDF
if input_pdf is not None:
    reader = PdfReader(input_pdf)
    combined_input += "\nPDF Content".join(page.extract_text() for page in reader.pages if page.extract_text())

input_json = st.file_uploader("🧾 **Upload JSON**", type=["json"])
# -- Extract from JSON
if input_json is not None:
    try:
        json_content = json.load(input_json)
        chats = find_chats_from_json(json_content)
        combined_input += "\nSlack Chats" + chats
    except Exception as e:
        st.error(f"Error reading JSON: {e}")

input_image = st.file_uploader("🖼️ **Upload Image**", type=["png", "jpg", "jpeg"])
# -- Image placeholder (no OCR implemented yet)
if input_image is not None:
    combined_input += "\n[Image uploaded but OCR is not implemented]"

if not combined_input.strip():
    st.error("🚨 Please provide at least one form of input: Text, PDF, JSON, or Image.")
    st.stop()

# Display the final input used
st.success("✅ Input collected from selected source(s).")
requirements_input = st.text_area("📄 Final Combined Input", value=combined_input, height=300, key="final_input", disabled=True)

# ------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               Pydantic State Container
# ------------------------------------------------------------------------------------------------------------------------------------------------
class GlobalState:
    gbl_requirements: str = ""
    gbl_instructions: str = ""
    gbl_strategies: str = ""
    gbl_ia_mermaids: str = ""
    gbl_uf_mermaids: str = ""
class RequirementState(BaseModel):
    requirements: str = requirements_input
    instructions: str = ""
    strategies: str = ""
    ia_mermaids: str = ""
    uf_mermaids: str = ""
    manager_ouput : dict = {}
# ------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               Flow Definitions
# ------------------------------------------------------------------------------------------------------------------------------------------------

class MainFlow(Flow[RequirementState]):      
    @start()
    def get_inputs(self):
        st.success("Requirements input received ✅")
        print("Requirements input received : ", self.state.requirements)

    @listen(get_inputs)
    def management(self):   
        st.info("🧠 Generating Instructions...")
        result = (
            ManagerCrew()
            .crew()
            .kickoff(inputs={"requirements": self.state.requirements})
        )
        print(type(result.raw))
        print(result.raw)
        
        self.state.manager_ouput = json.loads(result.raw)
        print("Json type in manager : ", type(self.state.manager_ouput))
        GlobalState.gbl_instructions = result.raw
        st.success("Instructions created!")
        st.write(result.raw)

    @listen(management)
    def team_leader(self):
        st.info("📋 Generating Strategy...")
        
        # Convert each page into a separate dictionary with page_info key
        pages_as_dicts = [{"page_info": page} for page in self.state.manager_ouput["core_pages"]]
        
        result = (
            TeamLeaderCrew()
            .crew()
            .kickoff_for_each(inputs=pages_as_dicts)
        )
        print(f"Result of Kickoff for each 🚀🚀{result}")
        self.state.strategies = result
        GlobalState.gbl_strategies = result
        st.success("Strategy generated!")
        exit()

    @listen(team_leader)
    def ia_developer(self):
        st.info("🎨 Generating Mermaid for IA Diagram...")
        result = (
            IADeveloperCrew()
            .crew()
            .kickoff(inputs={"strategies": self.state.strategies})
        )
        self.state.ia_mermaids = result.raw
        GlobalState.gbl_ia_mermaids = result.raw
        st.success("IA Mermaid code ready!")

    @listen(team_leader)
    def uf_developer(self):
        st.info("🎨 Generating Mermaid for UserFlow Diagram...")
        result = (
            UFDeveloperCrew()
            .crew()
            .kickoff(inputs={"strategies": self.state.strategies})
        )
        self.state.uf_mermaids = result.raw
        GlobalState.gbl_uf_mermaids = result.raw
        st.success("UserFlow Mermaid code ready!")

    def end(self):
        st.balloons()
        st.success("🎉 Flow completed successfully!")


# # ------------------------------------------------------------------------------------------------------------------------------------------------
# #                                                               Streamlit UI
# # ------------------------------------------------------------------------------------------------------------------------------------------------
if st.button("Run UXWeaver Flow 🚀"):
    flow = MainFlow()
    flow.kickoff()
        
    st.subheader("📄 Instructions")
    st.code(GlobalState.gbl_instructions, language="markdown", height=500)

    st.subheader("📊 Strategy")
    st.code(GlobalState.gbl_strategies, language="markdown", height=500)

    st.subheader("🧬 IA Mermaid Diagram Code")
    st.code(GlobalState.gbl_ia_mermaids, language="ia_mermaid", height=500)

    st.subheader("🧬 IA Mermaid Diagram Code")
    st.code(GlobalState.gbl_uf_mermaids, language="uf_mermaid", height=500)

    try:
        st.subheader("🔍 Information Architecture    Diagram ")
        st_mermaid(GlobalState.gbl_ia_mermaids, show_controls=False)

        st.subheader("🔍 User Flow Diagram ")
        st_mermaid(GlobalState.gbl_uf_mermaids, show_controls=False)

    except ImportError:
        st.warning("Install `streamlit-mermaid` to render diagram preview.")

# import streamlit as st
# from streamlit_mermaid import st_mermaid
# from PyPDF2 import PdfReader
# import json
# from PIL import Image
# import io
# import sys
# import os
# from pydantic import BaseModel
# from crewai.flow import Flow, listen, start
# import google.generativeai as genai

# from crews.uxweaver_crew.instructions_crew import (
#     ManagerCrew,
#     TeamLeaderCrew,
#     IADeveloperCrew,
#     UFDeveloperCrew,
# )
# from tools.extract_conversation_from_slack import find_chats_from_json

# # Configure Google Generative AI with API key
# # In production, use environment variables for API keys
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAiKsAg5rMeMluMi2khVbzTunKbTEeaoCo")
# genai.configure(api_key=GEMINI_API_KEY)

# # Initialize the Gemini vision model
# gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# def analyze_image_with_gemini(image, text_context=""):
#     """Process image using Google's Gemini model with text context"""
#     # Prompt for image analysis
#     prompt = """
#     You are UXWeaver, an AI agent embedded within the FeatureFlow platform. Your goal is to assist UX designers by transforming visual input into structured UX artifacts.
    
#     Please analyze this image (sketch/whiteboard/mockup) and extract:
#     1. User goals: What users want to accomplish
#     2. Pain points: User frustrations, blockers, or inefficiencies
#     3. Tasks: Actions or workflows users are trying to complete
#     4. System actions: How the system responds to user behavior
#     5. UX structure: Navigation, screens, sections, flows
    
#     Additional context from text requirements is provided below (if any):
#     {text_context}
    
#     Format your response as structured insights that can be integrated with other UX requirements.
#     """
    
#     formatted_prompt = prompt.format(text_context=text_context)
    
#     try:
#         # Generate response from the model
#         response = gemini_model.generate_content([formatted_prompt, image])
#         return response.text
#     except Exception as e:
#         return f"Error analyzing image: {str(e)}"

# # Page configuration
# st.set_page_config(page_title="UXWeaver – Requirement Flow")
# st.title("📐 UXWeaver – Convert Requirements to Diagrams")

# # ------------------------------------------------------------------------------------------------------------------------------------------------
# #                                                               MultiModal Inputs
# # ------------------------------------------------------------------------------------------------------------------------------------------------
# combined_input = ""

# st.markdown("## 📥 Input Requirements")
# input_text = st.text_area("✍️ **Text Input**", height=200)
# # -- Append Text
# if input_text.strip():
#     combined_input += "\n" + input_text.strip()

# input_pdf = st.file_uploader("## 📄 **Upload PDF**", type=["pdf"])
# # -- Extract from PDF
# if input_pdf is not None:
#     reader = PdfReader(input_pdf)
#     combined_input += "\nPDF Content: " + " ".join(page.extract_text() for page in reader.pages if page.extract_text())

# input_json = st.file_uploader("🧾 **Upload JSON**", type=["json"])
# # -- Extract from JSON
# if input_json is not None:
#     try:
#         json_content = json.load(input_json)
#         chats = find_chats_from_json(json_content)
#         combined_input += "\nSlack Chats: " + chats
#     except Exception as e:
#         st.error(f"Error reading JSON: {e}")

# # Image handling with preview
# input_image = st.file_uploader("🖼️ **Upload Image**", type=["png", "jpg", "jpeg"])
# image_analysis_result = ""

# if input_image is not None:
#     # Display the uploaded image
#     image = Image.open(input_image)
#     st.image(image, caption="Uploaded Image", use_column_width=True)
    
#     # Process the image with Gemini
#     with st.spinner("Analyzing image with AI..."):
#         # Pass current text context to help with image analysis
#         image_analysis_result = analyze_image_with_gemini(image, input_text)
#         st.info("✅ Image analyzed successfully")
        
#     # Display image analysis results
#     st.subheader("Image Analysis Results")
#     st.write(image_analysis_result)
    
#     # Add image analysis to combined input
#     combined_input += "\n\nImage Analysis Results:\n" + image_analysis_result

# if not (combined_input.strip() or image_analysis_result):
#     st.error("🚨 Please provide at least one form of input: Text, PDF, JSON, or Image.")
#     st.stop()

# # Display the final input used
# st.success("✅ Input collected from selected source(s).")
# requirements_input = st.text_area("📄 Final Combined Input", value=combined_input, height=300, key="final_input", disabled=True)

# # ------------------------------------------------------------------------------------------------------------------------------------------------
# #                                                               Pydantic State Container
# # ------------------------------------------------------------------------------------------------------------------------------------------------
# class GlobalState:
#     gbl_requirements: str = ""
#     gbl_instructions: str = ""
#     gbl_strategies: str = ""
#     gbl_ia_mermaids: str = ""
#     gbl_uf_mermaids: str = ""
# class RequirementState(BaseModel):
#     requirements: str = requirements_input
#     instructions: str = ""
#     strategies: str = ""
#     ia_mermaids: str = ""
#     uf_mermaids: str = ""

# # ------------------------------------------------------------------------------------------------------------------------------------------------
# #                                                               Flow Definitions
# # ------------------------------------------------------------------------------------------------------------------------------------------------

# class MainFlow(Flow[RequirementState]):      
#     @start()
#     def get_inputs(self):
#         st.success("Requirements input received ✅")
#         print("Requirements input received : ", self.state.requirements)

#     @listen(get_inputs)
#     def management(self):   
#         st.info("🧠 Generating Instructions...")
#         result = (
#             ManagerCrew()
#             .crew()
#             .kickoff(inputs={"requirements": self.state.requirements})
#         )
#         print(type(result.raw))
#         print(result.raw)
        
#         self.state.instructions = result.raw
#         GlobalState.gbl_instructions = result.raw
#         st.success("Instructions created!")
#         st.write(result.raw)
#         exit()

#     @listen(management)
#     def team_leader(self):
#         st.info("📋 Generating Strategy...")
#         result = (
#             TeamLeaderCrew()
#             .crew()
#             .kickoff(inputs={"instructions": self.state.instructions})
#         )
#         self.state.strategies = result.raw
#         GlobalState.gbl_strategies = result.raw
#         st.success("Strategy generated!")

#     @listen(team_leader)
#     def ia_developer(self):
#         st.info("🎨 Generating Mermaid for IA Diagram...")
#         result = (
#             IADeveloperCrew()
#             .crew()
#             .kickoff(inputs={"strategies": self.state.strategies})
#         )
#         self.state.ia_mermaids = result.raw
#         GlobalState.gbl_ia_mermaids = result.raw
#         st.success("IA Mermaid code ready!")

#     @listen(team_leader)
#     def uf_developer(self):
#         st.info("🎨 Generating Mermaid for UserFlow Diagram...")
#         result = (
#             UFDeveloperCrew()
#             .crew()
#             .kickoff(inputs={"strategies": self.state.strategies})
#         )
#         self.state.uf_mermaids = result.raw
#         GlobalState.gbl_uf_mermaids = result.raw
#         st.success("UserFlow Mermaid code ready!")

#     def end(self):
#         st.balloons()
#         st.success("🎉 Flow completed successfully!")


# # ------------------------------------------------------------------------------------------------------------------------------------------------
# #                                                               Streamlit UI
# # ------------------------------------------------------------------------------------------------------------------------------------------------
# if st.button("Run UXWeaver Flow 🚀"):
#     flow = MainFlow()
#     flow.kickoff()
        
#     st.subheader("📄 Instructions")
#     st.code(GlobalState.gbl_instructions, language="markdown", height=500)

#     st.subheader("📊 Strategy")
#     st.code(GlobalState.gbl_strategies, language="markdown", height=500)

#     st.subheader("🧬 IA Mermaid Diagram Code")
#     st.code(GlobalState.gbl_ia_mermaids, language="ia_mermaid", height=500)

#     st.subheader("🧬 UF Mermaid Diagram Code")
#     st.code(GlobalState.gbl_uf_mermaids, language="uf_mermaid", height=500)

#     try:
#         st.subheader("🔍 Information Architecture Diagram")
#         st_mermaid(GlobalState.gbl_ia_mermaids, show_controls=False)

#         st.subheader("🔍 User Flow Diagram")
#         st_mermaid(GlobalState.gbl_uf_mermaids, show_controls=False)

#     except ImportError:
#         st.warning("Install `streamlit-mermaid` to render diagram preview.")

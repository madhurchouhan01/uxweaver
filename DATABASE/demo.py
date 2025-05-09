import google.generativeai as genai
import json
 
# Configure Gemini
genai.configure(api_key="AIzaSyAiKsAg5rMeMluMi2khVbzTunKbTEeaoCo")
model = genai.GenerativeModel("gemini-1.5-flash")
 
# Sample input
input_data = {
    "pages": [
        {
            "page": "Dashboard",
            "pain_point": "Agents need a quick overview of their active listings, upcoming appointments, and important communications.",
            "solution": "Displays key metrics, upcoming appointments, recent messages, and a summary of active listings, providing a centralized hub for managing daily tasks."
        },
        {
            "page": "Property Listing Creation",
            "pain_point": "Agents spend too much time manually creating listings across multiple platforms, leading to inconsistencies and missed opportunities.",
            "solution": "A streamlined form with guided input fields, automated data validation, and support for rich media (photos, videos, virtual tours) to quickly and accurately create listings."
        },
        {
            "page": "Property Listing Management",
            "pain_point": "Agents struggle to efficiently update listing details, track viewings, and manage inquiries across multiple properties.",
            "solution": "Allows agents to easily edit existing listings, track viewing schedules, manage inquiries, and see listing performance data in a centralized location."
        },
        {
            "page": "Calendar/Scheduling",
            "pain_point": "Scheduling viewings often involves multiple back-and-forth communications, leading to wasted time and missed appointments.",
            "solution": "Integrated calendar allowing agents to manage appointments, send automated reminders, and provide buyers with convenient self-scheduling options through availability slots."
        },
        {
            "page": "Messaging/Communication",
            "pain_point": "Agents need a reliable way to communicate with clients and colleagues without relying on external messaging apps.",
            "solution": "A built-in messaging system for secure, real-time communication with clients and colleagues"
        }
    ]
}
 
# Prompt template
prompt_template = """
You are a product strategist. For the given feature, break it down into sub-components within each page (list each one briefly),
and then propose a design strategy for each sub-component to solve the stated pain point.
 
Input Context: {input_context}
Feature: {feature}
Pain Point: {pain_point}
 
Respond strictly in this JSON format:
 
{{
   "components": [
     {{
       "name": "String component name",
       "description": "String describing the component’s purpose"
     }}
   ],
   "design_strategies": [
     {{
       "component": "String component name",
       "strategy": "String describing design approach to address pain point",
       "rationale": "String explaining alignment with pain point and context"
     }}
   ],
   "information_flow": {{
     "description": "String describing data exchange or dependencies",
     "sequence": ["Array of steps or interactions between components"]
   }},
   "user_story": {{
     "text": "String in format: 'As a [user], I want [functionality], so that [benefit]'",
     "alignment": "String explaining how it addresses the pain point"
   }}
}}
"""
 
# Collect results
output_json = {}
 
for page in input_data["pages"]:
    feature = page["page"]
    pain_point = page["pain_point"]
    input_context = page["solution"]
 
    prompt = prompt_template.format(
        input_context=input_context,
        feature=feature,
        pain_point=pain_point
    )
 
    try:
        response = model.generate_content(prompt)
        json_response = json.loads(response.text.strip())
        output_json[feature] = json_response
 
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON for feature: {feature}")
        ("Raw response:\n", response.text)
    except Exception as ex:
        print(f"[ERROR] Unexpected issue for feature: {feature}")
        print(str(ex))
 
# Print structured output
print(json.dumps(output_json, indent=2))
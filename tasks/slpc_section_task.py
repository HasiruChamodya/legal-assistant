# slpc_section_task.py

from crewai import Task
from agents.slpc_section_agent import slpc_section_agent
from tasks.case_intake_task import case_intake_task

slpc_section_task = Task(
    agent=slpc_section_agent,
    context=[case_intake_task],
    description=(
        "You are provided with the structured legal context generated from the previous task.\n\n"
        "Your job is to identify and retrieve the most relevant sections from the Sri Lankan Penal Code (SLPC) "
        "that apply to this legal issue. Use your tool to search and extract the top 3 most relevant SLPC sections.\n\n"
        "Return the results in clean JSON format with the following fields:\n"
        "- `section`\n"
        "- `section_title`\n"
        "- `chapter`\n"
        "- `chapter_title`\n"
        "- `content`"
    ),
    expected_output=(
        "```json\n"
        "[\n"
        "  {\n"
        "    \"section\": \"SLPC Section 365\",\n"
        "    \"section_title\": \"Kidnapping or abducting with intent to murder\",\n"
        "    \"chapter\": \"Chapter XVI\",\n"
        "    \"chapter_title\": \"Of Offences Affecting the Human Body\",\n"
        "    \"content\": \"Whoever kidnaps or abducts any person...\"\n"
        "  },\n"
        "  { ... },\n"
        "  { ... }\n"
        "]\n"
        "```"
    )
)

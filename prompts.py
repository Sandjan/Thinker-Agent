prompts = {
    1: """Read the following text and reflect freely on it. Write down all thoughts, associations, and first impressions that come to mind.
Let your mind wander and capture every aspect that strikes you – including seemingly minor details, emotions, or connections.
Your response should be a maximum of 500 words.
Text:
---
{0}
---

Start your output with `### FREE_REFLECTION ###`.""",

    2: """Based on the following free reflection, formulate the user's core problem or key question in no more than two sentences.

Free Reflection:
---
{0}
---

Start your output with `### CORE_PROBLEM ###`.""",

    3: """Based on this core problem, formulate 4–5 open-ended questions to clarify the user's personal values, goals, fears, and boundaries.

Core Problem:
---
{0}
---

Start your output with `### QUESTIONS ###`.""",

    4: """Summarize the following answers into a "Priorities Profile". Extract the key goals, fears, and non-negotiables in 3–5 sentences.

Answers:
---
{0}
---

Start your output with `### PROFILE ###`.""",

    5: """Based on the free reflection and original text, systematically explore all relevant dimensions of the problem. 
Consider emotional, practical, social, temporal, financial, and personal aspects. Write 2–3 concrete points for each dimension.

Free Reflection:
---
{0}
---
Original Text:
---
{1}
---

Start your output with `### DIMENSION_EXPLORATION ###`.""",

    6: """From the dimension exploration and original text, extract all individual statements that could serve as arguments for or against a possible decision.
List each point on a separate line.

Dimension Exploration:
---
{0}
---
Original Text:
---
{1}
---

Start your output with `### RAW_ARGUMENTS ###`.""",

    7: """Categorize each argument in the following list. Write "[Pro]" or "[Con]" in front of each argument.

List of Arguments:
---
{0}
---

Start your output with `### CATEGORIZED_ARGUMENTS ###`.""",

    8: """Identify all individuals or groups (e.g., family, team, friends) affected by the situation or decision. 
Use both the original text and the dimension exploration.

Original Text:
---
{0}
---
Dimension Exploration:
---
{1}
---

Start your output with `### STAKEHOLDERS ###`.""",

    9: """Sort the following arguments by time horizon.
Create two lists: one for short-term impacts (within the next 6 months) and one for long-term consequences.

Arguments:
---
{0}
---

Start your output with `### TIME_HORIZONS ###`.""",

    10: """Analyze the free reflection, the original text, and the user's answers.
List 3–5 implicit assumptions that shape the user's thinking.

Free Reflection:
---
{0}
---
Original Text:
---
{1}
---
User Answers:
---
{2}
---

Start your output with `### ASSUMPTIONS ###`.""",

    11: """Create a final Markdown table ("Argument", "Type", "Weight (1–10)", "Justification"). Use the categorized arguments. The weighting must strictly reflect the Priorities Profile. Justify the weight with reference to the priorities.

Categorized Arguments:
---
{0}
---
Priorities Profile:
---
{1}
---

Start your output with `### FINAL_ANALYSIS ###`.""",

    12: """Based on the final analysis, uncovered assumptions, and dimension exploration, develop 4–6 different, concrete courses of action or next steps. Be creative and consider unconventional solutions. Do not evaluate them yet.

Final Analysis:
---
{0}
---
Assumptions:
---
{1}
---
Dimension Exploration:
---
{2}
---

Start your output with `### OPTIONS ###`.""",

    13: """Evaluate each of these action options in terms of how well it aligns with the user's priorities profile. Provide a detailed assessment for each option (e.g., "Strong alignment with Goal X, but overlooks Fear Y, moderate feasibility").

Options:
---
{0}
---
Priorities Profile:
---
{1}
---

Start your output with `### EVALUATION ###`.""",

    14: """Finally, based on your previous analyses, what would you recommend to the user?
Please give clear recommendations as buttelpoints that get to the point!
Your recommendations should be distributed across 3 categories:
“experimental and innovative”, “pragmatic recommendations for action”, “decision-making aids”
Give reasons for your recommendations.
The recommendations should be aimed directly at the user.
Conclude with some final strategic thoughts based on your recommendations.

Your analysis so far:
---
{0}
---
The options you have considered so far:
---
{1}
---
Your time horizon analysis:
---
{2}
---

Start your output with `### RECOMMENDATIONS ###`."""
}

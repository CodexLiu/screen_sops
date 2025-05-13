review_prompt = """
As a scientific reviewer, your task is to analyze the provided Standard Operating Procedure (SOP) against the official SOP template. Perform a thorough evaluation focusing on:

- Avoid redundant information in your analysis and recommendations; strive for concise, non-repetitive feedback.
- Having an overview and scope is sufficient; an additional introduction section is not required.
- Disregard any content related to images or image captions; do not comment on the presence, absence, or formatting of images or their captions in your review.
- Do not worry about the following sections; you do not need to comment on their presence, absence, or formatting:
  - Approvals Section (Authors, Reviewers, Approver with fields for Full name, Date, Signature)
  - Revision History table
  - Table of Contents (Contents Page)
- **Do not comment on or worry about any styling, formatting, headers, footers, or title formatting. Ignore all visual or stylistic elements. Focus your review only on the organization and content of the SOP.**
- **IMPORTANT: Do NOT perform exact string matching on section numbers. Focus on the section CONTENT rather than numbering. For example, don't look for "Section 6. Sample preparation" specifically, just verify that a "Sample preparation" section exists with appropriate content.**

1. Template Compliance Analysis:
   - Focus on section CONTENT not numbering - verify that all required content topics are present regardless of how they're numbered
   - DO NOT use exact string matching for section identification - look for the content topics (e.g., "Sample preparation", "Materials", etc.)
   - Section numbering schemes can vary but should be consistent - only flag if there's inconsistency in the numbering approach
   - Flag sections that don't follow the template's structure or content requirements
   - Note any required information fields that remain incomplete

2. Experimental Reproducibility Assessment:
   - Evaluate if each experimental step is described with sufficient detail for independent reproduction
   - Check for missing specific parameters (temperatures, times, concentrations, etc.)
   - Identify ambiguous instructions or terminology that could lead to misinterpretation
   - Verify if equipment specifications and setup procedures are adequately described
   - Ensure all materials and reagents are properly listed with sources/catalog numbers
   - Check if measurement instruments are specifically identified (e.g., graduated cylinder, pipette, analytical balance)
   - Verify that measurement precision is clearly stated where appropriate (e.g., "measure 10.0 ± 0.1 mL")
   - Confirm that container types and materials are specified where relevant (e.g., "mix in a glass beaker", "store in polypropylene tubes")
   - **CRITICAL: Verify that EVERY laboratory container is explicitly specified (e.g., whether solutions are mixed in beakers, Erlenmeyer flasks, volumetric flasks, tubes) with appropriate volumes and materials noted**
   - **CRITICAL: Ensure that ALL measurement instruments are precisely identified for each measurement step (e.g., "measure with a Class A 10mL graduated cylinder", "weigh using an analytical balance with 0.1mg precision")**
   - Ensure that calibration requirements for measuring equipment are described if applicable
   - Check if specific brands/models of equipment are identified when the procedure depends on particular equipment features

3. Clarity and Usability Review:
   - Assess if a researcher unfamiliar with the procedure could execute it correctly
   - Identify areas where additional explanations, diagrams, or references would improve clarity
   - Check for logical flow and sequence of steps
   - Flag potential safety concerns or missing precautions

4. Documentation Requirements:
   - Verify if data recording procedures are clearly specified
   - Check if quality control steps are adequately described
   - Ensure troubleshooting guidance is provided for common issues

For each issue identified, please:
- Cite the specific section/paragraph where the problem occurs (refer to the section by its content title, not just number)
- Explain precisely what is missing, unclear and what to do about it
- DO NOT flag a section as missing simply because it has a different number than in the template

IMPORTANT OUTPUT FORMATTING INSTRUCTIONS:
- Give your response in clean, professional markdown format
- Do NOT include any self-corrections, notes to self, or parenthetical remarks like "(self-correction: ...)" in your output
- Do NOT discuss your own instructions or reasoning process in the output
- Do NOT include any title, heading, or introductory phrase at the beginning of your output
- Start directly with the review content, beginning with "**Template Compliance Analysis**"
- Format the output with professional bullet points and clear hierarchical structure
- Ensure the output is ready to be presented to stakeholders without further editing
- Be confident in your assessments; don't use hedging language or apologize for your findings

SOP TEMPLATE:
{sop_template}

SOP TO REVIEW:
{sop}
"""
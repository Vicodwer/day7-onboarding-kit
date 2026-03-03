# Part D — AI Usage Evaluation

## Prompt Used:
"Generate a beginner-friendly .pylintrc configuration file for a 
Python 3.11 AI/ML project. Students are in a postgrad program learning 
Python. Disable rules too strict for beginners. Keep PEP 8 enforcement 
for naming and line length. Output only the file content."

## Critical Evaluation (150-200 words):

The AI-generated .pylintrc was mostly well-suited for a beginner 
environment. It correctly disabled R0903 (too-few-public-methods) 
and C0415 (import-not-at-top), which are rules that confuse new 
learners without teaching good habits. Setting max-line-length=88 
to match Black was a smart choice that prevents conflicting warnings.

However, the AI initially disabled W0611 (unused-import) entirely, 
which I would change — unused imports are a real beginner mistake 
that should be caught early. Keeping that rule ON actually helps 
students learn faster.

The generated-members setting for numpy and requests was excellent, 
preventing false positives that would frustrate beginners who haven't 
learned about dynamic attributes yet.

One rule that felt too lenient was disabling C0114 (module docstring) 
— while not critical, writing a module description is a good habit 
worth encouraging from day one. Overall the AI output was 80% usable 
with minor tweaks needed for a proper beginner learning environment.
"""Build workbook edition 1.1 while preserving original pages, forms and outlines.

Run from the repository root with the optional PDF build dependencies installed.
The original edition is read from Git, so the output is never used as its own base.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "ab05250c95aaba3293b6a11887e3974e141af3ed"
GUIDE_COMMIT = "ab05250c95aaba3293b6a11887e3974e141af3ed"
BASE_SHA256 = "311ddf49323db0da8fedd0643a17109a4e19c3bdd313860814ad393123fb42ed"
PDF_PATH = "docs/AI_Engineering_Bootcamp_Flamong.pdf"
REPO = "https://github.com/flamong-devs/flamong-ai-engineering-bootcamp"
GUIDES = f"{REPO}/blob/{GUIDE_COMMIT}/docs/learning/"
EDITION = "1.1"
DATE = "29 September 2026"
W, H = 595.2756, 841.8898
M, WIDTH = 44, W - 88
INK = colors.HexColor("#242424")
MUTED = colors.HexColor("#666661")
RED = colors.HexColor("#ed3426")
GREY = colors.HexColor("#f0f0f0")


def rich(text):
    """Render the deliberately small inline Markdown subset used in the guides."""
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


def guide(name, label):
    return f'<link href="{GUIDES}{name}" color="#b82b22"><u>{escape(label)}</u></link>'


class Page:
    def __init__(self, number, section, title, subtitle="", floor=72):
        self.number, self.floor = number, floor
        self.title = title
        self.buf = io.BytesIO()
        self.c = canvas.Canvas(self.buf, pagesize=(W, H), invariant=1)
        self.links = []
        self.c.setFillColor(INK)
        self.c.setFont("SourceBold", 9)
        self.c.drawString(M, H - 35, "FLAMONG")
        self.c.setFillColor(MUTED)
        self.c.setFont("Source", 8)
        self.c.drawString(139, H - 35, section.upper())
        self.c.setFillColor(RED)
        self.c.rect(W - M - 25, H - 36, 25, 3, fill=1, stroke=0)
        self.y = H - 65
        self.para(title, size=25, leading=29, bold=True, after=9)
        if subtitle:
            self.para(subtitle, size=10, leading=13, after=16)

    def check(self, height):
        if self.y - height < self.floor:
            raise ValueError(f"Page {self.number}: content overflows at y={self.y:.1f}, height={height:.1f}, floor={self.floor}")

    def para(self, text, size=11, leading=14.5, bold=False, after=8):
        style = ParagraphStyle("body", fontName="SourceBold" if bold else "Source", fontSize=size,
                               leading=leading, textColor=INK, spaceAfter=0)
        p = Paragraph(text, style)
        _, h = p.wrap(WIDTH, H)
        self.check(h + after)
        p.drawOn(self.c, M, self.y - h)
        self.y -= h + after

    def head(self, text):
        self.para(text, size=12, leading=15, bold=True, after=5)

    def code(self, lines, size=9.2):
        lines = lines.splitlines()
        for line in lines:
            if pdfmetrics.stringWidth(line, "Courier", size) > WIDTH - 22:
                raise ValueError(f"Code too wide on page {self.number}: {line}")
        h = 20 + len(lines) * 13
        self.check(h + 10)
        self.c.setFillColor(GREY)
        self.c.roundRect(M, self.y - h, WIDTH, h, 5, fill=1, stroke=0)
        self.c.setFont("Courier", size)
        self.c.setFillColor(INK)
        for i, line in enumerate(lines):
            self.c.drawString(M + 11, self.y - 17 - i * 13, line)
        self.y -= h + 10

    def table(self, rows, widths, size=10, leading=12.5):
        style = ParagraphStyle("cell", fontName="Source", fontSize=size, leading=leading, textColor=INK)
        data = [[Paragraph(str(t), style) for t in row] for row in rows]
        tab = Table(data, colWidths=widths, hAlign="LEFT")
        tab.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), GREY),
            ("LINEBELOW", (0, 0), (-1, 0), .7, RED),
            ("LINEBELOW", (0, 1), (-1, -1), .35, colors.HexColor("#d6d6d0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        _, h = tab.wrap(WIDTH, H)
        self.check(h + 12)
        tab.drawOn(self.c, M, self.y - h)
        self.y -= h + 12

    def internal(self, label, destination):
        top = self.y
        self.para(f'<font color="#b82b22"><u>{escape(label)}</u></font>', size=10, leading=13, after=5)
        self.links.append((destination, (M, self.y + 3, W - M, top)))

    def reflection(self, rect, question):
        top = float(rect[3])
        if self.y < top + 47:
            raise ValueError(f"Page {self.number}: reflection overlaps body")
        self.y = top + 43
        old = self.floor
        self.floor = top + 1
        self.para("LAB REFLECTION", size=9, leading=11, bold=True, after=4)
        self.para(question, size=10, leading=13, after=0)
        self.floor = old

    def finish(self):
        self.c.setStrokeColor(colors.HexColor("#d6d6d0"))
        self.c.setLineWidth(.5)
        self.c.line(M, 39, W - M, 39)
        self.c.setFillColor(INK)
        self.c.setFont("SourceBold", 7.5)
        self.c.drawString(M, 24, "Prepared by Flamong.com")
        self.c.setFillColor(MUTED)
        self.c.setFont("Source", 7)
        self.c.drawCentredString(W / 2, 24, "AI ENGINEERING BOOTCAMP  |  EDITION 1.1")
        self.c.drawRightString(W - M, 24, str(self.number))
        self.c.showPage()
        self.c.save()
        return PdfReader(self.buf)


def source_pdf():
    return subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{PDF_PATH}"], cwd=ROOT)


def read_guide(name):
    return subprocess.check_output(
        ["git", "show", f"{GUIDE_COMMIT}:docs/learning/{name}"], cwd=ROOT, text=True
    )


def rubric_rows():
    text = read_guide("CAPSTONE_RUBRIC.md")
    rows = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) == 5 and parts[1].isdigit():
            rows.append(parts)
    assert len(rows) == 8 and sum(int(r[1]) for r in rows) == 100
    return rows


def diagnostic_parts():
    text = read_guide("DIAGNOSTIC.md")
    chunks = re.split(r"(?=^\*\*\d+\.)", text, flags=re.M)[1:]
    questions = []
    for chunk in chunks:
        chunk = re.split(r"^## ", chunk, maxsplit=1, flags=re.M)[0].strip()
        parts = re.split(r"```python\n(.*?)```", chunk, flags=re.S)
        questions.append(parts)
    assert len(questions) == 10
    return questions


def make_pages(original):
    pages = {}

    # Keep the original cover logo; rebuild the edition and licence information.
    p = Page(1, "", "", floor=60)
    p.c.setFillColor(colors.white)
    p.c.rect(0, 0, W, H, fill=1, stroke=0)
    logo = list(original.pages[0].images)[0]
    p.c.drawImage(ImageReader(io.BytesIO(logo.data)), M, H - 135, 88, 88, preserveAspectRatio=True, mask="auto")
    p.y = H - 181
    p.para('<font color="#b82b22">FLAMONG LEARNING</font>', size=10, bold=True, after=24)
    p.para("AI Engineering<br/>Bootcamp", size=38, leading=46, bold=True, after=28)
    p.para("From software engineering to AI systems you can build, explain and evaluate.", size=15, leading=20, after=23)
    p.c.setFillColor(RED)
    p.c.rect(M, p.y, 67, 5, fill=1, stroke=0)
    p.y -= 30
    p.para("An in-depth study guide, a practical build path, and a workbook for engineers learning together.", after=22)
    p.head("THE PROJECT")
    p.para("Build a support-ticket classifier, then an evidence-based assistant with retrieval, optional local-model generation, and read-only tools for a fictional Nigerian fintech.", after=22)
    p.head("Prepared by Flamong.com")
    p.para(f"Edition {EDITION} | Revised {DATE}<br/>Companion repository snapshot: {GUIDE_COMMIT[:7]}", size=10, leading=14)
    p.para(f'<link href="{REPO}" color="#b82b22"><u>flamong-devs/flamong-ai-engineering-bootcamp</u></link>', size=10)
    p.para('Workbook and teaching materials: <link href="https://creativecommons.org/licenses/by/4.0/" color="#b82b22">CC BY 4.0</link>, with attribution to Flamong.com. Accompanying software: MIT. Licence scope is documented in the repository.', size=9, leading=12)
    p.para("12 modules | Runnable starter kit | 46 preserved fillable fields", size=9, leading=12)
    pages[1] = p

    p = Page(2, "Start here", "Your route through the bootcamp", "Choose a module or appendix. Links stay inside this workbook unless marked online.")
    titles = ["Think like an AI engineer", "Use the maths you need", "Train and measure honestly", "Understand how weights learn", "Read language as numbers", "Understand the model lifecycle", "Shape useful behaviour", "Control context and retrieval", "Build and evaluate the RAG system", "Let the system use tools", "Improve without losing control", "Demonstrate engineering judgement"]
    for i, title in enumerate(titles, 1):
        p.internal(f"{i:02d}  {title}  -  page {3*i+3}", 3*i+3)
    p.head("Read, recall, build")
    p.para("Read one lesson, close the page, answer its checks, then build. Review answers after your own attempt. Revisit difficult ideas the next day and the following week.", size=10, leading=13)
    p.head("Keep evidence and use the fields")
    p.para("Save a personal copy in a PDF viewer that supports forms. Keep longer experiments and code in your repository. Record commands, versions, predictions, results, and limits.", size=10, leading=13)
    for label, dest in [("Optional model setup - page 42",42),("Project and experiment worksheets - pages 43-44",43),("Repository and rubric overview - page 45",45),("Sources - page 47",47),("Module answer keys - pages 48-59",48),("Beginner diagnostic - pages 60-61",60),("Preparation and learning plan - page 62",62),("Diagnostic answers - page 63",63),("Rubric scoring anchors and completion gates - pages 64-66",64)]:
        p.internal(label,dest)
    pages[2] = p

    p = Page(3, "Preparation", "Choose your starting point", "Use evidence about your current skills to plan preparation before Module 1.")
    p.head("Start with the diagnostic")
    p.para("Allow 20-30 minutes for the ten questions on pages 60-61. Write your own answers before opening page 63. Score Python, maths, Git, evaluation, and AI systems separately, each out of two.")
    p.para("For every area below 2/2, complete its preparation task on page 62. A high total does not replace a missing prerequisite. If all areas score 2/2 and the setup on page 5 works, start Module 1. This short diagnostic is a placement aid, not an entrance exam.")
    p.internal("Open the diagnostic - page 60",60)
    p.internal("Open preparation and your learning plan - page 62",62)
    p.head("What you should bring")
    p.para("Practise writing and debugging a small program, Git, JSON, HTTP APIs, and basic tests. Python newcomers should complete preparation before relying on Module 1 as a bridge. The core labs do not require a GPU or a paid API.")
    p.head("How this supports further study")
    p.para("This independent Flamong curriculum selects foundations useful for CS329Z and related AI engineering study. The course routes below are references, not required courses to complete in sequence. Check current course prerequisites at source R1 on page 47.", size=10, leading=13)
    p.table([["Reference route", "Relevant emphasis", "Modules"], ["CS224N [R2]", "Representations, gradients, transformers and language models", "2-7"], ["CS224U [R3]", "Language understanding, experiment design and evaluation", "3, 5, 9, 12"], ["CS224V [R4]", "Agentic applications, retrieval and structured knowledge", "8-10, 12"], ["CS336 [R5]", "Language-model construction, data, training and systems", "4-6, 8, 11"]], [100, WIDTH-183,83])
    p.para("These are original exercises, not Stanford assignment solutions or a substitute for university depth, credit, or assessment. Optional neural-network, embedding, and model-adaptation extensions require additional setup and study.", size=10, leading=13)
    p.para(guide("START_HERE.md","Online: setup, preparation and learning plan"),size=10)
    pages[3]=p

    p=Page(4,"Cohort plan","Eight weeks. Visible progress.","Suggested pace: 10-12 hours each week; extend the schedule to suit preparation needs.")
    p.table([["Week","Learn and build","Evidence to bring"],["1","Modules 1-2: task, data, Python and maths","Data contract; hand-checked functions"],["2","Modules 3-4: evaluation and learning","Baseline; error review; gradient log"],["3","Modules 5-6: representations and model lifecycle","Similarity experiment; tiny count model"],["4","Modules 7-8: prompts and retrieval","Prompt specification; retrieval comparison"],["5","Module 9: evidence review; optional generation","Reviewed evidence or model answers; abstention cases"],["6","Module 10: tools and bounded loops","Scripted or model-directed trace; boundary tests"],["7","Module 11: cost and release controls","Timing report; release decision"],["8","Module 12: capstone and further study","Frozen evaluation; individual defence"]],[40,250,WIDTH-290])
    p.head("Choose a route; keep the same review standard")
    p.para("The offline route uses retrieval, evidence preview, manual source review, and scripted tool-loop tests. The local-model route adds actual generation or model-directed tool use and the evidence needed to assess those claims. Either route can earn 100 points.")
    p.head("A weekly rhythm")
    p.para("Spend roughly two hours reviewing concepts, four building, two evaluating, and two explaining or fixing gaps. Rotate implementer and reviewer roles. Each learner should reproduce a result and explain a failure independently.")
    p.para("A sound experiment that finds no improvement is useful progress. Reward clear explanations and honest limits. If studying alongside CS329Z, prioritise Modules 1-3 and 5-10, and return to maths gaps and deeper reviews.",size=10,leading=13)
    p.internal("Assessment weights and evidence - page 45",45)
    pages[4]=p

    p=Page(5,"Starter kit","Get your first result today.","Clone the public repository, then run commands from its root.")
    p.para(f'<link href="{REPO}" color="#b82b22"><u>{REPO}</u></link>',size=9.5,leading=12)
    p.code("git clone https://github.com/flamong-devs/flamong-ai-engineering-bootcamp.git\ncd flamong-ai-engineering-bootcamp",size=8.8)
    p.para("The core uses Python 3.10+ and the standard library. After cloning, it needs no API key, package installation, or model download. Substitute python3 or py -3 if that is your Python command.")
    p.code("python --version\npython -m bootcamp audit\npython -m unittest discover -s tests -v\npython -m bootcamp classify --split dev\npython -m bootcamp search \"pending transfer\" --k 3")
    p.head("What you should see")
    p.para("The audit reports 36 training, 12 development, and 12 test tickets. The starter classifier gets 9/12 correct on dev (75%) and card recall of 0.50. The 19 starter tests pass. These are tiny synthetic teaching results; record your own Python version and commit.")
    p.head("Know what is running")
    p.para("Default ask returns extractive evidence without an LLM. The optional --mode ollama path adds generation. Its protocol has a mocked test; live-model quality remains for your group to evaluate. Setup is on page 42.")
    p.head("If something fails")
    p.para("No module named bootcamp: check that your terminal is in the repository root. Ran 0 tests: confirm tests/test_core.py exists and use the exact command above. Save an unexpected error and inspect your changes before continuing.",size=10,leading=13)
    p.para("Keep final-test cases separate from development. The public starter labels are visible; the capstone requires a fresh independently held set after the candidate is frozen.",size=10,leading=13)
    p.internal("Preparation and learning plan - page 62",62)
    pages[5]=p

    def lab(n,section,title,subtitle):
        rect=next(a.get_object()['/Rect'] for a in original.pages[n-1]['/Annots'] if a.get_object().get('/Subtype')=='/Widget')
        return Page(n,section,title,subtitle,floor=float(rect[3])+50),rect

    p,rect=lab(14,"Module 03 / Build lab","Lab 03 / Train, inspect, improve","Build a classifier without teaching to the final exam.")
    p.head("Split by case group before fitting")
    p.table([["Train","Dev","Test"],["Fit model parameters","Choose design changes","Evaluate the frozen candidate"]],[WIDTH/3]*3)
    p.para("Keep messages from the same case in one split. Each split has a distinct job; final-test feedback must not become development feedback.",size=10.5,leading=14)
    p.code("python -m bootcamp classify --split dev")
    p.para("1. Save the baseline dev report: 9/12 correct (75%), against the balanced majority baseline of 33.3%. Card recall is 0.50.",size=10.5,leading=14)
    p.para("2. Read the three errors. Check whether the wording is absent from training, ambiguous, or poorly represented.",size=10.5,leading=14)
    p.para("3. Propose one change using training data and dev feedback only. Keep the original result and compare with the same procedure.",size=10.5,leading=14)
    p.para("4. Freeze the candidate before final evaluation. For the capstone, use a fresh independently held set as described on pages 41 and 66.",size=10.5,leading=14)
    p.head("Deliver and check")
    p.para("Submit a baseline report, short error analysis and one controlled experiment. Explain why overall accuracy of 0.75 can coexist with card recall of 0.50. An honest result without a measured gain is valid evidence.",size=10.5,leading=14)
    p.reflection(rect,"What improvement might raise the score while making the experiment less honest?")
    pages[14]=p

    p,rect=lab(29,"Module 08 / Build lab","Lab 08 / Compare retrieval choices","Measure retrieval, inspect the evidence, then test a chunking change.")
    p.code('python -m bootcamp search "pending transfer" --k 3\npython -m bootcamp evaluate --split dev --k 1\npython -m bootcamp evaluate --split dev --k 3')
    p.table([["Starter setting","Answerable hit rate","Mean recall","Unsupported with hits"],["k=1","6/6 (1.0)","1.0","0/2"],["k=3","6/6 (1.0)","1.0","0/2"]],[82,132,102,WIDTH-316],size=9.5,leading=12)
    p.para("The sample search returns P01 then P02, not necessarily three passages. Both k settings already reach 6/6 on these dev cases. Inspect relevance and fresh probes; do not manufacture a gain or call a retrieval score answer quality.",size=10,leading=13)
    p.para("1. Add three development probes: a paraphrase, an unsupported request, and a restricted-source request under an unauthorised role. Specify expected behaviour before running them.",size=10,leading=13)
    p.para("2. Add a long fictional policy in a scratch copy; compare paragraph and fixed-size chunks. Keep status, roles, version, source and parent document ID. Define stable chunk IDs.",size=10,leading=13)
    p.para("3. Map chunk IDs back to parent gold IDs for document-level recall and deduplicate parents. Check archive exclusion, role filtering, empty queries and citation validation. Freeze the procedure before final evaluation.",size=10,leading=13)
    p.para("DELIVER: settings, baseline/candidate commits, comparison table, probes, chunking decision and regression evidence. "+guide("MODULE_08_RETRIEVAL.md","Online: detailed guided lesson"),size=9.5,leading=12)
    p.reflection(rect,"How could excellent retrieval scores coexist with a bad final answer?")
    pages[29]=p

    p,rect=lab(32,"Module 09 / Build lab","Lab 09 / Review evidence and answers","Required offline evidence review; optional local-model generation.")
    p.head("Offline route")
    p.code('python -m bootcamp ask "How do I handle a failed transfer?"')
    p.para("1. Review the six answerable and two unanswerable dev questions. Save retrieved IDs and passages; judge whether they support a useful answer. Write any manual answers yourself and label them as human-written.",size=10.5,leading=14)
    p.para("2. Add a question that needs transaction status. Explain why a policy passage cannot verify a transaction outcome. Record retrieval misses, irrelevant evidence, missing support and tool-needed cases.",size=10.5,leading=14)
    p.head("Optional local-model route")
    p.para("Follow page 42 to install and select a model, then run generation on the same cases and preserve the actual outputs.",size=10.5,leading=14)
    p.code('python -m bootcamp ask "How do I handle a failed transfer?" --mode ollama',size=9)
    p.para("Have a partner judge each generated claim against its cited passage. Record the model, settings, prompt and corpus versions. Inspect invalid JSON, unsupported claims and incorrect abstention as well as retrieval failures.",size=10.5,leading=14)
    p.head("Deliver and check")
    p.para("Submit eight reviewed dev cases, the extra transaction-status case, a failure table and a manifest. Distinguish extractive, human-written and model-generated output. Offline submissions mark generation as untested; either route can earn full credit.",size=10.5,leading=14)
    p.reflection(rect,"What result would make you remove generation from one product flow?")
    pages[32]=p

    p,rect=lab(35,"Module 10 / Build lab","Lab 10 / Inspect the boundary","Keep tool execution, authorisation and loop control in application code.")
    p.head("Required offline work")
    p.code("python -m bootcamp transaction TX100 --actor learner_a\npython -m bootcamp transaction TX200 --actor learner_a\npython -m unittest discover -s tests -v")
    p.para("1. The first lookup succeeds; the second must fail with a permission error and a non-zero exit status. Do not change the actor to make the forbidden read pass.",size=10.5,leading=14)
    p.para("2. Inspect test_actor_injection, test_unknown_tool, test_trace, test_loop_repeat and test_budget. Annotate the scripted action, observation and stopping condition. A scripted planner demonstrates loop control, not model intelligence.",size=10.5,leading=14)
    p.para("3. Add malformed-argument and hostile-source regression cases. Explain which application check enforces each permission, and what remains untested.",size=10.5,leading=14)
    p.head("Optional model-directed trace")
    p.code('python -m bootcamp agent "What should I do about TX100?" --mode ollama',size=9)
    p.para("Use an installed model configured as on page 42. Save the real trace, review claims against observations, and inspect failures and termination. The agent's final answer still needs human review.",size=10.5,leading=14)
    p.head("Deliver and check")
    p.para("Submit an annotated scripted or model-directed trace and two boundary tests. Label the route. Caller identity comes from application context; CLI actor/role flags are simulation fixtures, not authentication. Neither route performs real payments.",size=10.5,leading=14)
    p.reflection(rect,"What could go wrong if you store every tool result forever?")
    pages[35]=p

    p,rect=lab(41,"Module 12 / Build lab","Lab 12 / Defend a frozen candidate","Use one assessment standard for the offline and local-model routes.")
    p.code("python -m unittest discover -s tests -v")
    p.para("1. Freeze the candidate commit, data, prompts, model and settings. A peer or facilitator holds at least 12 fresh final cases until the freeze, with expected outcomes defined before execution. Cover success, unsupported or ambiguous requests, and relevant boundaries.")
    p.para("2. Run baseline and candidate under the same final procedure. Report denominators, all outcomes and failure analysis. If results guide another change, obtain a new independent set for the next final claim.")
    p.para("3. Submit the task definition, architecture, data notes, implementation, manifest, evaluation, release note and run instructions. Keep evidence in reports/capstone.md; the starter ignores reports/*.json.")
    p.para("4. Present a five-minute demo: success, insufficient evidence, and a denied tool request. Explain one metric, one failure, one access boundary and two testable next experiments.")
    p.head("Route and completion check")
    p.para("Offline submissions label generation as untested and traces as scripted. Local-model claims include actual outputs and claim-support review. All 19 starter tests still pass; both routes can earn full credit. Without independently held final cases, label the work self-evaluation and keep that assessment gate pending.",size=10.5,leading=14)
    p.para("Use the weights on page 45 and the exact scoring anchors and completion gates on pages 64-66. Public starter test labels do not replace the fresh-set requirement.",size=10,leading=13)
    p.reflection(rect,"What would you change before offering this assistant to real support staff?")
    pages[41]=p

    p=Page(42,"Implementation appendix","Run the optional model path.","The offline route is complete without a model; generation requires a separately installed one.")
    p.head("Prepare your machine")
    p.para('Follow <link href="https://docs.ollama.com/quickstart" color="#b82b22">Ollama\'s official quickstart</link> [R12]. Install a model that fits your memory and usage rights. Confirm its exact name with ollama list and ensure the local service is running. Downloads need internet and may be large; the kit does not download models.')
    p.code('# macOS / Linux: replace with an installed model name\nexport OLLAMA_MODEL="your-installed-model"\npython -m bootcamp ask "Explain failed transfers" --mode ollama\n\n# PowerShell environment variable equivalent:\n$env:OLLAMA_MODEL = "your-installed-model"',size=9)
    p.head("What the adapter does")
    p.para("bootcamp/llm.py calls /api/chat at 127.0.0.1:11434. It requests non-streaming JSON, temperature zero, and a 120-second timeout. The RAG path validates fields and citation IDs; it does not prove that every claim is supported. Invalid JSON, unknown citations and server failures surface as errors.")
    p.table([["Inspect","Purpose"],["bootcamp/core.py","Baselines, retrieval, metrics, tools and validation"],["bootcamp/llm.py","Optional generation and bounded tool loop"],["data/","Synthetic tickets, policies, questions and dated fixtures"],["tests/test_core.py","19 starter regression and boundary checks"],["docs/learning/","Diagnostic, guided lesson and common capstone rubric"]],[150,WIDTH-150])
    p.para("No live model was evaluated for this workbook revision. Record the exact model, settings, hardware, prompt/corpus versions and observed outputs in your own run. A passed mock test verifies a protocol path, not generation quality.",size=10,leading=13)
    p.internal("Offline and local-model assessment - page 66",66)
    pages[42]=p

    rows=rubric_rows()
    p=Page(45,"Cohort delivery","A repository and one review standard.","Public repository: flamong-devs/flamong-ai-engineering-bootcamp")
    p.para(f'<link href="{REPO}" color="#b82b22"><u>Open the repository</u></link>. The starter is at the root, the workbook is in docs/, and learning guides are in docs/learning/. Use small learner branches and reviewed changes. Branch protection remains a recommendation unless configured.')
    p.table([["Assessment criterion","Points"]]+[[r[0],r[1]] for r in rows]+[["Total","100"]],[WIDTH-60,60],size=10,leading=12)
    p.para("Score each category at zero, half or full credit using the anchors on pages 64-65. An experiment that does not improve the baseline can earn full credit when the implementation, comparison and decision are sound.",size=10,leading=13)
    p.head("Pass conditions")
    p.para("Pass: at least 70/100, every completion gate met, and at least half credit in Evaluation quality and Permissions and failure behaviour. Distinction: at least 85/100 with those same conditions. Otherwise revise. An unmet gate remains pending even with a high score.",size=10,leading=13)
    p.para("The common gates cover reproducibility, passing tests, appropriate data, enforced access, independent frozen evaluation, and claims supported by the demonstrated route. Full details and reviewer record: page 66.",size=10,leading=13)
    p.para("This is a coaching assessment, not an employment prediction, production-readiness certification or university grading scheme. "+guide("CAPSTONE_RUBRIC.md","Online: full assessment rubric"),size=10,leading=13)
    p.para('Workbook: CC BY 4.0, attribution to Flamong.com. Code: MIT. Third-party resources retain their own terms. See <link href="'+REPO+'/blob/main/LICENSING.md" color="#b82b22">LICENSING.md</link>.',size=9.5,leading=12)
    pages[45]=p

    qs=diagnostic_parts()
    for n, inds, subtitle in [(60,range(0,4),"Python and maths | Write your answers before opening page 63."),(61,range(4,10),"Git, evaluation and AI systems | Explain the reason for each answer.")]:
        p=Page(n,"Beginner diagnostic",f"Diagnostic / {'1 of 2' if n==60 else '2 of 2'}",subtitle)
        if n==60:p.para("Allow 20-30 minutes for both pages. Each question is worth one point. Use a notebook or reports/learning-plan.md; this is a preparation aid, not an entrance exam.",size=10,leading=13)
        for i in inds:
            for j,part in enumerate(qs[i]):
                if not part.strip():continue
                if j%2:p.code(part.rstrip(),size=9)
                else:p.para(rich(part.replace('\n',' ')),size=11,leading=14.5,after=12)
        p.para("After your first attempt, use the answers on page 63 and the preparation route on page 62. Keep each area score separate: Python, maths, Git, evaluation and AI systems.",size=10,leading=13)
        p.internal("Preparation tasks and learning plan - page 62",62)
        p.internal("Answers - page 63 (after your attempt)",63)
        pages[n]=p

    p=Page(62,"Preparation and progress","Turn gaps into a learning plan.","Complete the preparation task for each diagnostic area below 2/2.")
    p.para("Do not skip a missing prerequisite because your total is high. After preparation, explain a new example to a peer; repeating a memorised quiz answer is not new evidence.",size=10,leading=13)
    p.table([["Area","Preparation task","Readiness evidence"],["Python","Write a function counting labels in three fictional ticket dictionaries. Try an empty list.","Predict both results and explain each line."],["Maths","Calculate 3/8, the mean of 2, 4, 6, and the dot product of [1, 2] and [3, 4]. Verify in Python.","Explain 0.375, 4, and 11."],["Git","On a practice branch, edit Markdown, inspect, stage and commit. Check status.","Explain working, staged, committed and pushed changes."],["Evaluation","Read Module 3 and assign a job to train, dev and final-test data.","Explain why tuning on final results requires a fresh final set."],["AI systems","Run search and default ask for pending transfer. Read the passages.","Distinguish policy evidence, generated text and transaction observations."]],[62,270,WIDTH-332],size=10,leading=13)
    p.head("Record reports/learning-plan.md")
    p.para("Include your goal, weekly study time, Python/OS versions, starting commit, audit/test results, five area scores, preparation evidence, next module and route choice. Only include information you intend to share if you commit the file.")
    p.table([["Module/date","Evidence file or commit","I can explain / need to review"],["1 / ...","...","..."]],[85,175,WIDTH-260])
    p.para("Follow LABS.md and read the capstone requirements early. Keep commands, settings, predictions, observed results and limitations after each module. A working setup plus readiness evidence is your signal to begin Module 1.",size=10,leading=13)
    p.para(guide("START_HERE.md","Online: complete first-session guide and plan template"),size=10)
    p.internal("Return to Module 1 - page 6",6)
    pages[62]=p

    p=Page(63,"Diagnostic answers","Check understanding, then prepare.","One point per question when both the answer and explanation are correct.")
    answers=read_guide('DIAGNOSTIC_ANSWERS.md')
    for line in answers.splitlines():
        m=re.match(r'^\| (\d+) \| (.*?) \|$',line)
        if m:p.para(f'<b>{m[1]}.</b> '+rich(m[2]),size=10.3,leading=13.3,after=10)
    p.para("Questions 1-2: Python; 3-4: maths; 5-6: Git; 7-8: evaluation; 9-10: AI systems. Each area scores 0-2. Any area below two maps to its preparation task on page 62. Equivalent wording and valid command variants are acceptable.",size=10,leading=13)
    p.para("For a follow-up, change the list, class counts or tool request. Ask for a prediction and explanation before running code. Use the result to identify concepts needing practice.",size=10,leading=13)
    pages[63]=p

    for n,part in ((64,rows[:4]),(65,rows[4:])):
        p=Page(n,"Capstone scoring anchors",f"Rubric / {'1 of 2' if n==64 else '2 of 2'}","Score each criterion at zero, half or full credit. Record an evidence link and reason.")
        for name,weight,zero,half,full in part:
            p.head(f"{name} / {weight} points")
            p.para(f"<b>Zero:</b> {escape(zero)}<br/><b>Half ({float(weight)/2:g}):</b> {escape(half)}<br/><b>Full ({weight}):</b> {escape(full)}",size=11,leading=15,after=16)
        p.para("A well-designed experiment that finds no improvement can earn full credit. Assess the implementation, comparison and resulting decision. Numeric scores do not override unmet completion gates.",size=10,leading=13)
        p.internal("Completion gates and evidence - page 66",66)
        pages[n]=p

    p=Page(66,"Capstone completion","Evidence before a pass.","Use with the weights on page 45 and scoring anchors on pages 64-65.")
    p.head("Submit one evidence bundle")
    p.para("Project brief and architecture; baseline and frozen candidate commits; runtime, data and optional model/prompt versions; exact run commands; development and final evaluation with counts and per-case outcomes; at least three inspected failure or boundary cases; test output; measured latency and labelled cost assumptions; fallback, rollback trigger and feedback owner; demo, limitations and assistance/source credits.",size=10.5,leading=14)
    p.head("Meet every completion gate")
    gates=["The reviewer can run the submitted commit. All 19 starter tests pass without removing or weakening checks; relevant added tests pass.","The submission contains no credentials, actual customer records or private company documents.","Evaluated cases do not bypass caller/role restrictions or the allowed-tool boundary. Repair and retest any detected bypass.","Freeze the candidate, data, prompt, model and settings before revealing at least 12 independently held fresh final cases. Define expected outcomes first; cover success, unsupported/ambiguous inputs and relevant boundaries. Compare baseline and candidate fairly and retain all results. If final feedback guides a change, obtain a fresh set for a new final claim.","Claims match the evidence: fixtures are fictional, scripted traces are labelled, and generated-answer claims include live-model outputs and source-support review."]
    for i,t in enumerate(gates,1):p.para(f"<b>{i}.</b> {escape(t)}",size=10.5,leading=14,after=7)
    p.para("Twelve cases are a teaching minimum, not population-level evidence. Self-study without an independently held set stays labelled self-evaluation, with that gate pending. A model route without live evidence is completed or reassessed as an offline submission.",size=10,leading=13)
    p.head("Record the decision")
    p.para("Pass: 70+ and all gates, with at least half credit in Evaluation quality and Permissions and failure behaviour. Distinction: 85+ with the same conditions. Otherwise revise. Record route, commits, final-set owner/version, freeze and evaluation dates, scores and links, gate evidence, decision, revisions, reviewer role and review date.",size=10.5,leading=14)
    p.para("Keep reports/capstone.md reviewable; reports/*.json is ignored by the starter. "+guide("CAPSTONE_RUBRIC.md","Online: complete rubric and reviewer-record template"),size=10,leading=13)
    pages[66]=p
    return pages


def widgets(reader):
    found={}
    for i,page in enumerate(reader.pages):
        for ref in page.get('/Annots',[]):
            a=ref.get_object()
            if a.get('/Subtype')=='/Widget':
                name=a.get('/T') or a.get('/Parent',{}).get_object().get('/T')
                found[name]=(i,tuple(float(v) for v in a['/Rect']),str(a.get('/V','')))
    return found


def build(output):
    for name,file in [('Source','SourceSans3-Regular.ttf'),('SourceBold','SourceSans3-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,ROOT/'tools/pdf-assets'/file))
    pdfmetrics.registerFontFamily('Source',normal='Source',bold='SourceBold',italic='Source',boldItalic='SourceBold')
    base=source_pdf()
    assert hashlib.sha256(base).hexdigest()==BASE_SHA256, "Unexpected original workbook"
    original=PdfReader(io.BytesIO(base))
    assert len(original.pages)==59 and len(original.get_fields())==46
    replacements=make_pages(original)
    writer=PdfWriter()
    writer.clone_document_from_reader(original)
    for number,design in sorted(replacements.items()):
        rendered=design.finish()
        new=rendered.pages[0]
        if number<=59:
            page=writer.pages[number-1]
            retained=ArrayObject(a for a in page.get('/Annots',[]) if a.get_object().get('/Subtype')=='/Widget')
            page[NameObject('/Contents')]=new.raw_get('/Contents').clone(writer)
            page[NameObject('/Resources')]=new.raw_get('/Resources').clone(writer)
            page[NameObject('/Annots')]=retained
            for ref in new.get('/Annots',[]):
                annotation=DictionaryObject({k:v for k,v in ref.get_object().items() if k!='/P'})
                writer.add_annotation(number-1,annotation.clone(writer))
        else:
            assert number==len(writer.pages)+1
            writer.add_page(new)
    for number,design in replacements.items():
        for destination,rect in design.links:
            writer.add_annotation(number-1,Link(rect=rect,target_page_index=destination-1))
    # Keep existing bookmark destinations but align renamed pages with their headings.
    page_numbers={page.indirect_reference.idnum:i+1 for i,page in enumerate(writer.pages)}
    def rename_outline(ref):
        while ref:
            node=ref.get_object()
            dest=node.get('/Dest')
            number=page_numbers.get(dest[0].idnum) if dest and hasattr(dest[0],'idnum') else None
            if number in replacements and replacements[number].title:
                node[NameObject('/Title')]=TextStringObject(replacements[number].title)
            if node.get('/First'):
                rename_outline(node['/First'])
            ref=node.get('/Next')
    rename_outline(writer.root_object['/Outlines'].get('/First'))
    for number,title in [(60,'Beginner diagnostic: Python and maths'),(61,'Beginner diagnostic: Git, evaluation and AI'),(62,'Preparation and learning plan'),(63,'Diagnostic answers'),(64,'Capstone rubric: criteria 1-4'),(65,'Capstone rubric: criteria 5-8'),(66,'Capstone evidence and completion gates')]:
        writer.add_outline_item(title,number-1)
    # Credentials attached to the original bytes cannot certify this revised edition.
    names=writer.root_object.get('/Names')
    names=names.get_object() if names else None
    if names and '/EmbeddedFiles' in names:
        assert list(original.attachments)==['Content Credentials']
        del names['/EmbeddedFiles']
        writer.root_object.pop('/AF',None)
    writer.add_metadata({'/Title':'AI Engineering Bootcamp | Flamong.com | Edition 1.1',
                         '/Author':'Flamong.com','/Subject':f'Revised {DATE}; companion snapshot {GUIDE_COMMIT}; workbook CC BY 4.0; code MIT',
                         '/Creator':'Flamong workbook revision builder',
                         '/ModDate':"D:20260929000000Z"})
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_suffix('.pending.pdf')
    writer.write(temp)
    final=PdfReader(temp)
    assert len(final.pages)==66
    assert widgets(final)==widgets(original)
    assert set(final.get_fields())==set(original.get_fields())
    for name,field in final.get_fields().items():
        assert field.get('/V')==original.get_fields()[name].get('/V')
    for i in range(59):
        if i+1 not in replacements:
            assert final.pages[i].extract_text()==original.pages[i].extract_text()
    text='\n'.join(p.extract_text() or '' for p in final.pages)
    assert 'a shared GitHub repository has not been created' not in text
    assert 'Sources: page 46.' not in text
    assert 'Edition 1.0' not in text
    assert 'CC BY 4.0' in text
    temp.replace(output)
    print(f'Built {output}: 66 pages, 46 preserved fields, 7 new appendix bookmarks.')
    print(f'Source PDF SHA-256: {hashlib.sha256(base).hexdigest()}')
    print('Revised pages:', ', '.join(map(str,sorted(replacements))))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=str(ROOT/PDF_PATH))
    args=parser.parse_args()
    build(args.output)

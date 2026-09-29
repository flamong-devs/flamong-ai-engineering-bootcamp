# Workbook editions and publishing

## Edition 1.1 - 29 September 2026

The [workbook](AI_Engineering_Bootcamp_Flamong.pdf) now has 66 pages. Existing module and answer-key page numbers remain unchanged; new appendices occupy pages 60-66. All 46 original fillable fields retain their names, locations and values.

This edition:

- Replaces starter-archive-only instructions with the public repository and clone command.
- Adds the approved CC BY 4.0 workbook licence and MIT code licence information.
- Adds the beginner diagnostic, separate answers, preparation tasks and learning-plan guidance.
- Aligns offline and optional local-model work in the schedule, Modules 9-10, and capstone.
- Adds verified retrieval baseline counts, development probes and chunk-to-document evaluation guidance.
- Replaces the old five-category rubric with the common eight-category rubric, scoring anchors and completion gates.
- Cleans duplicate hidden navigation text, expands contents links and bookmarks, and replaces the overlapping arrows in the Module 3 split diagram with a clear split-purpose table.

The companion code and learning-guide snapshot is commit `ab05250c95aaba3293b6a11887e3974e141af3ed`. The revision's publication commit contains the new PDF and builder. Snapshot links inside the PDF point to the guide version used for this edition.

## Rebuild this edition

The original document source was not included in the starter kit. The builder therefore retrieves edition 1.0 from the pinned Git commit, rewrites selected pages, and preserves the remaining page content, form fields and bookmark destinations. Diagnostic questions, answers, and rubric rows are read directly from the pinned Markdown guide revision. It does not yet regenerate every lesson from Markdown.

Use a full clone with Git history. The core bootcamp remains standard-library-only; these dependencies are optional and only needed to publish the PDF:

```sh
python -m venv .venv
# macOS/Linux:
. .venv/bin/activate
# Windows PowerShell alternative: .venv\Scripts\Activate.ps1
python -m pip install -r tools/requirements-pdf.txt
python tools/build_workbook.py
```

The default output is `docs/AI_Engineering_Bootcamp_Flamong.pdf`. Use `--output` to select a review copy. The script checks the base document hash, page count, field names/values/positions, unchanged-page text and removal of obsolete instructions before replacing the requested output.

For a later edition, update `GUIDE_COMMIT`, edition/date values and revised page content deliberately. Keep `BASE_COMMIT` and `BASE_SHA256` pointing to the original edition unless the preservation strategy is also updated. Fonts and their licence are included in [tools/pdf-assets](../tools/pdf-assets/README.md).

An embedded Content Credentials attachment from the original PDF is omitted from the revised output because it cannot certify the edited bytes. The original file remains available in Git history and the user's supplied download.

## Checks before publishing

Render every page and inspect the layout, with close review of changed pages. Check internal and external link destinations, bookmarks and page references. Fill a temporary copy of all 46 fields, save it, reopen it, verify canonical and widget values and appearance streams, and render representative filled worksheets. Publish the blank workbook, not the filled test copy.

For edition 1.1, the 19 starter tests pass; PDF structure, fields, links and rendered pages were checked. No live model evaluation is claimed.

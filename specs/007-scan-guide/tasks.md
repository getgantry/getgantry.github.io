---

description: "Task list for the image scan guide"
---

<!-- STE deviation: spec-kit template headings, task format and paths stay verbatim. -->
# Tasks: Image Scan Guide and Guide Heading Fix

- [x] T001 Write spec.md, plan.md and tasks.md
- [x] T002 Add the guide to `GUIDES`, `GUIDE_CODE` and `SHOTS` in `build_pages.py`
- [x] T003 Copy `guides.scan-container-images-mac` into the 26 language files
- [x] T004 Rename the list variable in `sections_html`, so that headings after a list stay headings
- [x] T005 Add the guide to `llms.txt`
- [x] T006 Run `build_docs.py`, `build_pages.py`, `build_pages.py --check` and `scripts/check_links.py`. Result: 27 languages ok, 255 pages, 0 problems, 0 pages with `<ul id=`
- [ ] T007 Open the PR and merge it
- [ ] T008 After the merge, send the changed URLs to IndexNow

# Tools for Data Science - Basic Development Tools

> **Audience:** Students new to modern Python and collaborative workflows  
> **Duration:** 3 sessions

---

## Schedule Overview

| Session | Topic                               | Duration | Material                                                  |
| ------- | ----------------------------------- | -------- | --------------------------------------------------------- |
| 1       | IDE, Extensions & AI Agents         | 1h 30min | [session_1.md](materials/session_1.md) (Needs Review)     |
| 2       | Python Environments, Libraries & UV | 2h 00min | [session_2.md](materials/session_2.md) (Needs Review)     |
| 3       | Project Collaboration with GitLab   | 1h 30min | [session_3.md](materials/session_3.md) (Work in Progress) |

---

## Learning Objectives

By the end of this course, students will be able to:

1. Set up a modern Python development environment.
2. Use AI coding assistants responsibly to enhance productivity without sacrificing code quality.
3. Manage Python dependencies and environments effectively with `uv`.
4. Collaborate on Python projects using GitLab for version control and code review.

---

# Appendix A — Quick Reference Cards

## UV Cheat Sheet

```bash
uv init <name>                    # new project
uv python install 3.12            # install Python version
uv python pin 3.12                # pin project to version
uv add <package>                  # add dependency
uv add --dev <package>            # add dev dependency
uv remove <package>               # remove dependency
uv sync                           # install from lock file
uv sync --dev                     # include dev deps
uv run <command>                  # run in project env
uv run pytest                     # run tests
uv run ruff check .               # lint
uv lock --upgrade                 # upgrade all packages
uv pip list                       # list installed packages
```

## Git Cheat Sheet

```bash
git clone <url>                   # download repo
git status                        # what changed?
git add <file>                    # stage file
git commit -m "<message>"         # commit staged changes
git push origin <branch>          # push to remote
git pull origin main              # get latest main
git checkout -b <branch>          # create + switch branch
git checkout <branch>             # switch branch
git merge <branch>                # merge into current
git log --oneline --graph         # visual history
git diff                          # unstaged changes
git stash                         # temporarily shelve changes
git stash pop                     # restore shelved changes
```

## Conventional Commits Cheat Sheet

```
feat:      new feature
fix:       bug fix
docs:      documentation
style:     formatting (no logic change)
refactor:  restructure without feature/fix
test:      tests
chore:     build, dependencies, config
ci:        CI/CD pipeline
perf:      performance improvement
revert:    revert a commit
```

---

# Appendix B — Recommended Reading

| Topic                | Resource                            |
| -------------------- | ----------------------------------- |
| UV documentation     | https://docs.astral.sh/uv           |
| Conventional Commits | https://www.conventionalcommits.org |
| GitLab CI/CD docs    | https://docs.gitlab.com/ee/ci       |
| Pandas documentation | https://pandas.pydata.org/docs/     |
| Numpy documentation  | https://numpy.org/doc/stable/       |

---

# Appendix C — Glossary

| Term                    | Definition                                                              |
| ----------------------- | ----------------------------------------------------------------------- |
| **Virtual environment** | Isolated Python installation with its own packages                      |
| **Dependency**          | A package your project requires to run                                  |
| **Lock file**           | Exact pinned versions of all packages in the dependency tree            |
| **CI/CD**               | Automated pipeline: test, build, and deploy on every push               |
| **Merge Request (MR)**  | A proposal to merge one branch into another, with review                |
| **Branch**              | An independent line of commits diverging from a base                    |
| **Protected branch**    | A branch that requires CI and review before accepting changes           |
| **Hallucination (AI)**  | When an AI model generates plausible-sounding but incorrect information |
| **pyproject.toml**      | The modern standard configuration file for Python projects              |
| **Wheel**               | A pre-built binary package format for fast installation                 |
| **SAST**                | Static Application Security Testing — automated code security analysis  |

---

_Course material version 1.0 — prepared for a 5-hour session._  
_All code examples require Python ≥ 3.11 and UV ≥ 0.4._

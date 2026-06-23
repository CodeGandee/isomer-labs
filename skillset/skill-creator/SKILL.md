---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or package a skill for distribution.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it.
- Write a draft of the skill.
- Create a few test prompts and run them through subagents (with the skill and without it).
- Help the user evaluate the results both qualitatively and quantitatively.
  - While the runs happen in the background, draft quantitative assertions if none exist. Then explain them to the user.
  - Use the `eval-viewer/generate_review.py` script to show the user the results, and also show them the quantitative metrics.
- Rewrite the skill based on the user's feedback (and on any glaring flaws that show up in the quantitative benchmarks).
- Repeat until you are satisfied.
- Expand the test set and try again at larger scale.

Your job when using this skill is to figure out where the user is in this process and then help them progress through these stages. For instance, the user might say "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

If the user already has a draft, go straight to the eval/iterate part of the loop.

Stay flexible. If the user says they do not need a lot of evaluations, work with them directly instead.

## Communicating with the User

The skill creator may be used by people with a wide range of familiarity with coding jargon. Pay attention to context cues to decide how to phrase your communication. In the default case:

- "evaluation" and "benchmark" are borderline, but acceptable.
- For "JSON" and "assertion", look for cues that the user knows those terms before using them without explanation.

Briefly explain terms if you are in doubt. It is OK to clarify with a short definition when you are unsure whether the user will understand.

---

## Creating a Skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (for example, "turn this into a skill"). If so, extract answers from the conversation history first: the tools used, the sequence of steps, corrections the user made, and input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding.

1. What should this skill enable the agent to do?
2. When should this skill be invoked? (what user phrases or contexts)
3. What is the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often do not need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you have this part ironed out.

Research in parallel via subagents when useful (searching docs, finding similar skills, looking up best practices). Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (kebab-case, lowercase letters, digits, hyphens).
- **description**: When to invoke the skill and what it does. The description helps the agent decide when to invoke the skill. Include both what the skill does and the specific contexts in which to use it. Make the description a little "pushy" so the skill is not underused. For example, instead of "How to build a simple fast dashboard to display internal data", write "How to build a simple fast dashboard to display internal data. Use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they do not explicitly ask for a 'dashboard'."
- **compatibility**: Required tools, dependencies (optional, rarely needed).
- **the rest of the skill**: Markdown instructions for the agent that invokes the skill.

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) - Always in context (~100 words).
2. **SKILL.md body** - In context whenever the skill is invoked (<500 lines ideal).
3. **Bundled resources** - As needed (unlimited; scripts can execute without loading the whole reference).

These word counts are approximate. Go longer if needed.

**Key patterns:**

- Keep SKILL.md under 500 lines. If you approach this limit, add another layer of hierarchy and clear pointers about where the agent should go next.
- Reference files clearly from SKILL.md with guidance on when to read them.
- For large reference files (>300 lines), include a table of contents.

**Domain organization**: When a skill supports multiple domains or frameworks, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The agent reads only the relevant reference file.

#### Principle of Least Surprise

Skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in intent. Do not create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities.

#### Writing Patterns

Prefer the imperative form in instructions.

**Defining output formats** - You can do it like this:

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - Include examples when useful:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Explain to the agent why things are important rather than relying on heavy-handed MUSTs. Use theory of mind and make the skill general, not super-narrow to specific examples. Start with a draft, then review it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Do not write assertions yet — just the prompts. You will draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you will add later).

---

## Running and Evaluating Test Cases

This section is one continuous sequence — do not stop partway through.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Do not create all of this upfront — create directories as you go.

### Step 1: Spawn All Runs (With-Skill and Baseline) in the Same Turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. This is important: do not spawn the with-skill runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

Use the agent runtime's subagent mechanism to spawn subagents. Provide a complete prompt with all necessary context. A new subagent instance does not see your current context.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
- Also save a transcript.md describing what you did and a metrics.json with tool-call counts.
```

The executor subagent should read the skill's SKILL.md and follow it. See `agents/executor.md` for the full executor instructions.

**Baseline run** (same prompt, but the baseline depends on context):

- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it is testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — do not assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While Runs Are in Progress, Draft Assertions

Do not just wait for the runs to finish — use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective skills (writing style, design quality) are better evaluated qualitatively — do not force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they will see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As Runs Complete, Capture Timing Data

When each subagent task completes, the result includes timing information. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, Aggregate, and Launch the Viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:

   ```bash
   python scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
   ```

   This produces `benchmark.json` and `benchmark.md` with pass rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects. Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:

   ```bash
   python eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json
   ```

   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

   Note: use `generate_review.py` to create the viewer; there is no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the User Sees in the Viewer

The "Outputs" tab shows one test case at a time:

- **Prompt**: the task that was given.
- **Output**: the files the skill produced, rendered inline where possible.
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output.
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail.
- **Feedback**: a textbox that auto-saves as they type.
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox.

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, the user clicks "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the Feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the Skill

This is the heart of the loop. You have run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to Think About Improvements

1. **Generalize from the feedback.** The goal is to create skills that can be used many times across many different prompts. The user knows the example cases well and can assess new outputs quickly. But if the skill works only for those examples, it is useless. Rather than put in fiddly overfit changes or oppressively constrictive MUSTs, try branching out and using different metaphors or recommending different patterns of working.

2. **Keep the prompt lean.** Remove things that are not pulling their weight. Read the transcripts, not just the final outputs — if the skill is making the agent waste time on unproductive steps, get rid of the parts of the skill that cause that and see what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you ask the model to do. Today's LLMs are smart. They have good theory of mind and, when given a good harness, can go beyond rote instructions. Even if the user's feedback is terse or frustrated, try to understand the task and why the user wrote what they wrote, and then transmit that understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that is a yellow flag — reframe and explain the reasoning so the model understands why the thing you are asking for is important.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach. If all three test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that is a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it.

### The Iteration Loop

After improving the skill:

1. Apply your improvements to the skill.
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration.
4. Wait for the user to review and tell you they're done.
5. Read the new feedback, improve again, repeat.

Keep going until:

- The user says they're happy.
- The feedback is all empty (everything looks good).
- You're not making meaningful progress.

---

## Advanced: Blind Comparison

For situations where you want a more rigorous comparison between two versions of a skill (for example, the user asks "is the new version actually better?"), there is a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

Skills are invoked explicitly by the agent. The description in the SKILL.md frontmatter is not an automatic trigger, but it still helps the agent decide when to invoke the skill. After creating or improving a skill, review the description with the user and refine it manually for clarity and coverage.

There is no automated trigger-optimization loop in most runtimes. Instead:

1. Generate 10-20 realistic user prompts that should and should not invoke the skill.
2. Review them with the user to make sure they represent real usage.
3. Rewrite the description to clearly cover the should-invoke cases while staying distinct from adjacent skills.
4. Keep the description under 1024 characters and around 100-200 words.
5. Use the `scripts/quick_validate.py` script to check that the SKILL.md frontmatter is valid.

---

## Packaging and Presenting

When the skill is ready, package it for distribution. Use the included packager:

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

This creates a `.skill` file (a zip archive) that can be shared or installed into another project's skill directory by extracting it there.

After packaging, tell the user the path to the resulting `.skill` file.

---

## Runtime Notes

Different agent runtimes invoke skills in slightly different ways. Some use a `Skill` tool, some load skills automatically from a directory, and some require an explicit command. Adapt the invocation phrasing to the runtime you are operating in, but keep the core workflow the same: draft → test → review → improve → repeat.

- **Invoking skills**: Invoke the skill by name according to the runtime's mechanism. The runtime loads its SKILL.md and any bundled resources.
- **Running test cases**: Spawn subagents using the runtime's subagent mechanism. Provide each subagent a complete, self-contained prompt that includes the eval task, the skill path (for with-skill runs), and where to save outputs. The executor agent prompt template is in `agents/executor.md`.
- **Transcripts and metrics**: The executor agent should save `transcript.md` and `metrics.json` alongside its outputs. The grader agent uses these files. If the subagent does not produce them, run the grading inline from the parent agent using the returned output.
- **Reviewing results**: Use `eval-viewer/generate_review.py` to generate the review viewer. In headless environments, use `--static <output_path>` to create a standalone HTML file.
- **Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem.
- **Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. In this case:
  - **Preserve the original name.** Note the skill's directory name and `name` frontmatter field — use them unchanged. For example, if the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
  - **Copy to a writable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
  - **If packaging manually, stage in `/tmp/` first**, then copy to the output directory — direct writes may fail due to permissions.

---

## Reference Files

The `agents/` directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/executor.md` — How to run a test prompt as a subagent.
- `agents/grader.md` — How to evaluate assertions against outputs.
- `agents/comparator.md` — How to do blind A/B comparison between two outputs.
- `agents/analyzer.md` — How to analyze why one version beat another.

The `references/` directory has additional documentation:

- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating the core loop for emphasis:

- Figure out what the skill is about.
- Draft or edit the skill.
- Run the skill on test prompts.
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them.
  - Run quantitative evals.
- Repeat until you and the user are satisfied.
- Package the final skill and return it to the user.

Please add steps to your TodoList to make sure you don't forget. Specifically, put "Create evals JSON and run `eval-viewer/generate_review.py` so the human can review test cases" in your TodoList to make sure it happens.

Good luck!

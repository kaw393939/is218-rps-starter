# Build a game you can trust—with AI

This is a **self-paced, guided first lab**. Make one round of Rock, Paper, Scissors work, then show why you trust the result. You will agree on a short spec, guide an AI coding agent, use automatic checks, and review its work.

Start with **your GitHub copy → SSH clone → local AI project**. The steps below use **ChatGPT desktop in Codex mode**, terminal Git, and a browser. **VS Code is optional.** This path needs no API key, separate Codex CLI, or classroom demonstration.

**Try → Decide → Build → Check → Keep.** If you stop, return to this README at the last checkpoint you completed. [Visual overview](https://kaw393939.github.io/218_spec/).

**Work through it as a conversation.** The agent will pause for your prediction, an explanation of one test, and something you saw while playing. A sentence is enough; “I'm not sure” is useful too. Ask for a hint or example whenever you need one. Follow its questions and use the steps below to keep your place; the sample prompts are there when you need a nudge.

## 1. Try the starter

**First, get the repo into your AI project.** Use your existing class SSH setup in macOS Terminal or Ubuntu/WSL on Windows. The agent will help check Python and prepare the app after you open the folder.

Sign in to GitHub. On [the starter](https://github.com/kaw393939/is218-rps-starter), choose **Use this template → Create a new repository**. Use your account, name it `my-rps`, choose **Public**, leave **Include all branches** off, and leave the optional Copilot prompt blank. Wait until your new repository shows its README/files before cloning. Already made your copy? Open it and skip creating another.

Open your class terminal in your existing projects folder. If your clone is already there, `cd` into it instead of cloning again. Replace `YOUR-USERNAME` below. If you chose another repository name, replace `my-rps` too. **Run one command at a time; stop if one fails.** `pwd` must end in your repository's folder name, and both lines from `git remote -v` must identify **your copy** using `git@github.com:`.

```sh
git clone git@github.com:YOUR-USERNAME/my-rps.git
cd my-rps
pwd
git remote -v
```

In **ChatGPT desktop**, select **Codex** from the ChatGPT dropdown. Open this cloned folder as a **local project** with **⌘O on Mac / Ctrl+O on Windows**. Start a chat in that project, choose **Work in → This computer**, and leave **Worktree** off. On Windows, first follow the [one-time WSL app setup](https://kaw393939.github.io/218_spec/setup.html#windows-wsl).

Ask:

> Read README.md, AGENTS.md, and SPEC.md. Guide me through this lab one small step at a time. Explain briefly, then give me one action or question and wait for my reply. Ask me to predict and explain as we go; help if I'm unsure. Start by confirming this folder and helping me run the unfinished game. Do not implement the rules, commit, or push yet.

**Connection checkpoint:** the agent reports the full clone path and your SSH remote, then explains the task from its files. It should not need you to upload or paste them. [Using another coding agent?](https://kaw393939.github.io/218_spec/setup.html#another-coding-agent)

Let it verify **Python 3.12.x**, prepare `.venv`, install the pinned requirements and Chromium, and run `.venv/bin/python check.py`. Ask it to explain errors and the smallest fix; [Python help](https://kaw393939.github.io/218_spec/setup.html#python-version) covers the class setup. Expect **PASS** at each check and **STARTER BASELINE ONLY**: the missing game rules are not verified yet.

When ready, use your original **class terminal**, still in the clone, to start the game:

```sh
.venv/bin/python run.py
```

Open the printed address, usually **http://127.0.0.1:5050**. If port 5050 is busy, leave other programs running and use `PORT=5051 .venv/bin/python run.py`, then open its printed address instead. Click a move: expect both choices and **“Starter: game rules not built yet.”** A missing winner is the task, not a failed setup. Leave this terminal running the game. You will open the AI project's separate terminal for checks and Git in Step 2.

This is the recommended **local development mode**. Once you **save** a Python, HTML template, CSS, or JavaScript change, the open browser automatically returns to the starting page with that change. Python saves restart the server; the browser waits for it to return. If a Python error stops the server, fix the error shown in the terminal and run the same start command again. The displayed round clears instead of resubmitting your last move. Saved files remain on disk; there is no saved game history. Stop the server with **Ctrl+C** in this terminal.

Optional manual preview: stop the server, run `.venv/bin/python run.py --plain`, and open the printed address again. Reuse your `PORT=5051` prefix if needed. This mode does not restart or refresh automatically: after Python or template edits, restart it and reopen its address; after CSS/JavaScript edits, refresh manually. Checks use their own servers, so run `.venv/bin/python check.py` in the other terminal. GitHub Pages hosts the instructions; your Python game runs locally.

**Checkpoint:** your agent is connected to the clone, the starter checks pass, and you can see the game's unfinished notice. Stuck? [Setup help](https://kaw393939.github.io/218_spec/setup.html).

Tell the agent what you see. It will ask what the passing starter checks verified; talk that through before planning the missing rules.

**Returning later?** Check your game terminal first. If the server is still running, use its printed address. Otherwise `cd` to this existing clone and run `.venv/bin/python run.py`, reusing your `PORT` prefix if you chose another port. Reopen the same project/chat and continue at your last checkpoint; do not clone or install again.

## 2. Decide with your coding agent

Continue in this same project chat. The agent will guide the discussion; if you need a nudge, say:

> The starter is running. Help me plan RPS-001. Ask me to predict one round before you explain it. Wait for my answer, then help me agree on a short plan and checks. Do not edit yet. Keep scoring for later.

Give your prediction and why. Check it against the [nine-matchup table](SPEC.md#expected-results), and ask for help if they differ. Discuss a valid losing round and an input the server should reject. A valid loss is a **positive** case; missing or unsupported input is a **negative** case. The agent can explain this using the game. [Short introduction to the checks](https://kaw393939.github.io/218_spec/checks.html).

When the plan makes sense to you, ask the agent to save it under **Agreed plan** in `SPEC.md`, preserving the expected results. Keep the app unchanged for now.

Open **New tab → Terminal** in ChatGPT desktop. This terminal should be in your cloned folder. Keep using it for checks and Git:

```sh
pwd
cat SPEC.md
```

Confirm the path and saved plan. Setup and the baseline checks were completed in Step 1; keep using this same clone.

In **your GitHub repository → Issues → New issue**, create **“RPS-001: Play a round”**. Describe the scope and checks you agreed on; you can ask the agent for a short draft. Review before posting. Give its URL to the agent and ask it to put that link in **SPEC.md → Work record**.

**Checkpoint:** `SPEC.md` contains your agreed plan and issue link. No transfer between AI apps or manual code copying is needed.

## 3. Build and let AI check first

In the app's terminal:

```sh
git status --short --branch
git switch -c rps-001
```

Before switching, expect the `main` branch and your intended `M SPEC.md` edit. That uncommitted plan carries onto the new `rps-001` branch. If the branch exists, use `git switch rps-001`.

In the **same AI chat**, tell the agent you are ready to build. For example:

> Check our saved plan against the code, then build RPS-001 and its agreed tests. Run .venv/bin/python check.py and review the diff without weakening checks. Show me one actual test for my predicted matchup and ask what it checks. Wait for my answer. Do not commit or push.

Review file/command approval requests. The prepared checks use **Black** for formatting, **Pylint** for Python analysis, and **pytest** for behavior, including a small real-browser journey. The agent should add nine rule cases, a real request/result check, and a browser round with replay—not repeat every case through the browser.

**Checkpoint:** AI reports actual commands/results and shows you one new test. Explain what mistake it could catch; ask for a hint if needed. Passing unchanged starter tests alone is not enough.

## 4. Check and give feedback

Open the server's printed address again, then choose a move. Play several rounds. Do both choices and the result make sense? Can you play again? Try Tab and Enter too; in Safari, use Option+Tab if Tab skips buttons.

In the app's terminal:

```sh
.venv/bin/python check.py
git status --short
git diff
cat tests/test_game.py
cat tests/e2e/test_round.py
```

Press `q` if Git opens a scrolling view. `??` means a new, untracked file: `git diff` does not show it yet, so inspect the two test files above too. Find the assertion for your predicted matchup and compare it with the spec; check that the browser test plays again using real rules. You can open files in the app with **⌘P / Ctrl+P**, or optionally inspect them in VS Code.

Tell the agent about one round: your move, the computer's move, and why the result makes sense. For a mismatch, describe the action, expected result, and observed result; ask for a focused fix and retest. [Worked failure example](https://kaw393939.github.io/218_spec/checks.html#when-a-check-fails) shows how.

During fixes, `.venv/bin/python check.py --fast` skips the browser. Use the full command before review and the PR. For formatting, `.venv/bin/python -m black *.py tests` applies the shared style; inspect its edits. Do not remove meaningful assertions or disable checks just to pass.

Ask the agent to replace starter status in **SPEC.md → Work record** with actual checks, your browser observations, and real code/test links. Preserve the plan and issue. Do not record checks nobody performed.

**Checkpoint:** you can connect one requirement to its code and a meaningful test. You have tried the result yourself.

## 5. Keep the reviewed change

Expect `game.py`, `tests/test_game.py`, `tests/e2e/test_round.py`, and `SPEC.md`. Ask about other changed files before keeping them.

```sh
git add game.py tests/test_game.py tests/e2e/test_round.py SPEC.md
git diff --cached
git commit -m "RPS-001: play a round"
git push -u origin rps-001
```

In **your GitHub repository → Pull requests → New pull request**, use base `main` and compare `rps-001`. Describe the result and actual checks; add **`Closes #N`** with your issue number. In **Files changed**, verify the added tests use real rules rather than just the supplied stubs. Have the agent add the actual PR and CI run links to `SPEC.md` and push that record update. Wait for **Python checks** on the latest commit to pass, then merge when it matches the spec.

**Done:** the game works locally, the PR is merged, its issue is closed, and the spec links to code and actual checks. Return to the **class terminal running the game** and stop it with Ctrl+C. No website deployment or extra reflection document is required.

**Next, with less guidance:** [choose another small feature](NEXT.md). Try first-to-two scoring, explain why a move won, or personalize the game. Choose one, write your own short request and test plan, and use a separate issue/PR.

# Hands-on exercises

Do these in order after pushing the project to GitHub. Each one shows a
different part of how pipelines behave.

---

## 1. Break the build 🔴

Edit `app/calculator.py` and introduce a bug:

```python
def add(a: float, b: float) -> float:
    return a - b      # oops
```

Commit and push to `main`. Then in the **Actions** tab:

- `02 · CI` → all 3 `test` jobs fail. Open one and find the red assertion message.
- `03 · Full Pipeline` → `test` fails, so `build` and `deploy` are **skipped**.
  Your live website still shows the **old** version. That's the point of CI/CD:
  broken code never gets deployed.

Fix the bug, push again, and watch everything turn green and the site update
(check the commit SHA on the page).

## 2. Break the linter 🧹

Add an unused import at the top of `app/calculator.py`:

```python
import os
```

Push. The `lint` job fails with `F401 'os' imported but unused`. In `03`, nothing
after lint even starts. Remove it and push.

## 3. Pull requests — CI as a gatekeeper 🚦

```bash
git checkout -b feature/power
```

Add a function and a test:

```python
# app/calculator.py
def power(a: float, b: float) -> float:
    return a ** b
```

```python
# tests/test_calculator.py   (also add power to the import line)
def test_power():
    assert power(2, 10) == 1024
```

```bash
git add . && git commit -m "Add power()" && git push -u origin feature/power
```

Open a pull request on GitHub. Notice:

- The checks run **on the PR** and show at the bottom of the PR page.
- In `03 · Full Pipeline`, `deploy` is **skipped** — its `if:` only allows `main`.
- `07 · Use Reusable Workflow` also runs (it listens to `pull_request`).

**Bonus:** Settings → Branches → Add branch protection rule for `main` →
"Require status checks to pass" → select `lint` and `test (py3.12)`.
Now push a failing test to the PR: the **Merge** button is blocked.

Merge the PR when green → the merge is a push to `main` → it deploys.

## 4. Path filters 📁

Edit only `README.md` and push to `main`. `02 · CI` does **not** run (look at its
`paths:` filter), but `01` and `03` do (they have no filter).

## 5. Manual run with inputs 🎛️

Actions → **04 · Manual Run** → **Run workflow**. Try:

1. `environment = production` → see which steps ran and which were skipped.
2. `simulate_failure = true` → the "Runs only if everything succeeded" step is
   skipped, the `failure()` and `always()` steps run.

## 6. Secrets and variables 🔐

Settings → Secrets and variables → Actions:

- **Secrets** tab → New repository secret: `MY_SECRET` = `super-secret-123`
- **Variables** tab → New repository variable: `APP_COLOR` = `green`

Run `04` again. The secret is printed as `***` — GitHub masks it. The variable
is printed normally.

## 7. Cut a release 📦

```bash
git checkout main && git pull
git tag v1.0.0
git push origin v1.0.0
```

`08 · Release` runs. When done, look at the **Releases** section on the repo home
page — there's a zip file attached and auto-generated release notes.

## 8. Write your own workflow ✍️

Create `.github/workflows/09-my-first.yml` that:

1. Runs on `workflow_dispatch` with a `name` string input.
2. Has job `count` that checks out the code and prints how many lines are in
   `app/calculator.py` (`wc -l app/calculator.py`).
3. Has job `greet` that runs **after** `count` and prints `Hello, <name>!`.
4. Has a step that only runs if `name` is `admin`.

<details>
<summary>Solution</summary>

```yaml
name: "09 · My First"
on:
  workflow_dispatch:
    inputs:
      name:
        type: string
        default: world
jobs:
  count:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: wc -l app/calculator.py
  greet:
    needs: count
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello, ${{ inputs.name }}!"
      - if: inputs.name == 'admin'
        run: echo "Welcome back, admin."
```
</details>

## 9. Extra challenges 🏆

- Add `windows-latest` and `macos-latest` to the matrix in `02-ci.yml`
  (hint: `matrix: { os: [...], python-version: [...] }` and `runs-on: ${{ matrix.os }}`).
  How many jobs run now?
- Add a manual approval before deploy: Settings → Environments → `github-pages`
  → Required reviewers → add yourself. Push to main and approve the deploy.
- Make the test job fail if coverage is below 90%: `pytest --cov=app --cov-fail-under=90`.
  (Current coverage is ~86%, so it will fail. Write tests for `app/build_site.py` until it passes!)

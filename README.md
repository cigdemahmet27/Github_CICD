# Learn GitHub Actions — a working CI/CD example

A tiny Python app wrapped in a **real CI/CD pipeline**. Every workflow file is
a numbered lesson with comments that explain each line. Push it to GitHub,
open the **Actions** tab, and watch it all run.

```
            push / pull request
                    │
                    ▼
  ┌────────┐   ┌────────┐   ┌────────┐   ┌──────────────────┐
  │  lint  │──▶│  test  │──▶│ build  │──▶│ deploy (Pages)   │──▶ live website
  └────────┘   └────────┘   └────────┘   └──────────────────┘
   ruff         pytest       make site    only on main branch
```

## The key idea in 30 seconds

| Term | Meaning |
|---|---|
| **Workflow** | A YAML file in `.github/workflows/`. GitHub runs it automatically. |
| **Trigger** (`on:`) | *When* it runs: a push, a pull request, a schedule, a button click, a tag… |
| **Job** | A group of steps that runs on a **fresh virtual machine** (a *runner*). Jobs run in parallel unless you chain them with `needs:`. |
| **Step** | One command (`run:`) or one reusable action (`uses:`). Steps run in order; if one fails, the job stops. |
| **Action** | Ready-made building block, e.g. `actions/checkout` (get the code), `actions/setup-python`. |
| **Artifact** | A file saved from a run (reports, builds). Also how jobs share files, since each job is a separate machine. |
| **Secret** | An encrypted value (API key, password). Masked as `***` in logs. |

**CI** (Continuous Integration) = automatically lint + test every change.
**CD** (Continuous Delivery/Deployment) = automatically build and ship it if the tests pass.

## Project layout

```
app/calculator.py          the code being tested
app/build_site.py          builds the web page that gets deployed
tests/                     pytest tests
.github/workflows/
  01-hello-world.yml       anatomy: triggers, jobs, steps, contexts
  02-ci.yml                lint + test, matrix, cache, artifacts, concurrency
  03-full-pipeline.yml     lint → test → build → deploy, needs, outputs, if, environments
  04-manual-inputs.yml     button-triggered with a form, secrets, failure()/always()
  05-scheduled.yml         cron schedule
  06-reusable-tests.yml    a reusable workflow (like a function)
  07-use-reusable.yml      calling the reusable workflow
  08-release.yml           create a GitHub Release when you push a tag
docs/EXERCISES.md          hands-on exercises — do these!
Makefile                   run the same steps on your own machine
```

## Step 1 — Run it locally first

The pipeline only runs commands you could run yourself. Try them:

```bash
make install     # create .venv and install pytest, ruff
make lint        # = the "lint" job
make test        # = the "test" job
make build       # = the "build" job → open site/index.html in a browser
```

## Step 2 — Put it on GitHub

1. Create a **new empty repository** on github.com (no README), e.g. `github-cicd-demo`. Make it **public** (free Pages + unlimited Actions minutes).
2. Push this project:
   ```bash
   git branch -M main
   git add .
   git commit -m "Initial CI/CD demo"
   git remote add origin https://github.com/<your-username>/github-cicd-demo.git
   git push -u origin main
   ```
3. Turn on Pages: repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
   (If the first deploy failed because Pages was off, just re-run it: Actions → the run → *Re-run jobs*.)

## Step 3 — Watch it run

Open the **Actions** tab. You'll see several workflows start from that one push:

- **01 · Hello World** — click into it, open each step, read the log. Compare with the YAML.
- **02 · CI** — notice `lint` and the 3 `test` jobs run **in parallel**. Scroll down on the run page to find the **Artifacts** (coverage reports).
- **03 · Full Pipeline** — the graph shows the **chain** `lint → test → build → deploy`. When done, the `deploy` box shows the URL of your live site. Open it: it shows the commit SHA and run number that built it.

Then trigger the others by hand: **Actions → pick workflow → Run workflow**.

## Step 4 — Learn by breaking things

Go to **[docs/EXERCISES.md](docs/EXERCISES.md)**. You'll make a test fail, open a pull
request, watch the pipeline block the deploy, add a secret, cut a release, and more.

## Where to look on GitHub

| What | Where |
|---|---|
| All runs | **Actions** tab |
| A job's logs | click a run → click the job → expand steps |
| Downloadable files | bottom of a run's summary page → **Artifacts** |
| Deployments | repo home page, right sidebar → **Deployments** |
| Secrets & variables | **Settings → Secrets and variables → Actions** |
| PR check results | bottom of any pull request ("Checks") |
| Require CI before merging | **Settings → Branches → Add rule → Require status checks** |

## Cheat sheet

```yaml
on: [push, pull_request]               # triggers
on: { schedule: [{ cron: "0 3 * * *" }] }
on: { workflow_dispatch: {} }           # manual button

jobs:
  a:
    runs-on: ubuntu-latest              # or windows-latest, macos-latest
  b:
    needs: a                            # run after a
    if: github.ref == 'refs/heads/main' # condition
    strategy:
      matrix: { version: [1, 2, 3] }    # run 3 times
    steps:
      - uses: actions/checkout@v5
      - run: echo "${{ matrix.version }} ${{ secrets.TOKEN }}"
      - run: echo "key=value" >> "$GITHUB_OUTPUT"   # step output
      - run: echo "# Hi" >> "$GITHUB_STEP_SUMMARY"  # summary page
      - if: failure()                    # also: always(), success(), cancelled()
        run: echo "something broke"
```

Official docs: https://docs.github.com/actions

# Evals

- `evals.json`: the tuned evals (iterations 1-2). `heldout.json`: held-out evals, never used for tuning.
- `files/`, `heldout/`: synthetic inputs with planted errors; safe to publish.

## Run protocol (avoid leaking answers)

Never put `eval_metadata.json` (it holds the assertions) inside a run folder while agents run.
Keep it in `workspace/<iteration>/_meta/` and copy it into `eval-*/` and `*/run-1/` only after all
runs finish, just before grading and `generate_review.py`. In heldout-1 the file was present and all
four no-skill baselines read it, so their scores there are inflated.

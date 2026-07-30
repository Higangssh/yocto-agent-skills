# Evaluations

Two layers, one manual and one machine-runnable.

## `prompts.md` — manual forward tests

A prompt list with, for each one, what a good answer has to do. Paste a prompt into an
agent with the skills installed and check the answer against the stated criteria. This is
the layer that works today and needs no tooling.

## `cases/` — runnable eval cases

```text
cases/<case-name>/
├── prompt.md              # the user turn
└── graders/
    └── correctness.md     # pass criteria, automatic fails, and score improvers
```

Intended to run with `claude plugin eval`, which scores cases against the plugin and can
run a no-plugin baseline arm (`--ablation with-without`) to show whether the skills
actually change the answer.

**Status: not yet executed.** `claude plugin eval` reports `plugin eval is currently in
early access`, so these cases have never been run and the layout follows
`claude plugin eval --help` rather than a published schema. Treat the directory structure
as provisional and expect to adjust it once the runner is generally available.

The graders are useful regardless. Each one states what a correct answer must contain and
which answers fail outright, so they double as review rubrics for the manual pass.

### Choosing cases

Cases target the mistakes a model makes without the skills, not Yocto trivia. A good case
has a plausible wrong answer that a general model reliably produces:

- `package-not-in-image`: `DEPENDS` in an image recipe, where the tempting answer is a
  rebuild or a clean.
- `installed-vs-shipped`: a QA error where the tempting answer is `INSANE_SKIP`.

Both fail loudly if the model reaches for a generic Linux fix, which is what makes them
worth scoring.

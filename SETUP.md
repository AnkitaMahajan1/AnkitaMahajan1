# Setup: AnkitaMahajan1 GitHub profile

1. Create a **public** repository named exactly `AnkitaMahajan1`. It must match your GitHub username.
2. Upload the contents of this package to the repository root, preserving `assets/`, `scripts/` and `.github/workflows/`.
3. Open **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and save.
4. Open **Actions → Refresh profile graphics → Run workflow**. After a successful run, an `output` branch will contain `stats.svg` and the contribution-snake SVGs.
5. Refresh your profile. The README is already configured to load the generated graphics from that branch.

## Personalize it
- Rewrite the bio to match your real experience.
- Keep only technology icons for tools you have actually used.
- Replace the featured project placeholders with real repository links, screenshots and measurable outcomes.
- Pin 3–6 strong repositories on your GitHub profile.

## Notes
- The workflow uses GitHub's built-in `GITHUB_TOKEN`; no personal access token is needed.
- If publishing fails, check that Actions are enabled and workflow permissions are set to read/write.
- If the generated images show 404, wait for the first workflow run to finish.
- Scheduled runs use UTC and can be delayed by GitHub during high load.

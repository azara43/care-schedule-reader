# Before you push this to GitHub

Two placeholders are left for you to fill in. Run this from the repo root,
replacing the two values with your own:

```bash
GH_USER="your-github-username"
EMAIL="the-address-you-want-public"

grep -rl 'YOUR_GITHUB_USERNAME' . | xargs sed -i '' "s|YOUR_GITHUB_USERNAME|$GH_USER|g"   # macOS
grep -rl 'YOUR_EMAIL'           . | xargs sed -i '' "s|YOUR_EMAIL|$EMAIL|g"                # macOS
# On Linux/WSL use `sed -i` without the '' argument.
```

**About the email**: it goes in `marketplace.json` and will be public. If you
would rather not publish a personal address, delete the `"email"` line from
`.claude-plugin/marketplace.json` entirely — it is optional.

Then:

```bash
git init
git add .
git commit -m "care-schedule-reader v0.1.0"
git branch -M main
git remote add origin git@github.com:$GH_USER/care-schedule-reader.git
git push -u origin main
```

## Check before every push

- [ ] `git status` shows no `legend.md`, no photos, nothing from your own household
- [ ] The only image committed is `examples/sample-schedule.png` (fictional)
- [ ] `grep -ri "YOUR_" .` returns nothing

## Regenerating the sample image

```bash
cd examples && python3 make_sample.py
```
Requires Pillow. The output is deterministic (fixed random seed), so re-running
produces the same image.

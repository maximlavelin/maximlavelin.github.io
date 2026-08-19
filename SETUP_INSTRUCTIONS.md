# Exact steps to get this live at maxim-lavelin.github.io

## 1. Create the repo (name matters!)
On GitHub, create a new repository named **exactly**:
```
maxim-lavelin.github.io
```
This exact name (username + `.github.io`) is what makes GitHub serve it as your root
personal site instead of `username.github.io/reponame`. Do NOT name it anything else.

## 2. Add your files
Unzip the folder I gave you. You should have:
```
maxim-lavelin.github.io/
├── index.html
├── assets/
│   ├── style.css
│   ├── NYC_TAXI_Lavelin.pdf          ← copy your real PDF here
│   ├── NYC_CODE_LAVELIN.ipynb        ← copy your real notebook here
│   └── Maxim_Lavelin_CV.pdf          ← add your resume here
└── projects/
    ├── nyc-taxi.html
    ├── vehicle-safety.html
    ├── retail-consultant.html
    ├── transit-accessibility.html
    └── web-tracking.html
```

**For each of the other 4 projects**, also copy in:
- The report PDF and notebook (`.ipynb`) into `assets/`
- Update the `href="#"` placeholders in that project's HTML page to point to the real files,
  e.g. `href="../assets/vehicle-safety-report.pdf"`

## 3. Fill in the bracketed placeholders
I left `[X.XX]`, `[N]`, `[value]` etc. in 4 of the 5 project pages (everything except NYC Taxi,
which I filled from your actual report). Search each HTML file for `[` and replace with your
real numbers from each report — this is the single most important step. Never leave a bracket
placeholder live on the public site.

## 4. Export key plots as images (recommended, not required)
Each project page has room for a figure but none are embedded yet. For each project:
1. Open the notebook, re-render your best 1-2 plots
2. Save as PNG into `assets/` (e.g. `assets/taxi-actual-vs-predicted.png`)
3. In the HTML, inside `<article class="body-content">`, add:
```html
<figure class="fig">
  <img src="../assets/taxi-actual-vs-predicted.png" alt="Actual vs predicted demand">
  <figcaption>Actual vs. XGBoost predicted demand, November 2024</figcaption>
</figure>
```

## 5. Push to GitHub
```bash
cd maxim-lavelin.github.io
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/maxim-lavelin/maxim-lavelin.github.io.git
git push -u origin main
```

## 6. Enable Pages (usually automatic for this repo name)
Go to repo → Settings → Pages → confirm source is "Deploy from branch: main / root".
Site goes live at `https://maxim-lavelin.github.io` within ~1 minute.

## 7. Update links elsewhere
- LinkedIn "Featured" section → add the site URL
- Resume → add the site URL under your name/contact line
- GitHub profile README (optional) → link to it

## 8. Fix real links still needed
- `mailto:` links use your BIU email — swap for whichever email you want employers to use
- `href="https://github.com/maxim-lavelin"` in the footer — confirm this is your actual GitHub username
- LinkedIn `href="#"` in the footer — add your real profile URL

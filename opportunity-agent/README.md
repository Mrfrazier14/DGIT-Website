# DGIT opportunity tracker

This starter searches federal contract notices and remote federal IT jobs, ranks likely matches, and writes a review report. It does not send email, submit bids, or apply for jobs.

## Set up

1. Install Python 3.10 or newer.
2. Obtain a SAM.gov public opportunities API key in your SAM.gov account. Obtain a USAJOBS API key at developer.usajobs.gov if you want federal job results. USAJOBS requires the email used to request that key as an API header; it is used only for API authentication, not for messaging.
3. In PowerShell, set credentials for this session:

```powershell
$env:SAM_API_KEY = 'YOUR_SAM_KEY'
$env:USAJOBS_API_KEY = 'YOUR_USAJOBS_KEY'
$env:USAJOBS_API_EMAIL = 'EMAIL_USED_FOR_USAJOBS_KEY'
python .\opportunity_agent.py
```

The report is written to `opportunities.md`. Only SAM results are fetched when USAJOBS credentials are absent. No keys are written to disk by this script.

The same results are saved to `opportunities.json` for the dashboard. To view the dashboard locally, run `python -m http.server 8000` from this folder and open `http://localhost:8000`. Run the tracker again whenever you want fresh results.

Edit `config.json` to add your verified website URL, tune the keywords, or change the minimum score. The website field is blank until you provide the exact DGIT Services URL.

Review each original notice for eligibility, set-aside, place of performance, and response instructions before pursuing it. A search result is never a bid submission.

The dashboard is a local review tool. It does not run scheduled searches or provide secure login. Keep `opportunities.json` private if live results or notes should not be public. Do not commit API keys, client information, or private proposal drafts to GitHub.


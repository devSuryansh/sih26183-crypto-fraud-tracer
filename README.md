# SIH26183 – Real-Time Identification of Fraud-Linked Cryptocurrency Exchanges from Victim-Reported Suspect Wallet Addresses through Automated Blockchain Analytics

- **PS id:** SIH26183
- **Organization:** Ministry of Home Affairs (I4C)
- **Theme:** Blockchain & Cybersecurity | **Track:** Software

Enter a victim-reported suspect wallet; the app traces fund flow over a transaction graph and ranks the most likely exchanges with confidence and paths.

## Requirements → code

| Requirement | Where |
|---|---|
| Accept victim-reported suspect wallet | `/api/trace?wallet=`, input box in `templates/index.html` |
| Automated blockchain analytics (graph tracing) | `tracer.trace` (networkx DiGraph, hop-limited path walk, proportional value share) |
| Identify exchanges | labelled sample exchange address list in `data/sample_graph.json` |
| Rank / confidence | per-exchange score with hop decay, normalised confidence |
| Show evidence | all paths and hop counts returned and displayed |
| "Real-time" | on-demand API; a live node/indexer feed would replace `tracer.load` |

## Run locally
```
pip install -r requirements.txt
python app.py          # http://127.0.0.1:5002  (try wallet 0xSUSPECT)
pip install pytest && pytest
```
Regenerate sample data: `python gen_data.py`.

## Limitations
All addresses, transactions and exchange labels are **synthetic samples**; no real blockchain or exchange data is used. Scoring is a simple heuristic, not forensic evidence.

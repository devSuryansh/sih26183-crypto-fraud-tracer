import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__))); os.chdir(os.path.dirname(os.path.dirname(__file__)))
import app as A

def test_suspect_ranks_alpha_first():
    r = A.app.test_client().get("/api/trace?wallet=0xSUSPECT").get_json()
    assert r["ranked_exchanges"][0]["exchange_id"] == "EXCH_ALPHA"
    assert abs(sum(e["confidence"] for e in r["ranked_exchanges"]) - 1) < 0.01

def test_unknown_wallet_404():
    assert A.app.test_client().get("/api/trace?wallet=nope").status_code == 404

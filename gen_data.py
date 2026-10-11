"""Build SYNTHETIC transaction graph + labelled SAMPLE exchange list. All addresses are fake."""
import json, random
random.seed(7)
exch = {"EXCH_ALPHA": "Alpha Exchange (sample)", "EXCH_BETA": "Beta Exchange (sample)", "EXCH_GAMMA": "Gamma Exchange (sample)"}
labels = {"0xEXA1": "EXCH_ALPHA", "0xEXA2": "EXCH_ALPHA", "0xEXB1": "EXCH_BETA", "0xEXG1": "EXCH_GAMMA"}
tx = []
def t(a, b, amt): tx.append({"from": a, "to": b, "amount": amt})
# scam case: victims -> suspect -> mule layers -> mostly Alpha, some Beta
for v in ("0xVICTIM1", "0xVICTIM2"): t(v, "0xSUSPECT", 5.0)
t("0xSUSPECT", "0xMULE1", 6); t("0xSUSPECT", "0xMULE2", 3); t("0xSUSPECT", "0xMULE3", 1)
t("0xMULE1", "0xMULE4", 3); t("0xMULE1", "0xEXA1", 3); t("0xMULE2", "0xMULE4", 3)
t("0xMULE4", "0xEXA2", 5); t("0xMULE4", "0xMULE5", 1); t("0xMULE5", "0xEXB1", 1)
t("0xMULE3", "0xEXB1", 1)
# unrelated noise
for i in range(40):
    a, b = f"0xN{random.randrange(15)}", f"0xN{random.randrange(15)}"
    if a != b: t(a, b, round(random.uniform(.1, 3), 2))
t("0xN3", "0xEXG1", 2)
json.dump({"exchanges": exch, "labels": labels, "transactions": tx}, open("data/sample_graph.json", "w"), indent=1)

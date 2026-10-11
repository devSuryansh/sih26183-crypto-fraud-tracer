"""Trace suspect wallet -> labelled exchange deposit addresses over a SYNTHETIC graph.
Score = sum over simple paths (<= max_hops) of proportional value share * decay**hops; normalised to confidence."""
import json, networkx as nx

def load(path="data/sample_graph.json"):
    d = json.load(open(path)); g = nx.DiGraph()
    for t in d["transactions"]:
        if g.has_edge(t["from"], t["to"]): g[t["from"]][t["to"]]["amount"] += t["amount"]
        else: g.add_edge(t["from"], t["to"], amount=t["amount"])
    return g, d["labels"], d["exchanges"]

def trace(g, labels, names, wallet, max_hops=6, decay=0.85):
    if wallet not in g: return None
    scores, paths = {}, {}
    def walk(node, path, share):
        if len(path) - 1 >= max_hops: return
        out = sum(g[node][n]["amount"] for n in g.successors(node))
        for n in g.successors(node):
            if n in path: continue
            s = share * g[node][n]["amount"] / out; p = path + [n]
            if n in labels:
                ex = labels[n]; sc = s * decay ** (len(p) - 1)
                scores[ex] = scores.get(ex, 0) + sc
                paths.setdefault(ex, []).append({"hops": len(p) - 1, "share": round(s, 3), "path": p})
            else: walk(n, p, s)
    walk(wallet, [wallet], 1.0)
    total = sum(scores.values()) or 1
    ranked = [{"exchange_id": e, "exchange": names[e], "score": round(s, 4), "confidence": round(s / total, 3),
               "paths": sorted(paths[e], key=lambda p: -p["share"])} for e, s in sorted(scores.items(), key=lambda x: -x[1])]
    return {"wallet": wallet, "ranked_exchanges": ranked}

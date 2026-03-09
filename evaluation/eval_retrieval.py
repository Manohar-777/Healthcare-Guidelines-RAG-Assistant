
import csv, os, requests
APP = os.getenv("APP_URL","http://localhost:9070")
def run():
    ok=0; total=0
    with open("evaluation/queries_custom.csv") as f:
        for row in csv.DictReader(f):
            q=row["question"]; exp=row["expected"].lower()
            r=requests.post(f"{APP}/qa", json={"question":q,"top_k":5}).json()
            cits=r.get("citations",[])
            hit=any(exp in c.get("path","").lower() or exp in c.get("section","").lower() for c in cits)
            ok+=int(hit); total+=1
    print(f"Precision@1 (proxy): {ok}/{total} = {ok/total if total else 0:.2f}")
if __name__ == "__main__":
    run()

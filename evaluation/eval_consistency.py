
import csv, os, requests
APP = os.getenv("APP_URL","http://localhost:9070")
def run():
    conf=[]; passed=0; total=0
    with open("evaluation/queries_custom.csv") as f:
        for row in csv.DictReader(f):
            q=row["question"]
            r=requests.post(f"{APP}/qa", json={"question":q,"top_k":5}).json()
            conf.append(float(r.get("confidence",0)))
            passed+=int(r.get("status","needs_review")=="validated")
            total+=1
    mean_conf = sum(conf)/len(conf) if conf else 0.0
    print(f"Mean confidence: {mean_conf:.2f}")
    print(f"Validation pass rate @0.6: {passed}/{total} = {passed/total if total else 0:.2f}")
if __name__ == "__main__":
    run()

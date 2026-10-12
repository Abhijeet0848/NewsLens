import urllib.request
import json

tests = [
    ("Business", "Wall Street rallied on Monday as inflation slowed and the Federal Reserve indicated potential interest rate cuts later this year. S&P 500 gained 1.2% while banking stocks surged."),
    ("Tech", "OpenAI announced a new neural network architecture with improved reasoning benchmarks and reduced latency across complex coding tasks on personal computers and servers."),
    ("Politics", "Parliament debated the new taxation bill on Wednesday as prime minister and opposition leaders clashed over government spending and national budget deficits."),
    ("Sport", "Real Madrid secured their 15th Champions League title on Saturday, defeating Borussia Dortmund 2-0 at Wembley Stadium. Goals from Dani Carvajal and Vinicius Junior sealed the victory.")
]

for expected, text in tests:
    data = json.dumps({"text": text, "model": "linear-svm"}).encode()
    req = urllib.request.Request("http://localhost:8000/api/classify", data=data, headers={"Content-Type": "application/json"})
    res = urllib.request.urlopen(req)
    out = json.loads(res.read().decode())
    print(f"Expected: {expected:<12} -> Predicted: {out['category']:<12} ({out['confidence']*100:.1f}%)")
    print(f"  Distribution: {out['all_scores']}\n")

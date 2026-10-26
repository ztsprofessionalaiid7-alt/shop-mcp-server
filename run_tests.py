import json
import sys

import server

TOOLS = {
    "search_orders": server.search_orders,
    "get_order": server.get_order,
    "get_customer_orders": server.get_customer_orders,
    "customer_summary": server.customer_summary,
}


def run(path):
    passed = total = 0
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        case = json.loads(line)
        total += 1
        inp = case["input"]
        try:
            out = TOOLS[inp["tool"]](**inp["args"])
        except Exception as e:
            out = {"exception": str(e)}
        text = json.dumps(out, ensure_ascii=False)
        ok = case["expected"] in text
        passed += ok
        print("PASS" if ok else "FAIL", case["tag"], inp["tool"], inp["args"], "->", text[:150])
    print(f"{passed}/{total}")


run(sys.argv[1])

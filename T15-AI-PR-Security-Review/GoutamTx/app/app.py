from flask import Flask, request
from utils import dangerous_eval

app = Flask(__name__)

@app.get("/hello")
def hello():
    name = request.args.get("name", "world")
    return f"Hello, {name}!"

@app.get("/demo")
def demo():
    return "This is a demo endpoint"

@app.post("/calc")
def calc():
    expr = request.json.get("expr", "0")
    # Intentionally insecure: Snyk Code should flag this
    return {"result": dangerous_eval(expr)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


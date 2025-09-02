# Intentionally insecure helper that Snyk should report

def dangerous_eval(expr: str):
    return eval(expr)  # nosec – intentionally vulnerable for demo


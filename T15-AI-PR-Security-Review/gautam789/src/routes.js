const express = require("express");
const router = express.Router();
const { runCommand, unsafeEval } = require("./utils");

// ❌ Command Injection
router.get("/exec", (req, res) => {
  const userInput = req.query.cmd;
  runCommand(userInput, res);
});

// ❌ XSS Vulnerability
router.get("/greet", (req, res) => {
  const name = req.query.name || "Guest";
  res.send(`<h1>Hello ${name}</h1>`); // unsanitized
});

// ❌ Dangerous eval
router.get("/calc", (req, res) => {
  const expr = req.query.expr;
  res.send("Result: " + unsafeEval(expr));
});

module.exports = router;


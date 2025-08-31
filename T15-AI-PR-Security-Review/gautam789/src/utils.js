const { exec } = require("child_process");

// Command injection
function runCommand(cmd, res) {
  exec(cmd, (err, stdout, stderr) => {
    if (err) res.send("Error: " + err.message);
    else res.send("Output: " + stdout);
  });
}

// Dangerous eval
function unsafeEval(input) {
  return eval(input); // ⚠️ vulnerable
}

module.exports = { runCommand, unsafeEval };


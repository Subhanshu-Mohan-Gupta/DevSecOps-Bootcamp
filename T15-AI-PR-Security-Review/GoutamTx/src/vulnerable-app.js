const express = require('express');
const mysql = require('mysql2');
const crypto = require('crypto');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

// Hardcoded secrets - should trigger critical findings
const API_KEY = "sk-1234567890abcdef";
const DATABASE_PASSWORD = "admin123"; 
const JWT_SECRET = "my-super-secret-jwt-key";

// SQL Injection vulnerability
app.get('/user/:id', (req, res) => {
    const connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: DATABASE_PASSWORD,
        database: 'users'
    });
    
    // Direct SQL injection - should trigger high severity
    const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
    connection.execute(query, (err, results) => {
        res.json(results);
    });
});

// Command Injection vulnerability  
app.post('/execute', (req, res) => {
    const command = req.body.command;
    
    // Command injection - should trigger critical
    exec(`ls -la ${command}`, (error, stdout, stderr) => {
        res.send(stdout);
    });
});

// XSS vulnerability
app.get('/welcome', (req, res) => {
    const name = req.query.name;
    
    // Reflected XSS - should trigger high severity
    res.send(`<h1>Welcome ${name}!</h1>`);
});

// Weak cryptography
function weakHash(data) {
    // MD5 is cryptographically broken - should trigger medium/high
    return crypto.createHash('md5').update(data).digest('hex');
}

// Insecure random generation
function generateToken() {
    // Math.random() is not cryptographically secure
    return Math.random().toString(36).substring(7);
}

// Path Traversal vulnerability
app.get('/file', (req, res) => {
    const filename = req.query.file;
    
    // Path traversal - should trigger high severity
    res.sendFile(__dirname + '/files/' + filename);
});

// Eval injection - extremely dangerous
app.post('/calculate', (req, res) => {
    const expression = req.body.expr;
    
    // Code injection via eval - should trigger critical
    const result = eval(expression);
    res.json({ result });
});

// Insecure HTTP headers and settings
app.listen(3000, '0.0.0.0', () => {
    console.log('Server running on http://0.0.0.0:3000');
});

module.exports = app;


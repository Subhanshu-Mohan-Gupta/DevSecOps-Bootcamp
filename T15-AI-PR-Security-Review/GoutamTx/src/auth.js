const crypto = require('crypto');

// Hardcoded encryption key - should trigger critical
const ENCRYPTION_KEY = "1234567890123456";

// Weak password hashing
function hashPassword(password) {
    // Using deprecated and weak hashing - should trigger high
    return crypto.createHash('sha1').update(password).digest('hex');
}

// Timing attack vulnerability
function comparePasswords(input, stored) {
    // Not using constant-time comparison - should trigger medium
    return input === stored;
}

// Insecure session management
function generateSessionId() {
    // Predictable session IDs - should trigger high
    return Date.now().toString() + Math.random().toString();
}

module.exports = {
    hashPassword,
    comparePasswords,
    generateSessionId
};


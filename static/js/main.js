// SQL Injection Demo
async function testVulnerable() {
    const username = document.getElementById('vulnUsername').value;
    const response = await fetch('/sqli/vulnerable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}`
    });
    
    const data = await response.json();
    document.getElementById('vulnResult').innerHTML = `
        <strong>Query executed:</strong><br>
        <code>${data.query}</code><br><br>
        <strong>Results (${data.users.length} found):</strong><br>
        <pre>${JSON.stringify(data.users, null, 2)}</pre>
    `;
}

async function testSecure() {
    const username = document.getElementById('secureUsername').value;
    const response = await fetch('/sqli/secure', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}`
    });
    
    const data = await response.json();
    document.getElementById('secureResult').innerHTML = `
        <strong>Query executed:</strong><br>
        <code>SELECT * FROM users WHERE username = ?</code><br>
        <code>Parameter: "${username}"</code><br><br>
        <strong>Results (${data.users.length} found):</strong><br>
        <pre>${JSON.stringify(data.users, null, 2)}</pre>
    `;
}

// XSS Demo
async function testXSSVulnerable() {
    const comment = document.getElementById('vulnComment').value;
    const response = await fetch('/xss/vulnerable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `comment=${encodeURIComponent(comment)}`
    });
    
    const data = await response.json();
    document.getElementById('vulnXssResult').innerHTML = `
        <strong>User comment:</strong><br>
        ${data.comment}<br><br>
        <strong>Try this payload:</strong><br>
        <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>
    `;
}

async function testXSSSecure() {
    const comment = document.getElementById('secureComment').value;
    const response = await fetch('/xss/secure', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `comment=${encodeURIComponent(comment)}`
    });
    
    const data = await response.json();
    document.getElementById('secureXssResult').innerHTML = `
        <strong>User comment (escaped):</strong><br>
        ${data.comment}<br><br>
        <strong>Raw HTML:</strong><br>
        <code>${data.comment}</code>
    `;
}

// CSRF Demo
function testCSRFVulnerable() {
    // Create a hidden form (simulates an attacker's site)
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/csrf/vulnerable/transfer';
    form.target = '_blank';
    
    // Hidden inputs
    const amountInput = document.createElement('input');
    amountInput.type = 'hidden';
    amountInput.name = 'amount';
    amountInput.value = '5000';
    
    const accountInput = document.createElement('input');
    accountInput.type = 'hidden';
    accountInput.name = 'to_account';
    accountInput.value = 'hacker456';
    
    form.appendChild(amountInput);
    form.appendChild(accountInput);
    
    // Submit the form
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
    
    document.getElementById('maliciousResult').innerHTML = 
        '<span style="color: #dc2626;">⚠️ Malicious request sent! The vulnerable form accepted it.</span>';
}

async function testCSRFSecure() {
    try {
        const response = await fetch('/csrf/secure/transfer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'amount=9999&to_account=hacker'
        });
        
        if (response.status === 400) {
            document.getElementById('secureResult').innerHTML = 
                '<span style="color: #16a34a;">✅ Blocked! CSRF token missing (400 Bad Request)</span>';
        } else {
            const text = await response.text();
            document.getElementById('secureResult').innerHTML = 
                `<span style="color: #dc2626;">❌ Request succeeded: ${text}</span>`;
        }
    } catch (error) {
        document.getElementById('secureResult').innerHTML = 
            '<span style="color: #16a34a;">✅ Blocked by CSRF protection!</span>';
    }
}

// Input Validation Demo
async function testValidationVulnerable() {
    const email = document.getElementById('vulnEmail').value;
    const age = document.getElementById('vulnAge').value;
    
    const response = await fetch('/validation/vulnerable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(email)}&age=${encodeURIComponent(age)}`
    });
    
    const data = await response.json();
    const resultDiv = document.getElementById('vulnValidationResult');
    
    if (data.status === 'accepted') {
        resultDiv.innerHTML = `
            <div style="color: var(--success);">
                <strong>✓ Data accepted:</strong><br>
                Email: ${data.email}<br>
                Age: ${data.age}
            </div>
            <div class="warning" style="color: var(--warning); margin-top: 1rem;">
                ⚠️ Warning: No validation performed!
            </div>
        `;
    }
}

async function testValidationSecure() {
    const email = document.getElementById('secureEmail').value;
    const age = document.getElementById('secureAge').value;
    
    const response = await fetch('/validation/secure', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(email)}&age=${encodeURIComponent(age)}`
    });
    
    const data = await response.json();
    const resultDiv = document.getElementById('secureValidationResult');
    
    if (data.status === 'error') {
        resultDiv.innerHTML = `
            <div style="color: var(--danger);">
                <strong>✗ Validation errors:</strong><br>
                <ul>
                    ${data.errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            </div>
            <div style="color: var(--success); margin-top: 1rem;">
                ✓ Input validation is working!
            </div>
        `;
    } else {
        resultDiv.innerHTML = `
            <div style="color: var(--success);">
                <strong>✓ Data accepted:</strong><br>
                Email: ${data.email}<br>
                Age: ${data.age}
            </div>
        `;
    }
}
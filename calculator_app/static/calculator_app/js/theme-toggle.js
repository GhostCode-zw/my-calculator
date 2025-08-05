// Theme Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        if (themeToggle) themeToggle.checked = true;
    }
    
    // Theme toggle event listener
    if (themeToggle) {
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                body.classList.add('light-theme');
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.remove('light-theme');
                localStorage.setItem('theme', 'dark');
            }
        });
    }
    
    // Add smooth transitions
    body.style.transition = 'all 0.5s ease';
});

// Calculator functionality
class NeonCalculator {
    constructor() {
        this.display = document.getElementById('display');
        this.history = document.getElementById('history');
        this.currentValue = '0';
        this.previousValue = '';
        this.operation = null;
        this.shouldResetDisplay = false;
        
        this.init();
    }
    
    init() {
        this.updateDisplay();
        this.bindEvents();
    }
    
    bindEvents() {
        document.querySelectorAll('.neon-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const value = e.target.dataset.value || e.target.textContent;
                this.handleInput(value);
            });
        });
        
        // Keyboard support
        document.addEventListener('keydown', (e) => {
            this.handleKeyPress(e);
        });
    }
    
    handleInput(value) {
        if (value >= '0' && value <= '9') {
            this.appendNumber(value);
        } else if (value === '.') {
            this.appendDecimal();
        } else if (value === 'C') {
            this.clear();
        } else if (value === '←') {
            this.delete();
        } else if (['+', '-', '×', '÷'].includes(value)) {
            this.setOperation(value);
        } else if (value === '=') {
            this.calculate();
        }
    }
    
    appendNumber(number) {
        if (this.shouldResetDisplay) {
            this.currentValue = '';
            this.shouldResetDisplay = false;
        }
        
        if (this.currentValue === '0') {
            this.currentValue = number;
        } else {
            this.currentValue += number;
        }
        this.updateDisplay();
    }
    
    appendDecimal() {
        if (this.shouldResetDisplay) {
            this.currentValue = '0';
            this.shouldResetDisplay = false;
        }
        
        if (!this.currentValue.includes('.')) {
            this.currentValue += '.';
        }
        this.updateDisplay();
    }
    
    clear() {
        this.currentValue = '0';
        this.previousValue = '';
        this.operation = null;
        this.history.textContent = '';
        this.updateDisplay();
    }
    
    delete() {
        if (this.currentValue.length > 1) {
            this.currentValue = this.currentValue.slice(0, -1);
        } else {
            this.currentValue = '0';
        }
        this.updateDisplay();
    }
    
    setOperation(op) {
        if (this.operation !== null) {
            this.calculate();
        }
        
        this.previousValue = this.currentValue;
        this.operation = op;
        this.shouldResetDisplay = true;
        this.history.textContent = `${this.previousValue} ${op}`;
    }
    
    calculate() {
        if (this.operation === null || this.previousValue === '') return;
        
        const prev = parseFloat(this.previousValue);
        const current = parseFloat(this.currentValue);
        let result;
        
        switch (this.operation) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '×':
                result = prev * current;
                break;
            case '÷':
                if (current === 0) {
                    alert('Cannot divide by zero!');
                    return;
                }
                result = prev / current;
                break;
            default:
                return;
        }
        
        this.history.textContent = `${this.previousValue} ${this.operation} ${this.currentValue} =`;
        this.currentValue = result.toString();
        this.operation = null;
        this.previousValue = '';
        this.shouldResetDisplay = true;
        this.updateDisplay();
    }
    
    updateDisplay() {
        if (this.display) {
            this.display.value = this.currentValue;
        }
    }
    
    handleKeyPress(e) {
        if (e.key >= '0' && e.key <= '9') {
            this.handleInput(e.key);
        } else if (e.key === '.') {
            this.handleInput('.');
        } else if (e.key === '+') {
            this.handleInput('+');
        } else if (e.key === '-') {
            this.handleInput('-');
        } else if (e.key === '*') {
            this.handleInput('×');
        } else if (e.key === '/') {
            e.preventDefault();
            this.handleInput('÷');
        } else if (e.key === 'Enter' || e.key === '=') {
            this.calculate();
        } else if (e.key === 'Backspace') {
            this.delete();
        } else if (e.key === 'Escape') {
            this.clear();
        }
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.neon-calculator')) {
        new NeonCalculator();
    }
});

// Interest Calculator functionality
class InterestCalculator {
    constructor() {
        this.form = document.getElementById('interest-form');
        this.results = document.getElementById('interest-results');
        
        if (this.form) {
            this.init();
        }
    }
    
    init() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculate();
        });
    }
    
    calculate() {
        const principal = parseFloat(document.getElementById('principal').value);
        const rate = parseFloat(document.getElementById('rate').value);
        const time = parseFloat(document.getElementById('time').value);
        
        if (isNaN(principal) || isNaN(rate) || isNaN(time)) {
            alert('Please enter valid numbers');
            return;
        }
        
        const simpleInterest = (principal * rate * time) / 100;
        const totalAmount = principal + simpleInterest;
        
        this.displayResults({
            principal: principal,
            rate: rate,
            time: time,
            interest: simpleInterest,
            total: totalAmount
        });
    }
    
    displayResults(data) {
        if (!this.results) return;
        
        this.results.innerHTML = `
            <div class="neon-result-card">
                <div class="neon-result-item">
                    <span class="result-label">Principal Amount:</span>
                    <span class="neon-value">$${data.principal.toFixed(2)}</span>
                </div>
                <div class="neon-result-item">
                    <span class="result-label">Interest Rate:</span>
                    <span class="neon-value">${data.rate

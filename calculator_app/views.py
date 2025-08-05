from django.shortcuts import redirect, render
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import json

# Create your views here.
def home_view(request):
    return redirect('calculator_app:standard_calculator')

def standard_calculator_view(request):
    """
    View for the standard arithmetic calculator
    Handles both GET (display form) and POST (process calculation) requests
    """
    context = {
        'title': 'Standard Calculator',
        'result': None,
        'error': None
    }
    
    if request.method == 'POST':
        try:
            # Get calculation data from POST request
            expression = request.POST.get('expression', '').strip()
            
            if expression:
                # Sanitize and evaluate the expression
                # Only allow numbers, operators, parentheses, and decimal points
                allowed_chars = set('0123456789+-*/().')
                if all(c in allowed_chars or c.isspace() for c in expression):
                    # Additional check for consecutive operators
                    import re
                    if re.search(r'[\+\-\*/]{2,}', expression):
                        context['error'] = 'Invalid calculation'
                    else:
                        try:
                            result = eval(expression)
                            context['result'] = str(result)
                        except (ZeroDivisionError, SyntaxError, ValueError) as e:
                            context['error'] = 'Invalid calculation'
                else:
                    context['error'] = 'Invalid characters in expression'
            else:
                context['error'] = 'No expression provided'
                
        except Exception as e:
            context['error'] = 'Calculation error occurred'
    
    return render(request, 'calculator_app/standard_calculator.html', context)

def interest_calculator_view(request):
    """
    View for the interest rate calculator
    Calculates simple interest: Interest = (Principal * Rate * Time) / 100
    """
    context = {
        'title': 'Interest Calculator',
        'principal': '',
        'rate': '',
        'time': '',
        'interest': None,
        'total_amount': None,
        'error': None
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            principal_str = request.POST.get('principal', '').strip()
            rate_str = request.POST.get('rate', '').strip()
            time_str = request.POST.get('time', '').strip()
            
            # Preserve input values for form
            context['principal'] = principal_str
            context['rate'] = rate_str
            context['time'] = time_str
            
            # Validate inputs
            if not all([principal_str, rate_str, time_str]):
                context['error'] = 'All fields are required'
            else:
                try:
                    # Convert to Decimal for precise calculations
                    principal = Decimal(principal_str)
                    rate = Decimal(rate_str)
                    time = Decimal(time_str)
                    
                    # Validate positive values
                    if principal <= 0 or rate < 0 or time <= 0:
                        context['error'] = 'Principal and time must be positive, rate cannot be negative'
                    else:
                        # Calculate simple interest
                        interest = (principal * rate * time) / 100
                        total_amount = principal + interest
                        
                        # Format results to 2 decimal places
                        context['interest'] = f"{interest:.2f}"
                        context['total_amount'] = f"{total_amount:.2f}"
                        
                except InvalidOperation:
                    context['error'] = 'Please enter valid numbers'
                    
        except Exception as e:
            context['error'] = 'Calculation error occurred'
    
    return render(request, 'calculator_app/interest_calculator.html', context)

def installment_calculator_view(request):
    """
    View for calculating loan installments based on fixed rates and tenure using formula:
    installment = principal * (1 + (rate * tenure)) / tenure
    """
    context = {
        'title': 'Installment Calculator',
        'principal': '',
        'rate': '',
        'months': '',
        'emi': None,
        'total_payment': None,
        'total_interest': None,
        'error': None,
    }
    
    if request.method == 'POST':
        try:
            principal_str = request.POST.get('principal', '').strip()
            rate_str = request.POST.get('annual_rate', '').strip()
            months_str = request.POST.get('months', '').strip()
            
            context['principal'] = principal_str
            context['rate'] = rate_str
            context['months'] = months_str
            
            if not all([principal_str, rate_str, months_str]):
                context['error'] = 'All fields are required'
            else:
                try:
                    principal = float(principal_str)
                    rate = float(rate_str) / 100  # Convert percentage to decimal
                    months = int(months_str)
                    
                    if principal <= 0 or rate < 0 or months <= 0:
                        context['error'] = 'Principal must be positive'
                    elif rate not in [0.13, 0.15]:
                        context['error'] = 'Rate must be 13 or 15'
                    elif months < 2 or months > 12:
                        context['error'] = 'Months must be between 2 and 12'
                    else:
                        # Calculate installment using formula
                        installment = principal * (1 + (rate * months)) / months
                        total_payment = installment * months
                        total_interest = total_payment - principal
                        
                        context['emi'] = f"{installment:.2f}"
                        context['total_payment'] = f"{total_payment:.2f}"
                        context['total_interest'] = f"{total_interest:.2f}"
                except ValueError:
                    context['error'] = 'Please enter valid numbers'
        except Exception:
            context['error'] = 'Calculation error occurred'
    
    return render(request, 'calculator_app/installment_calculator.html', context)
    
    def interpolate(x0, y0, x1, y1, x):
        # Linear interpolation formula
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    
    def get_installment(principal, rate, months):
        # Get the closest lower and upper principal amounts from the table
        principals = sorted(loan_table[rate][months].keys())
        if principal <= principals[0]:
            return loan_table[rate][months][principals[0]]
        if principal >= principals[-1]:
            return loan_table[rate][months][principals[-1]]
        # Find lower and upper bounds for interpolation
        lower = max(p for p in principals if p <= principal)
        upper = min(p for p in principals if p >= principal)
        if lower == upper:
            return loan_table[rate][months][lower]
        # Interpolate between lower and upper
        return interpolate(lower, loan_table[rate][months][lower], upper, loan_table[rate][months][upper], principal)
    
    context = {
        'title': 'Installment Calculator',
        'principal': '',
        'rate': '',
        'months': '',
        'emi': None,
        'total_payment': None,
        'total_interest': None,
        'error': None,
        'valid_rates': [13, 15],
        'valid_months': list(range(2, 13))
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            principal_str = request.POST.get('principal', '').strip()
            rate_str = request.POST.get('annual_rate', '').strip()
            months_str = request.POST.get('months', '').strip()
            
            # Preserve input values for form
            context['principal'] = principal_str
            context['rate'] = rate_str
            context['months'] = months_str
            
            # Validate inputs
            if not all([principal_str, rate_str, months_str]):
                context['error'] = 'All fields are required'
            else:
                try:
                    # Convert to Decimal for precise calculations
                    principal = Decimal(principal_str)
                    rate = int(rate_str)
                    months = int(months_str)
                    
                    # Validate positive values and allowed rates/months
                    if principal <= 0 or rate not in context['valid_rates'] or months not in context['valid_months']:
                        context['error'] = 'Principal must be positive, rate must be 13 or 15, months between 2 and 12'
                    else:
                        # Calculate installment using loan table with interpolation
                        installment = get_installment(float(principal), rate, months)
                        total_payment = installment * months
                        total_interest = total_payment - float(principal)
                        
                        # Format results to 2 decimal places
                        context['emi'] = f"{installment:.2f}"
                        context['total_payment'] = f"{total_payment:.2f}"
                        context['total_interest'] = f"{total_interest:.2f}"
                        
                except (InvalidOperation, ValueError):
                    context['error'] = 'Please enter valid numbers'
                    
        except Exception as e:
            context['error'] = 'Calculation error occurred'
    
    return render(request, 'calculator_app/installment_calculator.html', context)

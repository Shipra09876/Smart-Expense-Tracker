from django.core.mail import EmailMessage

def send_report_email(user, pdf_path, month, year):
    subject = f"Smart Expense Tracker Monthly Report ({month}/{year})"
    body = f"Hi {user.username},\n\nHere is your monthly expense report for {month}/{year}. Please find the attached PDF."
    email = EmailMessage(subject, body, "noreply@expensetracker.com", [user.email])
    email.attach_file(pdf_path)
    email.send()

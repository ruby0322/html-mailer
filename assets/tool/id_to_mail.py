emails = []
while (email := input().lower()) != '-1':
    if email:
        emails.append(f'{email}@ntu.edu.tw')

for email in emails:
    print(email)
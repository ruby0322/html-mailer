import os
from config import Config
from mail import Mail
import smtplib
import ssl
from email.message import EmailMessage
import json

class Mailer:
    
    def __load_config(self) -> None:
        with open('assets/config.json', 'r') as f:
            self.config = Config(json.load(f))
    
    def __save_config(self) -> None:
        with open('assets/config.json', 'w') as f:
            json.dump(self.config.__dict__, f, indent=4)
    
    def __log(self, content: str) -> None:
        print('[Mailer]', content)

    def __init__(self) -> None:
        
        self.__load_config()
        self.mail = Mail()
        self.__reset()
        
    def __reset(self) -> None:
        with open(self.config.get_subject_full_path(), 'r', encoding='utf-8') as f:
            self.mail.subject = ''
            for line in f.readlines():
                self.mail.subject += line
        with open(self.config.get_greeting_full_path(), 'r', encoding='utf-8') as f:
            self.mail.greeting = ''
            for line in f.readlines():
                self.mail.greeting += line
        with open(self.config.get_body_full_path(), 'r', encoding='utf-8') as f:
            self.mail.body = ''
            for line in f.readlines():
                self.mail.body += line
                self.mail.body += '\n<br>\n'
        with open(self.config.get_closing_full_path(), 'r', encoding='utf-8') as f:
            self.mail.closing = ''
            for line in f.readlines():
                self.mail.closing += line
                self.mail.closing += '\n'
        with open(self.config.get_template_full_path(), 'r', encoding='utf-8') as f:
            self.mail.template = ''
            for line in f.readlines():
                self.mail.template += line
                self.mail.template += '\n'
        with open(self.config.get_sender_full_path(), 'r', encoding='utf-8') as f:
            self.mail.sender = ''
            for line in f.readlines():
                self.mail.sender += line
                self.mail.sender += '\n'
        
        self.mail.html = self.mail.template.replace('{GREETING}', self.mail.greeting).replace('{BODY}', self.mail.body).replace('{CLOSING}', self.mail.closing).replace('{SENDER}', self.mail.sender)
        
        with open(self.config.get_receiver_full_path(), 'r', encoding='utf-8') as f:
            self.receivers = []
            for email in f.readlines():
                self.receivers.append(email)
                
    def __iconfig(self) -> None:
        
        configs = os.listdir(self.config.assets_folder_path + '/mail')
        for config in configs:        
            print(f'[iConfig] Choose the {config} for your mail.')
            print('Options: ')
            dirs = os.listdir(self.config.assets_folder_path + f'/mail/{config}')
            for no in range(len(dirs)):
                print(f'{no+1}. {dirs[no]}')
            print(f'{len(dirs)+1}. Create A New File')
            while True:
                while True:
                    try:
                        action = int(input('>>> '))
                        break
                    except:
                        print('Invalid input.')
                if 0 < action <= len(dirs):
                    setattr(self.config, f'{config}_file_name', dirs[action-1])
                    break
                elif action == len(dirs) + 1:
                    print('[iConfig] Enter content(enter !QUIT to quit): ')
                    content = ''
                    line = ''
                    while (line := input('>>> ')) != '!QUIT':
                        content += line
                        content += '\n'
                    print('[iConfig] Enter file name(w/out .txt): ')
                    file_name = input('>>> ')
                    with open(self.config.assets_folder_path + f'/mail/{config}/{file_name}.txt', 'w') as wf:
                        wf.write(content)
                    setattr(self.config, f'{config}_file_name', f'{file_name}.txt')
                    break
                else:
                    print('Invalid input.')
        
        
        self.__save_config()
        self.__reset()

    def __login(self) -> None:
        self.__log('Please login your email account.')
        while '@' not in (email := input('Email: ')):
            pass
        while not (password := input('Password: ')):
            pass
        self.config.sender_email = email
        self.config.sender_password = password

        
        
    
    def command_line_interface(self) -> None:
        while True:
            self.__login()
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    self.__log('Logging in...')
                    server.login(self.config.sender_email, self.config.sender_password)
                    self.__log('Logged in successfully.')
                    break
            except:
                self.__log('Login failed. Please try again.')

        while True:
            print('='*30)
            print(f'{"CLI for Mailer by Ruby":^{30}}')
            print('='*30)
            print('Options:')
            print('1. Display mail')
            print('2. Send mail')
            print('3. Interactive configuration')
            print('4. Quit')
            action = (input('>>> '))
            
            try:
                action = int(action)
                if action <= 0 or action > 4:
                    print('Invalid input.')
                    continue
            except:
                print('Invalid input.')
                continue

            if action == 1:
                print(self.mail)
            elif action == 2:
                self.send()
            elif action == 3:
                self.__iconfig()
            elif action == 4:
                print('='*30)
                self.__log('Thank you for using CLI for Mailer by Ruby. Bye!')
                print('='*30)
                break

    def send(self) -> None:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.config.sender_email, self.config.sender_password)
            for receiver in self.receivers:
                receiver = receiver.strip()
                if '@' in receiver:
                    self.__log(f'Sending to {receiver}...')
                    mail = EmailMessage()
                    mail['From'] = self.config.sender_email
                    mail['To'] = receiver
                    mail['Subject'] = self.mail.subject
                    mail.add_alternative(self.mail.html, subtype='html')
                    server.sendmail(self.config.sender_email, receiver, mail.as_string())
                    self.__log(f'Sent to {receiver}.')
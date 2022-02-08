
class Mail:

    def __init__(self) -> None:
        self.subject = ''
        self.greeting = ''
        self.body = ''
        self.closing = ''
        self.sender = ''
        self.html = ''

    def __repr__(self) -> str:
        return (
            "="*30 +            
            f"""
This is the current mail in plain text.

Subject:
{self.subject}.

Content:
{self.greeting}
{self.body}
{self.closing}
{self.sender}
""".replace('\n<br>\n', '\n')
        )

        
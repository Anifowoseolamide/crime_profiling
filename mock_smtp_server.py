"""
Mock SMTP Server for Testing Email Verification
Captures emails instead of sending them
"""

import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPServer
from email import message_from_bytes
import re
from datetime import datetime

class MockSMTPHandler:
    """Handler for mock SMTP server"""
    
    def __init__(self):
        self.emails = []
    
    async def handle_DATA(self, server, session, envelope):
        """Handle incoming email"""
        print(f"\n{'='*60}")
        print(f"  📧 Email Captured - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        print(f"From: {envelope.mail_from}")
        print(f"To: {', '.join(envelope.rcpt_tos)}")
        
        # Parse email content
        msg = message_from_bytes(envelope.content)
        subject = msg.get('Subject', 'No Subject')
        print(f"Subject: {subject}")
        
        # Extract body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
                elif part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()
        
        # Extract verification link
        verification_link = None
        token = None
        
        # Try to find verification link
        link_match = re.search(r'http[s]?://[^\s<>"]+/verify\?token=([a-zA-Z0-9-]+)', body)
        if link_match:
            verification_link = link_match.group(0)
            token = link_match.group(1)
            print(f"\n🔗 Verification Link Found:")
            print(f"   {verification_link}")
            print(f"\n🎫 Token: {token}")
        
        # Store email
        email_data = {
            'timestamp': datetime.now(),
            'from': envelope.mail_from,
            'to': envelope.rcpt_tos,
            'subject': subject,
            'body': body[:500],  # First 500 chars
            'verification_link': verification_link,
            'token': token
        }
        self.emails.append(email_data)
        
        print(f"\n📝 Total Emails Captured: {len(self.emails)}")
        print(f"{'='*60}\n")
        
        return '250 Message accepted for delivery'

def run_mock_smtp():
    """Run the mock SMTP server"""
    handler = MockSMTPHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    
    print("=" * 60)
    print("  Mock SMTP Server for Email Testing")
    print("  Running on localhost:1025")
    print("=" * 60)
    print("\nConfiguration for Django settings:")
    print("  EMAIL_HOST = 'localhost'")
    print("  EMAIL_PORT = 1025")
    print("  EMAIL_USE_TLS = False")
    print("  EMAIL_HOST_USER = ''")
    print("  EMAIL_HOST_PASSWORD = ''")
    print("\nWaiting for emails...")
    print("=" * 60)
    print()
    
    controller.start()
    
    try:
        # Keep server running
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down mock SMTP server...")
        controller.stop()

if __name__ == '__main__':
    run_mock_smtp()

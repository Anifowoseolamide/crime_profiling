"""
LASU API Verification and Email Services
Handles student verification via LASU API and email verification workflow
"""

import requests
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import RegistrationToken

logger = logging.getLogger(__name__)


class LASUVerificationService:
    """
    Service for verifying students via LASU API
    """
    
    def __init__(self):
        self.api_url = getattr(settings, 'LASU_API_URL', None)
        self.api_key = getattr(settings, 'LASU_API_KEY', None)
        self.timeout = getattr(settings, 'LASU_API_TIMEOUT', 10)
    
    def verify_student(self, matric_number):
        """
        Verify student via LASU API
        
        Args:
            matric_number (str): Student's matric number
            
        Returns:
            dict: {
                'success': bool,
                'exists': bool,
                'status': str,
                'data': dict or None,
                'error': str or None
            }
        """
        if not self.api_url or not self.api_key:
            logger.warning("LASU API not configured, falling back to manual verification")
            return {
                'success': False,
                'exists': None,
                'status': 'API_NOT_CONFIGURED',
                'data': None,
                'error': 'LASU API not configured'
            }
        
        try:
            # Make API request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {'matric': matric_number}
            
            response = requests.get(
                f"{self.api_url}/verify-student",
                headers=headers,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Expected response format:
                # {
                #     "exists": true,
                #     "status": "ACTIVE",
                #     "full_name": "John Doe",
                #     "email": "john.doe@student.lasu.edu.ng",
                #     "department": "Computer Science"
                # }
                
                return {
                    'success': True,
                    'exists': data.get('exists', False),
                    'status': data.get('status', 'UNKNOWN'),
                    'data': data if data.get('exists') else None,
                    'error': None
                }
            
            elif response.status_code == 404:
                return {
                    'success': True,
                    'exists': False,
                    'status': 'NOT_FOUND',
                    'data': None,
                    'error': 'Student not found in LASU database'
                }
            
            else:
                logger.error(f"LASU API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'exists': None,
                    'status': 'API_ERROR',
                    'data': None,
                    'error': f'API returned status code {response.status_code}'
                }
        
        except requests.Timeout:
            logger.error(f"LASU API timeout for matric {matric_number}")
            return {
                'success': False,
                'exists': None,
                'status': 'TIMEOUT',
                'data': None,
                'error': 'API request timed out'
            }
        
        except requests.RequestException as e:
            logger.error(f"LASU API request error: {str(e)}")
            return {
                'success': False,
                'exists': None,
                'status': 'REQUEST_ERROR',
                'data': None,
                'error': str(e)
            }
        
        except Exception as e:
            logger.error(f"Unexpected error in LASU verification: {str(e)}")
            return {
                'success': False,
                'exists': None,
                'status': 'UNKNOWN_ERROR',
                'data': None,
                'error': str(e)
            }


class EmailVerificationService:
    """
    Service for handling email verification during student registration
    """
    
    @staticmethod
    def generate_verification_token(matric_number, email, lasu_data=None, ip_address=None, user_agent=None):
        """
        Generate a verification token for student registration
        
        Args:
            matric_number (str): Student's matric number
            email (str): Student's email address
            lasu_data (dict, optional): Data from LASU API verification
            ip_address (str, optional): IP address of requester
            user_agent (str, optional): User agent string
            
        Returns:
            RegistrationToken: Created token instance
        """
        expiry_minutes = getattr(settings, 'REGISTRATION_TOKEN_EXPIRY_MINUTES', 15)
        
        # Invalidate any existing active tokens for this matric number
        RegistrationToken.objects.filter(
            matric_number=matric_number,
            is_used=False
        ).update(is_used=True)
        
        # Create new token
        token = RegistrationToken.create_token(
            matric_number=matric_number,
            email=email,
            lasu_data=lasu_data,
            ip_address=ip_address,
            user_agent=user_agent,
            expiry_minutes=expiry_minutes
        )
        
        return token
    
    @staticmethod
    def send_verification_email(email, token, full_name=None):
        """
        Send verification email to student
        
        Args:
            email (str): Student's email address
            token (str): Verification token
            full_name (str, optional): Student's full name
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Get frontend URL from settings
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            verification_link = f"{frontend_url}/verify?token={token}"
            
            # Email context
            context = {
                'full_name': full_name or 'Student',
                'verification_link': verification_link,
                'expiry_minutes': getattr(settings, 'REGISTRATION_TOKEN_EXPIRY_MINUTES', 15)
            }
            
            # Render email templates
            subject = 'Verify Your LASU CampusGuard Account'
            html_message = render_to_string('emails/verification_email.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"Verification email sent to {email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {str(e)}")
            return False
    
    @staticmethod
    def verify_token(token_string):
        """
        Verify a registration token
        
        Args:
            token_string (str): Token to verify
            
        Returns:
            dict: {
                'valid': bool,
                'token': RegistrationToken or None,
                'error': str or None
            }
        """
        try:
            token = RegistrationToken.objects.get(token=token_string)
            
            if token.is_used:
                return {
                    'valid': False,
                    'token': None,
                    'error': 'Token has already been used'
                }
            
            if token.is_expired:
                return {
                    'valid': False,
                    'token': None,
                    'error': 'Token has expired'
                }
            
            return {
                'valid': True,
                'token': token,
                'error': None
            }
        
        except RegistrationToken.DoesNotExist:
            return {
                'valid': False,
                'token': None,
                'error': 'Invalid token'
            }
    
    @staticmethod
    def cleanup_expired_tokens():
        """
        Cleanup expired tokens (should be run as periodic task)
        
        Returns:
            int: Number of tokens deleted
        """
        cutoff_date = timezone.now() - timedelta(days=7)  # Delete tokens older than 7 days
        deleted_count, _ = RegistrationToken.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        
        logger.info(f"Cleaned up {deleted_count} expired registration tokens")
        return deleted_count

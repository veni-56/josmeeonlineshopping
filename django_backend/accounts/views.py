from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddressForm, PhoneVerificationForm, OTPVerificationForm, SellerDocumentForm
from .models import CustomUser, Address, OTPVerification, SellerDocument
import requests
import os


def send_otp_sms(phone, otp):
    """Send OTP via SMS using a reliable service"""
    try:
        # Option 1: Using Twilio (recommended for production)
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        
        if twilio_account_sid and twilio_auth_token and twilio_phone:
            from twilio.rest import Client
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(
                body=f'Your OTP is: {otp}. Valid for 10 minutes. Do not share this code.',
                from_=twilio_phone,
                to=phone
            )
            print(f"[v0] SMS sent successfully via Twilio. SID: {message.sid}")
            return True
        
        # Option 2: Using AWS SNS
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if aws_access_key and aws_secret_key:
            import boto3
            sns_client = boto3.client(
                'sns',
                region_name=os.getenv('AWS_REGION', 'us-east-1'),
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            response = sns_client.publish(
                PhoneNumber=phone,
                Message=f'Your OTP is: {otp}. Valid for 10 minutes. Do not share this code.'
            )
            print(f"[v0] SMS sent successfully via AWS SNS. MessageId: {response['MessageId']}")
            return True
        
        # Option 3: Using Fast2SMS (Indian SMS service - free tier available)
        fast2sms_key = os.getenv('FAST2SMS_API_KEY')
        if fast2sms_key:
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "route": "q",
                "message": f"Your OTP is: {otp}. Valid for 10 minutes. Do not share this code.",
                "language": "english",
                "flash": 0,
                "numbers": phone
            }
            headers = {
                "authorization": fast2sms_key
            }
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"[v0] SMS sent successfully via Fast2SMS")
                return True
            else:
                print(f"[v0] Fast2SMS error: {response.text}")
                return False
        
        # Option 4: Using MSG91 (Indian SMS service)
        msg91_key = os.getenv('MSG91_AUTH_KEY')
        if msg91_key:
            url = "https://api.msg91.com/apiv5/flow/"
            payload = {
                "route": "4",
                "sender": "KARUP",
                "mobiles": phone,
                "message": f"Your OTP is: {otp}. Valid for 10 minutes. Do not share this code.",
                "authkey": msg91_key
            }
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                print(f"[v0] SMS sent successfully via MSG91")
                return True
            else:
                print(f"[v0] MSG91 error: {response.text}")
                return False
        
        # Fallback: Log to console for development
        print(f"[v0] WARNING: No SMS service configured. OTP for {phone}: {otp}")
        print(f"[v0] Configure one of: TWILIO_ACCOUNT_SID, AWS_ACCESS_KEY_ID, FAST2SMS_API_KEY, or MSG91_AUTH_KEY")
        return False
        
    except Exception as e:
        print(f"[v0] Error sending SMS: {str(e)}")
        return False


def phone_verification_view(request):
    """Phone verification view - first step before login/register"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            # Create OTP
            otp = OTPVerification.create_otp(phone)
            
            sms_sent = send_otp_sms(phone, otp.otp)
            
            if sms_sent:
                # Store phone in session for next step
                request.session['phone_for_verification'] = phone
                request.session['otp_id'] = otp.id
                
                messages.success(request, f'OTP sent to {phone}. Please check your SMS.')
                return redirect('accounts:verify_otp')
            else:
                messages.warning(request, f'OTP created but SMS delivery failed. OTP: {otp.otp} (for testing only)')
                request.session['phone_for_verification'] = phone
                request.session['otp_id'] = otp.id
                return redirect('accounts:verify_otp')
    else:
        form = PhoneVerificationForm()
    
    return render(request, 'accounts/phone_verification.html', {'form': form})


def verify_otp_view(request):
    """OTP verification view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    phone = request.session.get('phone_for_verification')
    otp_id = request.session.get('otp_id')
    
    if not phone or not otp_id:
        messages.error(request, 'Please start the verification process again.')
        return redirect('accounts:phone_verification')
    
    try:
        otp_obj = OTPVerification.objects.get(id=otp_id)
    except OTPVerification.DoesNotExist:
        messages.error(request, 'OTP expired. Please try again.')
        return redirect('accounts:phone_verification')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            
            if otp_obj.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('accounts:phone_verification')
            
            if otp_obj.attempts >= 5:
                messages.error(request, 'Too many attempts. Please request a new OTP.')
                return redirect('accounts:phone_verification')
            
            if otp_obj.otp == entered_otp:
                otp_obj.is_verified = True
                otp_obj.save()
                
                # Store verified phone in session
                request.session['verified_phone'] = phone
                del request.session['phone_for_verification']
                del request.session['otp_id']
                
                messages.success(request, 'Phone verified successfully!')
                return redirect('accounts:register')
            else:
                otp_obj.attempts += 1
                otp_obj.save()
                messages.error(request, f'Invalid OTP. {5 - otp_obj.attempts} attempts remaining.')
    else:
        form = OTPVerificationForm()
    
    context = {
        'form': form,
        'phone': phone,
        'attempts_remaining': 5 - otp_obj.attempts
    }
    return render(request, 'accounts/verify_otp.html', context)


def resend_otp_view(request):
    """Resend OTP to phone"""
    if request.method == 'POST':
        phone = request.session.get('phone_for_verification')
        if not phone:
            return JsonResponse({'error': 'Phone not found'}, status=400)
        
        # Create new OTP
        otp = OTPVerification.create_otp(phone)
        send_otp_sms(phone, otp.otp)
        
        request.session['otp_id'] = otp.id
        return JsonResponse({'success': True, 'message': 'OTP resent successfully'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    # Check if phone is verified
    verified_phone = request.session.get('verified_phone')
    if not verified_phone:
        return redirect('accounts:phone_verification')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set the verified phone
            user.phone = verified_phone
            user.phone_verified = True
            user.pan_number = form.cleaned_data.get('pan_number') or None
            user.gst_number = form.cleaned_data.get('gst_number') or None
            user.save()
            
            # Clear session
            del request.session['verified_phone']
            
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            
            # Redirect based on role
            if user.is_seller:
                return redirect('accounts:upload_seller_documents')
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'phone': verified_phone})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next parameter or dashboard
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('accounts:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """User dashboard - redirects based on role"""
    if request.user.is_seller:
        return redirect('dashboard:seller_dashboard')
    elif request.user.is_admin_user:
        return redirect('dashboard:admin_dashboard')
    else:
        return redirect('dashboard:buyer_dashboard')


@login_required
def profile_view(request):
    """User profile view and edit"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            # Update user fields
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.save()
            
            # Update profile
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def address_list_view(request):
    """List all user addresses"""
    addresses = request.user.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_create_view(request):
    """Create a new address"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('accounts:address_list')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Add'})


@login_required
def address_edit_view(request, pk):
    """Edit an existing address"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('accounts:address_list')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Edit'})


@login_required
def address_delete_view(request, pk):
    """Delete an address"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully.')
        return redirect('accounts:address_list')
    
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})


def auth_landing_view(request):
    """Landing page for authentication - directs to login or signup"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    return render(request, 'accounts/auth_landing.html')


@login_required
def upload_seller_documents_view(request):
    """View for sellers to upload documents"""
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can upload documents.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = SellerDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully. It will be verified by our team.')
            return redirect('accounts:seller_documents')
    else:
        form = SellerDocumentForm()
    
    return render(request, 'accounts/upload_document.html', {'form': form})


@login_required
def seller_documents_view(request):
    """View to list seller documents"""
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can view documents.')
        return redirect('accounts:dashboard')
    
    documents = request.user.seller_documents.all()
    return render(request, 'accounts/seller_documents.html', {'documents': documents})

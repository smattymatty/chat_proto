from django.contrib.auth import get_user_model, logout
from django.urls import resolve
import uuid

User = get_user_model()

class GuestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure `request.user` exists (depends on AuthenticationMiddleware)
        if not hasattr(request, "user"):
            return self.get_response(request)

        # Force evaluation of `request.user`
        user = request.user  # Accessing user to resolve `SimpleLazyObject`
        _ = user.is_authenticated  # Trigger actual evaluation of the lazy object

        # Define auth-related URL names that should trigger guest logout
        auth_urls = ['account_login', 'account_signup', 'account_reset_password']

        # Check if the current URL is an auth URL
        current_url = resolve(request.path_info).url_name
        is_auth_url = current_url in auth_urls
        print(f"GuestMiddleware: is_auth_url = {is_auth_url}")
        if is_auth_url:
            return self.get_response(request)



        # Handle guest user logic
        if not request.user.is_authenticated:
            self._handle_guest_user(request)

        return self.get_response(request)



    def _logout_guest(self, request):
        """Logs out guest users and clears session data."""
        logout(request)
        request.session.pop('guest_id', None)
        request.session.pop('guest_user_id', None)

    def _handle_guest_user(self, request):
        """Ensures guest user exists and is attached to the request."""
        guest_id = request.session.get('guest_id')
        if not guest_id:
            # Create new guest user
            guest_user = self._create_guest_user()
            guest_id = guest_user.profile.guest_id  # Assuming `guest_id` is stored in Profile
            request.session['guest_id'] = guest_id
            request.session['guest_user_id'] = guest_user.id
            print(f"Created new guest user: {guest_user.username}")
        else:
            # Try retrieving existing guest user
            guest_user_id = request.session.get('guest_user_id')
            guest_user = self._get_guest_user(guest_user_id)
            if not guest_user:
                # If guest user doesn't exist, restart flow
                self._logout_guest(request)
                print("Guest user not found, restarting flow.")
                self._handle_guest_user(request)
                return
            print(f"Using existing guest user: {guest_user.username}")

        # Attach the guest user to the request
        request.user = guest_user
        print(f"GuestMiddleware: request.user set to {request.user.username}")

    def _create_guest_user(self):
        """Creates and returns a new guest user."""
        guest_id = str(uuid.uuid4())
        username = f'guest_{guest_id[:8]}'
        guest_user = User.objects.create_user(
            username=username,
            password=uuid.uuid4().hex[:12]  # Temporary password
        )
        # Ensure Profile is updated
        guest_user.profile.is_guest = True
        guest_user.profile.guest_id = guest_id
        guest_user.profile.save()
        return guest_user

    def _get_guest_user(self, user_id):
        """Retrieves guest user by ID or returns None if not found."""
        try:
            return User.objects.get(id=user_id, profile__is_guest=True)
        except User.DoesNotExist:
            return None

# from django.contrib.auth import get_user_model
# User = get_user_model()
# user = User.objects.get(username="pydanny")

# # from webhooks.models import Webhook
# from djwebhooks.models import WebhookTarget
# from djwebhooks.decorators import hook


# WebhookTarget.objects.create(
#     owner=user,
#     event="notify.team",
#     target_url="https://mystorefront.com/webhooks/",
#     header_content_type=WebhookTarget.CONTENT_TYPE_JSON,
# )

# @hook(event="notify.team")
# def send_notification_to_team(request):
#     print("---re--------",request)
#     user_ip = get_client_ip(request)
#     return {
#         "user": request,
#         "ip": user_ip,
#     }
    
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
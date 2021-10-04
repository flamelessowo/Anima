# from django.contrib.auth.models import AnonymousUser
# from .forms import ReviewForm
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
#
#
# def check_user_login_before_review(sender, instance, logged, **kwargs):
#     if instance.type(AnonymousUser):
#         raise Exception("Authorize firstly")
#
#
# pre_save.connect(check_user_login_before_review, sender=ReviewForm)

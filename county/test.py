import os
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_county_stats.settings')
    import django
    django.setup()

    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    import os
    from django.core.mail import send_mail
    from coronavirus_county_stats.settings import EMAIL_HOST_USER

    html_message = render_to_string('newEmail.html')
    plain_message = strip_tags(html_message)
    send_mail(" Clear Cov-19 Report", plain_message, EMAIL_HOST_USER,
          ['vvictor.llin@gmail.com'], html_message=html_message)

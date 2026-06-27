from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Article

@shared_task
def send_new_article_notification(article_id):
    """
    Отправляет уведомление всем пользователям о новой статье
    """
    try:
        article = Article.objects.get(id=article_id)
        users = User.objects.filter(is_active=True)
        
        for user in users:
            # Пропускаем автора статьи (он и так знает)
            if user == article.author:
                continue
                
            send_mail(
                subject=f'🦕 Новая статья: {article.title}',
                message=f'''
Привет!

Пользователь {article.author.username} опубликовал новую статью:
"{article.title}"

Читать: http://127.0.0.1:8000{article.get_absolute_url()}

---
Jurassic Blog
                ''',
                from_email='noreply@jurassicblog.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
    except Article.DoesNotExist:
        pass
    except Exception as e:
        print(f'Ошибка отправки уведомлений: {e}')
    
from django.dispatch import receiver
from django.db.models.signals import post_delete
from photos.models import Post


@receiver(post_delete, sender=Post)
def delete_attachmented_image(sender, instance, **kwargs):
    if not instance.image:
        return

    instance.image.delete(save=False)
#Post모델의 image필드가 변경이 되면서 자동으로 save되면서 데이터가 사라지지 않음
#save=False를 넣어 변경이 되더라도 save를 하지 않도록 설정
#post_delete.connect(delete_attachmented_image, sender=Post)

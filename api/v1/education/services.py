from django.core.exceptions import ValidationError

def upload_location_image(instance, image):
    """
    Faylga joylashgan address | format: (media)/company/exams/question_or_answer/
    """
    if instance.question:
        return f'{instance.question.creator.company}/exams/questions/{image}'
    return f'{instance.answer.creator.company}/exams/answers/{image}'


def validate_size_image(file_in_obj):
    """
    Rasm hajmini tekshirish
    """

    size_limit = 10
    if file_in_obj.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum file size: {size_limit}mb')
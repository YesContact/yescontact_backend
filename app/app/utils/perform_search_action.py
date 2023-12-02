from .notifications import send_notification  


def perform_search_action(user1, user2):
    from core.models import SearchRecord
    SearchRecord.objects.create(searcher=user1, searched_user=user2)
    message = f"{user1.username} viewed your contacts"
    send_notification(user2, message)
import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Action


# The create_action() function allows you to create actions that optionally include a target object.
# You can use this function anywhere in your code as a shortcut to add new actions to the activity stream.
# user: The Django User object who performed the action
# verb: A string describing what the user did (e.g., "liked", "commented on")
# target: Optional object that received the action (e.g., a photo that was liked)
def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute
        # created__gte=last_minute:
        # This part of the query is using Django’s ORM lookup syntax. The __gte stands for "greater than or equal to."
        # It means that the query will return all Action records whose created timestamp is later than or equal to last_minute.
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False

# Explanation of the above code:
# The previous click is recorded and remains in the database.
# Every time the function is called, it checks if there's any Action record in the last minute that matches the user,
# verb, and target.
#
# The one-minute check (created__gte=last_minute) works by comparing timestamps:
# It ensures that if a similar action was recorded in the last 60 seconds, no new action is added to avoid duplicates.
#
# New Records After One Minute:
# After the one-minute window, even if the action details (user, verb, target) are the same, the new record is treated
# as a separate event because its timestamp is outside the window of the previous record.
#
# This mechanism helps to prevent accidental multiple clicks (like double-clicks) from creating duplicate actions,
# while still allowing a new action to be recorded if enough time has passed.


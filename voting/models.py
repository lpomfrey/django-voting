# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from voting.managers import VoteManager


@python_2_unicode_compatible
class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    UPVOTE = +1
    DOWNVOTE = -1
    SCORES = (
        (UPVOTE, '+1'),
        (DOWNVOTE, '-1'),
    )

    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=SCORES)
    time_stamp = models.DateTimeField(editable=False, default=now)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        return '{}: {} on {}'.format(self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote == self.UPVOTE

    def is_downvote(self):
        return self.vote == self.DOWNVOTE

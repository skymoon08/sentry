from __future__ import absolute_import

from sentry.api.bases.avatar import AvatarMixin
from sentry.api.bases.team import TeamEndpoint
from sentry.models import TeamAvatar


class TeamAvatarEndpoint(AvatarMixin, TeamEndpoint):
    object_type = 'team'
    model = TeamAvatar

    def get(self, request, team):
        return super(TeamAvatarEndpoint, self).get(request, team)

    def put(self, request, team):
        return super(TeamAvatarEndpoint, self).put(request, team)

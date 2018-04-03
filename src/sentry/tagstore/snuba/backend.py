"""
sentry.tagstore.snuba.backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2018 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from datetime import datetime, timedelta
import pytz
import six

from sentry.tagstore import TagKeyStatus
from sentry.tagstore.base import TagStorage
from sentry.utils import snuba


class SnubaTagStorage(TagStorage):

    # Tag keys and values
    def get_tag_key(self, project_id, environment_id, key, status=TagKeyStatus.VISIBLE):
        pass

    def get_tag_keys(self, project_id, environment_id, status=TagKeyStatus.VISIBLE):
        pass

    def get_tag_value(self, project_id, environment_id, key, value):
        pass

    def get_tag_values(self, project_id, environment_id, key):
        pass

    def get_group_tag_key(self, project_id, group_id, environment_id, key):
        pass

    def get_group_tag_keys(self, project_id, group_id, environment_id, limit=None):
        pass

    def get_group_tag_value(self, project_id, group_id, environment_id, key, value):
        pass

    def get_group_tag_values(self, project_id, group_id, environment_id, key):
        pass

    def get_group_list_tag_value(self, project_id, group_id_list, environment_id, key, value):
        pass

    def get_group_tag_value_count(self, project_id, group_id, environment_id, key):
        pass

    def get_group_tag_values_for_users(self, event_users, limit=100):
        pass

    def get_top_group_tag_values(self, project_id, group_id, environment_id, key, limit=3):
        pass

    def get_group_tag_keys_and_top_values(self, project_id, group_id, environment_id, user=None):
        from sentry import tagstore
        end = datetime.utcnow().replace(tzinfo=pytz.UTC)
        start = end - timedelta(days=90)
        filters = {
            'project_id': [project_id],
            'environment': [environment_id],
            'issue': [group_id],
        }
        results = snuba.query(start, end, ['tags.key'], None, filters,
                              'topK(10)', 'tags.value', arrayjoin='tags')

        return [{
            'id': key,
            'name': tagstore.get_tag_key_label(key),
            'key': tagstore.get_standardized_key(key),
            'uniqueValues': 0,  # TODO do we need another query for this?
            'totalValues': 0,  # TODO do we need another query for this?
            'topValues': [{
                'id': val,
                'name': tagstore.get_tag_value_label(key, val),
                'key': tagstore.get_standardized_key(val),
                'value': val,
                # TODO we don't know any of these without more queries
                'count': 0,
                'lastSeen': 0,
                'firstSeen': 0,
            } for val in values],
        } for key, values in six.iteritems(results)]

    # Releases
    def get_first_release(self, project_id, group_id):
        pass

    def get_last_release(self, project_id, group_id):
        pass

    def get_release_tags(self, project_ids, environment_id, versions):
        pass

    def get_group_event_ids(self, project_id, group_id, environment_id, tags):
        pass

    def get_group_ids_for_users(self, project_ids, event_users, limit=100):
        pass

    def get_groups_user_counts(self, project_id, group_ids, environment_id):
        pass

    # Search
    def get_group_ids_for_search_filter(self, project_id, environment_id, tags):
        from sentry.search.base import ANY, EMPTY

        # Any EMPTY value means there can be no results for this query so
        # return an empty list immediately.
        if any(val == EMPTY for _, val in six.iteritems(tags)):
            return []

        filters = {
            'environment': [environment_id],
            'project_id': [project_id],
        }

        conditions = []
        for tag, val in six.iteritems(tags):
            col = 'tags[{}]'.format(tag)
            if val == ANY:
                conditions.append((col, 'IS NOT NULL', None))
            else:
                conditions.append((col, '=', val))

        end = datetime.utcnow().replace(tzinfo=pytz.UTC)
        start = end - timedelta(days=90)
        issues = snuba.query(start, end, ['issue'], conditions, filters)

        # convert
        #    {issue1: count, ...}
        # into
        #    [issue1, ...]
        return issues.keys()

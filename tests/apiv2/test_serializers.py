import datetime
import random

from django.test import TransactionTestCase

from tests.randgen import (
    generate_donation,
    generate_donations,
    generate_donor,
    generate_event,
)
from tracker.api.serializers import DonationSerializer, EventSerializer
from tracker.models import Event


class TestDonationSerializer(TransactionTestCase):
    rand = random.Random()

    def setUp(self):
        super(TestDonationSerializer, self).setUp()
        self.event = generate_event(self.rand)
        self.event.save()
        self.donor = generate_donor(self.rand)
        self.donor.save()
        self.donation = generate_donation(self.rand, event=self.event, donor=self.donor)
        self.donation.save()

    def test_includes_all_public_fields(self):
        expected_fields = [
            'type',
            'id',
            'donor',
            'donor_name',
            'event',
            'domain',
            'transactionstate',
            'readstate',
            'commentstate',
            'amount',
            'currency',
            'timereceived',
            'comment',
            'commentlanguage',
            'pinned',
            'bids',
        ]

        serialized_donation = DonationSerializer(self.donation).data
        for field in expected_fields:
            self.assertIn(field, serialized_donation)

    def test_does_not_include_modcomment_without_permission(self):
        serialized_donation = DonationSerializer(self.donation).data
        self.assertNotIn('modcomment', serialized_donation)

    def test_includes_modcomment_with_permission(self):
        serialized_donation = DonationSerializer(
            self.donation, with_permissions=('tracker.change_donation',)
        ).data
        self.assertIn('modcomment', serialized_donation)


class TestEventSerializer(TransactionTestCase):
    rand = random.Random()

    def setUp(self):
        super(TestEventSerializer, self).setUp()
        self.event = generate_event(self.rand)
        self.event.save()
        self.donor = generate_donor(self.rand)
        self.donor.save()
        generate_donations(
            self.rand,
            self.event,
            5,
            start_time=self.event.datetime,
            end_time=self.event.datetime + datetime.timedelta(hours=1),
        )

    def test_includes_all_public_fields(self):
        expected_fields = [
            'type',
            'id',
            'short',
            'name',
            'hashtag',
            'datetime',
            'timezone',
            'use_one_step_screening',
        ]

        serialized_event = EventSerializer(self.event).data
        for field in expected_fields:
            self.assertIn(field, serialized_event)

    def test_does_not_include_totals_fields(self):
        serialized_event = EventSerializer(self.event).data
        self.assertNotIn('amount', serialized_event)
        self.assertNotIn('donation_count', serialized_event)

    def test_includes_totals_fields_with_opt_in(self):
        event = Event.objects.with_annotations().get(pk=self.event.pk)
        serialized_event = EventSerializer(event, with_totals=True).data
        self.assertIn('amount', serialized_event)
        self.assertIn('donation_count', serialized_event)

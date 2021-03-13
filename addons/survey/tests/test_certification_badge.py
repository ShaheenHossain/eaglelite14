# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.survey.tests import common
from psycopg2 import IntegrityError
from odoo.exceptions import AccessError
from odoo.tools import mute_logger


class TestCertificationBadge(common.TestSurveyCommon):

    def setUp(self):
        super(TestCertificationBadge, self).setUp()
        self.certification_survey = self.env['survey.survey'].with_user(self.survey_manager).create({
            'title': 'Certification Survey',
            'access_mode': 'public',
            'users_login_required': True,
            'scoring_type': 'scoring_with_answers',
            'certification': True,
            'state': 'open',
        })

        self.certification_survey_2 = self.env['survey.survey'].with_user(self.survey_manager).create({
            'title': 'Another Certification Survey',
            'access_mode': 'public',
            'users_login_required': True,
            'scoring_type': 'scoring_with_answers',
            'certification': True,
            'state': 'open',
        })

    def test_archive(self):
        """ Archive status of survey is propagated to its badges. """
        self.certification_survey.write({
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge.id
        })

        self.certification_survey.action_archive()
        self.assertFalse(self.certification_survey.active)
        self.assertFalse(self.certification_badge.active)

        self.certification_survey.action_unarchive()
        self.assertTrue(self.certification_survey.active)
        self.assertTrue(self.certification_badge.active)

    def test_give_badge_without_badge(self):
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.certification_survey.write({'certification_give_badge': True})
                self.certification_survey.flush(['certification_give_badge'])

    def test_remove_badge_with_give_badge(self):
        self.certification_survey.write({
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge.id
        })
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.certification_survey.write({'certification_badge_id': None})
                self.certification_survey.flush(['certification_badge_id'])

    def test_remove_badge_with_give_badge_multi(self):
        self.certification_survey.write({
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge.id
        })
        self.certification_survey_2.write({
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge_2.id
        })
        surveys = self.env['survey.survey'].browse([
            self.certification_survey.id,
            self.certification_survey_2.id
        ])
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                surveys.write({'certification_badge_id': None})
                surveys.flush(['certification_badge_id'])

    def test_set_same_badge_on_multiple_survey(self):
        self.certification_survey.write({
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge.id
        })
        # set the same badge on another survey should fail:
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.certification_survey_2.write({
                    'certification_give_badge': True,
                    'certification_badge_id': self.certification_badge.id
                })
                self.certification_survey.flush()

    def test_certification_badge_access(self):
        self.certification_badge.with_user(self.survey_manager).write(
            {'description': "Spoiler alert: I'm Aegon Targaryen and I sleep with the Dragon Queen, who is my aunt by the way! So I can do whatever I want! Even if I know nothing!"})
        self.certification_badge.with_user(self.survey_user).write({'description': "Youpie Yeay!"})
        with self.assertRaises(AccessError):
            self.certification_badge.with_user(self.user_emp).write({'description': "I'm a dude who think that has every right on the Iron Throne"})
        with self.assertRaises(AccessError):
            self.certification_badge.with_user(self.user_portal).write({'description': "Guy, you just can't do that !"})
        with self.assertRaises(AccessError):
            self.certification_badge.with_user(self.user_public).write({'description': "What did you expect ? Schwepps !"})

    def test_badge_configuration_multi(self):
        vals = {
            'title': 'Certification Survey',
            'access_mode': 'public',
            'users_login_required': True,
            'scoring_type': 'scoring_with_answers',
            'certification': True,
            'certification_give_badge': True,
            'certification_badge_id': self.certification_badge.id,
            'state': 'open'
        }
        survey_1 = self.env['survey.survey'].create(vals.copy())
        vals.update({'certification_badge_id': self.certification_badge_2.id})
        survey_2 = self.env['survey.survey'].create(vals.copy())
        vals.update({'certification_badge_id': self.certification_badge_3.id})
        survey_3 = self.env['survey.survey'].create(vals)

        certification_surveys = self.env['survey.survey'].browse([survey_1.id, survey_2.id, survey_3.id])
        self.assertEqual(len(certification_surveys), 3, 'There should be 3 certification survey created')

        # Test write multi
        certification_surveys.write({'certification_give_badge': False})
        for survey in certification_surveys:
            self.assertEqual(survey.certification_badge_id.active, False,
                             'Every badge should be inactive if the 3 survey does not give badge anymore')

        certification_surveys.write({'certification_give_badge': True})
        for survey in certification_surveys:
            self.assertEqual(survey.certification_badge_id.active, True,
                             'Every badge should be reactivated if the 3 survey give badges again')


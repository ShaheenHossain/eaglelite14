# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Surveys',
    'version': '3.2',
    'category': 'Marketing/Surveys',
    'description': """
Create beautiful surveys and visualize answers
==============================================
    """,
    'summary': 'Create surveys and analyze answers',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'auth_signup',
        'http_routing',
        'mail',
        'web_tour'],
    'data': [
        'views/survey_report_templates.xml',
        'views/survey_reports.xml',
        'data/mail_template_data.xml',
        'data/ir_actions_data.xml',
        'security/survey_security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/survey_menus.xml',
        'views/survey_survey_views.xml',
        'views/survey_user_views.xml',
        'views/survey_question_views.xml',
        'views/survey_templates.xml',
        'views/survey_templates_management.xml',
        'views/survey_templates_print.xml',
        'views/survey_templates_statistics.xml',
        'views/survey_templates_user_input_session.xml',
        'wizard/survey_invite_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [
        'data/survey_demo_user.xml',
        'data/survey_demo_feedback.xml',
        'data/survey_demo_certification.xml',
        'data/survey_demo_quiz.xml',
        'data/survey_demo_quiz_userinput.xml',
        'data/survey_demo_conditional.xml',
        'data/survey.user_input.line.csv'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 220,
}

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task, task
from celery.schedules import crontab
from datetime import date, datetime, timedelta
import stripe

from apps.bids.models import Bid
from apps.commons.constants import *
from apps.items.models import Item


@task()
def change_item_status():
    hour_from_now = datetime.now() + timedelta(hours=1)
    hour_min_from_now = hour_from_now + timedelta(minutes=1)
    items = Item.objects.filter(item_status=ITEM_CONSTANTS['PENDING'], date_time__gte=hour_from_now, date_time__lt=hour_min_from_now)
    items.update(item_status=ITEM_CONSTANTS['ACTIVE'])
    
    min_from_now = datetime.now() + timedelta(minutes=1)
    items = Item.objects.filter(item_status=ITEM_CONSTANTS['ACTIVE'], date_time__gte=datetime.now(), date_time__lt=min_from_now)
    items.update(item_status=ITEM_CONSTANTS['ONHOLD'])



@shared_task
def send_mail_to_requester(item_name, item_requester, request_status):

    ctx = {
            'name': item_requester['name'],
            'item': item_name,
        }
    email_html_temp=''
    email_txt_temp=''
        
    if request_status:
        email_html_temp='requester_congrats.html'
        email_txt_temp='requester_congrats.txt'
    else:
        email_html_temp='requester_sorry.html'
        email_txt_temp='requester_sorry.txt'
    
    send_mail(
            'Item Request Status',
            render_to_string(email_txt_temp, ctx),
            settings.DDM_MANAGER,
            [item_requester['email']],
            fail_silently=True,
            html_message=render_to_string(email_html_temp, ctx),
            )        

@shared_task
def send_mail_to_seller(item_name, seller):
    ctx = {
            'name': seller['name'],
            'item': item_name,
        }
    
    send_mail(
            'Bid Status',
            render_to_string('seller_congrats.txt', ctx),
            settings.DDM_MANAGER,
            [seller['email']],
            fail_silently=True,
            html_message=render_to_string('seller_congrats.html', ctx),
            )           

@shared_task
def refund_bidder(item_id, item_name):
    unsold_bids = Bid.objects.filter(item__id= item_id, validity__in= [BIDS_CONSTANTS['VALID'], BIDS_CONSTANTS['INVALID']])
    
    for unsold_bid in unsold_bids:
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        refund = stripe.Refund.create(
                charge= unsold_bid.charge_info['id'],
                amount= GLOBAL_CONSTANTS['ONE_DOLLAR'],
                )
        seller= unsold_bid.seller
        ctx = {
            'name': seller.get_short_name(),
            'item': item_name,
        }
        send_mail(
            'Bid Refund Email',
            render_to_string('bid_refund.txt', ctx),
            settings.DDM_MANAGER,
            [seller.email],
            fail_silently=True,
            html_message=render_to_string('bid_refund.html', ctx),
        )

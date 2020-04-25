import os
import argparse
import datetime
from pprint import pprint

import requests
import chart_studio.tools as chart_studio_tools
import chart_studio.plotly as py
import plotly.graph_objects as go
from dotenv import load_dotenv


def convert_to_utc_timestamp(date_to_convert):
    utc_timestamp = datetime.datetime(
        year=date_to_convert.year,
        month=date_to_convert.month,
        day=date_to_convert.day,
        tzinfo=datetime.timezone.utc
    ).timestamp()

    return utc_timestamp


def get_one_day_utc_timestamps(end_of_day, convert_to_utc_timestamp):
    start_of_day = end_of_day - datetime.timedelta(days=1)

    start_of_day_timestamp = convert_to_utc_timestamp(start_of_day)
    end_of_day_timestamp = convert_to_utc_timestamp(end_of_day)

    one_day_utc_timestamps = {
        'day': start_of_day,
        'start': start_of_day_timestamp,
        'end': end_of_day_timestamp
    }

    return one_day_utc_timestamps


def get_utc_timestamps_for_days_period(days_period, convert_to_utc_timestamp):
    timestamps_for_days_period = []

    for days_delta in range(days_period):
        today = datetime.date.today()
        end_of_day = today - datetime.timedelta(days=days_delta)

        one_day_utc_timestamps = get_one_day_utc_timestamps(
            end_of_day,
            convert_to_utc_timestamp
        )

        timestamps_for_days_period.append(one_day_utc_timestamps)

    return timestamps_for_days_period


def check_errors_in_vk_response(vk_response):
    if 'error' in vk_response:
        raise requests.exceptions.HTTPError(vk_response['error'])


def get_keyword_mentions(token, keyword, max_count, start_time='', end_time=''):
    url = 'https://api.vk.com/method/newsfeed.search?PARAMETERS&access_token=ACCESS_TOKEN&v=V'
    payload = {
        'q': keyword,
        'count': max_count,
        'start_time': start_time,
        'end_time': end_time,
        'access_token': token,
        'v': 5.103
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    keyword_mentions = response.json()
    check_errors_in_vk_response(keyword_mentions)

    return keyword_mentions['response']


def get_mentions_by_days(timestamps_for_days_period,
                         vk_service_key,
                         keyword,
                         max_count):
    mentions_by_days = []

    for timestamps_for_day in timestamps_for_days_period:
        day = timestamps_for_day['day']
        start_day_timestamp = timestamps_for_day['start']
        end_day_timestamp = timestamps_for_day['end']

        mentions = get_keyword_mentions(
            vk_service_key,
            keyword,
            max_count,
            start_time = start_day_timestamp,
            end_time = end_day_timestamp
        )
        mentions_count = mentions['total_count']

        mentions_by_day = {
            'day': day,
            'count': mentions_count
        }

        mentions_by_days.append(mentions_by_day)

    return mentions_by_days


def main():
    load_dotenv()
    vk_service_key = os.getenv('VK_SERVICE_KEY')

    parser = argparse.ArgumentParser(
        description='This script get all mentions by keyword in vk.com \
                     count its and visualize with plotly bar chart.'
    )
    parser.add_argument('keyword', help='Input keyword for search')
    parser.add_argument(
        '-d',
        '--days_period',
        default= 7,
        type=int,
        help='Enter days count to search starting today'
    )
    args = parser.parse_args()

    days_period = args.days_period
    timestamps_for_days_period = get_utc_timestamps_for_days_period(
        days_period,
        convert_to_utc_timestamp
    )

    keyword = args.keyword
    max_count = 10
    mentions_by_days = get_mentions_by_days(
        timestamps_for_days_period,
        vk_service_key,
        keyword,
        max_count
    )

    plotly_api_key = os.getenv('PLOTLY_API_KEY')
    plotly_username = os.getenv('PLOTLY_USERNAME')
    chart_studio_tools.set_credentials_file(
        username=plotly_username,
        api_key=plotly_api_key
    )

    days = [mentions_by_day['day'] for mentions_by_day in mentions_by_days]
    mentions_count = [mentions_by_day['count'] for mentions_by_day in mentions_by_days]

    mentions_by_days_bar_chart = go.Figure([go.Bar(x=days, y=mentions_count)])

    chart_url = py.plot(
        mentions_by_days_bar_chart ,
        filename = '{} in vk mentions chart'.format(keyword),
        auto_open=True
    )
    print(chart_url)


if __name__ == '__main__':
    main()

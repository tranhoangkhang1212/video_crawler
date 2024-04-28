import os
import subprocess
import requests
import json
import requests
from bs4 import BeautifulSoup

def get_page_info(url):
    headers = {
        'cookie': 'id_video=806; PHPSESSID=nboru4qd9vlua4ap5qcgbl4gqp; _gid=GA1.2.209186439.1714205116; wordpress_logged_in_41c2992caeeefa602e9a6456d3cf93fb=Milky.rive%7C1714377931%7CwHODH25P28BUEeO4yX1Cx2iHCuOdP79wwb86c9OHVsz%7C4ed3919c5c574522823f5dbb44dba672ae08a8f5ebc1d5564a98c31464779eed; _ga_ESKS26JHMK=GS1.1.1714244499.4.1.1714246514.0.0.0; _ga_6M6N2MR48K=GS1.1.1714244499.4.1.1714246514.0.0.0; _ga=GA1.2.1223232138.1714205116; _ga_Y04VS404RP=GS1.2.1714244500.4.1.1714246514.0.0.0',
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data_video_list = []
        soup = BeautifulSoup(response.content, 'html.parser')
        list_data = soup.find_all('div', class_=lambda x: x and x.startswith('show_data_'))
        
        title = soup.find('h3').text.strip()
        folder_name = title.replace(' ', '_').lower()
        for data in list_data:
            li_tags = data.find_all('li')

            for li_tag in li_tags:
                data_video_value = li_tag.get('data-video')
                data_video_list.append(data_video_value)

        return {
            'video_ids': data_video_list,
            'folder_name': folder_name
        }
    else:
        print("Failed to retrieve data from URL:", url)


def get_m3u8_link(videoId):
    url = 'https://lopveonline.com/wp-admin/admin-ajax.php'
    headers = {
        'cookie': 'wordpress_sec_41c2992caeeefa602e9a6456d3cf93fb=Milky.rive%7C1714377931%7CwHODH25P28BUEeO4yX1Cx2iHCuOdP79wwb86c9OHVsz%7Cf8d333cc175d89073fd2ef456ef56a39bd890faaba75918f1e42ac3ba7fb4f1c; PHPSESSID=nboru4qd9vlua4ap5qcgbl4gqp; _gid=GA1.2.209186439.1714205116; wordpress_logged_in_41c2992caeeefa602e9a6456d3cf93fb=Milky.rive%7C1714377931%7CwHODH25P28BUEeO4yX1Cx2iHCuOdP79wwb86c9OHVsz%7C4ed3919c5c574522823f5dbb44dba672ae08a8f5ebc1d5564a98c31464779eed; _gat_UA-212783152-1=1; _ga_ESKS26JHMK=GS1.1.1714244499.4.1.1714244652.0.0.0; _ga_6M6N2MR48K=GS1.1.1714244499.4.1.1714244652.0.0.0; _ga=GA1.2.1223232138.1714205116; _ga_Y04VS404RP=GS1.2.1714244500.4.1.1714244652.0.0.0',
    }

    data = {
        'action': 'ajax_video_views',
        'id_video': videoId,
        '_wpnonce': 'bb83bb034e',
        'ip_request': '183.80.39.6',
        'device': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'server': '1',
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = json.loads(response.text)
    video_link = response_data['link']
    parts = video_link.split('/')
    combo_name = parts[-2]

    return {
        'link': video_link,
        'combo_name': combo_name
    }


def download_m3u8(url, output_file, key_uri=None):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ffmpeg_command = ['ffmpeg', '-i', url]

    if key_uri:
        ffmpeg_command.extend(['-hls_key_info_file', key_uri])
    ffmpeg_command.extend(['-c', 'copy', output_file])
    print("FFmpeg Command:", ' '.join(ffmpeg_command))
    subprocess.run(ffmpeg_command)


def download_page_videos(video_id): 
    new_url = 'https://lopveonline.com/account/?type=lop-hoc&id={}'.format(video_id)
    print(new_url)
    page_info = get_page_info(new_url)
    video_ids = page_info['video_ids']
    folder_name = page_info['folder_name']

    os.makedirs('downloaded_videos/' + folder_name, exist_ok=True)
        
    if (video_ids):
        for video_id in video_ids:
            m3u8File = get_m3u8_link(video_id)
            link = m3u8File['link']
            name = m3u8File['combo_name']
            output_file = 'downloaded_videos/{}/{}.mp4'.format(folder_name, name)
            key_uri = "https://video.lopveonline.vn/m3u8/vithanhlam.key"
            download_m3u8(link, output_file, key_uri)

def get_video_ids():
    url = 'https://lopveonline.com/account/?type=khoa-hoc'
    headers = {
        'cookie': 'id_video=2566; PHPSESSID=nboru4qd9vlua4ap5qcgbl4gqp; _gid=GA1.2.209186439.1714205116; wordpress_logged_in_41c2992caeeefa602e9a6456d3cf93fb=Milky.rive%7C1714448736%7C24sbvb2I25vRiRnnWfPahx1B40vvDafiJCXXAisJPke%7C4d947315c8ef9c46309f9044c48d4c4eedf61ac0f299e95d1ecf12558ae8408c; _ga_ESKS26JHMK=GS1.1.1714275602.6.1.1714275959.0.0.0; _ga=GA1.1.1223232138.1714205116; _ga_6M6N2MR48K=GS1.1.1714275602.6.1.1714275959.0.0.0; _ga_Y04VS404RP=GS1.2.1714275603.6.1.1714275959.0.0.0',
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        video_ids = []
        soup = BeautifulSoup(response.content, 'html.parser')
        groups = soup.find_all('div', class_='nhomhoctap')
        for group in groups:
            id = group.get('data-id')
            video_ids.append(id)
        return video_ids        
    
video_ids = get_video_ids()
if (video_ids):
    for video_id in video_ids:
        download_page_videos(video_id)
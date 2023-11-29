import re
from datetime import timezone, timedelta, datetime
import requests
import yaml

ad_url = ['https://raw.githubusercontent.com/Goooler/1024_hosts/master/hosts',
          'https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts']

white_url = ['https://raw.githubusercontent.com/Goooler/1024_hosts/master/whitelist']

# proxies = {
#     "http": "http://localhost:7890",
#     "https": "http://localhost:7890",
# }

ad_master_rule = "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml"
white_master_rule = "https://raw.githubusercontent.com/privacy-protection-tools/dead-horse/master/anti-ad-white-for-clash.yaml"


def downlaod_clash_rule_set(url: str):
    # resp = requests.get(url, proxies=proxies)
    resp = requests.get(url)
    return resp.text


def remove_comments(text: str):
    lines = text.split("\n")
    result = "\n"
    for i in lines:
        if i.startswith("#"):
            continue
        result += i + "\n"
    return result


def get_domain(text: str):
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+'
    cleaned_text = re.sub(ip_pattern, '', text, flags=re.MULTILINE)
    cleaned_text = re.sub(r'^white\s+', '', cleaned_text, flags=re.MULTILINE)
    return cleaned_text.strip()


def write_to_file(text: str, file_name: str):
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)

    with open(file_name, 'w', encoding="utf-8") as f:
        # text文件头添加当前时间
        f.write(f"# 自动生成  {beijing_now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(text)


if __name__ == '__main__':
    t = ""
    for i in ad_url:
        t += get_domain(remove_comments(downlaod_clash_rule_set(i)))
    t = '\n'.join(set(t.splitlines()))
    # print(t)

    t2 = downlaod_clash_rule_set(ad_master_rule)
    data = yaml.safe_load(t2)
    data['payload'].extend(t.splitlines())
    data['payload'].remove('360.cn')
    # print(data['payload'])
    write_to_file(yaml.dump(data), 'Clash_Rule_Set_AntiAD.yaml')

    t = ''
    for i in white_url:
        t += get_domain(remove_comments(downlaod_clash_rule_set(i)))
    t = '\n'.join(set(t.splitlines()))
    t2 = downlaod_clash_rule_set(white_master_rule)
    data = yaml.safe_load(t2)
    data['payload'].extend(t.splitlines())
    write_to_file(yaml.dump(data), 'Clash_Rule_Set_White.yaml')

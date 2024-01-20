from datetime import timezone, datetime, timedelta

import requests
import yaml

ad_url = "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt"
add_url = "https://raw.githubusercontent.com/Latticect/clash-anti-ad-rule-set/main/add.txt"


def get_adblock(url) -> str:
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        adblock = res.text
        return adblock


def str_to_list(adblock: str) -> list:
    adblock = adblock.split("\n")
    adblock = [x for x in adblock if x != ""]
    return adblock


def deal_list(adBlock: list):
    block = []
    white = []
    for i in adBlock:
        if i.startswith("||"):
            block.append(i.replace("||", "+.")[:-1])
        elif i.startswith("@@||"):
            white.append(i.replace("@@||", "+.")[:-1])
    add = str_to_list(get_adblock(add_url))
    for i in add:
        block.append(f"+.{i}")
    return [block, white]


def make_yaml(data: list):
    yaml_str = yaml.dump({"payload": data})
    return yaml_str


def write_yaml(yaml_str: str, file_name: str):
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"# 更新时间：{beijing_now}\n\n{yaml_str}")


def main():
    adblock = get_adblock(ad_url)
    adblock = str_to_list(adblock)
    block, white = deal_list(adblock)
    yaml_str = make_yaml(block)
    write_yaml(yaml_str, "Clash_Rule_Set_AntiAD.yaml")
    yaml_str = make_yaml(white)
    write_yaml(yaml_str, "Clash_Rule_Set_White.yaml")


if __name__ == "__main__":
    main()

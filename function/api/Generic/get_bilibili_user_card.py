import requests


def get_bilibili_user_card(mid, photo=False) -> dict:
    """
    获取Bilibili用户名片信息

    参数:
    mid (int/str): 目标用户mid (必需)
    photo (bool): 是否请求用户主页头图 (可选，默认为False)

    返回:
    dict: 解析后的用户信息字典，包含主要字段
    """
    # API地址
    url = "https://api.bilibili.com/x/web-interface/card"

    # 请求参数
    params = {
        'mid': mid,
        'photo': 'true' if photo else 'false'
    }

    # 添加浏览器头信息 - 解决412错误
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://space.bilibili.com/',
        'Origin': 'https://space.bilibili.com'
    }

    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10  # 添加超时设置
        )
        response.raise_for_status()  # 检查HTTP错误

        # 解析JSON响应
        data = response.json()

        # 检查API返回状态
        if data['code'] != 0:
            return {
                'error': True,
                'code': data['code'],
                'message': data['message'],
                'ttl': data.get('ttl', 1)
            }

        # 提取主要数据
        result = {
            'basic_info': {
                'mid': data['data']['card'].get('mid', ''),
                'name': data['data']['card'].get('name', ''),
                'sex': data['data']['card'].get('sex', '保密'),
                'avatar': data['data']['card'].get('face', ''),
                'sign': data['data']['card'].get('sign', ''),
                'level': data['data']['card']['level_info']['current_level'] if 'level_info' in data['data'][
                    'card'] else 0,
                'status': '正常' if data['data']['card'].get('spacesta', 0) == 0 else '封禁'
            },
            'stats': {
                'following': data['data'].get('following', False),
                'archive_count': data['data'].get('archive_count', 0),
                'follower': data['data'].get('follower', 0),
                'like_num': data['data'].get('like_num', 0),
                'attention': data['data']['card'].get('attention', 0)  # 关注数
            },
            'verification': {
                'role': data['data']['card']['Official'].get('role', -1) if 'Official' in data['data']['card'] else -1,
                'title': data['data']['card']['Official'].get('title', '') if 'Official' in data['data'][
                    'card'] else '',
                'type': data['data']['card']['Official'].get('type', -1) if 'Official' in data['data']['card'] else -1
            },
            'vip_info': {
                'type': data['data']['card']['vip'].get('vipType', 0) if 'vip' in data['data']['card'] else 0,
                'status': data['data']['card']['vip'].get('vipStatus', 0) if 'vip' in data['data']['card'] else 0,
                'label': data['data']['card']['vip']['label'].get('text', '') if 'vip' in data['data'][
                    'card'] and 'label' in data['data']['card']['vip'] else ''
            }
        }

        # 如果请求了头图
        if photo and 'space' in data['data']:
            result['space_image'] = {
                'small': data['data']['space'].get('s_img', ''),
                'large': data['data']['space'].get('l_img', '')
            }

        # 添加勋章信息（如果存在）
        if 'nameplate' in data['data']['card']:
            result['nameplate'] = {
                'id': data['data']['card']['nameplate'].get('nid', 0),
                'name': data['data']['card']['nameplate'].get('name', ''),
                'image': data['data']['card']['nameplate'].get('image', ''),
                'level': data['data']['card']['nameplate'].get('level', '')
            }

        # 添加挂件信息（如果存在）
        if 'pendant' in data['data']['card']:
            result['pendant'] = {
                'id': data['data']['card']['pendant'].get('pid', 0),
                'name': data['data']['card']['pendant'].get('name', ''),
                'image': data['data']['card']['pendant'].get('image', '')
            }

        return result

    except requests.exceptions.RequestException as e:
        return {'error': True, 'message': f'网络请求失败: {str(e)}'}
    except ValueError as e:
        return {'error': True, 'message': f'JSON解析失败: {str(e)}'}
    except KeyError as e:
        return {'error': True, 'message': f'响应数据缺少必要字段: {str(e)}'}


# 使用示例
if __name__ == "__main__":
    # 获取用户mid=2的信息，并请求主页头图
    user_info = get_bilibili_user_card(mid=143474500, photo=True)

    if 'error' in user_info and user_info['error']:
        print(f"获取用户信息失败: {user_info.get('message', '未知错误')}")
    else:
        print("用户基本信息:")
        print(f"UID: {user_info['basic_info']['mid']}")
        print(f"昵称: {user_info['basic_info']['name']}")
        print(f"性别: {user_info['basic_info']['sex']}")
        print(f"等级: LV{user_info['basic_info']['level']}")
        print(f"签名: {user_info['basic_info']['sign']}")
        print(f"状态: {user_info['basic_info']['status']}")

        print("\n用户统计:")
        print(f"粉丝数: {user_info['stats']['follower']}")
        print(f"关注数: {user_info['stats']['attention']}")
        print(f"稿件数: {user_info['stats']['archive_count']}")
        print(f"点赞数: {user_info['stats']['like_num']}")
        print(f"已关注: {'是' if user_info['stats']['following'] else '否'}")

        if 'space_image' in user_info:
            print(f"\n主页头图(大): {user_info['space_image']['large']}")
            print(f"主页头图(小): {user_info['space_image']['small']}")

        if user_info['verification']['role'] != -1:
            print(f"\n认证信息: {user_info['verification']['title']}")

        if user_info['vip_info']['status'] == 1:
            vip_type = "月度大会员" if user_info['vip_info']['type'] == 1 else "年度大会员"
            print(f"\n会员状态: {vip_type} - {user_info['vip_info']['label']}")

        if 'nameplate' in user_info:
            print(f"\n勋章: {user_info['nameplate']['name']} (等级: {user_info['nameplate']['level']})")
            print(f"勋章图片: {user_info['nameplate']['image']}")

        if 'pendant' in user_info:
            print(f"\n挂件: {user_info['pendant']['name']}")
            print(f"挂件图片: {user_info['pendant']['image']}")

# naver_search_config_parser.py
import configparser

# 정수 값 판단 문자일 경우 default 사용
def safe_int(config, section, option, default):
    try:
        return int(config.get(section, option, fallback=str(default)))
    except ValueError:
        return default

# 문자열 옵션을 읽고 유효하지 않으면 default 반환
def safe_choice(config, section, option, valid_choices, default):

    value = config.get(section, option, fallback=default)
    if value not in valid_choices:
        return default
    return value

# search_config.ini 파일을 읽고 검색 작업 설정을 받음
def load_config():
    config = configparser.ConfigParser()
    try:
        config.read('search_config.ini', encoding='utf-8')
    except FileNotFoundError:
        print(f"'search_config.ini' 설정 파일을 찾을 수 없습니다.")
        return None

    # 검색 관련 데이터를 모두 저장함
    search_dictionary = {}
    for section in config.sections():
        search_dictionary[section] = {
            'keyword': config.get(section, 'keyword', fallback='뉴스'),
            'detail_choice': safe_choice(config, section, 'detail_choice', ['Y', 'N'], 'Y'),
            'alignment': safe_choice(config, section, 'alignment', ['1','2','3'], '1'), # 기본값 : 관련도순
            'duration': safe_choice(config, section, 'duration', ['a', 'd', 'w', 'm'], 'a') # 기본값 : 전체 기간
        }

    # DEFAULT 섹션은 별도로 저장해야 함
    search_dictionary['DEFAULT'] = {
        'desired_count': safe_int(config, 'DEFAULT', 'desired_count', 20),
        'scroll_pause': safe_int(config, 'DEFAULT', 'scroll_pause', 5)
    }
    return search_dictionary
@classmethod
def get_cookie_expires(cls, jar_cookies):
    """
    获取 jar_cookies 里面 sessionid 或 sessionid_ss 或 sid_tt 的有效期
    """
    result = None
    for item in jar_cookies:
        if item.name == "sessionid" or item.name == "sessionid_ss" or item.name == "sid_tt":
            timestamp = item.expires
            if timestamp:
                result = cls.timestamp_to_datetime(timestamp)
    return result


@staticmethod
def timestamp_to_datetime(timestamp):
    """
    时间戳转datetime
    :param timestamp:
    :return: datetime
    """
    result = datetime.fromtimestamp(timestamp)
    return result
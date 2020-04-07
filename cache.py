CHANNEL_CACHE = []
SCORE_CACHE = []

def add_channel_to_cache(channel):
    if not has_entry(channel):
        CHANNEL_CACHE.append(channel)

def has_entry(channel):
    return channel in CHANNEL_CACHE

def remove_channel_from_cache(channel):
    CHANNEL_CACHE.remove(channel)

def add_score_to_cache(value):
    SCORE_CACHE.append(value)

def empty_all_caches():
    SCORE_CACHE = []
    CHANNEL_CACHE = []

def get_mean_score():
    return sum(SCORE_CACHE)/len(SCORE_CACHE)

def get_median_score():
    return SCORE_CACHE[int(len(SCORE_CACHE) / 2)]

def get_answer_count():
    return len(SCORE_CACHE)
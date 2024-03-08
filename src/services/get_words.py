import random


async def get_quiz(data: list[tuple[str, str, int]]) -> tuple[str, list]:
    needed_word = _get_max_weight_word(data)
    data.remove(needed_word)
    use_original_word = random.choice([True, False])

    if use_original_word:
        word = needed_word[0]
        options = [x[1] for x in data]
        options.insert(0, needed_word[1])
    else:
        word = needed_word[1]
        options = [x[0] for x in data]
        options.insert(0, needed_word[0])

    return word, options


def _get_max_weight_word(words):
    total_weight = sum(weight for _, _, weight in words)
    rand_num = random.uniform(0, total_weight)
    cumulative_weight = 0

    for word, translation, weight in words:
        cumulative_weight += weight
        if rand_num <= cumulative_weight:
            return word, translation, weight



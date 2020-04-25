def get_description(text):
    import wikipedia

    wikipedia.set_lang('ru')
    answer = wikipedia.summary(text)
    return answer

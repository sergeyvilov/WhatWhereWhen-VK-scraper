# -*- coding: utf-8 -*-:wq

def remove_rubbish(s):
    n_op_br = s.count('[')
    n_cl_br = s.count(']')
    if n_op_br == n_cl_br > 1:
        start = s.find(']')
        for i in range(len(s) - 1, start, -1):
            if s[i] == '[':
                end = i
                break 
        s = s[start + 1:end]
    s = s.replace(u'(Ответ находится в описании к картинке)','') 
    return s.strip()
        

def get_post(raw_post):
    if raw_post['text'].find(u'questions_of_chgk') < 0:
        return None
    if raw_post.get('likes'):
       likes = raw_post['likes']['count']
    else:
       likes = None
    if raw_post.get('views'):
       views = raw_post['views']['count']
    else:
       views = None
    post = {
        'text': remove_rubbish(raw_post['text']),
        'id': raw_post['id'],
        'date': raw_post['date'],
        'answer': None, 
        'poll': {'yes': None, 'no': None},
        'likes': likes,
        'views': views
    }
    attachments = raw_post['attachments']
    for i in range(len(attachments)):
        if (attachments[i].get('poll') and 
        attachments[i]['poll']['question'].find(u'Получилось') >= 0):
            post['poll']['yes'] = attachments[i]['poll']['answers'][0]['votes']
            post['poll']['no'] = attachments[i]['poll']['answers'][1]['votes']
        if attachments[i].get('photo'):
            post['answer'] = attachments[i]['photo']['text']
    if not post['answer']:
        return None
    return post
    #print('---------')
    #print(post['text'])
    #print(post['id'])
    #print(post['date'])
    #print(post['answer'])
    #print(post['poll']['yes'])
    #print(post['poll']['no'])
    #print(post['likes'])
    #print(post['views'])
    



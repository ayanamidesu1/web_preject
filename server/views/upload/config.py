settings = {
    'paths': {
        'ill': ('H:/web_project/image/', 'H:/web_project/image/thumbnail/'),
        'comic': ('H:/web_project/image/comic/', 'H:/web_project/image/comic/thumbnail/'),
        'novel': ('H:/web_project/image/novel/', 'H:/web_project/image/novel/thumbnail/')
    },
    'queries': {
        'ill': ('INSERT INTO illustration_work (name, content_file_list, belong_to_user, belong_to_user_id, '
                'work_tags, create_time, brief_introduction, age_classification,work_approved) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)'),
        'comic': ('INSERT INTO comic (work_name, content_file_list, belong_to_user, belong_to_userid, create_time, '
                  'work_tags, age_classification, brief_introduction,work_approved) '
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)'),
        'novel': ('INSERT INTO novel_work (work_name, work_cover, belong_to_username, belong_to_userid, '
                  'work_create_time, work_series, work_tags, brief_introduction, author_say, age_classification, '
                  'work_status) '
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    }
}
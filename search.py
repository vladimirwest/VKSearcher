import vk_api
import json
from check_similarity import check_similarity
from operator import itemgetter

phone_num = '+7999999999'
login_pass = ''
user_id = '69041410'

#params:
group_id = ''
school = ''
birth_day = ''
birth_month = ''
age_from = '20'
age_to = '30'
sex = ''
count = '1000'
city = '1'
country = '1'
has_photo = '1'

vk_session = vk_api.VkApi(phone_num, login_pass, api_version = '5.89')
vk_session.auth()
vk = vk_session.get_api()

search = vk.users.search(sex = sex, age_from = age_from, age_to = age_to, count = count, country = country, city = city, group_id = group_id, has_photo = has_photo, fields = 'bdate,blacklisted')

with open('data.txt', 'w') as file:
    file.write(json.dumps(search))

users = search.get('items')

groups = vk.users.getSubscriptions(user_id = user_id, extended = '0')

main_acc_groups = groups.get('groups').get('items')

print('users count: ' + str(len(users)))

count = 0
for user in users:
    count+=1
    print('current percent: ' + str (count/len(users)*100) + ' %')
    if(user.get('is_closed')!=True and str(user.get('blacklisted'))!=str(1)):
        current_user_id = user.get('id')
        user_pages = vk.users.getSubscriptions(user_id = current_user_id, extended = '0')
        user_groups = user_pages.get('groups').get('items')
        #user['groups'] = user_groups
        user['score'] = len((check_similarity(user_groups, main_acc_groups)))/(len(user_groups)+1)*100
        #user['score'] = len(check_similarity(user_groups, main_acc_groups))
    else:
        user['score'] = -1

scored_list = sorted(users, key=itemgetter('score'), reverse=True)
		
with open('scores.txt', 'w') as file:
     file.write(json.dumps(scored_list))
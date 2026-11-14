"""Generates demo-data/demo-year.json: one year of demo activity.
Days are stored as 'ago' (days before today), the app converts them to real dates."""
import json, random
random.seed(2026)
Y = 365
TITLES = ['Почему заявки теряются в директе','3 ошибки в настройке CRM','Как я собираю воронку за вечер','Бот вместо менеджера','Сколько стоит потерянный лид','Kommo за 60 секунд','Автоответ, который продаёт','Разбор заявки подписчика','Сквозная аналитика простыми словами','Как CRM теряет заявки','Автоворонка за 5 минут','Бот для заявок в Telegram','Ошибка, которая стоит клиентов','Разбор воронки подписчика','Что такое сквозная аналитика','Как я веду клиентов в CRM','Три ошибки в карточке сделки','Интеграция без программиста']
videos, results, skills, followers, tasks = [], [], [], [], []
# videos: pace grows from ~1.5 to ~3 per week
for ago in range(Y, -1, -1):
    pace = 1.5 + 1.8 * (Y - ago) / Y            # per week
    if random.random() < pace / 7:
        videos.append({'ago': ago, 'title': random.choice(TITLES)})
for v in videos:
    if random.random() < .45:
        results.append({'ago': max(0, v['ago'] - random.randint(1, 4)), 'views': random.choice([600,900,1200,1800,2600,3400,5200,8100]), 'money': random.choice([0,0,0,0,4500,9000]), 'note': ''})
for ago in range(Y, -1, -1):
    if ago % 2 == 0 and random.random() < .8: skills.append({'ago': ago, 'action': 'workout', 'title': 'Тренировка'})
    if random.random() < .22: skills.append({'ago': ago, 'action': 'exercise', 'title': 'Дикция, 15 минут'})
    if random.random() < .08: skills.append({'ago': ago, 'action': 'method', 'title': random.choice(['Хук в первые 3 секунды','J-cut в монтаже','Субтитры для Reels'])})
    if random.random() < .03: skills.append({'ago': ago, 'action': 'consult', 'title': 'Консультация по воронке'})
    if random.random() < .015: skills.append({'ago': ago, 'action': 'course', 'title': 'Курс по свету'})
    if random.random() < .015: skills.append({'ago': ago, 'action': 'book', 'title': 'Книга по продажам'})
# followers: every ~2 days, 130 -> 850 (S-curve-ish with noise), always monotone
n = Y // 2
val = 130
for i in range(n + 1):
    ago = Y - i * 2
    t = i / n
    target = 130 + (850 - 130) * (0.55 * t + 0.45 * t * t)
    val = max(val, int(target + random.randint(-3, 3)))
    followers.append({'ago': ago, 'count': val})
followers[-1]['ago'] = 0; followers[-1]['count'] = 850
for i, c in enumerate(['Обновить шапку профиля','Написать пяти клиентам','Разобрать воронку','Снять ролик про автоворонку','Записать упражнение на дикцию']):
    tasks.append({'ago': 40 - i * 7, 'doneAgo': 38 - i * 7 if i < 3 else None, 'text': c, 'cat': ['other','sales','sales','content','speech'][i]})
json.dump({'videos': videos, 'results': results, 'skills': skills, 'followers': followers, 'tasks': tasks}, open('demo-data/demo-year.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(videos), len(results), len(skills), len(followers))

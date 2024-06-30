import sqlite3 as sq
import aiosqlite

async def db_start():
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS profile(
                   user_username TEXT PRIMARY KEY,
                   user_id INTEGER,
                   wallet_address TEXT, 
                   ref_link TEXT, 
                   count_invited INTEGER, 
                   payload TEXT, 
                   balance INTEGER,
                   friends_balance INTEGER,
                   user_score INTEGER,
                   friends_score INTEGER,
                   total FLOAT,
                   last_reset_time TEXT
                );''')
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS check_user(
                       user_username TEXT PRIMARY KEY, user_id INTEGER, 
                       canal_ru BOOlEAN, chat_ru BOOlEAN,
                       canal_en BOOlEAN, chat_en BOOlEAN,
                       quest_1 BOOlEAN, quest_2 BOOlEAN, 
                       quest_3 BOOlEAN, quest_4 BOOlEAN, 
                       quest_5 BOOlEAN, quest_6 BOOlEAN                  
                    );''')
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS message(
                       user_username TEXT PRIMARY KEY,
                       admin_message TEXT
                    );''')
    db.commit()

    db.close()



async def create_check_user(user_username, user_id):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    user = cur.execute('''SELECT 1 FROM check_user WHERE user_username == ?;''', (user_username,)).fetchone()
    if not user:
        cur.execute(
            '''INSERT INTO check_user(
                        user_username, user_id, 
                        canal_ru, chat_ru,
                        canal_en, chat_en,
                        quest_1, quest_2, 
                        quest_3, quest_4, 
                        quest_5, quest_6) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);''',
            (user_username, user_id, None, None, None, None, None, None, None, None, None, None))
    db.commit()
    db.close()


async def create_profile(user_username, user_id, payload):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    user = cur.execute('''SELECT 1 FROM profile WHERE user_username == ?;''', (user_username,)).fetchone()
    if not user:
        cur.execute(
            '''INSERT INTO profile(user_username, user_id, wallet_address, 
                                   ref_link, count_invited, payload, balance, friends_balance,
                                   user_score, friends_score, total, last_reset_time) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
            (user_username, user_id, None, "", 0, payload, 0, 0, 0, 0, 0, None))
        if payload != "":
            cur.execute(
                '''UPDATE profile SET count_invited = count_invited + 1 WHERE user_username = ?;''',
                (payload,))
        db.commit()
    db.close()


async def update_link_profile(user_username, ref_link):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    link = cur.execute(f'''SELECT ref_link FROM profile WHERE user_username == '{user_username}';''').fetchone()
    if link[0] == '':
        cur.execute(f'''UPDATE profile SET ref_link = ? WHERE user_username == ?;''', (ref_link, user_username))
        db.commit()
    db.close()

async def get_user_score_profile(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    user_score = cur.execute(f'''SELECT user_score from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return user_score[0]

async def update_canal_ru_check(user_username):
    async with aiosqlite.connect("mydb.db") as db:
        await db.execute('''UPDATE check_user SET canal_ru = TRUE WHERE user_username = ?;''', (user_username,))
        await db.commit()

async def check_canal_ru_status(user_username: str) -> bool:
    async with aiosqlite.connect("mydb.db") as db:
        async with db.execute("SELECT canal_ru FROM check_user WHERE user_username = ?", (user_username,)) as cursor:
            record = await cursor.fetchone()
            if record is None:
                return False
            return record[0]

async def update_canal_en_check(user_username):
    async with aiosqlite.connect("mydb.db") as db:
        await db.execute('''UPDATE check_user SET canal_en = TRUE WHERE user_username = ?;''', (user_username,))
        await db.commit()

async def check_canal_en_status(user_username: str) -> bool:
    async with aiosqlite.connect("mydb.db") as db:
        async with db.execute("SELECT canal_en FROM check_user WHERE user_username = ?", (user_username,)) as cursor:
            record = await cursor.fetchone()
            if record is None:
                return False
            return record[0]

async def update_chat_ru_check(user_username):
    async with aiosqlite.connect("mydb.db") as db:
        await db.execute('''UPDATE check_user SET chat_ru = TRUE WHERE user_username = ?;''', (user_username,))
        await db.commit()

async def check_chat_ru_status(user_username: str) -> bool:
    async with aiosqlite.connect("mydb.db") as db:
        async with db.execute("SELECT chat_ru FROM check_user WHERE user_username = ?", (user_username,)) as cursor:
            record = await cursor.fetchone()
            if record is None:
                return False
            return record[0]

async def update_chat_en_check(user_username):
    async with aiosqlite.connect("mydb.db") as db:
        await db.execute('''UPDATE check_user SET chat_en = TRUE WHERE user_username = ?;''', (user_username,))
        await db.commit()

async def check_chat_en_status(user_username: str) -> bool:
    async with aiosqlite.connect("mydb.db") as db:
        async with db.execute("SELECT chat_en FROM check_user WHERE user_username = ?", (user_username,)) as cursor:
            record = await cursor.fetchone()
            if record is None:
                return False
            return record[0]

async def update_twitter_check(user_username):
    async with aiosqlite.connect("mydb.db") as db:
        await db.execute('''UPDATE check_user SET quest_1 = TRUE WHERE user_username = ?;''', (user_username,))
        await db.commit()

async def check_twitter_status(user_username: str) -> bool:
    async with aiosqlite.connect("mydb.db") as db:
        async with db.execute("SELECT quest_1 FROM check_user WHERE user_username = ?", (user_username,)) as cursor:
            record = await cursor.fetchone()
            if record is None:
                return False
            return record[0]

async def get_count_profile(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    count = cur.execute(f'''SELECT count_invited from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return count[0]

async def update_friends_score():
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE profile SET friends_score = (
                    SELECT IFNULL(SUM(user_score), 0)
                    FROM profile AS friends
                    WHERE friends.payload = profile.user_username
                   );''')
    db.commit()
    db.close()

async def get_friends_score_profile(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    balance = cur.execute(f'''SELECT friends_score from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return balance[0]

async def get_invited_users(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    invited_users = cur.execute('''SELECT user_username, total FROM profile WHERE payload = ?;''', (user_username,)).fetchall()
    db.close()
    return [(user[0], user[1]) for user in invited_users]

async def update_wallet_address(address, user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE profile SET wallet_address = ? WHERE user_username = ?;''', (address, user_username))
    db.commit()
    db.close()

async def get_top_50_users():
    async with aiosqlite.connect("mydb.db") as db:
        cur = await db.execute('''SELECT user_username, total FROM profile ORDER BY total DESC LIMIT 50;''')
        result = await cur.fetchall()
        return result

async def get_wallet_address(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    wallet = cur.execute(f'''SELECT wallet_address from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return wallet[0]

async def get_all_user_ids():
    async with aiosqlite.connect("mydb.db") as db:
        cur = await db.execute('''SELECT user_id FROM profile''')
        result = await cur.fetchall()
        return [row[0] for row in result]

async def db_message_start():
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS message(
                   user_username TEXT PRIMARY KEY,
                   admin_message TEXT
                );''')
    db.commit()
    db.close()

async def create_message(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    user = cur.execute('''SELECT 1 FROM message WHERE user_username == ?;''', (user_username,)).fetchone()
    if not user:
        cur.execute(
            '''INSERT INTO message(user_username, admin_message) VALUES(?,?);''',
            (user_username, ''))
    db.commit()
    db.close()

async def update_message(admin_message, user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE message SET admin_message = ? WHERE user_username = ?;''', (admin_message, user_username))
    db.commit()
    db.close()

async def get_message(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    message = cur.execute(f'''SELECT admin_message from message WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return message[0]

async def update_balance(profit, user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE profile SET balance = balance + ? WHERE user_username = ?;''', (profit, user_username))
    db.commit()
    db.close()

async def get_balance_profile(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    balance = cur.execute(f'''SELECT balance from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return balance[0]

async def update_friends_balance():
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE profile SET friends_balance = (
                    SELECT IFNULL(balance, 0)
                    FROM profile AS friends
                    WHERE friends.payload = profile.user_username
                   );''')
    db.commit()
    db.close()

async def get_friends_balance(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    balance = cur.execute(f'''SELECT friends_balance from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return balance[0]

async def update_total(total, user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    cur.execute('''UPDATE profile SET total = ? WHERE user_username = ?;''', (total, user_username))
    db.commit()
    db.close()

async def get_total(user_username):
    db = sq.connect("mydb.db")
    cur = db.cursor()

    total = cur.execute(f'''SELECT total from profile WHERE user_username == '{user_username}';''').fetchone()
    db.close()
    return total[0]











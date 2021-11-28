import os
import psycopg2

class Database:
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']

        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        
        self.connection.close()

    def commit(self):
        """Commit changes"""

        self.connection.commit()

    def check_level_up(self, new_experience, now_level):
        _experience = new_experience
        _level = now_level

        while _experience >= _level * 10:
            _experience -= _level * 10
            _level += 1

        return {
            'level_up': True if _level > now_level else False,
            'experience': _experience,
            'level': _level
        }

    def create_user(self, discord_user_id, name, guild_id):
        """
        Create user and create level with the user id.
        
        Return inserted user id.
        """

        if not self.check_user_exist(discord_user_id, guild_id):
            self.cursor.execute('INSERT INTO users(discord_user_id, name, guild_id) VALUES(%(discord_user_id)s, %(name)s, %(guild_id)s) RETURNING id', {
                'discord_user_id': int(discord_user_id),
                'name': name,
                'guild_id': int(guild_id)
            })

            new_user_id = self.cursor.fetchone()[0]

            self.cursor.execute('INSERT INTO levels(user_id, level, experience) VALUES(%(new_user_id)s, %(level)s, %(experience)s)', {
                'new_user_id': int(new_user_id),
                'level': 1,
                'experience': 0
            })

            self.commit()

            return new_user_id

    def level_up(self, discord_user_id, guild_id, points):
        """
        Add experience.
        
        Return check_level_up_result.
        """

        self.cursor.execute('SELECT levels.level, levels.experience, levels.id FROM levels INNER JOIN users on users.id = levels.user_id WHERE users.discord_user_id = %(discord_user_id)s AND users.guild_id = %(guild_id)s', {
            'discord_user_id': int(discord_user_id),
            'guild_id': int(guild_id)
        })
        
        now_user = self.cursor.fetchone()

        check_level_up_result = self.check_level_up(now_level=now_user[0], new_experience=points + now_user[1])

        if (check_level_up_result['level_up']):
            self.cursor.execute('UPDATE levels SET level = %(level)s, experience = %(experience)s WHERE id = %(id)s', {
                'level': int(check_level_up_result['level']),
                'experience': int(check_level_up_result['experience']),
                'id': int(now_user[2])
            })
        else:
            self.cursor.execute('UPDATE levels SET experience = %(experience)s WHERE id = %(id)s', {
                'experience': int(check_level_up_result['experience']),
                'id': int(now_user[2])
            })

        self.commit()

        return check_level_up_result

    def get_user_stats(self, discord_user_id, guild_id):
        user = self.cursor.execute('SELECT users.id, users.discord_user_id, users.name, users.guild_id, levels.level, levels.experience FROM levels INNER JOIN users on users.id = levels.user_id WHERE users.discord_user_id = %(discord_user_id)s AND users.guild_id = %(guild_id)s', {
            'discord_user_id': int(discord_user_id),
            'guild_id': int(guild_id)
        })
        
        user = self.cursor.fetchone()

        if user is None:
            return False
        else:
            return {
                'id': user[0],
                'discord_user_id': user[1],
                'name': user[2],
                'guild_id': user[3],
                'level': user[4],
                'experience': user[5]
            }

    def check_user_exist(self, discord_user_id, guild_id):
        self.cursor.execute('SELECT * FROM users WHERE discord_user_id = %(discord_user_id)s AND users.guild_id = %(guild_id)s', {
            'discord_user_id': int(discord_user_id),
            'guild_id': int(guild_id)
        })

        user = self.cursor.fetchone()

        if user:
            return True
        else:
            return False

    def get_user(self, discord_user_id, name, guild_id):
        if not self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        self.cursor.execute('SELECT id, discord_user_id, name, guild_id FROM users WHERE discord_user_id = %(discord_user_id)s AND users.guild_id = %(guild_id)s', {
            'discord_user_id': int(discord_user_id),
            'guild_id': int(guild_id)
        })

        user = self.cursor.fetchone()

        return {
            'id': user[0],
            'discord_user_id': user[1],
            'name': user[2],
            'guild_id': user[3]
        }

    def suggestion_status(self, suggestion_id):
        self.cursor.execute('SELECT id, content, status, user_id FROM suggestions WHERE id = %(id)s', {
            'id': int(suggestion_id)
        })

        suggestion = self.cursor.fetchone()

        if isinstance(suggestion, type(None)):
            return False

        return {
            'id': suggestion[0],
            'content': suggestion[1],
            'status': suggestion[2],
            'user_id':suggestion[3] 
        }

    def new_suggestion(self, discord_user_id, guild_id, name, suggestion):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        if self.get_user_stats(discord_user_id, guild_id)['level'] < 10:
            return False

        user = self.get_user(discord_user_id, name, guild_id)

        self.cursor.execute('INSERT INTO suggestions(content, status, user_id) VALUES(%(content)s, %(status)s, %(user_id)s) RETURNING id', {
            'content': suggestion,
            'status': 'not_yet_approved',
            'user_id': user['id']
        })

        self.commit()

        suggestion_id = self.cursor.fetchone()[0]

        suggestion = self.suggestion_status(suggestion_id)

        return suggestion

    def get_all_my_suggestion(self, discord_user_id, guild_id, name):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        if self.get_user_stats(discord_user_id, guild_id)['level'] < 10:
            return False

        user = self.get_user(discord_user_id, name, guild_id)

        self.cursor.execute('SELECT id, content, status FROM suggestions WHERE user_id = %(user_id)s', {
            'user_id': user['id']
        })

        all_suggestion = list(self.cursor.fetchall())

        all_suggestion_return = [
            {
                'id': i[0],
                'content': i[1],
                'status': i[2],
            }
            for i in all_suggestion
        ]

        return all_suggestion_return

    def get_suggestion_detail(self, discord_user_id, guild_id, name, suggestion_id):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        if self.get_user_stats(discord_user_id, guild_id)['level'] < 10:
            return False

        suggestion = self.suggestion_status(suggestion_id)

        if not suggestion:
            return 'no_suggestion'

        return suggestion

    def get_all_suggestion(self, discord_user_id, guild_id, name):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        if self.get_user_stats(discord_user_id, guild_id)['level'] < 10:
            return False

        user = self.get_user(discord_user_id, name, guild_id)

        self.cursor.execute('SELECT id, content, status FROM suggestions')

        all_suggestion = list(self.cursor.fetchall())

        all_suggestion_return = [
            {
                'id': i[0],
                'content': i[1],
                'status': i[2],
            }
            for i in all_suggestion
        ]

        return all_suggestion_return


    def approve_suggestion(self, discord_user_id, guild_id, name, suggestion_id):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        user = self.get_user(discord_user_id, name, guild_id)
        
        suggestion = self.get_suggestion_detail(discord_user_id, guild_id, name, suggestion_id)

        if suggestion['status'] == 'approved':
            return False

        self.cursor.execute('UPDATE suggestions SET status = %(status)s WHERE id = %(id)s', {
            'status': 'approved',
            'id': int(suggestion_id)
        })

        self.commit()

        return True

    def decline_suggestion(self, discord_user_id, guild_id, name, suggestion_id):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        user = self.get_user(discord_user_id, name, guild_id)

        suggestion = self.get_suggestion_detail(discord_user_id, guild_id, name, suggestion_id)

        if suggestion['status'] == 'declined':
            return False

        self.cursor.execute('UPDATE suggestions SET status = %(status)s WHERE id = %(id)s', {
            'status': 'declined',
            'id': int(suggestion_id)
        })

    def delete_suggestion(self, discord_user_id, guild_id, name, suggestion_id):
        if self.check_user_exist(discord_user_id, guild_id):
            self.create_user(discord_user_id, name, guild_id)

        user = self.get_user(discord_user_id, name, guild_id)

        suggestion = self.get_suggestion_detail(discord_user_id, guild_id, name, suggestion_id)

        if suggestion['status'] == 'deleted':
            return False

        self.cursor.execute('UPDATE suggestions SET status = %(status)s WHERE id = %(id)s', {
            'status': 'deleted',
            'id': int(suggestion_id)
        })

        self.commit()

        return True

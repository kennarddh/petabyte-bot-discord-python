import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data/data.db')

        self.cursor = self.connection.cursor()

    def close():
        self.cursor.close()
        
        self.connection.close()

    def commit(self):
        """Commit changes"""

        self.connection.commit()

    def check_level_up(self, now_experience, now_level):
        _experience = now_experience
        _level = now_level

        while _level * 10 >= _experience:
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
        
        self.cursor.execute('INSERT INTO users(discord_user_id, name, guild_id) VALUES(?,?,?)', (discord_user_id, name, guild_id))

        new_user_id = self.cursor.lastrowid

        self.cursor.execute('INSERT INTO levels(user_id, level, experience) VALUES(?,?,?)', (new_user_id, 0, 1))

        self.commit()

        return new_user_id

    def level_up(self, discord_user_id, guild_id, points):
        """
        Add experience.
        
        Return check_level_up_result.
        """
        now_user = self.cursor.execute('SELECT levels.level, levels.experience, levels.id FROM levels JOIN users on users.id = levels.user_id WHERE users.discord_user_id = ? AND users.guild_id = ?', (discord_user_id, guild_id)).fetchone()

        check_level_up_result = self.check_level_up(now_level=now_user[0], now_experience=now_user[1])

        if (check_level_up_result['level_up']):
            self.cursor.execute('UPDATE levels SET level = ?, experience = ? WHERE id = ?', (
                check_level_up_result['level'],
                check_level_up_result['experience'],
                now_user[2]
            ))
        else:
            self.cursor.execute('UPDATE levels SET experience = ? WHERE id = ?', (
                check_level_up_result['experience'],
                now_user[2]
            ))

        self.commit()

        return check_level_up_result

    def get_user_level(self, discord_user_id, guild_id):
        user = self.cursor.execute('SELECT users.id, users.discord_user_id, users.name, users.guild_id, levels.level, levels.experience FROM levels JOIN users on users.id = levels.user_id WHERE users.discord_user_id = ? AND users.guild_id = ?', (discord_user_id, guild_id)).fetchone()

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
        user = self.cursor.execute('SELECT * FROM users WHERE discord_user_id = ? AND users.guild_id = ?', (discord_user_id, guild_id)).fetchone()

        if user is None:
            return False
        else:
            return True
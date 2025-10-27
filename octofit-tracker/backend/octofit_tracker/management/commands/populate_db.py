from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Collections
        users = db['users']
        teams = db['teams']
        activities = db['activities']
        leaderboard = db['leaderboard']
        workouts = db['workouts']

        # Clean up
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Create unique index for email
        users.create_index([('email', 1)], unique=True)

        # Teams
        marvel_team = {'name': 'Marvel', 'members': ['ironman@hero.com', 'spiderman@hero.com']}
        dc_team = {'name': 'DC', 'members': ['batman@hero.com', 'wonderwoman@hero.com']}
        teams.insert_many([marvel_team, dc_team])

        # Users
        user_data = [
            {'name': 'Iron Man', 'email': 'ironman@hero.com', 'team': 'Marvel'},
            {'name': 'Spider-Man', 'email': 'spiderman@hero.com', 'team': 'Marvel'},
            {'name': 'Batman', 'email': 'batman@hero.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@hero.com', 'team': 'DC'},
        ]
        users.insert_many(user_data)

        # Activities
        activities.insert_many([
            {'user': 'ironman@hero.com', 'activity': 'Running', 'duration': 30},
            {'user': 'spiderman@hero.com', 'activity': 'Cycling', 'duration': 45},
            {'user': 'batman@hero.com', 'activity': 'Swimming', 'duration': 60},
            {'user': 'wonderwoman@hero.com', 'activity': 'Yoga', 'duration': 50},
        ])

        # Leaderboard
        leaderboard.insert_many([
            {'team': 'Marvel', 'points': 75},
            {'team': 'DC', 'points': 110},
        ])

        # Workouts
        workouts.insert_many([
            {'user': 'ironman@hero.com', 'workout': 'Pushups', 'reps': 100},
            {'user': 'spiderman@hero.com', 'workout': 'Pullups', 'reps': 50},
            {'user': 'batman@hero.com', 'workout': 'Squats', 'reps': 80},
            {'user': 'wonderwoman@hero.com', 'workout': 'Plank', 'duration': 5},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

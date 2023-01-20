from pymongo import MongoClient

class Retriever():
    def __init__(self):
        self.client = MongoClient("link") ###
        self.db = self.client['db_name'] ###
        print("connected to the database")

    def get_votes(self):
        """
        Retrive the votes for each candidate in the election.

        Returns:
        2D list: A list of lists of votes for each candidate.
        """
        payload = self.db.collection ###
        votes = payload["results"]
        signature = payload["signature"]
        public_key = payload["public-key"]
        status = payload["status"]
        ##
        return votes


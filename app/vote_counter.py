from phe import paillier
import random
from datetime import datetime
from app.logger import Logger

logger = Logger()


class VoteCounter:
    @classmethod
    def __init__(self, release_time):
        self.pub_key, self.priv_key = paillier.generate_paillier_keypair()
        self.results = {}
        self.is_results_available = False
        self.release_time = release_time
        logger.print_line()
        logger.header("Vote counter has initialized")
        logger.header(
            "Results will be released at " + self.release_time.strftime("%Y-%b-%d %H:%M:%S")
        )
        logger.print_line()

    @classmethod
    def get_public_key(self):
        return self.pub_key

    @classmethod
    def get_encrypted_votes(self):
        logger.none("Collecting votes from the database")
        logger.none("Votes are collected from the database.")
        logger.none("Checking the validity of collected votes from the database.")
        cand = 10
        vote_count = 5
        votes = []
        for _ in range(73):
            vot = (cand - 1) * [0] + [1]
            random.shuffle(vot)
            votes.append(vot)

        for _ in range(2):
            vot = (cand - 1) * [0] + [5]
            random.shuffle(vot)
            votes.append(vot)

        for _ in range(2):
            vot = (cand - 2) * [0] + [1, 1, 1, 1]
            random.shuffle(vot)
            votes.append(vot)
        logger.green("Collected votes from the database are valid")
        return [self.encrypt_vote(vote) for vote in votes]

    @classmethod
    def encrypt_vote(self, vote):
        return [self.pub_key.encrypt(i) for i in vote]

    @classmethod
    def decrypt_vote_counts(self, vote):
        return [self.priv_key.decrypt(i) for i in vote]

    @classmethod
    def count_vote_for_each_candidate(self, encrypted_votes):
        """
        Count the votes for each candidate in the election.

        Parameters:
        encrypted_votes (list): A list of encrypted votes.

        Returns:
        list: A list of the sum of votes for each candidate.
        """
        return [sum(can) for can in zip(*encrypted_votes)]

    @classmethod
    def check_valid_vote(self, vote):
        """
        Check if a given vote is valid or not.

        Args:
            vote (list): The vote that needs to be validated.

        Returns:
            bool: True if the vote is valid, False otherwise.
            string: Message representing what went wrong if invalid
        """
        # check each value is valid
        for v in vote:
            if not (self.priv_key.decrypt(v) == 0 or self.priv_key.decrypt(v) == 1):
                return False, "Vote contains invalid values"

        # check vote consists with at least one vote
        if self.priv_key.decrypt(sum(vote)) <= 0:
            return False, "Vote does not contain sufficient number of votes"

        # check the vote has not contains more than the valid number of votes
        valid_vote_count = 3
        if self.priv_key.decrypt(sum(vote)) > valid_vote_count:
            return False, "Vote contains invalid number of votes"

        return True, "Vote is valid"

    @classmethod
    def generate_results(self):
        """
        Generate and return the final results

        Returns:
            bool: True if the process is completed, False otherwise.
            dict: Results
        """
        # check that whether that it is time calculate results
        if datetime.now() <= self.release_time:
            return False, "Trying to access vote results before publishing"

        if self.is_results_available:
            return True, self.results

        # get votes from the database
        votes = self.get_encrypted_votes()

        # shuffle the collected voted
        random.shuffle(votes)

        # check votes are valid
        valid_votes = []
        rejected = 0
        valid = 0
        total = 0
        logger.none("Checking is a given vote is a valid vote")
        for vote in votes:
            total += 1
            is_valid, msg = self.check_valid_vote(vote)
            if not is_valid:
                logger.warning("Vote is rejected: [REASON]: " + msg)
                rejected += 1
                continue
            valid += 1
            valid_votes.append(vote)
        logger.print_line()
        logger.info("Total Votes    : " + str(total))
        logger.info("Rejected Votes : " + str(rejected))
        logger.info("Valid Votes    : " + str(valid))
        logger.print_line()

        # calculate the final results
        logger.none("Calculating the final results")
        results = self.count_vote_for_each_candidate(valid_votes)
        self.results = {
            "results": self.decrypt_vote_counts(results),
            "valid_votes": valid,
            "rejected_votes": rejected,
            "total_votes": total,
        }
        self.is_results_available = True
        logger.green("Final results are calculated")
        return True, self.results


if __name__ == "__main__":
    vc = VoteCounter(datetime(2023, 1, 20, 13, 40))
    print(vc.generate_results())

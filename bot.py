import praw
import keyring
import random
import re
import time


def generate_response(obj, facts):
    '''Generates a response to a reddit post/comment, providing the author with a fact about rats'''
    # Capture the author of the post/comment
    author = obj.author

    # Select a random fact from a list of facts
    fact = random.choice(facts)

    # Generate a response
    response = f'Did someone mention rats?! Here is a fact about rats:\n\t{fact}\n'
    response += f'Hey, u/{author}, checkout https://www.automatictrap.com/pages/101-rat-facts for more rat facts.'

    return response


if __name__ == '__main__':

    # Reads in information from my ratbot keyring, so only those logged into my computer and account can access
    client_id = keyring.get_password("ratbot", "client_id")
    client_secret = keyring.get_password("ratbot", "client_secret")
    username = keyring.get_password("ratbot", "username")
    password = keyring.get_password("ratbot", "password")
    user_agent = keyring.get_password("ratbot", "user_agent")

    # Read in a list of ratfacts
    with open("ratfacts.txt", "r") as f:
        ratfacts = [line.rstrip() for line in f.readlines()]

    # Set global variables
    CRITERIA = 'rats'

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    # Get CCOMP-12P subreddit
    subreddit = reddit.subreddit('mechanicalMercs')

    # Check the 5 newest submissions
    for submission in subreddit.new(limit=5):

        # Diagnostic
        print(f"Checking Submission: {submission.title}")

        # I save submissions that I've already seen
        if not submission.saved:
            title = submission.title.lower()
            body = submission.selftext.lower()

            # Convert string into list of words
            words = re.findall(r'\w+', title + " " + body)

            # Check whether "rats" is in the resulting list of words
            if CRITERIA in words:
                response = generate_response(submission, ratfacts)

                # So we can skip it next time
                submission.save()

                # Provide a rat fact
                submission.reply(response)

                # UPVOTE
                submission.upvote()

                # Cool down before moving on to the next submission
                time.sleep(5)

        # Peruse the top level comments
        for comment in submission.comments:

            if isinstance(comment, praw.models.MoreComments):
                continue

            # Diagnostic
            print(f"\tChecking Comment: {comment.body}")

            if not comment.saved and comment.author != 'vanrats':
                body = comment.body.lower()

                # Convert string into list of words
                words = re.findall(r'\w+', body)

                # Check that "rats" is in the comment
                if CRITERIA in words:
                    response = generate_response(comment, ratfacts)

                    # So we can skip it next time
                    comment.save()

                    # Provide a rat fact
                    comment.reply(response)

                    # UPVOTE
                    comment.upvote()

                    # Cool down before checking the next comment
                    time.sleep(5)

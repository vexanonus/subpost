# Start here

subpost is one Python file (`subpost.py`), its tests (`test.py`), and a `queue/` folder of drafts.

## The flow

1. **Draft.** A moderator writes a post for one subreddit and says why it helps that community (`--why`).
2. **Approve.** A second person reads it and approves it by name. Drafts nobody approves never post.
3. **Post.** `run post` sends approved posts, ten minutes apart.
4. **Answer.** `run replies` lists replies. A person answers each one on Reddit, in their own words.

## Following Reddit's Responsible Builder Policy

- One dedicated app account, used only for this.
- Only the subreddits and API calls it needs: submit a post, read its own inbox.
- No identical posts across subreddits (enforced in code and tested).
- No voting, no direct messages, no data kept or used for AI training.
- Stays under Reddit's rate limits.

## Making a change

Edit `subpost.py`, add a test to `test.py`, run `./run test`.

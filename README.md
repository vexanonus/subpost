
# subpost: share useful things with a subreddit, with a person checking every post

LAST UPDATED 17 November 2026

<img width="1672" height="941" alt="Subpost_ Human-Curated Resource Board" src="https://github.com/user-attachments/assets/23ef2a9e-62be-4480-9099-7181959edb36" />

Small communities live on good posts. The people who run them rarely have time to post. subpost lets a moderator queue up something worth sharing (a free tool, a guide, a support resource), has a second person read and approve it, then posts it at a calm pace. When people reply, subpost lists the replies so a person answers each one. A person reads every post before it goes out and answers every reply.

## What it does

- **Drafts go into a queue first.** Plain files anyone on the team can read. Nothing reaches Reddit from a draft.
- **A named person approves each post.** The approver's name is saved with the post.
- **One subreddit per post.** It refuses to queue the same post for a second subreddit, so every community gets something written for it.
- **Posts slowly.** At least ten minutes between posts, and it backs off when Reddit's rate limit runs low.
- **Replies go to people.** `subpost replies` lists new comments with links, and a person answers each one.

## What it never does

Vote, send direct messages, comment on other people's posts, scrape, store or sell Reddit data, or use it to train AI. It uses one dedicated app account, only in subreddits where we moderate or have the moderators' permission.

## How to run it

Python 3.9 or newer, nothing to install.

```sh
export REDDIT_CLIENT_ID=... REDDIT_SECRET=... REDDIT_USERNAME=... REDDIT_PASSWORD=...
./run draft rpg "A free dice roller that works offline" --url https://example.com --why "Asked for weekly in the help thread"
./run list
./run approve 2026-11-17-rpg-1a2b3c --by Sam
./run post
./run replies
./run test
```

More in [docs/START.md](docs/START.md).

## Licence

MIT. See [LICENSE](LICENSE).

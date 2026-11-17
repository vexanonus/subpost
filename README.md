# subpost: share useful things with a subreddit, with a person checking every post

LAST UPDATED 17 November 2026

<img width="1672" height="941" alt="Subpost_ Human-Curated Resource Board" src="https://github.com/user-attachments/assets/23ef2a9e-62be-4480-9099-7181959edb36" />

Share things that help people, one subreddit at a time, with a person reading every post before it goes out and answering every reply. It is built so it can't spam: each post is written for one subreddit only, it posts slowly, and it never votes or sends messages.

What gets shared: places people can turn to (suicide support, child-safety courses, parent helplines), things worth reading, and lighter things like games.

## What it does

- **Drafts go into a queue first.** Plain files a person can read. Nothing reaches Reddit from a draft.
- **A named person approves each post.** The approver's name is saved with the post.
- **One subreddit per post.** It refuses to queue the same post for a second subreddit, so every community gets something written for it.
- **Posts slowly.** At least ten minutes between posts, and it backs off when Reddit's rate limit runs low.
- **Replies go to people.** `subpost replies` lists new comments with links, and a person answers each one.

## What it never does

Vote, send direct messages, comment on other people's posts, scrape, store or sell Reddit data, or use it to train AI. It uses one dedicated app account, and follows each subreddit's rules.

## How to run it

Python 3.9 or newer, nothing to install.

```sh
export REDDIT_CLIENT_ID=... REDDIT_SECRET=... REDDIT_USERNAME=... REDDIT_PASSWORD=...
./run draft boardgames "A two-player game for rainy days" --url https://example.com --why "Fits the weekly recommendations thread"
./run list
./run approve 2026-11-17-rpg-1a2b3c --by Alex
./run post
./run replies
./run test
```

More in [docs/START.md](docs/START.md).

## License

MIT. See [LICENSE](LICENSE).

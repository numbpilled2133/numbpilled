# numbpilled

```
the nerve center.
│
├── queue/         ← post drafts (write → auto-publishes)
├── maps/          ← llm refusal boundaries (updated weekly)
├── log/           ← daily system logs
├── gists/         ← gist drafts
├── .github/
│   └── workflows/
│       ├── publish-queue.yml       (mon/wed/fri 1pm)
│       ├── weekly-refusal-map.yml  (sunday)
│       └── update-readme.yml       (every 6 hours)
│
╰── README.md      ← this file (auto-updates)
```

this repo is the brainstem. what happens here radiates outward.

### how it works

| path | purpose |
|------|---------|
| `queue/` | drop a .md file -> auto-posted to bluesky on next cycle |
| `maps/` | weekly refusal boundary snapshots from refusal-mapper |
| `log/` | the account's heartbeat -- auto-generated |
| `gists/` | draft gists awaiting publication |

### connected systems

- [refusal-mapper](/numbpilled2133/refusal-mapper) -- llm boundary cartography
- [terminal-medium](/numbpilled2133/terminal-medium) -- creative terminal experiments
- [@numbpilled](https://bsky.app/profile/numbpilled.bsky.social) -- bluesky

---

*built by [numbpilled](https://github.com/numbpilled2133)*

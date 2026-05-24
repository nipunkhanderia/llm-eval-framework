# 🦗 Locust Beginner Project

A dead-simple load testing project using Locust + Flask.

---

## What's in this project?

| File | What it does |
|---|---|
| `app.py` | A tiny fake website (3 pages) that we'll attack with fake users |
| `locustfile.py` | Tells Locust what the fake users should do |

---

## Step-by-step Setup

### 1. Install the dependencies

Open your terminal and run:

```bash
pip install flask locust
```

---

### 2. Start the fake website

In **Terminal 1**, run:

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Leave this running. This is your "server" being tested.

---

### 3. Start Locust

In **Terminal 2** (a new terminal window), run:

```bash
locust
```

Locust automatically looks for a file named `locustfile.py` in the current folder.

---

### 4. Open the Locust Web UI

Go to your browser and open:

```
http://localhost:8089
```

You'll see a form with 3 fields:

| Field | What to type |
|---|---|
| Number of users | `10` (start small!) |
| Spawn rate | `2` (add 2 users per second) |
| Host | `http://localhost:5000` |

Click **Start swarming** 🚀

---

## What you'll see

Locust shows you a live dashboard:

- **Requests/s** — how many requests per second your server handles
- **Failures** — any pages that returned an error
- **Response time** — how long each page takes to respond (in ms)
- **Charts tab** — pretty graphs of the data over time

---

## Key concepts recap

```
HttpUser    → One simulated user
@task       → Something that user does (visits a page)
weight      → How often that task is chosen (higher = more often)
wait_time   → How long the user pauses between tasks
on_start    → Runs once when the user "arrives" (good for login)
```

---

## Experiment ideas (once you're comfortable)

1. Change `between(1, 3)` to `between(0.1, 0.5)` — users act much faster. What happens to response time?
2. Bump users to 100. Does the server start struggling?
3. Add a new `@task` that hits a page that doesn't exist (`/missing`) — watch the failure count go up.

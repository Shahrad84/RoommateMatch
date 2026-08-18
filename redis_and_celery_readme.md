# Redis & Celery

## Start

### 1. Redis

```bash
redis-server
```

### 2. Celery

in a new terminal:

```bash
celery -A RoommateMatch worker -l info
```

### 3. Django

in a new terminal:

```bash
python manage.py runserver
```

---

## Stop

### Redis

if Redis in terminal is runned:

```bash
Ctrl + C
```

or:

```bash
redis-cli shutdown
```

### Celery

in celery terminal:

```bash
Ctrl + C
```

### Django

in Django terminal:

```bash
Ctrl + C
```

---

## Check Redis

```bash
redis-cli ping
```

If you saw that input , that means Redis is on:

```text
PONG
```

## Check Celery

```bash
ps aux | grep celery
```

---

## summery

every time you wanna run the project

**Terminal 1**

```bash
redis-server
```

**Terminal 2**

```bash
cd /media/shahradlf/New\ Volume/python\ AI\ and\ math/Back\ end\ django/RoommateMatch
celery -A RoommateMatch worker -l info
```

**Terminal 3**

```bash
cd /media/shahradlf/New\ Volume/python\ AI\ and\ math/Back\ end\ django/RoommateMatch
python manage.py runserver
```

for turning off all them press `Ctrl + C`


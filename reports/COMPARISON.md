# Performance Summary by Load Level

| Load | Total Requests | Total Failures | Avg RPS | Avg Response Time |
|------|----------------|----------------|---------|-------------------|
| 10 users | 267 | 0 | 4.63 | 93ms |
| 50 users | 998 | 0 | 16.89 | 267ms |
| 100 users | 905 | 0 | 15.38 | 1122ms |

---

# Endpoint Performance Comparison
**Generated:** 2026-02-10 18:48:15
---

## GET /albums

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 15 | 0 | 29ms | 22ms | 36ms | 0.26 |
| 50 users | 68 | 0 | 277ms | 17ms | 3407ms | 1.15 |
| 100 users | 61 | 0 | 465ms | 18ms | 5579ms | 1.04 |

**Performance Degradation:** +1521.9% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## GET /comments

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 41 | 0 | 82ms | 17ms | 2354ms | 0.71 |
| 50 users | 132 | 0 | 144ms | 15ms | 2761ms | 2.23 |
| 100 users | 131 | 0 | 1019ms | 17ms | 6734ms | 2.23 |

**Performance Degradation:** +1143.5% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## GET /posts

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 57 | 0 | 50ms | 19ms | 1108ms | 0.99 |
| 50 users | 227 | 0 | 227ms | 17ms | 3410ms | 3.84 |
| 100 users | 209 | 0 | 900ms | 17ms | 9309ms | 3.55 |

**Performance Degradation:** +1690.1% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## GET /posts/1

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 35 | 0 | 54ms | 18ms | 1017ms | 0.61 |
| 50 users | 143 | 0 | 194ms | 17ms | 4814ms | 2.42 |
| 100 users | 123 | 0 | 674ms | 17ms | 5737ms | 2.09 |

**Performance Degradation:** +1152.0% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## GET /posts?userId=1

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 14 | 0 | 202ms | 17ms | 1307ms | 0.24 |
| 50 users | 64 | 0 | 215ms | 17ms | 4650ms | 1.08 |
| 100 users | 61 | 0 | 1551ms | 17ms | 5438ms | 1.04 |

**Performance Degradation:** +667.0% at 100 users

⚠️ **WARNING:** Significant performance degradation

---

## GET /users

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 34 | 0 | 179ms | 18ms | 2268ms | 0.59 |
| 50 users | 129 | 0 | 168ms | 17ms | 4736ms | 2.18 |
| 100 users | 128 | 0 | 1100ms | 15ms | 10602ms | 2.18 |

**Performance Degradation:** +515.5% at 100 users

⚠️ **WARNING:** Significant performance degradation

---

## GET /users/1

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 23 | 0 | 70ms | 20ms | 1020ms | 0.40 |
| 50 users | 75 | 0 | 260ms | 18ms | 5048ms | 1.27 |
| 100 users | 74 | 0 | 1335ms | 19ms | 9397ms | 1.26 |

**Performance Degradation:** +1796.8% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## POST /posts

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 23 | 0 | 140ms | 68ms | 1551ms | 0.40 |
| 50 users | 76 | 0 | 409ms | 70ms | 5759ms | 1.29 |
| 100 users | 59 | 0 | 2309ms | 69ms | 9517ms | 1.00 |

**Performance Degradation:** +1551.1% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---

## PUT /posts/1

| Load | Requests | Failures | Avg Time | Min | Max | RPS |
|------|----------|----------|----------|-----|-----|-----|
| 10 users | 25 | 0 | 106ms | 81ms | 285ms | 0.43 |
| 50 users | 84 | 0 | 749ms | 79ms | 5335ms | 1.42 |
| 100 users | 59 | 0 | 1892ms | 80ms | 9336ms | 1.00 |

**Performance Degradation:** +1692.3% at 100 users

🔴 **CRITICAL:** Severe performance degradation

---


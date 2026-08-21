# Common Cron Patterns

## Frequency Patterns

| Description | Expression |
|-------------|------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every 30 minutes | `*/30 * * * *` |
| Every hour | `0 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Daily at midnight | `0 0 * * *` |
| Daily at 6am | `0 6 * * *` |
| Daily at 9am | `0 9 * * *` |
| Weekly (Sunday midnight) | `0 0 * * 0` |
| Weekly (Monday 9am) | `0 9 * * 1` |
| Monthly (1st at midnight) | `0 0 1 * *` |

## Best Practices

1. **Don't schedule at exact hour marks** - Many jobs run at :00, use :05 or :17 to spread load
2. **Use descriptive names** - Makes management easier
3. **Log output** - Redirect to log files for debugging
4. **Set timeouts** - Prevent hung jobs from piling up
5. **Monitor failures** - Use health-monitor skill to alert on failures

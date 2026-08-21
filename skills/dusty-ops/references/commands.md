# Dusty Commands Reference

## Quick Commands

```bash
# Service Management
dusty start          # Start all services
dusty stop           # Stop all services
dusty restart        # Restart all services
dusty status         # Check service health

# Agent Management
dusty agents list              # List all agents
dusty agents add <name>        # Add new agent
dusty agents remove <name>     # Remove agent
dusty agents rotate-keys       # Rotate API keys

# Revenue Operations
dusty revenue report           # Generate revenue report
dusty revenue monthly          # This month's revenue
dusty revenue calculate        # Calculate 10% fees

# Monitoring
dusty logs --tail              # Tail logs
dusty logs --service=core      # Core agent logs
dusty health                   # Full health check
dusty health --exchanges       # Exchange API health

# Maintenance
dusty backup                   # Backup database
dusty backup restore <file>    # Restore from backup
dusty update                   # Update to latest version
dusty rotate-secrets           # Rotate all secrets/keys

# Emergency
dusty emergency-stop           # Immediate stop
dusty emergency-lockdown       # Lockdown mode (no outbound)
```

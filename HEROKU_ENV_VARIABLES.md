# HEROKU Environment Variables Configuration

## Required Environment Variables for Production Deployment

### Flask Configuration
```
FLASK_ENV=production
PORT=(set automatically by Heroku)
```

### Supabase Database Configuration
```
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here  
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
```

### SECTRO Integration
```
SECTRO_API_URL=http://localhost:8080
SECTRO_ENABLED=true
```

### System Configuration
```
SYSTEM_VERSION=36.1
ALLOWED_HOSTS=*
CORS_ORIGINS=*
```

## Heroku CLI Commands to Set Variables

```bash
# Set Supabase configuration
heroku config:set SUPABASE_URL=your_supabase_url
heroku config:set SUPABASE_ANON_KEY=your_anon_key
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your_service_key

# Set SECTRO configuration  
heroku config:set SECTRO_API_URL=http://localhost:8080
heroku config:set SECTRO_ENABLED=true

# Set Flask environment
heroku config:set FLASK_ENV=production
heroku config:set SYSTEM_VERSION=36.1
```

## Database Migration (if needed)
The app uses existing Supabase PostgreSQL database, no migration required. 
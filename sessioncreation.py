from staffspy import LinkedInAccount

# First-time login to create the session
account = LinkedInAccount(
    session_file="session.pkl",  # where session info will be stored
    log_level=2
)

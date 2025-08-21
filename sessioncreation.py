from staffspy import LinkedInAccount

# First-time login to create the session
account = LinkedInAccount(
    session_file="session.pkl",  # where session info will be stored
    log_level=2
)

# # # This will open a browser to log in manually
# # account.create_session()  # <-- make sure to call this


# from staffspy import LinkedInAccount

# # This opens a browser ONLY the first time
# account = LinkedInAccount(
#     session_file="session.pkl",
#     log_level=2
# )

# # Only call this once to save session
# account.create_session()

team 4 README
Zane Dawson and Garret Eatinger
APIs:
    login_get:
        Renders the html for the login page at the given URL
    login_post:
        Reads the entered data in the forms and compares them with the data-
        base. If it is a user, they are logged in, If they aren't, then the
        login page reloads.
    profile_get:
        Uses hash from the URL to get userdata and posts that are from that
        user from the database. Then sends data to the profilecards html
        for rendering.
    profile_post:
        Not Used.
    post_delete:
        Deletes a post with the given posthash.
    post_get:
        Takes the hash of the user viewing the post along with the hash of
        the post to render the full post.
    feed_get:
        Uses the userhash to grab all posts not created by the user and
        renders them in reverse-chronological order with pagination.
    create_get:
        Renders the html for the post creation page.
    create_post:
        Uses the entered data to create the post and save it to the database.
        Creates a posthash based off the time and content of the post.
    register_get:
        Renders the html for the registration page
    register_post:
        Takes the entered data in the forms and adds them to the database.
        Uses the entered data to create a hash unique to said user. If someone
        tries to register with a prexisting username and password, they are
        instead logged in.
    votes_get:
        Loads the data for the posts' likes/dislikes on a given page.
    votes_post:
        Whenever a new like/dislike is created, the API scrubs the previous
        row of that like/dislike if it exists, recreates it, and then fills
        the like/dislike column with the correct type.

Schema:
    Foreign keys are enabled
    users:
        name:
            username associated with account
        pass:
            password associated with account
        hash:
            unique hash generated from name and pass
    posts:
        userhash (foreign referencing users->hash):
            the hash of the user that made the post
        time:
            the time the post was created
        posthash:
            unique post hash created from content of post and time of creation
        likes:
            current like amount
        content:
            contains the body of the post
        title:
            contains the title of the post
    likes:
        userhash (foreign referencing users->hash):
            the hash of the user that is viewing the post when it is liked/disliked
        posthash:
            unique post hash created from content of post and time of creation
        type:
            upvote or downvote From specific user on specific post

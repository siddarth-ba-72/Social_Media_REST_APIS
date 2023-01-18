CREATE_MESSAGES_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        likes_count INTEGER DEFAULT 0
    );
    """
)

ADD_MESSAGE_TO_TABLE = (
    """
    INSERT INTO messages (text) VALUES (%s) RETURNING text;
    """
)

VIEW_ALL_MESSAGES = (
    """
    SELECT messages.text FROM messages
    ORDER BY messages.created_at DESC;
    """
)

LIST_ALL_MESSAGES_WITH_LIKES = (
    """
    SELECT messages.message, messages.likes_count
    FROM messages
    ORDER BY messages.created_at DESC;
    """
)

CREATE_LIKES_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS likes (
        id SERIAL PRIMARY KEY,
        message_id INTEGER REFERENCES messages(id),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
)

TRIGGER_FOR_LIKE = (
    """
    CREATE OR REPLACE FUNCTION like_a_msg_func() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE messages SET likes_count = likes_count + 1 WHERE id = NEW.message_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER like_msg_trigger
    BEFORE INSERT ON likes
    FOR EACH ROW
    EXECUTE FUNCTION like_a_msg_func();
    """
)

TRIGGER_FOR_UNLIKE = (
    """
    CREATE OR REPLACE FUNCTION unlike_a_msg_func() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE messages SET likes_count = likes_count - 1 WHERE id = NEW.message_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE TRIGGER unlike_msg_trigger
    AFTER DELETE ON likes
    FOR EACH ROW
    EXECUTE FUNCTION unlike_a_msg_func();
    """
)

# CREATE OR REPLACE FUNCTION update_likes_count() RETURNS TRIGGER AS $$
#     BEGIN
#         UPDATE messages SET likes_count = (SELECT COUNT(*) FROM likes WHERE message_id = NEW.message_id) WHERE id = NEW.message_id;
#         RETURN NEW;
#     END;
#     $$ LANGUAGE plpgsql;

# CREATE TRIGGER update_likes_trigger
#     BEFORE INSERT OR DELETE ON likes
#     FOR EACH ROW
#     EXECUTE FUNCTION update_likes_count();

LIKE_A_MESSAGE = (
    """
    INSERT INTO likes (message_id) values (%s);
    """
)

UNLIKE_A_MESSAGE = (
    """
    DELETE FROM likes WHERE likes.message_id = (%s)
    AND likes.created_at in (
        SELECT MAX(created_at)
        FROM likes
        WHERE likes.message_id = (%s)
    );
    """
)

-- DROP TABLE USERS1_ARTICLES1;
-- DROP SEQUENCE USERS1_ARTICLES1_LOG_SEQ;

-- CREATE SEQUENCE USERS1_ARTICLES1_LOG_SEQ;

-- CREATE TABLE USERS1_ARTICLES1 (
--     user_id NUMBER NOT NULL,
--     FOREIGN KEY(user_id) REFERENCES USERS1(id),
--     article_id NUMBER NOT NULL,
--     FOREIGN KEY(article_id) REFERENCES ARTICLES1(id)
-- );


CREATE OR REPLACE PACKAGE users_articles_pkg AS
  CURSOR users_articles_cur (
    p_user_id     users1_articles1.user_id%TYPE
    -- p_article_id  users1_articles1.article_id%TYPE
  ) IS
  SELECT user_id, article_id 
  FROM users1_articles1 
  WHERE user_id = p_user_id;

  TYPE users_articles_array IS
    TABLE OF users_articles_cur%rowtype;

  FUNCTION select_users_articles_where (
    p_user_id     users1_articles1.user_id%TYPE
  ) RETURN users_articles_array 
    PIPELINED;


  PROCEDURE insert_users_articles (
    p_user_id     users1_articles1.user_id%TYPE,
    p_article_id  users1_articles1.article_id%TYPE
  );

  PROCEDURE delete_users_articles (
    p_user_id     users1_articles1.user_id%TYPE,
    p_article_id  users1_articles1.article_id%TYPE
  );
END;
/

CREATE OR REPLACE PACKAGE BODY users_articles_pkg AS
  FUNCTION select_users_articles_where (
    p_user_id     users1_articles1.user_id%TYPE
  ) RETURN users_articles_array
    PIPELINED
  IS
  BEGIN
    FOR user_article IN users_articles_cur(p_user_id) LOOP PIPE ROW ( user_article );
    END LOOP;
    return;
  END;

  PROCEDURE insert_users_articles (
    p_user_id     users1_articles1.user_id%TYPE,
    p_article_id  users1_articles1.article_id%TYPE
  ) IS
  BEGIN
    INSERT INTO users1_articles1 VALUES (
        p_user_id, 
        p_article_id
    );
    COMMIT;
  END;

  PROCEDURE delete_users_articles (
    p_user_id     users1_articles1.user_id%TYPE,
    p_article_id  users1_articles1.article_id%TYPE
  ) IS
  BEGIN
    DELETE FROM users1_articles1 WHERE user_id=p_user_id AND article_id=p_article_id;
    COMMIT;
  END;

END;
/


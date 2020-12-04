CREATE OR REPLACE PACKAGE users_pkg AS
  CURSOR users_cur IS
    SELECT id, email, first_name, last_name
    FROM users1;

  TYPE users_array IS
    TABLE OF users_cur%rowtype;

  FUNCTION select_all_users RETURN users_array
    PIPELINED;

  CURSOR user_cur (
    p_email      users1.email%TYPE,
    p_password   users1.password%TYPE
  ) IS
  SELECT id, email, first_name, last_name
  FROM users1
  WHERE email = p_email
    AND password = p_password;

  TYPE user_array IS
    TABLE OF user_cur%rowtype;

  FUNCTION select_user_where (
    email      users1.email%TYPE,
    password   users1.password%TYPE
  ) RETURN user_array
    PIPELINED;

  PROCEDURE insert_user (
    email        users1.email%TYPE,
    password     users1.password%TYPE,
    first_name   users1.first_name%TYPE,
    last_name    users1.last_name%TYPE
  );
END;
/

CREATE OR REPLACE PACKAGE BODY users_pkg AS
  FUNCTION select_all_users RETURN users_array
    PIPELINED
  IS
  BEGIN
    FOR user IN users_cur LOOP PIPE ROW ( user );
    END LOOP;
    return;
  END;

  FUNCTION select_user_where (
    email      users1.email%TYPE,
    password   users1.password%TYPE
  ) RETURN user_array
    PIPELINED
  IS
  BEGIN
    FOR user IN user_cur(email, password) LOOP PIPE ROW ( user );
    END LOOP;

    return;
  END;

  PROCEDURE insert_user (
    email        users1.email%TYPE,
    password     users1.password%TYPE,
    first_name   users1.first_name%TYPE,
    last_name    users1.last_name%TYPE
  ) IS
  BEGIN
    INSERT INTO users1 VALUES (
      users1_seq.NEXTVAL,
      email,
      password,
      first_name,
      last_name
    );
    COMMIT;
  END;
END;
/


CREATE OR REPLACE PACKAGE articles_pkg AS
  PROCEDURE insert_article (
    source      sources1.name%TYPE, 
    category    categories1.name%TYPE,
    author      articles1.author%TYPE, 
    title       articles1.title%TYPE, 
    description articles1.description%TYPE, 
    url         articles1.url%TYPE, 
    urlToImage  articles1.urlToImage%TYPE, 
    content     articles1.content%TYPE
  );
END;
/

CREATE OR REPLACE PACKAGE BODY articles_pkg AS
  PROCEDURE insert_article (
    source      sources1.name%TYPE, 
    category    categories1.name%TYPE, 
    author      articles1.author%TYPE,
    title       articles1.title%TYPE,
    description articles1.description%TYPE,
    url         articles1.url%TYPE,
    urlToImage  articles1.urlToImage%TYPE,
    content     articles1.content%TYPE
  ) IS 
    source_id NUMBER := NULL;
    category_id NUMBER := NULL;
  BEGIN 
    BEGIN 
      SELECT id INTO source_id FROM SOURCES1 WHERE name=source;
    Exception
      WHEN no_data_found THEN source_id := NULL;
    END;

    BEGIN 
      SELECT id INTO category_id FROM CATEGORIES1 WHERE name=category;
    Exception
      WHEN no_data_found THEN category_id := NULL;
    END;

    IF source_id IS NULL THEN
      INSERT INTO SOURCES1 VALUES(SOURCES1_SEQ.NEXTVAL, source);
      source_id := SOURCES1_SEQ.currval;
    END IF;

    IF category_id IS NULL THEN
      INSERT INTO CATEGORIES1 VALUES(CATEGORIES1_SEQ.NEXTVAL, category);
      category_id := CATEGORIES1_SEQ.currval;
    END IF;

    INSERT INTO ARTICLES1 VALUES(ARTICLES1_SEQ.NEXTVAL, source_id, category_id, author, title, description, url, urlToImage, SYSDATE, content);
    COMMIT;
  END;
END;
/


CREATE OR REPLACE PACKAGE categories_pkg AS
  CURSOR categories_cur IS
    SELECT * FROM categories1;

  TYPE categories_array IS
    TABLE OF categories_cur%rowtype;
  FUNCTION select_all_categories RETURN categories_array
    PIPELINED;
END;
/

CREATE OR REPLACE PACKAGE BODY categories_pkg AS

  FUNCTION select_all_categories RETURN categories_array
    PIPELINED
  IS
  BEGIN
    FOR user IN categories_cur LOOP PIPE ROW ( user );
    END LOOP;
    return;
  END;

END;
/


CREATE OR REPLACE PACKAGE users_articles_pkg AS
  CURSOR users_articles_cur (
    p_user_id     users1_articles1.user_id%TYPE
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


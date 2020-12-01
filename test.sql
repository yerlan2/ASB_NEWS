

-- DROP TABLE USERS;
-- DROP SEQUENCE USERS_SEQ;
/* 
CREATE TABLE USERS (
    id          NUMBER PRIMARY KEY,
    email       VARCHAR2(255) NOT NULL UNIQUE,
    password    VARCHAR2(510) NOT NULL,
    first_name  VARCHAR2(255) NOT NULL,
    last_name   VARCHAR2(255) 
);
CREATE SEQUENCE USERS_SEQ;
/* */

/* SQL> desc users;

 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 ID                                        NOT NULL NUMBER(38)
 NAME                                      NOT NULL VARCHAR2(255)
 PASSWORD                                  NOT NULL VARCHAR2(510)
 FIRST_NAME                                NOT NULL VARCHAR2(255)
 LAST_NAME                                 NOT NULL VARCHAR2(255)

*/

-- INSERT INTO USERS VALUES(3, 'jadeben', 'password', 'Jade', 'Ben');



-- DROP TABLE ARTICLES;
-- DROP SEQUENCE ARTICLES_SEQ;
-- DROP TABLE CATEGORIES;
-- DROP SEQUENCE CATEGORIES_SEQ;
-- DROP TABLE SOURCES;
-- DROP SEQUENCE SOURCES_SEQ;

-- CREATE SEQUENCE SOURCES_SEQ;
/* 
CREATE TABLE SOURCES (
    id      NUMBER PRIMARY KEY,
    name    VARCHAR2(255) NOT NULL UNIQUE
);
/* */

-- CREATE SEQUENCE CATEGORIES_SEQ;
/* 
CREATE TABLE CATEGORIES (
    id      NUMBER PRIMARY KEY,
    name    VARCHAR2(255) NOT NULL UNIQUE
);
/* */

-- CREATE SEQUENCE ARTICLES_SEQ;
/* 
CREATE TABLE ARTICLES (
    id              NUMBER PRIMARY KEY,
    source_id       NUMBER NOT NULL,
    FOREIGN KEY(source_id) REFERENCES SOURCES(id),
    category_id     NUMBER NOT NULL,
    FOREIGN KEY(category_id) REFERENCES CATEGORIES(id),
    author          VARCHAR2(255),
    title           VARCHAR2(511) NOT NULL,
    description     VARCHAR2(2047),
    url             VARCHAR2(511),
    urlToImage      VARCHAR2(1023),
    publishedAt     DATE NOT NULL,
    content         VARCHAR2(4000)
);
/* */


CREATE OR REPLACE PACKAGE users_pkg AS
  CURSOR users_cur IS
  SELECT
    id,
    email,
    first_name,
    last_name
  FROM
    users;

  TYPE users_array IS
    TABLE OF users_cur%rowtype;

  FUNCTION select_all_users RETURN users_array
    PIPELINED;

  PROCEDURE insert_user (
    email        users.email%TYPE,
    password     users.password%TYPE,
    first_name   users.first_name%TYPE,
    last_name    users.last_name%TYPE
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

  PROCEDURE insert_user (
    email        users.email%TYPE,
    password     users.password%TYPE,
    first_name   users.first_name%TYPE,
    last_name    users.last_name%TYPE
  ) IS
  BEGIN
    INSERT INTO users VALUES (
      users_seq.NEXTVAL,
      email,
      password,
      first_name,
      last_name
    );
    COMMIT;
  END;
END;
/


CREATE OR REPLACE PROCEDURE insert_article (
    source      VARCHAR2, 
    category    VARCHAR2, 
    author      VARCHAR2,
    title       VARCHAR2,
    description VARCHAR2,
    url         VARCHAR2,
    urlToImage  VARCHAR2,
    publishedAt DATE,
    content     VARCHAR2
) IS 
    source_id NUMBER := NULL;
    category_id NUMBER := NULL;
BEGIN 
    BEGIN 
        SELECT id INTO source_id FROM SOURCES WHERE name=source;
    Exception
        WHEN no_data_found THEN
            source_id := NULL;
    END;

    BEGIN 
        SELECT id INTO category_id FROM CATEGORIES WHERE name=category;
    Exception
        WHEN no_data_found THEN
            category_id := NULL;
    END;

    IF source_id IS NULL THEN
        INSERT INTO SOURCES VALUES(SOURCES_SEQ.NEXTVAL, source);
        source_id := SOURCES_SEQ.currval;
    END IF;

    IF category_id IS NULL THEN
        INSERT INTO SOURCES VALUES(CATEGORIES_SEQ.NEXTVAL, category);
        category_id := CATEGORIES_SEQ.currval;
    END IF;

    INSERT INTO ARTICLES VALUES(ARTICLES_SEQ.NEXTVAL, source_id, category_id, author, title, description, url, urlToImage, publishedAt, content);
    COMMIT;
END;
/

CREATE OR REPLACE PACKAGE categories_pkg AS
  CURSOR categories_cur IS
    SELECT * FROM categories;

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
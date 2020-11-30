

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



DROP TABLE ARTICLES;
DROP SEQUENCE ARTICLES_SEQ;
DROP TABLE CATEGORIES;
DROP SEQUENCE CATEGORIES_SEQ;
DROP TABLE SOURCES;
DROP SEQUENCE SOURCES_SEQ;

CREATE SEQUENCE SOURCES_SEQ;
/* */
CREATE TABLE SOURCES (
    id      NUMBER PRIMARY KEY,
    name    VARCHAR2(255) NOT NULL UNIQUE
);
/* */

CREATE SEQUENCE CATEGORIES_SEQ;
/* */
CREATE TABLE CATEGORIES (
    id      NUMBER PRIMARY KEY,
    name    VARCHAR2(255) NOT NULL UNIQUE
);
/* */

CREATE SEQUENCE ARTICLES_SEQ;
/* */
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
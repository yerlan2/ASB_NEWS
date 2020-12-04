DROP TABLE USERS1_ARTICLES1;
DROP TABLE USERS1_ARTICLES1_LOG;
DROP SEQUENCE USERS1_ARTICLES1_LOG_SEQ;

DROP TABLE USERS1_LOG;
DROP TABLE USERS1;
DROP SEQUENCE USERS1_LOG_SEQ;
DROP SEQUENCE USERS1_SEQ;

DROP TABLE ARTICLES1_LOG;
DROP TABLE SOURCES1_LOG;
DROP TABLE CATEGORIES1_LOG;
DROP SEQUENCE ARTICLES1_LOG_SEQ;
DROP SEQUENCE SOURCES1_LOG_SEQ;
DROP SEQUENCE CATEGORIES1_LOG_SEQ;

DROP TABLE ARTICLES1;
DROP TABLE SOURCES1;
DROP TABLE CATEGORIES1;
DROP SEQUENCE ARTICLES1_SEQ;
DROP SEQUENCE SOURCES1_SEQ;
DROP SEQUENCE CATEGORIES1_SEQ;

-- CREATE TRIGGER >>> CREATE TABLE
CREATE OR REPLACE TRIGGER create_table_log_trigger
	AFTER DDL ON SCHEMA
BEGIN
	IF ORA_SYSEVENT = 'CREATE' AND ORA_DICT_OBJ_TYPE = 'TABLE' AND NOT ORA_DICT_OBJ_NAME LIKE '%_LOG' THEN
		DBMS_OUTPUT.PUT_LINE('>>> '|| ORA_DICT_OBJ_NAME);
		create_log_trg(ORA_DICT_OBJ_NAME);
	END IF;
END;
/

-- CREATE LOG TABLE AND TRIGGER
CREATE OR REPLACE PROCEDURE create_log_trg(p_table_name VARCHAR2) IS 
	create_log VARCHAR2(32767);
	create_trg VARCHAR2(32767);

	CURSOR column_name_cur IS 
		SELECT column_name, data_type, data_length 
		FROM all_tab_cols
		WHERE table_name = p_table_name;
BEGIN 
	-- CREATE LOG TABLE
	create_log := 'CREATE TABLE '||p_table_name||'_LOG(ID NUMBER, OPERATION_DATE DATE, ';
	FOR i IN column_name_cur LOOP
		IF i.data_type IN ('NUMBER', 'DATE') THEN
			create_log := create_log||'OLD_'||i.column_name||' '||i.data_type||', ';
			create_log := create_log||'NEW_'||i.column_name||' '||i.data_type||', ';
		ELSE
			create_log := create_log||'OLD_'||i.column_name||' '||i.data_type||'('||i.data_length||'), ';
			create_log := create_log||'NEW_'||i.column_name||' '||i.data_type||'('||i.data_length||'), ';
		END IF;
	END LOOP;
	create_log := create_log ||'ACTION VARCHAR(255), ACTIONAUTHOR VARCHAR(255))';
	EXECUTE IMMEDIATE create_log;
  DBMS_OUTPUT.PUT_LINE('LOG TABLE CREATED');

	-- CREATE LOG TRIGGER
	create_trg := 'CREATE OR REPLACE TRIGGER '||p_table_name||'_TRIGGER '||
		'AFTER INSERT OR UPDATE OR DELETE ON '||p_table_name||' FOR EACH ROW '||
		'DECLARE '||
			'PROCEDURE insert_into_LOG (p_action VARCHAR2) IS '||
			'BEGIN '||
				'INSERT INTO '||p_table_name||'_LOG VALUES ('||
					p_table_name||'_LOG_SEQ.NEXTVAL,'||
					'SYSDATE,';
					FOR i IN column_name_cur LOOP
						create_trg := create_trg||':OLD.'||i.column_name||',';
						create_trg := create_trg||':NEW.'||i.column_name||',';
					END LOOP;
					create_trg := create_trg||
					'p_action,'||
					'USER'||
				');'||
			'END;'||
		'BEGIN '||
			'IF inserting THEN '||
				'insert_into_log(''INSERT'');'||
			'ELSIF deleting THEN '||
				'insert_into_log(''DELETE'');'||
			'ELSIF updating THEN '||
				'insert_into_log(''UPDATE'');'||
			'END IF;'||
		'END;';
	EXECUTE IMMEDIATE create_trg;
  DBMS_OUTPUT.PUT_LINE('LOG TRIGGER CREATED');
END;
/

CREATE SEQUENCE USERS1_SEQ;
CREATE SEQUENCE USERS1_LOG_SEQ;

CREATE TABLE USERS1 (
  id          NUMBER PRIMARY KEY,
  email       VARCHAR2(255) NOT NULL UNIQUE,
  password    VARCHAR2(511) NOT NULL,
  first_name  VARCHAR2(255) NOT NULL,
  last_name   VARCHAR2(255) 
);

CREATE SEQUENCE SOURCES1_LOG_SEQ;
CREATE SEQUENCE SOURCES1_SEQ;
CREATE TABLE SOURCES1 (
  id      NUMBER PRIMARY KEY,
  name    VARCHAR2(255) NOT NULL UNIQUE
);


CREATE SEQUENCE CATEGORIES1_LOG_SEQ;
CREATE SEQUENCE CATEGORIES1_SEQ;
CREATE TABLE CATEGORIES1 (
  id      NUMBER PRIMARY KEY,
  name    VARCHAR2(255) NOT NULL UNIQUE
);


CREATE SEQUENCE ARTICLES1_LOG_SEQ;
CREATE SEQUENCE ARTICLES1_SEQ;
CREATE TABLE ARTICLES1 (
  id              NUMBER PRIMARY KEY,
  source_id       NUMBER NOT NULL,
  FOREIGN KEY(source_id) REFERENCES SOURCES1(id),
  category_id     NUMBER NOT NULL,
  FOREIGN KEY(category_id) REFERENCES CATEGORIES1(id),
  author          VARCHAR2(255),
  title           VARCHAR2(511) NOT NULL,
  description     VARCHAR2(2047),
  url             VARCHAR2(511),
  urlToImage      VARCHAR2(1023),
  publishedAt     DATE NOT NULL,
  content         VARCHAR2(4000)
);

CREATE SEQUENCE USERS1_ARTICLES1_LOG_SEQ;
CREATE TABLE USERS1_ARTICLES1 (
  user_id NUMBER NOT NULL,
  FOREIGN KEY(user_id) REFERENCES USERS1(id),
  article_id NUMBER NOT NULL,
  FOREIGN KEY(article_id) REFERENCES ARTICLES1(id)
);
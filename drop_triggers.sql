BEGIN  
  FOR i in (select trigger_name, owner from dba_triggers where owner = 'HR' ) LOOP
    EXECUTE IMMEDIATE 'DROP TRIGGER '|| i.owner || '.' || i.trigger_name;
  END LOOP;  
END;
/

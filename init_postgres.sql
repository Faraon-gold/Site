-- Скрипт инициализации PostgreSQL

-- Создаем пользователя, если он не существует
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='postgres') THEN
        CREATE ROLE postgres LOGIN PASSWORD '1234' SUPERUSER CREATEDB CREATEROLE;
    END IF;
END
$$;
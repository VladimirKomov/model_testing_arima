BACKUP_FILE=../dump/emerson_bk
CONTAINER_NAME=pg-bk-db

include .env
export

.PHONY: network up restore all

# Отдельная цель для создания сети (один раз вручную)
network:
	docker network create model_testing_arima_arima_network

# Поднимаем контейнер
up:
	docker-compose --env-file .env -f docker-compose.yml -f docker-compose.base.yml up -d

# Восстанавливаем БД
restore:
	docker cp $(BACKUP_FILE) $(CONTAINER_NAME):/dump.bk
	docker exec -i $(CONTAINER_NAME) pg_restore -U $(POSTGRES_USER) -d $(POSTGRES_DB) --clean --no-owner /dump.bk

first_restore:
	docker cp $(BACKUP_FILE) $(CONTAINER_NAME):/dump.bk
	docker exec -i $(CONTAINER_NAME) pg_restore -U $(POSTGRES_USER) -d $(POSTGRES_DB) --no-owner /dump.bk

# Всё вместе (если сеть уже создана)
all: up first_restore

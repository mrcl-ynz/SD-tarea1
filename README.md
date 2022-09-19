# Tarea 1 - Sistemas Distribuidos

Para levantar las instancias dentro de la topología
```sh
docker-compose up --build
```

GET
```
http://localhost:8000/search?search=ejemplo
```

Para bajar las instancias del compose
```
docker-compose down
```

Borrar cache en contenedores
```
docker system prune -a
```

Borrar cache en volumenes
```
docker volume rm $(docker volume ls -q)
```
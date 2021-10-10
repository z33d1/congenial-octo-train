## RSOI lab 2 Miroservices
Users - const  
Cards - const

[![Build Status](https://travis-ci.com/bmstu-rsoi/lab2-microservices-zeed951.svg?branch=dev)](https://travis-ci.com/bmstu-rsoi/lab2-microservices-zeed951)


root URI = `http://localhost:8080`

| URI | METHOD | Description |Body parameters | Parameters | Status codes|
| :---:              | :---:|    :---:      |:---:      | :---:      | :---: |
| /card?page={page}&size={size} | GET | Get all cards with pagination| - | page, size(optional) | 200, 400, 404 |
| /card/{card_id}| GET | Get info about card | - | card_id | 200, 404 |
| /user/{user_id}| GET | Get info about user | - | user_id | 200, 404 |
| /user/{user_id}/order| GET | Get all orders for user | - | user_id | 200, 404 |
| /user/{user_id}/order| POST | Get all orders for user | card_id | user_id | 200, 400, 404 |
| /user/{user_id}/order| DELETE | Delete all orders for user | - | user_id | 204, 404 |
| /user/{user_id}/order/{order_id}| DELETE | Delete order by id for user | - | user_id order_id | 204, 404 |
| /user/{user_id}/order/{order_id}| GET | Get order by id for user | - | user_id order_id | 200, 404 |


# Applifting Python 3 backend developer exercise

Simple python project for Applifting company

## Installation

1. Make sure you have docker downloaded
2. cd into app root
3. run the command to build
```bash
docker build -t applifting .
```
4. Run the following command to start
```bash
docker run -p 8000:8000 applifting
```
5. Your app will now run on 0.0.0.0:8000


## Api

#### Get JWToken
  Request Json Web Token tu authorise all future requests
  
* **URL**

  `/api/token/`

* **Method:**

  `POST`
  
* **Data Params**

  **Required:**

  `username="matej"`<br>
  `password="applifting2020"`
  
  This is hardcoded in app.management.commands.init_admin.py for demonstration purposes only.
  
* **Success Response:**

  * **Code:** 200 <br>
    **Content:** `{
    "refresh": "[string]",
    "access": "[string]"
}`

#### Create a product
  Create a product and register it with the offers microservice

* **URL**

  `/product/`

* **Method:**

  `POST`

* **Headers:**

  `Bearer: [your token]`
  
* **Data Params**

  **Required:**

  `name=[string]`
  `description=[string]`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{
    "id": [string],
    "name": [string],
    "description": [description]
    }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST

    **Content:** `Offers microservice failed to register a product`

  OR

  * **Code:** 401 UNAUTHORISED

    **Content:** `You are not authorised to make this request`

* **Sample Call:**

  `requests.post('http://0.0.0.0:5000/product/', data={"name": "Harry Potter", 
  "description": "A book about a wizard."})`

<br>

#### Change a product
  Put (change) a product's name and description

* **URL**

  `/product/<str:product_id>/`

* **Method:**

  `PUT`

* **Headers:**

  `Bearer: [your token]`
  
* **Data Params**

  **Required:**

  `name=[string]`
  `description=[string]`

* **Success Response:**

  * **Code:** 200
 
* **Sample Call:**

  `requests.put('http://0.0.0.0:5000/product/d65ca39d-1818-45b8-98b4-4dc60f2701a0/', 
  data={"name": "Harry Potter", "description": "A book about a wizard."})`
  

<br>

#### Get a product
  Get a product's name and description

* **URL**

  `/product/<str:product_id>`

* **Method:**

  `GET`

* **Headers:**

  `Bearer: [your token]`
  
* **Success Response:**

  * **Code:** 200
  
    **Content:** `{
        "description": "value",
        "name": "value"
    }`
    
* **Error Response:**

  * **Code:** 404 NOT FOUND
 
* **Sample Call:**

  `requests.get('http://0.0.0.0:5000/product/d65ca39d-1818-45b8-98b4-4dc60f2701a0/')`


<br>


#### Delete a product
  Delete a product

* **URL**

  `/product/<str:product_id>/`

* **Method:**

  `DELETE`

* **Headers:**

  `Bearer: [your token]`
  
* **Success Response:**

  * **Code:** 200
 
* **Sample Call:**

  `requests.delete('http://0.0.0.0:5000/product/d65ca39d-1818-45b8-98b4-4dc60f2701a0/')`

<br>


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what 
you would like to change.

Please make sure to update tests as well.

## License
[MIT](https://choosealicense.com/licenses/mit/)
# Hospital recommendation system

***

> - This is a project carried out as ***Minor Project*** under the curriculum.

> - The user can search for *hospitals* within their preferred *search radius*

> - The user can view their and the hospitals around them location in the *map*. The application uses python *Folium* library for rendering maps.

> - The user can either *search-by-category* of the diseases or can *search-by-symptom* to find hospitals. The application uses *OpenAI API's davinci auto-complete model* to find related category according to *symptoms*.

> - The user can view the *route* to hospitals from current location or the entered location. The application uses *Open Route Service* to get the route and python *geocoder* library to convert entered location into latitude and longitude.

> - The user can also add their *Schedule* to visit the hospital.

> - The user can add a hospital to **Preference list** after which the hospital will be listed on top if it satisfies the user's search criteria

***
To run the application run the following commands (*Make sure you have python and pip installed*)

> - Browse to the directory where you want to store the application and run the following commmand in the command line
  ```git clone https://github.com/nabin25/hospital-recommendation-app-django.git```

> - cd inside the cloned folder and make a python virtual environment using the following command
  ```virtualenv <env_name>```

> - activate the virtual environment by running following code
    ```<env_name>/Scripts/activate```

> - Install the requirements using the given command
    ```pip install -r requirement.txt```

> - Run the following command to make migrations and apply those changes in database
    ```python manage.py makemigrations```
    ```python manage.py migrate```

> - To create a superuser use the command and enter the credentials
    ```python manage.py createsuperuser```

> - Then run the server using the following code. The server should be live on 'http://localhost:8000'
      ```python manage.py runserver```

***

*Make sure to add your OpenAI and Open Route Service API key for the full functioning of the project*

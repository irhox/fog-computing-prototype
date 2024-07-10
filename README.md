# Fog Computing Prototype

This project was created as part of a master course at the TU Berlin university.
Its purpose is to showcase an application that overcomes fog specific challenges.

More detailed information is found in the [DOCUMENTATION.md](./DOCUMENTATION.md) file.

## Getting Started

1. Install all the dependencies using the requirements.txt file that is placed on the root folder of the project.
2. Run **Power Sensor** using the `python power_sensor/mqtt_simulator/main.py`.
3. Run **Fuel Sensor** using the `python fuel_sensor/mqtt_simulator/main.py`.

### Local Component:

In order to work with the local component you need a working PostgreSQL database instance. That is where the sensor
information as well as the aggregated data are stored. You can use for example the Postgres container from
the `local_component/compose.yml` with `docker compose up -d`

1. Create a .env file that contains the database information variables as shown in the .env-example file.
2. Run the file db_configuration.py by using `python local_component/db_configuration.py`. That will create the needed
   tables in the database.
3. Start the local component by using `python local_component/main.py`.

Example log lines from Local Component:

```plaintext
TOPIC:  power  PAYLOAD:  {"power_in_volts": 10728.59}
Power data is successfully created.
Deleted data with id:  027fc149-2423-4547-bd69-054fa67071e9  after success message from cloud component
Deleted data with id:  d68d1479-acad-4d98-80d9-38cad2299b44  after success message from cloud component
Deleted data with id:  fc0690aa-f8c0-43ff-b142-44ef725ab3c9  after success message from cloud component
Deleted data with id:  3d12ea2c-a838-4c56-b094-bf6e567175d1  after success message from cloud component
Deleted data with id:  88d908a3-0f1b-490e-8b84-e0aa8af27c5d  after success message from cloud component
Deleted data with id:  57e48fc2-595f-4cb5-9cd3-22cfac76347f  after success message from cloud component
TOPIC:  fuel  PAYLOAD:  {"fuel_level": 83.54226649105428}
Fuel Data is successfully created.
TOPIC:  power  PAYLOAD:  {"power_in_volts": 11535.48}
Power data is successfully created.
```

### Cloud Component:

#### In order to work with the cloud component locally:

1. Run the cloud component by using `python cloud_component/main.py` command. It will start the application and generate
   an SQLite database. That is where the final sensor data is stored.

#### In order to work with the cloud component on the GCP:

1. Create a new Google Cloud project;
2. Activate Compute Engine API;
3. Change the value of the `gcp_project_id` variable
   in  [fog-computing-prototype/terraform/terraform.tfvars](./terraform/terraform.tfvars)
   to the id of your GCP project;
4. Inside of
   the [fog-computing-prototype/terraform/](./terraform/)
   folder execute the following commands:
    - `gcloud auth login`
    - `terraform init`
    - `terraform plan`
    - `terraform apply`
1. To establish an SSH connection to a virtual machine instance on GCP
   run: `gcloud compute ssh cloud-component-vm --zone=europe-west3-a --project=<YOUR_GCP_PROJECT_ID>`
2. Ensure that the container is up and running: `sudo docker ps`
3. Copy the name of the container and run the following command to see the logs: `sudo docker logs <CONTAINER_NAME>`

Now you can explore the logs in the terminal and see for yourself how the data is stored in the local component and then
deleted from the local component after getting confirmation from the cloud component that the data is stored there.

```other
INFO:mqtt_broker:Connected successfully
INFO:mqtt_broker:Received message from topic power-station/data
INFO:mqtt_broker:Message c81a53d4 is successfully saved in the database
INFO:mqtt_broker:Message f377e78e is successfully saved in the database
INFO:mqtt_broker:Message 0d0bdf3a is successfully saved in the database
INFO:mqtt_broker:Message 46dc5bc1 is successfully saved in the database
```
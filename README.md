# Toolbox

This application helps instructors transform their courses/lectures so that these can be taught in online environments.

### Install packages and save Categories/Building Blocks and online ideas to the Database
1. To install the packages needed for the application to run, please refer to `requeriments.txt`
2. Create  `json5` representations of both the building blocks and teaching tools/ideas. 
3. Store these files (generated in step 2) in `data/categories` and `data/ideas` directory respectively.
4. Execute `python manage.py read_data --save_category` and `python manage.py read_data --save_idea` to store the information into the database.

## Architecture

### Apps

- **tbcore:** handles the core functionality of the website and contains the database models used throughout the project. 
- **plan:** here one can find the code that allows the users to create, update, read and delete course plans. 

### Database

These are the models implemented throughout the development of the project:
- Category: Every instance (data point) contains information about a single building block (e.g., category_name, short_description etc.)
- OnlineIdea: Every instance (data point) contains information about a single teaching tool (e.g., idea_name, implementation_steps etc. )
- Plan: used to store information about user's course plans. 
- PlanCategoryOnlineIdea: establishes ForeignKey relationships to the `Category`, `OnlineIdea` and `Plan` models. It also used to manage the user's notes.

See [here](./doc/database/database_diagram.png) a database diagram. 

### About the json5 files. 

The content of this website can be easily modified by making changes to the json5 files found in the `data` directory.
Take these into consideration when making changes:
- The content is written in Markdown.
- Execute `python manage.py read_data --save_category` or `python manage.py read_data --save_idea` to save changes to the database.

#### Static files (``json5``)

The supporting documents and images used throughout the ``json5`` files are stored in the `tbcore/static` directory:
- **support_documents:** this directory contains supporting documents (e.g.,``pdf`` files).
- **images:** this directory contains the images used in the ``json`` files.

#### How to update the Support documents or images:
1. Make changes to the files stored in the `support_documents` or `images` directory.
2. Update the `json` files with the new information.
   1. For example, to add the image `human_touch.png`, you can use the following code snippet (style it as desired): ``<img src=\"/static/tbcore/images/human_touch.png\" alt=\"Human Touch\" width=\"40%\" height=\"50%\" class=\"rounded mx-auto d-block\">"``
   2. To add a support document called `How_to_add_task_plugIn_to_Stud.Ip_course.pdf`, you can use the following code snippet (style it as desired): ``<a href="/static/tbcore/support_documents/How_to_add_task_plugIn_to_Stud.Ip_course.pdf" target="_blank">Tasks (reflection) Plug-In</a>``
   3. Execute `python manage.py read_data --save_category`; `python manage.py read_data --save_idea` and  `python manage.py populate_db` to save changes to the database.

# Docker

You can develop or deploy this application using Docker.

## Development

1. Create a `.env.dev` file from `env.dev-example`
   ```
   cp .env.dev-example .env.dev
   ```
2. Start the ToolBox
   ```
   docker compose -f docker-compose.yml up
   ```
3. To access the Toolbox visit ` http://localhost:8000/`
   


## Production

1. Create a `.env.prod` file from `env.prod-example`
   ```
   cp .env.dev-example .env.prod
   ```
2. Start the ToolBox
   ```
   docker compose -f docker-compose.prod.yml up
   ```
3. In the container toolbox_prod_container, make migrations and execute them. 
4. (In the container) Do not forget to run the commands explained above (section: How to update the Support documents or images)
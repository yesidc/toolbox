# Toolbox

This application helps instructors transform their courses/lectures so that these can be taught in online environments.

### Install packages and save Categories/Building Blocks and online ideas to the Database
1. To install the packages needed for the application to run, please refer to `requeriments.txt`
2. Create  `json5` representations of both the building blocks and teaching tools/ideas. 
3. Store these files (generated in step 2) in `data/categories` or `data/ideas` directory respectively.
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

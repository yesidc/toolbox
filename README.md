## Note: this tool is under development

# toolbox

### Install packages and save Categories/Building Blocks and online ideas to the Database
1. To install the packages needed for the application to run, please refer to `requeriments.txt`
2. Create a `json5` file with the information correspoding to a single Category or Online Idea
3. Store these files (generated in step 2) in `data/categories` or `data/ideas` directory repectevely.
4. Execute `python manage.py read_data --save_category` and `python manage.py read_data --save_idea` to store the information into the database.




## Note: this tool is under development

# toolbox
## Save Categories/Building Blocks and online ideas to the Database
1. Create a `json5` file with the information correspoding to a single Category or Online Idea
2. Store these files (generated in step 1) in `data/categories` or `data/ideas` directory repectevely.
3. Execute `python manage.py read_data --save_category` and `python manage.py read_data --save_idea` to store the information into the database.
3. Execute `python manage.py create_coi` to create the corresponding `CategoryOnlineIdea` objects. 



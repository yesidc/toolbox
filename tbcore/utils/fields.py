
# todo do not hard code this, user the __dict__ of the class

def idea_fields():
    return ["idea_name", "idea_id", "brief_description", "technology", "implementation_steps", "teacher_effort",
            "recommendations",
            "resources", "testimony", "use_cases", "references", "reusable", "task_complexity", "category"]


def category_fields():
    return ["category_name","category_id", "short_description", "titles_accordion", "content_accordion", "references", "category_url",
            "next_page"]
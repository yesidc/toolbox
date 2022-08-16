from django.db import migrations


def create_online_ideas(apps, schema_editor):
    OnlineIdea = apps.get_model('tbcore', 'OnlineIdea')

    student_intro = OnlineIdea.objects.create(
        idea_name='Short Student Introduction/ 2 Truths one lie',
        brief_description='Students write a short introduction/ description about themselves. The topic or focus is free for them to choose, so they can write something authentic about themselves with which they feel comfortable sharing. This way, course participants get a feel for who else is in the course and what they are interested in. The point is to make the course human, so students can write anything that shows they are not an AI This is a gamified approach! Students can write anything about their background or even come up with a funny story about themselves that mustn Alternatively, everyone shares 2 truths and one lie about themselves. ',
        examples_application='In all courses to get to know each other.',
        tool="""
        <ul>
<li>Forum: students can react to each other's posts via the comment function. </li>

<li>Courseware: create a page that everybody can edit or a page for every individual. Comments are possible but have to be opened manually.</li>   

<li>Element: everyone can respond to each other's posts and the mobile app supports quick reactions from students</li>
  </ul>
        """,

        implementation_steps="""
        <ol>
<li>Inform students about the introduction / two truths one lie.</li>   
<li>Set boundaries to keep it really short, e.g. a limit of 200 words.</li> 
<li>Encourage students to be creative and allow to post pictures, a small poster, a text, a comic, a song, basically any form that they are inspired to.</li>
<li>Inform students where and when they should submit their little description/ two truths and one lie.</li> 
<li>Students have to react to at least one other description by commenting, forming groups, finding two persons with the same interest, or figure out the lie.</li> 
</ol>
        """,
        teacher_effort="It's fun to read the student posts!",
        recommendations="""
        You might want to give some prompts for students which stimulates their creativity. 
<h5>Description topics could be:</h5>
<ul>

<li>academic interest</li>
<li>hobbies</li>
<li>a routine</li> 
<li>favourite course + why (also from their Bachelor)</li>
  </ul>
        """,
        reusable='Yes',
    )

    instructor_introduction_video = OnlineIdea.objects.create(
        idea_name='Instructor introduction video',
        brief_description="<p>"
                          "<strong>""A short video in which you introduce yourself as the instructor of the course to the students and welcome them to your course. </strong>""Most importantly, the video should be authentic, i.e. there is no fixed template or a 'must-do/ must talk about' for it, rather, you can show yourself in a way that you feel comfortable with."
                          "</p>",

        examples_application="In every course where you introduce yourself to the students ",
        tool='<ol>'
             '<li> <a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/opencast-studio/">Opencast Studio:</a>'
             'easily create/edit videos without installing software on your computer.</li>'
             '<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/courseware/">Courseware:</a>'
             'Once you have created the micro lecture videos, you can integrate them into Courseware (or Virtual Learning Enviroment).  To integrate videos into Courseware you can use the Opencast block. You can also take a look at these other video blocks. </li>',

        implementation_steps='<ol>'
                             '<li>Prepare some bullet points of'
                             '<ul>'
                             "<li>What you want to say about yourself (be authentic, you don't need to share something private, rather, something that allows students to get a good impression of who you are (see the recommendations for inspiration)</li>"
                             "<li>How you understand your role as the instructor of the course and </li>"
                             "<li>what your wish for the course is.</li>"
                             "</ul>"

                             '</li>'
                             '<li>Decide your recording mode: Opencast studio (at home) or Lehrkolleg professional recording studio (alte Münze) </li>'
                             '<li>Prepare set-up (software, room lightning, close windows) and equipment (microphone and camera) </li>'
                             '<li>Record / edit your video to max. 10 min. </li>'
                             '<li>Embedd your video in courseware via video blocks</li>'
                             '<li>Send a welcome message to all course participants with a link to your introduction video</li>'

                             '</ol>',

        teacher_effort="""
<ul>
  <li>Prepare coarsely what you want to say. </li>
  <li>Video recording + editing: 15-20 min. </li>
  <li>Upload the video in your courseware introduction section.</li>
</ul>
""",
        recommendations="""
  It doesn't need to be perfect and mispronunciations are ok, after all it's human! The introduction is meant to give students an impression about who their instructor is and not more. 

<ul>Some inpiration for your introduction:
<li>What was the question that initially led you to inquire more in this field? </li>
<li>What are your expectations for the course (e.g. participation, questions to address, interaction)</li> 
<li>What is your teaching style? </li>
<li>What are you looking forward to?</li>
<li>Be authentic and do something that you feel comfortable with.</li> 
<li>Tell students something that lets them know about your personality: a show you are watching, family photo, your hobby, your pets etc.</li>
<li>Insert a handwritten signature below your welcome message.</li>
</ul>
    """,
        supplementary_material="""
<a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/videostudio/">Video Studios</a>
""",

        reusable="Yes, for the same course",

    )

    instructor_introduction_video = OnlineIdea.objects.create(
        idea_name='Share stories and experiences with students',
        brief_description='Share professional and relevant personal anecdotes and be humorous if appropriate. Invite students to share their own experiences.'
                          'Students come to your class for the story. The content is already in the books.',
        examples_application='Someone who uses a self-written program to organize files on their brand new Mac',
        tool="""
    <ol>
<li>Microlectures: spice up your micro lectures with an annecdote.</li> 
<li>Courseware: you can use the explanatory texts and the design of the pages and sections to share stories or experiences which relate to the presented material. THis can give our whole courseware a new flavor, even if you do it only in a few instances.</li> 
<li>BBB: you can easily share stories during a discussion.</li> 
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/instant-messenger-element-vorher-riot/">Element:</a> You can open the discussion with your students by sharing a story, experience or anecdote and connect it to a question about a topic in the written discussion. You might want to consider a "tearoom" in Element (adapt the name to something that you like) where students and instructors can share professional or relevant personal anecdotes. Element is quick and provides a mobile app which is handy for spontaneous communication.</li>
<li>Forum: You can do the same as in element but the forum just has a different connotation and is not as fast but more sorted.</li>
</ol>
    """,
        implementation_steps="There's no one size fits all, so use your own best judgement of what and when you want to tell stories and share experiences with students to motivate them or to simply liven up the discussion.",
        teacher_effort='This is very individual.',
        recommendations="""
    <ul>

<li>Think about the session a day earlier: Is there a funny story or annecdote about this topic from a conference / from when you were a student/ an activity of students that you still remember, etc...?  When was the topic relevant in the news? </li>


<li>You can make your course more personal by showing your own style. 
You might have one thing about you that is odd in a random way, like wearing funny ties, giving topic-unrelated riddles in class just to keep up the student's attention, or even a mascott that sits in your BBB conferences, virtually or in the room that you are calling from. </li>

<li>Which lecturers do you like and why? Is there something that you can adapt from them? </li>

<li>Being eccentric is ok. drink from your favourite cup.</li>
  </ul>
    """,
        supplementary_material="""
    <a href="https://www.youtube.com/watch?v=TmWd4cfHQb0&list=PL9F536001A3C605FC&index=11">Patrick Winston about how to find your own style</a>
    """,
    )

    # Online Ideas Organization

    syllabus = OnlineIdea.objects.create(
        idea_name='Syllabus',
        brief_description="One document- all answers. The syllabus is a course manual, providing complete and exact course information about organizational aspects, prerequisites, requirements, course goals, learning resources, assignment instructions and expectation rubrics and a grading scale.",
        examples_application="For all courses (many universities require a syllabus for a course) ",
        tool="""
    <ul>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/courseware/">Courseware:</a> Virtual Learning Environment that helps you structure and organize the content and sections of your syllabus in a more appealing and easy-to-navigate way.</li>
<li>Courseware-syllabus template: This template gives you a general structure as well as a set of instructions and tips you can use to construct your syllabus. First <a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareExport">import</a> the syllabus template into your course courseware section and then activate the edit mode from the menu on the left. Now you can visualize and modify the different pages and blocks that make up this template. </li>
  </ul>
    """,
        implementation_steps="""
<h5>Provide complete and exact information about: </h5>
<ol>
<li> Course information: Meeting days, time and location, teaching mode, credits and prerequisites </li>
<li>Instructor contact information: "Very important note: I prefer Email and expect you to check your emails at Sogo.uos.de and NOT the messages in Stud.IP. Please make sure that your stud.IP messages are forwarded to your email address, so you don't miss our course announcements." </li> 
<li>Course description and schedule </li>
<li>Learning resources, technology and texts </li>
<li>Learning goals of your course </li>
<li>Assignment information, due dates, instructions and grading rubric/ assessment criteria </li>
<li>Grading scale </li>
  </ol>
    """,
        teacher_effort="""
    The syllabus ties all links of your course together. The more precise you list the prerequisites, learning goals, your teaching approach and the resources, the more clarity you and your students will have during the semester. <br> 
The most time consuming yet worthwhile parts of writing a syllabus are: 
<ul>
<li>clear learning goals (they help coming up with meaningful assignments) </li>
<li>clear assignment instructions and expectations </li>
<li>teaching mode / learning scenario (when will you meet in person, what should students prepare, how can students participate online, etc. </li>
  </ul>
    """,
        recommendations="""
    <a href="https://myshare.uni-osnabrueck.de/f/c72d79cb8a764b088391/">Use this template from Purdue OWL</a> to fill in your course information. Use the prompts and complete the necessary sections 
including assignment instructions that clearly outline your expectations of the students' output. 

<ul>
<li>Give complete and exact information by the start of the semester and always refer to the syllabus section/ PDF. </li>

<li>Provide a syllabus PDF and a courseware integration of the syllabus. </li>

<li>Consider adding some words about: 
  <ul>
<li>handling incompletes or late work (less for interaction)</li>  
<li>course logistics (less for interaction but organization) </li>
    </ul>
  </li>
  </ul>
    """,
        supplementary_material="""
    <ul>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/2022/03/18/ein-dokument-alle-antworten-oder-haben-sie-schon-im-syllabus-nachgeschaut/">Short overview about a syllabus</a> </li>

<li><a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareVideotutorials">Courseware crashcourse:</a> This tutorial will teach you the necessary skills to configure Courseware so that you can structure and display your course content using pages, sections, and blocks. </li>
  </ul>
    """,
        reusable="Yes, most parts of it and if you do the same course again, you only need to change the dates."
                 "Large parts of the syllabus can be reused in other courses, so the time investment is spread out. ",

    )

    weekly_emails_periodic_communication = OnlineIdea.objects.create(
        idea_name='Weekly emails/ periodic communication',
        brief_description="Sending/ posting announcements on a regular basis establishes structure in the everyday life of students and keeps them on their toes. Weekly emails are a great opportunity to establish a course rhythm, give reminders, to put certain topics in the spotlight or to provide additional resources, tips or links just in time and to show that the course is organized by someone."
                          "Further, showing that you are available to get in touch with students and are following the course. Timely response, availability and presence help students to build a connection to instructors.",
        examples_application="""
    <ul>
<li>It's relevant for all courses but especially relevant for courses where there's less interaction. Weekly emails make it more personal. </li>
<li>For courses with a lot of deadlines to remind students. </li> 
  </ul>
    """,
        tool="""
    <a href="https://myshare.uni-osnabrueck.de/f/c72d79cb8a764b088391/">Use this template from Purdue OWL</a> to fill in your course information. Use the prompts and complete the necessary sections 
including assignment instructions that clearly outline your expectations of the students' output. 

<ol>
<li>Stud.IP email to all participants</li> 
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/kursverwaltung-mit-stud-ip/">Announcements:</a> Intended for current news. Announcements appear prominently on the event summary pages, profile, and/or facility summary pages</li>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/instant-messenger-element-vorher-riot/">Element:</a> Element is a tool comparable to Slack or Discord that implements conversation threading and can easily be used for the day-to-day organization of events, replacing the need to send emails. For example, you can create a separate room dedicated to general/organizational matters where you constantly make announcements about the course.</li>
  </ol>
    """,
        implementation_steps="""
    <h5>Inform students about </h5>
<ul>

<li>this week's focus </li>
<li>study tips (if applicable) </li>
<li>organizational information (e.g. how late submissions will be handled) </li>
  <li>special dates</li>
<li>how to reach you (e.g. Element Chat, Email, walk-in hours/ office hours)</li>
  </ul>
    """,
        teacher_effort="Regular session preparation + 15 minutes / week to write an email before the session",
        recommendations="""
    Let students know how they can reach you best (e.g. via Element, a Chat application hosted by VirtUOS) and if you will be unavailable for certain times 
<ul>
<li>if you use element: make your announcements stand out visually, e.g. by giving them a title in bold face "Announcement" /"weekly update" so your message doesn't get lost and remember to use the @room mention (to notify everyone in the room) </li>
<li>Element: you can create a separate room for announcements only and give students reading rights only (but that means, they can't refer to your post to ask for clarification) 
Put this on the syllabus: "Very important note: I prefer Email and expect you to check your emails at <a href="https://sogo.uni-osnabrueck.de/SOGo/">Sogo.uos.de</a> and NOT the messages in Stud.IP! Please make sure that your stud.IP messages are forwarded to your email address, so you don't miss our course announcements." </li>
<li>important: set an alert in your calendar</li>
</ul>
    """,

        reusable="Not the texts but the structure. If you develop a habit, it's gonna be super quick. ",

        references="Martin, Ritzhaupt et al. 2019 – Award-winning faculty online teaching practices",
    )

    clear_assignment_expectations = OnlineIdea.objects.create(
        idea_name='Clear assignment expectations',
        brief_description="Clear expectations set the tone for communication and interaction between you and the students. The more specific your expectations are, the better students can show that they have mastered the topic or reached learning goal. It's like on google maps: Once you know the destination, you can search for a route to get there.",
        examples_application='to be completed',
        tool="""
    <ul>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/courseware/">Courseware:</a> create a courseware page and use any of the available <a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareBloecke">blocks</a> to deliver the assignment expectations. </li>
<li><a href="https://academiccloud.de/services">Cloud:</a> The ONLYOFFICE Document application provided by Academic Cloud is a tool similar to google docs that can be used as a word processor to formulate and share your assignment expectations with your students. </li>
<li><a href="https://academiccloud.de/services">Clould:</a> The ONLYOFFICE Spreadsheet application provided by Academic Cloud is a tool similar to Google Sheets that can be used to create a rubric with assignment criteria. </li>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/etherpad/">Etherpad: </a>Formulate and share the assignment expectations with your students. In the menu on the left, you can publish your document and then pass on the displayed URL so it can also be used outside Stud.IP. Additionally, you can activate the 'read-only' option to prevent people from editing the document. </li>
  </ul>
    """,
        implementation_steps="""
    <h5>Write down for this course: </h5>
<ol>

<li>How do you envision the interaction with your students? What will you do to realize that vision? </li>
<li>For this course, what do you accept as evidence for understanding the material? What do you not accept? (assessment rubric)</li>
<li>What should the students do in order to demonstrate that they have mastered the learning and reached the course goals? (Assignment instructions) </li>

<li>Communicate your expectations to your students. </li>
  </ol>
    """,
        teacher_effort="The effort depends on how much clarity you have about the learning goals and about what you would accept as evidence of the students' understanding.  Since there are plenty of ways to demonstrate mastery of a topic, it is rather a matter of being conscious and clear about the boundaries, i. e. what you accept as a demonstration of mastery and what not and why. (assessment rubric)"

                       "The more specific your assignments instructions (i.e. what students should do, which steps to perform/ consider, what the result should entail and what not), the more effort it is for you before the semester. However and most likely, this effort saves you time and headache during and by the end of the term, because clear expectations can prevent organizational back and forth or grading discussions. ",
        recommendations="""
    Your expectations should clearly align with your learning goals. Sometimes, it's useful to take a step back and think of the enduring understandings in your course: What should students take home from your course after forgetting most of the details? 
<h5>What students can expect from you: </h5>
<ul>
<li>Let students know how you will support them in reaching these goals but also what they have to do, to pass the course (i.e. NOT just "hand in three assignments" but rather show by.... that you can apply this algorithm) </li>

<li>Create checklists for students for assignments and units. </li>

<li>Create an assessment rubric for yourself with a continuum between "expected" and "not sufficient" like in this <a href="https://myshare.uni-osnabrueck.de/f/49ad36cdc8d84e20bb27/">example</a>. Sharing the rubric with your students may help students reflect and assess their own output. </li>
  </ul>
    """,

    )

    # Assignments

    reflection_portfolio = OnlineIdea.objects.create(
        idea_name="Reflection portfolio",
        brief_description="The reflection portfolio is a tool for students to keep track of their learning process in a reflected manner. It helps to acquire more self-knowledge and consciousness about their learning progress, the standards to meet, and awareness for their own dispositions and habits when approaching tasks.",
        examples_application="""
 <ul>
<li><a href="https://myshare.uni-osnabrueck.de/f/34cb8878311c4f09aca9/">Individual reflection portfolio example instructions</a></li>

<li><a href="https://myshare.uni-osnabrueck.de/f/8b3ba4792076428399c9/">Alternative reflection idea</a></li> 
  
  </ul>
    """,
        tool="""
       <ul>
  <li><a href="https://hilfe.studip.de/help/5.0/de/Basis/Dateien">Files Stud.Ip:</a> Reflection portfolio files can be up- and downloaded by students and lecturers.</li>

<li><a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareSeite">Courseware:</a> Create a page for each student in the courseware of your course in which they write their portfolio. Ideally, you create a reflection portfolio template with writing prompts in you workspace in stud.IP and copy it as many times as the number of students into your courseware. Now, you can give editing and reading rights to individual students or groups for pages within courseware and you can make pages invisible for certain participants.</li>
  </ul>
    """,
        implementation_steps='to be completed',
        teacher_effort="Reading the Reflection portfolios (pass/ fail) Depends on the time frame that the portfolio represents",
        recommendations="""
    <h5>We recommend using reflection portfolios as:</h5>
<ul>

<li>the tip on the scale for grading</li>
  <li>means for individual assessment</li>
<li>encouraging student reflection</li>
<li>set a word limit of about 750 words</li>
  
  </ul>
    """,
        supplementary_material="""
    
<a href="https://myshare.uni-osnabrueck.de/f/0186fb38cf8244e4b631/">The list with Ideas for individual assessment contains many writing prompt examples</a>
  <a href=""></a>

    """,
    )

    peer_review = OnlineIdea.objects.create(
        idea_name="Peer Review",
        brief_description="Students review each others' assignments based on given criteria and give feedback, which is then integrated or rejected with sound reasoning. Peer review helps to create awareness for assessment criteria and to think with the eyes of an external. Practising meta-cognition skills help to detect issues quickly and to plan task implementation.",
        examples_application="""
        <a href="https://myshare.uni-osnabrueck.de/f/c49dc6e081de4a108cac/">Feedback for video assignments example procedure + feedback instructions</a>
        """,
        tool="""
        For project reports; Word/PDF comment functionality offers a wide variety of tools students can use to review and give feedback to their fellow students.
<ul>
<li><a href="https://academiccloud.de/services">ShareLaTeX (Overleaf):</a> Service provided by Academic Cloud. Activate the review function to give feedback.</li> 
<li><a href="https://academiccloud.de/services">Cloud: </a>ONLYOFFICE service provided by Academic Cloud. Create documents, share them, collaborate and, give feedback in the comments (works like google docs)</li>
<li>Forum for peer feedback: Students upload their submissions in the forum and others can give feedback in the comment function.</li>
<li><a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareSeite">Courseware:</a> create an extra page with editing rights for reviewers or give feedback via the comment function in courseware. Further, a discussion block is currently being built for courseware.
Code (Git irgendwas)</li> 
  
</ul>
        """,
        implementation_steps='to be completed',
        teacher_effort="Additional effort for reading the feedback but chances are that final submissions improve.",
        recommendations="""
        <ul>
<li>Clearly detail they procedure for peer feedback since it is easy to get confused about which group provides feedback for whom or deadlines.</li>
  <li>Share clear expectations and assignment instructions to which the students can refer in their feedback.</li>
<li>Providing protocols for peer-review that is focused on specific criteria helps students to see how they can support each other.</li>
  </ul>
        """,
        supplementary_material="""
        <ul>
<li><a href="https://myshare.uni-osnabrueck.de/f/c42885e290c7436daa00/">Rubric Feedback practice</a></li>
  <li><a href="https://myshare.uni-osnabrueck.de/f/ccdf9a55f85f4128a2b6/">Checklist: criteria for quality feedback</a></li>
  </ul>
        """,
        reusable='Yes',

    )
    problem_statement = OnlineIdea.objects.create(
        idea_name='Problem Statement',
        brief_description="A problem statement is the first part of a research proposal and introduces which problem you would like to investigate, why the problem is important and what kind of solution or idea you offer to this problem. This includes the rationale for the focus of this study, along with good reasons why the problem is important, such as gaps in the current literature, problems that need to be solved, or tools we need to develop due to societal changes.",
        examples_application='to be completed',
        tool="""
        <ul>
<li>word processor and common research tools like google scholar, science direct</li>
<li><a href="https://digitale-lehre.virtuos.uni-osnabrueck.de/eintrag/etherpad/">Etherpad:</a> Etherpad is a simple collaborative online writing environment. Its primary focus is the text itself instead of complex format templates; this enables fast and smooth joint writing, making it an ideal tool for writing short texts such as problem statements.  </li>
<li><a href="https://academiccloud.de/services">Cloud: </a>ONLYOFFICE provided by Academic Cloud is a tool similar to google docs that students can use as a word processor to formulate their problem statements. </li>
<li><a href="https://hilfe.studip.de/help/5.0/de/Basis/CoursewareSeite">Courseware:</a> Create a page for each student in the courseware of your course in which they write their problem statement. Ideally, you create a problem-statement template with writing prompts in you workspace in stud.IP and copy it as many times as the number of students into your courseware. Now, you can give editing and reading rights to individual students or groups for pages within courseware and you can make pages invisible for certain participants. </li>
  </ul>
        """,

        teacher_effort="Read the students' problem statements (or use the peer review for a first check) and give feedback, e.g. by sending them an annotated version.",
        recommendations='to be completed',
        supplementary_material='to be completed',
        reusable='to be completed',
        testimony='to be completed',
        references='to be completed',

    )


#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )
#    peer_review = OnlineIdea.objects.create(
#        idea_name=,
#        brief_description=,
#        examples_application=,
#        tool=,
#        implementation_steps=,
#        teacher_effort=,
#        recommendations=,
#        supplementary_material=,
#        reusable=,
#        testimony=,
#        references=,
#
# )


def undo_online_ideas(apps, schema_editor):
    OnlineIdea = apps.get_model('tbcore', 'OnlineIdea')
    OnlineIdea.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tbcore', '0002_category'),
    ]
    operations = [
        migrations.RunPython(create_online_ideas, undo_online_ideas)
    ]

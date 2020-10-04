# Resume Recommender System
## Data Science Project - 4th year of Computer Science Engineering
## Higher Private School of Engineering and Technology - Ecole Supérieure Privée d'Ingénierie et de Technologie
# I-Project Introduction
## 1-General Introduction
Talent acquisition is one of the most crucial steps for a company’s future, every
stakeholder is trying to do it the right way, making sure that the best and most
fitting profiles pass the process.
Reducing the costs of this process is as equally important too, the ultimate goal in
human resource management is acquiring the top employees without spending
too much.
And this is where machine learning is emerging in 3 main pillars of human
resources:
• Talent recruitment: companies are training machine learning
algorithms to help employers automate repetitive aspects of the
recruitment process such as resume and application review
• Talent Sourcing: Companies are using machine learning to help
identify top candidates from large candidate pools.
• Candidate Screening and Engagement: Companies are developing AI
assistants to pre-screen candidates and to respond to inquiries
regarding positions using natural language processing.

## 2-Project context
As part of our data science project, our school cooperated with Wevioo, a giant in
the consulting, digital, and IOT sectors, who has given us access to 10.000 profiles,
allowing us to set up a solution for optimizing the recruitment process by selecting
the top profiles.
## 3-Wevioo description
Since its creation in 1998, the Wevioo Group has been supporting its customers in
their digital transformation projects by providing expertise and know-how in 3
areas: Consulting, Digital and IOT.
As a committed partner, Wevioo provides its customers with digital innovation
solutions perfectly adapted to their agility, performance and development
challenges.
With a culture of innovation at the heart of its DNA, Wevioo invests in R&D to
provide its customers and partners with innovative solutions and cutting-edge
expertise.
Wevioo has several hundred demanding projects carried out by its business and
technology experts in more than 30 countries in Europe, North America, Africa
and the Middle East. 

# II-Objectives
## 1-Business objectives
The given data contain details of applicant’s resumes (experience, skills,
education, etc.) and information about their previous and current jobs.
The tool that we are aiming to create should consolidate the CV search
system, filtering and the classification of profiles according to the criteria
requested (diplomas, skills, seniority, etc.) by the HR recruitment team.
An important functionality is the implementation of a system of
recommendation of the closest profiles to the ultimate profile that has
already been set and defined by the HR department of Wevioo.
2-Data Science objectives
• Collecting data: on behalf of the information provided from wevioo,
we need to scrape more details from LinkedIn profiled in order to
update the current data
• Data cleaning and feature engineering: the most important phase is
to create pertinent features from the source database that show the
most information about the individual in order to work with them on
machine learning algorithms
• Analysing profiles
• Developing a Scoring system of profiles: our application will return
the k best candidates for designated position according to our Scoring
system developed using machine learning tools and the closest
profiles to a chosen candidate.

## 3-Methodology
To ensure the realization of our project we opted for the IBM Master Plan
methodology which starts from the business understanding phase until the
deployment and feedback phases going through different other steps as the
following diagram explains:

# III-Data preparation
## 1- Internal Data preparation
### a - Data source identification and description
WEVIOO provided us with a BSON file that contains a list of 10000 Resumes
collected from information scraped from LinkedIn profiles of candidates and from
PDF files.

Below the list of features found on the database and their description:
- Search: search tags Wevioo has used to find the candidate’s profile
- URL: LinkedIn URL of the candidate’s profile
- Personal Information:
o Name: Name of the candidate
o Headline: Current post name
o Company: Current company name
o School: the name of the last school the candidate went to
o Location: the actual address of the candidate
o Summary: a brief description of the candidate’s experience
o Image: the image of the profile
o Email: email address
o Phone: phone number
o Connected: status of the profile
o Website: website of the candidate
- Skills:
o Name: label of the skill
o Endorsements: number of recommendations the candidate earned
from professionals or colleges
- Scraped Time: the date Wevioo collected the information from the profile
- Experiences:
o Jobs:
 Title: Title of the job
 Company: Name of the company
 Date Range: the period during which the candidate has worked
in the company
 Location: the address of the company
 Description: Description of the job and the work accomplished
 LinkedIn Company URL: LinkedIn URL of the company’s profile
o Education:
 Degree: Type of the degree
 Grades:

 Field of Study:
 Date Range: the period during which the candidate has
attended the school
 Activities: list of activities the candidate’s participated in
o Volunteering: description of volunteering work or clubs the candidate
is/was part of.
- Interests: list of fields the candidate’s interested in
- Accomplishments:
o Publications: list of posts the candidates has posted on LinkedIn
o Certifications: list of certifications the candidate has earned
o Patents:
o Courses: list of online courses the candidate has participated in
o Projects: list of personal projects and their description
o Honors: honors and awards the candidate has earned during his
career
o Test Scores: Scores of international tests
o Languages: list of languages mastered by the candidate
o Organizations: list of organizations the candidate is/was part of
### B - ETL
For an easier handling, we decided to store the bson file in a MongoDB
database and connect to the database with python for data manipulation.
The first step was then to import the data to MongoDB:

### C - Data Manipulation:
First, we looked at columns that looks important for the RH like skills and
experiences.
- Skills:
After a deep look at skills we found that a lot of skills are wrongly written and also
some of the candidates doesn’t match any of the required profiles.
In that case we decided to create a dictionary that puts the wrong skill spelling to
its correct form.
So, we extracted a large number of possible spelling found in the raw data that
describes the skill we are looking for with a degree of resemblance and take only
the correct ones. 

We also performed a semantic search accuracy by understanding the purpose of
the search and the contextual meaning.

For each skill, we decided to replace the endorsement from LinkedIn by another
score calculated (/3) by:
+1: Mentioning the skill
 +1: Using the skill in one or more projects
+1: Using the skill in one or more professional experience
Finally, for each skill we calculated the duration that the candidate spent working
on a professional level with it, making each skill acquired by a candidate
measurable by two important factors: the experience time and the level of
proficiency.

- Accomplishments + new features:
In the accomplishments we selected and calculated the number of certificates,
languages, organizations, honours and projects.
The tenure: How long does the employee usually stay at a job. That is Generated
using a formula that takes into consideration the weight of the experience.
After that we calculate the duration of all the experiences of a person and finally
the tenure of a candidate in a job which is a probability (~ indicator) of staying X
number of years in a job.

## 2- External Data preparation
### a - Data collection: web scraping
We used a combination of Selenium, chrome driver, a long with python to scrape
updated information about the 10,000 profiles.

### b - Data transformation (reformation)
After scraping the data about our profiles, we had to apply major transformation
to the format that was initially very different to our data frame, a transformation
that is mandatory for the next phase which is comparing the scraped data and the
one we have to see if there has been any updated on the candidate’s profiles
recently.
### c - Data Integration:
After we transformed the scraped data into the same format as our data set, we
started comparing each candidate’s information and updating the attributes and
features that had changes.

# IV-Modelling
In the context of finding the best “K” candidates, we decided to suppose the
existence of a perfect profile that acquires the highest values in every feature, and
finding the best candidates would come down to simply finding the closest ones to
that perfect profile.
As a metric for the distance between profiles, we picked the Euclidean distance
since we’re dealing with discrete data so the closest profile would eventually have
the lowest distance to the perfect candidate.

First, we need to extract the needed skills for Backend only as choosing the top 5
candidates should only imply the relevant skills for that profile needed.
Once we have our profile extracted, our model can pick the top 5 profiles for

# V-Deployment
For the deployment phase we wanted an easy-to-use and simple platform that
highlights the features of our model.
For this matter we used Flask: a micro web framework written in Python.

# VI-Conclusion
Slowly but surely, AI is finding its way into every part of the recruitment process,
from sourcing through pre-selection and interviewing to reference and
background checks and determining fair compensation.
With this project we hope to optimize this process for Wevioo, making it faster,
cheaper, and more efficient




---
[Flask Dashboard Atlantis Dark](https://appseed.us/admin-dashboards/flask-dashboard-atlantis-dark) provided by **AppSeed**

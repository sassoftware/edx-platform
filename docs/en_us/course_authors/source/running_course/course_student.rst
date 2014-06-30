.. _Student Data:

############################
Student Data
############################

You can access data about the students who are enrolled in your course at any
time after you create the course.

For information about the data you can access, see the following topics:

* :ref:`PII`

* :ref:`Access_student_data`

* :ref:`Access_anonymized`

You can also view charts of certain student demographics for graded problems.
See :ref:`Grades`.

.. _PII:

***************************************************************
Guidance for working with personal information
***************************************************************

The information that edX collects from site registrants includes personal
information that can be used to identify, contact, and locate individuals. This
information is available to course authors for the students who are enrolled in
their courses.

Course staff should follow the policies established by their organizations
and comply with the legal requirements of their locales to prevent public
distribution or misuse of this information.

.. **Question**: I just made this statement up. What guidance can/should we give, for immediate publication and in the future? (sent to Tena and Jennifer Adams 31 Jan 14)

.. _Access_student_data:

****************************
Access student data
****************************

You can download data about the students who are currently enrolled in your
course in a CSV (comma-separated values) file. For courses that have fewer than
200 students enrolled, you can also view data for enrolled students on the
Instructor Dashboard.

======================
Student-reported data
======================

When students register with edX, they select a public username and supply
information about themselves. Most of this information is optional, so not all
of the students who are enrolled in your course provide it.

 .. image:: ../Images/Registration_page.png
   :alt: Fields that collect student information during registration

Students then register for as many individual courses as they choose, which
enrolls them in each selected course.

You can access this self-reported information for all of the students who are
enrolled in your course:

* email
* username
* name
* level_of_education
* gender
* year_of_birth
* mailing_address
* goals

The student data that is available to course staff always reflects the set of
live, current enrollments. Students can register for your course throughout the
defined enrollment period, and they can unregister from a course at any time,
which unenrolls them. Students can also change their email addresses and full
names at any time. As a result, you may want to download student data
periodically to gain insights into how the student population changes over
time.

.. note:: In the future, edX may also request that students select a language and location. This data is not collected at this time.

.. _View and download student data:

==========================================
Download or view student data
==========================================

You can download student data to learn about population demographics at a
specific point in time, compare demographics at different points in time, and
plot trends in the population over time.

In addition to the data for enrolled students, data for the course staff is
included in the file or display.

.. important:: Do not navigate away from this page while you wait for the data to be prepared. The larger the enrollment for your course, the longer it takes to create and output the data. 

For smaller courses, you also have the option to view student data on the
Instructor Dashboard.

To download or view student data:

#. View the live version of your course.

#. Click **Instructor**, then click **Data Download**.

#. To download data about enrolled students in a CSV file, click **Download profile information as a CSV**.

   You are prompted to open or save the enrolled_profiles.csv file. All
   student-supplied data is included without truncation.

#. To display data about enrolled students, click **List enrolled students'
   profile information**. (This option is available only for courses with an
   enrollment of less than 200.)

   A table of the student data displays, with one row for each enrolled
   student. Longer values, such as student goals, are truncated.

 .. image:: ../Images/StudentData_Table.png
  :alt: Table with columns for the collected data points and rows for each student on the Instructor Dashboard

.. note:: The columns for language and location are included in this report for backward compatibility only. This data is no longer collected during student registration.

==========================================
View demographic distributions
==========================================

You can view a course-wide summary of certain demographic distributions for
your currently enrolled students. The total count for each value reported for
gender and educational attainment displays on the Instructor Dashboard. Because
this data is optional, the totals for each of these self-reported values are
likely to be lower than your course enrollment total. You can also view a chart
with the ages of all currently enrolled students.

To display demographic data for your students:

#. View the live version of your course.

#. Click **Instructor**, then click **Analytics**. 

   * The Year of Birth section displays a chart of enrolled students plotted by
     year of birth.

   * The Gender Distribution and Level of Education sections show tables with
     counts of responses made by enrolled students.

   .. image:: ../Images/Distribution_Education.png
    :alt: Table with columns for different possible values for level of education completed and total count reported for each value

   .. image:: ../Images/Distribution_Gender.png
    :alt: Table with columns for different possible values for gender and total count reported for each value

   "No Data" is the sum of the students for whom no value exists for the
   demographic.

  Data for individual students is not shown, and you cannot download data
  directly from this page. See :ref:`View and download student data`.

.. _Access_anonymized:

********************************
Access anonymized student IDs
********************************

Some of the tools that are available for use with the edX platform, including
external graders and surveys, work with anonymized student data. If it becomes
necessary for you to deanonymize previously anonymized data, you can download a
CSV file to use for that purpose.

To download a file of assigned user IDs and anonymized user IDs:

#. View the live version of your course.

#. Click **Instructor**, then click **Data Download**.

#. Click **Get Student Anonymized IDs CSV**.

You are prompted to open or save the {course-id}-anon-id.csv file for your
course. This file contains the user ID that is assigned to each student at
registration and its corresponding edX-wide anonymized user ID and course
specific anonymized user ID. Values are included for every student who ever
enrolled for your course.

To research and deanonymize student data, you can use this file together with
the enrolled_profile.csv file of student data or the
{course_id}_grade_report_{date}.csv file of grades.




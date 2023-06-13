**App live link -**[http://manant.pythonanywhere.com/](http://manant.pythonanywhere.com/) **
**


**The PDF Management & Collaboration System** is a web application designed
to facilitate the seamless management and collaboration of pdfs. The system
enables users to sign up, upload PDFs, share them with other users, and
collaborate through comments. This PRD outlines the features, functionality, and
specifications of the application.

1: User Signup and Authentication:
a. Users can create an account by providing essential information such as name,
email address, and password etc. Users can also their passwords.
b. Authentication mechanisms implemented to ensure secure access to
the application.

2: File Upload:
a. Authenticated users can upload a PDF file to the system.
b. The PDF files  securely stored and accessible only to authorized users.
c. The application validate the uploaded files to ensure they are in PDF
format.

3:Dashboard:
a. Users  able to search for acccessible PDF files based on file names i.e file uploaded by them and invited files.
b. Clicking on it will take them to a specific pdf file and see all the comments which are commented by invitees.

4: File Sharing:
a. Users should have the ability to share PDF files with others with a unique secure link which is sent to email ID of invitees.
b. Invited users may not have authenticated accounts to access shared PDF files.

5:Invited User File Access and Commenting:
a. Invited users  able to access shared pdf files through their invite link.
b. The app provide a user-friendly interface to view the PDF files.
c. Invited users can add comments related to the PDF file on a sidebar and can view existing comments.

6: **Authors can able to change/ or reply to the existing comments by viewer and viewers can be able to see that reply on the link which is shared to them ,it is like chat based feedback**

procedure:

1: make virtual environment and activate

2: clone the repository.

3: pip install -r requirement.txt

4: python manage.py runserver

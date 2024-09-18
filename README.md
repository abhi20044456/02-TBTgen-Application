# TBTgen Application

### Download link-: https://drive.google.com/drive/folders/1xn7fEr0z7L6BpPGjaWJWExXUqMzTozka


1. Objective:
   - Develop a Python application to generate a PDF file that compiles team images and TBT images, with custom headers including team details and data.

2. Key Features:
   - **Image Management:**
     - Automatically arranges and inserts team and TBT images into the PDF.
     - Ensures images are correctly ordered and formatted.

   - Custom Headers:
     - Adds a header to the PDF with dynamic team information and relevant data.
     - Header includes details such as team name, date, and specific topics.

   - File Naming and Saving:
     - Saves the generated PDF with a filename that incorporates the team name and date.
     - Streamlines document management and retrieval.

3. Libraries Used:
   - Pillow (PIL):
     - Used for image processing, including opening, manipulating, and saving images.
   - ReportLab:
     - Utilized for PDF generation and formatting.
     - Handles the insertion of images, text, and custom headers into the PDF.
   - os:
     - Manages file paths and directory operations.
   - datetime:
     - Handles date and time functions for generating dynamic headers and filenames.

4. How It Works:
   - Image Selection:
     - User selects team images and TBT images through the application’s GUI.
     - Application organizes the selected images according to specified rules (e.g., TBT images at the top).

   - PDF Generation:
     - The application uses ReportLab to create a new PDF document.
     - Inserts the team and TBT images into the PDF in the correct order.
     - Adds a custom header with dynamic team details and data.

   - Saving the PDF:
     - The application generates a filename based on the team name and date.
     - Saves the completed PDF to the specified location with the generated filename.

5. User Interface:
   - Provides a graphical interface for selecting images and specifying options (e.g., team, date).
   - Includes progress indicators to show the status of PDF generation.

6. Efficiency and Benefits:
   - Automates the creation of team documentation, reducing manual effort and errors.
   - Ensures consistency and professionalism in the final PDF output.


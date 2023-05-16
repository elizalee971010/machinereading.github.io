# machinereading.github.io
NYC DDC faced challenges extracting information from NYS DEC forms due to handwritten and printed content requiring manual input. To address this problem, this capstone project was initiated to develop a product using optical handwriting recognition techniques, enabling streamlined analysis and digitization of form information. This solution aims to improve efficiency, reduce errors, and enhance productivity when working with forms and archaic documents, empowering users to extract and analyze data quickly.

Our team developed this machine reading website using Google Cloud Platform + Google Vision API as a primary handwriting and text recognition function. The uploaded pdf has to be preprocessed to let the vision API better identify the part of the designated area; the preprocessing methods include Image positioning and cutting, using regular String expression and matching to extract text, and finally transferring the Json format file to CSV file for downloading purpose.

The Users can upload their scanned PDF forms, and then the website generates a CSV file that will only cover all the essential details in these specific NYS DEC forms. Users should click the ‘try it’ button and upload their NYS DEC forms, and then a downloaded CSV file will be automatically generated.

Attention: this website is designed for NYC DEC form only, and can be upload one page pdf file only. make sure the original pdf are justified and has clear handwriting content

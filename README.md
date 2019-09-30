# Patient timeline representation to model EHR data.

# Authors
Parth Tandel, Priya Singh, Monica Mishra

# Summary
Though a vast majority of healthcare data is present in digital format due to the unstructured nature (dates, notes, lab results) of the dataset, typical machine learning model are restricted to only a few variables. The MIMIC-III dataset eradicates this problem by structuring data from various sources into a set of formulated tables namely ADMISSIONS (information about patient's visits), INPUTEVENTS (readings of health monitor machines), CHARTEVENTS (record of medicines taken by patients), etc. The dataset is rich in information yet due to the immense size of tables (~50 GB), it cannot be used directly in its raw form and hence there is a need to build a pipeline. This pipeline then can be used to build a timeline of a patient's visit for data analysis or model creation. Our efforts are heavily inclined towards creating a single source dataset that captures the entire history of a patient which advertently makes training an ML model straightforward.
 
To access the MIMIC-III data a special training is required and once the training is completed, an application is submitted for credentialed access.

# Proposed plan of research
The main task of the project is the creation of a data pipeline to represent a patient's history, after extensive research on restructuring the data, 
we understood that the Fast Healthcare Interoperability Resources (FHIR) format is a universally accepted structure. 
 standardize the data in FHIR format, we intend to explore Google’s Protocol buffer which is Google's language-neutral, 
 platform-neutral, extensible mechanism for serializing structured data. This enables a user to decide how the data should be structured and it can be accessed using special generated source code in a variety of languages. This allows ease of use to read and write the data from a variety of data streams.

![Figure 1: MIMIC-III critical care database](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fsdata.2016.35/MediaObjects/41597_2016_Article_BFsdata201635_Fig1_HTML.jpg?as=webp)
<center> Figure 1: MIMIC-III critical care database </center>

After the dataset is stored in FHIR format, we aim to create sequence vectors to capture the timeline of events 
using deep neural network techniques such as Long Short Term Memory (LSTM) and Convolutional Neural Network (CNN), and 
try to answer critical questions for instance:
* What are the chances of a patient to be readmitted? 
* How long would a patient stay for a known ailment? 
* Is it possible to predict the chance of survival? 

### Data description
The dataset used is MIMIC-III<sup>1</sup> (‘Medical Information Mart for Intensive Care’) which is an openly available dataset developed by the MIT Lab for Computational Physiology. 
MIMIC-III is a large, freely-available database comprising de-identified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.
The database includes information such as demographics, vital sign measurements made at the bedside (~1 data point per hour), laboratory test results, procedures, medications, caregiver notes, imaging reports, and mortality (including post-hospital discharge).

MIMIC-III is a relational database consisting of 26 tables. Tables are linked by identifiers which usually have the suffix ‘ID’. For example, SUBJECT_ID refers to a unique patient, HADM_ID refers to a unique admission to the hospital, and ICUSTAY_ID refers to a unique admission to an intensive care unit.
Charted events such as notes, laboratory tests, and fluid balance are stored in a series of ‘events’ tables. For example, the OUTPUTEVENTS table contains all measurements related to output for a given patient, while the LABEVENTS table contains laboratory test results for a patient.
Tables prefixed with ‘D_’ are dictionary tables and provide definitions for identifiers. For example, every row of CHARTEVENTS is associated with a single ITEMID which represents the concept measured, but it does not contain the actual name of the measurement. By joining CHARTEVENTS and D_ITEMS on ITEMID, it is possible to identify the concept represented by a given ITEMID.
Broadly speaking, five tables are used to define and track patient stays: ADMISSIONS; PATIENTS; ICUSTAYS; SERVICES; and TRANSFERS. Another five tables are dictionaries for cross-referencing codes against their respective definitions: D_CPT; D_ICD_DIAGNOSES; D_ICD_PROCEDURES; D_ITEMS; and D_LABITEMS. The remaining tables contain data associated with patient care, such as physiological measurements, caregiver observations, and billing information.

# Preliminary results
Performed basic exploratory data analysis on the admissions table to gather the summary statistics and analyzed the duration of stay.
<br />![Figure 2: Descriptive Statistics](https://github.com/priyasingh16/Fully-Automated-GCP-Healthcare-API/blob/master/Assets/descriptive_statistics.png)
<br /><center>Figure 2: Descriptive Statistics </center> <br />
![Figure 3: Histogram](https://github.com/priyasingh16/Fully-Automated-GCP-Healthcare-API/blob/master/Assets/histogram.png)
<br /><center>Figure 3: Distribution of length of stay in hospitals </center><br />
As the size of some of the tables is too big to be loaded in local machine's memory, instead of performing analysis on the entire dataset, we analyzed an individual record in all the tables. 
To understand the structure of the data and the relationship between the tables, the journey of a particular patient was analyzed. Using this we created a timeline of the patient's visit and health status over a long period of time.
The timeline consists of information about every admission, diagnosis, service such as ICU, transfers, and discharge of a given patient. 
This gives us an idea of what to capture in a sequence model for building patient's visit history.
![Figure 4: Patient Timeline](https://raw.githubusercontent.com/priyasingh16/Fully-Automated-GCP-Healthcare-API/master/Assets/Patient_timeline.png)
<center> Figure 4: Patient Timeline </center>

# References
1. Alpha.physionet.org. (2019). MIMIC-III Clinical Database v1.4. [online] Available at: https://alpha.physionet.org/content/mimiciii/1.4/ [Accessed 28 Sep. 2019].
2. Johnson, A., Pollard, T., Shen, L., Lehman, L., Feng, M., Ghassemi, M., Moody, B., Szolovits, P., Anthony Celi, L. and Mark, R. (2019). MIMIC-III, a freely accessible critical care database.
3. Rajkomar, A., Oren, E., Chen, K., Dai, A., Hajaj, N., Hardt, M., Liu, P., Liu, X., Marcus, J., Sun, M., Sundberg, P., Yee, H., Zhang, K., Zhang, Y., Flores, G., Duggan, G., Irvine, J., Le, Q., Litsch, K., Mossin, A., Tansuwan, J., Wang, D., Wexler, J., Wilson, J., Ludwig, D., Volchenboum, S., Chou, K., Pearson, M., Madabushi, S., Shah, N., Butte, A., Howell, M., Cui, C., Corrado, G. and Dean, J. (2018). Scalable and accurate deep learning with electronic health records. npj Digital Medicine, 1(1).


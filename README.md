# Patient timeline representation to model EHR data.
Fully Automated GCP Healthcare API /Pipeline to model EHR Data using sequential modeling (with attention) for patient timeline representation of features(https://mimic.physionet.org/) [Plug and play based serverless GCP architecture for sequential model training and inference pipeline on EHR data]
 
# Authors
Parth Tandel, Priya Singh, Monica Mishra

# Summary
Though a vast majority of healthcare data is present in digital format but due to the unstructured nature (dates, notes, lab results) of the dataset, typical machine learning model are restricted to only a few variables. The MIMIC-III dataset eradicates this problem by structuring data from various sources into a set of formulated tables namely ADMISSIONS (information about patient's visits), INPUTEVENTS (readings of health monitor machines), CHARTEVENTS (record of medicines taken by patients), etc. The dataset is rich in information yet due to the immense size of tables (~50 GB), there is a need to build timeline of a patient's visit for future data analysis or model creation. Our efforts are heavily inclined towards creating a single source dataset that captures entire history of a patient which advertently makes training an ML model straightforward.


# Proposed plan of research
The main task of the project is the creation of a data pipeline to represent a patient's history, after extensive research on restructuring the data, we understood that the Fast Healthcare Interoperability Resources (FHIR) format is an universaly accepted form. To standardize the data in FHIR format, we intend to explore Google’s Protocol buffer which are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. 

![Figure 1: MIMIC-III critical care database](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fsdata.2016.35/MediaObjects/41597_2016_Article_BFsdata201635_Fig1_HTML.jpg?as=webp)



### Data description
The dataset used is MIMIC-III<sup>1</sup> (‘Medical Information Mart for Intensive Care’) which is a openly available 
dataset developed by the MIT Lab for Computational Physiology. 
MIMIC-III is a large, freely-available database comprising deidentified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.

The database includes information such as demographics, vital sign measurements made at the bedside (~1 data point per hour), laboratory test results, procedures, medications, caregiver notes, imaging reports, and mortality (including post-hospital discharge).

The information of patients is deidentified and comprehensive healthcare information is collected from adult patients admitted to critical care units between 2001 and 2012 at large tertiary care hospitals. 
It includes admissions, demographics, chart notes, fluid balances, vital signs, billing information, laboratory tests, medications, etc.

MIMIC-III is a relational database consisting of 26 tables. Tables are linked by identifiers which usually have the suffix ‘ID’. For example, SUBJECT_ID refers to a unique patient, HADM_ID refers to a unique admission to the hospital, and ICUSTAY_ID refers to a unique admission to an intensive care unit.

Charted events such as notes, laboratory tests, and fluid balance are stored in a series of ‘events’ tables. For example the OUTPUTEVENTS table contains all measurements related to output for a given patient, while the LABEVENTS table contains laboratory test results for a patient.

Tables prefixed with ‘D_’ are dictionary tables and provide definitions for identifiers. For example, every row of CHARTEVENTS is associated with a single ITEMID which represents the concept measured, but it does not contain the actual name of the measurement. By joining CHARTEVENTS and D_ITEMS on ITEMID, it is possible to identify the concept represented by a given ITEMID.

Broadly speaking, five tables are used to define and track patient stays: ADMISSIONS; PATIENTS; ICUSTAYS; SERVICES; and TRANSFERS. Another five tables are dictionaries for cross-referencing codes against their respective definitions: D_CPT; D_ICD_DIAGNOSES; D_ICD_PROCEDURES; D_ITEMS; and D_LABITEMS. The remaining tables contain data associated with patient care, such as physiological measurements, caregiver observations, and billing information.

The MIMIC dataset amongst other information covers the following types of information:

•Admissions
•Discharges: details of patient leaving hospital
•Transfers: records of the movement of patients betweencareunits and wards during their stay
•Caregivers: details of what type of staff cared for a patientduring their hospital stay
•Prescriptions: medication information from the hospitalcomputerized hospital order entry (CPOE) system
•Chart information: the patient’s medical chart
•Labevents: lab tests
•Diagnoses: various information on diagnoses from acrossmultiple tables
•Procedures: various information on the procedures carriedout on patients from across multiple tables
•Patients: demographic information on patients
•Patient notes: the patient notes recorded for each patien



# Preliminary results
1-2 paragraphs describing any preliminary results you have. At the very least,
this should include some basic summary statistics or exploratory data analysis results from your
dataset(s) or a pilot/preliminary dataset (if you are scraping or mining data).

# References
1. Alpha.physionet.org. (2019). MIMIC-III Clinical Database v1.4. [online] Available at: https://alpha.physionet.org/content/mimiciii/1.4/ [Accessed 29 Sep. 2019].
2. Johnson, A., Pollard, T., Shen, L., Lehman, L., Feng, M., Ghassemi, M., Moody, B., Szolovits, P., Anthony Celi, L. and Mark, R. (2019). MIMIC-III, a freely accessible critical care database.


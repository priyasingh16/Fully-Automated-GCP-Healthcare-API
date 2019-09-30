# Patient timeline representation to model EHR data.
Fully Automated GCP Healthcare API /Pipeline to model EHR Data using sequential modeling (with attention) for patient timeline representation of features(https://mimic.physionet.org/) [Plug and play based serverless GCP architecture for sequential model training and inference pipeline on EHR data]
 
# Authors
Parth Tandel, Priya Singh, Monica Mishra

# Summary
2-3 paragraphs summarizing the problem you wish to solve, including a description of the
dataset(s), and a very brief, non-technical description of your proposed methods.

A major challenge is the lack of a standard representation to store healthcare data. 
This is mainly due to no common structure, vendors using different codes for the same medication and the information of
a patient is spread across multiple tables.    
Due to this a vast majority of the patients data is discarded. 
The fast 

# Proposed plan of research
2-3 paragraphs describing in detail the methods you will use to solve
the problem. These may be processing, visualization, and statistical and machine learning methods. It
may also include the data science tools and resources you will utilize.

Fast Healthcare Interoperability Resources (FHIR) format

To standardize the data in FHIR format, we intend to explore Google’s Protocol buffer which are  Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. 

### Data description
The dataset used is MIMIC-III<sup>1</sup> (‘Medical Information Mart for Intensive Care’) which is a openly available 
dataset developed by the MIT Lab for Computational Physiology. 
This deidentified and comprehensive healthcare information is collected from over 50,000 adult patients admitted to critical care units between 2001 and 2012 at large tertiary care hospitals. 
It includes admissions, demographics, chart notes, fluid balances, vital signs, billing information, laboratory tests, medications, etc.
To deidentify the patients all the dates have been changed to future but the relative time between event has been maintained.
Since it is not a public dataset, to get access to the data, request access at this [link] (https://mimic.physionet.org/gettingstarted/access/).
![Figure 1: MIMIC-III critical care database](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fsdata.2016.35/MediaObjects/41597_2016_Article_BFsdata201635_Fig1_HTML.jpg?as=webp)
<center>Figure 1: MIMIC-III critical care database</center><sup>2</sup>


# Preliminary results
1-2 paragraphs describing any preliminary results you have. At the very least,
this should include some basic summary statistics or exploratory data analysis results from your
dataset(s) or a pilot/preliminary dataset (if you are scraping or mining data).

# References
1. Alpha.physionet.org. (2019). MIMIC-III Clinical Database v1.4. [online] Available at: https://alpha.physionet.org/content/mimiciii/1.4/ [Accessed 29 Sep. 2019].
2. Johnson, A., Pollard, T., Shen, L., Lehman, L., Feng, M., Ghassemi, M., Moody, B., Szolovits, P., Anthony Celi, L. and Mark, R. (2019). MIMIC-III, a freely accessible critical care database.
3. Rajkomar, A., Oren, E., Chen, K., Dai, A., Hajaj, N., Hardt, M., Liu, P., Liu, X., Marcus, J., Sun, M., Sundberg, P., Yee, H., Zhang, K., Zhang, Y., Flores, G., Duggan, G., Irvine, J., Le, Q., Litsch, K., Mossin, A., Tansuwan, J., Wang, D., Wexler, J., Wilson, J., Ludwig, D., Volchenboum, S., Chou, K., Pearson, M., Madabushi, S., Shah, N., Butte, A., Howell, M., Cui, C., Corrado, G. and Dean, J. (2018). Scalable and accurate deep learning with electronic health records. npj Digital Medicine, 1(1).

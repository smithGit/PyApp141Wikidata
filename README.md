# Python Access to Wikidata

![Project Logo or Screenshot](link-to-image.png) <!-- Optional: If you have a logo or screenshot, add it here -->

Welcome to the "Python Access to Wikidata" project! This repository provides Python code and
examples for accessing data from Wikidata and creating a multi-sheet Excel Workbook with the results. 

The specific query of this example is to query Wikidata for all causes of death that are COVID-19, retrieve the Occupation(s) of each individual as well as date of birth and date of death, and analyze the results. 



## Table of Contents

- [Getting Started](#getting-started)
- [App Features](#app-features)
- [Usage](#usage)
- [Interpreting Results](#interpreting-results)
- [Collaborators](#collaborators)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with the "Python Access to Wikidata" project, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python packages by running: `pip install -r requirements.txt`.
3. Explore the provided code examples and documentation to understand how to access Wikidata using Python.

## App Features

The features of this app are: 

1. Use of WikidataIntegrator, developed by SuLab at Scripps Institute,
2. Access query.wikidata.org with a SPARQL query
3. Decode the JSON results to create both a list containing all rows returned and a dictionary with each person as key, data fields returned from WD, and a dictionary of occupations held by each person,
4. use of xlswriter to create the Excel workbook with  multiple sheets:  
  1. sht_wd_covid - List of Rows returned (excluding any with no English label)
  2. Notes - notes about the workbook as well as statistics
  3. distinctPeople - row for each individual person returned
  4. distinctOccup - row for each occupation, showing total count and breakdown by age 
  5. personOccupations - for each person, a column for each occupation held showin occupation id and label.

## Usage

Here's a brief overview of how you can use this project to access Wikidata using Python:

1. Import the necessary modules: `import wikidata`
2. Use the provided functions to query and retrieve data from Wikidata.
3. Process the retrieved data for your specific use case.

For detailed usage instructions and examples, refer to the [documentation](documentation.md).

## Interpreting Results

The age ranges and codes are as follows:

- young - 21 or younger 
- adult - 22 to 35 - adult, starting a career and family 
- midlife - 36 to 50 - establshing career, supporting the family 
- senior - 51 - 65 - career established, becoming empty nester 
- socsec - 65 - 80 - Social Security age, many retire 
- old - over 80 - Few remain working, health issues become common 

## Collaborators

This application was developed in connection with the Occupation Ontology (OccO) informal workgroup consistint of:

1. Dr. Yongqun (Oliver) He, University of Michigan Medical Center
2. Dr. Jie Zheng, University of Michigan Medical Center
3. Dr. John Beverley, The New York State University at Buffalo
4. Dr. Bill Duncan, The University of Florida
5. PhD Candidate Matthew Diller, The University of Florida
6. Sam Smith, retired volunteer in Dr. He's HeLab and programmer (SmithGit)

## Contributing


Contributions are welcome! If you'd like to contribute to the project, follow these steps:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push the changes to your fork and create a pull request.
<!--
For more information, see [CONTRIBUTING.md](CONTRIBUTING.md).  -->

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code according to the terms of the license.

---

For questions, issues, or more information about this project, contact [Sam Smith](mailto:samsmith1963bc@gmail.com).

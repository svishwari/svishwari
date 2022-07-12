export default [
  {
    type: "children_under_18",
    description: "Children in Household",
    values: ["true"],
  },
  {
    type: "age",
    description: "Age",
    values: ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
  },
  {
    type: "adults_per_household",
    description: "Adults per Household",
    values: ["1", "2", "3+"],
  },
  {
    type: "gender",
    description: "Gender",
    values: ["Male", "Female", "Gender-fluid/Non-binary", "Prefer not to say"],
  },
  {
    type: "highest_level_of_education",
    description: "Highest level of education",
    values: [
      "Some High School",
      "High School Diploma",
      "Vocational Training",
      "Undergraduate Degree",
      "Graduate Degree",
      "Post-graduate Degree",
    ],
  },
  {
    type: "race_ethnicity",
    description: "Race & Ethnicity",
    values: [
      "White or Caucasian",
      "Black or African",
      "Asian",
      "American-Indian or Alaska Native",
      "Native Hawaiian or Other Pacific Islander",
      "Hispanic or Latino",
      "Other race or ethnicity",
      "Prefer not to say",
      "Multi-racial",
    ],
  },
  {
    type: "household_income",
    description: "Household Income",
    values: [
      "Less than $20K",
      "$20K-$40K",
      "$40K-$60K",
      "$60K-$80K",
      "$80K-$100K",
      "$100K-$150K",
      "$150K+",
      "Prefer not to say",
    ],
  },
]

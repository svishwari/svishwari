const audienceFilterMock = {
  rule_attributes: {
    general: {
      age: {
        max: 100,
        min: 0,
        name: "Age",
        type: "range",
      },
      email: {
        name: "Email",
        type: "text",
      },
      gender: {
        name: "Gender",
        options: [],
        type: "text",
      },
      location: {
        city: {
          name: "City",
          options: [],
          type: "text",
        },
        country: {
          name: "Country",
          options: [],
          type: "text",
        },
        name: "Location",
        state: {
          name: "State",
          options: [],
          type: "text",
        },
        zip_code: {
          name: "Zip code",
          type: "text",
        },
      },
    },
    model_scores: {
      actual_lifetime_value: {
        max: 50000,
        min: 0,
        name: "Actual lifetime value",
        steps: 1000,
        type: "range",
      },
      propensity_to_purchase: {
        max: 1,
        min: 0,
        name: "Propensity to purchase",
        steps: 0.05,
        type: "range",
      },
      propensity_to_unsubscribe: {
        max: 1,
        min: 0,
        name: "Propensity to unsubscribe",
        steps: 0.05,
        type: "range",
      },
    },
  },
  text_operators: {
    contains: "Contains",
    does_not_contain: "Does not contain",
    does_not_equal: "Does not equal",
    equals: "Equals",
  },
}
export default audienceFilterMock

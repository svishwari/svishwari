const audienceFilterMock = {
  model_scores() {
    return {
        propensity_to_unsubscribe: {
            name: "Propensity to unsubscribe",
            type: "range",
            min: 0.0,
            max: 1.0,
            steps: 0.05,
        },
        actual_lifetime_value: {
            name: "Actual lifetime value",
            type: "range",
            min: 0,
            max: 50000,
            steps: 1000,
        },
        propensity_to_purchase: {
            name: "Propensity to purchase",
            type: "range",
            min: 0.0,
            max: 1.0,
            steps: 0.05,
        },
    }
  },
  general() {
    return {
        age: {
            name: "Age",
            type: "range",
            min: 0,
            max: 100,
            steps: 1,
        },
        email: { 
            name: "Email", 
            type: "text" 
        },
        gender: {
            name: "Gender",
            type: "text",
            options: [],
        },
        location: {
            name: "Location",
            country: {
                name: "Country",
                type: "text",
                options: [],
            },
            state: {
                name: "State",
                type: "text",
                options: [],
            },
            city: {
                name: "City",
                type: "text",
                options: [],
            },
            zip_code: { 
                name: "Zip code", 
                type: "text" 
            },
        },
    }
  },
}
export default audienceFilterMock

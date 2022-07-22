const attributeRules = {
  text_operators: {
    contains: "Contains",
    not_contains: "Does not contain",
    equals: "Equals",
    not_equals: "Does not equal",
    within_the_last: "Within the last",
    not_within_the_last: "Not within the last",
    between: "Between",
    value: "Value",
    decile_percentage: "Decile percentage",
  },
  rule_attributes: {
    model_scores: {
      propensity_to_unsubscribe: {
        name: "Propensity to unsubscribe",
        type: "range",
      },
      ltv_predicted: {
        name: "Predicted lifetime value",
        type: "range",
      },
      propensity_to_purchase: {
        name: "Propensity to purchase",
        type: "range",
      },
    },
    general: {
      age: {
        name: "Age",
        type: "range",
      },
      contact_preference: {
        name: "Contact preference",
        type: "list",
        options: [
          {
            email: "Email",
          },
          {
            text: "Text",
          },
        ],
      },
      email: {
        name: "Email",
        type: "list",
        options: [
          {
            "fake.com": "fake.com",
          },
        ],
      },
      gender: {
        name: "Gender",
        type: "list",
        options: [
          {
            female: "Female",
          },
          {
            male: "Male",
          },
          {
            other: "Other",
          },
        ],
      },
      location: {
        name: "Location",
        country: {
          name: "Country",
          type: "list",
          options: [
            {
              US: "US",
            },
          ],
        },
        state: {
          name: "State",
          type: "list",
          options: [
            {
              AL: "Alabama",
            },
            {
              AK: "Alaska",
            },
            {
              AZ: "Arizona",
            },
            {
              AR: "Arkansas",
            },
            {
              CA: "California",
            },
            {
              CO: "Colorado",
            },
            {
              CT: "Connecticut",
            },
            {
              DE: "Delaware",
            },
            {
              DC: "District of Columbia",
            },
            {
              FL: "Florida",
            },
            {
              GA: "Georgia",
            },
            {
              HI: "Hawaii",
            },
            {
              ID: "Idaho",
            },
            {
              IL: "Illinois",
            },
            {
              IN: "Indiana",
            },
            {
              IA: "Iowa",
            },
            {
              KS: "Kansas",
            },
            {
              KY: "Kentucky",
            },
            {
              LA: "Louisiana",
            },
            {
              ME: "Maine",
            },
            {
              MD: "Maryland",
            },
            {
              MA: "Massachusetts",
            },
            {
              MI: "Michigan",
            },
            {
              MN: "Minnesota",
            },
            {
              MS: "Mississippi",
            },
            {
              MO: "Missouri",
            },
            {
              MT: "Montana",
            },
            {
              NE: "Nebraska",
            },
            {
              NV: "Nevada",
            },
            {
              NH: "New Hampshire",
            },
            {
              NJ: "New Jersey",
            },
            {
              NM: "New Mexico",
            },
            {
              NY: "New York",
            },
            {
              NC: "North Carolina",
            },
            {
              ND: "North Dakota",
            },
            {
              OH: "Ohio",
            },
            {
              OK: "Oklahoma",
            },
            {
              OR: "Oregon",
            },
            {
              PA: "Pennsylvania",
            },
            {
              RI: "Rhode Island",
            },
            {
              SC: "South Carolina",
            },
            {
              SD: "South Dakota",
            },
            {
              TN: "Tennessee",
            },
            {
              TX: "Texas",
            },
            {
              UT: "Utah",
            },
            {
              VT: "Vermont",
            },
            {
              VA: "Virginia",
            },
            {
              WA: "Washington",
            },
            {
              WV: "West Virginia",
            },
            {
              WI: "Wisconsin",
            },
            {
              WY: "Wyoming",
            },
            {
              PR: "Puerto Rico",
            },
          ],
        },
        city: {
          name: "City",
          type: "list",
          options: [],
        },
        zip_code: {
          name: "Zip",
          type: "list",
          options: [],
        },
      },
      mailing_address: {
        name: "Mailing address",
        mailing_country: {
          name: "Country",
          type: "list",
          options: [
            {
              US: "US",
            },
          ],
        },
        mailing_state: {
          name: "State",
          type: "list",
          options: [
            {
              AL: "Alabama",
            },
            {
              AK: "Alaska",
            },
            {
              AZ: "Arizona",
            },
            {
              AR: "Arkansas",
            },
            {
              CA: "California",
            },
            {
              CO: "Colorado",
            },
            {
              CT: "Connecticut",
            },
            {
              DE: "Delaware",
            },
            {
              DC: "District of Columbia",
            },
            {
              FL: "Florida",
            },
            {
              GA: "Georgia",
            },
            {
              HI: "Hawaii",
            },
            {
              ID: "Idaho",
            },
            {
              IL: "Illinois",
            },
            {
              IN: "Indiana",
            },
            {
              IA: "Iowa",
            },
            {
              KS: "Kansas",
            },
            {
              KY: "Kentucky",
            },
            {
              LA: "Louisiana",
            },
            {
              ME: "Maine",
            },
            {
              MD: "Maryland",
            },
            {
              MA: "Massachusetts",
            },
            {
              MI: "Michigan",
            },
            {
              MN: "Minnesota",
            },
            {
              MS: "Mississippi",
            },
            {
              MO: "Missouri",
            },
            {
              MT: "Montana",
            },
            {
              NE: "Nebraska",
            },
            {
              NV: "Nevada",
            },
            {
              NH: "New Hampshire",
            },
            {
              NJ: "New Jersey",
            },
            {
              NM: "New Mexico",
            },
            {
              NY: "New York",
            },
            {
              NC: "North Carolina",
            },
            {
              ND: "North Dakota",
            },
            {
              OH: "Ohio",
            },
            {
              OK: "Oklahoma",
            },
            {
              OR: "Oregon",
            },
            {
              PA: "Pennsylvania",
            },
            {
              RI: "Rhode Island",
            },
            {
              SC: "South Carolina",
            },
            {
              SD: "South Dakota",
            },
            {
              TN: "Tennessee",
            },
            {
              TX: "Texas",
            },
            {
              UT: "Utah",
            },
            {
              VT: "Vermont",
            },
            {
              VA: "Virginia",
            },
            {
              WA: "Washington",
            },
            {
              WV: "West Virginia",
            },
            {
              WI: "Wisconsin",
            },
            {
              WY: "Wyoming",
            },
            {
              PR: "Puerto Rico",
            },
          ],
        },
        mailing_city: {
          name: "City",
          type: "list",
          options: [],
        },
        mailing_zip_code: {
          name: "Zip",
          type: "list",
          options: [],
        },
      },
      shipping_address: {
        name: "Shipping address",
        shipping_country: {
          name: "Country",
          type: "list",
          options: [
            {
              US: "US",
            },
          ],
        },
        shipping_state: {
          name: "State",
          type: "list",
          options: [
            {
              AL: "Alabama",
            },
            {
              AK: "Alaska",
            },
            {
              AZ: "Arizona",
            },
            {
              AR: "Arkansas",
            },
            {
              CA: "California",
            },
            {
              CO: "Colorado",
            },
            {
              CT: "Connecticut",
            },
            {
              DE: "Delaware",
            },
            {
              DC: "District of Columbia",
            },
            {
              FL: "Florida",
            },
            {
              GA: "Georgia",
            },
            {
              HI: "Hawaii",
            },
            {
              ID: "Idaho",
            },
            {
              IL: "Illinois",
            },
            {
              IN: "Indiana",
            },
            {
              IA: "Iowa",
            },
            {
              KS: "Kansas",
            },
            {
              KY: "Kentucky",
            },
            {
              LA: "Louisiana",
            },
            {
              ME: "Maine",
            },
            {
              MD: "Maryland",
            },
            {
              MA: "Massachusetts",
            },
            {
              MI: "Michigan",
            },
            {
              MN: "Minnesota",
            },
            {
              MS: "Mississippi",
            },
            {
              MO: "Missouri",
            },
            {
              MT: "Montana",
            },
            {
              NE: "Nebraska",
            },
            {
              NV: "Nevada",
            },
            {
              NH: "New Hampshire",
            },
            {
              NJ: "New Jersey",
            },
            {
              NM: "New Mexico",
            },
            {
              NY: "New York",
            },
            {
              NC: "North Carolina",
            },
            {
              ND: "North Dakota",
            },
            {
              OH: "Ohio",
            },
            {
              OK: "Oklahoma",
            },
            {
              OR: "Oregon",
            },
            {
              PA: "Pennsylvania",
            },
            {
              RI: "Rhode Island",
            },
            {
              SC: "South Carolina",
            },
            {
              SD: "South Dakota",
            },
            {
              TN: "Tennessee",
            },
            {
              TX: "Texas",
            },
            {
              UT: "Utah",
            },
            {
              VT: "Vermont",
            },
            {
              VA: "Virginia",
            },
            {
              WA: "Washington",
            },
            {
              WV: "West Virginia",
            },
            {
              WI: "Wisconsin",
            },
            {
              WY: "Wyoming",
            },
            {
              PR: "Puerto Rico",
            },
          ],
        },
        shipping_city: {
          name: "City",
          type: "list",
          options: [],
        },
        shipping_zip_code: {
          name: "Zip",
          type: "list",
          options: [],
        },
      },
      events: {
        name: "Events",
        viewed_checkout: {
          name: "Viewed checkout",
          type: "text",
        },
        traits_analysed: {
          name: "Trait",
          type: "text",
        },
        sales_made: {
          name: "Sale",
          type: "text",
        },
        content_viewed: {
          name: "View Content",
          type: "text",
        },
        purchases_made: {
          name: "Purchase",
          type: "text",
        },
        abandoned_carts: {
          name: "Abandoned cart",
          type: "text",
        },
        products_searched: {
          name: "Product Search",
          type: "text",
        },
      },
    },
  },
}
export default attributeRules

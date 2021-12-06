const defaultAudience = {
  id: 1,
  name: "My Audience",
  destinations: [],
  engagements: [],
  filters: [
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "filter_field",
          type: "type",
          value: "value",
        },
      ],
    },
  ],
}

const multipleSectionFiltersAudience = {
  audience_insights: {
    total_customers: 121321321,
    total_countries: 2,
    total_us_states: 28,
    total_cities: 246,
    min_age: 34,
    max_age: 100,
    gender_women: 0.4651031,
    gender_men: 0.481924,
    gender_other: 0.25219,
  },
  destinations: [],
  filters: [
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "propensity_to_unsubscribe",
          type: "range",
          value: [0.3, 0.5],
        },
        {
          field: "age",
          type: "range",
          value: [18, 30],
        },
        {
          field: "gender",
          type: "equals",
          value: "female",
        },
      ],
    },
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "propensity_to_purchase",
          type: "range",
          value: [0.55, 0.75],
        },
        {
          field: "age",
          type: "range",
          value: [30, 60],
        },
        {
          field: "gender",
          type: "equals",
          value: "male",
        },
      ],
    },
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "ltv_predicted",
          type: "range",
          value: [250, 460],
        },
        {
          field: "City",
          type: "equals",
          value: "River Forest",
        },
        {
          field: "Zip",
          type: "equals",
          value: "19129",
        },
      ],
    },
  ],
  name: "Audience with multiple filters",
  size: 3022188,
}

const lookalikeAbleAudience1 = {
  updated_by: "Rahul Goel",
  created_by: "Rahul Goel",
  is_lookalike: true,
  audience_insights: {
    total_customers: 121321321,
    total_countries: 2,
    total_us_states: 28,
    total_cities: 246,
    min_age: 34,
    max_age: 100,
    gender_women: 0.4651031,
    gender_men: 0.481924,
    gender_other: 0.25219,
  },
  destinations: [],
  source_exists: true,
  filters: [
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "propensity_to_unsubscribe",
          type: "range",
          value: [0.7, 1],
        },
      ],
    },
  ],
  name: "Customers likely to unsubscribe",
  last_delivered: "2019-04-28T06:39:31.659551",
  create_time: "2021-06-24T18:44:00.381000",
  size: 3022188,
  id: "60d4d270d364622dd6cc9a7",
  update_time: "2021-06-24T18:44:00.381000",
}

const lookalikeAbleAudience2 = {
  updated_by: "Mohit Bansal",
  created_by: "Mohit Bansal",
  is_lookalike: true,
  audience_insights: {
    total_customers: 121321321,
    total_countries: 2,
    total_us_states: 28,
    total_cities: 246,
    min_age: 34,
    max_age: 100,
    gender_women: 0.4651031,
    gender_men: 0.481924,
    gender_other: 0.25219,
  },
  destinations: [],
  source_exists: false,
  filters: [
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "propensity_to_unsubscribe",
          type: "range",
          value: [0.7, 1],
        },
      ],
    },
  ],
  name: "Customers likely to subscribe",
  last_delivered: "2019-04-28T06:39:31.659551",
  create_time: "2021-06-24T18:44:00.381000",
  size: 3022188,
  id: "60d4d270d364622dd6cc9b7",
  update_time: "2021-06-24T18:44:00.381000",
}

export default [
  defaultAudience,
  multipleSectionFiltersAudience,
  lookalikeAbleAudience1,
  lookalikeAbleAudience2,
]

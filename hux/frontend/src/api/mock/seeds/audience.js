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
          field: "gender",
          type: "equals",
          value: "female",
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "viewed_checkout",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-27", "2022-06-28"],
            },
          ],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "abandoned_carts",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-17", "2022-06-28"],
            },
          ],
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
          field: "gender",
          type: "equals",
          value: "female",
        },
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
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "viewed_checkout",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-27", "2022-06-28"],
            },
          ],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "abandoned_carts",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-17", "2022-06-28"],
            },
          ],
        },
      ],
    },
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "gender",
          type: "equals",
          value: "female",
        },
        {
          field: "age",
          type: "range",
          value: [30, 60],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "viewed_checkout",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-27", "2022-06-28"],
            },
          ],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "abandoned_carts",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-17", "2022-06-28"],
            },
          ],
        },
      ],
    },
    {
      section_aggregator: "ALL",
      section_filters: [
        {
          field: "gender",
          type: "equals",
          value: "female",
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
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "viewed_checkout",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-27", "2022-06-28"],
            },
          ],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "abandoned_carts",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-17", "2022-06-28"],
            },
          ],
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
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "viewed_checkout",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-27", "2022-06-28"],
            },
          ],
        },
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "abandoned_carts",
            },
            {
              field: "created",
              type: "range",
              value: ["2022-06-17", "2022-06-28"],
            },
          ],
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
  audience_size_percentage: 1.5,
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
        {
          field: "event",
          type: "event",
          value: [
            {
              field: "event_name",
              type: "equals",
              value: "traits_analysed",
            },
            {
              field: "created",
              type: "range",
              value: ["2020-09-25", "2022-05-18"],
            },
          ],
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
  audience_size_percentage: 1.5,
}

export default [
  defaultAudience,
  multipleSectionFiltersAudience,
  lookalikeAbleAudience1,
  lookalikeAbleAudience2,
]

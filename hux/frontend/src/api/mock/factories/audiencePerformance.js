import faker from "faker"

const audiencePerformanceMock = {
  displayads_audience_performance: {
    summary() {
      return {
        spend: faker.datatype.number({ min: 100000, max: 99999 }),
        reach: faker.datatype.number({ min: 100000, max: 99999 }),
        impressions: faker.datatype.number({ min: 100000, max: 99999 }),
        conversions: faker.datatype.number({ min: 100000, max: 99999 }),
        clicks: faker.datatype.number({ min: 100000, max: 99999 }),
        frequency: faker.datatype.number({ min: 100, max: 999 }),
        cost_per_thousand_impressions: faker.finance.amount(50, 100, 3),
        click_through_rate: faker.datatype.number({ min: 20, max: 100 }),
        cost_per_action: faker.datatype.number({ min: 100, max: 999 }),
        cost_per_click: faker.datatype.number({ min: 100, max: 999 }),
        engagement_rate: faker.finance.amount(50, 100, 3),
      }
    },
    audience_performance() {
      let array = []
      let limit = faker.datatype.number({ min: 5, max: 10 })
      for (let i = 0; i < limit; i++) {
        let fake = {
          name: `Audience ${i + 1}`,
          spend: faker.datatype.number({ min: 100000, max: 99999 }),
          reach: faker.datatype.number({ min: 100000, max: 99999 }),
          impressions: faker.datatype.number({ min: 100000, max: 99999 }),
          conversions: faker.datatype.number({ min: 100000, max: 99999 }),
          clicks: faker.datatype.number({ min: 100000, max: 99999 }),
          frequency: faker.datatype.number({ min: 100, max: 999 }),
          cost_per_thousand_impressions: faker.finance.amount(50, 100, 3),
          click_through_rate: faker.datatype.number({ min: 20, max: 100 }),
          cost_per_action: faker.datatype.number({ min: 100, max: 999 }),
          cost_per_click: faker.datatype.number({ min: 100, max: 999 }),
          engagement_rate: faker.finance.amount(50, 100, 3),
        }
        fake["campaigns"] = (() => {
          let campaignArray = []
          let limit = faker.datatype.number({ min: 2, max: 3 })
          for (let i = 0; i < limit; i++) {
            let fakeCampaign = {
              name: faker.random.arrayElement([
                "Facebook",
                "Salesforce Marketing Cloud",
                "Google-Ads",
              ]),
              is_mapped: true,
              spend: faker.datatype.number({ min: 100000, max: 99999 }),
              reach: faker.datatype.number({ min: 100000, max: 99999 }),
              impressions: faker.datatype.number({
                min: 100000,
                max: 99999,
              }),
              conversions: faker.datatype.number({
                min: 100000,
                max: 99999,
              }),
              clicks: faker.datatype.number({ min: 100000, max: 99999 }),
              frequency: faker.datatype.number({ min: 100, max: 999 }),
              cost_per_thousand_impressions: faker.finance.amount(50, 100, 3),
              click_through_rate: faker.datatype.number({
                min: 20,
                max: 100,
              }),
              cost_per_action: faker.datatype.number({
                min: 100,
                max: 999,
              }),
              cost_per_click: faker.datatype.number({ min: 100, max: 999 }),
              engagement_rate: faker.finance.amount(50, 100, 3),
            }
            campaignArray.push(fakeCampaign)
          }
          return campaignArray
        })()
        array.push(fake)
      }
      return array
    },
  },
  email_audience_performance: {
    summary() {
      {
        return {
          sent: faker.datatype.number({ min: 100000, max: 99999 }),
          hard_bounces: faker.datatype.number({ min: 100, max: 999 }),
          hard_bounces_rate: faker.finance.amount(0, 1, 2),
          delivered: faker.datatype.number({ min: 100, max: 999 }),
          delivered_rate: faker.finance.amount(0, 1, 2),
          open: faker.datatype.number({ min: 100000, max: 99999 }),
          open_rate: faker.finance.amount(0, 1, 2),
          clicks: faker.datatype.number({ min: 100000, max: 99999 }),
          click_through_rate: faker.finance.amount(0, 1, 2),
          click_to_open_rate: faker.finance.amount(0, 1, 2),
          unique_clicks: faker.datatype.number({ min: 100000, max: 99999 }),
          unique_opens: faker.datatype.number({ min: 100000, max: 99999 }),
          unsubscribe: faker.datatype.number({ min: 100000, max: 99999 }),
          unsubscribe_rate: faker.finance.amount(0, 1, 2),
        }
      }
    },
    audience_performance() {
      let array = []
      let limit = faker.datatype.number({ min: 5, max: 10 })
      for (let i = 0; i < limit; i++) {
        let fake = {
          name: `Audience ${i + 1}`,
          sent: faker.datatype.number({ min: 100000, max: 99999 }),
          hard_bounces: faker.datatype.number({ min: 100, max: 999 }),
          hard_bounces_rate: faker.finance.amount(0, 1, 2),
          delivered: faker.datatype.number({ min: 100, max: 999 }),
          delivered_rate: faker.finance.amount(0, 1, 2),
          open: faker.datatype.number({ min: 100000, max: 99999 }),
          open_rate: faker.finance.amount(0, 1, 2),
          clicks: faker.datatype.number({ min: 100000, max: 99999 }),
          click_through_rate: faker.finance.amount(0, 1, 2),
          click_to_open_rate: faker.finance.amount(0, 1, 2),
          unique_clicks: faker.datatype.number({ min: 100000, max: 99999 }),
          unique_opens: faker.datatype.number({ min: 100000, max: 99999 }),
          unsubscribe: faker.datatype.number({ min: 100000, max: 99999 }),
          unsubscribe_rate: faker.finance.amount(0, 1, 2),
        }
        fake["campaigns"] = (() => {
          let campaignArray = []
          let limit = faker.datatype.number({ min: 2, max: 3 })
          for (let i = 0; i < limit; i++) {
            let fakeCampaign = {
              name: faker.random.arrayElement([
                "Facebook",
                "Salesforce Marketing Cloud",
                "Google-Ads",
              ]),
              is_mapped: true,
              sent: faker.datatype.number({ min: 100000, max: 99999 }),
              hard_bounces: faker.datatype.number({ min: 100, max: 999 }),
              hard_bounces_rate: faker.finance.amount(0, 1, 2),
              delivered: faker.datatype.number({ min: 100, max: 999 }),
              delivered_rate: faker.finance.amount(0, 1, 2),
              open: faker.datatype.number({ min: 100000, max: 99999 }),
              open_rate: faker.finance.amount(0, 1, 2),
              clicks: faker.datatype.number({ min: 100000, max: 99999 }),
              click_through_rate: faker.finance.amount(0, 1, 2),
              click_to_open_rate: faker.finance.amount(0, 1, 2),
              unique_clicks: faker.datatype.number({ min: 100000, max: 99999 }),
              unique_opens: faker.datatype.number({ min: 100000, max: 99999 }),
              unsubscribe: faker.datatype.number({ min: 100000, max: 99999 }),
              unsubscribe_rate: faker.finance.amount({ min: 0, max: 1 }),
            }
            campaignArray.push(fakeCampaign)
          }
          return campaignArray
        })()
        array.push(fake)
      }
      return array
    },
  },
}
export default audiencePerformanceMock

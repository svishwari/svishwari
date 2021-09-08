import faker from "faker"
const hasAdsData = Boolean(faker.datatype.number(1))
const audiencePerformanceMock = {
  displayads_audience_performance: {
    summary() {
      if (hasAdsData) {
        return {
          spend: faker.datatype.number({ min: 0, max: 99999 }),
          reach: faker.datatype.number({ min: 0, max: 99999 }),
          impressions: faker.datatype.number({ min: 0, max: 99999 }),
          conversions: faker.datatype.number({ min: 0, max: 99999 }),
          clicks: faker.datatype.number({ min: 0, max: 99999 }),
          frequency: faker.datatype.number({ min: 0, max: 999 }),
          cost_per_thousand_impressions: faker.finance.amount(0, 100, 3),
          click_through_rate: faker.datatype.number({ min: 0, max: 100 }),
          cost_per_action: faker.datatype.number({ min: 0, max: 999 }),
          cost_per_click: faker.datatype.number({ min: 0, max: 999 }),
          engagement_rate: faker.finance.amount(0, 100, 3) / 100,
        }
      } else {
        return {
          spend: 0,
          reach: 0,
          impressions: 0,
          conversions: 0,
          clicks: 0,
          frequency: 0,
          cost_per_thousand_impressions: 0,
          click_through_rate: 0,
          cost_per_action: 0,
          cost_per_click: 0,
          engagement_rate: 0,
        }
      }
    },
    audience_performance() {
      let array = []
      let limit = hasAdsData ? faker.datatype.number({ min: 2, max: 5 }) : 0
      if (limit === 0) {
        array = []
      }
      for (let i = 0; i < limit; i++) {
        let fake = {
          id: faker.datatype.uuid().replace(/-/g, ""),
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
          engagement_rate: faker.finance.amount(1, 100, 3) / 100,
        }
        fake["destinations"] = (() => {
          let destinationArray = []
          let limit = faker.datatype.number({ min: 1, max: 1 })
          for (let i = 0; i < limit; i++) {
            const name = faker.random.arrayElement(["Facebook"])
            const is_mapped =
              name === "Facebook" ? !Math.round(Math.random()) : true
            let fakeDestinationRollup = {
              id: faker.datatype.uuid().replace(/-/g, ""),
              name: name,
              is_mapped: is_mapped,
              spend: is_mapped
                ? faker.datatype.number({
                    min: 100000,
                    max: 99999,
                  })
                : 0,
              reach: is_mapped
                ? faker.datatype.number({ min: 100000, max: 99999 })
                : 0,
              impressions: is_mapped
                ? faker.datatype.number({
                    min: 100000,
                    max: 99999,
                  })
                : 0,
              conversions: is_mapped
                ? faker.datatype.number({
                    min: 100000,
                    max: 99999,
                  })
                : 0,
              clicks: is_mapped
                ? faker.datatype.number({ min: 100000, max: 99999 })
                : 0,
              frequency: is_mapped
                ? faker.datatype.number({ min: 100, max: 999 })
                : 0,
              cost_per_thousand_impressions: is_mapped
                ? faker.finance.amount(50, 100, 3)
                : 0,
              click_through_rate: is_mapped
                ? faker.datatype.number({
                    min: 20,
                    max: 100,
                  })
                : 0,
              cost_per_action: is_mapped
                ? faker.datatype.number({
                    min: 100,
                    max: 999,
                  })
                : 0,
              cost_per_click: is_mapped
                ? faker.datatype.number({ min: 100, max: 999 })
                : 0,
              engagement_rate: is_mapped
                ? faker.finance.amount(1, 100, 3) / 100
                : 0,
            }
            if (!is_mapped) fakeDestinationRollup["campaigns"] = []
            destinationArray.push(fakeDestinationRollup)
          }
          return destinationArray
        })()
        array.push(fake)
      }
      return array
    },
  },
  email_audience_performance: {
    summary() {
      {
        if (hasAdsData) {
          return {
            sent: faker.datatype.number({ min: 0, max: 99999 }),
            hard_bounces: faker.datatype.number({ min: 0, max: 999 }),
            hard_bounces_rate: faker.finance.amount(0, 100, 2) / 100,
            delivered: faker.datatype.number({ min: 0, max: 999 }),
            delivered_rate: faker.finance.amount(0, 100, 2) / 100,
            open: faker.datatype.number({ min: 0, max: 99999 }),
            open_rate: faker.finance.amount(0, 100, 2) / 100,
            clicks: faker.datatype.number({ min: 0, max: 99999 }),
            click_through_rate: faker.finance.amount(0, 100, 2) / 100,
            click_to_open_rate: faker.finance.amount(0, 100, 2) / 100,
            unique_clicks: faker.datatype.number({ min: 0, max: 99999 }),
            unique_opens: faker.datatype.number({ min: 0, max: 99999 }),
            unsubscribe: faker.datatype.number({ min: 0, max: 99999 }),
            unsubscribe_rate: faker.finance.amount(0, 100, 2) / 100,
          }
        } else {
          return {
            sent: 0,
            hard_bounces: 0,
            hard_bounces_rate: 0,
            delivered: 0,
            delivered_rate: 0,
            open: 0,
            open_rate: 0,
            clicks: 0,
            click_through_rate: 0,
            click_to_open_rate: 0,
            unique_clicks: 0,
            unique_opens: 0,
            unsubscribe: 0,
            unsubscribe_rate: 0,
          }
        }
      }
    },
    audience_performance() {
      let array = []
      let limit = hasAdsData ? faker.datatype.number({ min: 2, max: 5 }) : 0
      if (limit === 0) {
        array = [
          {
            id: "1",
            name: "Audience 1",
            sent: 0,
            hard_bounces: 0,
            hard_bounces_rate: 0.0,
            delivered: 0,
            delivered_rate: 0.0,
            open: 0,
            open_rate: 0.0,
            clicks: 0,
            click_through_rate: 0.0,
            click_to_open_rate: 0.0,
            unique_clicks: 0,
            unique_opens: 0,
            unsubscribe: 0,
            unsubscribe_rate: 0.0,
            destinations: [],
          },
        ]
      } else {
        for (let i = 0; i < limit; i++) {
          let fake = {
            name: `Audience ${i + 1}`,
            sent: faker.datatype.number({ min: 100000, max: 99999 }),
            hard_bounces: faker.datatype.number({ min: 100, max: 999 }),
            hard_bounces_rate: faker.finance.amount(1, 100, 2) / 100,
            delivered: faker.datatype.number({ min: 100, max: 999 }),
            delivered_rate: faker.finance.amount(1, 100, 2) / 100,
            open: faker.datatype.number({ min: 100000, max: 99999 }),
            open_rate: faker.finance.amount(1, 100, 2) / 100,
            clicks: faker.datatype.number({ min: 100000, max: 99999 }),
            click_through_rate: faker.finance.amount(1, 100, 2) / 100,
            click_to_open_rate: faker.finance.amount(1, 100, 2) / 100,
            unique_clicks: faker.datatype.number({ min: 100000, max: 99999 }),
            unique_opens: faker.datatype.number({ min: 100000, max: 99999 }),
            unsubscribe: faker.datatype.number({ min: 100000, max: 99999 }),
            unsubscribe_rate: faker.finance.amount(1, 100, 2) / 100,
          }
          fake["destinations"] = (() => {
            let destinationsArray = []
            let limit = faker.datatype.number({ min: 1, max: 1 })
            for (let i = 0; i < limit; i++) {
              let fakeDestinationRollup = {
                name: faker.random.arrayElement(["Salesforce Marketing Cloud"]),
                sent: faker.datatype.number({ min: 100000, max: 99999 }),
                hard_bounces: faker.datatype.number({ min: 100, max: 999 }),
                hard_bounces_rate: faker.finance.amount(1, 100, 2) / 100,
                delivered: faker.datatype.number({ min: 100, max: 999 }),
                delivered_rate: faker.finance.amount(1, 100, 2) / 100,
                open: faker.datatype.number({ min: 100000, max: 99999 }),
                open_rate: faker.finance.amount(1, 100, 2) / 100,
                clicks: faker.datatype.number({ min: 100000, max: 99999 }),
                click_through_rate: faker.finance.amount(1, 100, 2) / 100,
                click_to_open_rate: faker.finance.amount(1, 100, 2) / 100,
                unique_clicks: faker.datatype.number({
                  min: 100000,
                  max: 99999,
                }),
                unique_opens: faker.datatype.number({
                  min: 100000,
                  max: 99999,
                }),
                unsubscribe: faker.datatype.number({ min: 100000, max: 99999 }),
                unsubscribe_rate: faker.finance.amount({ min: 0, max: 1 }),
              }
              destinationsArray.push(fakeDestinationRollup)
            }
            return destinationsArray
          })()
          array.push(fake)
        }
      }
      return array
    },
  },
}
export default audiencePerformanceMock

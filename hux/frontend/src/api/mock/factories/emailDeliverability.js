import faker from "faker"
import chartData from "@/api/mock/fixtures/deliveredCountData.js"

export const emailDeliverabilityOveriew = {
    overall_inbox_rate: faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 }),
    interval: "Daily",
    sending_domains_overview: [
        {
            domain_name: faker.random.arrayElement(["gmail", "outlook"]),
            open_rate: faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 }),
            bounce_rate: faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 }),
            sent: 30,
            click_rate: faker.datatype.float({ min: 0, max: 1, precision: 0.000000001 }),
        }
    ],
    delivered_open_rate_overview: chartData.delivered_open_rate_overivew
}




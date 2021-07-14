import faker from "faker"

export default {
  campaigns: (() => {
    let campaigns = []
    let limit = faker.datatype.number({ min: 3, max: 3 })
    for (let i = 0; i < limit; i++) {
      let _campaign = {
        id: () => faker.datatype.uuid().replace(/-/g, ""),
        name: () => `Campaign ${i + 1}`,
        delivery_job_id: () => faker.datatype.uuid().replace(/-/g, ""),
        create_time: () => faker.date.recent(),
      }
      campaigns.push(_campaign)
    }
    return campaigns
  })(),
  delivery_jobs: (() => {
    let jobs = []
    let limit = faker.datatype.number({ min: 3, max: 3 })
    for (let i = 0; i < limit; i++) {
      let _job = {
        id: () => faker.datatype.uuid().replace(/-/g, ""),
        create_time: () => faker.date.recent(),
      }
      jobs.push(_job)
    }
    return jobs
  })(),
}

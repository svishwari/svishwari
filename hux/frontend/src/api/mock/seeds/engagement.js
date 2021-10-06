import defaultAudience from "./audience"

const defaultEngagement = {
  name: "Default engagement",
  description: null,
  delivery_schedule: null,
  status: "Delivered",
  audiences: [
    {
      id: defaultAudience.id,
      name: defaultAudience.name,
      size: defaultAudience.size,
      create_time: defaultAudience.create_time,
      created_by: defaultAudience.created_by,
      update_time: defaultAudience.update_time,
      updated_by: defaultAudience.updated_by,
      status: "Delivered",
      destinations: [
        {
          id: 1,
          latest_delivery: {
            status: "Not Delivered",
            size: 1000,
          },
        },
      ],
    },
  ],
}

const sampleEngagement = {
  create_time: "2021-07-15T19:13:26.281Z",
  update_time: "2021-07-15T19:13:26.281Z",
  audiences: [
    {
      id: "2",
      destinations: [
        {
          latest_delivery: {
            status: "Not Delivered",
            size: 1000,
          },
        },
      ],
      status: "Not Delivered",
    },
  ],
  id: "60f088d6c297e84b3a9e7514",
  created_by: "Rahul Goel",
  updated_by: "",
  status: "Not Delivered",
  description: "Pre-Demo Test Engagement",
  name: "Pre-Demo Test Engagement",
}

export default [defaultEngagement, sampleEngagement]
